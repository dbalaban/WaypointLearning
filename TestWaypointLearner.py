import DataHandler as dh
import WaypointDistributionNN as wdnn
import numpy as np
from numpy.random import multivariate_normal as mltnrm

def Train1Prob(dx, v0x, vf, obs_t, obs_offset):
    data_handler = dh.DataHandler(500, "optimal_nn.csv", "eval_nn.csv", True)
    T_opt, _, _, x = data_handler.getOptimalSolution(
                            dx, v0x, vf, obs_t, obs_offset)
    
    net = wdnn.WaypointDistributionNN(len(x), 0.001)
    
    while True:        
        mu, S = net(x)
        print(mu)
        print(np.mean(S))
        wpts = mltnrm(mu[0,:], S, 100)
        Cs = []
        C_tot = 0
        for i in range(1000):
            T, T_col = data_handler.Evaluate(
                dx, v0x, vf, wpts[i], obs_t, obs_offset)
            C = data_handler.GetCost(T_opt, T_col, T)
            Cs += [C/100]
            C_tot += C
        print(C_tot/100)
        print(wpts.shape)
        net.update(Cs, wpts, x)

def TestNet():
    # net = wdnn.WaypointDistributionNN(4, 0.01) # learns mu, not sigma
    net = wdnn.WaypointDistributionNN(4, 0.00001)
    nsamples = 100
    x = np.ones(4)
    count = 0
    while count < 10000:
        count += 1
        mu, S = net(x)
        print(mu)
        # print(S)
        print(np.sum(S))
        wpts = mltnrm(mu[0,:], S, nsamples)
        Cs = np.linalg.norm(wpts, axis=1)
        #print(Cs)
        print(np.sum(Cs)/nsamples)
        net.update(Cs, wpts, np.vstack([x]*nsamples))

if __name__ == "__main__":
    TestNet()
    dx = np.array([0, 1])
    v0x = 1
    vf = np.array([0, 1])
    obs_t=0.5
    obs_offset=0.0
    # Train1Prob(dx, v0x, vf, obs_t, obs_offset)