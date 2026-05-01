import argparse
import sys
from assistant import Assistant
from config import DEFAULT_MODE, MODEL


BANNER = f"""
╔══════════════════════════════════════════╗
║         OpenAssistant                   ║
║  Model: {MODEL:<32}║
║  Type  /help  for commands               ║
╚══════════════════════════════════════════╝
"""

HELP_TEXT = """
Commands:
  /mode chat      Switch to general chat mode
  /mode code      Switch to code assistant mode
  /mode custom    Switch to custom mode
  /reset          Clear conversation history
  /help           Show this message
  /quit           Exit
"""


def main():
    parser = argparse.ArgumentParser(description="OpenAssistant CLI")
    parser.add_argument(
        "--mode",
        choices=["chat", "code", "custom"],
        default=DEFAULT_MODE,
        help="Starting mode (default: chat)",
    )
    args = parser.parse_args()

    assistant = Assistant(mode=args.mode)

    print(BANNER)
    print(f"Mode: {assistant.mode.upper()}\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            sys.exit(0)

        if not user_input:
            continue

        # Handle commands
        if user_input.startswith("/"):
            parts = user_input.split()
            cmd = parts[0].lower()

            if cmd == "/quit":
                print("Goodbye!")
                sys.exit(0)

            elif cmd == "/help":
                print(HELP_TEXT)

            elif cmd == "/reset":
                assistant.reset()
                print("✓ Conversation history cleared.\n")

            elif cmd == "/mode" and len(parts) == 2:
                new_mode = parts[1].lower()
                if assistant.set_mode(new_mode):
                    print(f"✓ Switched to {new_mode.upper()} mode. History cleared.\n")
                else:
                    print(f"Unknown mode '{new_mode}'. Use: chat, code, custom\n")
            else:
                print(f"Unknown command. Type /help for options.\n")

            continue

        # Stream the response
        print("Assistant: ", end="", flush=True)
        for token in assistant.stream_chat(user_input):
            print(token, end="", flush=True)
        print("\n")


if __name__ == "__main__":
    main()
