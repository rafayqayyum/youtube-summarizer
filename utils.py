import os
from openai import  Audio, Completion
import openai
from pytube import YouTube
import moviepy.editor as mp
VIDEO_PATH='videos'
AUDIO_PATH='audios'
openai.api_key = os.environ.get("OPENAI_API_KEY")
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
        new_out_file=out_file.replace(" ", "_")
        # remove whitespace from video name
        if os.path.exists(os.path.join(VIDEO_PATH,new_out_file)) is False:
            os.rename(os.path.join(VIDEO_PATH,out_file),os.path.join(VIDEO_PATH,new_out_file))
        # return the video name
        return new_out_file
    except Exception as e:
        print(e)


def convert_video_to_audio(video_name):
    try:
        if os.path.exists(AUDIO_PATH) is False:
            os.mkdir(AUDIO_PATH)
        # create audio file name
        audio_file_name =os.path.join(AUDIO_PATH,video_name.split(".")[0] + ".mp3")
        # convert video to audio
        print(video_name)
        print(audio_file_name)
        clip = mp.AudioFileClip(os.path.join(VIDEO_PATH,video_name))
        clip.write_audiofile(audio_file_name)
        clip.close()
        # remove video file
        if os.path.exists(os.path.join(VIDEO_PATH,video_name)):
            os.remove(os.path.join(VIDEO_PATH,video_name))
        # return audio file name
        return audio_file_name
    except Exception as e:
        print(e)
        return None
    
def get_transcript(audio_file_name):
    try:
        print(audio_file_name)
        # get transcript
        audio_file= open(audio_file_name, "rb")
        transcript = Audio.translate("whisper-1", audio_file)
        audio_file.close()
        if os.path.exists(audio_file_name):
            os.remove(audio_file_name)
        return transcript['text']
    except Exception as e:
        print(e)
        return None

def summarize_video(transcript):
    if transcript is None:
        return None
    length= len(transcript.split())
    if length > 2500:
        transcript=' '.join(transcript.split()[:2500])
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
    except Exception as e:
        print(e)
        return None
    