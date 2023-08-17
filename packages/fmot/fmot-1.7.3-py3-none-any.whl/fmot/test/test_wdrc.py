import torch
import math
import fmot
import unittest
from fmot.nn.signal_processing import WideDynamicRangeCompressor, DynamicRangeCompressor, Limiter


def test_wdrc_quantize():
    # Define input parameters
    compress_thresh = -20.0
    compress_ratio = 3.0
    lim_thresh = -10.0
    knee_width = 10.0

    # Create test input tensor
    batch_size = 2
    seq_len = 10
    dimension = 16

    # Generate random positive values for log-domain input tensor for calibration
    num_samples = 5
    calibration_inputs = [torch.log(torch.abs(torch.randn(batch_size, seq_len, dimension))) for _ in range(num_samples)]

    # Generate random positive values for log-domain input tensor for testing
    test_input = torch.log(torch.abs(torch.randn(batch_size, seq_len, dimension)))

    # Instantiate the full-precision WideDynamicRangeCompressor module
    full_precision_module = WideDynamicRangeCompressor(compress_thresh, compress_ratio, lim_thresh, knee_width)

    # Quantize the full-precision model using fmot
    cmodel = fmot.ConvertedModel(full_precision_module, batch_dim=0, seq_dim=1)
    cmodel.quantize(calibration_inputs)
    fqir_graph = cmodel.trace()

    # Run inference on the quantized model using the test input
    quantized_output = fqir_graph.run(test_input.numpy(), dequant=True)

    # Forward pass using full-precision model
    full_precision_output = full_precision_module(test_input)

    # Calculate root mean squared error (RMSE) between full-precision and quantized outputs
    rmse = torch.sqrt(torch.mean(torch.pow(full_precision_output - quantized_output, 2)))

    # Define the tolerance for RMSE
    tolerance = 1e-3

    # Check if the RMSE is within the tolerance
    assert rmse <= tolerance; f"Rmse {rmse} is not within tolerance {tolerance}"


def test_dynamic_range_compressor():
    threshold = -20
    knee_width = 4
    ratio = 3
    compressor = DynamicRangeCompressor(threshold=threshold, knee_width=knee_width, ratio=ratio)
    xG = torch.linspace(-30, 10, steps=40)  # Input tensor ranging from -30 to 10
    G = compressor(xG)
    ref_output = xG + G

    # Calculate expected output
    expected_output = torch.empty_like(xG)

    # Below compression threshold, output equals input
    mask = (xG < threshold - knee_width / 2)
    expected_output[mask] = xG[mask]
    
    # In the transition region for compression
    mask = (xG >= threshold - knee_width / 2) & (xG <= threshold + knee_width / 2)
    expected_output[mask] = xG[mask] + (1 / ratio - 1) * (xG[mask] - threshold + knee_width / 2) ** 2 / (2 * knee_width)

    # In the compression region
    mask = (xG > threshold + knee_width / 2)
    expected_output[mask] = threshold + (xG[mask] - threshold) / ratio

    assert torch.allclose(ref_output, expected_output, atol=1e-5)

def test_limiter():
    threshold = 0
    knee_width = 4
    limiter = Limiter(threshold=threshold, knee_width=knee_width)
    xG = torch.linspace(-10, 10, steps=40)  # Input tensor ranging from -10 to 10
    G = limiter(xG)

    # Calculate expected output
    expected_output = torch.empty_like(xG)

    # Below limiter threshold, output equals input
    mask = (xG < threshold - knee_width / 2)
    expected_output[mask] = xG[mask]
    
    # In the transition region for limiting
    mask = (xG >= threshold - knee_width / 2) & (xG <= threshold + knee_width / 2)
    expected_output[mask] = xG[mask] - (xG[mask] - threshold + knee_width / 2) ** 2 / (2 * knee_width)

    # In the limiting region
    mask = (xG > threshold + knee_width / 2)
    expected_output[mask] = threshold

    assert torch.allclose(xG + G, expected_output, atol=1e-5)



if __name__ == '__main__':
    test_dynamic_range_compressor()
    test_limiter()
