# Dependencies #
``` bash
sudo apt install inotify-tools python-pips mariadb-server
pip install mysql-connector simple_json RPI.GPIO inotify_simple
sudo mysql_secure_installation 
```
# Code #
## sql.py ##
```python
import mysql.connector, json, sys
db = mysql.connector.connect(host="localhost",user="bubble",passwd="bubble")
file=sys.argv[1]
with open(file) as json_file :
    parser = json.load(json_file)
print("\n\n")
print("Connection ID:", db.connection_id)
#Connection established
cursor = db.cursor()
cursor.execute("use bubble")

try:
	#Device not found.
	sql = "INSERT INTO device_state (device_id, state) VALUES (%s, %s)"
	val = (parser["device"], parser["state"])
	cursor.execute(sql, val)
	print("INSERT "+parser["device"]+" "+parser["state"])

except:
	try:
		#Device exists.
		sql = "UPDATE device_state SET state = %s WHERE device_id = %s"
		val = (parser["state"], parser["device"])
		cursor.execute(sql, val)
		print("UPDATED "+parser["device"]+" "+parser["state"])
	except:
		print("ERROR "+parser["device"]+" "+parser["state"])
#Commit changes
db.commit()
cursor.close()
db.close()
```

## toggle.py ##
```python
import RPi.GPIO as GPIO
import sys, time, json

with open(sys.argv[1]) as json_file:
    parser = json.load(json_file)

device = {
    '0' : 00,#HUB
    '1' : 3,#LIGHT
    '2' : 8,#HEATER
    '3' : 10,#COMPUTER
    '4' : 11#AIRCON
}
#Pins will be different; each device will have a unique pin.

ID=parser["device"]
state=parser["state"]

#Could do a database look up to see what device is connected to what pins.
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
gpio=device[ID[0]]
GPIO.setup(gpio,GPIO.OUT)
if (state=='1'):
    print("LED on")
    GPIO.output(gpio,GPIO.HIGH)
else:
    print("LED off")
    GPIO.output(gpio,GPIO.LOW)
```

``` python
import os
from inotify_simple import INotify, flags
os.chdir('notify')
inotify = INotify()
watch_flags = flags.CLOSE_WRITE
wd = inotify.add_watch('device.json', watch_flags)
while True:
	for event in inotify.read():
		os.system('python -u ../database/sql.py device.json')
                os.system('python -u ../devices/toggle.py device.json')
```
