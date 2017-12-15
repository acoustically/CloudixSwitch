from threading import Thread
import time
import urllib3
import message
import json

class ServerConnectionThread(Thread):
    def __init__(self, message_queue):
        Thread.__init__(self)
        self.message_queue = message_queue
        self.http = urllib3.PoolManager()
    
    def run(self):
        while 1:
            json_data = json.dumps({"serial":"0000000001", "token":"acoustically"})
            res = self.http.request("POST", "http://13.124.7.228:3000/switchs/buttons.json", body=json_data, headers={"Content-Type":"application/json"})
            res = json.loads(res.data.decode("utf-8"));
            if res[0]["position"] == 1:
                if res[0]["power"] == 1:
                    self.message_queue.put(message.BUTTON_1_TURN_ON)
                elif res[0]["power"] == 0:
                    self.message_queue.put(message.BUTTON_1_TURN_OFF)
                if res[1]["power"] == 1:
                    self.message_queue.put(message.BUTTON_2_TURN_ON)
                elif res[1]["power"] == 0:
                    self.message_queue.put(message.BUTTON_2_TURN_OFF)
            elif res[0]["position"] == 2:
                if res[0]["power"] == 1:
                    self.message_queue.put(message.BUTTON_2_TURN_ON)
                elif res[0]["power"] == 0:
                    self.message_queue.put(message.BUTTON_2_TURN_OFF)
                if res[1]["power"] == 1:
                    self.message_queue.put(message.BUTTON_1_TURN_ON)
                elif res[1]["power"] == 0:
                    self.message_queue.put(message.BUTTON_1_TURN_OFF)
                
            time.sleep(1)
            
