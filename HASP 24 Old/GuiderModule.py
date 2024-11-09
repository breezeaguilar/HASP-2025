import cv2
import math

def calculate_coord(img, display=False, scale=1, blur=1):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    n=scale
    k=blur
    img_gray = cv2.resize(img_gray,(0,0),fx=1/n,fy=1/n)
    img_gray = cv2.blur(img_gray,(k,k))
    ret, img_thresh = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    a_act = 0
    b_act = 0
    w_act = 0
    h_act = 0
    largestarea = 0.0
    i=0
    if(len(contours)>0):
            for c in contours:
                    area = cv2.contourArea(c)
                    
                    a,b,w,h = cv2.boundingRect(c)
                    if(display): print("Run #: ", i,"a: ",a,"b: ",b,"w: ",w,"h: ",h)
                    
                    i+=1
                                    
                    if (area > largestarea):
                            largestarea = area
                            M_1= cv2.moments(c)
                            if M_1["m00"] == 0: M_1["m00", "m01"] = 1
                            x = int(M_1["m10"] / M_1["m00"])
                            y = int(M_1["m01"] / M_1["m00"])
                            a_act = a
                            b_act = b
                            w_act = w
                            h_act = h
                    
                            cv2.rectangle(img_gray,(int(a_act),int(b_act)),(int(a_act+w_act),int(b_act+h_act)),(0,255,0),2)
            if largestarea==0:return None,None,None,None,n,k,i
            
            ex = x - img_gray.shape[1] / 2
            ey = y - img_gray.shape[0] / 2
            
            x*=n
            y*=n
            ex*=n
            ey*=n
            return ex, ey, x, y, n, k, i
    return None,None,None,None,n,k,None

def GetSunPosition(DeltaGMT : float, NumberOfDays : int, LocalTime : float, Longitude : float, Latitude : float) -> tuple:
    # DeltaGMT is in hours
    # LocalTime is in hours
    LocalStandardTimeMeridian = 15 * DeltaGMT   # hours
    B = (360 / 365) * (NumberOfDays - 81)   # degrees
    EquationOfTime = 9.87 * math.sin(2 * math.radians(B)) - 7.53 * math.cos(math.radians(B)) - 1.5 * math.sin(math.radians(B))  # minutes
    TimeCorrection = 4 * (Longitude - LocalStandardTimeMeridian) + EquationOfTime   # minutes
    LocalSolarTime = LocalTime + TimeCorrection / 60    # hours
    HourAngle = 15 * (LocalSolarTime - 12)  # degrees
    Declanation = 23.45 * math.sin((math.radians(360/365)) * (NumberOfDays - 81))   # degrees
    Elevation = math.asin(math.sin(math.radians(Declanation)) * math.sin(math.radians(Latitude)) + math.cos(math.radians(Declanation)) * math.cos(math.radians(Latitude)) * math.cos(math.radians(HourAngle)))  # radians
    Azimuth = math.acos(((math.sin(math.radians(Declanation)) * math.cos(math.radians(Latitude))) - (math.cos(math.radians(Declanation)) * math.sin(math.radians(Latitude)) * math.cos(math.radians(HourAngle)))) / math.cos(math.radians(Elevation)))  # radians
    return math.degrees(Elevation), math.degrees(Azimuth)

def get_check_sum(b: bytearray) -> bytes:
    c = 0
    for byte in b:
        c+=byte
    return c.to_bytes(math.ceil(math.log2(c)/8), "big")[-1:]

def step(max, min, threshold, val):
    if(val>=threshold):
        return min
    else:
        return max    