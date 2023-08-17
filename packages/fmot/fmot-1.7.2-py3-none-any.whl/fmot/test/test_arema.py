import torch
import math
import fmot
import unittest
from fmot.nn.signal_processing import AREMA

def test_arema():
    # Define input parameters
    features = 16
    dim = 1
    attack_time = 0.1
    release_time = 0.2
    delta_t = 0.01

    # Create test input tensor
    batch_size = 2
    seq_len = 10
    input_tensor = torch.randn(batch_size, seq_len, features)

    # Instantiate the full-precision AREMA module
    full_precision_module = AREMA(features, dim, attack_time, release_time, delta_t)

    # Forward pass using full-precision model
    full_precision_output = full_precision_module(input_tensor)

    # Generate random calibration inputs
    num_samples = 5
    quant_inputs = [torch.randn(batch_size, seq_len, features) for _ in range(num_samples)]

    # Quantize the full-precision model using fmot
    cmodel = fmot.ConvertedModel(full_precision_module, batch_dim=0, seq_dim=1)
    cmodel.quantize(quant_inputs)
    fqir_graph = cmodel.trace()
    quantized_output = fqir_graph.run(input_tensor.numpy(), dequant=True)

    # Calculate root mean squared error (RMSE) between full-precision and quantized outputs
    rmse = torch.sqrt(torch.mean(torch.pow(full_precision_output - quantized_output, 2)))

    # Define the tolerance for RMSE
    tolerance = 0.2
    
    # Check if the RMSE is within the tolerance
    assert rmse <= tolerance ; f"Rmse {rmse} is not within tolerance {tolerance}"

if __name__ == '__main__':
    test_arema()
