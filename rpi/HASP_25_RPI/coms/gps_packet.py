import re
from datetime import datetime

##encodes a GPGGA gps signal
def gpsencode(datarray) -> str :
    original_msg = datarray
    return original_msg
    ## this will be our "transmitter" of the packet
    # reverse of gps decode function
    # encode a str to a bytes object

##verifies a GPGGA gps signal
def verifyPacket(data : str ) -> bool:    ## put this in gpsdecode later

    # extract fields between '$' and '*'
    ch_between = data[1:data.find('*')]
    checksum = 0    # identity property

    # find a way to make it so the removal includes delimiter
    # track position using original data

    def intToHex(checksum, base=16) -> hex:
        return hex(checksum)
    splitmsg = data.split(',')

    for position in splitmsg :
        original_chksum = position
        if(original_chksum.startswith('*')) :
            original_chksum = original_chksum[1:]
            break
        else :
            print('checking ...')

    for ch in ch_between :
        checksum ^= ord(ch)
    checksum = intToHex(checksum)

    if(checksum[2:] == original_chksum) :
        print('Valid checksum, packet verified')
        gpsdecode(data)
    else :
        print('Invalid checksum')
        # discard original sentence

##decodes a GPGGA gps signal
def gpsdecode(data : str) : # could become a class later
    # this will be our "receiver of the packet" - 
    # read sentence completely before decode
    # decode fields

    if(data[0] == "$") :    # is it nmea?
        index = 1
        while data[index] != '*' and index < len(data) :
                index += 1
        if(data[index] == '*') :
            fields = data.split(',')    # split
            return parsemsg(fields)
        else :
            return "Sentence not read, '*' missing"

def parsemsg(fields) :
    UTC_Pattern = r'^\d{6}\.\d{2}$'
    Lat_Pattern = r'^\d{2}\d{2}\.\d{4}$'
    Long_Pattern = r'^\d{3}\d{2}\.\d{4}$'

    for index, part in enumerate(fields) :
          #part will update
        #isLong = re.match(longitudeFormat, part)
        # Format pattern identifiers  
            UTC_Match = re.match(UTC_Pattern,part)
            Lat_Match = re.match(Lat_Pattern,part)
            Long_Match = re.match(Long_Pattern,part)
            # Find UTC position 
            if UTC_Match:
                UTC_Position = part   
                check_time = datetime.strptime(part, "%H%M%S.%f")
                # Formatting UTC Pos.
                UTC_Position = datetime.strftime(check_time,'%H:%M:%S.%f')
                print(f'UTC Position found; {UTC_Position}')

            elif Lat_Match and index < len(fields) - 1: # ADD LATER: is degree between 0 and 90
                if fields[index+1] == 'S':
                    Lattitude = -float(part)   # Just testing
                elif fields[index+1] == 'N':
                    Lattitude = float(part)
                print(f'Lattitude found; {Lattitude}')  # format according to ddmm.mmmm
                # Correct Range 

            elif Long_Match and index < len(fields) - 1: # ADD LATER: is degree between 0 and 180
                # Check if East or West
                if fields[index+1] == 'W':
                    Longtitude = -float(part)   # Just testing
                elif fields[index+1] == 'E':
                    Longtitude = float(part)
                print(f'Longtitude found; {Longtitude}') # format according to dddmm.mmmm




        #if(fields[index + 1] == "N") :  # is the next field latitude?
        #    latitude = float(isLatitude(part))
        #elif(fields[index + 1] == "S") :
        #    latitude = float(-isLatitude(part))
        
      

        # check if both latidue and compass exist then we can get latiude
    


    #def UTCtime() :
        
        # detect hhmmss.ss format for time value
        # 
     #   pass

    #def latitude() :
        # detect ddmm.mmmm format for latitude
        # latitude compass direction (N or S)
      #  pass
    #def longitude() :
        # detect dddmm.mmmm format for longitude
        # longitude compass direction (W or E)
    #    pass   

        # decode string
   
        # don't decode
    #    pass