include_guard(DIRECTORY)

include(FetchContent)

if(POLICY CMP0135)
  cmake_policy(SET CMP0135 NEW)
endif()

FetchContent_Declare(
  pybind11

  URL            https://github.com/pybind/pybind11/archive/refs/tags/v2.10.4.tar.gz
  URL_HASH       SHA256=832e2f309c57da9c1e6d4542dedd34b24e4192ecb4d62f6f4866a737454c9970
  )

# set(PYBIND11_CPP_STANDARD -std=c++17)


FetchContent_MakeAvailable(pybind11)


