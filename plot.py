import matplotlib.pyplot as plt
import numpy as np
import csv
import os

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

xtrans=1
ytrans=1.4
vxinit=0.4
vxfinal=0.1
vyfinal=0.1
obs_pos=0.5
obs_offset=0.09


os.system("./bin/solve initpath "+str(xtrans)+" "+str(ytrans)+" "+str(vxinit)+" 0.1 0.1 0.5 0.09")

with open('initpath') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        ii=0
        datamat=[0,0]
        for row in spamreader:
            ii=ii+1
            if ii==1:
                vecin1=[float(i) for i in row]
            elif ii==2:
                vecin2=[float(i) for i in row]
            elif ii>=6:
                vecin=[float(i) for i in row]
                
                datamat=np.vstack((datamat,[vecin[1],vecin[2]]))
                

circle1=plt.Circle((vecin2[0],vecin2[1]),0.18,color='r',label='Obstacle region')  
          
fig,ax1=plt.subplots()
Topt=vecin1[0]
Tcoll=vecin1[len(vecin1)-1]
gamma=100
C=(1/Topt)*(Topt+gamma*Tcoll)-1

ax1.plot(datamat[:,0],datamat[:,1],color='#112233',label='T='+str(round(vecin1[0],2))+'s'+', C='+str(round(C,2)))

ax1.plot(vecin2[0],vecin2[1],'*')
ax1.plot(0,0,'x')
ax1.plot(xtrans,ytrans,'x')
ax1.add_patch(circle1)

#choosing random point in translational space 
time =10
cost=1000
for pindex in range(10):

    if pindex!=5:
        os.system("./bin/eval waypath1 1 1.4 0.4 0.1 0.1 "+str(vecin2[0]-1+0.2*pindex)+" "+str(vecin2[1])+" "+str(0.48)+" "+str(1.03)+" "+str(vecin2[0])+" "+str(vecin2[1]))
        
        with open('waypath1') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                ii=0
                wayamat2=[0,0]
                for row in spamreader:
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
        gamma=100
        Cw=(1/Topt)*(Ttot+gamma*Tcoll)-1       
        ax1.plot(wayamat2[:,0],wayamat2[:,1],label='T='+str(round(vec1w[0],2))+'s'+', C='+str(round(Cw,2)))
        if cost>Cw:
            wayptx=vecin2[0]-1+0.2*pindex
            waypty=vecin2[1]
            time=vec1w[0]
            cost=Cw
        ax1.plot(vecin2[0]-1+0.2*pindex,vecin2[1],'o',color='#112233')


ax1.legend(loc='left center',bbox_to_anchor=(-0.1,1))
plt.axis('equal')
plt.savefig('traj_posrange',bbox_inches='tight')


fig,ax2=plt.subplots()

ax2.plot(datamat[:,0],datamat[:,1],label='T='+str(round(vecin1[0],2))+'s'+', C='+str(round(C,2)),color='#112233')

ax2.plot(vecin2[0],vecin2[1],'*')
a=np.sqrt(0.48*0.48+1.03*1.03)
for angle in range(-5,5):
        os.system("./bin/eval waypath2 1 1.4 0.4 0.1 0.1 "+str(wayptx)+" "+str(waypty)+" "+str(a*np.cos(np.arctan(1.03/0.48)+0.3*np.pi*angle/5))+" "+str(a*np.sin(np.arctan(1.03/0.48)+0.3*np.pi*angle/5))+" "+str(vecin2[0])+" "+str(vecin2[1]))
        
        with open('waypath2') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                ii=0
                wayamat3=[0,0]
                for row in spamreader:
                    ii=ii+1
                    if ii==1:
                        vec3w3=[float(i) for i in row]
                    elif ii==2:
                        vec2w3=[float(i) for i in row]
                    else:
                        vecw3=[float(i) for i in row]
                        
                        wayamat3=np.vstack((wayamat3,[vecw3[1],vecw3[2]]))
        
        Ttot=vec3w3[0]
        Tcoll=vec3w3[1]
        gamma=100
        
        Cw2=(1/Topt)*(Ttot+gamma*Tcoll)-1  
        if Ttot>=Topt:        
            ax2.plot(wayamat3[:,0],wayamat3[:,1],label=str(round((180/np.pi)*(np.arctan(0.2)+0.3*np.pi*angle/5),2))+'\u00b0: T='+str(round(vec3w3[0],2))+'s'+', C='+str(round(Cw2,2)))
        
        
        ax2.plot(wayptx,waypty,'o',color='#112233')
circle2=plt.Circle((vecin2[0],vecin2[1]),0.18,color='r',label='Obstacle region')      
ax2.plot(0,0,'x')
ax2.plot(xtrans,ytrans,'x') 
ax2.add_patch(circle2)
ax2.legend(loc='left center',bbox_to_anchor=(-0.1,1))
plt.axis('equal')
plt.savefig('traj_Vrange',bbox_inches='tight')
