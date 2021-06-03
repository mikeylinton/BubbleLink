import os
from inotify_simple import INotify, flags
inotify = INotify()
watch_flags = flags.CLOSE_WRITE
wd = inotify.add_watch('device.json', watch_flags)
while True:
	for event in inotify.read():
		os.system('python -u ../database/sql.py device.json')
        	os.system('python -u ../devices/gpio.py')
