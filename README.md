# Voice Recognition & Frequency Analysis Program

This Python-based program allows users to record audio, perform frequency analysis, transcribe speech, and store the data in a SQLite database. The program also provides an interface to view recorded voices and their frequency analysis results.

## Features
- **Audio Recording**: Captures audio via microphone input.
- **Frequency Analysis**: Uses Fast Fourier Transform (FFT) to determine the top 5 dominant frequencies.
- **Speech Transcription**: Converts recorded speech to text using Google Speech Recognition.
- **Database Storage**: Saves audio data and user information in a SQLite database.
- **Data Retrieval**: Displays stored recordings and allows users to view corresponding frequency analysis and transcription.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x
- Required packages:
  - `speech_recognition`
  - `numpy`
  - `soundfile`
  - `sqlite3` (built-in with Python)
  - `os` (built-in with Python)
  - `threading` (built-in with Python)

Install the required packages with:
```bash
pip install SpeechRecognition numpy soundfile
```

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/voice-recognition-frequency-analysis.git
   cd voice-recognition-frequency-analysis
   ```
   
2. **Create Database**: When you run the program for the first time, it will automatically create a SQLite database and the necessary table to store user data.

3. **Run the Program**:
   ```bash
   python main.py
   ```

## Usage
1. **Recording and Analyzing Audio**:
   - Select option **1** in the menu.
   - Enter a name for the recording.
   - Press **Enter** when ready to stop recording.
   - The program will save a `.wav` file of the recording, perform frequency analysis, and transcribe the audio to text.

2. **Viewing Stored Recordings**:
   - Select option **2** in the menu to view all recorded voices.
   - Enter the name of a recording to view its frequency analysis and transcription.

3. **Exit the Program**:
   - Select option **3** in the menu.

## Project Structure
```
├── main.py                   # Main program file
├── README.md                 # Documentation file
├── database/
│   └── voice_recognition.db  # SQLite database (auto-generated)
├── voice_data/               # Directory for recorded .wav files and analysis (auto-generated)
└── requirements.txt          # List of dependencies
```

## Example
After running the program and recording a voice, the output might look like:
```
Menu:
1. Record voice and save it with frequency analysis
2. Show names of recorded voices
3. Exit

Please select an option (1-3): 1
Please enter your name: John
Recording... Press Enter to stop.

Analysis complete!
Dominant frequencies in the recording are: [100.00, 200.00, 300.00, 400.00, 500.00]
Transcription of the audio is: Hello, this is a test recording.
Audio data for 'John' stored successfully.
```

## Troubleshooting
- Ensure your microphone is connected and working.
- You may encounter limitations with Google Speech Recognition for complex audio; verify your internet connection for transcription.

## License
This project is licensed under the MIT License.

## Acknowledgements
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- [Numpy](https://numpy.org/)
- [Soundfile](https://pypi.org/project/SoundFile/)

