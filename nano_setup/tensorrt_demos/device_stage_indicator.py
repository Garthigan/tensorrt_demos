import time
import os
import subprocess
import Jetson.GPIO as GPIO


#ip_addresses =["8.8.8.8","52.24.122.165"]
power_pin = 7
wifi_pin = 11
tracksys_pin = 13

"""
LED COlor Definition for the Stage 

R   :   Wifi & Internet (0-Offline / 1-Online)
G   :   Power (0-OFF / 1-ON)
B   :   Tracking Sys (ObjectTracker.py)

"""
# Set up the GPIO channel
GPIO.setmode(GPIO.BOARD)
GPIO.setup(power_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(wifi_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(tracksys_pin, GPIO.OUT, initial=GPIO.LOW)


def power_stage():
    #     Always power up one GPIO pin
    pass

def check_internet_connection():
   try:
      output = subprocess.check_output(["ping", "-c", "1", "ip_address"])
      return True
   except subprocess.CalledProcessError as err:
       return False

def tracking_service_state():
    try:
        # Use systemctl to check the status of the service
        result = subprocess.run(['systemctl', 'is-active', 'senz_obj_track.service'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        # Check the output to determine the status
        if result.returncode == 0 and result.stdout.decode().strip() == 'active':
            return True  # Service is running
        else:
            return False  # Service is not running or an error occurred

    except Exception as e:
        #print(f"An error occurred: {str(e)}")
        return False  # An error occurred while checking the status

while True:
    GPIO.output(power_pin, GPIO.HIGH)
    power_stage()
    check_internet_connection()
    if check_internet_connection():
        GPIO.output(wifi_pin, GPIO.HIGH)
    else:
        GPIO.output(wifi_pin, GPIO.LOW)

    if tracking_service_state():
        GPIO.output(tracksys_pin, GPIO.LOW)
    else:
        GPIO.output(tracksys_pin, GPIO.HIGH)
    time.sleep(60)