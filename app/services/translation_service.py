import os
import re
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

def split_sentences(text, lang="default"):
    """
    Split text into sentences using punctuation-based splitting for default languages.
    For Thai, split using spaces but ensure a minimum of 10 characters per segment.
    """
    if lang == "th":
        words = text.split()
        sentences = []
        current_sentence = []
        current_length = 0

        for word in words:
            current_sentence.append(word)
            current_length += len(word)
            if current_length >= 10:
                sentences.append(" ".join(current_sentence))
                current_sentence = []
                current_length = 0

        if current_sentence:  # Add any remaining words as the last sentence
            sentences.append(" ".join(current_sentence))
        return sentences
    else:
        sentence_endings = re.compile(r'(.*?[.!?])\s+')
        sentences = sentence_endings.findall(text + ' ')
        if text and text[-1] not in '.!?':
            sentences.append(text)  # Add the last sentence if no punctuation
        return [s.strip() for s in sentences if s.strip()]

def calculate_time_intervals(sentences, start_time_offset, chunk_duration):
    """
    Calculate start and end times proportionally based on sentence length,
    with an initial time offset.
    """
    total_length = sum(len(s) for s in sentences)
    time_intervals = []
    current_time = start_time_offset
    
    for sentence in sentences:
        proportion = len(sentence) / total_length
        duration = proportion * chunk_duration
        start_time = current_time
        end_time = current_time + duration
        time_intervals.append((start_time, end_time, sentence))
        current_time = end_time
    return time_intervals

def format_time(seconds):
    """Format time in H:MM:SS.mmm format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

def translate_file(input_file: str, source_language: str = "ko", target_languages: list = ["vi", "th"], formality: str = "HAEYO") -> None:
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
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        try:
            index = int(base_name.split('_')[1])
            print(f"Translating chunk {index} to {lang}")
        except (IndexError, ValueError):
            index = 0

        start_time_offset = index * CHUNK_DURATION
        chunk_duration = CHUNK_DURATION
        sentences = split_sentences(translation, lang=lang)
        time_intervals = calculate_time_intervals(sentences, start_time_offset, chunk_duration)

        vtt_content = "WEBVTT\n\n"
        for start, end, sentence in time_intervals:
            vtt_content += f"{format_time(start)} --> {format_time(end)}\n"
            vtt_content += f"{sentence}\n\n"

        output_file = os.path.join(
            TRANSLATION_OUTPUT,
            f"{lang}/{base_name}.vtt"
        )
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        try:
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(vtt_content)
            print(f"Translation saved to {output_file}")
        except IOError as e:
            print(f"Error writing to file {output_file}: {e}")

