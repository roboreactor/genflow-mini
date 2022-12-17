import pyfirmata 
from roboreactmaster import Create_serial_motor,Create_serial_motor_logic
motor_1 = pyfirmata.ArduinoMega("/dev/ttyUSB0")
Create_serial_motor('STM32F103C8TX',1,[2,3],motor_1)
Create_serial_motor_logic('STM32F103C8TX',1,1,1,0)