add_executable(
  grc
  alist.c
  alist.c
  assign.c
  axconn.c
  bfconn.c
  biconn.c
  elem.c
  gnode.c
  grc.c
  hepend.c
  iline.c
  lclass.c
  print.c
  rdprocs.c
  scalar.c)
target_link_libraries(grc PRIVATE grclib)
install(TARGETS grc RUNTIME DESTINATION bin)

add_executable(grcprc elem.c genprc.c rdprocs.c)
target_link_libraries(grcprc PRIVATE grclib)
install(TARGETS grcprc RUNTIME DESTINATION bin)
