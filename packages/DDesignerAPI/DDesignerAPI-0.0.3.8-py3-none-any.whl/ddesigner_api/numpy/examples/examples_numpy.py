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
from ddesigner_api.numpy.xwn.optimization import Optimization



def transform():
    kernel = np.array([
        [ [ [2, 0.1, 0.5], [3, 0.2, 5.2], [1, 0.4, 8.2] ]],
        [ [ [0, 0.3, 0.1], [1, 0.4, 100.2], [4, 2.4, 10.4]]],
    ]).transpose((2,3,0,1))
    print('Kernel Shape = {}'.format(kernel.shape))
    
    print('====== Input ======')
    print(kernel)
    print('==========================')
    
    print('====== Ouptut by XWN =====')
    opt = Optimization(
        use_transform = True, 
        bit = 4, 
        max_scale = 4.0,
        use_pruning = False, 
        shape = kernel.shape,
    )
    o = opt.optimize(kernel)
    print(o)
    print('==========================')
    

def transform_pruning():
    kernel = np.array([
        [ [ [2, 0.1, 0.5], [3, 0.2, 5.2], [1, 0.4, 8.2] ]],
        [ [ [0, 0.3, 0.1], [1, 0.4, 100.2], [4, 2.4, 10.4]]],
    ]).transpose((2,3,0,1))                                                               
    print('Kernel Shape = {}'.format(kernel.shape))
    
    print('====== Input ======')
    print(kernel)
    print('==========================')
    
    print('====== Ouptut by XWN =====')
    opt = Optimization(
        use_transform = True, 
        bit = 4, 
        max_scale = 4.0,
        use_pruning = True, 
        prun_weight = 0.5, 
        shape = kernel.shape,
    )
    o = opt.optimize(kernel)
    print(o)
    print('==========================')


def main():
    print('====== NUMPY Examples======')

    while True:
        print('1: XWN Transform')
        print('2: XWN Transform and Pruning')
        print('q: Quit')
        print('>>> Select Case:')
        cmd = input()
        if cmd == '1':
            transform()
        elif cmd == '2':
            transform_pruning()
        elif cmd == 'q': 
            break
        
    return True



if __name__ == '__main__':
    main()
