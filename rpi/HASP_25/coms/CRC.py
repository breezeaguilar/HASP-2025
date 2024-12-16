import numpy as np

from HASP_2025_build import HASP_2025_CPP_lib



class CRC :
    crc = None
    def __init__(self) :
        self.crc = HASP_2025_CPP_lib.CRC()

    def get_generator(self) :
        return self.crc.getGenerator()

    def set_generator(self, ngen) :
        self.crc.setGenerator(ngen)

    def getEndianness(self) :
        return self.crc.getEndianness()

    def compute_CRC16(self, stream) :
        return self.crc.compute_CRC16(stream, len(stream))