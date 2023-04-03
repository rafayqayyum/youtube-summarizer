import streamlit as st
import re
from utils import download_video, summarize_video, get_transcript, convert_video_to_audio
st.set_page_config(page_title="Summarize a Youtube Video",page_icon='assets/icon2.png',layout='centered')
supported_languages = [
    "Afrikaans", "Arabic", "Armenian", "Azerbaijani", "Belarusian", "Bosnian", "Bulgarian", "Catalan",
    "Chinese", "Croatian", "Czech", "Danish", "Dutch", "English", "Estonian", "Finnish", "French", "Galician",
    "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Kannada",
    "Kazakh", "Korean", "Latvian", "Lithuanian", "Macedonian", "Malay", "Marathi", "Maori", "Nepali", "Norwegian",
    "Persian", "Polish", "Portuguese", "Romanian", "Russian", "Serbian", "Slovak", "Slovenian", "Spanish",
    "Swahili", "Swedish", "Tagalog", "Tamil", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese", "Welsh"]

def check_url(url):
    regex='(?:https?:\/\/)?(?:www\.)?youtu(?:\.be\/|be.com\/\S*(?:watch|embed)(?:(?:(?=\/[-a-zA-Z0-9_]{11,}(?!\S))\/)|(?:\S*v=|v\/)))([-a-zA-Z0-9_]{11,})'
    if re.match(regex,url):
        return True
    return False

with st.sidebar:
    st.image('assets/icon1.png',width=270,use_column_width=False)
    st.title("About Me:")
    st.subheader("Hi, I am Rafay :wave:")
    st.write("I am a software engineer and a ML enthusiast. I am passionate about building products and solving problems.")
    st.write("Find me on [Github](https://github.com/rafayqayyum) and [LinkedIn](https://www.linkedin.com/in/rafayqayyum/)")
    st.write("This is a YouTube Video Summarizer built using [OpenAI](https://openai.com/) and [Streamlit](https://streamlit.io/).")
    st.write("You can find the source code [here](https://github.com/Rafayqayyum/youtube-summarizer)")


with st.container():
    # add status text
    st.title("YouTube Video Summarizer")
    st.subheader("Provide a Youtube video link to get the summary of video.")
    # add text input
    text=st.text_input("Enter the YouTube video link: ")
    # add button
    # check if button is clicked
    if st.button("Summarize"):
        if check_url(text):
            progress_bar=st.progress(10,text='Downloading video...')
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
                    status,transcript= get_transcript(audio_path)
                    if status==False:
                        if transcript==None:
                            st.error("Invalid OpenAI API Key.")
                        else:
                            st.error(transcript)
                        st.error("Unable to get transcript.")
                    else:
                        progress_bar.progress(70,text = 'Summarizing video...')
                        # summarize video
                        status, summary= summarize_video(transcript)
                        if status==False:
                            if summary==None:
                                st.error("Unable to summarize video.")
                            else:
                                st.error(summary)
                        else:
                            progress_bar.progress(80,text='Generating summary...')
                            # show summary
                            st.text_area('Summary',summary,height=300)
                            progress_bar.progress(100,text='Completed!')
        else:
            st.error("Please enter a valid Youtube video link.")
    

# Footer section    
with st.container():
    st.markdown('##')
    st.subheader("Disclaimer:")
    st.markdown("<ol><li>This app supports Multiple Languages. However, The translation can be inaccurate.</li>\
                <li>Youtube Video longer than 25-30 minutes will not be supported.</li>\
                <li>Only the first 2500 words will be processed.</li>\
                <li>The summary will always be in English.</li></ol>",unsafe_allow_html=True)
    
    # Show supported languages, display on hover, supported languages text is h5, and the list is ul
st.markdown("<h4><details><summary>Supported Languages</summary><p><ul><li>" + ", &nbsp;".join(supported_languages) + "</li></ul></p></details></h4>", unsafe_allow_html=True)
    
    
    
    
