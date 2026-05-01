"""
OpenAssistant Test Suite
Tests config, assistant logic, app routes, security, and edge cases.
No Ollama needed — all AI calls are mocked.
"""

import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# ── Helpers ───────────────────────────────────────────────────────────────────

PASS = "  PASS"
FAIL = "  FAIL"

def section(title):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")

# ── 1. Config Tests ───────────────────────────────────────────────────────────

section("1 · Config")

from config import MODEL, OLLAMA_URL, PORT, SYSTEM_PROMPTS, DEFAULT_MODE

def test_config_model():
    assert isinstance(MODEL, str) and len(MODEL) > 0, "MODEL must be non-empty string"
    print(f"{PASS}  MODEL = '{MODEL}'")

def test_config_url():
    assert OLLAMA_URL.startswith("http://localhost"), "OLLAMA_URL must be local"
    print(f"{PASS}  OLLAMA_URL = '{OLLAMA_URL}'")

def test_config_port():
    assert isinstance(PORT, int) and 1024 <= PORT <= 65535, "PORT must be valid"
    print(f"{PASS}  PORT = {PORT}")

def test_config_prompts():
    for key in ["chat", "code", "custom"]:
        assert key in SYSTEM_PROMPTS, f"Missing mode: {key}"
        assert len(SYSTEM_PROMPTS[key]) > 10, f"Prompt '{key}' too short"
    print(f"{PASS}  SYSTEM_PROMPTS has all 3 modes")

def test_config_default_mode():
    assert DEFAULT_MODE in SYSTEM_PROMPTS, "DEFAULT_MODE must exist in SYSTEM_PROMPTS"
    print(f"{PASS}  DEFAULT_MODE = '{DEFAULT_MODE}'")

test_config_model()
test_config_url()
test_config_port()
test_config_prompts()
test_config_default_mode()

# ── 2. Assistant Unit Tests ───────────────────────────────────────────────────

section("2 · Assistant — Unit Logic")

from assistant import Assistant, MAX_HISTORY_PAIRS

def make_mock_response(content="Hello!", stream=False):
    """Build a mock requests.Response for Ollama."""
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {"message": {"content": content}}
    if stream:
        lines = [
            json.dumps({"message": {"content": c}, "done": False}).encode()
            for c in list(content)
        ]
        lines.append(json.dumps({"message": {"content": ""}, "done": True}).encode())
        mock.iter_lines.return_value = lines
        mock.__enter__ = lambda s: s
        mock.__exit__ = MagicMock(return_value=False)
    return mock

def test_default_mode():
    a = Assistant()
    assert a.mode == DEFAULT_MODE
    assert a.history == []
    print(f"{PASS}  Assistant initialises with default mode and empty history")

def test_invalid_mode_falls_back():
    a = Assistant(mode="nonexistent")
    assert a.mode == DEFAULT_MODE
    print(f"{PASS}  Invalid mode falls back to DEFAULT_MODE")

def test_set_mode_valid():
    a = Assistant()
    result = a.set_mode("code")
    assert result is True
    assert a.mode == "code"
    print(f"{PASS}  set_mode('code') succeeds and updates mode")

def test_set_mode_invalid():
    a = Assistant()
    result = a.set_mode("hacker")
    assert result is False
    assert a.mode == DEFAULT_MODE
    print(f"{PASS}  set_mode('hacker') returns False, mode unchanged")

def test_set_mode_resets_history():
    a = Assistant()
    a.history = [{"role": "user", "content": "hi"}]
    a.set_mode("code")
    assert a.history == []
    print(f"{PASS}  set_mode() clears history")

def test_reset():
    a = Assistant()
    a.history = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hey"}]
    a.reset()
    assert a.history == []
    print(f"{PASS}  reset() clears history")

def test_history_cap():
    a = Assistant()
    # Fill history beyond the cap
    for i in range(MAX_HISTORY_PAIRS * 2 + 10):
        a.history.append({"role": "user", "content": f"msg {i}"})
        a.history.append({"role": "assistant", "content": f"reply {i}"})
    a._trim_history()
    assert len(a.history) <= MAX_HISTORY_PAIRS * 2
    print(f"{PASS}  _trim_history() caps at {MAX_HISTORY_PAIRS * 2} messages")

def test_chat_success():
    a = Assistant()
    with patch("requests.post", return_value=make_mock_response("Hi there!")):
        reply = a.chat("Hello")
    assert reply == "Hi there!"
    assert len(a.history) == 2
    assert a.history[0]["role"] == "user"
    assert a.history[1]["role"] == "assistant"
    print(f"{PASS}  chat() returns reply and saves both sides to history")

