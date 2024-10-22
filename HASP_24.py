#! /usr/bin/python3

#### IMPORTS ####

from Camera import Camera
from Motor import Motor
from Digital import Digital
from TempSensors import TempSensors
from GuiderModule import *
from Utils import *

import RPi.GPIO as GPIO
import cv2

from binascii import hexlify
from datetime import datetime
from pytz import UTC
from time import time
from threading import Thread
import serial
import os
import subprocess

#### GLOBAL VARIABLES ####

PIN_MOTOR_X_ENA = 24
PIN_MOTOR_X_STEP = 25
PIN_MOTOR_X_DIR = 12
PIN_MOTOR_Y_ENA = 18
PIN_MOTOR_Y_STEP = 6
PIN_MOTOR_Y_DIR = 16
PIN_LIMIT_SWITCH_CW = 19
PIN_LIMIT_SWICTH_UP = 20
PIN_LIMIT_SWICTH_DOWN = 13
PIN_PHOTODIODE_N = 5
PIN_PHOTODIODE_E = 22
PIN_PHOTODIODE_S = 27
PIN_PHOTODIODE_W = 17
PIN_TEMP = 4

MotorStepDelay = 1000
MotorCurrentRun = 31
MotorCurrentHold = 31
MotorMicrosteps = 4
MotorSPIBus = 0
MotorASPIDevice = 1
MotorBSPIDevice = 0
MotorSPISpeed = 2000000
Motor_UP = 1
Motor_DOWN = 0
Motor_CW = 1
Motor_CCW = 0
pixels_to_step_X_guide = 10
pixels_to_step_Y_guide = 25

CameraDLLPath = "/home/hasp2024/Downloads/ASI_Camera_SDK/ASI_linux_mac_SDK_V1.33/lib/armv8/libASICamera2.so"
GuideCameraPath = "/home/hasp2024/HASP_2024_FINAL/GuideImages/"
ScienceCameraPath = "/home/hasp2024/HASP_2024_FINAL/ScienceImages/"

GuideCameraFrequency = 10

GuideCameraExposure = 1000
GuideCameraGain = 300
GuideCameraResX = 3840
GuideCameraResY = 2160
GuideCameraId = 0
ScienceCameraExposure = 1000
ScienceCameraGain = 1
ScienceCaameraResX = 3840
ScienceCameraResY = 2160
ScienceCameraId = 1

azimuth_offset = 65
elevation_offset = -75
science_x_tol = 100
science_y_tol = 100

TempSensorsNum = 8

DeltaGMT = -6 # HOURS

DownlinkPath = "/home/hasp2024/HASP_2024_FINAL/Downlink.txt"

port = '/dev/ttyAMA0'
baudrate = 4800
bytesize = 8
timeout = 1
stopbits = serial.STOPBITS_ONE
parity = "N"

SaveThreadLoopDelay = 3 # SECONDS
InputThreadLoopDelay = 5 # SECONDS
OutputThreadLoopDelay = 10 # SECONDS
MainThreadLoopDelay = 1 # SECONDS
timeout_tracking = 10*60 # SECONDS
timeout_homing = 1*60 # SECONDS

# DO NOT EDIT
program_phase = None
dir_X = None
dir_Y = None
init_move_done = False
homing_X_CW_1_done = False
homing_X_CW_2_done = False
homing_Y_UP_1_done = False
homing_Y_UP_2_done = False
homing_Y_DOWN_1_done = False
homing_Y_DOWN_2_done = False
photodiode_detection_done = False
photodiode_ignore = False
hunt_found = False

motorX = None
motorY = None
guidecamera = None
sciencecamera = None
limitswitches = None
photodiodes = None
tempsensors = None
ser = None

time_timeout_tracking = None
time_timeout_homing = None
time_from_uplink = []
GPS_time_data = [] # [[LOCAL_TIME(days) LOCAL_TIME(hours) LONGTITTUDE(degrees) LATITUDE(degrees)],...]
uplink_data = []
downlink_data = []
science_images = []
guide_images = []
main_watch = []
science_num_saved = 0
guide_num_saved = 0
azimuth_error = None
elevation_error = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#### FUNCTIONS ####

