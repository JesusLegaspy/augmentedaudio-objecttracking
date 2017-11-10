import os
import cv2
import time
import argparse
import numpy as np
import tensorflow as tf
import logging

from queue import Queue
from threading import Thread
from utils.app_utils import FPS, WebcamVideoStream, draw_boxes_and_labels
from object_detection.utils import label_map_util
from depth_sensing import func

import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core

from client.UnityTrackerResource import UnityTracker
unity = UnityTracker()

CWD_PATH = os.getcwd()

# Path to frozen detection graph. This is the actual model that is used for the object detection.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
PATH_TO_CKPT = os.path.join(CWD_PATH, 'object_detection', MODEL_NAME, 'frozen_inference_graph.pb')

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join(CWD_PATH, 'object_detection', 'data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90

# Loading label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                            use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def detect_objects(image_np, sess, detection_graph):
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np[:, :, :-1], axis=0)

    #print('[INFO] elapsed time for the array weirdness: {:.9f}'.format(time.time() - ticks))

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

    # Each box represents a part of the image where a particular object was detected.
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

    ##logging.debug(image_np_expanded.shape)
    # Actual detection.
    (boxes, scores, classes, num_detections) = sess.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})


    # Visualization of the results of a detection.
    rect_points, class_names, class_colors = draw_boxes_and_labels(
        boxes=np.squeeze(boxes),
        classes=np.squeeze(classes).astype(np.int32),
        scores=np.squeeze(scores),
        category_index=category_index,
        min_score_thresh=.5
    )
    return dict(rect_points=rect_points, class_names=class_names, class_colors=class_colors)


def worker(input_q, output_q):
    # Load a (frozen) Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    fps = FPS().start()
    while True:
        fps.update()
        frame = input_q.get()
        output_q.put(detect_objects(frame, sess, detection_graph))

    fps.stop()
    sess.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-src', '--source', dest='video_source', type=int,
                        default=0, help='Device index of the camera.')
    parser.add_argument('-wd', '--width', dest='width', type=int,
                        default=1280, help='Width of the frames in the video stream.')
    parser.add_argument('-ht', '--height', dest='height', type=int,
                        default=720, help='Height of the frames in the video stream.')
    args = parser.parse_args()

    input_q = Queue(5)  # fps is better if queue is higher but then more lags
    output_q = Queue()
    for i in range(1):
        t = Thread(target=worker, args=(input_q, output_q))
        t.daemon = True
        t.start()
    '''
    video_capture = WebcamVideoStream(src=args.video_source,
                                      width=args.width,
                                      height=args.height).start()
    '''

    unity.connect()
    # Create a PyZEDCamera object
    zed = zcam.PyZEDCamera()

    # Create a PyInitParameters object and set configuration parameters
    init_params = zcam.PyInitParameters()
    init_params.camera_resolution = sl.PyRESOLUTION.PyRESOLUTION_HD720  # Use HD1080 video mode
    init_params.camera_fps = 30  # Set fps at 30

    # Open the camera
    err = zed.open(init_params)
    if err != tp.PyERROR_CODE.PySUCCESS:
        exit(1)

    image = core.PyMat()

    fps = FPS().start()

    while True:
        if zed.grab(zcam.PyRuntimeParameters()) == tp.PyERROR_CODE.PySUCCESS:
            # A new image is available if grab() returns PySUCCESS
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
            timestamp = zed.get_camera_timestamp()  # Get the timestamp at the time the image was captured
            logging.debug("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(), image.get_height(), timestamp))
            frame = image.get_data()

            '''
            frame = frame.tolist()
            for i in frame:
                for j in i:
                    j.pop()
            frame = np.array(frame)
            '''

            input_q.put(frame)

            t = time.time()
            centers = []

            if output_q.empty():
                pass  # fill up queue
            else:
                font = cv2.FONT_HERSHEY_SIMPLEX
                data = output_q.get()
                rec_points = data['rect_points']
                class_names = data['class_names']
                class_colors = data['class_colors']
                for point, name, color in zip(rec_points, class_names, class_colors):
                    cv2.rectangle(frame, (int(point['xmin'] * args.width), int(point['ymin'] * args.height)),
                                  (int(point['xmax'] * args.width), int(point['ymax'] * args.height)), color, 3)
                    cv2.rectangle(frame, (int(point['xmin'] * args.width), int(point['ymin'] * args.height)),
                                  (int(point['xmin'] * args.width) + len(name[0]) * 6,
                                   int(point['ymin'] * args.height) - 10), color, -1, cv2.LINE_AA)
                    cv2.putText(frame, name[0], (int(point['xmin'] * args.width), int(point['ymin'] * args.height)), font,
                                0.3, (0, 0, 0), 1)

                    xmin = int(point['xmin'] * args.width)
                    xmax = int(point['xmax'] * args.width)
                    ymin = int(point['ymin'] * args.height)
                    ymax = int(point['ymax'] * args.height)
                    center = int(xmin + float(xmax-xmin)/2), int(ymin + float(ymax-ymin)/2)
                    centers.append(center)
                    logging.debug (centers[0][0], centers[0][1])

                if (len(centers) > 0):
                    func(centers,zed,unity)


                cv2.imshow('Video', frame)

            fps.update()

            logging.debug('[INFO] elapsed time: {:.2f}'.format(time.time() - t))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    fps.stop()  # Lol IDK
    logging.debug('[INFO] elapsed time (total): {:.2f}'.format(fps.elapsed()))
    logging.debug('[INFO] approx. FPS: {:.2f}'.format(fps.fps()))

    zed.close()
    unity.close()
    cv2.destroyAllWindows()
