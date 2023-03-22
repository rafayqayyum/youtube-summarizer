import os
from openai import api_key, Audio, Completion
from pytube import YouTube
import ffmpeg
VIDEO_PATH='videos'
AUDIO_PATH='audios'
api_key = os.environ.get("OPENAI_API_KEY")
def download_video(url):
    try:
        # create a directory to store the video
        if not os.path.exists("videos"):
            os.mkdir("videos")
        # create youtube object
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file= video.download(output_path=VIDEO_PATH)
        # get the video name
        out_file = os.path.basename(out_file)
        # remove whitespace from video name
        new_out_file = out_file.replace(" ", "_")
        os.rename(VIDEO_PATH+'/'+out_file, VIDEO_PATH+'/'+new_out_file)
        # return the video name
        return new_out_file
    except:
        return None


def convert_video_to_audio(video_name):
    try:
        if os.path.exists(AUDIO_PATH) is False:
            os.mkdir(AUDIO_PATH)
        # create audio file name
        audio_file_name = AUDIO_PATH+'/'+video_name.split(".")[0] + ".wav"
        # convert video to audio
        stream = ffmpeg.input(VIDEO_PATH+'/'+video_name)
        stream = ffmpeg.output(stream, audio_file_name, format='mp3')
        ffmpeg.run(stream)
        # remove video file
        os.remove(video_name)
        # return audio file name
        return audio_file_name
    except Exception as e:
        print(e)
        return None
def get_transcript(audio_file_name):
    try:
        # get transcript
        audio_file= open(audio_file_name, "rb")
        transcript = Audio.translate("whisper-1", audio_file)
        return transcript['text']
    except:
        return None

def summarize_video(transcript):
    if transcript is None:
        return None
    length= len(transcript.split())
    if length > 2000:
        length= 2000
    try:
        response = Completion.create(
        model="text-davinci-003",
        prompt=f"{transcript} tl;dr:",
        temperature=0.91,
        max_tokens=500,
        top_p=0.8,
        frequency_penalty=0.1,
        presence_penalty=0.1)
        return response.choices[0].text.strip()
    except:
        return None
    