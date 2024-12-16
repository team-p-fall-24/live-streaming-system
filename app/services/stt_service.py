import os
import time
import torch
import whisper
import openai
from groq import Groq
from dotenv import load_dotenv
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

# Function to transcribe audio file with fallback to Groq after 3 OpenAI failures
def transcribe_audio(audio_file_path: str):
    """Transcribe a wav audio file to text and save to the file, with fallback to Groq"""
    max_retries = 3
    retries = 0
    transcription_text = ""

    # Ensure the audio file exists
    if not os.path.exists(audio_file_path):
        print(f"Audio file does not exist: {audio_file_path}")
        return

    # Try transcribing with OpenAI API
    while retries < max_retries:
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", file=audio_file
                )
            transcription_text = transcription.text or " "
            print("Extract text: ", transcription_text)
            break
        except openai.OpenAIError as e:
            retries += 1
            print(f"OpenAI API error (attempt {retries}) during transcription of {audio_file_path}: {e}")
        except Exception as e:
            retries += 1
            print(f"Unexpected error (attempt {retries}) during transcription of {audio_file_path}: {e}")

    # If OpenAI fails after retries, fallback to Groq
    if retries == max_retries:
        print("Falling back to Groq API for transcription.")
        transcription_text = transcribe_audio_with_groq(audio_file_path)

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
    