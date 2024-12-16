import os
import time
from dotenv import load_dotenv
import openai
from groq import Groq
import torch
import whisper

from app.variables import SUBTITLE_OUTPUT

# Load the OPENAI_API_KEY from the .env file
env_path = os.path.join(os.path.dirname(__file__), "../../.env")
load_dotenv(env_path, override=True)
api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

# Initialize the Groq client
groq_client = Groq(api_key=groq_api_key)

# Function to transcribe audio file using OpenAI API
def transcribe_audio(audio_file_path: str):
    """Transcribe a wav audio file to text and save to the file"""
    try:
        # Ensure the audio file exists
        if not os.path.exists(audio_file_path):
            print(f"Audio file does not exist: {audio_file_path}")
            return

        # Open the audio file in binary mode
        with open(audio_file_path, "rb") as audio_file:
            # Send the audio file to OpenAI's Whisper API
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file
            )

        # Extract the transcription text
        transcription_text = transcription.text
        if not transcription_text:
            transcription_text = " "
        print("Extract text ", transcription_text)
        

    except openai.OpenAIError as e:
        # Handle errors from the OpenAI API
        print(f"OpenAI API error during transcription of {audio_file_path}: {e}")
        transcription_text = f"Error: {e}"

    except Exception as e:
        # Handle any other exceptions
        print(f"Unexpected error during transcription of {audio_file_path}: {e}")
        transcription_text = f"Error: {e}"

    finally:
        # Define the transcription file path
        transcription_file_path = (
            f"{SUBTITLE_OUTPUT}/{os.path.splitext(os.path.basename(audio_file_path))[0]}.txt"
        )

        # Save the transcription to a .txt file
        with open(transcription_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(transcription_text.strip())

# Additional functions to support the STT services for other use cases
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

    except openai.OpenAIError as e:
        # Handle errors from the OpenAI API
        print(f"OpenAI API error during transcription of {audio_file_path}: {e}")
        transcription_text = f"Error: {e}"

    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
