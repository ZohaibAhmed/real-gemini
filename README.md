<h1 align="center">Real Gemini</h1>

<p align="center">
  <strong>Google's Gemini implemented with GPT-4 Vision, Whisper and Resemble AI</strong>
</p>
<p align="center">
  This project leverages the power of AI to answer questions based on visual inputs -- like Google's Gemini demo. It integrates GPT-4 Vision for image understanding, Whisper for voice recognition, and Resemble AI for voice synthesis, creating a comprehensive system capable of interpreting visual data and responding verbally.
</p>

<div align="center">
  <img src="https://github.com/OthersideAI/self-operating-computer/blob/main/readme/self-operating-computer.png" width="750"  style="margin: 10px;"/>
</div>

## Features
- **Visual Question Answering**: Uses GPT-4 Vision to interpret images from a camera feed and answer questions related to the visual content.
- **Voice Recognition**: Employs Whisper for accurate speech-to-text conversion, allowing users to ask questions verbally.
- **Voice Synthesis**: Utilizes Resemble AI for generating realistic voice responses, enhancing the interactive experience.

## Prerequisites
- Python 3.x
- Camera hardware compatible with your system
- Microphone and speaker setup for voice input and output

## Installation
1. **Clone the Repository**
   ```bash
   git clone [your-repo-url]
   cd [your-repo-directory]
   ```

2. **Install Dependencies**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**
   - Create a `.env` file in the project root.
   - Add your Resemble AI and OpenAI credentials to the `.env` file:


## Usage
Run the application using the following command:
```bash
python run.py
```
Place the camera in view of the subject and use a microphone to ask questions. The system will process the visual and audio inputs to provide a spoken answer.

## Contributions
Contributions to this project are welcome. Please create a pull request with your proposed changes.

## Acknowledgements
Special thanks to OpenAI for GPT-4 and Whisper APIs, and to Resemble AI for their voice synthesis technology.

