cmake_minimum_required(VERSION 3.18)
project(grcext LANGUAGES NONE)

install(
  FILES grcext.py
  DESTINATION bin
  PERMISSIONS
    OWNER_READ
    OWNER_WRITE
    OWNER_EXECUTE
    GROUP_READ
    GROUP_EXECUTE
    WORLD_READ
    WORLD_EXECUTE
  RENAME grcext)
