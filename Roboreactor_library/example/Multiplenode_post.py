from roboreactmaster import Multiplenode_server,Multiplenode_post_logic,Multiplenode_get_logic
from itertools import count 
for i in count(0):
         Multiplenode_post_logic({'Sensor1':30.56},"http://192.168.50.192","4060","Multiple_node_2")


