import argparse
import os

import torch
from torch import nn
from torch.nn.utils import prune
from torch.optim import lr_scheduler
from torchvision import datasets, transforms

from Project3.models.YourNet import YourNet
from eval.metrics import get_accuracy

parser = argparse.ArgumentParser()

parser.add_argument('--checkpoint-dir', type=str, required=True)
parser.add_argument('--last-checkpoint', type=str, default=None)

parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], default='cpu')
parser.add_argument('--batch-size', type=int, default=64)
parser.add_argument('--epoch-start', type=int, default=0)
parser.add_argument('--epoch-end', type=int, required=True)

args = parser.parse_args()


def train(model, train_loader, test_loader, optimizer, loss_fn, scheduler):
    ###################### Begin #########################
    # You can write your training code here to optimize the reference model (LeNet5)
    for epoch in range(args.epoch_start, args.epoch_end):
        print(f"Epoch {epoch}\n-------------------------------")
        size = len(train_loader.dataset)

        model.train()

        for batch_idx, (X, y) in enumerate(train_loader):

            X, y = X.to(args.device), y.to(args.device)
            # Compute prediction error
            pred_y = model(X)
            loss = loss_fn(pred_y, y)

            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            scheduler.step()

            if batch_idx % 100 == 0:
                loss, current = loss.item(), batch_idx * len(X)
                # print(epoch, scheduler.get_lr()[0])
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

        accuracy = get_accuracy(model, test_loader, args.device)
        accuracy2 = get_accuracy(model, train_loader, args.device)
        print("Train Accuracy: %.3f" % accuracy2)
        print("Test Accuracy: %.3f}" % accuracy)

        torch.save(model.state_dict(), args.checkpoint_dir + f'epoch-{epoch}.pth')
    ######################  End  #########################


if __name__ == '__main__':
    ###################### Begin #########################
    # You can run your train() here
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(root='./data', train=True, download=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=args.batch_size, shuffle=True)  # ?????????????????????

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(root='./data', train=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=args.batch_size, shuffle=True)  # ?????????????????????

    model = YourNet().to(device=args.device)  # ???????????????????????????

    if args.last_checkpoint is not None:
        model.load_state_dict(torch.load(args.last_checkpoint, map_location=args.device))
    # torch.load???????????????model.load_state_dict??? state_dict ?????????????????????????????? Module ???????????????

    LR = 0.005
    # optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    optimizer = torch.optim.Adam(model.parameters(), lr=LR, betas=(0.9, 0.99), eps=1e-08)
    # ??????????????????sgd/momentum/Nesterov/adagrad/adadelta
    # SGD?????????????????????????????????????????????Momentum??????????????????AdaGrad??????????????????RMSProp???????????????alpha
    # Adam?????????m??????momentum ????????????????????????v??????adagrad?????????????????????????????????????????????m???V???????????????.

    scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=2, eta_min=1e-12)  # good 0.986
    # scheduler = lr_scheduler.ExponentialLR(optimizer, gamma=0.002) # terrible 0.101
    # scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, mode='min') #bad 0.943

    # ???????????????
    loss_fn = nn.CrossEntropyLoss()  # ??????????????????

    if not os.path.exists(args.checkpoint_dir):
        os.makedirs(args.checkpoint_dir)
    # ??????????????????

    # ????????????
    # parameters_to_prune = (
    #     (model.conv1, 'weight'),
    #     (model.conv2, 'weight'),
    #     (model.fc1, 'weight'),
    #     (model.fc2, 'weight'),
    #     (model.fc3, 'weight'),
    # )
    #
    # prune.global_unstructured(
    #     parameters_to_prune,
    #     pruning_method=prune.L1Unstructured,
    #     amount=0.2,
    # )
    #
    # prune.remove(model.conv1, 'weight')
    # prune.remove(model.conv2, 'weight')
    # prune.remove(model.fc1, 'weight')
    # prune.remove(model.fc2, 'weight')
    # prune.remove(model.fc3, 'weight')

    train(model, train_loader, test_loader, optimizer, loss_fn, scheduler)
    ######################  End  #########################
