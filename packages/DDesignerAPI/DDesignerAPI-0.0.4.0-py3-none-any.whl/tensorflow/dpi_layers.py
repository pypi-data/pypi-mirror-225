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

from .xwn import keras_layers as klayers



##############
# Unit layers
##############
@tf.keras.utils.register_keras_serializable()
class SqueezeAndExcitation2D(layers.Layer):
    def __init__(
        self, 
        filters, 
        data_format=None,
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        # Optimization
        transform=None,
        pruning=None,
        bit=4,
        max_scale=4.0,
        prun_weight=0.5,
        **kwargs
    ):
        super(SqueezeAndExcitation, self).__init__()

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.max_scale = max_scale
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        self.conv_0 = klayers.Conv2D(
            se_filters, 
            (1,1),
            strides=(1,1), 
            padding='valid', 
            data_format=data_format,
            use_bias=False, 
            kernel_initializer=kernel_initializer, 
            bias_initializer=bias_initializer, 
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer,
            kernel_constraint=kernel_constraint,
            bias_constraint=bias_constraint,

            use_transform=self.use_transform, 
            bit=self.bit,
            max_scale=self.max_scale,
            use_pruning=self.use_pruning,
            prun_weight=self.prun_weight,
        )
        self.act = layers.ReLU()
        self.conv_1 = klayers.Conv2D(
            filters, 
            (1,1),
            strides=(1,1), 
            padding='valid', 
            data_format=data_format,
            use_bias=False, 
            kernel_initializer=kernel_initializer, 
            bias_initializer=bias_initializer, 
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer,
            kernel_constraint=kernel_constraint,
            bias_constraint=bias_constraint,

            use_transform=self.use_transform, 
            bit=self.bit,
            max_scale=self.max_scale,
            use_pruning=self.use_pruning,
            prun_weight=self.prun_weight,
        )

    def call(self, inputs, training=None):
        x = inputs
        x_se = tf.reduce_mean(x, axis=[1,2], keepdims=True)
        x_se = self.conv_0(x_se)
        x_se = self.act(x_se)
        x_se = self.conv_1(x_se)
        x_se = tf.nn.sigmoid(x_se)
        x *= x_se
        return x

    def get_config(self):
        cfg = super().get_config()
        return cfg

@tf.keras.utils.register_keras_serializable()
class SqueezeAndExcitation1D(layers.Layer):
    def __init__(
        self, 
        filters, 
        data_format=None,
        use_bias=False,
        kernel_initializer='glorot_uniform',
        bias_initializer='zeros',
        kernel_regularizer=None,
        bias_regularizer=None,
        activity_regularizer=None,
        kernel_constraint=None,
        bias_constraint=None,
        # Optimization
        transform=None,
        pruning=None,
        bit=4,
        max_scale=4.0,
        prun_weight=0.5,
        **kwargs
    ):
        super(SqueezeAndExcitation, self).__init__()

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.max_scale = max_scale
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        self.conv_0 = klayers.Conv1D(
            se_filters, 
            (1,1),
            strides=(1,1), 
            padding='valid', 
            data_format=data_format,
            use_bias=False, 
            kernel_initializer=kernel_initializer, 
            bias_initializer=bias_initializer, 
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer,
            kernel_constraint=kernel_constraint,
            bias_constraint=bias_constraint,

            use_transform=self.use_transform, 
            bit=self.bit,
            max_scale=self.max_scale,
            use_pruning=self.use_pruning,
            prun_weight=self.prun_weight,
        )
        self.act = layers.ReLU()
        self.conv_1 = klayers.Conv1D(
            filters, 
            (1,1),
            strides=(1,1), 
            padding='valid', 
            data_format=data_format,
            use_bias=False, 
            kernel_initializer=kernel_initializer, 
            bias_initializer=bias_initializer, 
            kernel_regularizer=kernel_regularizer,
            bias_regularizer=bias_regularizer,
            activity_regularizer=activity_regularizer,
            kernel_constraint=kernel_constraint,
            bias_constraint=bias_constraint,

            use_transform=self.use_transform, 
            bit=self.bit,
            max_scale=self.max_scale,
            use_pruning=self.use_pruning,
            prun_weight=self.prun_weight,
        )

    def call(self, inputs, training=None):
        x = inputs
        x_se = tf.reduce_mean(x, axis=1, keepdims=True)
        x_se = self.conv_0(x_se)
        x_se = self.act(x_se)
        x_se = self.conv_1(x_se)
        x_se = tf.nn.sigmoid(x_se)
        x *= x_se
        return x

    def get_config(self):
        cfg = super().get_config()
        return cfg


