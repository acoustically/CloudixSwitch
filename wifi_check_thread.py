import subprocess
import time
import argparse
import threading
import RPi.GPIO as GPIO

class WiFiCheckThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        parser = argparse.ArgumentParser(description="")
        parser.add_argument(dest="interface", nargs="?", default="wlan0")
        self.args = parser.parse_args()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

    def get_quality(self):
        cmd = subprocess.Popen("iwconfig %s" % self.args.interface, shell=True, stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if 'Signal level' in str(line):
                return int(str(line).split(" ")[14].split("=")[1].split("/")[0])
            elif 'Not-Associated' in str(line):
                return 0
    def run(self):
        while True:
            if self.get_quality() > 90:
                GPIO.output(16, True)
                GPIO.output(19, True)
                GPIO.output(20, True)
                GPIO.output(21, True)
            elif self.get_quality() > 70:
                GPIO.output(16, True)
                GPIO.output(19, True)
                GPIO.output(20, True)
                GPIO.output(21, False)
            elif self.get_quality() > 50:
                GPIO.output(16, True)
                GPIO.output(19, True)
                GPIO.output(20, False)
                GPIO.output(21, False)
            elif self.get_quality() > 30:
                GPIO.output(16, True)
                GPIO.output(19, False)
                GPIO.output(20, False)
                GPIO.output(21, False)
            else:
                GPIO.output(16, False)
                GPIO.output(19, False)
                GPIO.output(20, False)
                GPIO.output(21, False)
            time.sleep(1)
