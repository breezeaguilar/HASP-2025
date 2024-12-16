#include <pybind11/pybind11.h>
#include "CRC_Wrapper.cpp"


namespace py = pybind11;

PYBIND11_MODULE(HASP_2025_CPP_lib, m){
  bind_CRC_class(m);
}