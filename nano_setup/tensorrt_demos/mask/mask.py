import numpy as np
import matplotlib.pyplot as plt
import cv2

def plot_line(frame):

    img_name = "points/sample.png"
    img = cv2.imread(img_name)
    h, w = img.shape[:2]
    height, width = frame.shape[:2]
    edge_coordinates = [

        [int((31/w)*width),int((0/h)*height)],
        [int((182/w)*width),int((360/h)*height)],
        [int((835/w)*width),int((335/h)*height)],
        [int((919/w)*width),int((0/h)*height)]

        ]
    
    mask = np.ones((height,width))
    mask.fill(-1)
    roi_corners = np.array([edge_coordinates], dtype=np.int32)
    cv2.fillPoly(mask, roi_corners, (1))

    return mask



"""


        [int((31/w)*width),int((0/h)*height)],
        [int((182/w)*width),int((360/h)*height)],
        [int((835/w)*width),int((335/h)*height)],
        [int((919/w)*width),int((0/h)*height)]

        (31, 3)
        (182, 360)
         (835, 335)
        (919, 7)



"""