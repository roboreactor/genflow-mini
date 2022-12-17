import threading
from itertools import count
from roboreactmaster import Camera_pub_node,Camera_sub_node,Create_node_sub,Create_sub_node_string
def raw_cam():
      Camera_pub_node(0,65536,9801,'127.0.0.1')

def camera_sub():
   
         frame_out =   Camera_sub_node(0,65536,9801,'127.0.0.1','127.0.0.1',5630)
         print("frame_out:",frame_out) 
def camera_sub_node():
     
        for rt in count(0):
            global data_out;data_out = Create_node_sub(0,'127.0.0.1',66536,5630)
            print("frame_output ",data_out)
def camera_Sub_string():
       for rt in count(0): 
            global data_out;data_out = Create_sub_node_string('127.0.0.1',66536,5630)
            print("frame_data:",data_out)
t1 = threading.Thread(target=raw_cam)
t2 = threading.Thread(target=camera_sub)
#t3 = threading.Thread(target=camera_Sub_string)
t1.start() 
t2.start() 
#t3.start()