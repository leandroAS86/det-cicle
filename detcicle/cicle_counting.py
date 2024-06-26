
import os
import json
import time
import config
from datetime import datetime
from collections import defaultdict
from absl import logging

DEBUG = config.DEBUG
CICLIST_FILES = config.FILES

class CicleCounting():

    def __init__(self, track_history={}):
        self.total_cicle=0
        self.track_history = track_history
        self.cicle_couted = defaultdict(lambda: [])

    def __next__(self):
        self.counting()
        return self.total_cicle

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def counting(self):
        key_to_remove = []
        for k, c in self.track_history.items():

            _, to_couting, to_remove = c.next()
            if k not in self.cicle_couted:
                if to_couting:
                    self.total_cicle += 1
                    self.cicle_couted[k] = c

            if to_remove:
                key_to_remove.append(k)
                self.cicle_couted.pop(k, None)
                if to_couting:
                   self.save_to_json(c)

        for k in key_to_remove:
            self.track_history.pop(k, None)

        logging.info(f'Total: {self.total_cicle}')

    def save_to_json(self, ciclist):
        
        logging.debug(f'ID: {ciclist.id} Saving ciclist!')
        date = datetime.now()
        c = {
            "ID":ciclist.id,
            "data":date.strftime('%Y-%m-%d'),
            "horario":date.strftime('%H:%M:%S'),
            "estado":"PR",
            "cidade":"Curitiba",
            "direcaoInicial":ciclist.start_direction,
            "direcaoFinal":ciclist.end_direction,
            # "coordenadas":{
            #         "latitude":self.latitude,
            #         "longitude":self.longitude
            #     }
            }

        with open(os.path.join(CICLIST_FILES, f'{str(int(time.time()))}.json'), 'w') as ciclist_file:
            json.dump(c, ciclist_file, indent=4)
