import time
import math
import numpy as np
import config
from absl import logging

DEBUG = config.DEBUG
DISTANCE = config.DISTANCE 
TRACK_POINTS = config.TRACK_POINTS

LIMIT_TIME = config.LIMIT_TIME
ANGLE_POINTS = config.ANGLE_POINTS

COMPASS = config.COMPASS

class Ciclist():

    def __init__(self, id = None, track_poits = []):
        self.id=id
        self.info = ()
        self.angle = 0.0
        self.distance = ''
        self.end_direction = ''
        self.start_direction = ''
        self.to_remove = False
        self.to_couting = False
        self.created_at = time.time()
        self.track_poits = track_poits

    def __next__(self):
        self.countig()
        self.cicle_direction()
        self.remove()
        return self.end_direction, self.to_couting, self.to_remove

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def time(self):
        return time.time()

    def remove(self):

        if self.to_couting:
            last_time_update, _ = self.info
            if((self.time() - last_time_update)) > LIMIT_TIME:
                self.to_remove = True

        if not self.to_couting:
            if (len(self.track_poits) < TRACK_POINTS) and (self.time() - self.created_at > 2 * LIMIT_TIME):
                # self.print(f'ID: {self.id} Remover: %s'%(self.to_remove))
                self.to_remove = True

            # remove se nao for contado em 5 minutos
            if (self.time() - self.created_at > 10 * LIMIT_TIME):
                self.to_remove = True
        
        logging.debug(f'ID: {self.id} Remover: %s'%(self.to_remove))

    def countig(self):
        self.euclidian_distance() # atualiza a distância
        if not self.to_couting:
            if len(self.track_poits) >= TRACK_POINTS and self.distance >= DISTANCE:
                self.to_couting = True
                self.info = (self.time(), self.track_poits[-1]) # primeiro tempo de atualização do objeto

        logging.debug(f'ID: {self.id} Counting: {self.to_couting}')
        # logging.info(f'ID: {self.id} Total Points: {len(self.track_poits)}')
    
    def cicle_direction(self):
        direction = ''
        if self.to_couting:
            _, lest_point = self.info
            if tuple(np.subtract(lest_point, self.track_poits[-1])) != (0.0, 0.0):

                cx_first, cy_first = self.track_poits[-ANGLE_POINTS]
                cx_last, cy_last = self.track_poits[-1]
                delta_x, delta_y = (cx_last - cx_first, cy_last - cy_first)

                direction = self.direction(delta_x, delta_y)

                self.end_direction = direction
                if self.start_direction == '':
                    self.start_direction = self.end_direction

                self.info = (self.time(), self.track_poits[-1])
        
        logging.debug('ID: %s Direction: %s'%(self.id, direction))

    def euclidian_distance(self):
        cx_first, cy_first = self.track_poits[0]
        cx_last, cy_last = self.track_poits[-1]

        cx, cy = (cx_last - cx_first, cy_last - cy_first)
        distance = ''
        distance = math.hypot(cx, cy)

        logging.debug(f'ID: {self.id} Distance: {distance}')

        self.distance = distance

    # *************************************************
    # 
    #TODO: Melhorar esse algoritmo para obter a direção
    #
    # *************************************************
    def direction(self, delta_x, delta_y):
        angle = math.degrees(math.atan2(delta_x, delta_y))
        if angle < 0:
            angle += 360

        compass_lookup = round(angle / 90)
        self.angle = angle

        logging.debug('ID: %s Angulo: %s'%(self.id, angle))
        # self.print('ID: %s Angulo: %s'%(self.id, angle))
        
        # if angle > 0 and angle < 90:
        #     return '7 de Setembro'

        # if angle >= 90 and angle < 135:
        #     return 'Jd. Botanico'

        # if angle >= 135 and angle < 225:
        #     return 'Auto da XV'

        # if angle >= 225 and angle < 285:
        #     return 'Centro'

        # if angle >= 285 and angle < 360:
        #     return '7 de Setembro'

        return COMPASS[compass_lookup]