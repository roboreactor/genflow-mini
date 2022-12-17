from itertools import count 
import threading
import time 
from roboreactmaster import Camera_multi_cache,Cache_server,Camera_Qr_cache
def Camera_multi():
      Camera_multi_cache(0,'127.0.1.5',9999,320)
def Camera_cache_server():
      Cache_server('127.0.1.5','127.0.1.11',9999)
def Qr_code_scanner_0(): 
      time.sleep(3) 
      Camera_Qr_cache(0,1,'127.0.1.11',9999)
t1 = threading.Thread(target=Camera_multi)
t2 = threading.Thread(target=Camera_cache_server)
t3 = threading.Thread(target=Qr_code_scanner_0)
t1.start() 
t2.start()
t3.start()
