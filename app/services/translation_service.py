import os
import requests
import json
from dotenv import load_dotenv
from app.variables import TRANSLATION_OUTPUT, CHUNK_DURATION

# Load the XL8_API_KEY from the .env file
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path, override=True)
api_key = os.getenv("XL8_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please check your .env file.")

def translate_text(input_text: str, source_language: str = "ko", target_languages: list = ["vi", "th"], formality: str = "HAEYO") -> dict:
    """
    Translates text into one or more target languages using the XL8 API.

    Args:
        input_text (str): The text to translate.
        source_language (str): The source language code (default is "ko").
        target_languages (list): A list of target language codes.
        formality (str): Formality level for translation ("HAEYO" or others).

    Returns:
        dict: A dictionary with target languages as keys and their translations as values.
    """
    url = 'https://api.xl8.ai/v1/trans/request/rt'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    translations = {}
    
    for target_language in target_languages:
        # Prepare the request payload
        data = {
            "source_language": source_language,
            "target_language": target_language,
            "sentences": [input_text],
            "options": {"formality": [formality]}
        }
        
        try:
            # Send the POST request
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            
            # Process the response
            response_data = response.json()
            translated_sentences = response_data.get('sentences', [])
            if translated_sentences:
                translations[target_language] = translated_sentences[0]  # Fetch the first translated sentence
            else:
                print(f"Warning: No translation found for {target_language}")
                translations[target_language] = ""
        except requests.exceptions.RequestException as e:
            print(f"Error while translating to {target_language}: {e}")
            translations[target_language] = ""
    
    return translations

def translate_file(input_file: str, source_language: str = "ko", target_languages: list = ["vi", "th"], formality: str = "HAEYO") -> None:
    """
    Translates the content of a text file and saves the translations to .vtt files.

    Args:
        input_file (str): Path to the input text file.
        source_language (str): The source language code (default is "ko").
        target_languages (list): A list of target language codes.
        formality (str): Formality level for translation ("HAEYO" or others).
    """
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            input_text = file.read().strip()
    except IOError as e:
        print(f"Error reading from file {input_file}: {e}")
        return

    translations = translate_text(
        input_text,
        source_language=source_language,
        target_languages=target_languages,
        formality=formality
    )

    for lang, translation in translations.items():
        # Convert translation to WebVTT format
        vtt_content = "WEBVTT\n\n"
        vtt_content += f"00:00:00.000 --> 00:00:{CHUNK_DURATION:02d}.000\n"
        vtt_content += translation + "\n"

        output_file = os.path.join(
            TRANSLATION_OUTPUT,
            f"{lang}/{os.path.splitext(os.path.basename(input_file))[0]}.vtt"
        )
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(vtt_content)
            print(f"Translation saved to {output_file}")
        except IOError as e:
            print(f"Error writing to file {output_file}: {e}")

