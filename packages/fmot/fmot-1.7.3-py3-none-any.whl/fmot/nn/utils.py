import torch
from torch import Tensor

def temporal_fold_transpose1d(input: Tensor, kernel_size: int, stride: int=1, dilation: int=1):
    """Base implementation of the transposed-fold-1d operation.
    
    Arguments:
        input (Tensor): input time-series to apply transposed fold, shape ``(B, Cin, Lin)``
            where ``Cin`` is divisible by kernel_size
        kernel_size (int): kernel size
        stride (int): stride
        dilation (int): dilation, **must be 1** (for now)

    Returns:
        tensor of shape ``(B, Cin // kernel_size, Lin * stride)``

    Steps at time t: (this isn't the implementation here, but an equivalent algorithm)
    `k`: kernel-size
    `s`: stride
    `m`: buffer-size, `m = max(k - s, 0)`
    1. input x is chunked into `kernel_size` subvectors [x_1, ..., x_k]
    2. add buffer to the first `m` subvectors: {x_i = x_i + b_i; i = 1, ..., m}
    3. the first `s` subvectors are output: {y_{t*s + i} = x_i, i = 1, ..., s}
    4. the remaining `m` subvectors are stored as new values for the buffer: {b_i <- x_{s + i}, i = 1, ..., m}

    Examples:

    k = 4, s = 2

        y  | b' || x  | b  |||   eq'n
        ------------------------
        y0 | -- || x0 | b0 ||| y0 = x0 + b0
        y1 | -- || x1 | b1 ||| y1 = x1 + b1
        -- | b0 || x2 | -- ||| b0 = x2
        -- | b1 || x3 | -- ||| b1 = x3

    k = 4, s = 1

        y  | b' || x  | b  |   eq'n
        ------------------------
        y0 | -- || x0 | b0 ||| y0 = x0 + b0
        -- | b0 || x1 | b1 ||| b0 = x1 + b1
        -- | b1 || x2 | b2 ||| b1 = x2 + b2
        -- | b2 || x3 | -- ||| b2 = x3

    k = 4, s = 3

        y  | b' || x  | b  |   eq'n
        ------------------------
        y0 | -- || x0 | b0 ||| y0 = x0 + b0
        y1 | -- || x1 | -- ||| y1 = x1
        y2 | -- || x2 | -- ||| y2 = x2
        -- | b0 || x3 | -- ||| b0 = x3

    """
    assert dilation == 1, f"dilation != 1 not yet supported for FoldTranspose1d."
    buffsize = int(max(kernel_size - stride, 0))
    
    batch, ch_in, length = input.shape
    
    assert ch_in % kernel_size == 0, f"Input channels ({ch_in}) must be divisible by kernel_size ({kernel_size})"

    dtype = input.dtype
    device = input.device

    ch_out = ch_in // kernel_size
    buffer = torch.zeros(batch, buffsize * ch_out, dtype=dtype, device=device)

    length_out = length * stride

    outs = torch.empty((batch, length_out, ch_out), dtype=dtype, device=device)

    for i, x in enumerate(input.unbind(dim=2)):
        bpad = torch.nn.functional.pad(buffer, (0, (kernel_size - buffsize) * ch_out))
        x = x + bpad
        y, buffer = torch.split(x, [stride * ch_out, buffsize * ch_out], dim=1)
        outs[:, i*stride:(i+1)*stride, :] = y.reshape(batch, stride, ch_out)
    
    outs = outs.transpose(1, 2)
    return outs