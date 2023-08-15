# FindLibM
#
# Find the math library.
#
include(CheckFunctionExists)
include(FindPackageHandleStandardArgs)

find_library(LIBM_LIBRARIES NAMES m libm)

if(LIBM_LIBRARIES)
  set(LIBM_OK ${LIBM_LIBRARIES})
else()
  check_function_exists(pow LIBM_OK)
endif()

find_package_handle_standard_args(LibM REQUIRED_VARS LIBM_OK)

# message("LIBM_OK=${LIBM_OK}")

if(LIBM_OK AND NOT TARGET LibM::LibM)
  add_library(LibM::LibM INTERFACE IMPORTED)
  if(LIBM_LIBRARIES)
    target_link_libraries(LibM::LibM INTERFACE ${LIBM_LIBRARIES})
  endif()
endif()

mark_as_advanced(LIBM_LIBRARIES LIBM_OK)
