import requests
import json
from config import MODEL, OLLAMA_URL, SYSTEM_PROMPTS, DEFAULT_MODE


# Max number of message pairs kept in history to avoid exceeding model context window.
# Each pair = 1 user message + 1 assistant reply. 20 pairs = 40 messages max.
MAX_HISTORY_PAIRS = 20


class Assistant:
    def __init__(self, mode: str = DEFAULT_MODE):
        self.mode = mode if mode in SYSTEM_PROMPTS else DEFAULT_MODE
        self.history = []
        self.system_prompt = SYSTEM_PROMPTS[self.mode]

    def _trim_history(self):
        """Keep history within MAX_HISTORY_PAIRS to avoid context window overflow."""
        max_messages = MAX_HISTORY_PAIRS * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]

    def chat(self, user_message: str) -> str:
        """Send a message and get a response. Maintains conversation history."""
        self.history.append({"role": "user", "content": user_message})
        self._trim_history()

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                *self.history,
            ],
            "stream": False,
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            reply = data["message"]["content"]
            self.history.append({"role": "assistant", "content": reply})
            return reply

        except requests.exceptions.ConnectionError:
            self.history.pop()  # remove unanswered user message
            return "❌ Cannot connect to Ollama. Make sure it's running: open a terminal and run `ollama serve`"
        except requests.exceptions.Timeout:
            self.history.pop()
            return "❌ Request timed out. The model may be loading — try again in a moment."
        except Exception as e:
            self.history.pop()
            return f"❌ Error: {str(e)}"

    def stream_chat(self, user_message: str):
        """Stream a response token by token. Yields string chunks."""
        self.history.append({"role": "user", "content": user_message})
        self._trim_history()

        payload = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                *self.history,
            ],
            "stream": True,
        }

        full_reply = ""

        try:
            with requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        token = chunk.get("message", {}).get("content", "")
                        full_reply += token
                        yield token
                        if chunk.get("done"):
                            break
        except requests.exceptions.ConnectionError:
            # Remove the user message we just appended — history would be corrupted
            self.history.pop()
            yield "❌ Cannot connect to Ollama. Make sure it's running: `ollama serve`"
            return
        except requests.exceptions.Timeout:
            self.history.pop()
            yield "❌ Request timed out. The model may still be loading — try again."
            return
        except Exception as e:
            self.history.pop()
            yield f"❌ Error: {str(e)}"
            return

        # Only save to history if we got a real reply
        if full_reply:
            self.history.append({"role": "assistant", "content": full_reply})

    def reset(self):
        """Clear conversation history."""
        self.history = []

    def set_mode(self, mode: str):
        """Switch assistant mode and reset history."""
        if mode in SYSTEM_PROMPTS:
            self.mode = mode
            self.system_prompt = SYSTEM_PROMPTS[mode]
            self.reset()
            return True
        return False
