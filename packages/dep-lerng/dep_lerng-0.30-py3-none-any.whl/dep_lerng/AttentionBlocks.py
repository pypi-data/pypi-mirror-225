
from torch.nn import Module, Conv2d, Linear, MaxPool2d, AvgPool2d, Sequential, BatchNorm2d, Dropout, AdaptiveAvgPool2d, AdaptiveMaxPool2d, Conv1d
from torch.nn import BatchNorm1d, GroupNorm, LazyLinear, Identity, Sigmoid, Flatten, Unflatten, Tanh, Hardsigmoid, Hardtanh, Softmax
from torch.nn import Mish, ReLU, LeakyReLU, PReLU, SELU
from torch import mul

import torch.nn.functional as F

import torch

from torchvision.ops import DropBlock2d

from kornia.augmentation import Resize

#------------------------------
from .UtilityBlocks import FastGlobalAvgPool2d, ChannelPool
#------------------------------

#--------------------------------------------------------------------------------- Squeeze Excitation

class SE_Block(Module):
    def __init__(self, n_channels, compression_ratio):
        super(SE_Block, self).__init__()

        self.pool = FastGlobalAvgPool2d()
        self.squeeze = Sequential(
            Conv2d(n_channels, n_channels // compression_ratio, 1),
            Mish(inplace = True),

            Conv2d(n_channels // compression_ratio, n_channels, 1),
            Sigmoid(),
        )


    def forward(self, x):

        attention = x

        attention = self.pool(attention)
        attention = self.squeeze(attention)

        x = x * attention

        return x

#--------------------------------------------------------------------------------- Squeeze Excitation

#--------------------------------------------------------------------------------- MSCAM

class MSCAM(Module):
    def __init__(self, n_channels, compression_ratio):
        super(MSCAM, self).__init__()

        latent_channels = n_channels // compression_ratio

        self.GAP = FastGlobalAvgPool2d()

        self.Global_Context = Sequential(
            Conv2d(n_channels, latent_channels, 1, bias = False),
            BatchNorm2d(latent_channels),
            Mish(inplace = True),

            Conv2d(latent_channels, n_channels, 1, bias = False),
            BatchNorm2d(n_channels),
        )

        self.Local_Context = Sequential(
            Conv2d(n_channels, latent_channels, 1, bias = False),
            BatchNorm2d(latent_channels),
            Mish(inplace = True),

            Conv2d(latent_channels, n_channels, 1, bias = False),
            BatchNorm2d(n_channels),
        )

    def forward(self, x):

        g_context = self.GAP(x)
        g_context = self.Global_Context(g_context)
        l_context = self.Local_Context(x)

        attention = g_context + l_context

        attention = torch.sigmoid(attention)

        x = x * attention

        return x
    
#--------------------------------------------------------------------------------- MSCAM
    
#--------------------------------------------------------------------------------- SAM

class SAM(Module):
    def __init__(self):
        super(SAM, self).__init__()

        self.channel_pool = ChannelPool()
        self.conv = Sequential(
            Conv2d(2, 1, kernel_size=7, stride=1, padding=3, bias=False),  # Applies 7x7 Convolution to Extract Features
            BatchNorm2d(1),              
            Sigmoid(),
        )   


    def forward(self, x):
        spatial_x = self.channel_pool(x)
        spatial_x = self.conv(spatial_x)

        return x * spatial_x
    
#--------------------------------------------------------------------------------- SAM

#--------------------------------------------------------------------------------- Enchanced SAM

class ESAM(Module):
    def __init__(self, n_channels, compression_ratio):
        super(ESAM, self).__init__()

        latent_channels = n_channels // compression_ratio

        self.Width_Context = Sequential(
            Conv2d(n_channels, latent_channels, 1, bias = False),
            BatchNorm2d(latent_channels),
            Mish(inplace = True),

            Conv2d(latent_channels, n_channels, 1, bias = False),
            BatchNorm2d(n_channels),
            Sigmoid(),
        )

        self.Height_Context = Sequential(
            Conv2d(n_channels, latent_channels, 1, bias = False),
            BatchNorm2d(latent_channels),
            Mish(inplace = True),

            Conv2d(latent_channels, n_channels, 1, bias = False),
            BatchNorm2d(n_channels),
            Sigmoid(),
        )

    def forward(self, x):

        w_context = torch.mean(x, 2, True)
        h_context = torch.mean(x, 3, True)

        w_attention = self.Width_Context(w_context)
        h_attention = self.Height_Context(h_context)

        x = (w_attention * x) + (h_attention * x)

        return x
    
#--------------------------------------------------------------------------------- Enchanced SAM

#--------------------------------------------------------------------------------- ECA

class ECA(Module):
    def __init__(self, k_size=3):
        super(ECA, self).__init__()
        self.avg_pool = AdaptiveAvgPool2d(1)
        self.conv = Conv1d(1, 1, kernel_size=k_size, padding=(k_size - 1) // 2, bias=True) 
        self.sigmoid = Sigmoid()

    def forward(self, x):
        # x: input features with shape [b, c, h, w]
        b, c, h, w = x.size()

        # feature descriptor on the global spatial information
        y = self.avg_pool(x)

        # Two different branches of ECA module
        y = self.conv(y.squeeze(-1).transpose(-1, -2)).transpose(-1, -2).unsqueeze(-1)

        # Multi-scale information fusion
        y = self.sigmoid(y)

        return x * y.expand_as(x)

#--------------------------------------------------------------------------------- ECA

# class AFF(Module):
#     '''
#     多特征融合 AFF
#     '''

#     def __init__(self, channels=64, r=4):
#         super(AFF, self).__init__()
#         inter_channels = int(channels // r)

#         self.local_att = Sequential(
#             Conv2d(channels, inter_channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(inter_channels, momentum = moment),
#             acti,
#             Conv2d(inter_channels, channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(channels, momentum = moment),
#         )

#         self.global_att = Sequential(
#             AdaptiveAvgPool2d(1),
#             Conv2d(channels, inter_channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(inter_channels, momentum = moment),
#             acti,
#             Conv2d(inter_channels, channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(channels, momentum = moment),
#         )

#     def forward(self, x, residual):

#         xa = x + residual
#         # xl = self.local_att(xa)
#         # xg = 
#         wei = F.sigmoid(self.local_att(xa) + self.global_att(xa))
#         # wei = F.sigmoid(xlg)

#         xo = 2 * x * wei + 2 * residual * (1 - wei)

#         return xo

# class iAFF(Module):
#     '''
#     多特征融合 iAFF
#     '''

#     def __init__(self, channels=64, r=4):
#         super(iAFF, self).__init__()
#         inter_channels = int(channels // r)

#         # 本地注意力
#         self.local_att = Sequential(
#             Conv2d(channels, inter_channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(inter_channels),
#             acti,
#             Conv2d(inter_channels, channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(channels),
#         )

#         # 全局注意力
#         self.global_att = Sequential(
#             AdaptiveAvgPool2d(1),
#             Conv2d(channels, inter_channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(inter_channels),
#             acti,
#             Conv2d(inter_channels, channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(channels),
#         )

#         # 第二次本地注意力
#         self.local_att2 = Sequential(
#             Conv2d(channels, inter_channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(inter_channels),
#             acti,
#             Conv2d(inter_channels, channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(channels),
#         )
#         # 第二次全局注意力
#         self.global_att2 = Sequential(
#             AdaptiveAvgPool2d(1),
#             Conv2d(channels, inter_channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(inter_channels),
#             acti,
#             Conv2d(inter_channels, channels, kernel_size=1, stride=1, padding=0),
#             BatchNorm2d(channels),
#         )

#         self.sigmoid = Sigmoid()

#     def forward(self, x, residual):

#         xa = x + residual
#         xl = self.local_att(xa)
#         xg = self.global_att(xa)
#         xlg = xl + xg
#         wei = self.sigmoid(xlg)
#         xi = x * wei + residual * (1 - wei)

#         xl2 = self.local_att2(xi)
#         xg2 = self.global_att(xi)
#         xlg2 = xl2 + xg2
#         wei2 = self.sigmoid(xlg2)
#         xo = x * wei2 + residual * (1 - wei2)
#         return xo

# # class spatial_MSCAM(Module):

# #     def __init__(self, channels=64, r=4):
# #         super(spatial_AFF, self).__init__()
# #         inter_channels = int(channels // r)

# #         self.spatial = SAM()

# #         self.sigmoid = Sigmoid()

# #     def forward(self, x, residual):
# #         xa = x + residual
# #         xl = self.spatial(xa)
# #         wei = self.sigmoid(xl)

# #         xo = 2 * x * wei + 2 * residual * (1 - wei)
# #         return xo

