#ifndef SRC_TSOCS_STRUCTURES_H_
#define SRC_TSOCS_STRUCTURES_H_

#include "data_structures.h"
#include "tsocs_templates.h"

using Eigen::Vector2d;
using data_structs::Pose2D;

namespace data_structs {

template <typename S = float>
struct SolutionParameters {
  S a1, a2, a3, a4, T, cost;
  bool isInitialized;

  SolutionParameters() : isInitialized(false) {}

  SolutionParameters(const S a1, const S a2,
                     const S a3, const S a4,
                     const S T) : a1(a1), a2(a2),
                     a3(a3), a3(a3), T(T),
                     isInitialized(true), cost(cost) {}

  SolutionParameters(const S a1, const S a2,
                    const S a3, const S a4,
                    const S T, const S cost) : a1(a1), a2(a2),
                    a3(a3), a3(a3), T(T),
                    isInitialized(true), cost(cost) {}

  template <typename H>
  SolutionParameters(const SolutionParameters<H> &sol) :
                    a1(sol.a1), a2(sol.a2), a3(sol.a3), a4(sol.a4),
                    T(sol.T), cost(sol.cost),
                    isInitialized(sol.isInitialized) {}

  template <typename H>
  SolutionParameters& operator= (const SolutionParameters<H> &sol) {
    a1 = sol.a1;
    a2 = sol.a2;
    a3 = sol.a3;
    a4 = sol.a4;
    T = sol.T;
    cost = sol.cost;
    isInitialized = sol.isInitialized;

    return *this;
  }
};

struct Xdist {
  Xdist(Pose2D<float> displ, Pose2D<float> vel0, float coef) : 
      displ(displ), v0(vel0), coef(coef) {}

  template <typename T>
  bool operator()(const T* const a, const T* const b, const T* const c,
                  const T* const d, const T* const t, T* residual) const {
    if (*t < T(0)) {
      return false;
    }

    T x1 = X(*a, *b, *c, *d, *t) + T(v0.x) * t[0];
    T x2 = X(*b, *a, *d, *c, *t) + T(v0.y) * t[0];

    if (ceres::IsNaN(x1) || ceres::IsNaN(x2)) {
      printf("In Xdist:\n");
      cout << "x1 = " << x1 << endl;
      cout << "x2 = " << x2 << endl;
      cout << "a: " << *a << endl;
      cout << "b: " << *b << endl;
      cout << "c: " << *c << endl;
      cout << "d: " << *d << endl;
      cout << "T: " << *t << endl;
    }

    residual[0] =
        T(sqrt(coef)) * (x1 - T(displ.x));
    residual[1] =
        T(sqrt(coef)) * (x2 - T(displ.y));

    return true;
  }

  const Pose2D<float> displ;
  const Pose2D<float> v0;
  const float coef;
};

struct Vdist {
  Vdist(Pose2D<float> delta_vel, float coef) : delta_vel(delta_vel), coef(coef) {}

  template <typename T>
  bool operator()(const T* const a, const T* const b, const T* const c,
                  const T* const d, const T* const t, T* residual) const {
    if (*t < T(0)) {
      return false;
    }

    T v1 = V(*a, *b, *c, *d, *t);
    T v2 = V(*b, *a, *d, *c, *t);

    if (ceres::IsNaN(v1) || ceres::IsNaN(v2)) {
      printf("In Vdist:\n");
      cout << "v1 = " << v1 << endl;
      cout << "v2 = " << v2 << endl;
      cout << "a: " << *a << endl;
      cout << "b: " << *b << endl;
      cout << "c: " << *c << endl;
      cout << "d: " << *d << endl;
      cout << "T: " << *t << endl;
    }

    residual[0] =
        T(sqrt(coef)) * (v1 - T(delta_vel.x));
    residual[1] =
        T(sqrt(coef)) * (v2 - T(delta_vel.y));

    return true;
  }

  const Pose2D<float> delta_vel;
  const float coef;
};

}  // namespace data_structs

#endif  // SRC_TSOCS_STRUCTURES_H_
