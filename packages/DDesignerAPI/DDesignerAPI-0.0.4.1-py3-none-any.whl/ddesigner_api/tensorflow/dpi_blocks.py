# Copyright 2023 The Deeper-I Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import tensorflow as tf
from tensorflow.keras import layers

from . import dpi_layers as dlayers
from .xwn import keras_layers as klayers



##############
# Block layers
##############
@tf.keras.utils.register_keras_serializable()
class Conv1DBlock(layers.Layer):

    def __init__(
        self, 
        filters, 
        kernel_size, 
        strides=1, 
        padding='valid', 
        data_format=None,
        dilation_rate=1, 
        activation=None, 
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Components
        convolution=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['CONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        super(Conv1DBlock, self).__init__(**kwargs)

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout

        self.filters = filters
        self.kernel_size = kernel_size

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.max_scale = max_scale
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = False
        
        # Conv
        if convolution is None:
            self.conv = klayers.Conv1D(
                filters, 
                kernel_size,
                strides=strides, 
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                dtype=dtype,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'CONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
        }
        base_config = super(Conv1DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class Conv2DBlock(layers.Layer):

    def __init__(
        self, 
        filters, 
        kernel_size, 
        strides=(1,1), 
        padding='valid', 
        data_format=None,
        dilation_rate=(1,1), 
        activation=None, 
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Components
        convolution=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['CONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        super(Conv2DBlock, self).__init__(**kwargs)

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout
        
        self.filters = filters
        self.kernel_size = kernel_size
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = False
        
        # Conv
        if convolution is None:
            self.conv = klayers.Conv2D(
                filters, 
                kernel_size,
                strides=strides, 
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                dtype=dtype,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'CONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
        }
        base_config = super(Conv2DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class FCBlock(layers.Layer):

    def __init__(
        self, 
        units,
        activation=None,
        use_bias=True,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Components
        multiply_accumulate=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization - Reserved
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['FC', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        super(FCBlock, self).__init__(**kwargs)

        # Assign
        self.act = activation
        self.bn = batchnormalization
        self.dropout = dropout

        self.units = units
        
        # Conv
        if multiply_accumulate is None:
            self.fc = layers.Dense(
                units, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                dtype=dtype,
            )
        else:
            self.fc = multiply_accumulate

        self.layer_list = []
        for o in order:
            if o == 'FC': self.layer_list.append(self.fc)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'units' : self.units,
            'multiply_accumulate' : self.fc,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
        }
        base_config = super(FCBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class TConv2DBlock(layers.Layer):

    def __init__(
        self, 
        filters, 
        kernel_size, 
        strides=(1,1), 
        padding='valid', 
        data_format=None,
        dilation_rate=(1,1), 
        activation=None, 
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Components
        convolution=None, 
        batchnormalization=None, 
        dropout=None, 
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['TCONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):
        super(TConv2DBlock, self).__init__(**kwargs)

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout
        
        self.filters = filters
        self.kernel_size = kernel_size
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = True
        
        # TConv
        if convolution is None:
            self.conv = klayers.Conv2DTranspose(
                filters, 
                kernel_size,
                strides=strides, 
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias, 
                kernel_initializer=kernel_initializer, 
                bias_initializer=bias_initializer, 
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                dtype=dtype,

                use_transform=self.use_transform, 
                bit=self.bit,
                max_scale=self.max_scale,
                use_pruning=self.use_pruning,
                prun_weight=self.prun_weight,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'TCONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
        }
        base_config = super(TConv2DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x


@tf.keras.utils.register_keras_serializable()
class SBConv2DBlock(layers.Layer):                                                                   
    
    def __init__(                                                                                    
        self, 
        filters:int,
        kernel_size, 
        strides=(1,1), 
        padding='valid',
        data_format=None,
        dilation_rate=(1,1),
        activation=None,
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        dtype='float32',
        # Custom
        scale_ratio:int=2,
        # Components
        convolution=None,
        batchnormalization=None,
        dropout=None,
        # Optimization
        transform=None,
        pruning=None,
        max_scale=4.0,
        order=['SPCONV', 'BN', 'ACT', 'DROPOUT'],
        **kwargs
    ):  
        super(SBConv2DBlock, self).__init__(**kwargs)

        # Assign
        self.bn = batchnormalization
        self.act = activation
        self.dropout = dropout
        
        self.scale_ratio = scale_ratio
        self.filters = filters
        self.kernel_size = kernel_size
        self.transform = transform
        self.pruning = pruning
        self.max_scale = max_scale

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5
        self.transpose = False

        # SPConv
        if convolution is None:
            self.conv = klayers.SubPixelConv2D(
                filters, 
                kernel_size,
                strides=strides,
                padding=padding, 
                data_format=data_format,
                dilation_rate=dilation_rate, 
                use_bias=use_bias,
                kernel_initializer=kernel_initializer,
                bias_initializer=bias_initializer,
                kernel_regularizer=kernel_regularizer,
                bias_regularizer=bias_regularizer,
                activity_regularizer=activity_regularizer,
                kernel_constraint=kernel_constraint,
                bias_constraint=bias_constraint,
                dtype=dtype,

                scale_ratio=scale_ratio,
                transform=transform,
                pruning=pruning,
                max_scale=max_scale,
                **kwargs,
            )
        else:
            self.conv = convolution

        self.layer_list = []
        for o in order:
            if o == 'SPCONV': self.layer_list.append(self.conv)
            elif o == 'BN': self.layer_list.append(self.bn)
            elif o == 'ACT': self.layer_list.append(self.act)
            elif o == 'DROPOUT': self.layer_list.append(self.dropout)

    def get_config(self):
        config = {
            'filters' : self.filters,
            'kernel_size' : self.kernel_size,
            'scale_ratio' : self.scale_ratio,
            'transform' : self.transform,
            'max_scale' : self.max_scale,
            'pruning' : self.pruning,
            'convolution' : self.conv,
            'batchnormalization' : self.bn,
            'activation' : self.act,
            'dropout' : self.dropout,
        }
        base_config = super(SBConv2DBlock, self).get_config()
        base_config.update(config)
        return base_config

    def call(self, inputs, training=None):
        x = inputs
        for l in self.layer_list:
            if l is not None:
                x = l(x)

        return x



