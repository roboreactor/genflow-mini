import threading 
from roboreactmaster import Location_cellular_network,GPRS_communication_system,Create_node_sub # Getting the communication systemfunction 
from itertools import count
import serial 
sim800l = serial.Serial("/dev/ttyUSB2")
def gprs_loc_com():
       #command = 'ATD +6623918771'   # example command of calling with AT command
       Location_cellular_network(sim800l,'127.0.0.1',5642)
def sub_node_gprs():
    for rt in count(0):
            
            global data_out;data_out = Create_node_sub(1,'127.0.0.1',4096,5642)
            print("GPRS_response_loc ",data_out)
         
if __name__ =="__main__":
         t1 = threading.Thread(target=gprs_loc_com)
         t2 = threading.Thread(target=sub_node_gprs)
         t1.start() 
         t2.start() 