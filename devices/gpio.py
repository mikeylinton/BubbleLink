# import modules
import RPi.GPIO as GPIO
import time, sys, json
file=sys.argv[1]
with open(file) as json_file :
    parser = json.load(json_file)
ID=str(parser["device"])
state=str(parser["state"])
device = {
    '0' : 00,#HUB
    '1' : 3,#LIGHT
    '2' : 8,#HEATER
    '3' : 10,#COMPUTER
    '4' : 11#AIRCON
}
gpio=device[ID[0]]
GPIO.setwarnings(False)
# setup pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpio, GPIO.OUT)
GPIO.setup(gpio,GPIO.OUT)
if (state=='1'):
    print("ON")
    GPIO.output(gpio,GPIO.HIGH)
else:
    print("OFF")
    GPIO.output(gpio,GPIO.LOW)

print("\n\n")
