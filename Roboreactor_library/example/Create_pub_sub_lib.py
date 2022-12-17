import threading
from roboreactmaster import Create_node_pub,Create_node_sub 
from itertools import count
def Pub_node():
  for i in count():
      print("Pub_node_message ",{'actuators_2':{"Message":[5,7]}})
      Create_node_pub("actuators_2",{"Message":[5,7]},"127.0.0.1",5080)

def Sub_node():
     for vi in count():   
       data_out = Create_node_sub(1,"127.0.0.1",4096,5080) # Getting the local message 
       print(data_out)
             
t1 = threading.Thread(target=Pub_node)
t2 = threading.Thread(target=Sub_node)
t1.start() 
t2.start() 
