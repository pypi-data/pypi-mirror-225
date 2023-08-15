add_executable(grcfort ftgrf.c ftmakes.c genfort.c)
target_link_libraries(grcfort PRIVATE grclib)
install(TARGETS grcfort RUNTIME DESTINATION bin)
