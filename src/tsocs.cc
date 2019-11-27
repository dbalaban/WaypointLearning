#include "tsocs.h"

#include <eigen3/Eigen/Geometry>
#include "eigen3/Eigen/Dense"

#include <iostream>

using Eigen::Vector2f;
using data_structs::X;
using data_structs::V;
using data_structs::Xdist;
using data_structs::Vdist;
using data_structs::Pose2D;
using data_structs::RobotState;
using data_structs::SolutionParameters;

namespace tsocs {
float GetTimeBound(Vector2f v0,
                   Vector2f vf,
                   Vector2f dx) {
  // time to accelerate to rest
  const float t1 = v0.norm();
  const float t3 = vf.norm();
  // position after accelerating to rest, first rest point
  const Vector2f x_1 = v0 * t1 / 2;
  // position before accelerating to goal, second rest point
  const Vector2f x_2 = dx - vf * t3 / 2;

  // dist between two rest points
  const float x_tilda = (x_2 - x_1).norm();
  float t2 = 2 * sqrt(x_tilda);  // travel time between rest points
  // total time for 1D problems and acceleration to rest
  return t1 + t2 + t3;
}

float GetFeasibleTime(float tp, float tm, int ai, float dX, float dV, float vi) {
  double tpt = 2 * tp - ai * dV;
  double xp =
      vi * tpt + ai * tp * tpt - ai * (tp * tp + (tpt - tp) * (tpt - tp)) / 2;

  if (fabs(xp - dX) < kEpsilon_) {
    return tp;
  }

  return tm;
}

float GetAxisSolution(float x, float v0, float vf, int* sign_u0) {
  // switching funciton at time 0
  float x_switch_init;
  float tp, tm;

  if (v0 > vf) {
    x_switch_init = x + (vf * vf - v0 * v0) / 2.0;
  } else {
    x_switch_init = x - (vf * vf - v0 * v0) / 2.0;
  }

  if (0 < x_switch_init) {
    tp = -v0 + sqrt(x + (vf * vf + v0 * v0) / 2);
    tm = -v0 - sqrt(x + (vf * vf + v0 * v0) / 2);
    (*sign_u0) = 1;
    return GetFeasibleTime(tp, tm, 1, x, vf - v0, v0);
  } else if (0 > x_switch_init) {
    tp = v0 + sqrt((vf * vf + v0 * v0) / 2 - x);
    tm = v0 - sqrt((vf * vf + v0 * v0) / 2 - x);
    (*sign_u0) = -1;
    return GetFeasibleTime(tp, tm, -1, x, vf - v0, v0);
  } else {
    (*sign_u0) = 0;
    return 0;
  }
}


void GetGuess(Vector2f v0,
              Vector2f vf,
              Vector2f dx,
              SolutionParameters<float>* params) {
  const float theta_init =
      dx.norm() == 0 ? 0 : atan2(dx.y(), dx.x());
  const float cos_theta0 = cos(theta_init);
  const float sin_theta0 = sin(theta_init);
  int sign_uo_x, sign_uo_y;

  const float axis1_time =
      GetAxisSolution(dx.x() / cos_theta0, v0.x() / cos_theta0,
                      vf.x() / cos_theta0, &sign_uo_x);
  const float axis2_time =
      GetAxisSolution(dx.y() / sin_theta0, v0.y() / sin_theta0,
                      vf.y() / sin_theta0, &sign_uo_y);
  params->a3 = sign_uo_x * cos(theta_init);
  params->a4 = sign_uo_y * sin(theta_init);
  params->a1 = -params->a3 / (axis1_time + kEpsilon_);
  params->a2 = -params->a4 / (axis2_time + kEpsilon_);
}

bool GetSolution(RobotState<float> init,
                 RobotState<float> fin,
                 SolutionParameters<float>* params) {
  // scale units for unit acceleration
  init = init/accel_;
  fin = fin/accel_;
  
  // get difference between states
  RobotState<float> delta = fin - init;
  
  Vector2f v0(init.vel.x, init.vel.y);
  Vector2f vf(fin.vel.x, fin.vel.y);
  Vector2f dx(delta.pos.x, delta.pos.y);
  Vector2f dv(delta.vel.x, delta.vel.y);
  
  GetGuess(v0, vf, dx, params);
  const double t_max = GetTimeBound(v0, vf, dx);
  
  // copy params to double precision
  SolutionParameters<double> p(*params);
  p.T = t_max;

  // set optimization options
  ceres::Solver::Options options;
  options.max_num_iterations = kMaxIterations_;
  options.linear_solver_type = ceres::DENSE_QR;
  options.minimizer_progress_to_stdout = false;
  options.logging_type = ceres::SILENT;
  options.function_tolerance = 1e-20;
  
  // setup stage 1
  ceres::Problem stage1;
  stage1.AddResidualBlock(
      new ceres::AutoDiffCostFunction<Xdist, 2, 1, 1, 1, 1, 1>(new Xdist(delta.pos,     init.vel, x_coef_)),
      NULL, &(p.a1), &(p.a2), &(p.a3), &(p.a4), &(p.T));
  stage1.AddResidualBlock(
      new ceres::AutoDiffCostFunction<Vdist, 2, 1, 1, 1, 1, 1>(new Vdist(delta.vel, v_coef_)),
      NULL, &(p.a1), &(p.a2), &(p.a3), &(p.a4), &(p.T));
  stage1.SetParameterBlockConstant(&(p.T));
  
  // setup stage 2
  ceres::Problem stage2;
  stage2.AddResidualBlock(
      new ceres::AutoDiffCostFunction<Xdist, 2, 1, 1, 1, 1, 1>(new Xdist(delta.pos,     init.vel, x_coef_)),
      NULL, &(p.a1), &(p.a2), &(p.a3), &(p.a4), &(p.T));
  stage2.AddResidualBlock(
      new ceres::AutoDiffCostFunction<Vdist, 2, 1, 1, 1, 1, 1>(new Vdist(delta.vel, v_coef_)),
      NULL, &(p.a1), &(p.a2), &(p.a3), &(p.a4), &(p.T));
  stage2.SetParameterLowerBound(&(p.T), 0, 0);
//  stage2.SetParameterUpperBound(&(p.T), 0, t_max);
  
  // solve!
  ceres::Solver::Summary summary1;
  ceres::Solver::Summary summary2;
  
  Solve(options, &stage1, &summary1);
  
  if (kDebug_) {
    std::cout << "Frist Stage Solution:" << std::endl
              << p.a1 << ", " << p.a2 << ", " << p.a3 << ", "
              << p.a4 << ", " << p.T << ", " << summary1.final_cost << std::endl;
    RobotState<float> r;
    GetRobotState(init, &r, p, p.T);
    std::cout << "First Stage Final State:" << std::endl
              << r.pos.x << ", " << r.pos.y << ", " << r.vel.x << ", " << r.vel.y << std::endl;
  }
  
  Solve(options, &stage2, &summary2);
  
  if (kDebug_) {
    std::cout << "Second Stage Solution:" << std::endl
              << p.a1 << ", " << p.a2 << ", " << p.a3 << ", "
              << p.a4 << ", " << p.T << ", " << summary2.final_cost << std::endl;
    RobotState<float> r;
    GetRobotState(init, &r, p, p.T);
    std::cout << "Second Stage Final State:" << std::endl
              << r.pos.x << ", " << r.pos.y << ", " << r.vel.x << ", " << r.vel.y << std::endl
              << "Desired Final State:" << std::endl
              << fin.pos.x << ", " << fin.pos.y << ", " << fin.vel.x << ", " << fin.vel.y << std::endl;
    
  }
  
  p.cost = summary2.final_cost;
  
  p.isInitialized = summary2.final_cost <= kCostThreshold_ && 
      summary2.final_cost > 0;
  
  while (!p.isInitialized) {
    GetGuess(v0, vf, dx, params);
    p = *params;
    p.T = t_max * static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
    Solve(options, &stage1, &summary1);
    Solve(options, &stage2, &summary2);
    p.cost = summary2.final_cost;
  
    p.isInitialized = summary2.final_cost <= kCostThreshold_ && 
        summary2.final_cost > 0;
  }
  
  (*params) = p;
  
  return p.isInitialized;
}

void GetRobotState(RobotState<float> init,
                   RobotState<float>* at_time,
                   SolutionParameters<float> sol,
                   const float time_stamp) {
  
  float x = X(sol.a1, sol.a2, sol.a3, sol.a4, time_stamp) + time_stamp *init.vel.x;
  float y = X(sol.a2, sol.a1, sol.a4, sol.a3, time_stamp) + time_stamp *init.vel.y;
  float vx = V(sol.a1, sol.a2, sol.a3, sol.a4, time_stamp) + init.vel.x;
  float vy = V(sol.a2, sol.a1, sol.a4, sol.a3, time_stamp) + init.vel.y;
  
  at_time->pos = Pose2D<float>(x, y) + init.pos;
  at_time->vel = Pose2D<float>(vx, vy);
}


}  // namespace tsocs
