from torch import nn


class DebugNet(nn.Module):
    def __init__(self, in_channels, out_channels, mid_channels=128, bilinear=True):
        super(DebugNet, self).__init__()
        self.bilinear = bilinear
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(mid_channels),
            nn.ReLU(inplace=True),
        )
        self.conv2 = nn.Conv2d(mid_channels, out_channels, kernel_size=1)
        

    def forward(self, x):
        x = self.conv(x)
        logits = self.conv2(x)
        return logits