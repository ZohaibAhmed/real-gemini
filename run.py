from whisper_mic import WhisperMic
import cv2
from openai import OpenAI
import base64
from Streamer import Streamer
import pyaudio
import numpy as np
import os

from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

mic = WhisperMic(pause=0.7)

while True:
    result = mic.listen()
    print(result)

    # Capture a single frame
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if ret:
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)
        # Save the captured image to a file
        cv2.imwrite('captured_image.jpg', rotated_frame)
    else:
        print("Error: Could not capture an image.")

    # Release the camera
    cap.release()

    # Open the image file in binary mode
    with open('captured_image.jpg', 'rb') as image_file:
        # Read the binary data
        binary_data = image_file.read()

        # Encode the binary data to Base64
        base64_encoded_data = base64.b64encode(binary_data)

        # Convert the Base64 bytes to string
        base64_string = base64_encoded_data.decode('utf-8')

    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": result + ". Be Concise."},
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_string}",
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )

    ai_resp = response.choices[0].message.content
    print("\033[92m" + ai_resp + "\033[0m")

    streamer = Streamer(os.environ.get("RESEMBLE_API_KEY"))

    printed_header = False

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=22050,
                    output=True)


    start = datetime.now()
    is_first = True

    ai_resp = ai_resp.replace("&", "and")
    ai_resp = ai_resp.replace("!", " ")

    for audio_chunk in streamer.stream(os.environ.get("RESEMBLE_PROJECT"), os.environ.get("RESEMBLE_VOICE"), ai_resp):
        if is_first:
            current_time = datetime.now()
            time_difference = current_time - start
            is_first = False

        audio = np.frombuffer(audio_chunk, np.int16)
        stream.write(bytes(audio_chunk))

    stream.stop_stream()
    stream.close()

    p.terminate()
