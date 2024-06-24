import cv2
import time
import collections

import pandas as pd
import numpy as np

import config

WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
X_START = config.X_START
Y_START = config.Y_START

def avg_fps_counter(window_size):
    window = collections.deque(maxlen=window_size)
    prev = time.monotonic()
    yield 0.0  # First fps value.

    while True:
        curr = time.monotonic()
        window.append(curr - prev)
        prev = curr
        yield len(window) / sum(window)

def put_text_rect(img, text, pos, scale=3, thickness=3, colorT=(255, 255, 255),
                colorR=(255, 0, 255), font=cv2.FONT_HERSHEY_PLAIN,
                offset=10, border=None, colorB=(0, 255, 0)):
    """
    Creates Text with Rectangle Background
    :param img: Image to put text rect on
    :param text: Text inside the rect
    :param pos: Starting position of the rect x1,y1
    :param scale: Scale of the text
    :param thickness: Thickness of the text
    :param colorT: Color of the Text
    :param colorR: Color of the Rectangle
    :param font: Font used. Must be cv2.FONT....
    :param offset: Clearance around the text
    :param border: Outline around the rect
    :param colorB: Color of the outline
    :return: image, rect (x1,y1,x2,y2)
    """
    ox, oy = pos
    (w, h), _ = cv2.getTextSize(text[0] + text[1], font, scale, thickness)

    x1, y1, x2, y2 = ox - offset, oy + offset, ox + w + offset, oy - h - offset

    for i, line in enumerate(text, start=1):
        cv2.putText(img,line, (ox, oy + (15 * i)), font, scale, colorT, thickness)

    return img, [x1, y2, x2, y1]

def crop_frame(frame):
    # Cropping a frame
    # height, width, channels = frame.shape
    return frame[Y_START:HEIGHT + Y_START, X_START:WIDTH + X_START]


def frame_to_show(results, frame, total, track_history=None):

    classe = results[0].names[0]
    inference = results[0].speed['inference']/1000
    fps = 1 / inference

    text_lines = [
    #   'Inference: {:.2f} ms'.format((inference) * 1000),
    #   'FPS: {:.2f}'.format(fps),
      'Total: {}'.format(total)
    ]
    
    for i, line in enumerate(text_lines, start=1):
        text_size, _ = cv2.getTextSize(
            line, 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 2)
        text_w, text_h = text_size
        cv2.rectangle(frame, (5, 5), (15 + text_w, 15 + text_h), (255, 255, 255), -1)
        cv2.putText(img=frame, text=line, org=(10, i * 30),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
            color=(128,0,128), thickness=2, lineType=cv2.LINE_AA)

    if results[0].boxes.id is not None:
        points = []
        direction = ''
        color = (0, 0, 255)

        result = pd.DataFrame(
            results[0].boxes.data).astype("float")

        for index,row in result.iterrows():

            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])

            id = row[4]
            score = row[5] * 100
            ciclist = track_history[id] if id in track_history else None
            if ciclist is not None:

                direction = ciclist.end_direction
                color = (0, 255, 0) if ciclist.to_couting else (0, 0, 255)

                points = np.hstack(ciclist.track_poits).astype(np.int32).reshape((-1, 1, 2))
                cv2.polylines(frame, [points], isClosed=False, color=color, thickness=3)

                cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)

                text_lines = [
                  'ID:: {}'.format(id),
                  'Score:: {:.1f}'.format(score)
                ]

                if(ciclist.to_couting):
                    text_lines.insert(2, 'Direction:: {}'.format(direction))

                put_text_rect(frame, text_lines, (x1 + 10, y1 - 10), 1, 1)

    return frame
