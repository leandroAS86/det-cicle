import os
import cv2
import glob
from PIL import Image
from absl import flags
from absl import logging

import config
from utils.common import *
from gstream.gstream import *
from tracker.yolov8 import YoloV8
from counting.cicle_counting import CicleCounting

FLAGS = flags.FLAGS

DEBUG = config.DEBUG
DELAY = config.DELAY

WIDTH = config.WIDTH
HEIGHT = config.HEIGHT

VIDEO = config.VIDEO
VIDEO_PATH = config.VIDEO_PATH
RESULTS_VIDEOS = config.RESULTS_VIDEOS

RESULTS_CAPTURE = config. RESULTS_CAPTURE

IMAGES_PATH = config.IMAGES_PATH
RESULTS_IMAGES = config.RESULTS_IMAGES

CAPTURE_TIME = config.CAPTURE_TIME

class DetCicle():
    def __init__(self):
        self.model = YoloV8(conf=FLAGS.conf, iou=FLAGS.iou, imgsz=FLAGS.imgsz)
        self.counting = CicleCounting(self.model.track_history)
    
    def predict(self):
        
        img_id = 0
        path = FLAGS.path if FLAGS.path is not None else IMAGES_PATH
        predict = FLAGS.result if FLAGS.result is not None else RESULTS_IMAGES

        IMG_FORMAT = ['.png', '.jpg', '.jpeg']
        for img in IMG_FORMAT:
            image_path = os.path.join(path, '*{}'.format(img))
            for image in glob.glob(image_path):
                results = self.model.predict(image)[0].plot()[:, :, [2,1,0]]
                Image.fromarray(results).save(os.path.join(predict, '{}{}'.format(img_id, img)))
                img_id += 1

    
    def track_and_counting(self, frame):   
        results = self.model.track(frame)
        self.model.tracks_persisting(results)
        self.counting.next()

        return results        

    def track_and_save(self):

        path = FLAGS.path if FLAGS.path is not None else VIDEO_PATH
        predict = FLAGS.result if FLAGS.result is not None else RESULTS_VIDEOS

        cap = cv2.VideoCapture(path)

        if (cap.isOpened() == False):
            print("Error opening video stream or file")

        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        videoWriter = cv2.VideoWriter(predict, fourcc, 30.0, (WIDTH, HEIGHT))

        while cap.isOpened():
            # Wait for the  next frame
            ret, frame = cap.read()
            if ret == True:
                frame = crop_frame(frame)
                results = self.track_and_counting(frame)
                frame = frame_to_show(results, frame, self.counting.total_cicle, self.counting.track_history)

                cv2.imshow('DetCicle', frame)
                videoWriter.write(frame)

            if cv2.waitKey(DELAY) & 0xFF == ord('q'):
                break

        videoWriter.release()

    def track(self):

        path = FLAGS.path if FLAGS.path is not None else VIDEO_PATH
        cap = cv2.VideoCapture(path)

        if (cap.isOpened() == False):
            print("Error opening video stream or file")

        fps_counter = avg_fps_counter(30)
        while cap.isOpened():
            # Wait for the  next frame
            ret, frame = cap.read()
            if ret == True:
                frame = crop_frame(frame)
                results = self.track_and_counting(frame)
                frame = frame_to_show(results, frame, self.counting.total_cicle, self.counting.track_history)

                if FLAGS.debug:
                    fps = round(next(fps_counter))
                    if fps > 0:
                        print('FPS:: {} 1/FPS:: {:.5f}'.format(fps, 1/fps))

                cv2.imshow('DetCicle', frame)

            if cv2.waitKey(DELAY) & 0xFF == ord('q'):
                break
            
    def capture_and_track(self):
        
        video = Gstream()

        predict = FLAGS.result if FLAGS.result is not None else RESULTS_CAPTURE
        fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
        videoWriter = cv2.VideoWriter(
        os.path.join(predict, '{}.mp4'.format(str(int(time.time())))),
        fourcc, 30.0, (WIDTH, HEIGHT))

        video_time = 0
        start = time.perf_counter()

        capture_time = FLAGS.time if FLAGS.time is not None else CAPTURE_TIME
        while video_time <= capture_time:
        
            if not video.frame_available():
                continue
            
            # Wait for the  next frame
            frame = video.frame()
            frame = crop_frame(frame)
            self.track_and_counting(frame)

            # cv2.imshow('DetCicle', frame)

            # if cv2.waitKey(DELAY) & 0xFF == ord('q'):
            #     break
            
            videoWriter.write(frame)
            video_time = time.perf_counter() - start
        logging.debug(f'Capture time: {video_time}')
            
            