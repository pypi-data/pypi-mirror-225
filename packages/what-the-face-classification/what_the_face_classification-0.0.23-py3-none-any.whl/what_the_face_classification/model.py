
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

        self.fc1 = nn.Linear(latent_dim, linear_filter_input)
        self.fc2 = nn.Linear(linear_filter_input, 7)

    def forward(self, x):
        """
        Forward pass,
        x shape is 
        in the comments, we omit the batch_size in the shape
        """
        if self.filter_layers >= 1:
            x = F.relu(self.conv1(x))
            x = self.pool1(x)

        if self.filter_layers >= 2:   
            x = F.relu(self.conv2(x))
            x = self.pool2(x)

        if self.filter_layers >= 3:
            x = F.relu(self.conv3(x))
            x = self.pool3(x)

        # 
        x = x.view(-1, self.latent_dim)
        # 
        x = F.relu(self.fc1(x))
        # 64 -> 10
        # The softmax non-linearity is applied later (cf createLossAndOptimizer() fn)
        x = self.fc2(x)
        return x

    def createlossandoptimizer(self, net, learning_rate=0.001):
        # it combines softmax with negative log likelihood loss
        criterion = nn.CrossEntropyLoss()
        # optimizer = optim.SGD(self.parameters(), lr=learning_rate, momentum=0.9)
        optimizer = optim.Adam(net.parameters(), lr=learning_rate)
        return criterion, optimizer
