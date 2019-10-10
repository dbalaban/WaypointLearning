#include <iostream>
#include <eigen3/Eigen/Geometry>

#include "eigen3/Eigen/Dense"

#include "data_structures.h"
#include "tsocs.h"

using data_structs::RobotState;
using data_structs::Pose2D;
using data_structs::SolutionParameters;
using tsocs::GetSolution;
using tsocs::GetRobotState;

int main(int argc, char **argv) {
    std::cout << "Hello, world!" << std::endl;
    
    Pose2D<float> x0(0,0);
    Pose2D<float> v0(1,0);
    Pose2D<float> xf(0,1);
    Pose2D<float> vf(-1, 0);
    
    RobotState<float> init(x0, v0);
    RobotState<float> fin(xf, vf);
    
    SolutionParameters<float> params;
    bool didSucceed = GetSolution(init, fin, &params);
    
    if (didSucceed) {
      std::cout << "Success!" << std::endl;
      std::cout << "Cost: " << params.cost << std::endl;
      std::cout << "Total Time: " << params.T << std::endl;
      RobotState<float> f;
      tsocs::GetRobotState(init, &f, params, params.T);
      std::cout << "Final state: \n" 
                << f.pos.x << ", " << f.pos.y << ", "
                << f.vel.x << ", " << f.vel.y << std::endl;
      
      RobotState<float> h;
      tsocs::GetRobotState(init, &h, params, params.T/2.0);
      std::cout << "Halfway state: \n" 
                << h.pos.x << ", " << h.pos.y << ", "
                << h.vel.x << ", " << h.vel.y << std::endl;
      
    } else {
      std::cout << "failed with cost: " << params.cost << std::endl;
    }
    
    return 0;
}
