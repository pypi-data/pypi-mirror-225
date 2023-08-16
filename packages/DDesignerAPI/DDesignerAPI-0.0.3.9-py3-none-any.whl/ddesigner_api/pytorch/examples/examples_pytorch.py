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

# -*- coding: utf-8 -*-

import numpy as np
import torch
from ddesigner_api.pytorch.xwn import torch_nn as nn
from ddesigner_api.pytorch import dpi_nn as dnn



def fixed_input():
    x_in = np.array([[                                                                            
        [[2], [1], [2], [0], [1]],                                                                  
        [[1], [3], [2], [2], [3]],                                                                  
        [[1], [1], [3], [3], [0]],                                                                  
        [[2], [2], [0], [1], [1]],
        [[0], [0], [3], [1], [2]], ]])                                                              
    kernel_in = np.array([                                                                        
        [ [[2, 0.1]], [[3, 0.2]] ],                                                                  
        [ [[0, 0.3]], [[1, 0.4]] ], ])                                                               
    x = torch.from_numpy(np.transpose(x_in, (0,3,1,2)).astype('float32'))
    kernel = torch.from_numpy(np.transpose(kernel_in, (3,2,0,1)).astype('float32'))
    print('Input Shape = {}, Kernel Shape = {}'.format(x.shape, kernel.shape))
    
    print('====== torch.nn.Conv2d ======')
    with torch.no_grad():
        m = torch.nn.Conv2d(
            in_channels=1, 
            out_channels=2, 
            kernel_size=2, 
            stride=(1,1), 
            padding='valid', 
            bias=False
        )
        m.weight.copy_(kernel)
        # o = torch.permute(m(x), (0,2,3,1))
        o = m(x)
        print(o)
    print('==========================')
    
    print('====== dpi_nn.Conv2d (without opt) =====')
    with torch.no_grad():
        m = nn.Conv2d(
            in_channels=1, 
            out_channels=2, 
            kernel_size=2, 
            stride=(1,1), 
            padding='valid', 
            bias=False
        )
        m.weight.copy_(kernel)
        o = m(x)
        print(o)
    print('==========================')
    
    print('====== dpi_nn.Conv2d (with opt) =====')
    with torch.no_grad():
        m = nn.Conv2d(
            in_channels=1, 
            out_channels=2, 
            kernel_size=2, 
            stride=(1,1), 
            padding='valid', 
            bias=False,
            use_transform=True,
            bit=4,
            max_scale=4.0,
        )
        m.weight.copy_(kernel)
        o = m(x)
        print(o)
    print('==========================')


def random_input():
    torch.manual_seed(87)
    x = torch.randn(1,1,5,5)
    kernel = torch.nn.init.xavier_uniform_(torch.empty(2,1,2,2))
    print('Input Shape = {}, Kernel Shape = {}'.format((1,1,5,5), (2,1,2,2)))

    print('====== torch.nn.Conv2d ======')
    with torch.no_grad():
        m = torch.nn.Conv2d(
            in_channels=1, 
            out_channels=2, 
            kernel_size=2, 
            stride=(1,1), 
            padding='valid', 
            bias=False
        )
        m.weight.copy_(kernel)
        print(m(x))
    print('==========================')

    print('====== dpi_nn.Conv2d (without opt) =====')
    with torch.no_grad():
        m = nn.Conv2d(
            in_channels=1, 
            out_channels=2, 
            kernel_size=2, 
            stride=(1,1), 
            padding='valid', 
            bias=False
        )
        m.weight.copy_(kernel)
        print(m(x))
    print('==========================')

    print('====== dpi_nn.Conv2d (with opt) =====')
    with torch.no_grad():
        m = nn.Conv2d(
            in_channels=1, 
            out_channels=2, 
            kernel_size=2, 
            stride=(1,1), 
            padding='valid', 
            bias=False,
            use_transform=True,
            bit=4,
            max_scale=4.0,
        )
        m.weight.copy_(kernel)
        print(m(x))
    print('==========================')

