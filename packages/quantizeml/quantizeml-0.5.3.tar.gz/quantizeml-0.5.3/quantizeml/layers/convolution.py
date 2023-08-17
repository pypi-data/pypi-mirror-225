#!/usr/bin/env python
# ******************************************************************************
# Copyright 2022 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

__all__ = ["PaddedConv2D", "QuantizedConv2D", "QuantizedConv2DTranspose"]

import tensorflow as tf

from keras import layers, backend
from keras.utils import conv_utils

from .layers_base import (register_quantize_target, rescale_outputs, tensor_inputs,
                          neural_layer_init, register_aligned_inputs)
from .quantizers import AlignedWeightQuantizer
from ..tensors import QTensor, QFloat, FixedPoint


def apply_padding(inputs, strides, kernel_size, padding_value):
    """Apply "SAME" padding to the inputs

    Args:
        inputs (:obj:`QFloat`): the inputs tensor.
        strides (tuple): the strides tuple.
        kernel_size (int): the kernel size.
        padding_value (:obj:`QFloat`): the padding value to apply.

    Returns:
        tf.Tensor: padded inputs.
    """
    _, h, w, _ = inputs.shape
    filter_width = kernel_size[0]
    filter_height = kernel_size[1]
    if h % strides[0] == 0:
        pad_along_height = max(filter_height - strides[0], 0)
    else:
        pad_along_height = max(filter_height - (h % strides[0]), 0)
    if w % strides[1] == 0:
        pad_along_width = max(filter_width - strides[1], 0)
    else:
        pad_along_width = max(filter_width - (w % strides[1]), 0)
    pad_top = pad_along_height // 2
    pad_bottom = pad_along_height - pad_top
    pad_left = pad_along_width // 2
    pad_right = pad_along_width - pad_left
    padding = [[0, 0], [pad_top, pad_bottom], [pad_left, pad_right], [0, 0]]

    return tf.pad(inputs, padding, "CONSTANT", padding_value)