def test_chat_no_history_corruption_on_error():
    a = Assistant()
    import requests as req
    with patch("requests.post", side_effect=req.exceptions.ConnectionError):
        reply = a.chat("Hello")
    assert "Cannot connect" in reply
    assert a.history == [], f"History should be empty, got: {a.history}"
    print(f"{PASS}  chat() pops user message from history on connection error")

def test_chat_timeout_no_corruption():
    a = Assistant()
    import requests as req
    with patch("requests.post", side_effect=req.exceptions.Timeout):
        reply = a.chat("Hello")
    assert "timed out" in reply
    assert a.history == []
    print(f"{PASS}  chat() pops user message from history on timeout")

def test_stream_chat_success():
    a = Assistant()
    mock_resp = make_mock_response("Hello world", stream=True)
    with patch("requests.post", return_value=mock_resp):
        tokens = list(a.stream_chat("Hi"))
    full = "".join(tokens)
    assert len(full) > 0
    assert len(a.history) == 2
    print(f"{PASS}  stream_chat() yields tokens and saves history")

def test_stream_chat_no_history_corruption_on_error():
    a = Assistant()
    import requests as req
    with patch("requests.post", side_effect=req.exceptions.ConnectionError):
        tokens = list(a.stream_chat("Hello"))
    assert any("Cannot connect" in t for t in tokens)
    assert a.history == []
    print(f"{PASS}  stream_chat() pops user message on connection error")

test_default_mode()
test_invalid_mode_falls_back()
test_set_mode_valid()
test_set_mode_invalid()
test_set_mode_resets_history()
test_reset()
test_history_cap()
test_chat_success()
test_chat_no_history_corruption_on_error()
test_chat_timeout_no_corruption()
test_stream_chat_success()
test_stream_chat_no_history_corruption_on_error()

# ── 3. Flask Route Tests ──────────────────────────────────────────────────────

section("3 · Flask Routes")

from app import app as flask_app
flask_app.config["TESTING"] = True
client = flask_app.test_client()

def test_index_route():
    r = client.get("/")
    assert r.status_code == 200
    assert b"OpenAssistant" in r.data
    print(f"{PASS}  GET / returns 200 with page content")

def test_chat_empty_body():
    r = client.post("/chat", data="", content_type="application/json")
    assert r.status_code == 400
    print(f"{PASS}  POST /chat with empty body returns 400")

def test_chat_empty_message():
    r = client.post("/chat", json={"message": "   "})
    assert r.status_code == 400
    print(f"{PASS}  POST /chat with whitespace-only message returns 400")

def test_chat_missing_message_key():
    r = client.post("/chat", json={"not_message": "hello"})
    assert r.status_code == 400
    print(f"{PASS}  POST /chat with wrong key returns 400")

def test_chat_message_too_long():
    r = client.post("/chat", json={"message": "x" * 5000})
    assert r.status_code == 413
    print(f"{PASS}  POST /chat with 5000-char message returns 413")

def test_chat_valid_message():
    mock_resp = make_mock_response("Hi!", stream=True)
    with patch("assistant.requests.post", return_value=mock_resp):
        r = client.post("/chat", json={"message": "Hello"})
    assert r.status_code == 200
    print(f"{PASS}  POST /chat with valid message returns 200")

def test_reset_route():
    r = client.post("/reset")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert data["status"] == "ok"
    print(f"{PASS}  POST /reset returns 200 with ok status")

def test_mode_valid():
    r = client.post("/mode", json={"mode": "code"})
    assert r.status_code == 200
    data = json.loads(r.data)
    assert data["status"] == "ok"
    print(f"{PASS}  POST /mode with 'code' returns 200")

def test_mode_invalid():
    r = client.post("/mode", json={"mode": "hacker"})
    assert r.status_code == 400
    print(f"{PASS}  POST /mode with unknown mode returns 400")

def test_mode_missing_body():
    r = client.post("/mode", data="", content_type="application/json")
    assert r.status_code == 400
    print(f"{PASS}  POST /mode with missing body returns 400")

test_index_route()
test_chat_empty_body()
test_chat_empty_message()
test_chat_missing_message_key()
test_chat_message_too_long()
test_chat_valid_message()
test_reset_route()
test_mode_valid()
test_mode_invalid()
test_mode_missing_body()

# ── 4. Security Header Tests ──────────────────────────────────────────────────

section("4 · Security Headers")

def test_xframe_options():
    r = client.get("/")
    assert r.headers.get("X-Frame-Options") == "DENY"
    print(f"{PASS}  X-Frame-Options: DENY (clickjacking protection)")

