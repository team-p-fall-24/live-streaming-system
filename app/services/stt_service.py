import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

# Load the OPENAI_API_KEY from the .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path, override=True)
api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Initialize the Groq client
groq_client = Groq(api_key=groq_api_key)

# Function to transcribe an audio file using OpenAI API with the whisper-1 model
def transcribe_audio_with_openai(audio_file: str) -> str:
    try:
        with open(audio_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=file
            )
        return transcription.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Function to transcribe an audio file using Groq API with the whisper-large-v3-turbo model
def transcribe_audio_with_groq(audio_file: str) -> str:
    try:
        with open(audio_file, "rb") as file:
            transcription = groq_client.audio.transcriptions.create(
                file=(audio_file, file.read()),
                model="whisper-large-v3-turbo",
                response_format="verbose_json",
            )
        return transcription.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Testing the function
if __name__ == "__main__":
    audio_file_path = "audio.wav" # .wav file path to transcribe
    
    # Measure time for OpenAI transcription
    start_time = time.time()
    transcription_text = transcribe_audio_with_openai(audio_file_path)
    end_time = time.time()
    openai_duration = end_time - start_time
    if transcription_text:
        print(f"OpenAI Transcription: {transcription_text}")
    print(f"OpenAI Transcription Time: {openai_duration} seconds")
    
    # Measure time for Groq transcription
    audio_file_path_groq = "audio.wav" # .m4a file path to transcribe
    start_time = time.time()
    transcription_text_groq = transcribe_audio_with_groq(audio_file_path_groq)
    end_time = time.time()
    groq_duration = end_time - start_time
    if transcription_text_groq:
        print(f"Groq Transcription: {transcription_text_groq}")
    print(f"Groq Transcription Time: {groq_duration} seconds")