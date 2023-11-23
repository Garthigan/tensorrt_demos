# nolimit-kandy -format
import os

# comment out below line to enable tensorflow logging outputs
print("initializing")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import cv2
from mask import mask as md
import psutil
import time
import pycuda.autoinit
import tensorflow as tf
import json

# change number of blocks per thread
physical_devices = tf.config.experimental.list_physical_devices("GPU")
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
print(physical_devices)

import queue
import threading
import core.utils as utils
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as mqtt
from absl import app, flags, logging
from absl.flags import FLAGS
from core.config import cfg
from core.yolov4 import filter_boxes
from deep_sort import nn_matching, preprocessing
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from PIL import Image
from tensorflow.compat.v1 import ConfigProto, InteractiveSession
from tensorflow.python.saved_model import tag_constants
from tools import generate_detections as gdet
from utils.yolo_with_plugins import TrtYOLO



variable_nano_file_path = "/home/nvidia/Downloads/tensorrt_demos/variable_xaviar.json"
with open(variable_nano_file_path, 'r') as file:
    json_data = file.read()
parsed_data = json.loads(json_data)
rtsp_link = parsed_data['rtsp_link_2']
mask_coordinates = parsed_data['mask_coordinates_2']

flags.DEFINE_integer("category_num", 80, "number of object categories [80]")
flags.DEFINE_string("output", None, "path to output video")
flags.DEFINE_boolean("count", False, "count objects being tracked on screen")


class RTSVideoCapture:
    # Global exp_thread
    def __init__(self, name):
        self.name = name
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        self.stop_thread = False
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # Read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.cap = cv2.VideoCapture(self.name)

            if not self.q.empty():
                try:
                    # Discard previous (unprocessed) frame
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        if self.q.empty():
            return None
        return self.q.get()

    def stop(self):
        self.cap.release()
        self.stop_thread = True


