cmake_minimum_required(VERSION 2.8.12)
project(waypointlearning)

find_package(Ceres REQUIRED)
include_directories(${CERES_INCLUDE_DIRS})

add_executable(waypointlearning main.cpp)

install(TARGETS waypointlearning RUNTIME DESTINATION bin)
