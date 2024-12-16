import time
from HASP_25.coms.CRC import CRC

# holds different packet encodings, and handles generating and reading packets
class SP_PacketManager:

    PacketStrategies = {} 


    def __init__(self) :
        if(True) :
            print("ERROR: SP_PacketManager not implemented")
            return
    

    def packetize(data:object) -> bytearray:
        
        # insert necessary data
        # preprocess data
        # generate header
        # postProcess data
        # return packet bytearray stream
        if(True) :
            print("ERROR: SP_PacketManager.constructPacket not implemented")
            return
    
    # determine the precondition for this. takes in a packetType object
    def register_packet_type(packetType:object) :

        # generate a packetization strategy from packet factory
        # store packet strategy in packetStrategies
        if(True) :
            print("ERROR: SP_PacketManager.registerPacket")


# Data Structure containing all required data for managing packets
# C++ IMPLEMENTATION CANDIDATE
class SP_Packet_Util :
    SP_IDENTIFIER_SIZE_BYTES = 2
    ID_SIZE_BYTES = 4
    PACKET_TYPE_SIZE_BYTES = 1
    CHECKSUM_SIZE_BYTES = 2
    DATA_LENGTH_SIZE_BYTES = 1
    
    HEADER_SIZE_BYTES = 10  #TYPO IN PROPOSAL: off-by-one and ID took up 5 
                            #bytes made header size == 12 when it is 10. 
    MINIMAL_HEADER_SIZE_BYTES = 6
    MAX_PACKET_SIZE = 256
    MAX_DATA_SIZE = MAX_PACKET_SIZE - HEADER_SIZE_BYTES

    SP_IDENTIFIER_INDEX = 0
    ID_INDEX = 2
    PACKET_TYPE_INDEX = 6
    CHECKSUM_INDEX = 7
    DATA_LENGTH_INDEX = 9

    PACKET_ENDIANESS = "big"

    SP_IDENTIFIER = b'SP' # "SP" as raw ascii bytes

    Checksum_key = b'\x10\x21'

    Checksum = None

    PacketId = 0 #consider this to be uint functionally 

    def __init__(self) :
        self.Checksum = CRC()
        pass

    # generates and returns an unused packet id
    def get_packetID(self) -> bytearray :
        ret = self.PacketId
        self.PacketId+=1
        return ret.to_bytes(self.ID_SIZE_BYTES,self.PACKET_ENDIANESS)
    
    # get time in ns since epoch
    def get_time(self) -> bytearray :
        return time.time_ns().to_bytes(8,self.PACKET_ENDIANESS)
    
    # get a generic header byte array, with a valid header identifier and
    # packetID, totalling 6 Bytes in length.
    # Prequisite: None.
    def get_minimal_header(self) -> bytearray :
        header = bytearray(self.SP_IDENTIFIER)
        header.extend(self.get_packetID())
        return header
    
    # get a fully filled out packet header
    # Prerequisite: all packet datatype specific data evaluated and placed in data array
    def get_header(self, packetType: int, data: bytearray) -> bytearray :
        dataLen = len(data)
        header = self.get_minimal_header() # packet identifier and 
        header.extend(packetType.to_bytes(self.PACKET_TYPE_SIZE_BYTES,self.PACKET_ENDIANESS)) # Packet Type
        header.extend((0).to_bytes(self.CHECKSUM_SIZE_BYTES,self.PACKET_ENDIANESS)) # fill in temporary checksum value 0
        header.extend(dataLen.to_bytes(self.DATA_LENGTH_SIZE_BYTES,self.PACKET_ENDIANESS)) # fill in data type
        header[self.CHECKSUM_INDEX:self.DATA_LENGTH_INDEX] = self.get_checksum(header+data) # calculate checksum and insert it into header
        return header

    # get the configured checksum of the data bytearray
    def get_checksum(self, data: bytearray) -> int :
        return self.Checksum.compute_CRC16(data)

    # get the full packet in the form of a bytearray
    def get_packet_bytearray(self, packetType: int, data: bytearray) -> bytearray:
        if(len(data) > self.MAX_DATA_SIZE) :
            return None
        packet = self.get_header(packetType, data)
        packet.extend(data)
        return packet

    # verify the integrity of a packet
    def verify_packet(self, data) -> bool:
        if(True):
            print("ERROR: SP_PacketManager.SP_Packet_Util.verify_packet not implemented!")
        pass
