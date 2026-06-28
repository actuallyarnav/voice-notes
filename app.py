import argparse
import datetime
import json
import os
import sys

from agents.transcribe import transcribe_agent
from config import WHISPER_MODEL_NAME
from utils.audio_utils import transcribe_audio
from utils.file_utils import log_info, log_success, write_file
from utils.llm_utils import build_messages, load_prompts, run_llm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe a voice note and format it into a journal JSON object."
    )
    parser.add_argument("audio_file", help="Path to the audio file, such as .m4a")
    parser.add_argument(
        "--whisper-model",
        default=WHISPER_MODEL_NAME,
        help="Whisper model name to use for transcription",
    )
    parser.add_argument(
        "--llm-model",
        default="mistral",
        help="Ollama model name to use for formatting",
    )
    parser.add_argument(
        "--prompts-file",
        default="prompts.yaml",
        help="Path to the YAML file containing prompts",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the final JSON output",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        log_info("Transcribing...")
        transcribe_agent(audio=args.audio_file, model_name=args.whisper_model)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
