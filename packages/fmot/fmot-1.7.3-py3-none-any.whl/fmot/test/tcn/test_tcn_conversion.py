import torch
from fmot.nn.conv1d import TemporalConv1d, convert_tcn_to_unfold
from contextlib import nullcontext
import pytest

@pytest.mark.parametrize('bias', [True, False], ids=['bias', 'no_bias'])
@pytest.mark.parametrize('depthwise', [True, False], ids=['depthwise', 'standard'])
@pytest.mark.parametrize(['kernel_size', 'dilation'], [[3, 1], [3, 2], [1, 1]], ids=['k3_d1', 'k3_d2', 'k1_d1'])
@pytest.mark.parametrize(['in_channels', 'out_channels'], [[32, 32], [32, 64]])
@torch.no_grad()
def test_unfold_conversion_matching(in_channels: int, out_channels: int, kernel_size: int, dilation: int, depthwise: bool, bias: bool):

    if depthwise:
        groups = in_channels
    else:
        groups = 1

    kwargs = dict(
        in_channels = in_channels,
        out_channels = out_channels,
        kernel_size = kernel_size,
        dilation = dilation,
        groups = groups,
        bias = bias
    )

    print(f'depthwise = {depthwise}')
    print(kwargs)

    if depthwise and in_channels != out_channels:
        ctx = pytest.raises(Exception)
    else:
        ctx = nullcontext()

    with ctx:
        tcn = TemporalConv1d(**kwargs)
        converted = convert_tcn_to_unfold(tcn)

        x = torch.randn(8, in_channels, 16)
        y0 = tcn(x)
        y1 = converted(x)

        print(y0.shape)
        print(y1.shape)

        mse = (y0 - y1).pow(2).mean()
        assert mse <= 1e-6, f'MSE was {mse} ({type(converted)})'

        print(f'{type(converted)} passed comparison test')

if __name__ == '__main__':
    test_unfold_conversion_matching(32, 32, 3, 2, False, False)