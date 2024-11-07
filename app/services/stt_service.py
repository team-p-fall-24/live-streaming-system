import openai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to transcribe audio using OpenAI's Whisper API
def transcribe_audio_with_openai(audio_file: str) -> str:
    try:
        with open(audio_file, "rb") as audio:
            print(f"Transcribing the {audio_file}...")
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio,
                response_format="text"
            )
            print(f"Transcription successful for the {audio_file}")
            return transcription
    except openai.error.OpenAIError as oe:
        print(f"OpenAI API error in transcription: {oe}")
        return None
    except FileNotFoundError:
        print(f"File not found: {audio_file}")
        return None
    except IOError as ioe:
        print(f"I/O error when handling {audio_file}: {ioe}")
        return None
    except Exception as e:
        print(f"Unexpected error in transcription: {e}")
        return None
