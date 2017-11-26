import RPi.GPIO as GPIO
import time
import threading
import message


class ButtonObservingThread(threading.Thread):
    def __init__(self, message_queue, is_turn_on):
        threading.Thread.__init__(self)
        self.message_queue = message_queue
        self.is_turn_on = is_turn_on
    
    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.IN)
        GPIO.setup(4, GPIO.IN)
        try:
            while True:
                if GPIO.input(4) == 0:
                    if self.is_turn_on[0] != 1:
                        self.message_queue.put(message.BUTTON_1_TURN_ON)
                    else:
                        self.message_queue.put(message.BUTTON_1_TURN_OFF)
                if GPIO.input(27) == 0:
                    if self.is_turn_on[1] != 1:
                        self.message_queue.put(message.BUTTON_2_TURN_ON)
                    else:
                        self.message_queue.put(message.BUTTON_2_TURN_OFF)
                time.sleep(0.15)
        except:
            GPIO.cleanup() 

       