# class SubPixelConv1D(layers.Layer):
#     def __init__(
#         self, 
#         filters:int, 
#         kernel_size, 
#         strides=1, 
#         padding='valid', 
#         data_format=None,
#         dilation_rate=1, 
#         use_bias=False,
#         kernel_initializer='glorot_uniform',
#         bias_initializer='zeros',
#         kernel_regularizer=None,
#         bias_regularizer=None,
#         activity_regularizer=None,
#         kernel_constraint=None,
#         bias_constraint=None,
#         # Custom
#         scale_ratio:int=2,
#         # Optimization
#         transform=None,
#         pruning=None,
#         bit=4,
#         max_scale=4.0,
#         prun_weight=0.5,
#         **kwargs
#     ):
#         super(SqueezeAndExcitation, self).__init__()
# 
#         self.conv = klayers.Conv1D(
#             filters * (scale_ratio ** 2), 
#             kernel_size,
#             strides=strides, 
#             padding=padding, 
#             data_format=data_format,
#             use_bias=use_bias, 
#             kernel_initializer=kernel_initializer, 
#             bias_initializer=bias_initializer, 
#             kernel_regularizer=kernel_regularizer,
#             bias_regularizer=bias_regularizer,
#             activity_regularizer=activity_regularizer,
#             kernel_constraint=kernel_constraint,
#             bias_constraint=bias_constraint,
# 
#             transform=True if transform is not None else False, 
#             bit=transform if transform is not None else 4,
#             max_scale=max_scale,
#             pruning=True if pruning is not None else False,
#             prun_weight=pruning if pruning is not None else 0.5,
#         )
#         self.sr = scale_ratio
# 
#     def call(self, inputs, training=None):
#         x = self.conv(inputs)
#         x = tf.nn.depth_to_space(x, self.sr)
#         return x
# 
#     def get_config(self):
#         cfg = super().get_config()
#         return cfg

@tf.keras.utils.register_keras_serializable()
class SubPixelConv2D(layers.Layer):
    def __init__(
        self, 
        filters:int, 
        kernel_size, 
        strides=(1,1), 
        padding='valid', 
        data_format=None,
        dilation_rate=(1,1), 
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
        # Optimization
        transform=None,
        pruning=None,
        bit=4,
        max_scale=4.0,
        prun_weight=0.5,
        **kwargs
    ):
        super(SubPixelConv2D, self).__init__()

        # Assign
        self.sr = scale_ratio

        self.use_transform = True if transform is not None else False
        self.bit = transform if transform is not None else 4
        self.max_scale = max_scale
        self.use_pruning = True if pruning is not None else False
        self.prun_weight = pruning if pruning is not None else 0.5

        # Conv
        self.conv = klayers.Conv2D(
            filters * (scale_ratio ** 2), 
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
        )

    def call(self, inputs, training=None):
        x = self.conv(inputs)
        x = tf.nn.depth_to_space(x, self.sr)
        return x

    def get_config(self):
        cfg = super().get_config()
        return cfg

@tf.keras.utils.register_keras_serializable()
class EmbeddingCosineSimilarity(layers.Layer):                                                        
    def __init__(
        self,
        classes:int,
        initializer='glorot_uniform',
        regularizer=None,
        dtype='float32',
        **kwargs
    ):
        super(EmbeddingCosineSimilarity, self).__init__(**kwargs)
        self.classes = classes
        self.initializer = initializer
        self.regularizer = regularizer
        self.op_dtype = dtype
                             
    def build(self, input_shape):
        self.channel = input_shape[-1]
        self.w = self.add_weight(
            name='weight',
            shape=(self.channel, self.classes),
            initializer=self.initializer,
            regularizer=self.regularizer,
            dtype=self.op_dtype,
        )
    
    def call(self, inputs, training=None):
        # normalize feature
        x = tf.nn.l2_normalize(x = tf.cast(inputs, self.op_dtype), axis=-1)
        x = x[..., None] * tf.ones((self.classes,), dtype=self.dtype) # (..., E, C)
        
        # normalize weights
        w = tf.nn.l2_normalize(tf.cast(self.w, self.dtype), axis=0)  # (E, C)
        w = tf.broadcast_to(w, tf.shape(x))     # (..., E, C)
        x = tf.reduce_sum(x * w, axis=-2) # (..., C)
        
        return x                                                                                      
    
    def get_config(self):
        config = {
            'classes' : self.classes,
            'initializer' : self.initializer,
            'regularizer' : self.regularizer,
            'dtype' : self.op_dtype,
        }
        base_config = super(EmbeddingCosineSimilarity, self).get_config()
        base_config.update(config)
        return base_config
