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




os.system("./bin/solve initpath 0.6 0.7 0.2 0.1 0.5 0.5 0.02")

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
            
            
plt.plot(datamat[:,0],datamat[:,1],label='Initial path')

plt.plot(vecin2[0],vecin2[1],'*')

#choosing random point in translational space 
ptx=np.random.uniform(vecin2[0]-0.15,vecin2[0]+0.15)
while np.abs(ptx-vecin2[0])<0.1:
    ptx=np.random.uniform(vecin2[0]-0.2,vecin2[0]+0.2)

pty=np.random.uniform(vecin2[1]-0.15,vecin2[1]+0.15)
while np.abs(pty-vecin2[1])<0.1:
    pty=np.random.uniform(vecin2[1]-0.2,vecin2[1]+0.2)
    
vx=np.random.uniform(0.1,0.3)
vy=np.random.uniform(0.3,0.7)


os.system("./bin/eval waypath 0.6 0.7 0.2 0.1 0.1 "+str(ptx)+" "+str(pty)+" "+str(vx)+" "+str(vy)+" "+str(vecin2[0])+" "+str(vecin2[1]))


with open('waypath') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        ii=0
        wayamat1=[0,0]
        for row in spamreader:
            ii=ii+1
            if ii==1:
                vec1w1=[float(i) for i in row]
            elif ii==2:
                vec2w1=[float(i) for i in row]
            else:
                vecw1=[float(i) for i in row]
                
                wayamat1=np.vstack((wayamat1,[vecw1[1],vecw1[2]]))
                
plt.plot(wayamat1[:,0],wayamat1[:,1],label='Path through waypt 1')
plt.plot(ptx,pty,'o')


#choosing random point in translational space 
ptx2=np.random.uniform(vecin2[0]-0.15,vecin2[0]+0.15)
while np.abs(ptx2-vecin2[0])<0.1:
    ptx2=np.random.uniform(vecin2[0]-0.15,vecin2[0]+0.15)

pty2=np.random.uniform(vecin2[1]-0.2,vecin2[1]+0.2)
while np.abs(pty2-vecin2[1])<0.1:
    pty2=np.random.uniform(vecin2[1]-0.2,vecin2[1]+0.2)




os.system("./bin/eval waypath1 0.6 0.7 0.2 0.1 0.1 "+str(ptx2)+" "+str(pty2)+" "+str(vx)+" "+str(vy)+" "+str(vecin2[0])+" "+str(vecin2[1]))

with open('waypath1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        ii=0
        wayamat2=[0,0]
        for row in spamreader:
            ii=ii+1
            if ii==1:
                vec1w2=[float(i) for i in row]
            elif ii==2:
                vec2w2=[float(i) for i in row]
            else:
                vecw2=[float(i) for i in row]
                
                wayamat2=np.vstack((wayamat2,[vecw2[1],vecw2[2]]))
                
plt.plot(wayamat2[:,0],wayamat2[:,1],label='Path through waypt 2')
plt.plot(ptx2,pty2,'o')


if vec1w1[0]>vec1w2[0]:
    ptx=ptx2
    pty=pty2
    
vx2=vx+np.random.uniform(0,0.2)
vy2=vy+np.random.uniform(0,0.2)


os.system("./bin/eval waypath2 0.6 0.7 0.2 0.1 0.1 "+str(ptx)+" "+str(pty)+" "+str(vx2)+" "+str(vy2)+" "+str(vecin2[0])+" "+str(vecin2[1]))

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
                
plt.plot(wayamat3[:,0],wayamat3[:,1],label='Improved path through waypt 1')
plt.legend()
plt.plot(ptx,pty,'o')
plt.savefig('trajs.png')

print(vecin1[0],vec1w1[0],vec1w2[0],vec3w3[0])