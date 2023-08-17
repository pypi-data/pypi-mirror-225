# Copyright 2023 The Deeper-I Authors. All Rights Reserved.
#
# BSD 3-Clause License
# 
# Copyright (c) 2017, 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import torch
import torch.nn as nn

from .xwn import torch_nn as dnn



##############
# Unit layers
##############
class CascadeConv1d(nn.Module):
    '''
    A layer with a structure for constructing a convolution layer with a large kernel size with a small kernel size.
    '''
    def __init__(
        self, 
        in_channels, 
        out_channels, 
        kernel_size, 
        stride=1, 
        padding=0, 
        mid_channels=None,
        channel_ratio=0.5,
        bias=False,
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        **kwargs
    ):
        super(CascadeConv1d, self).__init__()

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.max_scale = max_scale
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        self.n_layers = (kernel_size // 2)
        if mid_channels is None:
            mid_channels = int(in_channels * channel_ratio)
        conv_list = []

        for i in range(self.n_layers):
            if i == 0: 
                _in_channels = in_channels
            else:
                _in_channels = mid_channels

            conv_list.append(
                dnn.Conv1d(
                    _in_channels, 
                    mid_channels, 
                    kernel_size=3, 
                    stride=1,
                    padding=1, # left and right 
                    bias=False,
                    use_transform=self.use_transform,
                    bit=self.bit,
                    max_scale=self.max_scale,
                    use_pruning=self.use_pruning,
                    prun_weight=self.prun_weight,
                )
            )

        self.pointwise_conv = dnn.Conv1d(
            mid_channels * self.n_layers, 
            out_channels, 
            kernel_size=1, 
            stride=stride,
            padding=padding, 
            bias=bias,
            use_transform=self.use_transform,
            bit=self.bit,
            max_scale=self.max_scale,
            use_pruning=self.use_pruning,
            prun_weight=self.prun_weight,
        )
        self.conv_list = nn.ModuleList(conv_list)

    def forward(self, x):
        x_list = []
        for i in range(self.n_layers):
            x = self.conv_list[i](x)
            x_list.append(x)
        
        x = torch.cat(x_list, dim=1)
        x = self.pointwise_conv(x)
        return x

class CascadeConv2d(nn.Module):
    '''
    A layer with a structure for constructing a convolution layer with a large kernel size with a small kernel size.
    '''
    def __init__(
        self, 
        in_channels, 
        out_channels, 
        kernel_size, 
        stride=1, 
        padding=0, 
        mid_channels=None,
        channel_ratio=0.5,
        bias=False,
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        **kwargs
    ):
        super(CascadeConv2d, self).__init__()

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.max_scale = max_scale
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        self.n_layers = (kernel_size // 2)
        if mid_channels is None:
            mid_channels = int(in_channels * channel_ratio)
        conv_list = []

        for i in range(self.n_layers):
            if i == 0: 
                _in_channels = in_channels
            else:
                _in_channels = mid_channels

            conv_list.append(
                dnn.Conv2d(
                    _in_channels, 
                    mid_channels, 
                    kernel_size=3, 
                    stride=1,
                    padding=1, # left and right 
                    bias=False,
                    use_transform=self.use_transform,
                    bit=self.bit,
                    max_scale=self.max_scale,
                    use_pruning=self.use_pruning,
                    prun_weight=self.prun_weight,
                )
            )

        self.pointwise_conv = dnn.Conv2d(
            mid_channels * self.n_layers, 
            out_channels, 
            kernel_size=1, 
            stride=stride,
            padding=padding, 
            bias=bias,
            use_transform=self.use_transform,
            bit=self.bit,
            max_scale=self.max_scale,
            use_pruning=self.use_pruning,
            prun_weight=self.prun_weight,
        )
        self.conv_list = nn.ModuleList(conv_list)

    def forward(self, x):
        x_list = []
        for i in range(self.n_layers):
            x = self.conv_list[i](x)
            x_list.append(x)
        
        x = torch.cat(x_list, dim=1)
        x = self.pointwise_conv(x)
        return x