def fixed_input_conv1d():
    x_in = np.array([                                                                            
        2, 1, 2, 0, 1,                                                                  
        1, 3, 2, 2, 3,                                                                  
        1, 1, 3, 3, 0,                                                                  
        2, 2, 0, 1, 1,
        3, 1, 0, 3, 1,
        0, 0, 3, 1, 2, ])                                                              
    kernel_in = np.array([                                                                        
        2, 0.1, 3,                                                                   
        0, 0.3, 1,  ])                                                               
    x = torch.from_numpy(np.reshape(x_in, (2,3,5)).astype('float32'))
    kernel = torch.from_numpy(np.reshape(kernel_in, (1,3,2)).astype('float32'))
    print('Input Shape = {}, Kernel Shape = {}'.format(x.shape, kernel.shape))
    
    print('====== torch.nn.Conv1d ======')
    with torch.no_grad():
        m = torch.nn.Conv1d(
            in_channels=3, 
            out_channels=1, 
            kernel_size=2, 
            stride=1, 
            padding='valid', 
            bias=False
        )
        m.weight.copy_(kernel)
        # o = torch.permute(m(x), (0,2,3,1))
        o = m(x)
        print(o)
    print('==========================')
    
    print('====== dpi_nn.Conv1d (without opt) =====')
    with torch.no_grad():
        m = nn.Conv1d(
            in_channels=3, 
            out_channels=1, 
            kernel_size=2, 
            stride=1, 
            padding='valid', 
            bias=False
        )
        m.weight.copy_(kernel)
        o = m(x)
        print(o)
    print('==========================')
    
    print('====== dpi_nn.Conv1d (with opt) =====')
    with torch.no_grad():
        m = nn.Conv1d(
            in_channels=3, 
            out_channels=1, 
            kernel_size=2, 
            stride=1, 
            padding='valid', 
            bias=False,
            use_transform=True,
            bit=4,
            max_scale=4.0,
        )
        m.weight.copy_(kernel)
        o = m(x)
        print(o)
    print('==========================')

def fixed_input_tconv1d():
    x_in = np.array([                                                                            
        2, 1, 2, 0, 1,                                                                  
        1, 3, 2, 2, 3,                                                                  
        1, 1, 3, 3, 0,                                                                  
        2, 2, 0, 1, 1,
        3, 1, 0, 3, 1,
        0, 0, 3, 1, 2, ])                                                              
    kernel_in = np.array([                                                                        
        2, 0.1, 3,                                                                   
        0, 0.3, 1,  ])                                                               
    x = torch.from_numpy(np.reshape(x_in, (2,3,5)).astype('float32'))
    kernel = torch.from_numpy(np.reshape(kernel_in, (3,1,2)).astype('float32'))
    print('Input Shape = {}, Kernel Shape = {}'.format(x.shape, kernel.shape))
    
    print('====== torch.nn.ConvTranspose1d ======')
    with torch.no_grad():
        m = torch.nn.ConvTranspose1d(
            in_channels=3, 
            out_channels=1, 
            kernel_size=2, 
            stride=1, 
            # padding='valid', 
            padding=0, 
            bias=False
        )
        m.weight.copy_(kernel)
        # o = torch.permute(m(x), (0,2,3,1))
        o = m(x)
        print(o)
    print('==========================')
    
    print('====== dpi_nn.ConvTranspose1d (without opt) =====')
    with torch.no_grad():
        m = nn.ConvTranspose1d(
            in_channels=3, 
            out_channels=1, 
            kernel_size=2, 
            stride=1, 
            # padding='valid', 
            padding=0, 
            bias=False
        )
        m.weight.copy_(kernel)
        o = m(x)
        print(o)
    print('==========================')
    
    print('====== dpi_nn.ConvTranspose1d (with opt) =====')
    with torch.no_grad():
        m = nn.ConvTranspose1d(
            in_channels=3, 
            out_channels=1, 
            kernel_size=2, 
            stride=1, 
            # padding='valid', 
            padding=0, 
            bias=False,
            use_transform=True,
            bit=4,
            max_scale=4.0,
        )
        m.weight.copy_(kernel)
        o = m(x)
        print(o)
    print('==========================')

