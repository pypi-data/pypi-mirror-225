from mineCube.core.streaming.stream_bucket import StreamBucket
class StreamProcessor:
    def __init__(self, window_size,columns,mc,save_path):
        self.bucket = StreamBucket(window_size,columns,mc,save_path)
        self.miniCube = mc

    def process_stream_data(self, data):
        # Parse the incoming data from the stream
        data_fields = data.decode('utf-8').split(',')  # Convert bytes to str and split by commas
        self.bucket.add_data(data_fields)
