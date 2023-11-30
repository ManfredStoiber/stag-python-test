cmake_minimum_required(VERSION 3.16)
project(stag-python)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Release)
ENDIF()

MESSAGE("Build type: " ${CMAKE_BUILD_TYPE})

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS}  -Wall -w  ")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -w ")

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/libarch)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/liblibr)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/binrunt)

# Check C++11 or C++0x support
set(CMAKE_CXX_STANDARD 11)
include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)

add_compile_options(-std=c++11 -fPIC -O3 /std:c++11)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 /std:c++11")

set(CMAKE_MODULE_PATH
        ${CMAKE_MODULE_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

find_package(OpenCV 4 REQUIRED)
find_package(NumPy REQUIRED)

get_target_property(tmp opencv_core LIBRARY_OUTPUT_DIRECTORY)
set_target_properties(opencv_core
        PROPERTIES
        ARCHIVE_OUTPUT_DIRECTORY "C:/stag-python-test/build/testarch/"
        LIBRARY_OUTPUT_DIRECTORY "C:/stag-python-test/build/testlib/"
        RUNTIME_OUTPUT_DIRECTORY "C:/stag-python-test/build/testrun/"
)

add_subdirectory(submodules/pybind11)
include_directories("submodules/pybind11/include")
include_directories("submodules/pybind11_opencv_numpy")

set(CMAKE_CXX_STANDARD 11)
pybind11_add_module(stag
        StagModule.cpp
        submodules/pybind11_opencv_numpy/ndarray_converter.cpp
)

file(GLOB SRC_FILE1 "submodules/stag/src/*.c*")
file(GLOB SRC_FILE2 "submodules/stag/src/ED/*.c*")

include_directories(
    ${OpenCV_INCLUDE_DIRS}
    ${NUMPY_INCLUDES}
    stag/
    stag/ED/
)
set(CMAKE_CXX_STANDARD 11)
add_library(
    staglib STATIC
    ${SRC_FILE1}
    ${SRC_FILE2}
)
set_property(TARGET staglib PROPERTY CXX_STANDARD 11)
set_property(TARGET staglib PROPERTY CXX_STANDARD_REQUIRED ON)

set_property(TARGET stag PROPERTY CXX_STANDARD 11)
set_property(TARGET stag PROPERTY CXX_STANDARD_REQUIRED ON)
target_link_libraries(
    staglib
    ${OpenCV_LIBS}
)

target_link_libraries(
    stag PRIVATE
    ${OpenCV_LIBS}
    staglib
)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/app)
