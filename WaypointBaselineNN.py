import numpy as np
from math import floor

import torch.optim as optim
import torch
import torch.nn as nn
import torch.nn.functional as F

class WaypointBaselineNN(nn.Module):
    def __init__(self, x_size, alpha, clamp):
        super(WaypointBaselineNN, self).__init__()
        self.alpha = alpha
        self.clamp = clamp
        
        self.fc1 = nn.Linear(x_size, x_size, bias=True).double()
        self.fc2 = nn.Linear(x_size, 1, bias=True).double()
        
    def forward(self, x):
        x = x[:,0,:]
        x = F.relu(self.fc1(x))
        y = self.fc2(x)
        return y

    def __call__(self,s):
        x = torch.from_numpy(s).double()
        y = self.forward(x)
        return y.detach().numpy()[0]

    def update(self,alpha,Cs,state):
        loss = nn.MSELoss()
        optimizer = optim.Adam(self.parameters(), lr=alpha)
        optimizer.zero_grad()
        x = torch.from_numpy(state).double()
        output = self(x).double()
        target = torch.from_numpy(Cs).double()
        l = loss(output, target)/2
        l.backward()
        optimizer.step()
        
        return None