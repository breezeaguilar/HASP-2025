import unittest

import struct
import numpy as np


from HASP_25.coms.SP_PacketManager import SP_PacketManager as PM
from HASP_25.coms.SP_PacketManager import SP_Packet_Util as PU
from HASP_25.coms.CRC import CRC
from HASP_25.coms.bind_test import square





class SP_PacketManagerTest(unittest.TestCase):

    # very basic test of the packet_util class used by packetmanager and 
    # packet strategies
    def test_packet_util(self) :
        structFormat = "> 2c I B H B"
        minStructFormat = "> 2c I"

        packetUtil = PU()

        minHeader = packetUtil.get_minimal_header()

        expectedMinHeader = bytearray(struct.pack(minStructFormat,b'S', b'P', 0))

        self.assertEqual(minHeader, expectedMinHeader)

    def test_CRC_Binding(self) :
        crcChecksum = CRC()
        array = np.array([1,2],dtype=np.uint8)
        generator = crcChecksum.get_generator()
        #print(generator)
        sum = crcChecksum.compute_CRC16(array)
        #print(sum)
        self.assertEqual(sum, 4979) # 4979 == 0x1373, the answer to crc16([0x0x,0x02])

    def test_binding(self) :
        self.assertEqual(square(2),4)


if __name__ == "__main__" :
    unittest.main()