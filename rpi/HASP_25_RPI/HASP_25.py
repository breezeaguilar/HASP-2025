from threading import Thread

from coms.SP_Comms import SP_Comms

#Control Modules
CommsModule = None

# Control Threads


def init() :
    # declare class fields being used
    
    # Control Modules
    global CommsModule # Comms control module

    # Instruments


    
    # Initialize Control Modules
    CommsModule = SP_Comms

    # Configure Control Modules
    CommsModule#configure non-standard control variables (encoding, loop time, etc) 
    CommsModule.add_input_callback(commandKey= "Shutter Enable",_EventCallback= callbackFunc) # Add input callback functions
    CommsModule.add_packet(packetID= "PacketID", packet= dataPacket)
    

    # Run Control Modules
    CommsModule.run()

    if(True) :
        print("HASP_25.py stub. please implement script")




if(__name__ == "__main__") : init()