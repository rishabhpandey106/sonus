import whisper
import srt
from datetime import timedelta
import torch
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import time

load_dotenv()

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# for model in genai.list_models():
#         print(model)
model = genai.GenerativeModel('models/gemini-2.0-flash-lite')

def generate_srt(output_file):
    model = whisper.load_model("large").to(device) 
    result = model.transcribe(output_file, task="transcribe", initial_prompt="The audio is a conversation in Hindi and English.", fp16=(device == "cuda"))
    return result

def is_hindi(text):
    # Check for presence of Hindi/Devanagari characters
    return bool(re.search(r'[\u0900-\u097F]', text))

def translate_with_gemini(text):
    try:
        time.sleep(2)

        if not is_hindi(text):
            return text
        
        prompt = f"""
        If the given text is in Hindi (Devanagari script), convert it to **Romanized Hindi** (transliteration, not translation).
        If the text is already in **English**, **return it unchanged**.
        If the text is in **any other language**, **return it unchanged**.
        Do not translate, just **convert the script** from Devanagari to Romanized Hindi, keeping the meaning the same.
        Correct any minor spelling errors while translating. 
        Return only the processed text without any extra explanations, comments, or formatting.

        Example:
        1. Hindi Input: "हाथ देगा, कोल देगा, छत्री के"
        Output: "Haath de ga, kol de ga, chatri ke"
        2. English Input: "What is your name?"
        Output: "What is your name?"

        Text: {text}
        """

        response = model.generate_content(prompt)
        result_text = response.text.strip()
        if not result_text:
            return text
        return result_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def convert_to_srt(transcript):
    segments = transcript["segments"]
    subtitles = []
    for i,seg in enumerate(segments):
        start_time = timedelta(seconds=seg['start'])
        end_time = timedelta(seconds=seg['end'])
        original_text = seg['text'].strip()
        translated_text = translate_with_gemini(original_text)
        subtitles.append(srt.Subtitle(
            index=i+1,
            start=start_time,
            end=end_time,
            content=translated_text
        ))
    return srt.compose(subtitles)

if __name__ == "__main__":
    output_file = "audio/sample.wav"
    transcript = generate_srt(output_file)
    srt_file = convert_to_srt(transcript)
    with open("transcript/sample1.srt", "w", encoding="utf-8") as f:
        f.write(srt_file)
    print("SRT file generated successfully.")