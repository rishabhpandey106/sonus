# Sonus 🎙️

**Sonus** is a simple yet powerful Streamlit-based web app that allows you to:

1. 🎥 Upload a video
2. 🎧 Extract audio
3. ✍️ Generate bilingual (Hindi-English) transcriptions using OpenAI Whisper
4. ✏️ Transliterate Hindi to Roman script using Gemini
5. ✉️ Edit subtitles in-browser
6. 📀 Burn subtitles into the video

---

## 🚀 Features

- 🎙 Transcribes code-mixed Hindi-English audio using OpenAI's Whisper
- 🎫 Transliterates Devanagari Hindi text into Roman script using Google's Gemini
- 🖊 Editable subtitles in a user-friendly interface
- 🎨 Burns hard subtitles onto the video using FFmpeg

---

## 📁 Project Structure

```
sonus/
├── audio/                  # Extracted audio files
├── output/                 # Final videos with burned subtitles
├── transcript/             # Generated SRT subtitle files
├── video/                  # Uploaded videos
├── main.py                 # Main Streamlit app
├── .env                    # Environment variables (Google API Key)
└── requirements.txt        # Python dependencies
```

---

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/rishabhpandey106/sonus.git
cd sonus
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

Make sure `ffmpeg` is installed and available in your system PATH:

```bash
# Ubuntu
sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html and add to PATH
```

### 5. Add Google API Key

Create a `.env` file:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 6. Run the App

```bash
streamlit run main.py
```

---

## 📊 How It Works

- `main.py` handles the UI and logic flow
- Audio is extracted using `moviepy`
- Transcription done by `whisper` (with Hindi-English prompt)
- Transliteration via Gemini API (Devanagari → Romanized Hindi)
- Subtitles are burned using `ffmpeg`

---

## 💡 Tips

- Use shorter videos for quicker processing
- You can edit the subtitles before burning
- Works best on CUDA-enabled systems (but CPU works too!)

---

## 🚧 Troubleshooting

**FFmpeg not found**\
Make sure `ffmpeg` is installed and accessible in your system's PATH.

**Gemini API errors**\
Check that your API key is correct and not rate-limited.

**CUDA issues**\
Falls back to CPU if no GPU is available.

---

## 🎓 License

MIT License.

---

## 🙏 Credits

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Google Gemini API](https://makersuite.google.com/app)
- [Streamlit](https://streamlit.io)
- [MoviePy](https://zulko.github.io/moviepy/)
- [FFmpeg](https://ffmpeg.org)

---

Built with ❤️ by Rishabh&#x20;

