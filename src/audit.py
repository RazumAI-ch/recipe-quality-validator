# =====================================
# File: audit.py
# Description:
#   Contains functions to analyze recipe files
#   and perform LLM-based quality audits.
# =====================================

import json
import logging
import os
from typing import Any

from dotenv import load_dotenv

import config
from src.utils import extract_json_from_text

# Load environment variables
load_dotenv()


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
        from portkey_ai import Portkey

        portkey = Portkey(
            api_key=os.getenv("PORTKEY_AZURE_API_KEY"),
            base_url=os.getenv("PORTKEY_BASE_URL"),
            debug=True,
            provider="azure-openai"
        )

        try:
            response = portkey.chat.completions.create(
                messages=messages,
                model="gpt-35-turbo",  # Azure deployment name
                max_tokens=500,  # hardcoded token limit
                temperature=0.7,  # hardcoded temperature
                stream=True
            )

            full_content = ""
            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_content += content
                    print(content, end="", flush=True)

            content = full_content

        except Exception as e:
            logging.error(f"Portkey API call failed: {str(e)}")
            raise ValueError("Portkey API call failed; check logs for details.")

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