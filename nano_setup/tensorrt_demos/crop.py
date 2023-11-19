import os
import cv2
import time

def crop_image(frame, bbox, id, score):
    min_x,min_y,max_x,max_y = bbox
    print(f"bbox  : {bbox}")

    crop_img = frame[int(bbox[1]):int(bbox[3]),int(bbox[0]): int(bbox[2])]
    # Display the image
    # cv2.imshow('image', crop_img)
    save_dir = "./img_data"
    os.listdir(save_dir)

    # Current time
    curr_time = round(time.time()*1000)

    file_name = f"{save_dir}/id_{id}_score_{score}.png"
    cv2.imwrite(file_name,crop_img)
    # cv2.waitKey(0)
    




