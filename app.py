import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv() # load all the environment variables

import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Configure api
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt=""" You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the importance summary in points
within 250 words. The transcript text will be appended here: """

# Define function to get transcript from youtube video
def extract_transcript(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_text:
            transcript += " "+ i["text"]
        return transcript
    except Exception as e:
        raise e

# Define function to summarize the transcript
def generate_gemini_content(transcript,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript)
    return response.text


# Initialize streamlit app
st.set_page_config(page_title="YTsummarizer")

# App name
st.markdown("<h4 style='text-align: center;'>Youtube Video Summarizer</h4>", unsafe_allow_html=True)

# Input
youtube_link=st.text_input(" ", key="input", placeholder="Enter Youtube video link")

if youtube_link:
    video_id=youtube_link.split("=")[1].split("&")[0]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize"):
    transcript=extract_transcript(youtube_link)

    if transcript:
        summary=generate_gemini_content(transcript,prompt)
        st.write(summary)
