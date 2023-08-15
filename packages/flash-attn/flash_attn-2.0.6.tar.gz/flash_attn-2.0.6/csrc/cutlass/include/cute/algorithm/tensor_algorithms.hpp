/***************************************************************************************************
 * Copyright (c) 2023 - 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: BSD-3-Clause
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this
 * list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 **************************************************************************************************/
/** Common algorithms on (hierarchical) tensors */

#pragma once

#include <cute/config.hpp>

#include <cute/tensor.hpp>

namespace cute
{

//
// for_each
//

template <class Engine, class Layout, class UnaryOp>
CUTE_HOST_DEVICE constexpr
void
for_each(Tensor<Engine,Layout> const& tensor, UnaryOp&& op)
{
  CUTE_UNROLL
  for (int i = 0; i < size(tensor); ++i) {
    static_cast<UnaryOp&&>(op)(tensor(i));
  }
}

template <class Engine, class Layout, class UnaryOp>
CUTE_HOST_DEVICE constexpr
void
for_each(Tensor<Engine,Layout>& tensor, UnaryOp&& op)
{
  CUTE_UNROLL
  for (int i = 0; i < size(tensor); ++i) {
    static_cast<UnaryOp&&>(op)(tensor(i));
  }
}

// Accept mutable temporaries
template <class Engine, class Layout, class UnaryOp>
CUTE_HOST_DEVICE constexpr
void
for_each(Tensor<Engine,Layout>&& tensor, UnaryOp&& op)
{
  return for_each(tensor, static_cast<UnaryOp&&>(op));
}

//
// transform
//

// Similar to std::transform but does not return number of elements affected
template <class Engine, class Layout, class UnaryOp>
CUTE_HOST_DEVICE constexpr
void
transform(Tensor<Engine,Layout>& tensor, UnaryOp&& op)
{
  CUTE_UNROLL
  for (int i = 0; i < size(tensor); ++i) {
    tensor(i) = static_cast<UnaryOp&&>(op)(tensor(i));
  }
}

// Accept mutable temporaries
template <class Engine, class Layout, class UnaryOp>
CUTE_HOST_DEVICE constexpr
void
transform(Tensor<Engine,Layout>&& tensor, UnaryOp&& op)
{
  return transform(tensor, std::forward<UnaryOp>(op));
}

// Similar to std::transform transforms one tensors and assigns it to another
template <class EngineIn, class LayoutIn, class EngineOut, class LayoutOut, class UnaryOp>
CUTE_HOST_DEVICE constexpr
void
transform(Tensor<EngineIn,LayoutIn>& tensor_in, Tensor<EngineOut,LayoutOut>& tensor_out, UnaryOp&& op)
{
  CUTE_UNROLL
  for (int i = 0; i < size(tensor_in); ++i) {
    tensor_out(i) = static_cast<UnaryOp&&>(op)(tensor_in(i));
  }
}

// Accept mutable temporaries
template <class EngineIn, class LayoutIn, class EngineOut, class LayoutOut, class UnaryOp>
CUTE_HOST_DEVICE constexpr
void
transform(Tensor<EngineIn,LayoutIn>&& tensor_in, Tensor<EngineOut,LayoutOut>&& tensor_out, UnaryOp&& op)
{
  return transform(tensor_in, tensor_out, std::forward<UnaryOp>(op));
}

} // end namespace cute
