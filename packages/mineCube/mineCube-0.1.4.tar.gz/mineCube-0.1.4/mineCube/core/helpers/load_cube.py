import pickle
from mineCube.core.offline.process_cube import ProcessCube


def load_cube(path):
    # Deserialize and load the metadata using pickle
    metadata = {}
    with open(path, 'rb') as file:
        metadata = pickle.load(file)
    print("Process cube loaded successfully !!" )
    return ProcessCube(metadata['cube'], metadata['dimensions'], metadata['date_column'], metadata['activity_column'],
                       metadata['case_id_column'],cube=metadata['cube'],cslms=metadata['cslms'],csms=metadata['csms'],models=metadata['models'],groups_activities=metadata['groups_activities'], time_freq=metadata['time_freq'], loaded=True)
