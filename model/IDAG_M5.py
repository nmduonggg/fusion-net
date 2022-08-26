"""
@author: nghiant
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from model.common import residual_stack

class IDAG_M5(nn.Module): #hardcode
    def __init__(self, scale=2):
        super(IDAG_M5, self).__init__()

        self.scale = scale

        self.conv = nn.ModuleList()

        self.conv.append(nn.Conv2d( 1, 64, 3, 1, 1)) #0
        self.conv.append(nn.Conv2d(64,  8, 1, 1, 0)) #1
        self.conv.append(nn.Conv2d( 8,  8, 3, 1, 1)) #2
        self.conv.append(nn.Conv2d( 8,  8, 3, 1, 1)) #3
        self.conv.append(nn.Conv2d( 8,  8, 3, 1, 1)) #4
        self.conv.append(nn.Conv2d( 8,  8, 3, 1, 1)) #5
        self.conv.append(nn.Conv2d(32, 64, 1, 1, 0)) #6

        self.conv.append(nn.Conv2d(64, scale * scale, 3, 1, 1)) #7:last layer
        
        # init_network:
        for i in range(len(self.conv)):
            self.conv[i].bias.data.fill_(0.01)
            nn.init.xavier_uniform_(self.conv[i].weight)

    def forward(self, x):
        z = x
        for i in range(6): # exclude the last layer
            z = F.relu(self.conv[i](z))
            if i == 2:
                c = z
            if i > 2 and i <= 5:
                c = torch.cat((c, z), 1)

        z = F.relu(self.conv[6](c))
        z = self.conv[7](z)

        y = residual_stack(z, x, self.scale)
        return y

    def save_dn_module(self, file_prefix):
        I = list(range(len(self.conv)))
        T = [ 0,  1,  2,  3,  4,  5,  6,  7]

        for i, t in zip(I, T):
            file_name = file_prefix + str(t)
            with open(file_name, 'w') as f:
                bias = self.conv[i].bias.data.numpy()
                weight = self.conv[i].weight.data.numpy().flatten()
                data = np.concatenate((bias, weight))
                data.tofile(f)