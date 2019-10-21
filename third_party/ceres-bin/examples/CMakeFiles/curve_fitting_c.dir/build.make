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
include examples/CMakeFiles/curve_fitting_c.dir/depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/curve_fitting_c.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/curve_fitting_c.dir/flags.make

examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o: examples/CMakeFiles/curve_fitting_c.dir/flags.make
examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o: /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/curve_fitting.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o   -c /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/curve_fitting.c

examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/curve_fitting_c.dir/curve_fitting.c.i"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/curve_fitting.c > CMakeFiles/curve_fitting_c.dir/curve_fitting.c.i

examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/curve_fitting_c.dir/curve_fitting.c.s"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples/curve_fitting.c -o CMakeFiles/curve_fitting_c.dir/curve_fitting.c.s

examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.requires:

.PHONY : examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.requires

examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.provides: examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.requires
	$(MAKE) -f examples/CMakeFiles/curve_fitting_c.dir/build.make examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.provides.build
.PHONY : examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.provides

examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.provides.build: examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o


# Object files for target curve_fitting_c
curve_fitting_c_OBJECTS = \
"CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o"

# External object files for target curve_fitting_c
curve_fitting_c_EXTERNAL_OBJECTS =

bin/curve_fitting_c: examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o
bin/curve_fitting_c: examples/CMakeFiles/curve_fitting_c.dir/build.make
bin/curve_fitting_c: lib/libceres.a
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libglog.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libgflags.so.2.2.1
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libspqr.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libcholmod.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libccolamd.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libcamd.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libcolamd.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libamd.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/liblapack.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libf77blas.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libatlas.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libsuitesparseconfig.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/librt.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libcxsparse.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/liblapack.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libf77blas.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libatlas.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libsuitesparseconfig.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/librt.so
bin/curve_fitting_c: /usr/lib/x86_64-linux-gnu/libcxsparse.so
bin/curve_fitting_c: examples/CMakeFiles/curve_fitting_c.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable ../bin/curve_fitting_c"
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/curve_fitting_c.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/curve_fitting_c.dir/build: bin/curve_fitting_c

.PHONY : examples/CMakeFiles/curve_fitting_c.dir/build

examples/CMakeFiles/curve_fitting_c.dir/requires: examples/CMakeFiles/curve_fitting_c.dir/curve_fitting.c.o.requires

.PHONY : examples/CMakeFiles/curve_fitting_c.dir/requires

examples/CMakeFiles/curve_fitting_c.dir/clean:
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples && $(CMAKE_COMMAND) -P CMakeFiles/curve_fitting_c.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/curve_fitting_c.dir/clean

examples/CMakeFiles/curve_fitting_c.dir/depend:
	cd /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0 /home/amodh/Downloads/WaypointLearning/third_party/ceres-solver-1.14.0/examples /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples /home/amodh/Downloads/WaypointLearning/third_party/ceres-bin/examples/CMakeFiles/curve_fitting_c.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/curve_fitting_c.dir/depend