def print_msg(msg) -> None:
    global program_phase
    print(f"PHASE: {program_phase} - {str(msg)}")

def save_images():
    global science_images
    global guide_images
    global science_num_saved
    global guide_num_saved

    num_science_dirs = len(os.listdir(ScienceCameraPath))
    ScienceCameraPathSpecific = f"{ScienceCameraPath}Science_{str(num_science_dirs)}/"
    while os.path.exists(ScienceCameraPathSpecific):
        num_science_dirs += 1
        ScienceCameraPathSpecific = f"{ScienceCameraPath}Science_{str(num_science_dirs)}/"
    os.makedirs(ScienceCameraPathSpecific)

    num_guide_dirs = len(os.listdir(GuideCameraPath))
    GuideCameraPathSpecific = f"{GuideCameraPath}Guide_{str(num_guide_dirs)}/"
    while os.path.exists(GuideCameraPathSpecific):
        num_guide_dirs += 1
        GuideCameraPathSpecific = f"{GuideCameraPath}{str(num_guide_dirs)}/"
    os.makedirs(GuideCameraPathSpecific)
    print_msg("DIRS MADE")


    while True:
        science_imgs_size = len(science_images)
        if(science_imgs_size > 0):
            science_filename = f"{ScienceCameraPathSpecific}{time()}_{science_num_saved}_ScienceSun.png"
            while os.path.exists(science_filename):
                science_num_saved += 1
                science_filename = f"{ScienceCameraPathSpecific}{time()}_{science_num_saved}_ScienceSun.png"
            cv2.imwrite(science_filename,science_images[science_imgs_size-1]) # SAVE SCIENCE IMAGE TO LOCATION PROVIDED
            del(science_images[:science_imgs_size])
            science_num_saved += 1

        guide_imgs_size = len(guide_images)
        if(guide_imgs_size>GuideCameraFrequency - 1):
            guide_filename = f"{GuideCameraPathSpecific}{time()}_{guide_num_saved}_GuideSun.jpg"
            while os.path.exists(guide_filename):
                guide_num_saved += 1
                guide_filename = f"{GuideCameraPathSpecific}{time()}_{guide_num_saved}_GuideSun.jpg"
            cv2.imwrite(guide_filename,guide_images[guide_imgs_size-1]) # SAVE GUIDE IMAGE TO LOCATION PROVIDED
            del(guide_images[:guide_imgs_size])
            guide_num_saved += 1
        
        DelaySeconds(SaveThreadLoopDelay)