def main(_argv):
    # Definition of the parameters
    max_cosine_distance = 0.4
    nn_budget = None
    nms_max_overlap = 1.0
    model_name = "yolov4-tiny-3l-ch-2203-416"
    # initialize deep sort
    model_filename = "model_data/mars-small128.pb"
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    # calculate cosine distance metric
    metric = nn_matching.NearestNeighborDistanceMetric(
        "cosine", max_cosine_distance, nn_budget
    )
    # Initialize tracker
    tracker = Tracker(metric)
    # Load configuration for object detector
    input_size = int(model_name[-3:])

    video_path = rtsp_link

    print("load model")

    # begin video capture
    try:
        vid = RTSVideoCapture(int(video_path))
    except Exception as ex:
        vid = RTSVideoCapture(video_path)
        print("Error in video path")
        print("Exception : {}".format(ex))

    out = None

    # get video ready to save locally if flag is set
    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width, height))

    frame_num = 0
    countt = 0
    send_status = 0
    pre_count = 0
    in_trackids = []  # added by thanu to store the ids of people who entered

    letter_box = False
    trt_yolo = TrtYOLO(model_name, FLAGS.category_num, letter_box)
    print("TrtYOLO LOADED")

    # Crop image count
    count = 0
    frame = vid.read()

    mask_2 = md.plot_line(frame, mask_coordinates)
    print(mask_2)

    # Create the log file
    tim = time.localtime()
    if not os.path.exists("log"): os.makedirs("log")
    msg_log_file = "log/message_{}_{}_{}.log".format(tim.tm_wday, tim.tm_hour, tim.tm_min)

    open(msg_log_file, "w").close()
    file = open("count2.log", "w")
    file.close()

    # while video is running
    log_file = open(msg_log_file, "a")
    time_7 = 0

    # while video is running
    print("Footfall counting system started")

    while True:
        time_1 = time.time()
        tim = time.localtime()

        # Stop system between 12AM to 08AM
        if tim.tm_hour < 8:
            print("system going to sleep mode")
            break

        frame = vid.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_wait = time.time() - time_7

        else:
            continue  # break

        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            continue

        frame_num += 1
        print("Frame number : ",frame_num)
        image_data = cv2.resize(frame, (input_size, input_size))

        start_time = time.time()
        # Conf Thresh
        conf_th = 0.25
        boxes, scores, classes = trt_yolo.detect(image_data, conf_th)
        end_time = time.time()

        time_4 = time.time()
        num_objects = len(boxes)
        bboxes = boxes[:, [1, 0, 3, 2]]
        bboxes = bboxes / input_size

        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(bboxes, original_h, original_w)

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)
        allowed_classes = ["bicycle"]
        names = []
        deleted_indx = []
        time_5 = time.time()

        tracks_len = len(tracker.tracks)
        for i in range(num_objects):
            class_indx = int(classes[i])
            class_name = class_names[class_indx]

            if class_name not in allowed_classes:
                deleted_indx.append(i)
            else:
                names.append(class_name)

            count = count + 1

        time_6 = time.time()
        names = np.array(names)
        count = len(names)

        bboxes = np.delete(bboxes, deleted_indx, axis=0)
        scores = np.delete(scores, deleted_indx, axis=0)

        # encode yolo detections and feed to tracker
        time_6_1 = time.time()
        features = encoder(frame, bboxes)
        detections = [
            Detection(bbox, score, class_name, feature)
            for bbox, score, class_name, feature in zip(bboxes, scores, names, features)
        ]
        time_6_2 = time.time()

        # initialize color map
        cmap = plt.get_cmap("tab20b")
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

        # run non-maxima supression
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(
            boxs, classes, nms_max_overlap, scores
        )
        detections = [detections[i] for i in indices]

        # Call the tracker
        time_6_3 = time.time()
        tracker.predict()
        time_6_4 = time.time()
        tracker.update(detections)
        time_6_5 = time.time()

        time_8 = time.time()
        for i, track in enumerate(tracker.tracks):
            if not track.is_confirmed() or track.time_since_update > 1:
                continue
            bbox = track.to_tlbr()

            class_name = track.get_class()
            # Added by thanu
            min_x, min_y, max_x, max_y = bbox
            new_mid_x = (min_x + max_x) / 2
            new_mid_y = (min_y + max_y) / 2

            distance = mask_2[int(new_mid_y), int(new_mid_x)]
            color_circle = (int((distance + 1) * 128), 0, 0)
            frame = cv2.circle(
                frame, (int(new_mid_x), int(new_mid_y)), 6, color_circle, -1
            )

            if distance > 0:
                sign = "positive"
            else:
                sign = "negative"

            if tracker.trackframes[int(track.track_id)]["init_sign"] == "undefined":
                tracker.trackframes[int(track.track_id)]["init_sign"] = sign
            else:
                if (
                    (
                        tracker.trackframes[int(track.track_id)]["init_sign"]
                        == "positive"
                    )
                    and sign == "negative"
                    and track.state == 2
                    and track.track_id not in in_trackids
                ):
                    in_trackids.append(track.track_id)

            # Arunn process track details
            dd = tracker.trackframes[int(track.track_id)]
            dd[1] += 1

            if dd[1] > 2 and dd[2] != "sent":
                dd[2] = "sent"
                tracker.trackframes[int(track.track_id)] = dd

            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]

            cv2.rectangle(
                frame,
                (int(bbox[0]), int(bbox[1])),
                (int(bbox[2]), int(bbox[3])),
                color,
                2,
            )
            cv2.putText(
                frame,
                "People IN Count(using door line): {}".format(len(in_trackids)),
                (5, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 0, 255),
                2,
            )

            # for i in range(len(edge_coordinates) - 1):
            #     color = (0, 0, 255)
        time_3 = time.time()
        if FLAGS.count:
            cv2.putText(
                frame,
                "total count: {}".format(countt),
                (5, 35),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                2,
                (0, 255, 0),
                2,
            )

        # calculate frames per second of running detections
        fps = 1.0 / (time.time() - start_time)
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        color = (255, 0, 0)

        # if output flag is set, save video file
        if FLAGS.output:
            out.write(result)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        len_trackid = len(in_trackids)
        time_7 = time.time()
        print(time.time(), "  total count : ",len_trackid)

        tim = time.localtime()
        # reset parameters in start of every day.
        if tim.tm_min % 2 == 0 and tim.tm_sec == 0:
            if send_status == 0:
                file = open("count2.log", "w+")
                two_min_count = len_trackid - pre_count
                data = "{} current people count {} {}\n".format(
                    time.ctime(), len_trackid, two_min_count
                )
                pre_count = len_trackid
                file.write(data)
                file.close()
                send_status = 1
        else:
            send_status = 0

        mem_used = psutil.virtual_memory()
        log_file.write(
            "{} : Frame : {}. No_Box :{} . YOLO_time :{:.4f} count :{} TTime :{:.4f} Trackes-Len : {} Memory_use :{}\n".format(
                time.ctime(),
                frame_num,
                len(boxes),
                end_time - start_time,
                len_trackid,
                time_7 - time_1,
                tracks_len,
                mem_used.percent,
            )
        )

        log_file.write(
            "{} : Frame : {} last_exe : {:.4f} T_time : {:.4f} Track_time : [T: {:.4f} e: {:.4f} p: {:.4f} u: {:.4f}] Log_time : {:.4f} Wait_frame : {:.4f}\n".format(
                time.ctime(),
                frame_num,
                time_7 - time_3,
                time_5 - time_4,
                time_8 - time_6,
                time_6_2 - time_6_1,
                time_6_4 - time_6_3,
                time_6_5 - time_6_4,
                time_3 - time_8,
                frame_wait,
            )
        )

    cv2.destroyAllWindows()
    vid.stop()
    print("System stoped")
    log_file.close()


if __name__ == "__main__":
    try:
        app.run(main)
    except SystemExit:
        pass