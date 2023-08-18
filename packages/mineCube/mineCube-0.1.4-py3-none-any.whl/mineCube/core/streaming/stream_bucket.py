import pandas as pd
from datetime import datetime
from mineCube.core.helpers.save_cube import save_cube


class StreamBucket:
    def __init__(self, window_size,columns,mc,save_path):
        self.window_size = window_size
        self.columns = columns
        self.data = pd.DataFrame(columns=columns)
        self.miniCube = mc
        self.save_path = save_path

    def add_data(self, data):
        self.data = self.data._append(pd.DataFrame([data],columns=self.columns),ignore_index=True)
        if len(self.data) >= self.window_size:
            self.process_data()

    def process_data(self):
        # Perform on-the-fly processing on the data in self.data
        # Store the results or do further analysis here
        # Reset self.data for the next bucket
        self.miniCube.set_data(self.data.copy())
        self.data.drop(index=self.data.index, inplace=True)
        self.miniCube.calculate_matrices()
        save_cube(self.miniCube, self.save_path+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("stream chunck stored and well processed !")
