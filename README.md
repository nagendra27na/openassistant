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
git clone https://github.com/nagendra27na/openassistant.git
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
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
brew install ollama
ollama serve &
ollama pull llama3.1
git clone https://github.com/nagendra27na/openassistant.git
cd openassistant
pip3 install -r requirements.txt
python3 check.py
python3 app.py
```

---

### Windows

1. Download and install **Python 3.9+** from [python.org](https://www.python.org/downloads/windows/)
   > During install: check **"Add Python to PATH"**

2. Download and install **Ollama** from [ollama.com/download](https://ollama.com/download)

3. Open **Command Prompt** or **PowerShell**:

```cmd
ollama pull llama3.1
git clone https://github.com/nagendra27na/openassistant.git
cd openassistant
pip install -r requirements.txt
python check.py
python app.py
```

4. Open [http://localhost:5000](http://localhost:5000) in your browser

> No Git? Download the ZIP from the green **Code** button, extract it, open a terminal in that folder, then run from step 3.

---

### Linux — Ubuntu / Debian

```bash
sudo apt update
sudo apt install python3 python3-pip git -y
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
git clone https://github.com/nagendra27na/openassistant.git
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
git clone https://github.com/nagendra27na/openassistant.git
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
git clone https://github.com/nagendra27na/openassistant.git
cd openassistant
pip install -r requirements.txt
python check.py
python app.py
```

---

### Using a virtual environment (recommended)

```bash
python3 -m venv venv        # macOS/Linux
python -m venv venv          # Windows

source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows

pip install -r requirements.txt
python check.py
python app.py
```

Deactivate with: `deactivate`

---

### Switching models

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
python cli.py
python cli.py --mode code
python cli.py --mode custom
```

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
MODEL = "llama3.1"
PORT  = 5000

SYSTEM_PROMPTS = {
    "custom": "You are a specialized assistant for..."
}
```

---

## Project Structure
openassistant/
├── app.py
├── cli.py
├── assistant.py
├── config.py
├── check.py
├── requirements.txt
├── templates/
│   └── index.html
├── INSTALL.md
└── README.md

---

## FAQ

**Does it need the internet to run?**
Only to download the model the first time. After that it works fully offline.

**Is my data private?**
Yes. Everything runs on your machine. Nothing is sent to any server.

**What hardware do I need?**
At least 8GB RAM. The default model uses ~5-6GB. For low-RAM machines use `phi3` (~4GB).

**Does it work on Apple Silicon (M1/M2/M3/M4)?**
Yes. Ollama has native Apple Silicon support.

**Is this actually free?**
Yes. Ollama is free. Models are free. Code is MIT licensed. No catch.

**Can I use a different model?**
Yes — any model in the [Ollama library](https://ollama.com/library). Change `MODEL` in `config.py`.

**Can I run multiple users at once?**
Not yet. Multi-user support is planned for v0.2.

**Can I build my own chatbot on top of this?**
Yes. MIT license — use, modify, fork, redistribute freely.

**Ollama keeps stopping.**
Linux: `sudo systemctl enable ollama`. macOS: menu bar app starts with login. Windows: system tray app.

**Port already in use error.**
Change `PORT = 5000` to `5001` in `config.py`.

---

## Roadmap

### v0.2 — Multi-user & persistence
- [ ] Per-user sessions in web UI
- [ ] Save and load conversations to disk
- [ ] Conversation history browser

### v0.3 — Files & plugins
- [ ] File upload — ask questions about PDFs and documents
- [ ] Plugin API — add custom tools
- [ ] Model selector in web UI

### v0.4 — Voice & export
- [ ] Voice input via browser microphone
- [ ] Export conversations as Markdown or PDF
- [ ] Docker image

### v1.0 — Full featured
- [ ] Persistent memory across sessions
- [ ] Conversation search
- [ ] Full plugin ecosystem

Have a feature idea? [Open an issue](https://github.com/nagendra27na/openassistant/issues).

---

## Development

```bash
git clone https://github.com/nagendra27na/openassistant.git
cd openassistant
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Dev mode:
```bash
FLASK_DEBUG=1 python app.py        # macOS/Linux
set FLASK_DEBUG=1 && python app.py  # Windows
```

---

## Telemetry

**OpenAssistant collects zero telemetry.**

No usage stats, no crash reports, no analytics. The only outbound request goes to `http://localhost:11434` — your own machine. Verify it yourself in `assistant.py`.

---

## Community & Plugins

Plugin system coming in v0.3. Until then:

- Fork and customize `SYSTEM_PROMPTS["custom"]` in `config.py`
- Share your fork in [GitHub Discussions](https://github.com/nagendra27na/openassistant/discussions)
- Tag your repo with `openassistant`
- [GitHub Issues](https://github.com/nagendra27na/openassistant/issues) — bugs and features
- [GitHub Discussions](https://github.com/nagendra27na/openassistant/discussions) — questions and ideas

---

## Contributing

**Reporting a bug** — open an issue with your OS, Python version, command you ran, and output of `python check.py`.

**Suggesting a feature** — open an issue. Check the roadmap first.

**Pull request steps:**
1. Fork and clone
2. Create a branch: `git checkout -b fix/your-fix`
3. Make changes
4. Run: `python check.py`, `python cli.py`, `python app.py`
5. Open a PR

**Good first contributions:** new system prompt mode, better error messages, FAQ additions, typo fixes.

---

## License

[MIT](LICENSE) — use it, fork it, build on it, sell it.

Model licenses: Llama 3.1 uses Meta's community license. Mistral and Qwen 2.5 use Apache 2.0.

---

<div align="center">

Built with Python · Powered by Ollama · MIT Licensed

</div>
