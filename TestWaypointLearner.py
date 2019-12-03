import DataHandler as dh
import WaypointDistributionNN as wdnn
import WaypointBaselineNN as wbnn
import numpy as np
import csv
from numpy.random import multivariate_normal as mltnrm
import torch
#from PlotTrajectory import PlotTraj
import matplotlib.pyplot as plt

def getSampleValues(n, value_range, isLogScale=False) :
  if isLogScale :
    value_range = np.log(np.array(value_range)).tolist()
  values = (value_range[1] - value_range[0])*(np.arange(0,n))/(n-1) + value_range[0]
  if isLogScale :
    values = np.exp(np.array(values))
  return values.tolist()

def Train1Prob(dx, v0x, vf, obs_t, obs_offset, use_baseline=True):
    data_handler = dh.DataHandler(10, "optimal_nn.csv", "eval_nn.csv", True, 1)
    T_opt, _, _, x = data_handler.getOptimalSolution(
                            dx, v0x, vf, obs_t, obs_offset)
    obs_x=x[13]
    obs_y=x[14]
    print(obs_x)
    print('done')
    print(obs_y)
    
    f = open("wpt_data.csv", "w+")
    f_writer = csv.writer(f, delimiter=',')
    if use_baseline:
        f_writer.writerow(["mu_x", "mu_y", "mu_vx", "mu_vy",
                        "var_x", "var_y", "var_vx", "var_vy",
                        "mu_cost", "avg_cost", "baseline_error"])
    else:
        f_writer.writerow(["mu_x", "mu_y", "mu_vx", "mu_vy",
                        "var_x", "var_y", "var_vx", "var_vy",
                        "mu_cost", "avg_cost"])
        
    f.close()
    
    x = np.ones(1)
    nsamples = 100
    net = wdnn.WaypointDistributionNN(len(x), 0.01, 1)
    baseline = wbnn.WaypointBaselineNN(len(x), 0.01, 1e2)
    fig,ax1=plt.subplots()
    n = 1000
    if use_baseline:
        data = np.zeros([n, 11])
    else :
        data = np.zeros([n, 10])
    for count in range(n):      
        mu, S = net(x)
        data[count,0:4] = mu
        data[count,4:8] = np.diag(S[0,:])
        print(mu)
        print(np.sum(S))
        T, T_col = data_handler.Evaluate(dx, v0x, vf, mu[0,:], obs_x, obs_y)
        C = data_handler.GetCost(T_opt, T_col, T)
        data[count, 8] = C
        print("Cost at mu:")
        print(C)
        wpts = mltnrm(mu[0,:], S[0,:], nsamples)
#        if count>990:
#            PlotTraj(dx, v0x, vf, obs_t, obs_offset,wpts,ax1)
#            
        Cs = []
        C_tot = 0
        print("average cost of distribution:")
        for i in range(nsamples):
            T, T_col = data_handler.Evaluate(
                dx, v0x, vf, wpts[i,:], obs_x, obs_y)
            C = data_handler.GetCost(T_opt, T_col, T)
            Cs += [C/nsamples]
            C_tot += C
        print(C_tot/nsamples)
        data[count, 9] = C_tot/nsamples
        if use_baseline:
            deltas = - (np.array(Cs) + baseline(x))
            print("baseline error:")
            print(np.sum(np.abs(deltas)))
            data[count, 10] = np.sum(np.abs(deltas))
            baseline.update(-np.array(Cs), np.vstack([x]*nsamples))
            net.update(deltas, wpts, np.vstack([x]*nsamples))
        else:
            net.update(-np.array(Cs), wpts, np.vstack([x]*nsamples))
        f = open("wpt_data.csv", "a")
        f_writer = csv.writer(f, delimiter=',')
        f_writer.writerow(data[count,:])
        f.close()
        
    best = np.argmin(data[:,8])
    print(data[best,:])
    data_handler.Evaluate(dx, v0x, vf, data[best,0:4], obs_x, obs_y)