def input():
    global program_phase
    global dir_X
    global dir_Y
    global init_move_done
    global homing_X_CW_1_done
    global homing_X_CW_2_done
    global homing_Y_UP_1_done
    global homing_Y_UP_2_done
    global homing_Y_DOWN_1_done
    global homing_Y_DOWN_2_done
    global photodiode_detection_done
    global photodiode_ignore

    global time_timeout_homing
    global time_timeout_tracking
    global time_from_uplink
    global GPS_time_data
    global uplink_data
    global azimuth_error
    global elevation_error

    while True:
        if (ser.in_waiting > 0):
            bytesread = ser.read(ser.in_waiting)
            print_msg("SERIAL DATA RECIEVED")
            bytesread_size = len(bytesread)
            match bytesread_size:
                case 125:
                    if((bytesread[0] == 0x01) and 
                       (bytesread[1] == 0x30) and 
                       (bytesread[122] == 0x03) and 
                       (bytesread[123] == 0x0D) and 
                       (bytesread[124] == 0x0A)):
                        elements = bytesread[2:].decode().split(",")
                        if((len(elements)>1) and (elements[1]=="$GPGGA")):
                            try:
                                time_from_uplink.append(elements[0])
                                UTC_time = datetime.fromtimestamp(float(elements[0]),UTC)
                                local_hour = (UTC_time.hour + DeltaGMT)%24 + UTC_time.minute/60
                                day_delta = 0
                                if(UTC_time.hour+DeltaGMT < 0):
                                    day_delta = -1
                                elif(UTC_time.hour+DeltaGMT > 24):
                                    day_delta = 1
                                local_day = (UTC_time.day + day_delta) % 365
                                longtitude = float(elements[5][:3]) + float(elements[5][3:])/60
                                if(elements[6] == "W"):
                                    longtitude = -longtitude
                                latitude = float(elements[3][:2]) + float(elements[3][2:])/60
                                if(elements[4] == "S"):
                                    latitude = -latitude
                                GPS_time_data.append([local_day, local_hour, longtitude, latitude])
                                print_msg("GPS DATA PARSED")
                            except:
                                print_msg("ERROR PARSING GPS DATA")
                case 7:
                    if((bytesread[0] == 0x01) and 
                       (bytesread[1] == 0x02) and 
                       (bytesread[4] == 0x03) and
                       (bytesread[5] == 0x0D) and
                       (bytesread[6] == 0x0A) and
                       (bytesread[2]+bytesread[3] == 256)):
                        print_msg("COMMAND RECIEVED")
                        uplink_data.append(bytesread[2:4])
                        match bytesread[2]:
                            case 0x90:
                                program_phase = "HOMING"
                                dir_X = Motor_CW
                                dir_Y = Motor_UP
                                init_move_done = False
                                homing_X_CW_1_done = False
                                homing_X_CW_2_done = False
                                homing_Y_UP_1_done = False
                                homing_Y_UP_2_done = False
                                homing_Y_DOWN_1_done = False
                                homing_Y_DOWN_2_done = False
                                photodiode_detection_done = False
                                time_timeout_tracking = None
                                time_timeout_homing = None
                                azimuth_error = None
                                elevation_error = None
                                print_msg("INIT")
                            case 0x91:
                                photodiode_ignore = not photodiode_ignore
                                print_msg("PHOTO SWITCH")
                            case 0x92:
                                motorX.Run(int(1458.5*MotorMicrosteps), 1, 1000)
                                print_msg("TURN 180")
                            case 0x9F:
                                print_msg("EXITED")
                                subprocess.run(["sudo", "shutdown", "-h", "now"])
                            case _:
                                pass
                case _:
                    pass
        else:
            DelaySeconds(InputThreadLoopDelay)

