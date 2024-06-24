import os
import cv2
from absl import app
from absl import flags
from absl import logging

import config
from utils.common import *
from detcicle.detcicle import DetCicle

flags.DEFINE_float('iou', config.IOU, 'IOU')
flags.DEFINE_float('conf', config.CONF, 'Confidence')
flags.DEFINE_integer('imgsz', config.IMGSZ, 'Image Size')
flags.DEFINE_float('time', config.CAPTURE_TIME, 'Tempo de captura pelo sistema')
flags.DEFINE_bool('save', False, 'Salvar inferências em video pré gravado')
flags.DEFINE_string('mode', None, 'Modo de operação do sistema: image, video ou capture')
flags.DEFINE_bool('debug', config.DEBUG, 'Modo de depuração')
flags.DEFINE_string('path', None, 'Local para carregar os arquivos de imagens ou video')
flags.DEFINE_string('result', None, 'Local para salvar o resultado')

flags.mark_flag_as_required('mode')

FLAGS = flags.FLAGS

def run():

    if FLAGS.debug:
        logging.set_verbosity(logging.DEBUG)
    
    detCicle = DetCicle()
    
    if FLAGS.mode == 'video':
        if FLAGS.save:
            detCicle.track_and_save()
        else:
            detCicle.track()
    elif FLAGS.mode == 'image':
        detCicle.predict()
    elif FLAGS.mode == 'capture':
        detCicle.capture_and_track()
    else:
        print('{}'.format(FLAGS))

    cv2.destroyAllWindows()

def main(_):
    run()

if __name__ == '__main__':    
    try:
        app.run(main)
    except SystemExit:
        pass
