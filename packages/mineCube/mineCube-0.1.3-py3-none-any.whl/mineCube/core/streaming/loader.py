import pickle
from mineCube.core.streaming.mini_cube import  MiniCube
from mineCube.core.offline.process_cube import ProcessCube
import pandas as pd
import os

class MiniCubesLoader:
    def __init__(self,folder_path):
        self.folder_path = folder_path

    def get_mini_cube(self,file_name):
        metadata = {}
        with open(self.folder_path+file_name, 'rb') as file:
            metadata = pickle.load(file)
        return MiniCube(metadata['dimensions'], metadata['date_column'],
                           metadata['activity_column'],
                           metadata['case_id_column'],cube=metadata['cube'],data=metadata['cube'], cslms=metadata['cslms'], csms=metadata['csms'],
                           models=metadata['models'], groups_activities=metadata['groups_activities'],
                           time_freq=metadata['time_freq'], loaded=True)

    def get_mini_cubes_names(self):
        files = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".pcube"):
                files.append(filename)
        return files