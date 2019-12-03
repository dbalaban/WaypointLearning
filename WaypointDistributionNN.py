import numpy as np
from math import floor
import torch
import torch.optim as optim

import torch.nn as nn
import torch.nn.functional as F

class WaypointDistributionNN(nn.Module):
    def __init__(self, x_size, alpha, clamp):
        super(WaypointDistributionNN, self).__init__()
        self.alpha = alpha
        self.clamp = clamp
        
        # c1 = 50
        # k1 = 5
        # s1 = 1
        # p1 = 3
        # 
        # c2 = 250
        # k2 = 5
        # s2 = 5
        # p2 = 3
        # 
        # c3 = 250
        # k3 = 3
        # s3 = 2
        # p3 = 2
        # self.conv1 = nn.Conv1d(1, c1, k1, stride=s1, padding=p1).double()
        # self.conv2 = nn.Conv1d(c1, c2, k2, stride=s2, padding=p2).double()
        # self.conv3 = nn.Conv1d(c2, c3, k3, stride=s3, padding=p3).double()
        # x_size = floor((x_size + 2*p1 - k1)/s1 + 1)
        # x_size = floor((x_size + 2*p2 - k2)/s2 + 1)
        # x_size = floor((x_size + 2*p3 - k3)/s3 + 1)
        # x_size = x_size*c3
        # self.fc1 = nn.Linear(x_size, x_size).double()
        # self.fc2 = nn.Linear(x_size, floor(x_size/10)).double()
        # self.fc3 = nn.Linear(floor(x_size/10), 4*4+4).double()
        # self.fc4 = nn.Linear(4*4+4, 4*4+4).double()
        # self.fc5 = nn.Linear(4*4+4, 4*4+4).double()
        # self.fc5.weight.data = torch.diag(torch.tensor([1] * 20)).double()
        
        self.fc1 = nn.Linear(x_size, 32, bias=True).double()
        self.fc2 = nn.Linear(32, 32, bias=False).double()
        # self.fc2.weight.data[:,:] = torch.tensor([0.38167919,  0.39101533, -0.44043292,  0.05524485, 1, 1, 1, 1]).view(8,1)
        # print(self.fc2.weight.data.shape)
        self.fc3 = nn.Linear(32,8, bias=True).double()
        # print(self.fc3.weight.data.shape)
        # self.fc1.weight.data = torch.diag(torch.tensor([1]*x_size)).double()
        # self.fc2.weight.data[0:4,0] = torch.tensor([0]*4).double()
        # self.fc2.weight.data[4:,0] = torch.tensor([1]*4).double()
        # self.fc2.weight.data[4:,:] = torch.diag(torch.tensor([1]*4)).double()
        self.fc3.weight.data[:,4:] *= 10
        self.optimizer = optim.Adam(self.parameters(), lr=self.alpha)
    
    def forward(self, x):
        # x = F.relu(self.conv1(x.double()))
        # x = F.relu(self.conv2(x))
        # x = F.relu(self.conv3(x))
        # x = x.view(-1, self.num_flat_features(x))
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        # x = self.fc4(x)
        # x[:,4:] = torch.abs(x[:,4:].clone())
        # y = self.fc5(x)
        # y[:,4:] = torch.abs(y[:,4:].clone())
        # x = x[:,0,:]
        # x = F.relu(self.fc1(x))
        # print(x.shape)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        y = self.fc3(x)
        # y = self.fc2(x)
        return y
        
    def loss(self, y, delta, P):
        total = torch.tensor([0])
        mu = y[:,0:4]
        #mu.register_hook(lambda grad: print("gradient:"+str(grad)))
        dmu = (P - mu).view(y.shape[0], 4, 1)
        dmut = dmu.permute(0,2,1)
        dot = torch.bmm(dmut, dmu).view(y.shape[0])/2
        #print("dot product:")
        print(dot)
        weight_dot = delta*dot
        #print("weighted:")
        #print(weight_dot)
        total = weight_dot.sum()/y.shape[0]
        # print(total)
        return total
        for i in range(y.shape[0]):
            mu = y[i,0:4].clone().view(4,1)
            A = y[i,4:].clone().view(4,4)
            p = P[i,:].clone().view(4,1)
            #S = torch.mm(A, torch.t(A))
            S = torch.diag(torch.tensor([0.001]*4)).double()
            Sinv = torch.inverse(S)
            dmu = p.clone() - mu.clone()
            dot = torch.mm(torch.mm(torch.t(dmu),Sinv),dmu).clone()
            # log = torch.log(torch.det(S))
            log = 0
            total = total.clone() + delta[i]*(log + dot.clone())/2
        #print(total)
        return total/y.shape[0]
        
    def update(self,deltas,P,state):
        self.optimizer.zero_grad()
        
        x = torch.from_numpy(state).double()
        y = self.forward(x)
        mu = y[:,0:4]
        sig = y[:,4:]
        S = torch.diag_embed(torch.mul(sig,sig))
        Sinv = torch.inverse(S)
        P = torch.from_numpy(P)
        dmu = (mu-P).view(x.shape[0], 1, 4)
        # print(Sinv.shape)
        # print(dmu.shape)
        Sinvdmu = torch.bmm(Sinv, dmu.permute(0,2,1))
        # Sinvdmu = dmu.permute(0,2,1)
        dotprod = torch.bmm(dmu, Sinvdmu).view(x.shape[0])
        det = torch.log(torch.det(S))
        detpdotprod = -(dotprod + det)/2
        weighted = detpdotprod*torch.from_numpy(deltas).view(x.shape[0])
        loss = -weighted.sum()/x.shape[0]
        # print(loss)
        # print(detpdotprod)
        loss.backward()
        # print(self.fc2.weight.data)
        # print(loss)
        # dw = self.alpha*torch.mm(torch.mm(y-P, subgrad),x.t())/x.shape[1]
        # dw = torch.mm(torch.mm(y-P, subgrad),x.t())/x.shape[1]
        # print(dw)
        # print(dw)
        # self.fc2.weight.data += dw
        # det.register_hook(lambda grad: print(grad))
        self.fc2.weight.register_hook(lambda grad: grad.clamp_(-self.clamp,self.clamp))
        # self.fc2.weight.register_hook(lambda grad: print(grad))
        self.optimizer.step()
        # print(self.fc2.weight.grad)
        
        return None
    
    def num_flat_features(self, x):
        size = x.size()[1:]  # all dimensions except the batch dimension
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

    def __call__(self,s):
        x = torch.from_numpy(s).double()
        y = self.forward(x.unsqueeze(0))
        mu = y[:,0:4]
        sig = y[:,4:]
        S = torch.diag_embed(torch.mul(sig,sig))
        # S = torch.from_numpy(np.identity(4))
        return mu.detach().numpy(), S.detach().numpy()