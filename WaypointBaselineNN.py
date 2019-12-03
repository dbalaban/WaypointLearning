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
        
        self.fc1 = nn.Linear(x_size, 32, bias=True).double()
        self.fc2 = nn.Linear(32, 32, bias=True).double()
        self.fc3 = nn.Linear(32, 1, bias=True).double()
        
        self.optimizer = optim.Adam(self.parameters(), lr=self.alpha)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        y = self.fc3(x)
        return y

    def __call__(self,s):
        x = torch.from_numpy(s).double()
        y = self.forward(x)
        return y.detach().numpy()[0]

    def update(self,Rs,state):
        loss = nn.MSELoss()
        self.optimizer.zero_grad()
        x = torch.from_numpy(state).double()
        output = self.forward(x)
        target = torch.from_numpy(Rs).double()
        l = loss(output, target.view(output.shape[0],1))/2
        l.backward()
        self.optimizer.step()
        
        return None