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
"""
Rescaling transformation for quantized models.
"""

__all__ = ["align_rescaling"]

import numpy as np

from copy import deepcopy
from keras.layers import Rescaling, Conv2D, Dense

from .transforms_utils import get_layers_by_type, get_layers
from ..utils import apply_weights_to_model
from ...layers.convolution import PaddedConv2D


def _find_rescaling_fold_target(rescaling):
    """ Find the folding target and check limitations.

    Args:
        rescaling (keras.layers.Layer): the rescaling layer

    Returns:
        keras.layers.Layer: the layer that follows the Rescaling if a valid candidate, None
        otherwise.
    """
    # Define layers that can accept Rescaling alignment
    supported_dst_layers = [Conv2D, Dense]

    scale_per_axis = isinstance(rescaling.scale, (list, tuple)) and len(rescaling.scale) > 1
    if not scale_per_axis and rescaling.offset == 0:
        # Rescaling is already aligned: nothing to do
        return None
    # Alignment is limited to single outbound node Rescaling layers
    if len(rescaling.outbound_nodes) != 1:
        raise ValueError("Found a non-aligned Rescaling layer in the model with multiple outbounds "
                         "which is not supported.")
    # Retrieve the destination layer and check its type
    dst_layer = rescaling.outbound_nodes[0].layer
    if type(dst_layer) not in supported_dst_layers:
        raise ValueError(f"Layer type {type(dst_layer)} after Rescaling not supported, must be in "
                         f"{supported_dst_layers}.")
    # When destination layer is a Conv2D with padding 'same', reject:
    #   - offsets defined per axis,
    #   - scales defined per axis when offset is not null.
    # Otherwise it would require a padding value per-axis which is not supported.
    same_conv2d = (isinstance(dst_layer, Conv2D)
                   and dst_layer.get_config()['padding'].lower() == 'same')
    offset_per_axis = isinstance(rescaling.offset, (list, tuple)) and len(rescaling.offset) > 1
    if same_conv2d and (offset_per_axis or rescaling.offset != 0 and scale_per_axis):
        raise NotImplementedError("Folding an offset per-axis or with a scale per-axis into a "
                                  "Conv2D with 'same' padding is not supported.")
    return dst_layer


def _fold_rescaling(model, offset, dst_layer):
    """ Folds the rescaling offset into next layer.

    Args:
        model (keras.Model): the original model
        offset (float, list, tuple): the offset to fold
        dst_layer (keras.layer): the layer where offset will be folded

    Returns:
        keras.Model: the updated model
    """
    # Copy configuration before applying modifications
    config = deepcopy(model.get_config())
    # Fold rescaling by editing the model configuration
    dst_config = get_layers(config, [dst_layer.name])[0]
    # Force bias
    dst_config['config']['use_bias'] = True
    # Replace Conv2D with 'same' padding by PaddedConv2D with correct padding value
    if isinstance(dst_layer, Conv2D) and dst_layer.padding.lower() == 'same':
        # Offset has a single value at this point
        if isinstance(offset, (list, tuple)):
            offset = offset[0]
        dst_config['config']['padding_value'] = float(-offset)
        dst_config['class_name'] = 'PaddedConv2D'

    # Reconstruct model from the config
    aligned_model = model.from_config(config, custom_objects={"PaddedConv2D": PaddedConv2D})

    # Restore model weights
    variables_dict = {var.name: var for var in model.variables}
    apply_weights_to_model(aligned_model, variables_dict, False)
    return aligned_model


def _set_folded_weights(rescaling_layer, dst_layer, had_bias):
    """ Sets folded weights in the given layers.

    Args:
        rescaling_layer (keras.layers.Layer): the Rescaling layer
        dst_layer (keras.layers.Layer): the layer where Rescaling is folded
        had_bias (bool): whether the original layer had a bias or not
    """
    base_weights = dst_layer.get_weights()
    new_w = base_weights[0].copy()
    filters = new_w.shape[-1]

    scale = rescaling_layer.scale
    if isinstance(scale, (list, tuple)) and len(scale) > 1:
        # If scale is not a scalar, align it
        target_scale = np.mean(scale)
        rescaling_layer.scale = target_scale
        # To compensate, adjust the weights of the next layer
        for i in range(filters):
            # Rescale weights filter by filter to enable broadcast
            new_w[..., i] *= scale / target_scale
        if isinstance(dst_layer, PaddedConv2D):
            # Also rescale the padding value
            dst_layer._padding_value *= scale / target_scale
    new_weights = [new_w]

    if dst_layer.use_bias:
        # Build zero initialized biases if the original layer didn't have any
        new_biases = base_weights[1].copy() if had_bias else np.zeros(filters)
        for i in range(filters):
            # Rescale biases filter by filter to enable broadcast if offsets are per channel
            w_i = base_weights[0][..., i]
            new_biases[i] += np.sum(w_i * rescaling_layer.offset)
        new_weights += [new_biases]
        rescaling_layer.offset = 0

    dst_layer.set_weights(new_weights)


def align_rescaling(model):
    """Aligns the Rescaling layer of the model to make it quantization ready.

    This aligns the Rescaling scale to a single scalar, adjusting the weights of
    the next layer.

    This also folds the offset into the bias of next layer.

    The resulting Rescaling is therefore compatible with a quantization to a
    QuantizedRescaling.

    If the source model does not contain a Rescaling or if its Rescaling is already
    aligned, then the original model is returned.

    Args:
        model (keras.Model): the source Keras model

    Returns:
        keras.Model: the original model or a new model with Rescaling layer aligned
    """
    # Check if the model has a Rescaling layer and return the original model if not
    rescaling_layer = get_layers_by_type(model, Rescaling)
    if not rescaling_layer:
        return model

    # Limit alignment to the first rescaling layer (a model should only have one)
    rescaling_layer = rescaling_layer[0]

    # Find folding target and check limitations
    dst_layer = _find_rescaling_fold_target(rescaling_layer)

    # If no folding target was found return the original model
    if dst_layer is None:
        return model

    # If there is a rescaling offset, it is folded in the dst_layer
    offset = rescaling_layer.offset
    if offset != 0:
        aligned_model = _fold_rescaling(model, offset, dst_layer)
    else:
        aligned_model = model

    # Set weights in the layers of the new model
    _set_folded_weights(aligned_model.get_layer(rescaling_layer.name),
                        aligned_model.get_layer(dst_layer.name),
                        dst_layer.use_bias)
    return aligned_model
