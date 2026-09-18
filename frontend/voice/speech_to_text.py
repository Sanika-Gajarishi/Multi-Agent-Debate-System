import io

import speech_recognition as sr


def audio_to_text(
    audio_bytes: bytes,
) -> str:
    """
    Convert recorded microphone audio into text.
    """

    recognizer = sr.Recognizer()

    audio_file = io.BytesIO(
        audio_bytes
    )

    with sr.AudioFile(
        audio_file
    ) as source:

        audio = recognizer.record(
            source
        )

    try:

        text = recognizer.recognize_google(
            audio
        )

        return text

    except sr.UnknownValueError:

        raise ValueError(
            "Could not understand the audio."
        )

    except sr.RequestError:

        raise ConnectionError(
            "Speech recognition service is unavailable."
        )