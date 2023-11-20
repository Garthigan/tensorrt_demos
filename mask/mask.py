import numpy as np
import matplotlib.pyplot as plt
import cv2
import json




def plot_line(frame  , mask_coordinates, sample_image):


    h, w = sample_image
    height, width = frame.shape[:2]

    edge_coordinates = [[int((a / w) * width), int((b / h) * height)] for a, b in mask_coordinates]
    mask = np.ones((height,width))
    mask.fill(-1)
    roi_corners = np.array([edge_coordinates], dtype=np.int32)
    cv2.fillPoly(mask, roi_corners, (1))

    return mask

