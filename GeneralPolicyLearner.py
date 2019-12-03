import DataHandler as dh
import WaypointDistributionNN as wdnn
import WaypointBaselineNN as wbnn
import numpy as np
import csv
import os.path as path
from numpy.random import multivariate_normal as mltnrm
import torch
from PlotTrajectory import PlotTraj
import matplotlib.pyplot as plt

class GeneralPolicylearner():
    def __init__(self, net, baseline, data_handler,
                 steps, sample_size, checkpoint, test_size):
        self.net = net
        self.baseline = baseline
        self.handler = data_handler
        self.nwpts = sample_size
        self.steps = steps
        self.checkpoint = checkpoint
        self.test_size = test_size
        self.checkpoint_cost = float('inf')

    def GenerateProblem(self):
        prob = {}
        prob['dx'] = np.random.uniform(-2,2,2)
        prob['v0x'] = np.random.uniform(0,2)
        prob['vf'] = np.random.uniform(-2,2,2)
        prob['obs_offset'] = np.random.uniform(-0.08, 0.08)
        prob['obs_t'] = np.random.uniform(0.2, 0.8)
        return prob
    
    def TrainNSteps(self, prob):
        try:
            T_opt, _, _, x = self.handler.getOptimalSolution(
                                    prob['dx'], prob['v0x'], prob['vf'],
                                    prob['obs_t'], prob['obs_offset'])
        except:
            return 1
        
        x = x[0:23]
        obs_x=x[13]
        obs_y=x[14]
        
        for count in range(self.steps):
            mu, S = self.net(x)
            v = self.baseline(x)
            
            # T, T_col = self.handler.Evaluate(prob['dx'],prob['v0x'],prob['vf'],
            #                                  mu[0,:], obs_x, obs_y)
            # C = self.handler.GetCost(T_opt, T_col, T)
            wpts = mltnrm(mu[0,:], S[0,:], self.nwpts)
            Cs = []
            for i in range(self.nwpts):
                T, T_col = data_handler.Evaluate(prob['dx'],prob['v0x'],prob['vf'],
                                              wpts[i,:], obs_x, obs_y)
                C = data_handler.GetCost(T_opt, T_col, T)
                Cs += [C/self.nwpts]
            deltas = - (np.array(Cs) + baseline(x))
            baseline.update(-np.array(Cs), np.vstack([x]*self.nwpts))
            net.update(deltas, wpts, np.vstack([x]*self.nwpts))
        return 0
        
    def TestNetwork(self):
        C_tot = 0
        for i in range(self.test_size):
            prob = self.GenerateProblem()
            try:
                T_opt, _, _, x = self.handler.getOptimalSolution(
                                    prob['dx'], prob['v0x'], prob['vf'],
                                    prob['obs_t'], prob['obs_offset'])
            except:
                i -= 1
                continue
            x = x[0:23]
            obs_x = x[13]
            obs_y = x[14]
            mu, _ = self.net(x)
            
            T, T_col = data_handler.Evaluate(prob['dx'],prob['v0x'],prob['vf'],
                                             mu[0,:], obs_x, obs_y)
            C = data_handler.GetCost(T_opt, T_col, T)
            C_tot += C
        C_tot = C_tot / self.test_size
        print("Checkpoint Cost:")
        print(C_tot)
        if C_tot < self.checkpoint_cost:
            self.checkpoint_cost = C_tot
            torch.save(self.net.state_dict(), "best_found.nn")
        
    def TrainProblems(self):
        count = 0
        while True:
            if count == 0:
                self.TestNetwork()
            prob = self.GenerateProblem()
            code = self.TrainNSteps(prob)
            
            if code == 0:
                count = (count+1)%self.checkpoint

if __name__ == "__main__":
    data_handler = dh.DataHandler(10, "optimal_temp.csv", "eval_policy.csv", True, 2)
    net = wdnn.WaypointDistributionNN(23, 0.01, 1)
    if (path.exists("best_found.nn")):
        net.load_state_dict(torch.load("best_found.nn"))
    baseline = wbnn.WaypointBaselineNN(23, 0.01, 1e2)
    learner = GeneralPolicylearner(net, baseline, data_handler, 10, 100, 10, 1000)
    learner.TrainProblems()