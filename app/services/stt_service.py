import os
from dotenv import load_dotenv
from openai import OpenAI

# Load the OPENAI_API_KEY from the .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path, override=True)
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

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


# Testing the function
if __name__ == "__main__":
    audio_file_path = "audio.wav" # .wav file path to transcribe
    transcription_text = transcribe_audio_with_openai(audio_file_path)
    if transcription_text:
        print(transcription_text)