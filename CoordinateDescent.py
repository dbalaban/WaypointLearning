#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 01:00:50 2019

@author: amodh
"""
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import random
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



errfile=open('error.txt','a')
def traj_cost(datastr):
    os.system("./bin/eval waypath1 "+datastr)
    with open('waypath1') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                ii=0
                wayamat2=[0,0]
                for row in spamreader:
                    if row==['tsocs could not find the solution']:
                        errfile=open('error.txt','a')
                        errfile.write(datastr+'\n')
                        errfile.close()
                        token=-1
                        return token
                    ii=ii+1
                    if ii==1:
                        vec1w=[float(i) for i in row]
                    elif ii==2:
                        vec2w=[float(i) for i in row]
                    else:
                        vecw2=[float(i) for i in row]
                        
                        wayamat2=np.vstack((wayamat2,[vecw2[1],vecw2[2]]))
    
    Ttot=vec1w[0]
    Tcoll=vec1w[1]
    
    C1=(1/Topt)*(Ttot+gamma*Tcoll)-1   
    #ax1.plot(wayamat2[:,0],wayamat2[:,1])
    return C1,wayamat2
        



xtrans=2
ytrans=6
vxinit=0.5
vxfinal=3
vyfinal=0.3
obs_pos=0.5
obs_offset=0.09


os.system("./bin/solve initpath "+str(xtrans)+" "+str(ytrans)+" "+str(vxinit)+" "+str(vxfinal)+" "+str(vyfinal)+" "+str(obs_pos)+" "+str(obs_offset))
datastr=str(xtrans)+" "+str(ytrans)+" "+str(vxinit)+" "+str(vxfinal)+" "+str(vyfinal)+" "+str(obs_pos)+" "+str(obs_offset)
with open('initpath') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        ii=0
        datamat=[0,0]
        for row in spamreader:
            if row==['tsocs could not find the solution']:
                errfile.write(datastr+'\n')
                errfile.close()
            ii=ii+1
            if ii==1:
                vecin1=[float(i) for i in row]
            elif ii==2:
                vecin2=[float(i) for i in row]
            elif ii>=6:
                vecin=[float(i) for i in row]
                
                datamat=np.vstack((datamat,[vecin[1],vecin[2]]))
                

circle1=plt.Circle((vecin2[0],vecin2[1]),0.18,color='r',label='Obstacle region')  
circle2=plt.Circle((vecin2[0],vecin2[1]),0.18,color='r',label='Obstacle region')  
          
fig,ax1=plt.subplots()
Topt=vecin1[0]
Tcoll=vecin1[len(vecin1)-1]
gamma=100


#ax1.plot(datamat[:,0],datamat[:,1],color='#112233',label='T='+str(round(vecin1[0],2))+'s'+', C='+str(round(C,2)))

ax1.plot(vecin2[0],vecin2[1],'*')
ax1.plot(0,0,'x')
ax1.plot(xtrans,ytrans,'x')
ax1.add_patch(circle1)

obs_dist=[vecin2[0],vecin2[1]]-datamat
dist_sq=np.square(obs_dist)
min_ind=np.argmin(np.sum(dist_sq,axis=1))

ax1.plot(datamat[min_ind,0],datamat[min_ind,1],'o')

wayptx=datamat[min_ind,0]
waypty=datamat[min_ind,1]
vxsel=vxfinal*(1-obs_pos)+vxinit*obs_pos
vysel=vyfinal*(1-obs_pos)
delta=0.001

D=100
gamma=100
step=0.18

waypt_coord=[wayptx,waypty,vxsel,vysel]
WPT=[wayptx,waypty,vxsel,vysel]
epsilon=0.001
D=100
coeff_sel=[-1,0,1]

while D>epsilon:
    C=np.zeros(3)
    step=0.1
    for iindex in range(0,4):
        step=0.1
        while step>0.001:
            
            for coeff in (-1,0,1):
            
                waypt_coord1=waypt_coord[iindex]+coeff*step
                
                wayptcoord_temp=waypt_coord[0:iindex]+[waypt_coord1]+waypt_coord[iindex+1:4]
                waypt_str=" "
                for jj in range(0,len(wayptcoord_temp)):
                    waypt_str=waypt_str+str(wayptcoord_temp[jj])+" "
                
                datastr=str(xtrans)+" "+str(ytrans)+" "+str(vxinit)+" "+str(vxfinal)+" "\
                          +str(vyfinal)+waypt_str+str(vecin2[0])+" "+str(vecin2[1])
                
                if traj_cost(datastr)==-1:
                    C[coeff+1]=float(100)
                    #wayptx_1=wayptx_1*(1+0.001*random.uniform(-1,1))
                    #datastr=str(xtrans)+" "+str(ytrans)+" "+str(vxinit)+" "+str(vxfinal)+" "\
                     #     +str(vyfinal)+" "+str(wayptx_1)+" "+str(waypty)+" "+str(vxsel)+" "+str(vysel)+" "+str(vecin2[0])+" "+str(vecin2[1])
                else:
                    Cx,wayamat1=traj_cost(datastr)
                    C[coeff+1]=Cx
        
            
            
            if C[0]==C[1] and C[0]==C[2] and C[0]==100:
                step=1.2*step
            else:
                sel=np.argmin(C)
                waypt_coord[iindex]=waypt_coord[iindex]+coeff_sel[sel]*step
                if coeff_sel[sel]==0:
                    step=step/2
                
                
                
    
            print(waypt_coord,iindex)
    
    Wayptvec1=waypt_coord
    Wayptvec2=np.array(waypt_coord)*-1
    print(Wayptvec2)
    WPT=np.array(WPT)
    print(WPT)
    D=np.linalg.norm(np.add(WPT,Wayptvec2))
    print(D)
    
    WPT=waypt_coord     
    
    
    
    
    
    
   

fig,ax2=plt.subplots()
ax2.add_patch(circle2)

waypt_str=" "
for jj in range(0,len(wayptcoord_temp)):
    waypt_str=waypt_str+str(waypt_coord[jj])+" "

datastr=str(xtrans)+" "+str(ytrans)+" "+str(vxinit)+" "+str(vxfinal)+" "\
          +str(vyfinal)+waypt_str+str(vecin2[0])+" "+str(vecin2[1])

if traj_cost(datastr)==-1:
    C[coeff]=float(100)
    #wayptx_1=wayptx_1*(1+0.001*random.uniform(-1,1))
    #datastr=str(xtrans)+" "+str(ytrans)+" "+str(vxinit)+" "+str(vxfinal)+" "\
     #     +str(vyfinal)+" "+str(wayptx_1)+" "+str(waypty)+" "+str(vxsel)+" "+str(vysel)+" "+str(vecin2[0])+" "+str(vecin2[1])
else:
    Cx,wayamat=traj_cost(datastr)


ax2.plot(wayamat[:,0],wayamat[:,1])
ax2.plot(waypt_coord[0],waypt_coord[1],'o')

#ax1.plot(wayptx,waypty,'o')
#        
#plt.axis('equal')