def output():
    global downlink_data
    global time_from_uplink
    global main_watch

    with open(DownlinkPath, "a") as downlink_file:
        downlink_file.write("NEW RUN\n\n")
    downlink_file.close()

    while True:
        downlink_data_size = len(downlink_data)
        if(downlink_data_size > 0):
            downlink_data_write = downlink_data[downlink_data_size-1]
            del(downlink_data[:downlink_data_size])
            ser.write(downlink_data_write)
            print_msg("SERIAL DATA SENT")
        else:
            downlink_data_save = bytearray()
            downlink_dict = {}
            time_from_uplink_size = len(time_from_uplink)
            if(time_from_uplink_size > 0):
                downlink_dict["time"] = int(float(time_from_uplink[time_from_uplink_size-1])).to_bytes(4,"big") # TIMESTAMP
                if(time_from_uplink_size>1):
                    del(time_from_uplink[:time_from_uplink_size-1])
            else:
                downlink_dict["time"] = (b"\xff"*4)
            try:
                temps = tempsensors.Read()
                for i in range(TempSensorsNum): # DONT KNOW THE NUMBER OF DIGITS IN TEMP, MIGHT NEED TO CHANGE
                    downlink_dict[f"temp_sensor_{i}"] = (int(temps[i]+273.15)*10).to_bytes(2,"big")
                downlink_dict["guide_temp"] = int(guidecamera.get_temp()[0]+2731.5).to_bytes(2,"big") # GUIDECAMERA TEMP
                downlink_dict["science_temp"] = int(sciencecamera.get_temp()[0]+2731.5).to_bytes(2,"big") # SCIENCECAMERA TEMP
                downlink_dict["motor_X_temp"] = (int(motorX.GetTemp()+273.15)*10).to_bytes(2,"big")
                downlink_dict["motor_Y_temp"] = (int(motorY.GetTemp()+273.15)*10).to_bytes(2,"big") # AMBIENT TEMP, FIX
            except:
                for i in range(TempSensorsNum):
                    downlink_dict[f"temp_sensor_{i}"] = b"\xff"
                downlink_dict["guide_temp"] = b"\xff"b"\xff"
                downlink_dict["science_temp"] = b"\xff"b"\xff"
                downlink_dict["motor_X_temp"] = b"\xff"b"\xff"
                downlink_dict["motor_Y_temp"] = b"\xff"b"\xff"
            if(science_num_saved < 65535): # IMAGES SAVED
                downlink_dict["science_num_saved"] = science_num_saved.to_bytes(2,"big")
            else:
                downlink_dict["science_num_saved"] = b'\xff'b'\xff'
            mode = b'\x00'
            match program_phase:
                case "HOMING":
                    mode = b'\x01'
                case "ELEVATE":
                    mode = b'\x02'
                case "PHOTODIODE_PAN":
                    mode = b'\x03'
                case "HUNT":
                    mode = b'\x04'
                case "SCIENCE":
                    mode = b'\x05'
            downlink_dict["system_mode"] = mode # SYSTEM MODE
            uplink_data_size = len(uplink_data)
            if(uplink_data_size>0): # LAST COMMAND RECIEVED
                downlink_dict["last_uplink_recieved"] = uplink_data[uplink_data_size-1]
            else:
                downlink_dict["last_uplink_recieved"] = b'\xff'b'\xff'
            heartbeat_register = ""
            heartbeat_register += str(int(homing_X_CW_1_done))
            heartbeat_register += str(int(homing_X_CW_2_done)) 
            heartbeat_register += str(int(homing_Y_UP_1_done))
            heartbeat_register += str(int(homing_Y_UP_2_done))
            heartbeat_register += str(int(homing_Y_DOWN_1_done))
            heartbeat_register += str(int(homing_Y_DOWN_2_done))
            heartbeat_register += str(int(photodiode_detection_done))
            heartbeat_register += str(int(photodiode_ignore))
            heartbeat_register += str(int(hunt_found))
            size_main_watch = len(main_watch)
            if(size_main_watch>0):
                heartbeat_register += str(int(main_watch[size_main_watch-1][0]))
                heartbeat_register += str(int(main_watch[size_main_watch-1][1]))
                heartbeat_register += str(int(main_watch[size_main_watch-1][2]))
                del(main_watch[:size_main_watch])
                heartbeat_register += "1"
            else:
                heartbeat_register += "0000"
            heartbeat_register = int(heartbeat_register,2)
            downlink_dict["heartbeat_register"] = heartbeat_register.to_bytes(2, 'big') # HEARTBEAT
            if(azimuth_error != None): # AZIMUTH ERROR
                downlink_dict["azimuth_err"] = int(abs(azimuth_error)).to_bytes(2, 'big')
            else:
                downlink_dict["azimuth_err"] = b'\xff'b'\xff'
            if(elevation_error != None): # ELEVATION ERROR
                downlink_dict["elevation_err"] = int(abs(elevation_error)).to_bytes(2, 'big')
            else:
                downlink_dict["elevation_err"] = b'\xff'b'\xff'
            photodiode_register = ""
            for photodiode in photodiodes:
                photodiode_register += str(photodiode.Read())
            photodiode_register = int(photodiode_register,2)
            downlink_dict["photodiode_register"] = photodiode_register.to_bytes(1,"big") # PHOTOREGISTER ERROR, FIX
            
            downlink_data_save.extend(b'\x01') # STARTING BYTE
            downlink_data_save.extend(downlink_dict["time"])
            for i in range(TempSensorsNum):
                downlink_data_save.extend(downlink_dict[f"temp_sensor_{i}"])
            downlink_data_save.extend(downlink_dict["guide_temp"])
            downlink_data_save.extend(downlink_dict["science_temp"])
            downlink_data_save.extend(downlink_dict["motor_X_temp"])
            downlink_data_save.extend(downlink_dict["motor_Y_temp"])
            downlink_data_save.extend(downlink_dict["science_num_saved"])
            downlink_data_save.extend(downlink_dict["system_mode"])
            downlink_data_save.extend(downlink_dict["last_uplink_recieved"])
            downlink_data_save.extend(downlink_dict["heartbeat_register"])
            downlink_data_save.extend(downlink_dict["azimuth_err"])
            downlink_data_save.extend(downlink_dict["elevation_err"])
            downlink_data_save.extend(downlink_dict["photodiode_register"])
            downlink_data_save.extend(get_check_sum(downlink_data_save[1:]))
            downlink_data_save.extend(b'\xfe')
            print_msg("DOWNLINK MADE")

            downlink_data.append(downlink_data_save) # TO SAVE DOWNLINK DATA TO A 'QUEUE' 

            # SAVE DOWNLINK DATA TO A TEXT FILE
            with open(DownlinkPath, "a") as downlink_file:
                downlink_file.write(str(hexlify(downlink_data_save))+"\n\n")
            downlink_file.close()
            
            DelaySeconds(OutputThreadLoopDelay)

