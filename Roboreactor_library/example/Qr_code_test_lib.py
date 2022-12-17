import threading
from itertools import count
from roboreactmaster import Camera_pub_node,Camera_QR_sub_node,Create_node_sub,Create_i2c_Servo,Create_serial_motor
import pyfirmata
hardware = pyfirmata.ArduinoMega("/dev/ttyUSB0")
led1 = hardware.get_pin('d:2:p')
def raw_cam():
      Camera_pub_node(0,65536,9801,'127.0.0.1')
def Qr_code(): 
      Camera_QR_sub_node(0,65536,9801,5020,'127.0.0.1')
def subnode():
   for i in count(0): 
       global data_out;data_out = Create_node_sub(1,"127.0.0.1",4096,5020) # Getting the local message 
       print("Message out",data_out)

       if list(data_out)[0] == "Message":
                  print(data_out.get(list(data_out)[0]).split(" ")[0]) 
                  key = str(data_out.get(list(data_out)[0]).split(" ")[0])
                  angle_data = {"5001":180,"5002":90,"5003":45,"5004":0}
                  angle_value = angle_data.get(key) 
                  Create_i2c_Servo(0,'servoleg',angle_value,0) # I2C servo motor tested working!
                  if key == "5001":
                      #Create_serial_motor("main_node","motor","/dev/ttyUSB0","STM32F103C8TX",1,[2, 3],"motor_1",1,'p',1,0)
                      led1.write(1)
                  else:
                      led1.write(0)  
                      #Create_serial_motor("main_node","motor","/dev/ttyUSB0","STM32F103C8TX",1,[2, 3],"motor_1",1,'p',0,0)           
if __name__=="__main__":
           t1 = threading.Thread(target=raw_cam)
           t2 = threading.Thread(target=Qr_code)
           t3 = threading.Thread(target=subnode)
           t1.start() 
           t2.start() 
           t3.start() 
           #t1.join() 
           #t2.join() 
           #t3.join() 
