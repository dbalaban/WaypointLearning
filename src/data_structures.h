#ifndef SRC_DATA_STRUCTURES_H_
#define SRC_DATA_STRUCTURES_H_

#include <Eigen/Dense>
#include <Eigen/Geometry>

#include "ceres/ceres.h"
#include "glog/logging.h"

#include "eigen3/Eigen/Dense"

namespace data_structs {

typedef Eigen::Matrix<float, 4, Eigen::Dynamic> StateSet;

template<typename T = float>
struct Pose2D {
  Pose2D() : x(0.0), y(0.0) {}
  
  Pose2D(const T x, const T y)
      : x(x), y(y) {}
  
  template<typename S>
  Pose2D operator-(const Pose2D<S>& r) const {
    return Pose2D(this->x - r.x, this->y - r.y);
  }
  template<typename S>
  Pose2D operator+(const Pose2D<S>& r) const {
    return Pose2D(this->x + r.x, this->y + r.y);
  }
  
  template<typename S>
  void operator+=(const Pose2D<S>& r) {
    this->x += r.x;
    this->y += r.y;
  }
  
  template<typename S>
  Pose2D operator*(const S m) const {
    return Pose2D(m*(this->x), m*(this->y));
  }
  
  template<typename S>
  Pose2D operator*=(const Pose2D<S>& m) const {
    this->x *= m;
    this->y *= m;
  }
  
  template<typename S>
  Pose2D operator/(const S m) const {
    return Pose2D((this->x)/m, (this->y)/m);
  }
  
  template<typename S>
  Pose2D operator/=(const Pose2D<S>& m) const {
    this->x /= m;
    this->y /= m;
  }
  
  template<typename S>
  Pose2D& operator=(const Pose2D<S>& pose) {
    x = pose.x;
    y = pose.y;
    
    return *this;
  }
  
  Eigen::Vector2f toEigen() {
    return Eigen::Vector2f(x, y);
  }
  
  T x;
  T y;
};

template<typename T>
struct RobotState {
  RobotState() : pos(), vel() {}

  RobotState(const Pose2D<T> pos, const Pose2D<T> vel)
      : pos(pos), vel(vel) {}

  template<typename S>
  RobotState operator-(const RobotState<S>& r) const {
    return RobotState(this->pos - r.pos, this->vel - r.vel);
  }
  
  template<typename S>
  RobotState operator+(const RobotState<S>& r) const {
    return RobotState(this->pos + r.pos, this->vel + r.vel);
  }
  
  template<typename S>
  void operator+=(const S& r) {
    this->pos += r.pos;
    this->vel += r.vel;
  }
  
  template<typename S>
  RobotState operator*(const S m) const {
    return RobotState(m*(this->pos), m*(this->vel));
  }
  
  template<typename S>
  void operator*=(const S m) {
    this->pos *= m;
    this->vel *= m;
  }
  
  template<typename S>
  RobotState operator/(const S m) const {
    return RobotState((this->pos)/m, (this->vel)/m);
  }
  
  template<typename S>
  void operator/=(const S m) {
    this->pos /= m;
    this->vel /= m;
  }
  
  template<typename S>
  RobotState& operator=(const RobotState<S>& state) {
    pos = state.pos;
    vel = state.vel;
    
    return *this;
  }

  Pose2D<T> pos;
  Pose2D<T> vel;
};

}  // namespace data_structs

#endif  // SRC_DATA_STRUCTURES_H_
