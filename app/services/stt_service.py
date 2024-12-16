import os
import time
import whisper
import torch
import warnings
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq

# Ignore the warning when using CPU
warnings.filterwarnings("ignore", message="You are using `torch.load` with `weights_only=False`")

# Load the OPENAI_API_KEY from the .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path, override=True)
api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Initialize the Groq client
groq_client = Groq(api_key=groq_api_key)

# Function to transcribe an audio file using OpenAI API with the whisper large model
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

# Function to transcribe an audio file using Groq API with the whisper large model
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
    
# Function to transcribe an audio file using Whisper model running locally
def transcribe_audio_with_whisper_local(audio_file: str) -> str:
    try:
        # Check for CUDA availability, otherwise fallback to CPU
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        # Load the Whisper large model - turbo version is optimized for speed
        model = whisper.load_model("turbo", device=device)

        # Perform transcription
        if(device == "cpu"):
            result = model.transcribe(audio_file, fp16=False)
        else:
            result = model.transcribe(audio_file, fp16=True)
        return result["text"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Testing the function
if __name__ == "__main__":
    audio_file_path = "../media/example-usage/audio_input.wav" # .wav file path to transcribe
    
    # Measure time for OpenAI transcription
    try:
        start_time = time.time()
        transcription_text = transcribe_audio_with_openai(audio_file_path)
        openai_duration = time.time() - start_time
        if transcription_text:
            print(f"OpenAI Transcription: {transcription_text}")
        print(f"OpenAI Transcription Time: {openai_duration:.2f} seconds")
    except Exception as e:
        print(f"OpenAI Transcription Error: {e}")

    # Measure time for Groq transcription
    try:
        start_time = time.time()
        transcription_text_groq = transcribe_audio_with_groq(audio_file_path)
        groq_duration = time.time() - start_time
        if transcription_text_groq:
            print(f"Groq Transcription: {transcription_text_groq}")
        print(f"Groq Transcription Time: {groq_duration:.2f} seconds")
    except Exception as e:
        print(f"Groq Transcription Error: {e}")

    # Measure time for Whisper local transcription
    try:
        start_time = time.time()
        transcription_text_whisper_local = transcribe_audio_with_whisper_local(audio_file_path)
        whisper_local_duration = time.time() - start_time
        if transcription_text_whisper_local:
            print(f"Whisper Local Transcription: {transcription_text_whisper_local}")
        print(f"Whisper Local Transcription Time: {whisper_local_duration:.2f} seconds")
    except Exception as e:
        print(f"Whisper Local Transcription Error: {e}")
