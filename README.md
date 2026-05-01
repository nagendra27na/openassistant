<div align="center">

# OpenAssistant

**A free, private, fully local AI assistant. No API keys. No cloud. No cost. Ever.**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-black)](https://ollama.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Quickstart](#-quickstart) · [Features](#-features) · [Install](#-installation) · [FAQ](#-faq) · [Roadmap](#-roadmap) · [Contributing](#-contributing)

</div>

---

## What is OpenAssistant?

OpenAssistant is an open-source AI assistant that runs **entirely on your own machine** using [Ollama](https://ollama.com) and open-weight models like Llama 3.1. It has a web UI and a terminal CLI, supports multiple assistant modes, and costs nothing to run after setup.

No account. No subscription. No data sent anywhere. Your conversations stay on your computer.

---

## Why is it different?

Most AI assistants are cloud products. They require an account, send your data to a server, charge per message or per month, and can be shut down or changed at any time.

OpenAssistant is the opposite:

| | OpenAssistant | ChatGPT / Claude / Gemini |
|---|---|---|
| **Cost** | Free forever | Free tier + paid plans |
| **Privacy** | 100% local, nothing leaves your machine | Conversations processed on cloud servers |
| **Internet required** | Only for setup | Always |
| **API key required** | No | Yes |
| **Works offline** | Yes, after setup | No |
| **Model you control** | Yes — swap models freely | No |
| **Can be shut down** | No — you own it | Yes |
| **Customizable prompts** | Yes, full control | Limited |
| **Open source** | Yes, MIT license | No |

The tradeoff: cloud models like GPT-4 and Claude are more capable than what runs locally today. But for most everyday tasks — Q&A, coding help, writing, research — a local Llama 3.1 8B is more than sufficient, and it never phones home.

---

## Features

**Core**
- General conversation and Q&A
- Code generation, debugging, and review
- Custom mode — define your own assistant persona and behavior via system prompt
- Streaming responses — text appears as it's generated, not all at once
- Persistent conversation history within a session

**Interfaces**
- Web UI — dark-themed browser interface, no extra install
- CLI — terminal interface with slash commands (`/mode`, `/reset`, `/help`)

**Model flexibility**
- Works with any model Ollama supports: Llama 3.1, Mistral, Qwen 2.5, Phi-3, Gemma 2, and more
- Switch models by changing one line in `config.py`
- No code changes needed

**Privacy and control**
- Zero telemetry by default — nothing is tracked or sent anywhere
- No accounts, no API keys, no rate limits
- Works fully offline after the model is downloaded

---

## Quickstart

Get running in under 5 minutes.

**Step 1 — Install Ollama**

Go to [https://ollama.com](https://ollama.com) and install it for your OS.

**Step 2 — Pull the model**

```bash
ollama pull llama3.1
```

**Step 3 — Clone and install**

```bash
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip install -r requirements.txt
```

**Step 4 — Check your setup**

```bash
python check.py
```

**Step 5 — Run**

```bash
python app.py       # Web UI — open http://localhost:5000
python cli.py       # Terminal
```

For full OS-specific instructions see [Installation](#-installation) below.

---

## Installation

### macOS

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install Ollama (or download the .dmg app from ollama.com)
brew install ollama
ollama serve &

# Pull model, clone repo, run
ollama pull llama3.1
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip3 install -r requirements.txt
python3 check.py
python3 app.py
```

> Alternatively, download Ollama as a native Mac app from [ollama.com/download](https://ollama.com/download) — it runs in your menu bar.

---

### Windows

1. Download and install **Python 3.9+** from [python.org](https://www.python.org/downloads/windows/)
   > During install: check **"Add Python to PATH"**

2. Download and install **Ollama** from [ollama.com/download](https://ollama.com/download)
   > It runs as a background service and appears in the system tray

3. Open **Command Prompt** or **PowerShell**:

```cmd
ollama pull llama3.1
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip install -r requirements.txt
python check.py
python app.py
```

4. Open [http://localhost:5000](http://localhost:5000) in your browser

> No Git installed? Download the ZIP from the green **Code** button on this GitHub page, extract it, open a terminal in that folder, then run from step 3.

---

### Linux — Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip3 install -r requirements.txt
python3 check.py
python3 app.py
```

---

### Linux — Fedora / RHEL / CentOS

```bash
sudo dnf install python3 python3-pip git -y
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip3 install -r requirements.txt
python3 check.py
python3 app.py
```

---

### Linux — Arch

```bash
sudo pacman -S python python-pip git
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip install -r requirements.txt
python check.py
python app.py
```

---

### Using a virtual environment (recommended for all OSes)

Keeps OpenAssistant's dependencies isolated from your system Python.

```bash
# Create
python3 -m venv venv        # macOS/Linux
python -m venv venv          # Windows

# Activate
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

# Install and run
pip install -r requirements.txt
python check.py
python app.py
```

Deactivate with: `deactivate`

---

### Switching models

Edit the `MODEL` line in `config.py`. Pull the model first.

| Model | Pull command | RAM needed | Best for |
|---|---|---|---|
| `llama3.1` | `ollama pull llama3.1` | 8 GB | Default — best balance |
| `mistral` | `ollama pull mistral` | 6 GB | Fast, lightweight |
| `qwen2.5` | `ollama pull qwen2.5` | 6 GB | Code tasks |
| `phi3` | `ollama pull phi3` | 4 GB | Low-RAM machines |
| `gemma2` | `ollama pull gemma2` | 6 GB | Instruction following |
| `llama3.1:70b` | `ollama pull llama3.1:70b` | 40 GB | Maximum quality |

---

## Usage

### Web UI

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000). Use the sidebar to switch modes or start a new conversation.

### CLI

```bash
python cli.py                  # default chat mode
python cli.py --mode code      # start in code assistant mode
python cli.py --mode custom    # start with your custom system prompt
```

**CLI commands:**

| Command | Action |
|---|---|
| `/mode chat` | Switch to general chat |
| `/mode code` | Switch to code assistant |
| `/mode custom` | Switch to your custom mode |
| `/reset` | Clear conversation history |
| `/help` | Show all commands |
| `/quit` | Exit |

---

## Customization

Edit `config.py`:

```python
MODEL = "llama3.1"          # change the model
PORT  = 5000                # change the web UI port

SYSTEM_PROMPTS = {
    "custom": "You are a specialized assistant for..."  # write your own
}
```

No other files need to change.

---

## Project Structure

```
openassistant/
├── app.py              # Flask web server
├── cli.py              # Terminal interface
├── assistant.py        # Core chat logic, streaming, history management
├── config.py           # Model, prompts, port — the only file most users need to edit
├── check.py            # Setup verification — run this first
├── requirements.txt    # Python dependencies (Flask, requests)
├── templates/
│   └── index.html      # Web UI — self-contained HTML/CSS/JS
├── INSTALL.md          # Detailed OS-specific install guide
└── README.md
```

---

## FAQ

**Does it need the internet to run?**
Only to download the model the first time (`ollama pull`). After that it works fully offline.

**Is my data private?**
Yes. Everything runs on your machine. Nothing is sent to any server. No analytics, no logging, no telemetry of any kind.

**What hardware do I need?**
A modern laptop or desktop with at least 8GB of RAM. The default model (Llama 3.1 8B) uses ~5-6GB RAM. For lower-spec machines, use `phi3` which needs ~4GB. A GPU is not required but speeds up responses significantly.

**Does it work on Apple Silicon (M1/M2/M3/M4)?**
Yes. Ollama has native Apple Silicon support and runs very fast on M-series chips.

**Can I run it on a Raspberry Pi or old laptop?**
Yes, with a small model like `phi3` or `tinyllama`. Responses will be slow but it works.

**Is this actually free? No hidden costs?**
Yes, completely free. Ollama is free software. The models are free to download. This code is MIT licensed. There is no paid tier, no usage cap, no catch.

**Can I use a different model than Llama?**
Yes — any model in the [Ollama library](https://ollama.com/library). Change `MODEL` in `config.py` and pull the model first.

**Can I run multiple users at once?**
The current setup is single-user. Multi-user session support is on the roadmap for v0.2.

**Can I build my own chatbot on top of this?**
Yes. The MIT license lets you use, modify, fork, and redistribute freely. Change the system prompt in `config.py` to create any specialized assistant you want.

**Why Llama 3.1 and not another model?**
It's the best default balance of quality, size, hardware requirements, and permissive licensing for most users. The code is model-agnostic — Llama 3.1 is just the recommended starting point.

**Ollama keeps stopping. How do I keep it running?**
On Linux, run `sudo systemctl enable ollama` to start it automatically on boot. On macOS, the menu bar app starts with login. On Windows, it starts with the system tray app.

**I get a "port already in use" error.**
Change `PORT = 5000` in `config.py` to another number like `5001`.

---

## Roadmap

### v0.2 — Multi-user & persistence
- [ ] Per-user sessions in web UI
- [ ] Save and load conversations to disk
- [ ] Conversation history browser in web UI

### v0.3 — Files & plugins
- [ ] File upload — ask questions about PDFs, text files, and documents
- [ ] Plugin API — add custom tools the assistant can call
- [ ] Model selector in web UI (no `config.py` edit needed)

### v0.4 — Voice & export
- [ ] Voice input via browser microphone
- [ ] Export conversations as Markdown or PDF
- [ ] Docker image for one-command deploy

### v1.0 — Full featured
- [ ] Persistent memory across sessions
- [ ] Conversation search
- [ ] Full plugin ecosystem with community-built tools

Have a feature idea? [Open an issue](https://github.com/YOUR_USERNAME/openassistant/issues) and describe it.

---

## Development

### Setup for contributors

```bash
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running in dev mode (auto-reload on file changes)

```bash
# macOS/Linux
FLASK_DEBUG=1 python app.py

# Windows
set FLASK_DEBUG=1 && python app.py
```

### How the code is structured

All AI logic lives in `assistant.py`. The `Assistant` class handles message history, system prompt injection, streaming from Ollama's `/api/chat` endpoint, and error recovery (conversation history is never corrupted on a failed request).

`app.py` and `cli.py` are thin wrappers. Both call `assistant.py`. If you want to change how the AI behaves, that file is where to start.

### Making changes

- Bug fix or small improvement: open a PR directly
- New feature: open an issue first to discuss before writing code
- New mode or system prompt: edit `config.py` and update the model table in the README

---

## Telemetry

**OpenAssistant collects zero telemetry.**

No usage statistics, no crash reports, no analytics, no phone-home of any kind. The app makes exactly one type of outbound network request: to `http://localhost:11434` — your own Ollama instance running on your machine.

Want to verify this yourself? The entire outbound request is in `assistant.py` at the `requests.post(OLLAMA_URL, ...)` calls. `OLLAMA_URL` is defined in `config.py` as `http://localhost:11434/api/chat`. That's it.

---

## Community & Plugins

There is no official plugin system yet — that is planned for v0.3. Here is what you can do today:

**Customize for your use case:**
Fork the repo and change `SYSTEM_PROMPTS["custom"]` in `config.py` to build a specialized assistant — customer support bot, coding tutor, research assistant, writing coach, etc.

**Share what you build:**
- Start a thread in [GitHub Discussions](https://github.com/YOUR_USERNAME/openassistant/discussions) to show a fork or customization
- Tag your GitHub repo with `openassistant` so others can find it
- When the plugin system ships (v0.3), tag plugins with `openassistant-plugin`

**Community channels:**
- [GitHub Issues](https://github.com/YOUR_USERNAME/openassistant/issues) — bug reports and feature requests
- [GitHub Discussions](https://github.com/YOUR_USERNAME/openassistant/discussions) — questions, ideas, show and tell

---

## Contributing

Contributions are welcome from everyone.

### Reporting a bug

Open an issue and include:
- Your OS and Python version
- What command you ran
- What happened vs. what you expected
- Output of `python check.py`

### Suggesting a feature

Open an issue describing what you want and why it's useful. Check the [Roadmap](#-roadmap) first — it may already be planned.

### Submitting a pull request

1. Fork the repo and clone your fork
2. Create a branch: `git checkout -b fix/your-fix` or `feature/your-feature`
3. Make your changes
4. Verify everything still works: `python check.py`, `python cli.py`, `python app.py`
5. Open a PR with a clear title and description

**Guidelines:**
- One fix or feature per PR — keep it focused
- Don't change existing CLI or web UI behavior without discussion
- If adding a dependency, explain why it's needed
- Match the existing code style

**Good first contributions:**
- Add a new system prompt mode to `config.py`
- Improve error messages
- Add to the FAQ
- Test on a new OS and report what works or doesn't
- Fix a typo

---

## License

[MIT](LICENSE) — use it, fork it, build on it, sell it. No restrictions.

The AI models downloaded via Ollama have their own licenses. Llama 3.1 uses Meta's community license, Mistral and Qwen 2.5 use Apache 2.0. See the [Ollama model library](https://ollama.com/library) for details on each model's license.

---

<div align="center">

Built with Python · Powered by Ollama · MIT Licensed

</div>
