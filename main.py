import queue
import message
import battery_check_thread
import wifi_check_thread
from server_connection_thread import ServerConnectionThread
#from speech_recognition_thread import SpeechRecognitionThread
from button_observing_thread import ButtonObservingThread

class Switch:
    """
    message

    BUTTON_1_TURN_ON
    BUTTON_1_TURN_OFF
    BUTTON_2_TURN_ON 
    BUTTON_2_TURN_OFF
    BATTERY_LOW
    BATTERY_HIGH
    WIFI_LOW
    WIFI_HIGH
    """
    def __init__(self):
        self.is_turn_on = [-1, -1]
  
    def start(self):
        message_queue = queue.Queue()
        server_connection_thread = ServerConnectionThread(message_queue)
        #speech_recognition_thread = SpeechRecognitionThread(message_queue)
        button_observing_thread = ButtonObservingThread(message_queue, self.is_turn_on)
        server_connection_thread.start()
        #speech_recognition_thread.start()
        button_observing_thread.start()
        self.process_message(message_queue)

    def process_message(self, message_queue):
        while 1:
            if not message_queue.empty():
                msg = message_queue.get()
                if msg == message.BUTTON_1_TURN_ON:
                    self.turn_on_button_1()
                  
                elif msg == message.BUTTON_1_TURN_OFF:
                    self.turn_off_button_1()

                elif msg == message.BUTTON_2_TURN_ON:
                    self.turn_on_button_2()

                elif msg == message.BUTTON_2_TURN_OFF:
                    self.turn_off_button_2()

                elif msg == message.BATTERY_LOW:    
                    self.turn_down_battery_led()

                elif msg == message.BATTERY_HIGH:
                    self.turn_up_battery_led()

                elif msg == message.WIFI_LOW:    
                    self.turn_down_wifi_led()
                
                elif msg == message.WIFI_HIGH:    
                    self.turn_up_wifi_led()

    def turn_on_button_1(self):
        if self.is_turn_on[0] != 1:
            self.is_turn_on[0] = 1
            print("turn_on_button_1")
       
    def turn_off_button_1(self):
        if self.is_turn_on[0] != 0:
            self.is_turn_on[0] = 0
            print("turn_off_button_1")

    def turn_on_button_2(self):
        if self.is_turn_on[1] != 1:
            self.is_turn_on[1] = 1
            print("turn_on_button_2")

    def turn_off_button_2(self):
        if self.is_turn_on[1] != 0:
            self.is_turn_on[1] = 0
            print("turn_off_button_2")

    def turn_down_battery_led():
        #TODO
        print("turn_down_battery_led")

    def turn_up_battery_led():
        #TODO
        print("turn_up_battery_led")

    def turn_down_wifi_led():
        #TODO
        print("turn_down_wifi_led")

    def turn_up_wifi_led():
        #TODO
        print("turn_up_wifi_led")

switch = Switch()
switch.start()








  
