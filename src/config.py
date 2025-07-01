# =====================================
# File: config.py
# Description:
#   Manages configuration via environment variables.
#   Dynamically loads the correct .env file based on ENV_MODE.
#   Validates correct setup for the selected LLM backend.
# =====================================

import os

from dotenv import load_dotenv, find_dotenv

# =========================
# Load .env based on ENV_MODE
# =========================
env_mode = os.getenv("ENV_MODE", "openai").lower()
dotenv_filename = f".env.{env_mode}"
dotenv_path = find_dotenv(filename=dotenv_filename)

if dotenv_path:
    print(f"[DEBUG] Loading environment from {dotenv_filename}")
    load_dotenv(dotenv_path)
else:
    print(f"[DEBUG] No {dotenv_filename} file found. Environment variables must be set externally.")

print("[DEBUG] Current working directory:", os.getcwd())

# =========================
# Load environment variables
# =========================
LLM_BACKEND = os.getenv("LLM_BACKEND", "OPENAI").upper()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

INTERNAL_API_PORT_KEY = os.getenv("INTERNAL_API_PORT_KEY")
INTERNAL_API_URL = os.getenv("INTERNAL_API_URL", "http://internal-api.example.com")
PORTKEY_VIRTUAL_KEY = os.getenv("PORTKEY_VIRTUAL_KEY")
PORTKEY_PROVIDER = os.getenv("PORTKEY_PROVIDER", "azure-openai")
PORTKEY_RETRY_ATTEMPTS = int(os.getenv("PORTKEY_RETRY_ATTEMPTS", "3"))

MAX_ENTRIES = int(os.getenv("MAX_ENTRIES", "64"))

# =========================
# Validation
# =========================
if LLM_BACKEND == "OPENAI":
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Please set it before running in OPENAI mode."
        )
elif LLM_BACKEND == "INTERNAL":
    if not INTERNAL_API_PORT_KEY:
        raise RuntimeError(
            "Missing INTERNAL_API_PORT_KEY. Please set it before running in INTERNAL mode."
        )
else:
    raise RuntimeError(
        f"Invalid LLM_BACKEND '{LLM_BACKEND}'. Must be 'OPENAI' or 'INTERNAL'."
    )

# =========================
# Centralized config object
# =========================
CONFIG = {
    "llm_backend": LLM_BACKEND,
    "openai_api_key": OPENAI_API_KEY,
    "internal_api_port_key": INTERNAL_API_PORT_KEY,
    "internal_api_url": INTERNAL_API_URL,
    "portkey_virtual_key": PORTKEY_VIRTUAL_KEY,
    "portkey_provider": PORTKEY_PROVIDER,
    "portkey_retry_attempts": PORTKEY_RETRY_ATTEMPTS,
    "max_entries": MAX_ENTRIES,
}

# =========================
# Debug output
# =========================
print(f"[DEBUG] Config loaded from mode: {env_mode.upper()}")
print(f"[DEBUG] LLM_BACKEND = {LLM_BACKEND}")
print(f"[DEBUG] OPENAI_API_KEY present: {bool(OPENAI_API_KEY)}")
print(f"[DEBUG] INTERNAL_API_PORT_KEY present: {bool(INTERNAL_API_PORT_KEY)}")
print(f"[DEBUG] CONFIG = {CONFIG}")
