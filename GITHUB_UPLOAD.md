# How to Upload OpenAssistant to GitHub

Step-by-step for macOS, Windows, and Linux.

---

## Before you start

You need:
- A GitHub account — create one free at [github.com](https://github.com)
- Git installed on your machine
- The OpenAssistant project folder on your computer

---

## Step 1 — Install Git

### macOS
```bash
git --version
```
If not installed, macOS will prompt you to install it. Or use Homebrew:
```bash
brew install git
```

### Windows
Download Git from [https://git-scm.com/download/win](https://git-scm.com/download/win) and run the installer.
Accept all defaults. After install, open **Git Bash** (installed with Git) for all commands below.

### Linux (Ubuntu/Debian)
```bash
sudo apt install git -y
```

### Linux (Fedora)
```bash
sudo dnf install git -y
```

Verify Git is installed on any OS:
```bash
git --version
```

---

## Step 2 — Configure Git with your name and email

This only needs to be done once. Use the same email as your GitHub account.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## Step 3 — Create a new repository on GitHub

1. Go to [https://github.com/new](https://github.com/new)
2. Fill in:
   - **Repository name:** `openassistant`
   - **Description:** `Free, local, open-source AI assistant — no API keys, no cloud`
   - **Visibility:** Public
   - **DO NOT** check "Add a README file" — you already have one
3. Click **Create repository**
4. GitHub will show you a page with a URL. Copy the HTTPS URL — it looks like:
   ```
   https://github.com/YOUR_USERNAME/openassistant.git
   ```

---

## Step 4 — Open a terminal in your project folder

### macOS / Linux
```bash
cd path/to/openassistant
```
Example: `cd ~/Downloads/openassistant`

### Windows (Git Bash)
```bash
cd /c/Users/YourName/Downloads/openassistant
```
Or right-click the folder in File Explorer → **Git Bash Here**

---

## Step 5 — Initialize Git and make your first commit

Run these commands one at a time:

```bash
# Initialize a new Git repository in the folder
git init

# Stage all files for commit
git add .

# Check what will be committed (optional but recommended)
git status

# Make your first commit
git commit -m "Initial release: OpenAssistant v0.1"
```

You should see output listing all the files being committed.

---

## Step 6 — Connect to GitHub and push

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Point your local repo to GitHub
git remote add origin https://github.com/YOUR_USERNAME/openassistant.git

# Rename the default branch to 'main' (GitHub's standard)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

Git will ask for your GitHub username and password.

> ⚠️ **Important:** GitHub no longer accepts your account password here.
> You need a **Personal Access Token** instead. See Step 7.

---

## Step 7 — Create a Personal Access Token (if asked for password)

1. Go to [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)
2. Note: `openassistant push`
3. Expiration: 90 days (or No expiration if you prefer)
4. Scopes: check **repo** (full control of repositories)
5. Click **Generate token**
6. Copy the token — you will only see it once
7. When Git asks for your password, paste the token instead

To avoid entering it every time:
```bash
git config --global credential.helper store
```
Then push once — Git will remember the token.

---

## Step 8 — Verify it worked

Go to `https://github.com/YOUR_USERNAME/openassistant` in your browser.

You should see all your files and the README displayed on the page.

---

## Making changes and pushing updates

After the first push, updating GitHub is just 3 commands:

```bash
# Stage changed files
git add .

# Commit with a message describing what changed
git commit -m "Fix: improved error handling in assistant.py"

# Push to GitHub
git push
```

---

## Useful Git commands

| Command | What it does |
|---|---|
| `git status` | Shows which files changed |
| `git log --oneline` | Shows commit history |
| `git diff` | Shows exactly what changed in each file |
| `git add filename.py` | Stage a specific file only |
| `git add .` | Stage all changed files |
| `git push` | Push latest commits to GitHub |

---

## Running the tests before pushing (recommended)

Always run the test suite before pushing a new version:

```bash
python test_suite.py
```

If all tests pass, then commit and push. If any fail, fix them first.

---

## Adding a GitHub topic tag (helps people find your project)

1. Go to your repo page on GitHub
2. Click the gear icon next to **About**
3. Under **Topics**, add: `ai`, `llm`, `ollama`, `open-source`, `local-ai`, `python`, `flask`
4. Click **Save changes**

This helps other GitHub users discover your project through search.

---

## Releases (optional — for publishing versioned downloads)

When you want to mark a stable version:

1. Go to your repo → **Releases** → **Draft a new release**
2. Tag version: `v0.1.0`
3. Title: `OpenAssistant v0.1.0 — Initial Release`
4. Write release notes (what's included, how to install)
5. Click **Publish release**

Users can then download a ZIP of exactly that version.
