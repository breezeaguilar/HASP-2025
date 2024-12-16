from abc import ABC, abstractmethod

class SP_Packet_Strategy(ABC):
    
    @abstractmethod
    def packetize(data: object) :
        pass

    @abstractmethod
    def depacketize(data: bytes) :
        pass