@tf.keras.utils.register_keras_serializable()
class PaddedConv2D(layers.Conv2D):
    """A convolutional layer that can use a custom padding value.

    Note that when a padding value is provided, padding 'SAME' will be applied with the provided
    value (overriding 'padding' parameter).

    Args:
        padding_value (float, optional): the value used when padding for the 'same' convolution
            type. If None, zero-padding is used. Defaults to None.
    """

    def __init__(self, *args, padding_value=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Raise an error if the padding value is not a scalar
        if padding_value is not None:
            if tf.size(padding_value) != 1:
                raise ValueError(f"The padding value must be a scalar. Receives {padding_value}.")
            # When a custom padding_value is given, self.padding is overwritten and 'SAME' padding
            # will be done explicitly in the call.
            self._padding_value = tf.constant(padding_value)
            self.padding = 'valid'
        else:
            self._padding_value = None

    def call(self, inputs):
        # We need a custom padding for specifics padding values
        if self._padding_value is not None:
            # Note that we use the custom padding even when padding value is 0.
            inputs = apply_padding(inputs,
                                   list(self.strides),
                                   (self.kernel.shape[1], self.kernel.shape[0]),
                                   self._padding_value)

        outputs = self.convolution_op(inputs, self.kernel)

        if self.use_bias:
            outputs = tf.add(outputs, self.bias)
        return outputs

    def get_config(self):
        config = super().get_config()
        config["padding_value"] = self._padding_value
        return config


@register_quantize_target([layers.Conv2D, PaddedConv2D])
@register_aligned_inputs
@tf.keras.utils.register_keras_serializable()
class QuantizedConv2D(layers.Conv2D):
    """A convolutional layer that operates on quantized inputs and weights.

    Note that when a padding value is provided, padding 'SAME' will be applied with the provided
    value (overriding 'padding' parameter).

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
        padding_value (float, optional): the value used when padding for the 'same' convolution
            type. If None, zero-padding is used. Defaults to None.
    """
    @neural_layer_init(False)
    def __init__(self, *args, padding_value=None, quant_config=None, **kwargs):
        if padding_value is None:
            self.padding_value = None
        else:
            self.padding_value = float(padding_value)
            # Raise an error if the padding value is not a scalar
            if tf.size(padding_value) != 1:
                raise ValueError(f"The padding value must be a scalar. Receives {padding_value}.")
            # We quantize the padding_value with the same bitwidth as the weights
            self.padding_value_quantizer = AlignedWeightQuantizer(self.weight_quantizer.bitwidth,
                                                                  signed=True)
            # When a custom padding_value is given, self.padding is overwritten and 'SAME' padding
            # will be done explicitely in the call.
            self.padding = 'valid'

    @tensor_inputs([QTensor, tf.Tensor])
    @rescale_outputs
    def call(self, inputs):
        # Quantize the weights
        kernel = self.weight_quantizer(self.kernel)

        if self.padding_value is not None:
            # We need to align the padding value on the inputs, which is only supported for QFloat
            # Note that this restriction is purely to reduce the cognitive and test cost: should
            # we need at some point to support it, we could extend the AlignedWeightQuantizer or
            # wrap the inputs in a QFloat of scale 1.
            if not isinstance(inputs, QFloat):
                raise ValueError("When using a non-zero padding value, the inputs must be QFloat.")
            # Quantize and align padding_value on the inputs
            padding_value = self.padding_value_quantizer(self.padding_value, inputs)

            # Note that we use the custom padding even when padding value is 0.
            inputs = apply_padding(inputs,
                                   list(self.strides),
                                   (kernel.shape[1], kernel.shape[0]),
                                   padding_value)

        if isinstance(self.padding, str):
            tf_padding = self.padding.upper()
        else:
            tf_padding = self.padding

        outputs = tf.nn.convolution(inputs,
                                    kernel,
                                    strides=list(self.strides),
                                    padding=tf_padding,
                                    dilations=list(self.dilation_rate),
                                    data_format=self._tf_data_format,
                                    name=self.__class__.__name__)

        if self.use_bias:
            # Quantize bias and align it on the outputs
            bias = self.bias_quantizer(self.bias, outputs)
            outputs = tf.add(outputs, bias)

        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        if self.padding_value is not None:
            config["padding_value"] = self.padding_value
        return config


@register_quantize_target(layers.Conv2DTranspose)
@register_aligned_inputs
@tf.keras.utils.register_keras_serializable()
class QuantizedConv2DTranspose(layers.Conv2DTranspose):
    """A transposed convolutional layer that operates on quantized inputs and weights.

    Args:
        quant_config (dict, optional): the serialized quantization configuration. Defaults to None.
    """
    @neural_layer_init(False)
    def __init__(self, *args, quant_config=None, **kwargs):
        pass

    @tensor_inputs([FixedPoint])
    @rescale_outputs
    def call(self, inputs):
        # Quantize the weights
        # Conv2DTranspose weight shape is (h, w, filters, channels) which cannot be quantized
        # 'per-axis' as it is: the last dimension is not the output last dimension (i.e filters)
        # so it must be transposed to (h, w, channels, filters) before quantization to have the
        # appropriate frac_bits shape. Kernel values will then be transposed back to apply the
        # Tensorflow operation.
        kernel = self.weight_quantizer(tf.transpose(self.kernel, (0, 1, 3, 2)))

        # Prepare deconvolution output shape
        inputs_shape = tf.shape(inputs)
        batch_size, height, width = inputs_shape[0], inputs_shape[1], inputs_shape[2]
        kernel_h, kernel_w = self.kernel_size
        stride_h, stride_w = self.strides

        if self.output_padding is None:
            out_pad_h = out_pad_w = None
        else:
            out_pad_h, out_pad_w = self.output_padding

        # Infer the dynamic output shape
        out_height = conv_utils.deconv_output_length(height,
                                                     kernel_h,
                                                     padding=self.padding,
                                                     output_padding=out_pad_h,
                                                     stride=stride_h,
                                                     dilation=self.dilation_rate[0])
        out_width = conv_utils.deconv_output_length(width,
                                                    kernel_w,
                                                    padding=self.padding,
                                                    output_padding=out_pad_w,
                                                    stride=stride_w,
                                                    dilation=self.dilation_rate[1])

        output_shape = (batch_size, out_height, out_width, self.filters)
        output_shape_tensor = tf.stack(output_shape)

        # Do transposed convolution
        outputs = backend.conv2d_transpose(inputs, kernel, output_shape_tensor,
                                           self.strides, self.padding, self.data_format,
                                           self.dilation_rate)

        if self.use_bias:
            # Quantize biases and align them on the inputs
            bias = self.bias_quantizer(self.bias, outputs)
            # Add biases
            outputs = tf.add(outputs, bias)

        return outputs

    def get_config(self):
        config = super().get_config()
        config["quant_config"] = self.quant_config
        return config
