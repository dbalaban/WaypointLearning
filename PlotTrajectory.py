#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:58:47 2019

@author: amodh
"""

import numpy as np
import matplotlib.pyplot as plt
import DataHandler as dh
import csv
import subprocess

#token is whether thee initial trajectory is plot (token=0) or the trajectory with waypoint (token=1)

def PlotOpimalSol(dx, v0x, vf, obs_t, obs_offset, ax1, datahandler):
    traj_mat, obs_xy = datahandler.GetOptimalTrajectory()
    
    ax1.plot(traj_mat[:,0],traj_mat[:,1])
    ax1.plot(0,0,'x')
    ax1.plot(dx[0],dx[1],'x')
    
    circle1=plt.Circle((obs_xy[0],obs_xy[1]),0.18,color='r',label='Collision Region') 
    
    ax1.add_patch(circle1)
    ax1.plot(traj_mat[:,0],traj_mat[:,1],label="Time Optimal Path")
    
    return ax1, obs_xy
    
def PlotWaypointTraj(dx, v0x, vf, obs_t, obs_xy, wpt, ax1, datahandler, label):
    traj_mat = datahandler.GetTrajectoryWithWaypoint(dx, v0x, vf, wpt, obs_xy[0], obs_xy[1])
    ax1.plot(traj_mat[:,0],traj_mat[:,1],label=label)
    ax1.plot(wpt[0], wpt[1], '*')
    return ax1

def PlotTraj(dx, v0x, vf, obs_t, obs_offset,wpts,ax1):
    
    
    cmd = "./bin/solve {} {} {} {} {} {} {} {}".format(
            'token.txt',round(dx[0],3),round(dx[1],3),round(v0x, 3),
            round(vf[0],3),round(vf[1],3),round(obs_t,3),round(obs_offset,3))
    try:
            status = subprocess.call(cmd, shell=True, timeout=1)
    except:
            print("timeout on command:")
            print(cmd)
            return float('inf'), float('inf')
            
    if status > 0:
            return float('inf'), float('inf')
        
    
    
    
    
    with open('token.txt') as csvfile:
                    lines = csv.reader(csvfile, delimiter=',')
                    ii=0
                    traj_mat=[0,0]
                    for row in lines:
                        
                        ii=ii+1
                        if ii==2:
                            obs_xy=[float(i) for i in row]
                        if ii>=6:
                            traj_pt=[float(i) for i in row]
                            
                            traj_mat=np.vstack((traj_mat,[traj_pt[1],traj_pt[2]]))
    
    
    ax1.plot(traj_mat[:,0],traj_mat[:,1])
    ax1.plot(0,0,'x')
    ax1.plot(dx[0],dx[1],'x')
    
    wpts=np.matrix(wpts)
    circle1=plt.Circle((obs_xy[0],obs_xy[1]),0.18,color='r',label='Obstacle region') 
    
    ax1.add_patch(circle1)
    
    #print(wpts)
    for iindex in range(np.size(wpts,axis=1)):
    #for wpt in wpts:
       
        wpt=(wpts[iindex,:])
        
        ax1.plot(wpt[:,0],wpt[:,1],'o')
        cmd = "./bin/eval {} {} {} {} {} {} {} {} {} {} {} {}".format(
                'token.txt',round(dx[0],3),round(dx[1],3),round(v0x, 3),
                round(vf[0],3),round(vf[1],3),float(wpt[:,0]),float(wpt[:,1]),
                float(wpt[:,2]),float(wpt[:,3]),round(obs_xy[0],3),round(obs_xy[1],3))
        try:
                status = subprocess.call(cmd, shell=True, timeout=1)
        except:
                print("timeout on command:")
                print(cmd)
                return float('inf'), float('inf')
                
        if status > 0:
                return float('inf'), float('inf')
            
        
        
        
        
        with open('token.txt') as csvfile:
                        lines = csv.reader(csvfile, delimiter=',')
                        ii=0
                        traj_mat=[0,0]
                        for row in lines:
                            
                            ii=ii+1
                            if ii>=4:
                                traj_pt=[float(i) for i in row]
                                
                                traj_mat=np.vstack((traj_mat,[traj_pt[1],traj_pt[2]]))
       
        
        print()
        ax1.plot(traj_mat[:,0],traj_mat[:,1])
    return ax1

if __name__ == "__main__":
    dx = np.array([0, 1])
    v0x = 1
    vf = np.array([0, 1])
    obs_t=0.5
    obs_offset=0.0
    fig, ax1 = plt.subplots()
    datahandler = dh.DataHandler(10, "optimal.csv", "eval.csv", True, 1)
    datahandler2 = dh.DataHandler(10, "optimal.csv", "eval_nn.csv", True, 1)
    ax1,obs_xy = PlotOpimalSol(dx, v0x, vf, obs_t, obs_offset, ax1, datahandler)
    wpt = np.array([ 0.22341839,  0.13741288, -0.42356584,  0.44567634])
    wpt2 = np.array([0.14423926,  0.18626884, -0.38961458,  0.53745378])
    ax1 = PlotWaypointTraj(dx, v0x, vf, obs_t, obs_xy, wpt, ax1, datahandler, "Coordinate Decent Waypoint")
    ax1 = PlotWaypointTraj(dx, v0x, vf, obs_t, obs_xy, wpt2, ax1, datahandler2, "Learned Waypoint")
    ax1.legend()
    plt.axis('equal')
    plt.show()