def callback_CW(channel):
    global program_phase
    global homing_X_CW_1_done
    global photodiode_detection_done
    match program_phase:
        case "HOMING":
            if(not homing_X_CW_1_done):
                motorX.Interrupt()
                homing_X_CW_1_done = True
        case "PHOTODIODE_PAN":
            motorX.Interrupt()
            photodiode_detection_done = True
        case "HUNT":
            if(not hunt_found):
                motorY.Run(20*MotorMicrosteps, dir_Y, 1000)
        case _:
            pass

def callback_UP(channel):
    global program_phase
    global homing_Y_UP_1_done
    global dir_Y
    if(init_move_done):
        motorY.Interrupt()
    match program_phase:
        case "HOMING":
            if(not homing_Y_UP_1_done):
                homing_Y_UP_1_done = True
        case "ELEVATE":
            program_phase = "PHOTODIODE_PAN"
        case "HUNT":
            dir_Y = Motor_DOWN
        case _:
            pass

def callback_DOWN(channel):
    global program_phase
    global homing_Y_DOWN_1_done
    global dir_Y
    if(homing_Y_UP_2_done):
        motorY.Interrupt()
        match program_phase:
            case "HOMING":
                if(not homing_Y_DOWN_1_done):
                    homing_Y_DOWN_1_done = True
            case "HUNT":
                dir_Y = Motor_UP
            case _:
                pass

