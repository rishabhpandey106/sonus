import subprocess
import os

def burn(video_path, srt_path, output_path, ffmpeg_path):
    video_path = os.path.abspath(video_path)
    srt_path = os.path.abspath(srt_path)
    output_path = os.path.abspath(output_path)
    # output_path = os.path.abspath(output_path)
    srt_path_escaped = srt_path.replace("\\", "\\\\").replace(":", "\\:")

    command = (
        f'"{ffmpeg_path}" -i "{video_path}" '
        f'-vf "subtitles=\'{srt_path_escaped}\'" '
        f'-c:v libx264 -c:a aac -strict experimental -b:a 192k "{output_path}"'
    )
    # command = f'"{ffmpeg_path}" -i "{video_path}" -vf "subtitles={srt_path}" -c:v libx264 -c:a aac -strict experimental -b:a 192k "{output_path}"'
    # command = f'"{ffmpeg_path}" -i "{video_path}" -vf "subtitles={srt_path}" "{output_path}"'

    print(f"Burning subtitles into video: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
        print("Subtitles burned into video successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error burning subtitles into video: {e}")


if __name__ == "__main__":
    video_path = r"video\sample.mp4"
    srt_path = r"transcript\caption.srt"
    output_path = r"output\video1.mp4"
    ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"

    burn(video_path, srt_path, output_path, ffmpeg_path)