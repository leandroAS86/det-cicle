import os
import video_path

IOU = 0.5
CONF = 0.5
IMGSZ = 416

LIMIT_TIME = 1
ANGLE_POINTS = 0
TRACK_POINTS = 25
DISTANCE = 250

DEBUG = 0
DELAY = 1
WIDTH = 1080
HEIGHT = 800

X_START = 100
Y_START = 50

CAPTURE_TIME = 60 # tempo em segundos de captura

RESULTS_VIDEOS = video_path.results()
VIDEO_PATH, VIDEO = video_path.video_path()

IMAGES_PATH = os.path.join(os.getcwd(), 'datasets', 'images')
RESULTS_IMAGES = os.path.join(os.getcwd(), 'results', 'images')

RESULTS_CAPTURE = os.path.join(os.getcwd(), 'results', 'capture')

FILES = os.path.join(os.getcwd(), 'files', 'ciclist')

MODEL_PATH = os.path.join(os.getcwd(), 'models', 'yolo_best_saved', 'best.pt') # GPU
# MODEL_PATH = os.path.join(os.getcwd(), 'models', 'yolo_best_saved', 'best_full_integer_quant.tflite') # CPU
# MODEL_PATH = os.path.join(os.getcwd(), 'models', 'yolo_best_saved', 'best_full_integer_quant_edgetpu.tflite.tflite') # Raspberry pi 4

# COMPASS = ['Norte', 'Leste', 'Sul', 'Oeste', 'Norte']
# COMPASS = ['Jd. Botanico', 'Centro', 'Agua Verde', 'Hauer', 'Jd. Botanico']
COMPASS = ['A +', 'B +', 'A -', 'B -', 'A +']
