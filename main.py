import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_GEMINI_API_KEY'))

prompt = ("You are Youtube video summarizer. You will be taking the transcript text and summarizing "
          "the entire video elaborately in simpler words and with examples where ever needed."
          "The Transcript text will be appended here: ")


# getting summary from google gemini api

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


# getting transcript from YT videos by id

def extract_transcript(youtube_video_url):
    try:
        video_id = get_video_id_from_url(youtube_video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    except Exception as e:
        raise e


# Utility function to extract video ID
def get_video_id_from_url(youtube_url):
    parsed_url = urlparse(youtube_url)
    video_id = parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise ValueError("Invalid YouTube URL")


st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter Youtube Video Link:")

if youtube_link:
    try:
        video_id = get_video_id_from_url(youtube_link)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Get Summary"):
    try:
        transcript_text = extract_transcript(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Summary:")
            st.write(summary)
    except Exception as e:
        st.error(f"Error: {e}")