def random_input_cascadeconv2d():
    torch.manual_seed(87)
    x = torch.randn(1,16,7,7)
    w_0 = torch.nn.init.xavier_uniform_(torch.empty(8,16,3,3))
    w_1 = torch.nn.init.xavier_uniform_(torch.empty(8,8,3,3))
    w_2 = torch.nn.init.xavier_uniform_(torch.empty(8,8,3,3))
    w_l = torch.nn.init.xavier_uniform_(torch.empty(32,24,1,1))
    print('Input Shape = {}'.format((1,16,7,7)))

    print('====== dpi_nn.CascadeConv2d (without opt) =====')
    with torch.no_grad():
        m = dnn.CascadeConv2d(
            16, # in_channels 
            32, # out_channels
            7, # kernel_size
            stride=(1,1), 
            bias=False
        )
        for l, w in zip(m.conv_list, [w_0, w_1, w_2]):
            l.weight.copy_(w)
        m.pointwise_conv.weight.copy_(w_l)
        print(m(x))
    print('==========================')

    print('====== dpi_nn.CascadeConv2d (with opt) =====')
    with torch.no_grad():
        m = dnn.CascadeConv2d(
            16, # in_channels 
            32, # out_channels
            7, # kernel_size
            stride=(1,1), 
            bias=False,
            transform=4,
            max_scale=4.0,
            pruning=None,
        )
        for l, w in zip(m.conv_list, [w_0, w_1, w_2]):
            l.weight.copy_(w)
        m.pointwise_conv.weight.copy_(w_l)
        print(m(x))
    print('==========================')


def random_input_cascadeconv1d():
    torch.manual_seed(87)
    x = torch.randn(1,16,7)
    w_0 = torch.nn.init.xavier_uniform_(torch.empty(8,16,3))
    w_1 = torch.nn.init.xavier_uniform_(torch.empty(8,8,3))
    w_2 = torch.nn.init.xavier_uniform_(torch.empty(8,8,3))
    w_l = torch.nn.init.xavier_uniform_(torch.empty(32,24,1))
    print('Input Shape = {}'.format((1,16,7)))

    print('====== dpi_nn.CascadeConv2d (without opt) =====')
    with torch.no_grad():
        m = dnn.CascadeConv1d(
            16, # in_channels 
            32, # out_channels
            7, # kernel_size
            stride=1, 
            bias=False
        )
        for l, w in zip(m.conv_list, [w_0, w_1, w_2]):
            l.weight.copy_(w)
        m.pointwise_conv.weight.copy_(w_l)
        print(m(x))
    print('==========================')

    print('====== dpi_nn.CascadeConv2d (with opt) =====')
    with torch.no_grad():
        m = dnn.CascadeConv1d(
            16, # in_channels 
            32, # out_channels
            7, # kernel_size
            stride=1, 
            bias=False,
            transform=4,
            max_scale=4.0,
            pruning=None,
        )
        for l, w in zip(m.conv_list, [w_0, w_1, w_2]):
            l.weight.copy_(w)
        m.pointwise_conv.weight.copy_(w_l)
        print(m(x))
    print('==========================')



def main():
    print('====== PYTORCH Examples======')

    while True:
        print('1: Fixed  Float32 Input Conv2D')
        print('2: Random Float32 Input Conv2D')
        print('3: Fixed  Float32 Input Conv1D')
        print('4: Fixed  Float32 Input Conv1DTranspose')
        print('5: Random Float32 Input CascadeConv2D')
        print('6: Random Float32 Input CascadeConv1D')
        print('q: Quit')
        print('>>> Select Case:')
        cmd = input()
        if cmd == '1':
            fixed_input()
        elif cmd == '2':
            random_input()
        elif cmd == '3':
            fixed_input_conv1d()
        elif cmd == '4': 
            fixed_input_tconv1d()
        elif cmd == '5': 
            random_input_cascadeconv2d()
        elif cmd == '6': 
            random_input_cascadeconv1d()
        elif cmd == 'q': 
            break
        
    return True



if __name__ == '__main__':
    main()
