# WaypointLearning
Reinforcement learning agent to avoid obstacles using TSOCS

install dependencies with:
./InstallPackages

compile with:
make

run test with:
./bin/waypointlearning

to get the first solution with no weighpoints run the following executable with 8 parameters:

./bin/solve p1 p2 p3 p4 p5 p6 p7 p8

p1: the name of the output file to print data to
p2: the translation x coordinate
p3: the translation y coordinate
p4: the initial x velocity
p5: the final x velocity
p6: the final y velocity
p7: the path-time an obstacle should be placed as a proportion of total time
p8: the offset distance the obstacle is placed at

it's possible, but unlikely, for the algorithm to fail to find a solution (~0.2% failure rate)
if this happens an exit status of 1 is returned.

the program expects all above units to be in meters (excpet p7),
this means values should be on the order of magnitude ~1 or less

a radius of 90mm (0.09m) is assumed for the obstacle,
so the offset distance should be < 0.09 for significant results,
maybe < 0.08 so that a significant time is guaranteed to be spent in collision,
if the start and end conditions are in conflict, the executable returns and exit status of 2.

the executable outputs a csv file to the specified directory,
the first element of the first line contains the total time of path trajectory,
the last element of the first line contains the time spent in collision,
the second line contains the x-y position of the obstacle
all other entries contain values that I suspect will be useful features to train on,
they are mostly time stamps and state features at those times.


to get data with a set waypoint runt he following executable with 12 parameters:

./bin/eval p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12

p1:  the name of the output file to print data to
p2:  the translation x coordinate
p3:  the translation y coordinate
p4:  the initial x velocity
p5:  the final x velocity
p6:  the final y velocity
p7:  the waypoint x position
p8:  the waypoint y position
p9:  the waypoint x velocity
p10: the waypoint y velocity
p11: the obstacle x coordinate
p12: the obstacle y coordinate

the executable with exit with status 1 if it fails to find a solution

the executable outputs a csv file to the specified directory,
the first line contains two elements, the first is the total time, the second is the time spent in collision,
each line afterwords has the following structure:

t, x, y, vx, vy

which describes the path the robot follows
