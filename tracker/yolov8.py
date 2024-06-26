
from ultralytics import YOLO
from collections import defaultdict
from detcicle.ciclist import Ciclist
import config

MODEL_PATH = config.MODEL_PATH

class YoloV8():
    def __init__(self, conf=0.5, iou=0.5, imgsz=416):
        # Store the track history
        self.iou=iou
        self.conf=conf
        self.imgsz=imgsz
        self.model = YOLO(MODEL_PATH.format(imgsz), task='detect')
        self.track_history = defaultdict(lambda: [])
        

    def predict(self, frame):
        return self.model.predict(
            frame,
            iou=self.iou,
            conf=self.conf,
            imgsz=self.imgsz
        )

    def track(self, frame, persist=True):
        return self.model.track(
            frame,
            iou=self.iou,
            conf=self.conf,
            persist=persist,
            imgsz=self.imgsz
        )
    
    def tracks_persisting(self, results):
        boxes = []
        track_ids = []

        if results[0].boxes.id is not None:
            boxes = [b for b in results[0].boxes.xywh.cpu().tolist()]
            track_ids = results[0].boxes.id.int().cpu().tolist()

        for box, track_id in zip(boxes, track_ids):
            
            if track_id not in self.track_history:
                self.track_history[track_id] = Ciclist(track_id, [])

            self.track_history[track_id].track_poits.append((float(box[0]), float(box[1])))