def GetBestModel(clamp, lr, ss, n, steps, dx, v0x, vf, obs_t, obs_offset):
    data_handler = dh.DataHandler(10, "optimal_nn.csv", "eval_nn.csv", True, 2)
    T_opt, _, _, x = data_handler.getOptimalSolution(
                            dx, v0x, vf, obs_t, obs_offset)
    obs_x=x[13]
    obs_y=x[14]
    best_cost = float('inf')
    best_mu = float('inf')*np.ones(4)
    best_sig = float('inf')*np.ones(4)
    for i in range(n):
        net = wdnn.WaypointDistributionNN(len(x), lr, clamp)
        count = 0
       
        while count < steps:
            count += 1
            mu, S = net(x)
            mu = mu[0,:]
            S = S[0,:,:]
            sig = np.diag(S)
            wpts = mltnrm(mu, S, ss)
            Cs = []
            C_tot = 0
            for i in range(ss):
                T, T_col = data_handler.Evaluate(
                    dx, v0x, vf, wpts[i,:], obs_x, obs_y)
                C = data_handler.GetCost(T_opt, T_col, T)
                Cs += [C/ss]
                C_tot += C
            C_avg = C_tot / ss
            if C_avg < best_cost:
                best_cost = C_avg
                best_mu[:] = mu
                best_sig[:] = sig
            net.update(-np.array(Cs), wpts, np.vstack([x]*ss))
    return best_cost, best_mu, best_sig

def HyperSearch(dx, v0x, vf, obs_t, obs_offset):
    clamp_values = getSampleValues(10, [1e-1, 1e4], True)
    lr_values = getSampleValues(10, [1e-5, 1e-1], True)
    ss_values = np.floor(getSampleValues(5, [1e0, 2e2], False)).astype(np.int)
    n = 5
    steps = 10
    
    best_costs = float('inf')*np.ones([10,10,5])
    best_values = np.zeros([10,10,5,8])
    hyper = np.zeros([10,10,5,3])
    for clamp_idx in range(len(clamp_values)):
        for lr_idx in range(len(lr_values)):
            for ss_idx in range(len(ss_values)):
                clamp = clamp_values[clamp_idx]
                lr = lr_values[lr_idx]
                ss = ss_values[ss_idx]
                hyper[clamp_idx, lr_idx, ss_idx, :] = np.array([clamp, lr, ss])
                C, mu, sig = GetBestModel(clamp, lr, ss, n, steps, dx,
                                          v0x, vf, obs_t, obs_offset)
                best_costs[clamp_idx, lr_idx, ss_idx] = C
                best_values[clamp_idx, lr_idx, ss_idx, 0:4] = mu
                best_values[clamp_idx, lr_idx, ss_idx, 4:] = sig
    print("Best Cost Found:")
    print(np.min(best_costs))
    np.savez("hyper_search.np", costs=best_costs,
             values=best_values, params=hyper)
    return mu,sig            

def TestNet():
    # net = wdnn.WaypointDistributionNN(4, 0.01) # learns mu, not sigma
    net = wdnn.WaypointDistributionNN(1, 0.001, 1e2)
    nsamples = 100
    x = np.ones(1)
    count = 0
    while count < 1000:
        count += 1
        mu, S = net(x)
        print(mu)
        #print(S[0,:])
        print(np.sum(S))
        wpts = mltnrm(mu[0,:], S[0,:], nsamples)
        print(wpts.shape)
        Cs = np.linalg.norm(wpts, axis=1)
        #print(Cs)
        print(np.sum(Cs)/nsamples)
        net.update(-Cs, wpts, np.vstack([x]*nsamples))
    print(S)

def TestBaseLine():
    net = wbnn.WaypointBaselineNN(4, 0.01, 1e2)
    nsamples = 100
    for i in range(100):
        S = np.identity(4)
        wpts = mltnrm(np.array([0,0,0,0]), S, nsamples)
        Cs = np.linalg.norm(wpts, axis=1)
        deltas = - (Cs + net(wpts))
        print(np.sum(np.abs(deltas)))
        net.update(-Cs, wpts)

if __name__ == "__main__":
    # TestNet()
    # TestBaseLine()
    dx = np.array([0, 1])
    v0x = 1
    vf = np.array([0, 1])
    obs_t=0.5
    obs_offset=0.0
    Train1Prob(dx, v0x, vf, obs_t, obs_offset)
    # HyperSearch(dx, v0x, vf, obs_t, obs_offset)
