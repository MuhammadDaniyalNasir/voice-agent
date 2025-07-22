from faster_whisper import WhisperModel

def transcribe_audio(audio_path):
    model = WhisperModel("base", compute_type = "int8")
    segments, _ = model.transcribe(audio_path)

    transcript = ""
    for segment in segments:
        transcript += f"{segment.text.strip()}"

    return transcript.strip()
    