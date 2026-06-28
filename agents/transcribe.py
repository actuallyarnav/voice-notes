import os
from datetime import datetime

from utils.audio_utils import transcribe_audio
from utils.file_utils import log_info, log_success, write_file
from utils.llm_utils import build_messages, load_prompts, run_llm


def transcribe_agent(audio, model_name):
    log_info(f"model type: {model_name}")
    raw_transcription = transcribe_audio(audio, model_name=model_name)
    prompts = load_prompts()

    system_prompt = prompts["punctuation_formatter_system"]
    user_template = prompts["punctuation_formatter_user"]

    user_prompt = user_template.format(text=raw_transcription)
    messages = build_messages(system=system_prompt, user=user_prompt)

    transcription = run_llm(messages=messages)
    """
            entry = format_journal_entry(
                transcription=transcription,
                model=args.llm_model,
                prompts_path=args.prompts_file,
            )
    """
    log_success("transcription complete, saving...")
    currtime = datetime.now()
    filename = os.path.join(
        os.getcwd(),
        "transcriptions",
        f"transcription_{currtime.strftime('%y-%m-%d_%h-%m-%s')}_{model_name}.txt",
    )
    write_file(filename, f"whisper mode: {model_name}\n")
    write_file(filename, transcription)
