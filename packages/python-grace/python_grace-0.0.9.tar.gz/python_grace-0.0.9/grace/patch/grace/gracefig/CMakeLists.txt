find_package(LibM REQUIRED)
find_package(X11)
find_package(Motif)

if(X11_FOUND
   AND X11_Xt_FOUND
   AND MOTIF_FOUND)
  add_executable(
    gracefig
    adjustf.c
    charlib.c
    gfgraph.c
    gfname.c
    gfread.c
    gftree.c
    gracefig.c
    putloop.c
    rmloop.c
    urx.c
    vtxtable.c)
  target_include_directories(gracefig PRIVATE ${MOTIF_INCLUDE_DIR})
  target_link_libraries(gracefig PRIVATE ${MOTIF_LIBRARIES} X11::Xt X11::X11
                                         LibM::LibM)
  install(TARGETS gracefig RUNTIME DESTINATION bin)

  # The -fcommon option is available with Clang, GNU, and Intel (Linux and
  # macOS) compilers.
  target_compile_options(gracefig PRIVATE "-fcommon")
endif()
