
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, BatchNorm2d, Dropout, AdaptiveAvgPool2d, AdaptiveMaxPool2d, Dropout2d, LPPool2d
from torch.nn import BatchNorm2d, GroupNorm, LazyLinear, Identity, Sigmoid, Flatten, Unflatten
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU
from torch import mul

from torchvision.ops import DropBlock2d

from kornia.augmentation import Resize
import torch

#------------------------------
from .AttentionBlocks import SE_Block, MSCAM, SAM, ESAM, ECA
from .UtilityBlocks import Downsample
#------------------------------

torch.manual_seed(43)

def ResBlock(args):

    """
 flavor, channel_attention, spatial_attention],
    args: [flavor, channels, squeeze, downsample]

    """

    channels, hyper_params, downsample = args

    flavor, attention, ratio = hyper_params
    
    if flavor == 'basic':
        return Basic_Block(channels, attention, ratio, downsample)
    
    elif flavor == 'bottleneck':
        return Bottleneck_Block(channels, attention, ratio, downsample)
    
    elif flavor == 'radon':
        return Radon_Block(channels, attention, ratio, downsample)


class ConvBlock(Module):
    def __init__(self, in_channels, out_channels, kernel_size = 3, stride = 1):
        super(ConvBlock, self).__init__()

        self.bn = BatchNorm2d(in_channels)
        self.activation = Mish(inplace = True)

        if type(kernel_size) == int:
            padding = kernel_size // 2
        else:
            padding = (kernel_size[0] // 2, kernel_size[1] // 2)

        self.conv = Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        
    def forward(self, x):

        x = self.bn(x)
        x = self.activation(x)
        x = self.conv(x)

        return x

#--------------------------------------------------------------------------------- Basic

class Basic_Block(Module):
    def __init__(self, channels, attention, ratio, downsample = False):
        super(Basic_Block, self).__init__()

        channel_attention, spatial_attention = attention

        if not downsample:
            stride = 1
            i_channels = channels 
            o_channels = channels 
        else:
            stride = 2
            i_channels = channels // 2
            o_channels = channels

        if downsample == 'new':

            self.BasicBlock = Sequential(
                ConvBlock(i_channels, o_channels),
                Downsample(channels = o_channels),
                ConvBlock(o_channels, o_channels),
            )

        else:

            self.BasicBlock = Sequential(
                ConvBlock(i_channels, o_channels, stride = stride),
                ConvBlock(o_channels, o_channels),
            )

        self.downsample = Sequential(
            AvgPool2d(stride, stride),
            ConvBlock(i_channels, o_channels, 1, 1),
        )

        if channel_attention == 'se':
            self.channel_attention = SE_Block(o_channels, ratio)
        elif channel_attention == 'mscam':
            self.channel_attention = MSCAM(o_channels, ratio)
        elif channel_attention == 'eca':
            self.channel_attention = ECA()

        if spatial_attention == 'sam':
            self.spatial_attention = SAM()
        elif spatial_attention == 'esam':
            self.spatial_attention = ESAM(o_channels, ratio)

    def forward(self, x):

        identity = x

        x = self.BasicBlock(x)
        identity = self.downsample(identity)

        try:
            x = self.channel_attention(x)
            x = self.spatial_attention(x)
        except:
            pass
        
        x += identity

        return x

#--------------------------------------------------------------------------------- Basic

#--------------------------------------------------------------------------------- Bottleneck

class Bottleneck_Block(Module):
    def __init__(self, channels, attention, ratio, downsample = False):
        super(Bottleneck_Block, self).__init__()

        channel_attention, spatial_attention = attention

        if not downsample:
            stride = 1
            i_channels = channels * 4
            m_channels = channels
            o_channels = channels * 4
        else:
            stride = 2
            i_channels = channels * 2
            m_channels = channels
            o_channels = channels * 4


        self.BottleneckBlock = Sequential(
            ConvBlock(i_channels, m_channels, kernel_size = 1),
            ConvBlock(m_channels, m_channels, stride = stride),
            ConvBlock(m_channels, o_channels, kernel_size = 1),
        )

        self.downsample = Sequential(
            AvgPool2d(stride, stride),
            ConvBlock(i_channels, o_channels, 1, 1),
        )

        if channel_attention == 'se':
            self.channel_attention = SE_Block(o_channels, ratio)
        elif channel_attention == 'mscam':
            self.channel_attention = MSCAM(o_channels, ratio)
        elif channel_attention == 'eca':
            self.channel_attention = ECA()

        if spatial_attention == 'sam':
            self.spatial_attention = SAM()
        elif spatial_attention == 'esam':
            self.spatial_attention = ESAM(o_channels, ratio)

    def forward(self, x):

        identity = x

        x = self.BottleneckBlock(x)
        identity = self.downsample(identity)

        try:
            x = self.channel_attention(x)
            x = self.spatial_attention(x)
        except:
            pass

        x += identity

        return x

#--------------------------------------------------------------------------------- Bottleneck

#--------------------------------------------------------------------------------- Radon

class Radon_Block(Module):
    def __init__(self, channels, attention, ratio, downsample = False):
        super(Radon_Block, self).__init__()

        channel_attention, spatial_attention = attention

        if not downsample:
            stride = 1
            i_channels = channels 
            o_channels = channels 
        else:
            stride = 2
            i_channels = channels // 2
            o_channels = channels

        self.BasicBlock = Sequential(
            ConvBlock(i_channels, o_channels, stride = stride),

            ConvBlock(o_channels, o_channels, kernel_size = (3, 1)),
            ConvBlock(o_channels, o_channels, kernel_size = (1, 3)),
        )

        self.downsample = Sequential(
            AvgPool2d(stride, stride),
            ConvBlock(i_channels, o_channels, 1, 1),
        )

        if channel_attention == 'se':
            self.channel_attention = SE_Block(o_channels, ratio)
        elif channel_attention == 'mscam':
            self.channel_attention = MSCAM(o_channels, ratio)
        elif channel_attention == 'eca':
            self.channel_attention = ECA()

        if spatial_attention == 'sam':
            self.spatial_attention = SAM()
        elif spatial_attention == 'esam':
            self.spatial_attention = ESAM(o_channels, ratio)

    def forward(self, x):

        identity = x

        x = self.BasicBlock(x)
        identity = self.downsample(identity)

        try:
            x = self.channel_attention(x)
            x = self.spatial_attention(x)
        except:
            pass
        
        x += identity

        return x





