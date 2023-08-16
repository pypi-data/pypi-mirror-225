
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, BatchNorm2d, Dropout, AdaptiveAvgPool2d, LazyConv2d, AlphaDropout, Bilinear
from torch.nn import BatchNorm1d, BatchNorm2d, GroupNorm, LazyLinear, LazyBatchNorm1d, LogSoftmax
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU, Tanh
from torch import flatten, unsqueeze

import torch

torch.manual_seed(43)

#------------------------------
from .ResBlock import ResBlock
from .UtilityBlocks import FastGlobalAvgPool2d, SpaceToDepth
from .ClassifierNet import ClassifierNet
#------------------------------

def make_layers(args, init_channels, ds_ver):

    stages = args.pop(0)

    res_stages = []

    for s, stage in enumerate(stages):
        for l in range(stage):

            if l == 0 and s != 0:
                downsample = ds_ver
            else:
                downsample = False
            
            channels = init_channels * (2 ** s)

            block = ResBlock((channels, args, downsample))
            
            res_stages.append(block)

    return Sequential(*res_stages)

class Resnet(Module):
    def __init__(self, variant, flavor, ratio, init_channels, r, ds_ver):

        """
        Accepted Variants:
        18 : [2, 2, 2, 2] -- Vanilla Block
        34 : [3, 4, 6, 3] -- Vanilla Block
        50 : [3, 4, 6, 3] -- Bottleneck Block
        101 : [3, 4, 6, 3] -- Bottleneck Block
        152 : [3, 4, 6, 3] -- Bottleneck Block

        Accepted Augments:
        None : No Augmenting
        V1 : Augmented data goes through shallow NN first, outputting a single digit ## DEPRECATED ##

        V1_A : Only Augment 1 ## DEPRECATED ##
        V1_B : Only Augment 2 ## DEPRECATED ##


        V2 : Augmented is concated directly with original data ## DEPRECATED ##

        
        V3 : Augmented data is SE'd then chosen     by a NN to directly augment original wafer ## DEPRECATED ##
        V3-Kai   : Combines V3 and V1 together ## DEPRECATED ##
        V3-Kai A : Only Augment 1 ## DEPRECATED ## 
        V4-Kai B : Only Augment 2 ## DEPRECATED ##

        V4 
       
        """

        attention = ['mscam', 'esam']

        variants = {

            '18' : [[2, 2, 2, 2], 'basic', attention, ratio],
            '34' : [[3, 4, 6, 3], 'basic', attention, ratio],

            'radon' : [r, flavor, attention, ratio],

            # '25_v2' : [[2, 4, 6, 2], 'bottleneck'],
            # 'custom' : [[2, 2, 2, 3], 'vanilla'],

            # '18'  : [[2, 2, 2, 2], 'vanilla'],
            # '34'  : [[3, 4, 6, 3], 'vanilla'],

            # '50'  : [[3 ,4, 6, 3], 'bottleneck'],
            # '101' : [[3 ,4, 23, 3], 'bottleneck'], 
            # '152' : [[3, 8, 36, 3], 'bottleneck'],
        }

        super(Resnet, self).__init__()

        if flavor == 'basic':
            channels = init_channels
        elif flavor == 'bottleneck':
            channels = init_channels * 4

        #---------------------------------------------------------------------------------- HEAD

        self.Head = Sequential(

            SpaceToDepth(),

            Conv2d(16, init_channels, 3, 1, 1, bias = False),
            BatchNorm2d(init_channels),
            Mish(inplace = True),
        )

        self.RadonHead = Sequential(

            Conv2d(1, channels, 3, 1, 1, bias = False),
            BatchNorm2d(channels),
            Mish(inplace = True),
        )

        #---------------------------------------------------------------------------------- HEAD

        #---------------------------------------------------------------------------------- RESBLOCKS

        self.ResBlocks = make_layers(variants[variant], init_channels, ds_ver)

        #---------------------------------------------------------------------------------- RESBLOCKS

        #---------------------------------------------------------------------------------- EXTRA FEATURES

        #-------------------------------------------------------------- RESBLOCKS

        self.RadonResBlocks = make_layers(variants['radon'], init_channels, ds_ver)

        #-------------------------------------------------------------- RESBLOCKS

        #---------------------------------------------------------------------------------- CLASSIFIER

        self.AvgPool = FastGlobalAvgPool2d(flatten = False)

        self.fc = ClassifierNet(flavor, init_channels)

    def forward(self, x):

        x1, x2 = x

        #--------------------------------------- HEAD

        x1 = self.Head(x1)
        x2 = self.RadonHead(x2)

        #--------------------------------------- HEAD

        #--------------------------------------- WAFER

        x1 = self.ResBlocks(x1)
        x1 = self.AvgPool(x1)

        #--------------------------------------- WAFER

        #--------------------------------------- RADON

        x2 = self.RadonResBlocks(x2)
        x2 = self.AvgPool(x2)

        #--------------------------------------- RADON

        #--------------------------------------- CLASSIFIER
        
        x = torch.cat((x1, x2), dim=1)
        x = self.fc(x)

        #--------------------------------------- CLASSIFIER

        return x
    