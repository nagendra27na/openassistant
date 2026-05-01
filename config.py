# config.py — edit this to customize your assistant

# Model to use (must be pulled via `ollama pull <model>`)
MODEL = "llama3.1"

# Ollama API endpoint (default, don't change unless you moved Ollama)
OLLAMA_URL = "http://localhost:11434/api/chat"

# Web UI port
PORT = 5000

# System prompts for each mode
SYSTEM_PROMPTS = {
    "chat": (
        "You are a helpful, friendly AI assistant. "
        "Answer questions clearly and honestly. "
        "If you don't know something, say so."
    ),
    "code": (
        "You are an expert software engineer and coding assistant. "
        "Help with code generation, debugging, code review, and technical explanations. "
        "Always provide working code examples. Explain your reasoning. "
        "Default to Python unless the user specifies another language."
    ),
    "custom": (
        # Replace this with your own system prompt for a specialized assistant
        "You are a specialized AI assistant. Be concise and accurate."
    ),
}

# Default mode on startup
DEFAULT_MODE = "chat"
