import whisper
import srt
from datetime import timedelta

def generate_srt(output_file):
    model = whisper.load_model("large")
    result = model.transcribe(output_file, language="hi")
    return result

def convert_to_srt(transcript):
    segements = transcript["segments"]
    subtitles = []
    for i,seg in enumerate(segements):
        subtitles.append(srt.Subtitle(index=i+1,
                                      start=timedelta(seconds=seg["start"]),
                                      end=timedelta(seconds=seg["end"]),
                                      content=seg["text"].strip()))
    return srt.compose(subtitles)

if __name__ == "__main__":
    output_file = "audio/sample.wav"
    transcript = generate_srt(output_file)
    srt_file = convert_to_srt(transcript)
    with open("transcript/sample.srt", "w", encoding="utf-8") as f:
        f.write(srt_file)
    print("SRT file generated successfully.")