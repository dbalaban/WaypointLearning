#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 01:00:50 2019

@author: amodh, dbalaban
"""
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import random
import DataHandler as dh
#./bin/solve p1 p2 p3 p4 p5 p6 p7 p8
#
#p1: the name of the output file to print data to
#p2: the translation x coordinate
#p3: the translation y coordinate
#p4: the initial x velocity
#p5: the final x velocity
#p6: the final y velocit
#p7: the path-time an obstacle should be placed as a proportion of total time
#p8: the offset distance the obstacle is placed at
#


# =============================================================================
# the executable outputs a csv file to the specified directory,
# the first element of the first line contains the total time of path trajectory,
# the last element of the first line contains the time spent in collision,
# the second line contains the x-y position of the obstacle
# all other entries contain values that I suspect will be useful features to train on,
# they are mostly time stamps and state features at those times.
# 6
# 
# =============================================================================

# =============================================================================
# ./bin/eval p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12
# 
# p1:  the name of the output file to print data to
# p2:  the translation x coordinate
# p3:  the translation y coordinate
# p4:  the initial x velocity
# p5:  the final x velocity
# p6:  the final y velocity
# p7:  the waypoint x position
# p8:  the waypoint y position
# p9:  the waypoint x velocity
# p10: the waypoint y velocity
# p11: the obstacle x coordinate
# p12: the obstacle y coordinate
# 
# the executable with exit with status 1 if it fails to find a solution
# 
# the executable outputs a csv file to the specified directory,
# the first line contains two elements, the first is the total time, the second is the time spent in collision,
# each line afterwords has the following structure:
# 
# t, x, y, vx, vy
# =============================================================================


#time stamps of latest plot 1.4658 2.35274 2.46999 2.2767

class CoordinateDecent():
    def __init__(self, data_handler, eps, step_init, step_decay):
        self.eps = eps
        self.step_init = step_init
        self.handler = data_handler
        self.lr = step_decay

    def solve(self, dx, v0x, vf, obs_t, obs_offset):
        T_opt, C, f, _ = self.handler.getOptimalSolution(
                            dx, v0x, vf, obs_t, obs_offset)
        tsocs_calls = 1
        wpt = self.handler.getInitialWaypoint(f)
        D = float('inf')
        Cs = np.array([float('inf'), C, float('inf')])
        waypoints = np.copy(wpt)
        loss = [C]
        while D > self.eps:
            wpt_save = np.copy(wpt)
            for ax in range(4):
                step = np.zeros(4)
                step[ax] = self.step_init
                while step[ax]>0.001:
                    if Cs[0] == float('inf'):
                        tsocs_calls  += 1
                        wpt_temp = wpt - step
                        T, T_col = self.handler.Evaluate(dx, v0x, vf, wpt_temp,
                                                      obs_t, obs_offset)
                        Cs[0] = self.handler.GetCost(T_opt, T_col, T)
                    if Cs[2] == float('inf'):
                        tsocs_calls  += 1
                        wpt_temp = wpt + step
                        T, T_col = self.handler.Evaluate(dx, v0x, vf, wpt_temp,
                                                         obs_t, obs_offset)
                        Cs[2] = self.handler.GetCost(T_opt, T_col, T)
                        
                    print(Cs)
                        
                    idx = np.argmin(Cs)
                    if idx == 0:
                        wpt -= step
                        temp = Cs[1]
                        Cs[1] = Cs[0]
                        Cs[0] = float('inf')
                        Cs[2] = temp
                    if idx == 1:
                        step[ax] *= self.lr
                        Cs[0] = float('inf')
                        Cs[2] = float('inf')
                    if idx == 2:
                        wpt += step
                        temp = Cs[1]
                        Cs[1] = Cs[2]
                        Cs[0] = temp
                        Cs[2] = float('inf')
            D = np.linalg.norm(wpt - wpt_save)
            waypoints = np.vstack([waypoints, wpt])
            loss += [Cs[1]]
        return Cs[1], wpt, tsocs_calls, waypoints, loss                

if __name__ == "__main__":
    data_handler = dh.DataHandler(500, "optimal.csv", "eval.csv", False)
    cd = CoordinateDecent(data_handler, 0.001, 1.5, .75)
    dx = np.array([0, 1])
    v0x = 1
    vf = np.array([0, 1])
    obs_t=0.5
    obs_offset=0.0
    C, wpt_opt, count, wpts, loss = cd.solve(dx, v0x, vf, obs_t, obs_offset)
    print(wpts)
    print(C)
