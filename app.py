import streamlit as st
import os
from transcribe import transcribe_audio
from extract import extract_meeting_data

st.title("🎙️ Meeting Audio Processor")

uploaded_file = st.file_uploader("Upload a meeting audio file", type = ["mp3", "wav", "m4a"])

if uploaded_file:
    os.makedirs("audio", exist_ok = True)
    audio_path = os.path.join("audio", uploaded_file.name)
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.success(f"Uploaded: {uploaded_file.name}")

    # Transcribe audio
    st.info("Transcribing...")
    transcript = transcribe_audio(audio_path)

    st.text_area("Transcript", transcript, height = 300)

    st.info("Extracting meeting information...")
    result = extract_meeting_data(transcript)
    st.text(result.get("summary", "No summary generated."))

    # st.subheader("📝 Summary")
    # st.text(meeting_info["summary"])

    st.subheader("✅ Action Items")
    st.write(result.get("action_items", "No action items found."))

    st.subheader("✉️ Follow-Up Email")
    st.text_area("Email", result.get("follow_up_email", "No email generated."), height = 250)