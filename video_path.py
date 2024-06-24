import os

PATH_BASE = os.getcwd() 
RESULTS = os.path.join(PATH_BASE, 'results', 'videos')
VIDEOS = os.path.join(PATH_BASE, 'datasets', 'videos')

VIDEO = 'video_teste.mp4'

VIDEO_PATH = os.path.join(VIDEOS, VIDEO)

def video_path():
    return VIDEO_PATH, VIDEO

def results():
    return os.path.join(RESULTS, VIDEO)