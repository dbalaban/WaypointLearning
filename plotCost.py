#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 21:41:17 2019

@author: amodh
"""

#Script to plot the avg cost and variance with number of iterations and plotting
#trajectoriees corresponding to the points selected by vector listvec on the plot of the avg cost

import matplotlib.pyplot as plt
import csv
import numpy as np
import os

cost1=[]
cost2=[]
mu=[0,0,0,0]

listvec=[800,900,950]

wptrow=np.zeros((1,11))

with open('wpt_data.csv') as csvfile:
                    lines = csv.reader(csvfile, delimiter=',')
                    ii=0
                    traj_mat=[0,0]
                   
                    for row in lines:
                        
                        ii=ii+1
                        if ii>=2:
                            vec=[float(i) for i in row]
                            wptrow=np.vstack((wptrow,vec))
                            
wptrow=wptrow[1:,:]

var_cost=np.sum(wptrow[:,4:8],axis=1)

fig,ax1=plt.subplots()

fig2,ax21=plt.subplots()



with open('optimal.csv') as csvfile:
                    lines = csv.reader(csvfile, delimiter=',')
                    itraj=0
                    traj_mat=[0,0]
                    for row in lines:
                        
                        itraj=itraj+1
                        if itraj==2:
                            obs_xy=[float(i) for i in row]
                        if itraj>=6:
                            traj_mat=np.vstack((traj_mat,[float(row[1]),float(row[2])]))




with open('optimal.csv') as csvfile:
                    lines = csv.reader(csvfile, delimiter=',')
                    itraj=0
                    traj_mat=[0,0]
                    for row in lines:
                        
                        itraj=itraj+1
                        if itraj==2:
                            obs_xy=[float(i) for i in row]
                        if itraj>=6:
                            traj_mat=np.vstack((traj_mat,[float(row[1]),float(row[2])]))

circle1=plt.Circle((obs_xy[0],obs_xy[1]),0.18,color='r',label='Obstacle region') 
circle2=plt.Circle((obs_xy[0],obs_xy[1]),0.18,color='r')#,label='Obstacle region') 


ax21.plot(10*np.log10(var_cost),color='c',label='trace(S) [dB]')
ax2=ax21.twinx()

ax2.plot((wptrow[:,9]),color='m',label='Average cost') 


ax2.set(xlabel='Iterations',ylabel='Average Cost')

ax21.set(ylabel='trace(S) [dB]')
ax21.legend(loc='upper right')





 
 

for index in range(len(listvec)):
    os.system("./bin/eval waypath"+str(index+1)+" 0 1 1 0 1 "
          +str(wptrow[listvec[index],0])+" "+str(wptrow[listvec[index],1])+" "
          +str(wptrow[listvec[index],2])+" "+str(wptrow[listvec[index],3])+" "+str(obs_xy[0])+" "+str(obs_xy[1]))

    wayamat2=[0,0]
    with open('waypath'+str(index+1)) as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',')
                    ii=0
                    
                    for row in spamreader:
                        ii=ii+1
                        if ii==1:
                            vec1w=[float(i) for i in row]
                        elif ii==2:
                            vec2w=[float(i) for i in row]
                        else:
                            vecw2=[float(i) for i in row]
                            
                            wayamat2=np.vstack((wayamat2,[vecw2[1],vecw2[2]]))
                    
    
    if listvec[index]==780:
        ax1.plot(wayamat2[:,0],wayamat2[:,1],label=str(index+1)+',best path')
    else:
        ax1.plot(wayamat2[:,0],wayamat2[:,1],label=str(index+1))
    if listvec[index]==780:
        ax2.plot(listvec[index],wptrow[listvec[index],9],'o',label=str(index+1)+',best path')
        
    else:
        ax2.plot(listvec[index],wptrow[listvec[index],9],'o',label=str(index+1))
        
    
    ax1.plot(wptrow[listvec[index],0],wptrow[listvec[index],1],'x',color='black')








ax1.plot(0,0,'o')
ax1.plot(0,1,'o')
ax1.set(xlabel='x',ylabel='y')
ax1.axis('equal')

ax1.plot()



ax1.add_patch(circle2)
ax1.legend()
ax2.legend(loc='left center',bbox_to_anchor=(-0.1,1))
fig.savefig('trajectories.eps',format='eps',bbox_inches='tight')

fig2.savefig('trajectories_cost.eps',format='eps',bbox_inches='tight')

























                            
    