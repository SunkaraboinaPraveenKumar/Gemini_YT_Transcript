import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

# Load environment variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
if not api_key:
    st.error("Google Gemini API Key not found. Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Define prompt template
prompt_template = (
    "You are a YouTube video summarizer. You will take the transcript text and summarize "
    "the entire video elaborately in simpler words, with examples where needed. "
    "The Transcript text will be appended here: "
)

# Function to generate content using Gemini API
def generate_gemini_summary(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Function to extract transcript from a YouTube video
def extract_transcript(youtube_video_url):
    try:
        video_id = get_video_id_from_url(youtube_video_url)
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = "".join(segment["text"] for segment in transcript_text)
        return transcript
    except Exception as e:
        raise e

# Utility function to extract video ID from URL
def get_video_id_from_url(youtube_url):
    parsed_url = urlparse(youtube_url)
    video_id = parse_qs(parsed_url.query).get("v")
    if video_id:
        return video_id[0]
    else:
        raise ValueError("Invalid YouTube URL")

# Function to split transcript into manageable blocks
def split_transcript_into_blocks(transcript, max_chars):
    return [transcript[i:i + max_chars] for i in range(0, len(transcript), max_chars)]

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = get_video_id_from_url(youtube_link)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Get Transcript"):
    try:
        transcript_text = extract_transcript(youtube_link)

        # Ensure the transcript text is not empty
        if transcript_text:
            # Display the entire transcript in a scrollable text area
            st.subheader("Video Transcript:")
            st.text_area("Transcript", transcript_text, height=300)

    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Get Summary"):
    try:
        transcript_text = extract_transcript(youtube_link)

        # Ensure the transcript text is not empty
        if transcript_text:
            # Process transcript in blocks if too large
            max_chars = 3000  # Adjust based on Gemini API limits
            transcript_blocks = split_transcript_into_blocks(transcript_text, max_chars)

            # Generate summaries for each block
            summary = ""
            for block in transcript_blocks:
                summary += generate_gemini_summary(block, prompt_template) + "\n"

            st.markdown("## Detailed Summary:")
            st.write(summary)
    except Exception as e:
        st.error(f"Error: {e}")
