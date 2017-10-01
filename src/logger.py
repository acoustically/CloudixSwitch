from datetime import datetime

class Logger:
    def __init__(self):
        self.f = open("../log/system_log.txt", "a")
    
    def log(self, string):
        log = self.__get_time() + "\t" + string + "\n"
        print(log)
        self.f.write(log)

    def __get_time(self):
        return datetime.now().strftime("%y-%m-%d/%H:%M:%s")
