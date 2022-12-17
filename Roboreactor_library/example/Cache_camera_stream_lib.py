from itertools import count 
import threading 
from roboreactmaster import Camera_multi_cache,Cache_server
def Camera_multi():
      Camera_multi_cache(0,'127.0.1.5',9999,320)
def Camera_cache_server():
      Cache_server('127.0.1.5','127.0.1.11',9999)
t1 = threading.Thread(target=Camera_multi)
t2 = threading.Thread(target=Camera_cache_server)
t1.start() 
t2.start()