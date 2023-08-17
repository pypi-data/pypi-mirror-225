import torch
from torch import nn, Tensor
import fmot
from typing import *

class OptionalInputModel(fmot.nn.SuperStructure):
    def __init__(self):
        super().__init__()
        self.lin = nn.Linear(32, 32)

    def forward(self, x: Tensor, y: Optional[Tensor]):
        z = self.lin(x)
        if y is not None:
            z = self.lin(y)
        return y

def test_optional_inputs():
    model = OptionalInputModel()

    cmodel = fmot.ConvertedModel(model)

    cmodel.quantize([(torch.randn(32, 32), None), (torch.randn(32, 32), None)])
    graph = cmodel.trace()

if __name__ == '__main__':
    # test_optional_inputs()
    class MyModel(torch.nn.Module):
        def forward(self, x):
            return torch.atan(x)
        
    # smodel = torch.jit.script(MyModel())
    # print(smodel.graph)
    cmodel = fmot.ConvertedModel(MyModel())
    cmodel.quantize([torch.randn(8, 8) for _ in range(4)])
    graph = cmodel.trace()

    print(graph)