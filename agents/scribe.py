import argparse
import datetime
import os
import sys

from llm import format_journal_entry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe a voice note and format it into a journal note"
    )
    parser.add_argument("transcription_file")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        currtime = datetime.datetime.now()
        transcr_file = args.transcription_file
        scribe_file = os.path.join(
            os.getcwd(),
            "scribe",
            f"scribe_{currtime.strftime('%Y-%m-%d_%H-%M-%S')}.txt",
        )
        with open(transcr_file, "r", encoding="utf-8") as f:
            transcription_text = f.read()
        response = format_journal_entry(transcription_text)
        with open(scribe_file, "w") as scribed:
            scribed.write(response)
            print("file saved!")

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
