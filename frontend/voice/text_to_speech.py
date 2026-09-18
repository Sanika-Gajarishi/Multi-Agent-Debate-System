from io import BytesIO

import streamlit as st
from gtts import gTTS


@st.cache_data
def text_to_audio_bytes(
    text: str,
    language: str = "en",
) -> bytes:

    if not text.strip():
        raise ValueError(
            "Text cannot be empty."
        )

    audio = BytesIO()

    tts = gTTS(
        text=text,
        lang=language,
        slow=False,
    )

    tts.write_to_fp(audio)

    return audio.getvalue()