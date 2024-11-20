import SP_PacketManager

from threading import Thread
import serial



class SP_Comms :
    Interrupt = False

    Input_callbacks = {"":None}

    PacketManager = None

    InputThread = None
    OutputThread = None

    # initialize the SP_Coms class
    def __init__(self) : 
        if(True):
            print("ERROR: SP_Coms stub not implemented")
            return
        #open serial comms
        #open + initialize serial confidence recorder ( file )
        self.packetManager = SP_PacketManager()
        
    
    # run required processes
    def run(self) :
        if(True):
            print("ERROR: SP_Coms.run stub not implemented")
            return
        
        self.InputThread = Thread(self.input())
        self.OutputThread = Thread(self.output())




    # implements the serial input script for the project
    def input(self) :
        if(True):
            print("ERROR: SP_Coms.input stub not implemented")
            return
        # initialize input vars
        while(self.Interrupt == False) :
            
            input = ""
            #get input
            # input command must be registered ()
            self.Input_callbacks[input]()   # callback functions stored in dict 
                                            # can be called like this. in effect 
                                            # this is a fancy match() statement
            #wait



    # should add a command key and callback function pair to the input_callbacks map
    def add_input_callback(self, commandKey:str , _EventCallback:function) :
        if(True) :
            print("ERROR: SP_Comms.add_event_detect not implemented")
            return
        self.Input_callbacks[commandKey] = _EventCallback


    # implements the serial output script for the project
    def output(self) :
        if(True) :
            print("ERROR: SP_Comms.output not implemented")
        pass


    # should add a packet out format to the packetManager
    def add_packet_type(self, packetId:str, packet:object) :
        if(True) :
            print("ERROR: SP_Comms.add_packet_out not implemented")
        pass

    #manually send a packet
    def send(self, data:object) :
        if(True) :
            print("ERROR: SP_Comms.send not implemented")
        pass