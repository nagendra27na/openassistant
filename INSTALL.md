# Installation Guide

Step-by-step setup for **macOS**, **Windows**, and **Linux**.

---

## macOS

### 1. Install Python 3.9+

Check if you already have it:
```bash
python3 --version
```

If not installed or below 3.9, install via [Homebrew](https://brew.sh):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

Or download directly from [python.org](https://www.python.org/downloads/).

### 2. Install Ollama

Download from [https://ollama.com/download](https://ollama.com/download) and run the `.dmg` installer.

Ollama will appear in your menu bar. Click it and select **"Start"** to run it.

Alternatively via Homebrew:
```bash
brew install ollama
ollama serve   # run in background
```

### 3. Pull the model

```bash
ollama pull llama3.1
```

This downloads ~5GB. Takes a few minutes depending on connection speed.

### 4. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip3 install -r requirements.txt
```

### 5. Verify setup

```bash
python3 check.py
```

### 6. Run

```bash
# Web UI (open http://localhost:5000 in browser)
python3 app.py

# CLI
python3 cli.py
```

---

## Windows

### 1. Install Python 3.9+

Download the installer from [python.org](https://www.python.org/downloads/windows/).

> ⚠️ **Important:** During installation, check **"Add Python to PATH"** before clicking Install.

Verify in a new Command Prompt or PowerShell window:
```cmd
python --version
```

### 2. Install Ollama

Download the Windows installer from [https://ollama.com/download](https://ollama.com/download) and run it.

After installation, Ollama runs in the system tray. It starts automatically.

### 3. Pull the model

Open **Command Prompt** or **PowerShell**:
```cmd
ollama pull llama3.1
```

### 4. Clone and install

If you have Git installed:
```cmd
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip install -r requirements.txt
```

No Git? Download the ZIP from the GitHub repo page (green **Code** button → **Download ZIP**), extract it, then open a terminal in that folder and run:
```cmd
pip install -r requirements.txt
```

### 5. Verify setup

```cmd
python check.py
```

### 6. Run

```cmd
# Web UI
python app.py

# CLI
python cli.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser for the web UI.

> 💡 **Windows Firewall:** If prompted, allow Python through the firewall to access the local network.

---

## Linux

### Ubuntu / Debian

```bash
# 1. Install Python and pip
sudo apt update
sudo apt install python3 python3-pip git -y

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. Start Ollama (runs as a background service automatically after install)
# If it's not running:
ollama serve &

# 4. Pull the model
ollama pull llama3.1

# 5. Clone and install
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip3 install -r requirements.txt

# 6. Verify
python3 check.py

# 7. Run
python3 app.py    # web UI at http://localhost:5000
python3 cli.py    # terminal
```

### Fedora / RHEL / CentOS

```bash
# 1. Install Python and pip
sudo dnf install python3 python3-pip git -y

# 2. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 3. Pull the model
ollama pull llama3.1

# 4. Clone and install
git clone https://github.com/YOUR_USERNAME/openassistant.git
cd openassistant
pip3 install -r requirements.txt

# 5. Verify and run
python3 check.py
python3 app.py
```

### Arch Linux

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

## Using a Virtual Environment (recommended)

Keeps dependencies isolated from your system Python. Works on all OSes.

```bash
# Create venv
python3 -m venv venv          # macOS/Linux
python -m venv venv            # Windows

# Activate
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

# Install
pip install -r requirements.txt

# Run
python app.py
python cli.py
```

To deactivate: `deactivate`

---

## Switching Models

Edit `config.py` and change `MODEL`:

| Model | Command to pull | RAM needed | Best for |
|---|---|---|---|
| `llama3.1` | `ollama pull llama3.1` | 8GB | General use (default) |
| `mistral` | `ollama pull mistral` | 6GB | Fast responses |
| `qwen2.5` | `ollama pull qwen2.5` | 6GB | Code tasks |
| `llama3.1:70b` | `ollama pull llama3.1:70b` | 40GB | Maximum quality |

---

## Troubleshooting

**"Cannot connect to Ollama"**
- macOS/Windows: Make sure the Ollama app is open (check menu bar / system tray)
- Linux: Run `ollama serve` in a separate terminal

**"Model not found"**
- Run `ollama pull llama3.1` again

**"pip not found" on macOS/Linux**
- Use `pip3` instead of `pip`

**Port 5000 already in use**
- Change `PORT` in `config.py` to another number (e.g. `5001`)

**Slow responses**
- Normal on first run — model loads into memory
- Subsequent responses will be faster
- If always slow, try a smaller model like `mistral`

**Python not found on Windows**
- Re-run the Python installer and check "Add Python to PATH"
- Or use the full path: `C:\Users\YOU\AppData\Local\Programs\Python\Python3xx\python.exe`
