from flask import Flask, jsonify, request ,render_template
from flask_cors import CORS
from datetime import datetime
from mineCube.core.helpers.mixed_cube import MixedCube


app = Flask(__name__,static_url_path="/static")
CORS(app)
loader = None
pc = None


@app.route('/')
def index():
    return render_template('index.html')

# Custom function to extract the datetime from the filename
def get_datetime_from_filename(filename):
    # Split the filename and extract the date-time part
    date_time_str = filename.split(".")[0]

    # Convert the date-time string to a datetime object
    return datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")



@app.route('/get_model', methods=['POST'])
def get_model():
    # Get data from the frontend request
    data = request.json

    # Extract the required parameters
    positive_observations = data.get('positive_observations')
    dependency_threshold = data.get('dependency_threshold')
    contribution_factor = data.get('contribution_factor')
    current_batch = data.get('current_batch')
    mincubes = sorted(loader.get_mini_cubes_names(), key=get_datetime_from_filename)
    if not current_batch :
        current_batch = len(mincubes)-1
    mc = loader.get_mini_cube(mincubes[current_batch])
    mix = MixedCube(pc,mc,contribution_factor=contribution_factor)
    mix.merge()
    mix.mine(algo="HM",positive_observations=positive_observations,dependency_threshold=dependency_threshold)
    # Create a dictionary to hold the response data
    response = {
        "models": mix.models,
        'current_batch':current_batch,
        "activities":  list(mix.offline_cube.get_unique_activities())
    }

    # Return the response as JSON
    return jsonify(response)


def start_web_ui(_pc,_loader):
    global loader
    global pc
    loader = _loader
    pc = _pc
    app.run(debug=True, port=4000)
