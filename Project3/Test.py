from torch import nn

conv1 = nn.Conv2d(1, 3, (3, 3))
conv2 = nn.Conv2d(3, 6, (1, 1))
# epoch4 = torch.load("./checkpoints/YourNet/epoch-4.pth", map_location=args.device)
# print(epoch4)

import torch.cuda

print(torch.__version__)
print(torch.cuda.is_available())

