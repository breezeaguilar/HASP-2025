#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

#include "CRC.h"

namespace py = pybind11;

template <typename MODULE>
void bind_CRC_class(MODULE m) {
  py::class_<CRC> CRC_binding(m, "CRC");
  CRC_binding.def(py::init());
  CRC_binding.def("setGenerator", &CRC::setGenerator);
  CRC_binding.def("getGenerator", &CRC::getGenerator);
  CRC_binding.def("compute_CRC16", 
  [CRC_binding](CRC& crc, py::array_t<uint8_t> array, int length) 
  {
    auto buf = array.request();
    uint8_t* ptr = (uint8_t*) buf.ptr;
    auto ret = crc.compute_CRC16(ptr,length);
    return ret;
  });
  CRC_binding.def("getEndianness", &CRC::getEndianness);
}