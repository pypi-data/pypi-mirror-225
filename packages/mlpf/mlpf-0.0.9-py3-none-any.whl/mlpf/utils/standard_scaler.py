import torch
from torch import nn, Tensor


class StandardScaler(nn.Module):
    """
    Standard scaler transform as a torch module.
    """

    def __init__(self, features_train: Tensor):
        super(StandardScaler, self).__init__()

        self.mean = torch.mean(features_train, dim=0)
        self.std = torch.std(features_train, dim=0)
        self.std[self.std < 1e-9] = 1.0

    def forward(self, x: Tensor) -> Tensor:
        return (x - self.mean) / self.std

    def _apply(self, fn):
        super(StandardScaler, self)._apply(fn)
        self.mean = fn(self.mean)
        self.std = fn(self.std)

        return self

    def inverse(self, z: Tensor) -> Tensor:
        return z * self.std + self.mean
