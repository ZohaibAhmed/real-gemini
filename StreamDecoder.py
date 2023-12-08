STREAMING_WAV_HEADER_BUFFER_LEN = 36
READ_MODE_FORMAT = "FORMAT"
READ_MODE_DATA = "DATA"

import struct

class StreamDecoder():
    def __init__(self, buffer_size, ignore_wav_header):
        if buffer_size < 8:
            raise ValueError("Buffer size cannot be less than 8")

        if buffer_size % 2 != 0:
            raise ValueError("Buffer size must be evenly divisible by 2.")

        self.buffer_size = buffer_size
        self.ignore_wav_header = ignore_wav_header
        self.header_buffer = bytearray()
        self.intermediary_buffer = bytearray()
        self.audio_buffer = bytearray()

        self.read_mode = READ_MODE_FORMAT
        self.rem_size = -1
        self.currently_read = 0

    def decode_chunk(self, chunk):
        if len(self.header_buffer) < STREAMING_WAV_HEADER_BUFFER_LEN and self.ignore_wav_header:
            self.header_buffer.extend(chunk)
            if len(self.header_buffer) >= STREAMING_WAV_HEADER_BUFFER_LEN:
                self.intermediary_buffer = self.header_buffer[STREAMING_WAV_HEADER_BUFFER_LEN:]
                self.header_buffer = self.header_buffer[0:STREAMING_WAV_HEADER_BUFFER_LEN]
        else:
            if self.read_mode == READ_MODE_FORMAT:
                self.intermediary_buffer.extend(chunk)
                # Parse out the FORMAT header
                if self.rem_size == -1 and len(self.intermediary_buffer) >= 8:
                    to_unpack = self.intermediary_buffer[0:8]
                    self.intermediary_buffer = self.intermediary_buffer[8:]
                    chunk_type, rem_size = struct.unpack("<4sL", to_unpack)
                    if chunk_type != b"data":
                        self.rem_size = rem_size
                    else:
                        # We've hit the data attribute, go to data read mode to read audio
                        self.read_mode = READ_MODE_DATA
                        self.audio_buffer.extend(self.intermediary_buffer)
                elif self.currently_read <= self.rem_size:
                    # Discard the data coming in until rem_size is hit
                    self.currently_read += len(chunk)
                    if self.currently_read >= self.rem_size:
                        # Make an in-place copy of the intermediary buffer just incase we need it
                        temp_intermediary_buffer = self.intermediary_buffer[0:]

                        # clear the buffer as we're discarding all the data
                        self.intermediary_buffer = bytearray()

                        # Sometimes the server doesn't send bytes of size 2 but instead will send a byte of size 1
                        # This may increment the currently_read counter past the rem size, we should
                        # make sure to add this data to the intermediary_buffer for future processing
                        if self.currently_read > self.rem_size:
                            self.intermediary_buffer = temp_intermediary_buffer[self.rem_size:]

                        # we've read all the data up to the specified rem_size, reset some counters
                        self.rem_size = -1
                        self.currently_read = 0

            elif self.read_mode == READ_MODE_DATA:
                self.audio_buffer.extend(chunk)
            else:
                raise Exception(f"Read mode is in an invalid state, state: {self.read_mode}")


    def flush_buffer(self, force=False):
        if force:
            return_buffer = self.audio_buffer[0:]
            self.audio_buffer = []
            return return_buffer
        if len(self.audio_buffer) >= self.buffer_size:
            # only get the request buffer size from the stored buffer
            return_buffer = self.audio_buffer[0:self.buffer_size]
            # This removes the current buffer being returned from the stored buffer
            self.audio_buffer = self.audio_buffer[self.buffer_size:]
            return return_buffer
        return None

    @staticmethod
    def byte_to_int(bytes):
        return int.from_bytes(bytes, byteorder='little')
