import os
import requests
import json
from dotenv import load_dotenv

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

# Example of usage and testing the translation service
if __name__ == "__main__":
    # Read input text from a file
    input_file = "../media/example-usage/translation_input.txt"
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            input_text = file.read().strip()
    except IOError as e:
        print(f"Error reading from file {input_file}: {e}")
        exit(1)
    
    source_language = "ko"
    target_languages = ["vi", "th"]  # Vietnamese and Thai
    
    # Get translations
    translations = translate_text(input_text, source_language=source_language, target_languages=target_languages)
    
    # Print the translations to the console
    for lang, translation in translations.items():
        print(f"{lang}: {translation}")
    
    # Save translations to a file
    output_file = "../media/example-usage/translation_output.txt"
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            for lang, translation in translations.items():
                file.write(f"{lang}: {translation}\n")
        print(f"Translations saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}")