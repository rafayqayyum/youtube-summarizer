# YouTube Summarizer App
This app allows users to generate a summary of a whole YouTube video using pytube to download the video's audio in mp4 format, moviepy to convert it to mp3 format, OpenAI Audio to Text API to transcribe the audio, and Text Summarizer API to generate a summary of the transcribed text. It also features a user-friendly interface built with Streamlit.

# Installation
1. Clone the repository
```git clone https://github.com/Rafayqayyum/youtube-summarizer```
2. Install the requirements
```pip install -r requirements.txt```
3. Sign up for an OpenAI API key [here](https://platform.openai.com/signup/)
4. Add your OpenAI API key to the environment variable by exporting it in your terminal:
``` export OPENAI_API_KEY='YOUR_API_KEY'```

# Usage
1. Run the app
```streamlit run app.py```
2. Enter the URL of the YouTube video you want to summarize.
3. Click the "Summarize" button.
4. Wait for the app to process the video and generate the summary.
5. The summary will be displayed on the screen.
