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

    # Determine backend and make the appropriate API call
    if config.LLM_BACKEND == "OPENAI":
        from openai import OpenAI
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt},
        ]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
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
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt},
        ]
        try:
            response = portkey.chat.completions.create(
                messages=messages,
                model="gpt-35-turbo",
                max_tokens=500,
                temperature=0.7,
                stream=True
            )
            full_content = ""
            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                    content_chunk = chunk.choices[0].delta.content
                    full_content += content_chunk
                    print(content_chunk, end="", flush=True)
            content = full_content
        except Exception as e:
            logging.error(f"Portkey API call failed: {str(e)}")
            raise ValueError("Portkey API call failed; check logs for details.")

    elif config.LLM_BACKEND == "GEMINI":  # <-- ADD THIS ENTIRE BLOCK
        import google.generativeai as genai
        genai.configure(api_key=config.GEMINI_API_KEY)

        # Gemini uses a different prompt structure (no system prompt)
        # We combine the system and user prompts into a single prompt.
        combined_prompt = f"{system_prompt}\n\n{full_prompt}"

        gemini_model = genai.GenerativeModel('gemini-pro')
        response = gemini_model.generate_content(combined_prompt)
        content = response.text.strip()

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