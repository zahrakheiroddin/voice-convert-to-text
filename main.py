import speech_recognition as sr
import numpy as np
import soundfile as sf
import sqlite3
import os
import threading

# Create SQLite database and users table if it doesn't exist
def create_database():
    os.makedirs("database", exist_ok=True)  # Ensure the database directory exists
    conn = sqlite3.connect('database/voice_recognition.db')  # Connect to the database
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            audio_data BLOB
        )
    ''')
    conn.commit()  # Save changes
    conn.close()  # Close the connection

# Function to record audio, analyze it, and transcribe the speech
def record_audio(name):
    recognizer = sr.Recognizer()
    audio_frames = []  # List to hold recorded audio frames

    # Function to listen to the microphone input
    def listen():
        with sr.Microphone() as source:
            print("Recording... Press Enter to stop.")
            while True:
                audio = recognizer.listen(source)
                audio_frames.append(audio)  # Store the AudioData object directly

    # Start the audio recording in a separate thread
    listener_thread = threading.Thread(target=listen)
    listener_thread.start()

    # Wait for user to press Enter to stop recording
    input()  

    # Stop the recording thread
    listener_thread.join(timeout=1)  # Wait for the thread to finish

    # Combine all audio frames into one AudioData object
    combined_audio = sr.AudioData(
        b''.join([frame.get_raw_data() for frame in audio_frames]), 
        sample_rate=44100, 
        sample_width=2  # Assuming 16-bit audio (2 bytes)
    )

    # Convert audio frames to numpy array for analysis
    audio_data = np.frombuffer(b''.join([frame.get_raw_data() for frame in audio_frames]), dtype=np.int16)
    os.makedirs("voice_data", exist_ok=True)  # Ensure voice data directory exists
    sf.write(f"voice_data/{name}.wav", audio_data, 44100)  # Save audio as a WAV file
    
    # Frequency analysis using FFT
    frequencies = np.fft.fftfreq(len(audio_data), 1 / 44100)
    fft_magnitude = np.abs(np.fft.fft(audio_data))

    # Get the top 5 dominant frequencies
    dominant_freq_indices = np.argsort(fft_magnitude)[-5:]  # Get the indices of the top frequencies
    dominant_frequencies = frequencies[dominant_freq_indices]

    # Transcribe audio to text using Google Speech Recognition
    try:
        transcription = recognizer.recognize_google(combined_audio)  # Use the combined audio for transcription
    except sr.UnknownValueError:
        transcription = "Could not understand audio. Please try again."
    except sr.RequestError as e:
        transcription = f"Could not request results from Google Speech Recognition service; {e}"

    # Save the dominant frequencies and transcription to a .txt file
    with open(f"voice_data/{name}_analysis.txt", "w") as analysis_file:
        analysis_file.write("Dominant frequencies (Hz):\n")
        for freq in dominant_frequencies:
            analysis_file.write(f"{freq:.2f}\n")
        analysis_file.write("\nTranscription:\n")
        analysis_file.write(transcription + "\n")

    # Print the results to the console
    print("\nAnalysis complete!")
    print("Dominant frequencies in the recording are:", dominant_frequencies)
    print("Transcription of the audio is:", transcription)
    return audio_data

# Function to store the recorded audio data in the database
def store_audio(name, audio_data):
    conn = sqlite3.connect('database/voice_recognition.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, audio_data) VALUES (?, ?)', (name, audio_data.tobytes()))
    conn.commit()  # Save changes
    conn.close()  # Close the connection
    print(f"Audio data for '{name}' stored successfully.")

# Function to display recorded voice names and open corresponding analysis files
def show_recorded_names():
    conn = sqlite3.connect('database/voice_recognition.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users')
    names = cursor.fetchall()
    conn.close()

    if names:
        print("\nRecorded voices:")
        for name in names:
            print(f"- {name[0]}")  # Print each recorded name with a bullet point
        
        # Prompt user to enter a filename
        selected_name = input("Please enter the name of the voice file you want to open (without extension): ")
        analysis_file_path = f"voice_data/{selected_name}_analysis.txt"
        
        # Check if the corresponding analysis file exists
        if os.path.exists(analysis_file_path):
            with open(analysis_file_path, "r") as analysis_file:
                print("\nContents of the analysis file:")
                print(analysis_file.read())
        else:
            print(f"No analysis file found for '{selected_name}'.")
    else:
        print("No voices recorded yet.")

# Main function to run the program
def main():
    create_database()  # Create the database if it doesn't exist
    while True:
        print("\nMenu:")
        print("1. Record voice and save it with frequency analysis")
        print("2. Show names of recorded voices")
        print("3. Exit")

        choice = input("Please select an option (1-3): ")

        if choice == '1':
            name = input("Please enter your name: ")
            audio_data = record_audio(name)  # Record audio and get frequency information

            if audio_data is not None:
                store_audio(name, audio_data)  # Store the audio data in the database

        elif choice == '2':
            show_recorded_names()  # Show names of recorded voices

        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break  # Exit the loop

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
