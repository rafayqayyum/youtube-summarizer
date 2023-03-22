import streamlit as st
from utils import download_video, summarize_video, get_transcript, convert_video_to_audio
st.set_page_config(page_title="Summarize a Yotube Video",page_icon='/assets/icon2.png',layout='wide')

def check_url(url):
    if url.startswith("https://www.youtube.com/"):
        return True
    else:
        return False

with st.sidebar:
    st.image('assets/icon1.png',width=270,use_column_width=False)
    st.title("About Me:")
    st.subheader("Hi, I am Rafay :wave:")
    st.write("I am a software engineer and a ML enthusiast. I am passionate about building products and solving problems.")
    st.write("Find me on [Github](https://github.com/rafayqayyum) and [LinkedIn](https://www.linkedin.com/in/rafayqayyum/)")
    st.write("This is a Youtube Video Summarizer built using [OpenAI](https://openai.com/) and [Streamlit](https://streamlit.io/).")
    st.write("You can find the source code [here](https://github.com/Rafayqayyum/youtube-summarizer)")


with st.container():
    # add status text
    st.title("Youtube Video Summarizer")
    st.subheader("Provide a Youtube video link and get a summary of the video.")
    # add text input
    text=st.text_input("Enter the Youtube video link: ")
    # add button
    # check if button is clicked
    if st.button("Summarize"):
        progress_bar=st.progress(10,text='Downloading video...')
        if check_url(text):
            video_path= download_video(text)
            if video_path is None:
                st.error("Please enter a valid Youtube video link.")
            else:
                progress_bar.progress(30,text='Converting video to audio...')
                # convert video to audio
                audio_path= convert_video_to_audio(video_path)
                # get transcript
                if audio_path is None:
                    st.error("Unable to convert video to audio.")
                else:
                    progress_bar.progress(50,text='Getting transcript...')
                    transcript= get_transcript(audio_path)
                    if transcript is None:
                        st.error("Unable to get transcript.")
                    else:
                        progress_bar.progress(70,text = 'Summarizing video...')
                        # summarize video
                        summary= summarize_video(transcript)
                        if summary is None:
                            st.error("Unable to summarize video.")
                        else:
                            progress_bar.progress(80,text='Generating summary...')
                            # show summary
                            st.text_area(summary)
                            progress_bar.progress(100,text='Completed!')
        else:
            st.error("Please enter a valid Youtube video link.")
    
        
        