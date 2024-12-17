from dotenv import load_dotenv
import os
import re
from pydub import AudioSegment
from openai import OpenAI

# Load API keys from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower() for text in _nsre.split(s)]

# Function to merge audio files
def merge_audio_files(audio_dir: str, output_file: str) -> None:
    audio_files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]
    audio_files.sort(key=natural_sort_key)

    combined_audio = AudioSegment.empty()
    for file in audio_files:
        audio_path = os.path.join(audio_dir, file)
        audio_segment = AudioSegment.from_file(audio_path)
        combined_audio += audio_segment
        print(f"Added: {file}")
    
    combined_audio.export(output_file, format="wav")
    print(f"Merged audio saved as: {output_file}")

# Function to transcribe audio with OpenAI API
def transcribe_audio_with_openai(audio_file: str) -> str:
    try:
        with open(audio_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=file
            )
        return transcription.text
    except Exception as e:
        print(f"An error occurred with OpenAI API: {e}")
        return ""

# Main script
if __name__ == "__main__":
    # Directory containing audio files
    audio_dir = "audio"
    merged_audio_path = "full-duration-output/merged_audio.wav"

    # Step 1: Merge all audio files
    merge_audio_files(audio_dir, merged_audio_path)

    # Step 2: Transcribe using OpenAI Whisper API
    print("Transcribing merged audio file...")
    transcription = transcribe_audio_with_openai(merged_audio_path)
    print("Transcription:")
    print(transcription)