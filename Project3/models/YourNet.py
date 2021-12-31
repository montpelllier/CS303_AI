import torch
from torch import nn
import torch.nn.utils.prune as prune
import torch.nn.functional as F

class YourNet(nn.Module):
    ###################### Begin #########################
    # You can create your own network here or copy our reference model (LeNet5)
    # We will conduct a unified test on this network to calculate your score

    def __init__(self):
        super(YourNet, self).__init__()
        self.quant = torch.quantization.QuantStub()
        self.dequant = torch.quantization.DeQuantStub()
        # 1 input image channel, 6 output channels, 3x3 square conv kernel
        self.conv1 = nn.Conv2d(1, 3, (5, 5))
        self.conv2 = nn.Conv2d(3, 8, (4, 4))
        self.fc1 = nn.Linear(8 * 3 * 3, 32)  # 5x5 image dimension
        # self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(32, 10)

    def forward(self, x):
        x = self.quant(x)
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2)) #2维最大池化
        x = F.max_pool2d(F.relu(self.conv2(x)), 3)
        x = x.view(-1, int(x.nelement() / x.shape[0]))
        x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        x = self.fc3(x)
        x = self.dequant(x)
        return x

    ######################  End  #########################