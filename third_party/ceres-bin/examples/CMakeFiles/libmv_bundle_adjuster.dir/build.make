# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin

# Include any dependencies generated for this target.
include examples/CMakeFiles/libmv_bundle_adjuster.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/libmv_bundle_adjuster.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/libmv_bundle_adjuster.dir/flags.make

examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o: examples/CMakeFiles/libmv_bundle_adjuster.dir/flags.make
examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o: /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/libmv_bundle_adjuster.cc
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o -c /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/libmv_bundle_adjuster.cc

examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.i"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/libmv_bundle_adjuster.cc > CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.i

examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.s"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/libmv_bundle_adjuster.cc -o CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.s

examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.requires:

.PHONY : examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.requires

examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.provides: examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.requires
	$(MAKE) -f examples/CMakeFiles/libmv_bundle_adjuster.dir/build.make examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.provides.build
.PHONY : examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.provides

examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.provides.build: examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o


# Object files for target libmv_bundle_adjuster
libmv_bundle_adjuster_OBJECTS = \
"CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o"

# External object files for target libmv_bundle_adjuster
libmv_bundle_adjuster_EXTERNAL_OBJECTS =

bin/libmv_bundle_adjuster: examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o
bin/libmv_bundle_adjuster: examples/CMakeFiles/libmv_bundle_adjuster.dir/build.make
bin/libmv_bundle_adjuster: lib/libceres.a
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libgflags.so.2.2.1
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libglog.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libspqr.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libcholmod.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libccolamd.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libcamd.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libcolamd.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libamd.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/liblapack.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libf77blas.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libatlas.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libsuitesparseconfig.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/librt.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libcxsparse.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/liblapack.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libf77blas.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libatlas.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libsuitesparseconfig.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/librt.so
bin/libmv_bundle_adjuster: /usr/lib/x86_64-linux-gnu/libcxsparse.so
bin/libmv_bundle_adjuster: examples/CMakeFiles/libmv_bundle_adjuster.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../bin/libmv_bundle_adjuster"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/libmv_bundle_adjuster.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/libmv_bundle_adjuster.dir/build: bin/libmv_bundle_adjuster

.PHONY : examples/CMakeFiles/libmv_bundle_adjuster.dir/build

examples/CMakeFiles/libmv_bundle_adjuster.dir/requires: examples/CMakeFiles/libmv_bundle_adjuster.dir/libmv_bundle_adjuster.cc.o.requires

.PHONY : examples/CMakeFiles/libmv_bundle_adjuster.dir/requires

examples/CMakeFiles/libmv_bundle_adjuster.dir/clean:
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && $(CMAKE_COMMAND) -P CMakeFiles/libmv_bundle_adjuster.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/libmv_bundle_adjuster.dir/clean

examples/CMakeFiles/libmv_bundle_adjuster.dir/depend:
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0 /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples/CMakeFiles/libmv_bundle_adjuster.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/libmv_bundle_adjuster.dir/depend

