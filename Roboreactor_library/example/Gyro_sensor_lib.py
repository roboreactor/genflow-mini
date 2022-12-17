import threading
from roboreactmaster import Gyroscope_sensor,Create_node_sub 
from itertools import count
def gyro():
   for rt in count(0):    
           Gyroscope_sensor("MPU6050","127.0.0.1",5620) 
def sub_node():
      for rt in count(0):
            global data_out;data_out = Create_node_sub(2,"127.0.0.1",4096,5620)
            print("Gyro_sensor_data ",data_out)
t1 = threading.Thread(target=gyro)
t2 = threading.Thread(target=sub_node)
t1.start() 
t2.start()
