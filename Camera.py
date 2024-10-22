#### HASP 2024 CAMERA CODE ####

#### IMPORTS ####

import zwoasi
import cv2
import numpy

import os, sys
sys.path.append(os.path.dirname(__file__))

#### CLASSES ####

class Camera:
    def __init__(self, gain: int, exposure: int, resx: int, resy: int, camera_id: int):
        self.gain = gain
        self.exposure = exposure
        self.resx = resx
        self.resy = resy
        self.camera_id = camera_id
        self.__initialized = False
        self.camera = None
    
    def get_image(self) -> tuple:
        if(not self.__initialized):
            return 0,1
        self.camera.set_image_type(zwoasi.ASI_IMG_RAW8)
        self.camera.start_exposure()
        camera_status = self.camera.get_exposure_status()
        while camera_status == 1:
            camera_status = self.camera.get_exposure_status()
        if camera_status == 2:
            img_array = self.camera.get_data_after_exposure()
            from PIL import Image
            img_camera = Image.frombuffer("L", (self.resx, self.resy), img_array)
            ocv_image = cv2.cvtColor(numpy.array(img_camera), cv2.COLOR_RGB2BGR)
            return ocv_image, 0
        elif  camera_status == 3:
            return 0, 2
        else:
            return 0, 3
    
    def Init(self, dll_path : str) -> int:
        try:
            zwoasi.init(dll_path)
        except:
            return 1
        if(zwoasi.get_num_cameras()==0):
            return 2
        self.camera = zwoasi.Camera(self.camera_id)
        self.camera.set_control_value(zwoasi.ASI_GAIN, self.gain)
        self.camera.set_control_value(zwoasi.ASI_EXPOSURE, self.exposure)
        self.__initialized = True
        return 0

    def get_temp(self):
        if(not self.__initialized):
            raise Exception("ERROR: Attempting to use a camera that has not been initialized!")
        return self.camera.get_control_value(zwoasi.ASI_TEMPERATURE)

    def close_camera(self) -> int:
        if(not self.__initialized):
            raise Exception("ERROR: Attempting to use a camera that has not been initialized!")
            
        self.camera.close()
        return 0
        
    def IsInitialized(self) -> bool:
        return self.__initialized