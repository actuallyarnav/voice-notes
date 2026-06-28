import os

from config import WHISPER_MODEL_NAME


def transcribe_audio(file_path: str, model_name: str = WHISPER_MODEL_NAME) -> str:
    """Transcribe the given audio file with Whisper."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        import whisper
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency 'whisper'. Install it before running this command."
        ) from exc

    model = whisper.load_model(model_name)
    result = model.transcribe(
        file_path,
        fp16=False,
        temperature=0.1,
        condition_on_previous_text=True,
        language="en",
    )
    text = result.get("text", "").strip()

    if not text:
        raise RuntimeError("Whisper returned an empty transcription.")

    return text
