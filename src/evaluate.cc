
#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>
#include <stdio.h>
#include <eigen3/Eigen/Geometry>

#include "eigen3/Eigen/Dense"

#include "data_structures.h"
#include "tsocs.h"
#include "utils.h"

using data_structs::RobotState;
using data_structs::Pose2D;
using data_structs::SolutionParameters;
using tsocs::GetSolution;
using tsocs::GetRobotState;
using std::string;

using std::stof;

using util::GetOffsetPoint;
using util::isInCollisionAtTime;
using util::BinarySearchCollisionBoundary;
using util::GetTimeInCollision;

int main(int argc, char **argv) {
  char* output_file = argv[1];
  std::ofstream ofs;
  
  const Pose2D<float> x0(0,0);
  const Pose2D<float> xf(stof(argv[2]), stof(argv[3]));
  const Pose2D<float> v0(stof(argv[4]), 0.0);
  const Pose2D<float> vf(stof(argv[5]), stof(argv[6]));
  const Pose2D<float> wpos(stof(argv[7]), stof(argv[8]));
  const Pose2D<float> wvel(stof(argv[9]), stof(argv[10]));
  const Vector2f obstacle(stof(argv[11]), stof(argv[12]));
  
  RobotState<float> init(x0, v0);
  RobotState<float> waypt(wpos, wvel);
  RobotState<float> fin(xf, vf);
  
  SolutionParameters<float> params1;
  SolutionParameters<float> params2;
  bool didSucceed1 = GetSolution(init, waypt, &params1);
  bool didSucceed2 = GetSolution(waypt, fin, &params2);
  
  if (!didSucceed1 || !didSucceed2) {
    std::cout << "did not succeed\n";
    ofs.open(output_file);
    ofs << "tsocs could not find the solution";
    ofs.close();
    return 1;
  }
  
  const float t1 = GetTimeInCollision(0.09, 0.001, 0.01, obstacle, params1, init);
  const float t2 = GetTimeInCollision(0.09, 0.001, 0.01, obstacle, params2, waypt);
  
  const float collision_time = t1 + t2;
  const float total_time = params1.T + params2.T;
  
  ofs.open(output_file);
  ofs << total_time << ", " << collision_time << std::endl;
      
  for (unsigned int i = 0; i < 100; i++) {
    const float t = i*params1.T / (100 - 1);
    RobotState<float> xt;
    GetRobotState(init, &xt, params1, t);
    ofs << t << ", " << xt.pos.x << ", " << xt.pos.y << ", "
        << xt.vel.x << ", " << xt.vel.y << std::endl;
  }
      
  for (unsigned int i = 1; i <= 100; i++) {
    const float t = i*params2.T / 100;
    RobotState<float> xt;
    GetRobotState(waypt, &xt, params2, t);
    ofs << t + params1.T << ", " << xt.pos.x << ", " << xt.pos.y << ", "
        << xt.vel.x << ", " << xt.vel.y << std::endl;
  }
  ofs.close();
  
  return 0;
}
