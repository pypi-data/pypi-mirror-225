"""Miscellaneous shared modules which can be used in various models."""

from torch import Tensor
from torch.autograd.function import Function, FunctionCtx


class _InvertGrad(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, input: Tensor, scale: float) -> Tensor:  # type: ignore[override]
        ctx.scale = scale
        return input

    @staticmethod
    def backward(ctx: FunctionCtx, grad_output: Tensor) -> tuple[Tensor, None]:  # type: ignore[override]
        return grad_output * ctx.scale, None


def scale_grad(x: Tensor, scale: float) -> Tensor:
    """Scales the gradient of the input.

    Args:
        x: Input tensor.
        scale: Scale factor.

    Returns:
        The identity of the input tensor in the forward pass, and the scaled
        gradient in the backward pass.
    """
    return _InvertGrad.apply(x, scale)


def invert_grad(x: Tensor) -> Tensor:
    return scale_grad(x, -1.0)


class _SwapGrads(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        return x, y

    @staticmethod
    def backward(ctx: FunctionCtx, grad_x: Tensor, grad_y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        return grad_y, grad_x


def swap_grads(x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:
    """Swaps the gradients of the inputs.

    On the forward pass, this function returns the identity of the inputs.
    On the backward pass, the gradients of X and Y are swapped.

    Args:
        x: First input tensor.
        y: Second input tensor.

    Returns:
        The identity of the inputs in the forward pass, and the swapped
        gradients in the backward pass.
    """
    return _SwapGrads.apply(x, y)


class _CombineGrads(Function):
    @staticmethod
    def forward(ctx: FunctionCtx, x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        return x, y

    @staticmethod
    def backward(ctx: FunctionCtx, grad_x: Tensor, grad_y: Tensor) -> tuple[Tensor, Tensor]:  # type: ignore[override]
        grad = grad_x + grad_y
        return grad, grad


def combine_grads(x: Tensor, y: Tensor) -> tuple[Tensor, Tensor]:
    """Combines the gradients of the inputs.

    On the forward pass, this function returns the identity of the inputs.
    On the backward pass, the gradients of X and Y are summed.

    Args:
        x: First input tensor.
        y: Second input tensor.

    Returns:
        The identity of the inputs in the forward pass, and the summed
        gradients in the backward pass.
    """
    return _CombineGrads.apply(x, y)
