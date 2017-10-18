import queue
import message
import button1_thread
import button2_thread
import battery_check_thread
import wifi_check_thread
from server_connection_thread import ServerConnectionThread
import speach_recognition_thread

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
        self.button1_power = -1
        self.button2_power = -1
  
    def start(self):
        message_queue = queue.Queue()
        server_connection_thread = ServerConnectionThread(message_queue)
        server_connection_thread.start()
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
        if self.button1_power != 1:
            self.button1_power = 1
            print("turn_on_button_1")
       
    def turn_off_button_1(self):
        if self.button1_power != 0:
            self.button1_power = 0
            print("turn_off_button_1")

    def turn_on_button_2(self):
        if self.button2_power != 1:
            self.button2_power = 1
            print("turn_on_button_2")

    def turn_off_button_2(self):
        if self.button2_power != 0:
            self.button2_power = 0
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








  
