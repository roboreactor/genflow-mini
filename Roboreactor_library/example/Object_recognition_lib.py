import requests
from roboreactmaster import Face_recognition, Camera_pub_node, Speech_recognition, Create_node_sub, Speaking_languages, Camera_yolo_sub_node
import threading
from itertools import count
model_prototxt = "MobileNetSSD_deploy.prototxt"
model_caffe_weights = "MobileNetSSD_deploy.caffemodel"

object_label = {0: 'background', 1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat', 5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair', 10: 'cow',
                                11: 'diningtable', 12: 'dog', 13: 'horse', 14: 'motorbike', 15: 'person', 16: 'pottedplant', 17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}


def Camera_raw():
    Camera_pub_node(0, 65536, 5609, '127.0.0.1')


def Object_recogition():
    Camera_yolo_sub_node(0, 65536, 5609, 5081, '127.0.0.1', 'Non', object_label, model_prototxt,
                         model_caffe_weights)  # ,'Non',object_label,model_prototxt,model_caffe_weights)


def object_rec_sub_node():
    for rt in count(0):
        global data_out_1
        data_out_1 = Create_node_sub(1, "127.0.0.1", 4096, 5081)
        print(data_out_1)


t1 = threading.Thread(target=Camera_raw)
t2 = threading.Thread(target=Object_recogition)
t3 = threading.Thread(target=object_rec_sub_node)
t1.start()
t2.start()
t3.start()
