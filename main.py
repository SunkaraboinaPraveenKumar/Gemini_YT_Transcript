import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


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

if st.button("Get Summary"):
    try:
        video_id = get_video_id_from_url(youtube_link)
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
        transcript_text = extract_transcript(youtube_link)
        st.markdown("## Detailed Transcript:")
        st.write(transcript_text)
    except Exception as e:
        st.error(f"Error: {e}")
