# import cv2
# import numpy as np
# import imutils

# cap = cv2.VideoCapture('./video/vid.avi')

# bgs = cv2.BackgroundSubtractorMOG2()

# # (x, y, w, h) = cv2.boundingRect(c)
# # cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 20)
# # roi = frame[y:y+h, x:x+w]


# while True:
#     ret, frame = cap.read()
#     if frame is None:
#         break

#     frame = imutils.resize(frame,width=720)


#     subf = bgs.apply(frame)
#     # cv2.imshow('Video', subf)
#     cv2.imshow('Video', frame)
#     if cv2.waitKey(1) == 27:
#         exit(0)

from __future__ import print_function
import cv2 as cv
import argparse
import numpy as np
import time
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2( )
    #detectShadows = False,varThreshold=30
else:
    backSub = cv.createBackgroundSubtractorKNN()

kernel_dil = np.ones((3,3),np.uint8)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))

capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened():
    print('Unable to open: ' + args.input)
    exit(0)

count = 1
avg_time = 0
total_tym = 0
while True:
    ret, frame = capture.read()
    if frame is None:
        break

    start_time =time.time()
    fshape = frame.shape
    cv.rectangle(frame, (355, 55), (700,140), (0,0,0), -1)
    cv.rectangle(frame, (520, 130), (700,180), (0,0,0), -1)
    frame = frame[:,:fshape[1]-100,:]
    # frame = cv.GaussianBlur(frame, (5,5), cv.BORDER_DEFAULT)

    if ret == True:
        fgmask = backSub.apply(frame)
        fgmask = cv.morphologyEx(fgmask, cv.MORPH_CLOSE,kernel)
        dilation = cv.dilate(fgmask, kernel_dil, iterations=1)

        (contours, hierarchy) = cv.findContours(dilation,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
        
        for pic , contour in enumerate(contours):
         
            area = cv.contourArea(contour)
            if area > 3500:
                print('area : ', area)
                x,y,w,h = cv.boundingRect(contour)
                print('x,y,w,h : ', x,y,w,h)
        #         img = cv.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

        end_time = time.time()
        total_tym = total_tym + end_time - start_time 
        avg_time = (total_tym )/count
        count = count+1
        print("detection run on a frame. Time =", end_time - start_time)
        print("AVG run on a frame. Time =", avg_time)
        print('\n\n')
        cv.imshow("original",dilation)
        if cv.waitKey(25)^ 0xFF == ord('q'):
            break
    else:
        break


#     gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

#     gaussian = cv.GaussianBlur(gray, (5,5), cv.BORDER_DEFAULT)


#     kernel = np.ones((3, 3), np.uint8)
#     closing = cv.morphologyEx(gaussian, cv.MORPH_CLOSE, kernel)

#     cv.rectangle(closing, (355, 55), (700,140), (0,0,0), -1)
#     cv.rectangle(closing, (520, 130), (700,180), (0,0,0), -1)
#     fgMask = backSub.apply(closing)
    
#     cv.rectangle(gaussian, (10, 2), (100,20), (255,255,255), -1)
#     cv.putText(gaussian, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
#                cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
#     cv.imshow('Frame', fgMask)
#     cv.imshow('FG Mask', closing)
    
#     keyboard = cv.waitKey(27)
#     if keyboard == 'q' or keyboard == 27:
#         break



