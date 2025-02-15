from threading import Thread

#Control Modules
CommsModule = None

# Control Threads

def init() :
    data = "$GPGGA,202212.00,3024.7205,N,09110.7264,W,1,06,1.69,00061,M,-025,M,,*51" # test packet
    # is NMEA identifier independent of packet verify ?
    if verifyPacket(data):  # checksum always isnt done

        pass

def verifyPacket(data) -> bool:    # packet received, perform checksum
    # TODO: perform bitwise XOR on characters between "$" and "*" of message
    # check calculated hex result against original message checksum



    # decode message after integrity check


    gpsdecode(data)
    pass

def gpsdecode(data) :
    # TODO: split strings using comma delimiters in message
    # get fields in between commas
    # calculate fields


    data[1] == 0
    
if(__name__ == "__main__") : init()