def test_content_type_options():
    r = client.get("/")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    print(f"{PASS}  X-Content-Type-Options: nosniff (MIME sniffing protection)")

def test_csp_header_present():
    r = client.get("/")
    csp = r.headers.get("Content-Security-Policy", "")
    assert "default-src 'self'" in csp
    print(f"{PASS}  Content-Security-Policy present with default-src 'self'")

def test_csp_blocks_external_scripts():
    r = client.get("/")
    csp = r.headers.get("Content-Security-Policy", "")
    assert "script-src 'self'" in csp
    print(f"{PASS}  CSP restricts scripts to 'self' (blocks external script injection)")

test_xframe_options()
test_content_type_options()
test_csp_header_present()
test_csp_blocks_external_scripts()

# ── 5. XSS Prevention Tests ───────────────────────────────────────────────────

section("5 · XSS Prevention (renderMarkdown logic)")

# Simulate the escapeHtml + renderMarkdown logic in Python for testing
import re

def escape_html(text):
    mapping = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"}
    return re.sub(r'[&<>"\']', lambda m: mapping[m.group()], text)

def render_markdown(text):
    code_blocks, inline_codes = [], []
    def save_block(m):
        code_blocks.append(m.group(1))
        return f"\x00CODE{len(code_blocks)-1}\x00"
    def save_inline(m):
        inline_codes.append(m.group(1))
        return f"\x00INLINE{len(inline_codes)-1}\x00"
    text = re.sub(r'```[\w]*\n?([\s\S]*?)```', save_block, text)
    text = re.sub(r'`([^`]+)`', save_inline, text)
    text = escape_html(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = text.replace("\n", "<br>")
    text = re.sub(r'\x00CODE(\d+)\x00', lambda m: f"<pre><code>{escape_html(code_blocks[int(m.group(1))])}</code></pre>", text)
    text = re.sub(r'\x00INLINE(\d+)\x00', lambda m: f"<code>{escape_html(inline_codes[int(m.group(1))])}</code>", text)
    return text

def test_xss_script_tag_blocked():
    result = render_markdown("<script>alert('xss')</script>")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result
    print(f"{PASS}  <script> tags are escaped, not executed")

def test_xss_img_onerror_blocked():
    result = render_markdown('<img src=x onerror=alert(1)>')
    assert "onerror" not in result or "&lt;" in result
    print(f"{PASS}  <img onerror=...> is escaped")

def test_xss_in_code_block_blocked():
    result = render_markdown("```\n<script>evil()</script>\n```")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result
    print(f"{PASS}  <script> inside code block is escaped")

def test_xss_in_inline_code_blocked():
    result = render_markdown("`<script>evil()</script>`")
    assert "<script>" not in result
    print(f"{PASS}  <script> inside inline code is escaped")

def test_bold_still_works():
    result = render_markdown("**hello**")
    assert "<strong>hello</strong>" in result
    print(f"{PASS}  **bold** markdown still renders correctly")

def test_newlines_still_work():
    result = render_markdown("line1\nline2")
    assert "<br>" in result
    print(f"{PASS}  Newlines still convert to <br>")

test_xss_script_tag_blocked()
test_xss_img_onerror_blocked()
test_xss_in_code_block_blocked()
test_xss_in_inline_code_blocked()
test_bold_still_works()
test_newlines_still_work()

# ── 6. Rate Limiting Test ─────────────────────────────────────────────────────

section("6 · Rate Limiting")

def test_rate_limit_triggers():
    from app import _rate_store, RATE_LIMIT, RATE_WINDOW
    import time
    # Simulate a fresh IP
    test_ip = "10.0.0.99"
    _rate_store[test_ip] = []
    now = time.time()
    # Fill up the rate window
    _rate_store[test_ip] = [now] * RATE_LIMIT
    mock_resp = make_mock_response("Hi", stream=True)
    with patch("assistant.requests.post", return_value=mock_resp):
        r = client.post(
            "/chat",
            json={"message": "Hello"},
            environ_base={"REMOTE_ADDR": test_ip}
        )
    assert r.status_code == 429, f"Expected 429, got {r.status_code}"
    print(f"{PASS}  Rate limit triggers 429 after {RATE_LIMIT} requests in {RATE_WINDOW}s")

test_rate_limit_triggers()

# ── Summary ───────────────────────────────────────────────────────────────────

print(f"\n{'═'*50}")
print(f"  ALL TESTS PASSED")
print(f"{'═'*50}\n")

