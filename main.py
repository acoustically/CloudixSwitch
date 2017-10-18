import queue
import message
import button1_thread
import button2_thread
import battery_check_thread
import wifi_check_thread
import server_connection_thread
import speach_recognition_thread

message_queue = queue.Queue()

while(1):
'''
message

BUTTON_1_TURN_ON
BUTTON_1_TURN_OFF
BUTTON_2_TURN_ON 
BUTTON_2_TURN_OFF
BATTERY_LOW
BATTERY_HIGH
WIFI_LOW
WIFI_HIGH
''' 
    if(!message.empty):
        msg = message_queue.get()
        if(msg == message.BUTTON_1_TURN_ON):
            turn_on_button_1()
        
        elif(msg == messge.BUTTON_1_TURN_OFF):
            turn_off_button_1()

        elif(msg == message.BUTTON_2_TURN_ON):
            turn_on_button_1()

        elif(msg == message.BUTTON_2_TURN_OFF):
            turn_off_button_1()

        elif(msg == message.BATTERY_LOW):    
            turn_down_battery_led()

        elif(msg == message.BATTERY_HIGH):
            turn_up_battery_led()

        elif(msg == message.WIFI_LOW):    
            turn_down_wifi_led()
        
        elif(msg == message.WIFI_HIGH):    
            turn_up_wifi_led()

        else:

def turn_on_button_1:

def turn_off_button_1:

def turn_on_button_2:

def turn_off_button_2:

def turn_down_battery_led:

def turn_up_battery_led:

def turn_down_wifi_led:

def turn_up_wifi_led:
  










    
