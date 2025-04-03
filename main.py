import streamlit as st
import os
import subprocess
from moviepy.editor import VideoFileClip
import whisper
import srt
from datetime import timedelta
import torch
import google.generativeai as genai
from dotenv import load_dotenv
import time
# import nest_asyncio
# nest_asyncio.apply()
import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import threading
import concurrent.futures

# Load environment variables
load_dotenv()

device = "cuda" if torch.cuda.is_available() else "cpu"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('models/gemini-2.0-flash-lite')

def extract_audio(video_path, audio_path):
    try:
        audio_dir = os.path.dirname(audio_path)
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)  

        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio

        if audio_clip:
            audio_clip.write_audiofile(audio_path)
            return True
        return False
    except Exception as e:
        print(f"An error occurred while extracting audio: {e}")
        return False

def transcribe_audio(audio_path):
    whisper_model = whisper.load_model("base").to(device)

    result = [None]  # Store result in a mutable list

    def run():
        result[0] = whisper_model.transcribe(audio_path, task="transcribe", initial_prompt="The audio is a conversation in Hindi and English.", fp16=(device == "cuda"))

    thread = threading.Thread(target=run)
    thread.start()
    thread.join()

    return result[0]

# def transcribe_audio(audio_path):
#     whisper_model = whisper.load_model("large").to(device)
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(
#         whisper_model.transcribe(audio_path, task="transcribe", initial_prompt="The audio is a conversation in Hindi and English.", fp16=(device == "cuda"))
#     )
#     return result

async def translate_with_gemini(text):
    try:
        time.sleep(2)  # Adding a delay to avoid rate limiting
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

        response = await model.generate_content(prompt)  # ✅ Await the async function

        if response and hasattr(response, 'text') and response.text:
            return response.text.strip()  # ✅ Ensure we never return None
        return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return text

def generate_srt(transcript):
    segments = transcript["segments"]
    subtitles = []
    for i, seg in enumerate(segments):
        start_time = timedelta(seconds=seg['start'])
        end_time = timedelta(seconds=seg['end'])
        original_text = seg['text'].strip()
        translated_text = asyncio.run(translate_with_gemini(original_text))
        if not translated_text:
            translated_text = original_text or "..."

        subtitles.append(srt.Subtitle(
            index=i+1,
            start=start_time,
            end=end_time,
            content=str(translated_text)
        ))
    return srt.compose(subtitles)

def burn_subtitles(video_path, srt_path, output_path):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    ffmpeg_cmd = f'ffmpeg -i "{video_path}" -vf "subtitles={srt_path}" -c:v libx264 -c:a aac "{output_path}"'
    subprocess.run(ffmpeg_cmd, shell=True, check=True)

st.title("Video Captioning Tool")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi"])

if uploaded_file:
    video_path = f"video/{uploaded_file.name}"
    audio_path = f"audio/{os.path.splitext(uploaded_file.name)[0]}.wav"
    srt_path = f"transcript/{os.path.splitext(uploaded_file.name)[0]}.srt"
    output_video_path = f"output/{os.path.splitext(uploaded_file.name)[0]}_subtitled.mp4"
    
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.video(video_path)
    
    if st.button("Extract Audio"):
        if extract_audio(video_path, audio_path):
            st.success("Audio extracted successfully!")
    
    if st.button("Generate Subtitles"):
        transcript = transcribe_audio(audio_path)
        srt_content = generate_srt(transcript)
        srt_dir = os.path.dirname(srt_path)
        if not os.path.exists(srt_dir):
            os.makedirs(srt_dir)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        st.success("Subtitles generated successfully!")
    
    if os.path.exists(srt_path):
        with open(srt_path, "r", encoding="utf-8") as f:
            srt_text = f.read()
        srt_text = st.text_area("Edit Subtitles", srt_text, height=300)
        if st.button("Save Changes"):
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_text.strip())
            st.success("Subtitles saved successfully!")
    
    if st.button("Burn Subtitles into Video"):
        burn_subtitles(video_path, srt_path, output_video_path)
        st.success("Subtitles burned successfully!")
        st.video(output_video_path)
