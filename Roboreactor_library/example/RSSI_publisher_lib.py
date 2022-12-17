from re import sub
from roboreactmaster import Create_node_sub,rssi_indoor
import threading
import subprocess 
from itertools import count
def Indoor_position():
    for i in count(0):
       rssi_indoor('127.0.0.1',5690)

def sub_rssi_node():
    
      for r in count(0):
         global data_out;data_out =  Create_node_sub(1,"127.0.0.1",4096,5690)  
         print("RSSI distance ",data_out," m")

def RSSI_realtime_raw(): 
     for t in count(0): 
          bssid_list = subprocess.check_output("iwlist scanning",shell=True)
          data_raw_decode = bssid_list.decode() # decode the raw data 
          #Finding the Signal strange from the list index
          for i in data_raw_decode.split(":"): 
               try:
           
                 if len(i.split("=")) == 3:
                     print(i.split("=")[2].split("\n")[0]) 
                     return i.split("=")[2].split("\n")[0].split(" ")[0]
          
               except: 
                    pass
t1 = threading.Thread(target=Indoor_position)
t2 = threading.Thread(target=sub_rssi_node)
t3 = threading.Thread(target=RSSI_realtime_raw)
t1.start() 
t2.start() 
t3.start()