def main_thread():
    global program_phase
    global dir_X
    global dir_Y
    global init_move_done
    global homing_X_CW_1_done
    global homing_X_CW_2_done
    global homing_Y_UP_1_done
    global homing_Y_UP_2_done
    global homing_Y_DOWN_1_done
    global homing_Y_DOWN_2_done
    global photodiode_detection_done
    global photodiode_ignore
    global hunt_found

    global motorX
    global motorY
    global guidecamera
    global sciencecamera
    global limitswitches
    global photodiodes
    global tempsensors
    global ser

    global time_timeout_tracking
    global time_timeout_homing
    global GPS_time_data
    global science_images
    global guide_images
    global azimuth_error
    global elevation_error
    global main_watch

    motorX = Motor(PIN_MOTOR_X_ENA,
                    PIN_MOTOR_X_STEP,
                    PIN_MOTOR_X_DIR,
                    MotorSPIBus, 
                    MotorASPIDevice, 
                    MotorSPISpeed, 
                    MotorCurrentRun, 
                    MotorCurrentHold, 
                    MotorMicrosteps)
    motorY = Motor(PIN_MOTOR_Y_ENA, 
                   PIN_MOTOR_Y_STEP, 
                   PIN_MOTOR_Y_DIR, 
                   MotorSPIBus, 
                   MotorBSPIDevice, 
                   MotorSPISpeed, 
                   MotorCurrentRun, 
                   MotorCurrentHold, 
                   MotorMicrosteps)

    guidecamera = Camera(GuideCameraGain, 
                         GuideCameraExposure, 
                         GuideCameraResX,
                         GuideCameraResY,
                         GuideCameraId)
    sciencecamera = Camera(ScienceCameraGain, 
                           ScienceCameraExposure, 
                           ScienceCaameraResX,
                           ScienceCameraResY,
                           ScienceCameraId)

    limitswitches = [Digital(PIN_LIMIT_SWITCH_CW),
                     Digital(PIN_LIMIT_SWICTH_UP),
                     Digital(PIN_LIMIT_SWICTH_DOWN)]
    
    photodiodes = [Digital(PIN_PHOTODIODE_N),
                   Digital(PIN_PHOTODIODE_E),
                   Digital(PIN_PHOTODIODE_S),
                   Digital(PIN_PHOTODIODE_W)]

    tempsensors = TempSensors(PIN_TEMP,TempSensorsNum)

    while (motorX.Init() != 0):
        print_msg("Failed to initialize motor X! Retrying...")
        DelaySeconds(1)
    while (motorY.Init() != 0):
        print_msg("Failed to initialize motor Y! Retrying...")
        DelaySeconds(1)
    print_msg("Successfully initialized motors!")
    while(guidecamera.Init(CameraDLLPath) != 0):
        print_msg("Failed to initialize guide camera! Retrying...")
        DelaySeconds(1)
    while(sciencecamera.Init(CameraDLLPath) != 0):
        print_msg("Failed to initialize science camera! Retrying...")
        DelaySeconds(1)
    print_msg("Successfully initialized cameras")
    for limitswitch in limitswitches:
        while (limitswitch.Init() != 0):
            print_msg("Failed to initialize limit switch! Retrying...")
            DelaySeconds(1)
    print_msg("Successfully initialized limit switches")
    for photodiode in photodiodes:
        while (photodiode.Init() != 0):
            print_msg("Failed to initialize photo diode! Retrying...")
            DelaySeconds(1)
    print_msg("Successfully initialized photodiodes")
    while(tempsensors.Init() != 0):
        print_msg("Failed to initialize temp sensors! Retrying...")
        DelaySeconds(1)
    print_msg("Successsfully initialized temp sensors")
    ser = serial.Serial(port = port, baudrate = baudrate, bytesize = bytesize, stopbits = stopbits, parity = parity)
    print_msg("Successfully initialized serial port")

    save_images_thread = Thread(target = save_images, args = ())
    input_thread = Thread(target = input, args = ())
    output_thread = Thread(target = output, args = ())

    save_images_thread.start()
    input_thread.start()
    output_thread.start()

    GPIO.add_event_detect(PIN_LIMIT_SWITCH_CW, GPIO.FALLING, callback = callback_CW)
    GPIO.add_event_detect(PIN_LIMIT_SWICTH_UP, GPIO.FALLING, callback = callback_UP)
    GPIO.add_event_detect(PIN_LIMIT_SWICTH_DOWN, GPIO.FALLING, callback = callback_DOWN)

    program_phase = "HOMING" # globals
    dir_X = Motor_CW # globals
    dir_Y = Motor_UP # globals
    
    while (True):
        match program_phase:
            case "HOMING":
                if(limitswitches[0].Read()==0):
                    motorX.Run(40*MotorMicrosteps, Motor_CCW, 5000)
                if(limitswitches[1].Read()==0):
                    motorY.Run(10*MotorMicrosteps, Motor_DOWN, 5000)
                if(limitswitches[2].Read()==0):
                    motorY.Run(10*MotorMicrosteps, Motor_UP, 5000)

                motorY.Run(20*MotorMicrosteps, Motor_DOWN, 5000)
                init_move_done = True
                print_msg("INIT MOVE DONE")

                while not homing_X_CW_1_done:
                    if(time_timeout_homing == None):
                        time_timeout_homing = time()
                    elif(time()-time_timeout_homing > timeout_homing):
                        break
                    motorX.Run(20*MotorMicrosteps, Motor_CW, 2000)
                time_timeout_homing = None
                motorX.Run(10*MotorMicrosteps, Motor_CCW, 5000)
                motorX.Run(10*MotorMicrosteps+1, Motor_CW, 10000)
                homing_X_CW_2_done = True
                print_msg("X HOMING DONE")

                while not homing_Y_UP_1_done: # LOOPS STOPS EXECUTING WHEN CALLBACK IS CALLED BY LIMIT SWITCH
                    if(time_timeout_homing == None):
                        time_timeout_homing = time()
                    elif(time()-time_timeout_homing > timeout_homing):
                        break
                    motorY.Run(20*MotorMicrosteps, Motor_UP, 2000)
                time_timeout_homing = None
                motorY.Run(5*MotorMicrosteps, Motor_DOWN, 5000)
                motorY.Run(5*MotorMicrosteps+1, Motor_UP, 10000)
                homing_Y_UP_2_done = True
                print_msg("Y UP HOMING DONE")
                
                while not homing_Y_DOWN_1_done: # LOOPS STOPS EXECUTING WHEN CALLBACK IS CALLED BY LIMIT SWITCH
                    if(time_timeout_homing == None):
                        time_timeout_homing = time()
                    elif(time()-time_timeout_homing > timeout_homing):
                        break
                    motorY.Run(20*MotorMicrosteps, Motor_DOWN, 2000)
                time_timeout_homing = None
                motorY.Run(5*MotorMicrosteps, Motor_UP, 5000)                         
                motorY.Run(5*MotorMicrosteps+1, Motor_DOWN, 10000)
                homing_Y_DOWN_2_done = True
                print_msg("Y DOWN HOMING DONE")
                
                program_phase = "ELEVATE"
            case "ELEVATE":
                elevate_data = []

                for i in range(3): # NUMBER OF TIMES ONE WANTS TO CHECK
                    DelaySeconds(10) # TIME TO WAIT BEFORE CHECKING AGAIN IN SECONDS
                    GPS_time_data_size = len(GPS_time_data)
                    if(GPS_time_data_size>0):
                        elevate_data = GPS_time_data[GPS_time_data_size-1]
                        print_msg("MAIN THREAD GOT GPS DATA")
                        del(GPS_time_data[:GPS_time_data_size])
                        break

                    if(program_phase=="HOMING"):
                        break
                
                if(len(elevate_data) > 0):
                    altitude, _ = GetSunPosition(DeltaGMT, elevate_data[0], elevate_data[1], elevate_data[2], elevate_data[3]) # FIX
                    if(altitude > 0 and altitude < 55):
                        steps_altitude = int(altitude*600*MotorMicrosteps/360)
                        motorY.Run(steps_altitude, Motor_UP, 10000)
                        print_msg("ELEVATED")
                    elif(altitude >= 55):
                        motorY.Run(int(55*600*MotorMicrosteps/360), Motor_UP, 10000)
                        print_msg("ELEVATED AT MAX")
                if(program_phase=="ELEVATE"):
                    program_phase = "PHOTODIODE_PAN"
                else:
                    program_phase = "HOMING"
            case "PHOTODIODE_PAN":
                while not (photodiode_detection_done or photodiode_ignore):
                    if(photodiodes[0].Read()==0 or (photodiodes[1].Read()==0 and photodiodes[3].Read()==0)):
                        photodiode_detection_done = True
                        break
                    motorX.Run(50*MotorMicrosteps, Motor_CW, 1000)
                    DelaySeconds(1) # TIME TO WAIT BEFORE CHECKING AGAIN IN SECONDS

                    if(program_phase=="HOMING"):
                        break
                
                if(program_phase=="PHOTODIODE_PAN"):
                    program_phase = "HUNT"
                else:
                    program_phase = "HOMING"
            case "HUNT":
                if(limitswitches[1].Read()==0):
                    motorY.Run(10*MotorMicrosteps, Motor_DOWN, 5000)
                if(limitswitches[2].Read()==0):
                    motorY.Run(10*MotorMicrosteps, Motor_UP, 5000)
                try:
                    guide_img, guide_stat = guidecamera.get_image()
                    if(guide_stat!=0):
                        continue
                    guide_img_error_properties = calculate_coord(guide_img)
                except:
                    continue
                '''small_g = cv2.resize(guide_img, (0,0), fx=0.33, fy=0.33)
                cv2.imshow('guide', small_g)
                cv2.waitKey(1000)'''

                if(guide_img_error_properties[0]!=None):
                    hunt_found = True
                    azimuth_error = guide_img_error_properties[0] + azimuth_offset
                    elevation_error = guide_img_error_properties[1] + elevation_offset

                    within_x_tol_guide = abs(azimuth_error) < pixels_to_step_X_guide/MotorMicrosteps
                    within_y_tol_guide = abs(elevation_error) < pixels_to_step_Y_guide/MotorMicrosteps
                    print_msg(f"guide: {within_x_tol_guide, within_y_tol_guide}")
                    
                    if(not within_x_tol_guide):
                        if(abs(azimuth_error)/azimuth_error>0):
                            dir_X = Motor_CW
                        else:
                            dir_X = Motor_CCW  
                        steps_X = int(abs(azimuth_error)*MotorMicrosteps/pixels_to_step_X_guide)
                        delay_X = step(10000, 1000, 15, abs(azimuth_error))
                        motorX.Run(steps_X, dir_X, delay_X)

                    if(not within_y_tol_guide):
                        if(abs(elevation_error)/elevation_error>0):
                            dir_Y = Motor_DOWN
                        else:
                            dir_Y = Motor_UP
                        steps_Y = int(abs(elevation_error)*MotorMicrosteps/pixels_to_step_Y_guide)
                        delay_Y = step(10000, 1000, 15, abs(elevation_error))
                        motorY.Run(steps_Y, dir_Y, delay_Y)

                    if(within_x_tol_guide and within_y_tol_guide):
                        azimuth_error = None
                        elevation_error = None
                        try:
                            science_img, science_stat = sciencecamera.get_image()
                        except:
                            continue
                        if(science_stat!=0):
                            continue
                        '''small_s = cv2.resize(science_img, (0,0), fx=0.33, fy=0.33)
                        cv2.imshow('science', small_s)
                        cv2.waitKey(1000)'''
                        science_images.append(science_img) # SAVE SCIENCE IMAGE TO A QUEUE
                        if(program_phase=="HOMING"):
                            continue
                        program_phase = "SCIENCE"

                    if(time_timeout_tracking == None):
                        time_timeout_tracking = time()
                    elif(time()-time_timeout_tracking>timeout_tracking):
                        time_timeout_tracking = None
                        motorX.Run(243*MotorMicrosteps, Motor_CW, 1000)

                    guide_images.append(guide_img) # SAVE GUIDE IMAGE TO A QUEUE
                else:
                    time_timeout_tracking = None
                    hunt_found = False
                    motorX.Run(100*MotorMicrosteps, dir_X, 1000)
            case "SCIENCE":
                try:
                    science_img, science_stat = sciencecamera.get_image()
                    if(science_stat!=0):
                        continue
                    science_img_brightened = cv2.convertScaleAbs(science_img, 1, 10)
                    science_img_error_properties = calculate_coord(science_img_brightened)
                except:
                    continue
                '''small_s = cv2.resize(science_img, (0,0), fx=0.33, fy=0.33)
                cv2.imshow('science', small_s)
                cv2.waitKey(1000)'''

                if(science_img_error_properties[0]!=None):
                    science_images.append(science_img)

                    science_azimuth_error = science_img_error_properties[0]
                    science_elevation_error = science_img_error_properties[1]

                    within_x_tol_science = abs(science_azimuth_error) < science_x_tol
                    within_y_tol_science = abs(science_elevation_error) < science_y_tol
                    print_msg(f"science: {within_x_tol_science, within_y_tol_science}")

                    if(not within_x_tol_science):
                        if(abs(science_azimuth_error)/science_azimuth_error>0):
                            dir_X = Motor_CCW
                        else:
                            dir_X = Motor_CW
                        motorX.Run(5, dir_X, 10000)
                    
                    if(not within_y_tol_science):
                        if(abs(science_elevation_error)/science_elevation_error>0):
                            dir_Y = Motor_UP
                        else:
                            dir_Y = Motor_DOWN
                        motorY.Run(1, dir_Y, 10000)
                    
                    if(time_timeout_tracking == None):
                        time_timeout_tracking = time()
                    elif(time()-time_timeout_tracking>timeout_tracking):
                        time_timeout_tracking = None
                        motorX.Run(243*MotorMicrosteps, Motor_CW, 1000)
                else:
                    time_timeout_tracking = None
                    program_phase = "PHOTODIODE_PAN"                
            case _:
                pass
        print_msg(program_phase)
        main_watch.append([save_images_thread.is_alive(), input_thread.is_alive(), output_thread.is_alive()])
        DelaySeconds(MainThreadLoopDelay)

if __name__ == "__main__":
    main_thread()