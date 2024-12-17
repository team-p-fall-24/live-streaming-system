import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load API keys from the .env file
load_dotenv()
xl8_api_key = os.getenv("XL8_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Check API keys
if not xl8_api_key or not openai_api_key:
    raise ValueError("API keys not found. Please check your .env file.")

# XL8 Translation Function
def translate_with_xl8(input_text: str, source_language: str, target_language: str) -> str:
    url = 'https://api.xl8.ai/v1/trans/request/rt'
    headers = {
        'Authorization': f'Bearer {xl8_api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        "source_language": source_language,
        "target_language": target_language,
        "sentences": [input_text],
        "options": {"formality": ["HAEYO"]}
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get('sentences', [''])[0]
    except Exception as e:
        print(f"XL8 Error: {e}")
        return ""

# OpenAI Translation Function
def translate_with_openai(input_text: str, source_language: str, target_language: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a translator converting the transcript of video from {source_language} to {target_language}. Ensure correctness of translation. Output only the translated text. vi: Vietnamese, ko: Korean, th: Thai"},
                {"role": "user", "content": f"Translate this transcript text: '{input_text}'. Output only the translated text."},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return ""

# Function to Process and Translate a Single File
def process_single_file(input_file: str, output_folder_xl8: str, output_folder_openai: str,
                        source_language: str, target_language: str):
    # Create output folders if they don't exist
    os.makedirs(output_folder_xl8, exist_ok=True)
    os.makedirs(output_folder_openai, exist_ok=True)

    # Read input file content
    with open(input_file, "r", encoding="utf-8") as file:
        input_text = file.read().strip()

    # Translate with XL8
    xl8_translation = translate_with_xl8(input_text, source_language, target_language)
    xl8_output_path = os.path.join(output_folder_xl8, os.path.basename(input_file))
    with open(xl8_output_path, "w", encoding="utf-8") as file:
        file.write(xl8_translation)

    # Translate with OpenAI
    openai_translation = translate_with_openai(input_text, source_language, target_language)
    openai_output_path = os.path.join(output_folder_openai, os.path.basename(input_file))
    with open(openai_output_path, "w", encoding="utf-8") as file:
        file.write(openai_translation)

    print(f"Translated '{input_file}' -> Saved to XL8 and OpenAI folders.")

# Main Execution
if __name__ == "__main__":
    input_file = "full-duration-output/full_subtitle.txt"  # Full subtitle file
    output_folder_xl8 = "full-duration-output/translate-xl8-th"  # Folder to save XL8 translations
    output_folder_openai = "full-duration-output/translate-openai-th"  # Folder to save OpenAI translations
    source_language = "ko"  # Source language (Korean)
    target_language = "th"  # Target language (Vietnamese)

    # Translate and save the file
    process_single_file(input_file, output_folder_xl8, output_folder_openai, source_language, target_language)
    print("Translation completed for the full subtitle file!")