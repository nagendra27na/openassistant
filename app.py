from flask import Flask, render_template, request, Response, stream_with_context, jsonify
from assistant import Assistant
from config import PORT
import time
from collections import defaultdict

app = Flask(__name__)

# Limit incoming request bodies to 1MB — blocks oversized payload attacks
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB

# Max characters allowed in a single user message
MAX_MESSAGE_LENGTH = 4000

# Simple in-memory rate limiter: max requests per IP per window
RATE_LIMIT = 30          # max requests
RATE_WINDOW = 60         # per 60 seconds
_rate_store = defaultdict(list)

# One assistant instance per server (single-user; multi-user needs sessions)
assistant = Assistant()


# ── Security headers ──────────────────────────────────────────────────────────

@app.after_request
def set_security_headers(response):
    # Prevent the page from being embedded in iframes (clickjacking)
    response.headers["X-Frame-Options"] = "DENY"
    # Stop browsers from MIME-sniffing the response type
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Only allow resources from the same origin (blocks external script injection)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; "
        "script-src 'self' 'unsafe-inline'; "
        "connect-src 'self'; "
        "img-src 'self' data:;"
    )
    # Disable caching for API responses
    if request.path.startswith("/chat") or request.path.startswith("/mode"):
        response.headers["Cache-Control"] = "no-store"
    return response


# ── Rate limiting ─────────────────────────────────────────────────────────────

def is_rate_limited(ip: str) -> bool:
    now = time.time()
    window_start = now - RATE_WINDOW
    # Drop timestamps outside the window
    _rate_store[ip] = [t for t in _rate_store[ip] if t > window_start]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        return True
    _rate_store[ip].append(now)
    return False


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", mode=assistant.mode)


@app.route("/chat", methods=["POST"])
def chat():
    ip = request.remote_addr
    if is_rate_limited(ip):
        return jsonify({"error": "Too many requests. Slow down."}), 429

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Block oversized messages
    if len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({
            "error": f"Message too long. Max {MAX_MESSAGE_LENGTH} characters."
        }), 413

    def generate():
        for token in assistant.stream_chat(user_message):
            yield token

    return Response(stream_with_context(generate()), mimetype="text/plain")


@app.route("/reset", methods=["POST"])
def reset():
    assistant.reset()
    return jsonify({"status": "ok"})


@app.route("/mode", methods=["POST"])
def set_mode():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "")
    if assistant.set_mode(mode):
        return jsonify({"status": "ok", "mode": mode})
    return jsonify({"error": f"Unknown mode: {mode}"}), 400


# ── Error handlers ────────────────────────────────────────────────────────────

@app.errorhandler(413)
def request_too_large(e):
    return jsonify({"error": "Request too large (max 1MB)"}), 413


@app.errorhandler(429)
def too_many_requests(e):
    return jsonify({"error": "Too many requests"}), 429


if __name__ == "__main__":
    print(f"\n  OpenAssistant running at http://localhost:{PORT}\n")
    app.run(debug=False, port=PORT, host="127.0.0.1")
