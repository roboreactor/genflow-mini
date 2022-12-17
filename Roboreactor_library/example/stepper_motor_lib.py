import threading
from itertools import count
from roboreactmaster import Stepper_serial_gcode
def Stepper_motor():
     g_code = ['G0 Z150','Go Z-150']
     for i in g_code: 
         Stepper_serial_gcode(0,"/dev/ttyUSB0",115200,str(i))
         time.sleep(2)
     #Stepper_serial_gcode(0,"/dev/ttyUSB0",115200,'G0 Z-150') # Sending file into the code to running the step 
t1 = threading.Thread(target=Stepper_motor)
t1.start()


