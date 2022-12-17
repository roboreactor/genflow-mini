import threading 
from itertools import count
from roboreactmaster import Multiplenode_post_logic   #Getting the multiple_node post logic to post the data from each function to the main function 

local_ip = "http://0.0.0.0" # Getting the local host from the socket data 
face_node_1 = {"face_recog_1":{'Name': 'korn', 'X': 120, 'Y': 244, 'dx': 0.8134618751638223, 'dy': 0.33619393872038544}}
odometry_node_2 = {"odometry_2":{"X":40,"Y":90,"Z":180}}

def face_node():
    for i in count(0): 
        #Need to using the Communication node subscriber  
        post_output_1 = Multiplenode_post_logic(face_node_1,local_ip,5340,"Multiplenode_logic")
        print("Post_request_1",post_output_1)
def odometry_node():
    for i in count(0): 
        #Neet to using the Communication node subscriber 
        post_output_2 = Multiplenode_post_logic(odometry_node_2,local_ip,5340,"Multiplenode_logic")
        print("Post_request_2",post_output_2)

t1 = threading.Thread(target=face_node)
t2 = threading.Thread(target=odometry_node)
t1.start() 
t2.start() 



