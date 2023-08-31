import RPi.GPIO as GPIO
import Adafruit_ADS1x15
import time

class GpioAdsControl():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.pinBTN1 = 17
        self.pinBTN2 = 27
        self.pinLED = 4

        #---------------- GPIO SETUP ---------------------
        GPIO.setup(self.pinBTN1, GPIO.IN)
        GPIO.setup(self.pinBTN2, GPIO.IN)
        GPIO.setup(self.pinLED, GPIO.OUT)

        # ---------------- GPIO ESTADO INICIAL ---------------------
        GPIO.input(self.pinBTN1)
        GPIO.input(self.pinBTN2)
        GPIO.output(self.pinLED, 0)

    def actionLed(self, stat):
        GPIO.output(self.pinLED, stat)

    def readBtn1(self):
        while True:
            input_value1 = GPIO.input(self.pinBTN1)
            if input_value1 == False:
                print('The button 1 has been pressed...')
                GPIO.output(self.pinLED, 1)
                time.sleep(0.5)
                GPIO.output(self.pinLED, 0)
                return True

    def readBtn2(self):
        while True:
            input_value2 = GPIO.input(self.pinBTN2)
            if input_value2 == False:
                print('The button 2 has been pressed...')
                GPIO.output(self.pinLED, 1)
                time.sleep(0.5)
                GPIO.output(self.pinLED, 0)
                return True






if __name__ == '__main__':
    cGpio = GpioAdsControl()
    #while(True):
        #time.sleep(2)
        #cGpio.actionLed(1)
        #time.sleep(2)
        #cGpio.actionLed(0)
    cGpio.readBtn1()
    cGpio.readBtn2()

