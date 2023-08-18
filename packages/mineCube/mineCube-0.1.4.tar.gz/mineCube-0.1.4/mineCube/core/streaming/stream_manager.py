from mineCube.core.streaming.stream_processor import StreamProcessor
import requests
import json
import pandas as pd
class StreamManager:
    def __init__(self, window_size, stream_url,data_header,mc,save_path="/exports/stream"):
        self.stream_processor = StreamProcessor(window_size,data_header,mc,save_path)
        self.stream_url = stream_url
        self.data_header = data_header
        self.is_streaming = False
        self.miniCube = mc

    def start_stream(self):
        # Start streaming data from self.stream_url
        # and call self.stream_processor.process_stream_data(data) for each incoming data
        if self.is_streaming:
            print("Stream is already running.")
            return

        self.is_streaming = True
        try:
            response = requests.get(self.stream_url, stream=True)

            for line in response.iter_lines():
                if not self.is_streaming:
                    break  # Stop processing the stream if stop_stream was called
                if line:
                    self.stream_processor.process_stream_data(line)

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while streaming: {e}")
        finally:
            self.stop_stream()

    def stop_stream(self):
        # Stop the streaming process
        self.is_streaming = False
