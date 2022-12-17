import os 
from roboreactmaster import Create_node_sub,get_datetime 
from itertools import count
import threading
def date_rt():
      get_datetime('127.0.0.1',5780)

def sub_node():
      for rt in count(0):
            global data_out;data_out = Create_node_sub(1,"127.0.0.1",4096,5780)
            print("Time_data ",data_out)

if __name__ =="__main__":
         t1 = threading.Thread(target=date_rt)
         t2 = threading.Thread(target=sub_node)
         t1.start() 
         t2.start() 





