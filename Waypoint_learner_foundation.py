# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

#Waypoint learner

#Generating a square from x,y=-1e3,-1e3 to x,y=1e3,1e3. This is assuemd to be travel grid.

x_up=1e3
y_up=1e3
x_lo=-1e3
y_lo=-1e3

#Putting the starting position at the center

x_start=0
y_start=0

nCases=1

for count in range(0,nCases-1):
    #Generating velocity towards x direction of a random value from 0 to 100
    
    v_start=np.random.random_sample()*100
    
    #choosing the ending position at a distance of 500 units at a random angle
    
    theta=np.random.random_sample()*(np.pi)
    x_end=500*np.cos(theta)
    y_end=500*np.sin(theta)
    
    #generate random final velocity angle phi
    
    phi=np.random.random_sample()*(2*np.pi)
    #with assumption that final velocity magnitude and starting velocity mmagnitude is same
    vx_end=v_start*np.cos(phi)
    vy_end=v_start*np.sin(phi)
    
    #generate obstacle position and radius. Gamma goes from 0 to 1, based on where it stands on the trajectory and radius is random from 20 to 50.
    gamma=np.random.random_sample()
    obs_rad=np.random.random_sample()*30+20# What should be the best radii for obstacle?
    
    
    
    #many independent samples for the trajectory and obstacles can be generated to gain experience.
    #to avoid obstacle, a waypoint can be generated inside the 2000x2000 square outside the obstacle radius and trajectory to the waypoint from source and from the waypoint to...
    #destination can be generated.