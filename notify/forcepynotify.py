import os
os.system('python -u ../database/sql.py device.json')
os.system('python -u ../devices/gpio.py device.json')
