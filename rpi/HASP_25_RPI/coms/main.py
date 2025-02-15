from gps_packet import verifyPacket

def init() :
    data = "$GPGGA,202212.00,3024.7205,N,09110.7264,W,1,06,1.69,00061,M,-025,M,,*51,"
    #data = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"

    #latitude = gpsdecode.latitude()
    #longitude = gpsdecode.longitude()
    verifyPacket(data)

if(__name__ == "__main__") : init()