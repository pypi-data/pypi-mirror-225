
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class SimpleConvolutionalNetwork(nn.Module):
    def __init__(self, filter_layers, io_list, kernals, padding, linear_filter_input, latent_dim):
        super(SimpleConvolutionalNetwork, self).__init__()

        self.filter_layers = filter_layers
        self.io_list = io_list
        self.kernals = kernals
        self.padding = padding
        self.linear_filter_input = linear_filter_input
        self.latent_dim = latent_dim
        
        if filter_layers >= 1:
            self.conv1 = nn.Conv2d(io_list[0][0], io_list[0][1], kernals[0], padding = padding[0])
            self.pool1 = nn.MaxPool2d(2, stride=2, padding=0)

        if filter_layers >= 2:
            self.conv2 = nn.Conv2d(io_list[1][0], io_list[1][1], kernals[1], padding = padding[1])
            self.pool2 = nn.MaxPool2d(2, stride=2, padding=0)

        if filter_layers >= 3:
            self.conv3 = nn.Conv2d(io_list[2][0], io_list[2][1], kernals[2], padding = padding[2])
            self.pool3 = nn.MaxPool2d(2, stride=2, padding=0)

        self.fc1 = nn.Linear(latent_dim, 2000)
        self.fc2 = nn.Linear(2000, 304)
        self.fc3 = nn.Linear(304, 7)

    def forward(self, x):
        if self.filter_layers >= 1:
            x = F.tanh(self.conv1(x))
            x = self.pool1(x)

        if self.filter_layers >= 2:   
            x = F.tanh(self.conv2(x))
            x = self.pool2(x)

        if self.filter_layers >= 3:
            x = F.tanh(self.conv3(x))
            x = self.pool3(x)


        x = x.view(-1, self.latent_dim)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        
        return x

    def createlossandoptimizer(self, net, learning_rate=0.001):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(net.parameters(), lr=learning_rate)
        return criterion, optimizer
