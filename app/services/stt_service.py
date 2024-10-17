import openai

def transcribe_audio_with_openai(audio_file: str):
    try:
        # Load audio data.
        with open(audio_file, "rb") as audio:
            # Send request to (OpenAI's) Whisper API
            transcription = openai.Audio.transcribe(
                model="whisper-1",  # Whisper, of OpenAI.
                file=audio,
                response_format="text"
            )
            return transcription
    except Exception as e:
        print(f"Error in transcription: {e}")
        return None