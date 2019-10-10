#ifndef SRC_TSOCS_H_
#define SRC_TSOCS_H_

#include <ceres/ceres.h>
#include <ceres/types.h>
#include <math.h>
#include <eigen3/Eigen/Geometry>

#include <algorithm>
#include <cmath>
#include <memory>
#include <vector>

#include "eigen3/Eigen/Dense"

#include "data_structures.h"
#include "tsocs_templates.h"
#include "tsocs_structures.h"

namespace tsocs {
  
using data_structs::RobotState;
using data_structs::Pose2D;
using data_structs::SolutionParameters;

float GetTimeBound(Eigen::Vector2f v0,
                   Eigen::Vector2f vf,
                   Eigen::Vector2f dx);

float GetFeasibleTime(float tp, float tm, int ai, float dX,
                      float dV, float vi);

float GetAxisSolution(float x, float v0, float vf, int* sign_u0);

void GetGuess(Eigen::Vector2f v0,
              Eigen::Vector2f vf,
              Eigen::Vector2f dx,
              SolutionParameters<float>* params);

bool GetSolution(RobotState<float> init,
                 RobotState<float> fin,
                 SolutionParameters<float>* params);

const float kEpsilon_ = 1e-6;
const float kCostThreshold_ = 1e-6;
const float accel_ = 1.0;
const float x_coef_ = 1.0;
const float v_coef_ = 1.0;

const unsigned int kMaxIterations_ = 100;
  
}  // namespace tsocs

#endif  // SRC_TSOCS_H_
