"""Small causal TCN, shared architecture for pose and geometry-only FB0."""

from __future__ import annotations

import torch
from torch import nn


class CausalBlock(nn.Module):
    """Frozen causal temporal convolution architecture."""

    def __init__(self, channels: int, dilation: int, dropout: float) -> None:
        """Initialise frozen architecture dimensions."""
        super().__init__()
        self.pad = 2 * dilation
        self.conv = nn.Conv1d(channels, channels, 3, dilation=dilation, padding=self.pad)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Compute causal logits without looking at future samples."""
        y = self.conv(x)[:, :, : -self.pad]
        return torch.relu(x + self.dropout(torch.relu(y)))


class TCN(nn.Module):
    """Frozen causal temporal convolution architecture."""

    def __init__(
        self,
        inputs: int = 76,
        channels: int = 64,
        dilations: tuple[int, ...] = (1, 2, 4),
        dropout: float = 0.1,
    ) -> None:
        """Initialise frozen architecture dimensions."""
        super().__init__()
        self.input = nn.Conv1d(inputs, channels, 1)
        self.blocks = nn.Sequential(*(CausalBlock(channels, d, dropout) for d in dilations))
        self.head = nn.Linear(channels, 6)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Compute causal logits without looking at future samples."""
        return self.head(self.blocks(torch.relu(self.input(x.transpose(1, 2))))[:, :, -1])
