import os
import glob
import time
from lcd1602 import LCD1602

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
	
lcd = LCD1602()
try:
    while True:
        c, f = read_temp()
        temp = str(int(c))
        msg = temp + ' degrees C'
        lcd.lcd_string("Temperature is",lcd.LCD_LINE_1)
        lcd.lcd_string(msg, lcd.LCD_LINE_2)
        time.sleep(1)

except KeyboardInterrupt:
    lcd.lcd_string("Closing ...", lcd.LCD_LINE_1)
    lcd.lcd_string("", lcd.LCD_LINE_2)
    time.sleep(3)

finally:
    lcd.lcd_clear()
    
