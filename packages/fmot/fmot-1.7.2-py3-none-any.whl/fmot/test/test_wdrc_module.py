import torch
import math
import fmot
import unittest
from fmot.nn.signal_processing import WDRCModule


def test_wdrc_module():
    # Define input parameters
    sr = 16000
    n_fft = 512
    n_mels = 20
    attack_time = 0.01
    release_time = 0.1
    delta_t = 0.01
    compress_thresh = -20.0
    compress_ratio = 3.0
    lim_thresh = -10.0
    knee_width = 10.0
    seq_len_dim = 1

    # Create test input tensor
    batch_size = 2
    seq_len = 10
    feat_dim = 2 * (n_fft//2 + 1) # We stack real and complex components
    input_tensor = torch.randn(batch_size, seq_len, feat_dim)

    # Instantiate the full-precision WDRCModule
    full_precision_module = WDRCModule(sr, n_fft, n_mels, attack_time, release_time, delta_t, compress_thresh,
                                        compress_ratio, lim_thresh, knee_width, seq_len_dim)

    # Forward pass using full-precision model
    full_precision_output = full_precision_module(input_tensor)

    # Generate random calibration inputs
    num_samples = 5
    calibration_inputs = [torch.randn(batch_size, seq_len, feat_dim) for _ in range(num_samples)]

    # Quantize the full-precision model using fmot
    cmodel = fmot.ConvertedModel(full_precision_module, batch_dim=0, seq_dim=1)
    cmodel.quantize(calibration_inputs)
    fqir_graph = cmodel.trace()

    # Run inference on the quantized model using the test input
    quantized_output = fqir_graph.run(input_tensor.numpy(), dequant=True)

    # Calculate root mean squared error (RMSE) between full-precision and quantized outputs
    rmse = torch.sqrt(torch.mean(torch.pow(full_precision_output - quantized_output, 2)))

    # Define the tolerance for RMSE
    tolerance = 1e-1

    # Check if the RMSE is within the tolerance
    assert rmse <= tolerance

if __name__ == '__main__':
    test_wdrc_module()
