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

int main(int argc, char **argv) {
  
  char* output_file = argv[1];
  std::ofstream ofs;
  
  const Pose2D<float> x0(0,0);
  const Pose2D<float> xf(stof(argv[2]), stof(argv[3]));
  const Pose2D<float> v0(stof(argv[4]), 0.0);
  const Pose2D<float> vf(stof(argv[5]), stof(argv[6]));
  
  const float gamma = stof(argv[7]);
  const float offset = stof(argv[8]);
  
  RobotState<float> init(x0, v0);
  RobotState<float> fin(xf, vf);
  
  SolutionParameters<float> params;
  bool didSucceed = GetSolution(init, fin, &params);
  
  if (!didSucceed) {
    std::cout << "did not succeed\n";
    ofs.open(output_file);
    ofs << "tsocs could not find solution";
    ofs.close();
    return 1;
  }
  
  const float collision_point_time = gamma*params.T;
  RobotState<float> collision_center;
  GetRobotState(init, &collision_center, params, collision_point_time);
  
  Eigen::Vector2f obstacle;
  GetOffsetPoint(collision_center.pos.toEigen(),
                 collision_center.vel.toEigen(),
                 offset, &obstacle);
  
  const bool init_collides = isInCollisionAtTime(0.0, 0.09, params, init, obstacle);
  const bool final_collides = isInCollisionAtTime(
      params.T, 0.09, params, init, obstacle);
  
  if (init_collides || final_collides) {
    std::cout << "boundary in collision\n";
    ofs.open(output_file);
    ofs << "a boundary condition is in collision";
    ofs.close();
    return 2;
  }
  
  const float min_col_time = BinarySearchCollisionBoundary(
      0.0, collision_point_time, 0.09, 0.001, obstacle, params, init);
  const float max_col_time = BinarySearchCollisionBoundary(
      collision_point_time, params.T, 0.09, 0.001, obstacle, params, init);
  
  const float time_in_collision = max_col_time - min_col_time;
  
  RobotState<float> xmin;
  RobotState<float> xmid;
  RobotState<float> xmax;
  
  ofs.open(output_file);
  ofs << params.T << ", " << params.a1 << ", " 
      << params.a2 << ", " << params.a3 << ", " 
      << params.a4 << ", " << time_in_collision << std::endl;
  
  for (unsigned int i = 0; i < 100; i++) {
    const float t = i*params.T / (100 - 1);
    RobotState<float> xt;
    GetRobotState(init, &xt, params, t);
    ofs << t << ", " << xt.pos.x << ", " << xt.pos.y << ", "
        << xt.vel.x << ", " << xt.vel.y << std::endl;
  }
  ofs.close();
  
  return 0;
}
