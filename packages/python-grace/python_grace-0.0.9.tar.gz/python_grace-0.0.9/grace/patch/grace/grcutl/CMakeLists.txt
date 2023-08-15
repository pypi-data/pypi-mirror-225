find_package(LibM REQUIRED)
find_package(X11)

if(X11_FOUND)
  add_executable(
    grcdraw
    dcx.c
    draw.c
    drgrf.c
    vr.c
    vrps.c
    vrx.c
    window.c)
  foreach(file dcx.c vrx.c)
    set_source_files_properties(${file} PROPERTIES COMPILE_DEFINITIONS "X11")
  endforeach()
  target_link_libraries(grcdraw PRIVATE grclib X11::X11 LibM::LibM)
  install(TARGETS grcdraw RUNTIME DESTINATION bin)
endif()

add_executable(grcplot drgrf.c plot.c vrplot.c vrps.c window.c)
target_link_libraries(grcplot PRIVATE grclib LibM::LibM)
install(TARGETS grcplot RUNTIME DESTINATION bin)

add_executable(grcmdl pread.c)
target_link_libraries(grcmdl PRIVATE grclib)
install(TARGETS grcmdl RUNTIME DESTINATION bin)

add_executable(qcdcut qcdcut.c)
target_link_libraries(qcdcut PRIVATE grclib)
install(TARGETS qcdcut RUNTIME DESTINATION bin)

add_executable(grcmom grcmom.c)
target_link_libraries(grcmom PRIVATE grclib)
install(TARGETS grcmom RUNTIME DESTINATION bin)

add_executable(tread tread.c)
target_link_libraries(tread PRIVATE grclib)
install(TARGETS tread RUNTIME DESTINATION bin)

add_executable(grccut grccut.c)
target_link_libraries(grccut PRIVATE grclib)
install(TARGETS grccut RUNTIME DESTINATION bin)
