# =====================================
# File: audit.py
# Description:
#   Contains functions to analyze recipe files
#   and perform LLM-based quality audits.
# =====================================

import json
import logging
from typing import Any

import requests

import config
from src.utils import extract_json_from_text


def analyze_recipe(recipe_entries, model="gpt-4o", system_prompt="", user_prompt=""):
    """
    Analyze recipe entries using the selected backend (OpenAI or Internal).
    """
    max_entries = config.MAX_ENTRIES

    # Truncate recipe entries if exceeding the limit
    if len(recipe_entries) > max_entries:
        truncated = recipe_entries[:max_entries]
        logging.warning(f"Truncated to first {max_entries} entries to stay within context limits.")
    else:
        truncated = recipe_entries

    full_prompt = (
        f"{user_prompt}\n\n"
        "Recipe data:\n"
        f"{json.dumps(truncated, indent=2, sort_keys=True)}"
    )

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": full_prompt},
    ]

    # Determine backend and make the appropriate API call
    if config.LLM_BACKEND == "OPENAI":
        # noinspection PyUnresolvedReferences
        from openai import OpenAI  # Local import to avoid issues when not using OpenAI
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore[arg-type]
            temperature=0,
            top_p=1,
        )
        content = response.choices[0].message.content.strip()

    elif config.LLM_BACKEND == "INTERNAL":
        # Internal API Call (via Portkey)
        payload = {
            "model": model,
            "messages": messages,
            "virtual_key": config.PORTKEY_VIRTUAL_KEY,
            "provider": config.PORTKEY_PROVIDER,
            "retry": {"attempts": config.PORTKEY_RETRY_ATTEMPTS},
        }
        headers = {"Authorization": f"Bearer {config.INTERNAL_API_PORT_KEY}"}

        response = requests.post(
            config.INTERNAL_API_URL,
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            logging.error(f"Internal API call failed: {response.status_code}, {response.text}")
            raise ValueError("Internal API call failed; check the logs for details.")

        content = response.json()

    else:
        raise ValueError(f"Unsupported LLM backend: {config.LLM_BACKEND}")

    # ✅ Clean Markdown fences or extra text
    clean_content = extract_json_from_text(content)

    # Parse response content
    try:
        parsed = json.loads(clean_content)
        if "summary_text" not in parsed:
            parsed["summary_text"] = ""
        return parsed
    except json.JSONDecodeError:
        logging.error(f"Failed to parse JSON output. Raw content:\n{content}")
        raise ValueError("Failed to parse JSON output from the selected backend.")