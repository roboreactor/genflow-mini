from itertools import count 
import threading
import time 
from roboreactmaster import Camera_multi_cache,Camera_Qr_cache,Cache_server,Face_cache,Create_node_sub
def Camera_multi():
      Camera_multi_cache(0,'127.0.1.6',9999,340) # Cache server camera 
def Camera_cache_server():
      Cache_server('127.0.1.6','127.0.1.13',9999)
def Face_recog_cache_0(): 
      #time.sleep(2) 
      Face_cache(0,'Face_db',1,'127.0.1.13',9999,'127.0.0.1',5081)
def Qr_code_scanner_0(): 
      time.sleep(2) 
      Camera_Qr_cache(1,1,'127.0.1.13',9999,'127.0.0.1',5081)
def Qr_cache_sub_node():
    for i in count(0): 
       global data_out;data_out = Create_node_sub(0,"127.0.0.1",4096,5081) # Getting the local message 
       print("Message out",data_out)

            
t1 = threading.Thread(target=Camera_multi)
t2 = threading.Thread(target=Camera_cache_server)
t3 = threading.Thread(target=Face_recog_cache_0) 
t4 = threading.Thread(target=Qr_code_scanner_0)
t5 = threading.Thread(target=Qr_cache_sub_node)
t1.start() 
t2.start() 
t3.start() 
t4.start() 
t5.start()

