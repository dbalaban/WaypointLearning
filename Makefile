C_compiler=/usr/bin/gcc
CXX_compiler=/usr/bin/g++

build_type=Release

ifeq ($(build_type),Debug)
	override build_dir=build_debug
else
	build_dir=build
endif
.SILENT:

all: $(build_dir) $(build_dir)/CMakeLists.txt.copy
	$(info $$build_type is [${build_type}])
	$(MAKE) --no-print-directory -C $(build_dir)

clean:
	rm -rf $(build_dir) bin lib

$(build_dir)/CMakeLists.txt.copy: CMakeLists.txt src/proto Makefile $(build_dir)
	cd $(build_dir) && cmake -DCMAKE_BUILD_TYPE=$(build_type) \
		-DCMAKE_CXX_COMPILER=$(CXX_compiler) \
		-DCMAKE_C_COMPILER=$(C_compiler) \
		-DSWARM_TARGETS=FALSE  ..
	cp CMakeLists.txt $(build_dir)/CMakeLists.txt.copy

$(build_dir):
	mkdir -p $(build_dir)

cleanup_cache:
	rm -rf $(build_dir)
