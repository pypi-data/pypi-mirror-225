configure_file(config.h.in config.h)

add_library(
  grclib
  args.c
  # cfbase.c
  # cfconv.c
  cfgrf.c
  cfnbase.c
  cfnconv.c
  cmfin.c
  # cmfort.c
  cmnfort.c
  cmutl.c
  conserv.c
  dagrf.c
  divide.c
  ergrf.c
  flgrf.c
  ilgrf.c
  mvert.c
  ordset.c
  outf.c
  path.c
  perm.c
  pset.c
  putid.c
  rational.c
  rdgrf.c
  rdptbl.c
  tlgrf.c
  token.c)
target_include_directories(grclib PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
target_include_directories(grclib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
