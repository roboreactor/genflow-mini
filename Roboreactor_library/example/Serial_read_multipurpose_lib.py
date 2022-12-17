import serial 
import threading
from itertools import count 
from roboreactmaster import Serial_write_multipurpose,Serial_read_multipurpose,Create_node_sub
board_1 = serial.Serial('/dev/ttyUSB1',115200)

def Serial_read_pub():
    for tr in count(0): 
       Serial_read_multipurpose(1,board_1,True,'utf-8','127.0.0.1',5740)

def Serial_read_sub(): 
    for rt in count(0):
              global data_serial;data_serial = Create_node_sub(1,"127.0.0.1",4096,5740)
              print(data_serial)

t1 = threading.Thread(target=Serial_read_pub)
t2 = threading.Thread(target=Serial_read_sub)
t1.start() 
t2.start() 