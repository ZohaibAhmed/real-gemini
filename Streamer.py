import requests
import os

from StreamDecoder import StreamDecoder

from dotenv import load_dotenv
load_dotenv()

DEFAULT_STREAM_ENDPOINT = os.environ.get("RESEMBLE_ENDPOINT")
DEFAULT_BUFFER_SIZE = 2 * 1024
CHUNK_SIZE = 2


class Streamer():

    def __init__(self, api_key: str, stream_endpoint: str = DEFAULT_STREAM_ENDPOINT):
        if api_key is None or len(api_key) <= 0:
            raise ValueError("api_key must be provided")

        self.api_key = api_key
        self.stream_endpoint = stream_endpoint

    def stream(self, project_uuid: str, voice_uuid: str, text: str, buffer_size=DEFAULT_BUFFER_SIZE,
               ignore_wav_header: bool = True):
        r = self.__post_streaming(project_uuid, voice_uuid, text)
        r.raise_for_status()
        stream_decoder = StreamDecoder(buffer_size, ignore_wav_header)

        # Iterate over the stream and start decoding, and returning data
        for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                stream_decoder.decode_chunk(chunk)
                buffer = stream_decoder.flush_buffer()
                if buffer:
                    yield buffer

        # Keep draining the buffer until the len(buffer) < buffer_size or len(buffer) == 0
        buffer = stream_decoder.flush_buffer()
        while buffer is not None:
            buff_to_return = buffer
            buffer = stream_decoder.flush_buffer()
            yield buff_to_return

        # Drain any leftover content in the buffer, len(buffer) will always be less than buffer_size here
        buffer = stream_decoder.flush_buffer(force=True)
        if buffer:
            yield buffer

    def __post_streaming(self, project_uuid: str, voice_uuid: str, text: str):
        headers = {"x-access-token": self.api_key}
        body = {
            "data": text,
            "project_uuid": project_uuid,
            "voice_uuid": voice_uuid,
            "sample_rate": 22050,
            "precision": 'PCM_16'
        }
        return requests.post(self.stream_endpoint, headers=headers, json=body, stream=True)
