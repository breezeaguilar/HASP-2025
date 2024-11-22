import unittest

import struct

from HASP_25_RPI.coms.SP_PacketManager import SP_PacketManager as PM
from HASP_25_RPI.coms.SP_PacketManager import SP_Packet_Util as PU




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

if __name__ == "__main__" :
    unittest.main()