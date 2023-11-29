cmake_minimum_required(VERSION 3.15...3.27)
project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES CXX)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Release)
ENDIF()

function(print_all_targets DIR)
    get_property(TGTS DIRECTORY "${DIR}" PROPERTY BUILDSYSTEM_TARGETS)
    foreach(TGT IN LISTS TGTS)
        message(STATUS "Target: ${TGT}")
        # TODO: Do something about it
    endforeach()

    get_property(SUBDIRS DIRECTORY "${DIR}" PROPERTY SUBDIRECTORIES)
    foreach(SUBDIR IN LISTS SUBDIRS)
        print_all_targets("${SUBDIR}")
    endforeach()
endfunction()


MESSAGE("Build type: " ${CMAKE_BUILD_TYPE})

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}  -Wall -w  ")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -w ")

# Check C++11 or C++0x support
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)

add_compile_options(-std=c++11 -fPIC -O3)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(CMAKE_MODULE_PATH
        ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

add_subdirectory(submodules/opencv-4.8.1)
#print_all_targets(.)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)
#find_package(OpenCV 4 REQUIRED)
find_package(NumPy REQUIRED)

#add_subdirectory(submodules/pybind11)
include_directories("submodules/pybind11/include")
include_directories("submodules/pybind11_opencv_numpy")

python_add_library(_core MODULE src/main.cpp submodules/pybind11_opencv_numpy/ndarray_converter.cpp WITH_SOABI)
target_link_libraries(_core PRIVATE pybind11::headers)

##pybind11_add_module(stag
##        src/StagModule.cpp
##        submodules/pybind11_opencv_numpy/ndarray_converter.cpp
##)

file(GLOB SRC_FILE1 "submodules/stag/src/*.c*")
file(GLOB SRC_FILE2 "submodules/stag/src/ED/*.c*")

include_directories(
    ${OpenCV_INCLUDE_DIRS}
    ${NUMPY_INCLUDES}
    stag/
    stag/ED/
)
add_library(
    staglib STATIC
    ${SRC_FILE1}
    ${SRC_FILE2}
)
target_link_libraries(
    staglib
    ${OpenCV_LIBS}
)

target_link_libraries(
    _core PRIVATE
    #${OpenCV_LIBS}
    #staglib
)

MESSAGE("${OpenCV_LIBS}")
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/app)
install(TARGETS _core DESTINATION stag)
install(TARGETS opencv_core opencv_imgproc DESTINATION stag)
