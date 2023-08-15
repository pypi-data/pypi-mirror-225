cmake_minimum_required(VERSION 3.18)
project(python-grace C Fortran)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

add_subdirectory(grace)
add_subdirectory(grcext)
