cmake_minimum_required(VERSION 3.18)
project(grace C Fortran)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

# configurations

cmake_host_system_information(RESULT BUILD_HOSTNAME QUERY HOSTNAME)

set(GRACE_DIR "$(GRACEROOT)")
set(GRACE_LIBDIR "$(GRACEROOT)/lib")
set(GRACE_MODEL_PATH ".:$(GRACEROOT)/lib/model")
set(GRACE_KINEM_PATH ".:$(GRACEROOT)/lib/dbkinem")
set(GRACE_FC "${CMAKE_Fortran_COMPILER}")
set(GRACE_FCFLAGS "${CMAKE_Fortran_FLAGS_RELEASE}")
set(GRACE_LDFLAGS "")
set(GRACE_REDUCE "reduce")
set(GRACE_FORM "form")
set(GRACE_FORMFLAGS "-M -si -D BESILENT")
set(GRACE_MPIHOME "/mpihome")
set(GRACE_CERNLIB "/cernlib")

# sources

add_subdirectory(basesv5.1)
add_subdirectory(chanel)
add_subdirectory(dbkinem)
add_subdirectory(gracefig)
add_subdirectory(grcfort)
add_subdirectory(grclib)
add_subdirectory(grcsrc)
add_subdirectory(grcutl)
add_subdirectory(kinemlib)
add_subdirectory(model)
add_subdirectory(netlib/blas)
add_subdirectory(netlib/lapack/double)
add_subdirectory(templates)
