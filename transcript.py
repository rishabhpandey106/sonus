import whisper
import os

def transcribe_audio(file_path):
    model = whisper.load_model("large")
    result = model.transcribe(file_path)
    return result   

if __name__ == "__main__":
    audio_file = "audio/sample.wav"
    transcript = transcribe_audio(audio_file)
    print(transcript["text"])
