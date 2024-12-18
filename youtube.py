import streamlit as st
from dotenv import load_dotenv
import openai
import os
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup


load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = """You are a summarizer. You will be taking the text input
and summarizing it to provide the most important points within 250 words. Please summarize the following text: """



def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e



def generate_openai_summary(text, prompt):
    try:

        full_prompt = prompt + "\n" + text


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a summarizer."},
                      {"role": "user", "content": full_prompt}],
            max_tokens=250,
            temperature=0.7
        )

        return response.choices[0].message["content"].strip()

    except Exception as e:
        raise e



def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")


        paragraphs = soup.find_all("p")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.get_text() + "\n"

        return text

    except Exception as e:
        raise e



st.title("Transcript to Detailed Notes Converter")


option = st.sidebar.selectbox(
    "Choose an option:",
    ["Summarize Video", "Show Full Transcript", "Ask a Question on Transcript", "Get Transcript from URL"]
)


url_input = st.text_input("Enter YouTube Video or URL:")


if url_input:
    if "youtube.com" in url_input:
        video_id = url_input.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Handle options
if option == "Summarize Video":
    if st.button("Get Summary"):
        if url_input:
            try:
                if "youtube.com" in url_input:

                    transcript_text = extract_transcript_details(url_input)
                else:

                    transcript_text = extract_text_from_url(url_input)

                if transcript_text:

                    summary = generate_openai_summary(transcript_text, prompt)

                    # Display the summary
                    st.markdown("## Detailed Notes:")
                    st.write(summary)

            except Exception as e:
                st.error(f"Error: {e}")

elif option == "Show Full Transcript":
    if st.button("Show Transcript"):
        if url_input:
            try:
                if "youtube.com" in url_input:

                    transcript_text = extract_transcript_details(url_input)
                else:

                    transcript_text = extract_text_from_url(url_input)

                if transcript_text:
                    # Display the full transcript
                    st.markdown("## Full Transcript:")
                    st.write(transcript_text)

            except Exception as e:
                st.error(f"Error: {e}")

elif option == "Ask a Question on Transcript":
    question = st.text_input("Ask a Question based on the Transcript:")

    if question and url_input:
        try:
            if "youtube.com" in url_input:

                transcript_text = extract_transcript_details(url_input)
            else:

                transcript_text = extract_text_from_url(url_input)

            if transcript_text:
                # Answer the question based on the transcript using OpenAI API
                answer = generate_openai_summary(transcript_text, f"Answer the question: {question}")

                # Display the answer
                st.markdown("## Answer:")
                st.write(answer)

        except Exception as e:
            st.error(f"Error: {e}")

elif option == "Get Transcript from URL":
    if st.button("Get Transcript"):
        if url_input:
            try:

                transcript_text = extract_text_from_url(url_input)

                if transcript_text:

                    st.markdown("## Extracted Text from URL:")
                    st.write(transcript_text)

            except Exception as e:
                st.error(f"Error: {e}")
