
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, Dropout2d, Dropout, AdaptiveAvgPool2d, LazyConv2d, AlphaDropout, Bilinear
from torch.nn import BatchNorm1d, BatchNorm2d, GroupNorm, LazyLinear, LazyBatchNorm1d, LogSoftmax, MultiheadAttention
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU, Tanh, Sigmoid, ELU, Flatten, Softmax
from torch import flatten, unsqueeze

import torch

#------------------------------
# from .AttentionBlocks import AFF,MSCAM, SAM, iAFF, ECA

# from custom_blocks import AFF,MSCAM, SAM, iAFF, ECA
#------------------------------

torch.manual_seed(43)
  
# torch.set_float32_matmul_precision("high")

acti = Mish(inplace = True)
# acti = PReLU()

class ClassifierNet(Module):
    def __init__(self, flavor, init_channels):
        super(ClassifierNet, self).__init__()

        if flavor == 'basic' or flavor == 'radon':
            feature_maps = init_channels * 10
        elif flavor == 'bottleneck':
            feature_maps = init_channels * 16

        self.final_fc = Sequential(
            # Dropout2d(dropout_p),
            # Conv2d(192, 128, kernel_size = 1, bias = False),
            # acti,
            # BatchNorm2d(128, momentum = b_moment),
            # ECA(),attention

            Conv2d(feature_maps, 9, kernel_size = 1, bias = False),
            Flatten()
        )

    def forward(self, x):   

        x = self.final_fc(x)

        return x
    