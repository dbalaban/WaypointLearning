cmake_minimum_required(VERSION 2.8.12)

project(waypointlearning)

SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
SET(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)
SET(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/third_party/")

ADD_LIBRARY(tsocs_library src/tsocs.cc)

find_package(Ceres REQUIRED)
include_directories(${CERES_INCLUDE_DIRS})

add_executable(waypointlearning src/main.cpp)
TARGET_LINK_LIBRARIES(waypointlearning tsocs_library ${CERES_LIBRARIES})

add_executable(solve src/solve.cc)
TARGET_LINK_LIBRARIES(solve tsocs_library ${CERES_LIBRARIES})

add_executable(eval src/evaluate.cc)
TARGET_LINK_LIBRARIES(eval tsocs_library ${CERES_LIBRARIES})

install(TARGETS waypointlearning RUNTIME DESTINATION bin)
install(TARGETS solve RUNTIME DESTINATION bin)
install(TARGETS eval RUNTIME DESTINATION bin)
