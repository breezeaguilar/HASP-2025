#### HASP 2024 DIGITAL ON OFF CODE ####

#### IMPORTS ####

import RPi.GPIO as GPIO
import os, sys
sys.path.append(os.path.dirname(__file__))

from Utils import *

#### CLASSES ####

class Digital:
    def __init__(self, pinDataValue: int) -> None:
        self.pinData = pinDataValue
        self.__initialized = False

    def Read(self) -> bool:
        if (self.__initialized is False): 
            raise Exception("ERROR: Attempting to read a digital that has not been initialized!")
        res = GPIO.input(self.pinData)
        return res

    def Init(self) -> bool:
        try:
            GPIO.setup(self.pinData, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__initialized = True
            return 0
        except:
            return 1

    def IsInitialized(self) -> bool:
        return self.__initialized