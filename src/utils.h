#include <algorithm>
#include <array>
#include <cmath>
#include <stdio.h>

#include "glog/logging.h"
#include "eigen3/Eigen/Dense"

#include "data_structures.h"
#include "tsocs.h"

#ifndef SRC_UTIL_H_
#define SRC_UTIL_H_

using Eigen::Vector2f;
using data_structs::SolutionParameters;
using data_structs::RobotState;

namespace util {
  
void GetOffsetPoint(const Vector2f x, const Vector2f v,
                    const float offset, Vector2f* offset_point) {
  const Vector2f perp = Vector2f(v.y(), -v.x()).normalized();
  (*offset_point) = x + offset*perp;
}

bool isInCollisionAtTime(const float time,
                         const float radius,
                         SolutionParameters<float> path,
                         RobotState<float> init,
                         const Vector2f obstacle) {
  RobotState<float> pose;
  tsocs::GetRobotState(init, &pose, path, time);
  Vector2f x = pose.pos.toEigen();
  
  const float dist = (x - obstacle).norm();
  
  return dist < 2*radius;
}

float BinarySearchCollisionBoundary(const float T_min,
                                    const float T_max,
                                    const float radius,
                                    const float tolerance,
                                    const Vector2f obstacle,
                                    SolutionParameters<float> path,
                                    RobotState<float> init) {
  const float T_mid = (T_min + T_max) / 2;
  if (T_max - T_min < tolerance) {
    return T_mid;
  }
  
  const bool TmaxInCollision = 
      isInCollisionAtTime(T_max, radius, path, init, obstacle);
  const bool doesCollide = isInCollisionAtTime(T_mid, radius, path, init, obstacle);
  
  if (doesCollide == TmaxInCollision) {
    return BinarySearchCollisionBoundary(T_min, T_mid, radius,
                                         tolerance,
                                         obstacle, path, init);
  } else {
    return BinarySearchCollisionBoundary(T_mid, T_max, radius,
                                         tolerance,
                                         obstacle, path, init);
  }
}

float GetTimeInCollision(const float radius,
                         const float tolerance,
                         const float interval,
                         const Vector2f obstacle,
                         SolutionParameters<float> path,
                         RobotState<float> init) {
  float t = 0.0;
  bool initCollides = isInCollisionAtTime(t, radius, path, init, obstacle);
  
  float enters_colision = 0.0;
  float exits_colision = 0.0;
  
  while (t < path.T) {
    t += interval;
    if (t > path.T) {
      t = path.T;
    }
    
    bool stateCollides = isInCollisionAtTime(t, radius, path, init, obstacle);
    if (initCollides != stateCollides) {
      const float time = BinarySearchCollisionBoundary(t - interval,
                                                       t, radius, tolerance, obstacle, path, init);
      if (initCollides) {
        return time;
      } else {
        enters_colision = time;
      }
      
      break;
    }
  }
  
  if (fabs(t - path.T) < 1e-4) {
    return 0.0;
  }
  
  bool endCollides = isInCollisionAtTime(path.T, radius, path, init, obstacle);
  if (endCollides) {
    exits_colision = path.T;
  } else {
    exits_colision = BinarySearchCollisionBoundary(t, path.T, radius, tolerance,
                                                   obstacle, path, init);
  }
  
  return exits_colision - enters_colision;
}

}
#endif  // SRC_UTIL_H_
