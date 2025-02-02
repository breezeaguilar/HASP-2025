cmake_minimum_required(VERSION 3.15...3.26)

project(HASP-2025 
    VERSION 0.0.1 
    DESCRIPTION "C/C++ backend for utilization with HASP_2025 python control scripts"
    LANGUAGES C CXX
    )


################################################################################
###    HASP 25 C++ Library    ##################################################
################################################################################

## find files to compile into shared library 
file(GLOB_RECURSE HASP-2025-Private-Source "${CMAKE_CURRENT_LIST_DIR}/HASP_25_CPP/src/*.cpp")
file(GLOB_RECURSE HASP-2025-Public-Headers "${CMAKE_CURRENT_LIST_DIR}/HASP_25_CPP/include/*.h")

## set include directory for C++
set(HASP-2025-Include "${CMAKE_CURRENT_LIST_DIR}/HASP_25_CPP/include")

add_library(HASP_2025_CPP_lib "")

target_sources(HASP_2025_CPP_lib
    PRIVATE
        ${HASP-2025-Private-Source}
    PUBLIC
        ${HASP-2025-Public-Headers}
)

target_include_directories(HASP_2025_CPP_lib
    PUBLIC
        ${HASP-2025-Include}
)

################################################################################
###    HASP 25 Testing    ######################################################
################################################################################

#enable_testing()

