import pickle
from mineCube.core.config import process_cube_extension

def save_cube(pc, path):
    file_with_extension = path + process_cube_extension
    metadata = {
        "dimensions": pc.dimensions,
        "date_column": pc.date_column,
        "activity_column": pc.activity_column,
        "case_id_column": pc.case_id_column,
        "time_freq": pc.time_freq,
        "csms": pc.csms,
        "cslms": pc.cslms,
        "models": pc.models,
        "groups_activities": pc.groups_activities,
        "cube": pc.cube
    }
    # Serialize and store the metadata using pickle
    with open(file_with_extension, 'wb') as file:
        pickle.dump(metadata, file)
