from moviepy.editor import VideoFileClip
import os

def extract_audio_from_video(video_path, output_audio_path):
    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        if audio_clip:
            audio_clip.write_audiofile(output_audio_path)
            print(f"Audio extracted and saved to {output_audio_path}")
        else:
            print(f"No audio found in {video_path}")
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")

if __name__ == "__main__":
    video_directory = "video/"
    audio_directory = "audio/"

    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    for filename in os.listdir(video_directory):
        if filename.endswith(".mp4") or filename.endswith(".avi"):
            video_path = os.path.join(video_directory, filename)
            audio_filename = os.path.splitext(filename)[0] + ".wav"
            output_audio_path = os.path.join(audio_directory, audio_filename)
            extract_audio_from_video(video_path, output_audio_path)
        else:
            print(f"Skipping non-video file: {filename}")