import RPi.GPIO as GPIO 
from utils import getCurrentTime

class Button:
    def __init__(self, GPIONum):
        self.GPIONum = GPIONum

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Use a pull down resistor (voltage is set when button pressed)
        GPIO.setup(self.GPIONum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def pressed(self):
        return (GPIO.input(self.GPIONum) == 1)

class LEDLight:
    def __init__(self, GPIONum, maxBlinks=None):
        if maxBlinks is None:
            maxBlinks = 4

        self.GPIONum = GPIONum

        self.numBlinks = maxBlinks
        self.maxBlinks = maxBlinks

        self.blinkTime = getCurrentTime()
        self.timeUntilBlink = 300

    def canBlink(self, gameTime):
        if (self.numBlinks < self.maxBlinks):
            timeSinceBlink = gameTime - self.blinkTime

            return (timeSinceBlink >= self.timeUntilBlink)
        else:
            return False

    def startBlinking(self):
        self.numBlinks = 0
    
    def blink(self):
        self.setLightStatus(self.numBlinks % 2 == 0)

        self.numBlinks += 1    

    def setLightStatus(self, isOn):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.GPIONum, GPIO.OUT)

        if (isOn == True):
            GPIO.output(self.GPIONum, GPIO.HIGH)
        else:
            GPIO.output(self.GPIONum, GPIO.LOW)
