import threading 
import socket 
from itertools import count 
from roboreactmaster import Multiplenode_get_logic 

local_ip = "http://0.0.0.0" # Getting the local host ip

def Multiple_node_1():
         for i in count(0):
                 dataout = Multiplenode_get_logic(local_ip,5340,"get_Multiplenode_logic")
                 print("node_1",dataout)
def Multiple_node_2():
         for i in count(0):
                  dataout2 = Multiplenode_get_logic(local_ip,5340,"get_Multiplenode_logic") 
                  print("node_2",dataout2)  

t1 = threading.Thread(target=Multiple_node_1)
t2 = threading.Thread(target=Multiple_node_2)
t1.start() 
t2.start() 
