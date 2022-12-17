import pyfirmata 
from roboreactmaster import Create_serial_Servo,Create_Servo_motor 

servo_1 = pyfirmata.ArduinoMega("/dev/ttyUSB0")
Create_serial_Servo(0,servo_1,"STM32F103C8TX",2)
Create_Servo_motor("STM32F103C8TX",0,90)