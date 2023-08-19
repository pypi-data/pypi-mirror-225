# Copyright 2023 The Jaxonnxruntime Authors.
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

# Copyright 2023 The Jaxonnxruntime Authors.
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
"""Define ONNX ReduceMax operator."""
from collections.abc import Callable, Sequence
import functools
from typing import Any

from jax import jit
from jax import numpy as jnp
from jaxonnxruntime.core import handler
from jaxonnxruntime.core import onnx_node


@handler.register_op('ReduceMax')
class ReduceMax(handler.Handler):
  """Implementation of the ONNX ReduceMax operator."""

  @classmethod
  def _prepare(
      cls, node: onnx_node.OnnxNode, inputs: Sequence[Any], onnx_jax_impl: Any
  ):
    node.attrs_dict['axes'] = node.attrs.get('axes')
    if len(inputs) >= 2:
      node.attrs_dict['axes'] = tuple(inputs[1].tolist())
      node.attrs_dict['axes'] = (
          None if len(node.attrs_dict['axes']) == 0 else node.attrs_dict['axes']
      )
    node.attrs_dict['keepdims'] = node.attrs.get('keepdims', 1)
    node.attrs_dict['noop_with_empty_axes'] = node.attrs.get(
        'noop_with_empty_axes', 0
    )

  @classmethod
  def version_13(
      cls, node: onnx_node.OnnxNode, inputs: Sequence[Any]
  ) -> Callable[..., Any]:
    """ONNX version_13 ReduceMax op."""
    cls._prepare(node, inputs, onnx_reducemax)
    return onnx_reducemax

  @classmethod
  def version_18(
      cls, node: onnx_node.OnnxNode, inputs: Sequence[Any]
  ) -> Callable[..., Any]:
    """ONNX version_18 ReduceMax op."""
    cls._prepare(node, inputs, onnx_reducemax)
    return onnx_reducemax


@functools.partial(
    jit, static_argnames=('axes', 'keepdims', 'noop_with_empty_axes')
)
def onnx_reducemax(
    *input_args,
    axes=None,
    keepdims=1,
    noop_with_empty_axes=0,
):
  """The impl for https://github.com/onnx/onnx/blob/v1.12.0/docs/Operators.md#ReduceSum."""
  assert len(input_args) == 1 or len(input_args) == 2
  data = input_args[0]
  if axes is None and noop_with_empty_axes > 0:
    return data
  return jnp.max(data, axis=axes, keepdims=keepdims > 0)
