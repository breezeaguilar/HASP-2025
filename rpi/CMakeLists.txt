cmake_minimum_required(VERSION 3.15...3.26)

project(HASP-2025 
    VERSION 0.0.1 
    DESCRIPTION "C/C++ backend for utilization with HASP_2025 python control scripts"
    LANGUAGES C CXX
    )


################################################################################
###    HASP 25 C++ Library    ##################################################
################################################################################

## find pybind11, installed on local system.
set(PYBIND11_NEWPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)

## find files to compile into pybind11 shared library 
file(GLOB_RECURSE HASP-2025-Private-Source "${CMAKE_CURRENT_LIST_DIR}/HASP_25_CPP/src/*.cpp")
file(GLOB_RECURSE HASP-2025-Bindings "${CMAKE_CURRENT_LIST_DIR}/pyBind11_Bindings/*.cpp")
file(GLOB_RECURSE HASP-2025-Public-Headers "${CMAKE_CURRENT_LIST_DIR}/HASP_25_CPP/include/*.h")

## set include directory for C++
set(HASP-2025-Include "${CMAKE_CURRENT_LIST_DIR}/HASP_25_CPP/include")


pybind11_add_module(HASP_2025_CPP_lib ${HASP-2025-Bindings})

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
###    HASP 25 C Library    ####################################################
################################################################################

## find files to compile into pybind11 shared library 
file(GLOB_RECURSE HASP-2025-C-Private-Source "${CMAKE_CURRENT_LIST_DIR}/HASP_25_C/src/*.c")
file(GLOB_RECURSE HASP-2025-C-Public-Headers "${CMAKE_CURRENT_LIST_DIR}/HASP_25_C/include/*.h")

## set include directory for C++
set(HASP-2025-C-Include "${CMAKE_CURRENT_LIST_DIR}/HASP_25_C/include")

add_library(HASP_2025_C_lib SHARED "")


set_target_properties(HASP_2025_C_lib PROPERTIES LINKER_LANGUAGE C)


target_sources(HASP_2025_C_lib
    PRIVATE
        ${HASP-2025-C-Private-Source}
        
    PUBLIC
        ${HASP-2025-C-Public-Headers}
        HASP_25_C/include/export.h
        HASP_25_C/include/test.h
        HASP_25_C/src/test.c
)

target_include_directories(HASP_2025_C_lib
    PUBLIC
        ${HASP-2025-C-Include}
)

## install pybind library
install(TARGETS HASP_2025_CPP_lib HASP_2025_C_lib HASP_2025_C_lib DESTINATION HASP_2025_build)