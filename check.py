#!/usr/bin/env python3
"""
Run this before starting OpenAssistant to verify your setup is correct.
Usage: python check.py
"""

import sys
import importlib.util

REQUIRED_PYTHON = (3, 9)

# Read model name from config so check.py always matches what the user configured
try:
    from config import MODEL as MODEL_NAME
except ImportError:
    MODEL_NAME = "llama3.1"


def check(label, fn):
    print(f"  Checking {label}... ", end="", flush=True)
    ok, msg = fn()
    if ok:
        print(f"✓ {msg}")
    else:
        print(f"✗ {msg}")
    return ok


def check_python():
    v = sys.version_info
    if v >= REQUIRED_PYTHON:
        return True, f"Python {v.major}.{v.minor}.{v.micro}"
    return False, f"Python {v.major}.{v.minor} found — need 3.9+"


def check_flask():
    spec = importlib.util.find_spec("flask")
    if spec:
        import flask
        return True, f"Flask {flask.__version__}"
    return False, "Flask not installed — run: pip install -r requirements.txt"


def check_requests():
    spec = importlib.util.find_spec("requests")
    if spec:
        import requests
        return True, f"requests {requests.__version__}"
    return False, "requests not installed — run: pip install -r requirements.txt"


def check_ollama_running():
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        if r.status_code == 200:
            return True, "Ollama is running"
        return False, f"Ollama returned status {r.status_code}"
    except Exception:
        return False, "Ollama not running — start it: open Ollama app, or run `ollama serve`"


def check_model_pulled():
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        if r.status_code != 200:
            return False, "Could not reach Ollama to check models"
        models = [m["name"] for m in r.json().get("models", [])]
        matches = [m for m in models if MODEL_NAME in m]
        if matches:
            return True, f"Found: {matches[0]}"
        available = ", ".join(models) if models else "none"
        return False, (
            f"Model '{MODEL_NAME}' not found. "
            f"Run: ollama pull {MODEL_NAME}  "
            f"(Available: {available})"
        )
    except Exception:
        return False, "Could not check — is Ollama running?"


def main():
    print("\n🔍 OpenAssistant Setup Check\n")

    results = [
        check("Python version", check_python),
        check("Flask",          check_flask),
        check("requests",       check_requests),
        check("Ollama",         check_ollama_running),
        check("Model",          check_model_pulled),
    ]

    print()
    if all(results):
        print("✅ Everything looks good! You can now run:")
        print("   Web UI : python app.py")
        print("   CLI    : python cli.py\n")
    else:
        failed = sum(1 for r in results if not r)
        print(f"❌ {failed} issue(s) found. Fix them above, then re-run: python check.py\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
