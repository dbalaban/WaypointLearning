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
        
    
    