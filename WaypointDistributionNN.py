import numpy as np

import torch.optim as optim
import torch
import torch.nn as nn
import torch.nn.functional as F

class WaypointDistributionNN(nn.Module):
    def __init__(self, x_size):
        super(WaypointDistributionNN, self).__init__()
        c1 = 50
        k1 = 5
        s1 = 1
        p1 = 3
        
        c2 = 250
        k2 = 5
        s2 = 5
        p2 = 3
        
        c3 = 250
        k3 = 3
        s3 = 2
        p3 = 2
        
        self.conv1 = nn.Conv1d(1, c1, k1, stride=s1, padding=p1).double()
        self.conv2 = nn.Conv1d(c1, c2, k2, stride=s2, padding=p2).double()
        self.conv3 = nn.Conv1d(c2, c3, k3, stride=s3, padding=p3).double()
        x_size = floor((x_size + 2*p1 - k1)/s1 + 1)
        x_size = floor((x_size + 2*p2 - k2)/s2 + 1)
        x_size = floor((x_size + 2*p3 - k3)/s3 + 1)
        self.fc1 = nn.Linear(x_size, x_size).double()
        self.fc2 = nn.Linear(x_size, floor(x_size/10)).double()
        self.fc3 = nn.Linear(floor(x_size/10), 4*4+4).double()
        self.fc4 = nn.Linear(4*4+4, 4*4+4).double()
    
    def forward(self, x):
        x = F.relu(self.conv1(x.double()))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        y = self.fc4(x)
        return y
        
    def loss(self, y, alpha, delta, P):
        mu = y[0:4]
        A = y[4:].view(4,4)
        S = torch.t(A) * A
        Sinv = torch.inverse(S)
        dmu = P - mu
        return alpha*delta*(torch.log(torch.det(S)) - torch.t(dmu)*Sinv*dmu)/2
        
    def update(self,alpha,delta,P,state):
        loss = nn.MSELoss()
        optimizer = optim.Adam(self.net.parameters(), lr=alpha)
        optimizer.zero_grad()
        
        x = torch.from_numpy(state).double()
        output = self.forward(x).double()
        
        loss = self.loss(output, alpha, delta, P)
        
        target = torch.Tensor([G]).double()
        l = loss(output, target)
        l.backward()
        optimizer.step()
        
        return None
        
    def __call__(self,s):
        x = torch.from_numpy(s).double()
        y = self.net.forward(x)
        mu = y[0:4]
        A = y[4:].view(4,4)
        S = torch.t(A) * A
        return A.detach().numpy()[0], S.detach().numpy()[0]