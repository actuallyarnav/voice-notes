import json
from pathlib import Path
from typing import Any

import yaml

DEFAULT_PROMPTS_PATH = "prompts.yaml"


def load_prompts(prompts_path: str = DEFAULT_PROMPTS_PATH) -> dict[str, str]:
    """Load all prompts from a YAML file."""
    path = Path(prompts_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompts file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ValueError("Prompts file must contain a top-level mapping.")

    return {k: str(v) for k, v in data.items()}


def build_messages(
    *,
    system: str | None = None,
    user: str,
) -> list[dict[str, str]]:
    """Build chat messages generically."""
    messages: list[dict[str, str]] = []

    if system:
        messages.append({"role": "system", "content": system})

    messages.append({"role": "user", "content": user})

    return messages


def build_messages_from_prompt(
    prompt_key: str,
    *,
    variables: dict[str, Any],
    prompts_path: str = DEFAULT_PROMPTS_PATH,
) -> list[dict[str, str]]:
    """
    Build messages using a prompt pair:
    expects keys:
      - <prompt_key>_system
      - <prompt_key>_user
    """
    prompts = load_prompts(prompts_path)

    system_key = f"{prompt_key}_system"
    user_key = f"{prompt_key}_user"

    if system_key not in prompts or user_key not in prompts:
        raise ValueError(f"Missing prompt pair: {system_key}, {user_key}")

    system_prompt = prompts[system_key]
    user_prompt = prompts[user_key].format(**variables)

    return build_messages(system=system_prompt, user=user_prompt)


def chat_once(messages: list[dict[str, str]], model: str = "mistral") -> str:
    """Send a single chat request to Ollama and return the assistant content."""
    try:
        import ollama
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency 'ollama'. Install it before running this command."
        ) from exc

    response = ollama.chat(model=model, messages=messages)
    content = response.get("message", {}).get("content", "").strip()

    if not content:
        raise RuntimeError("The LLM returned an empty response.")

    return content


def run_llm(
    *,
    model: str = "mistral",
    system: str | None = None,
    user: str | None = None,
    messages: list[dict[str, str]] | None = None,
) -> str:
    """
    Universal LLM entry point.

    You can either:
    - pass `messages`
    OR
    - pass `system` + `user`
    """
    if messages is None:
        if user is None:
            raise ValueError("Either 'messages' or 'user' must be provided.")
        messages = build_messages(system=system, user=user)

    return chat_once(messages, model=model)
