"""A small Qwen client: one chat call over the OpenAI-compatible API, with no extra packages to install.

The tutor switches on when QWEN_API_KEY or QWEN_BASE_URL is set (see backend/README.md, "Connect the tutor").
Until then, is_live() is False and the tutor page says the tutor is coming soon.

The same call works against every place Qwen runs:
  - Alibaba Cloud Model Studio (DashScope), the default: set QWEN_API_KEY (sk-...) and leave QWEN_BASE_URL unset.
  - Your own server: set QWEN_BASE_URL to its /v1 address, for example Ollama (http://localhost:11434/v1)
    or vLLM (http://your-gpu-box:8000/v1), and QWEN_MODEL to the model name it serves. A key is only sent if set.
"""
import json
import re
import urllib.error
import urllib.request

from flask import current_app

# Model Studio's international endpoint. Mainland China accounts use https://dashscope.aliyuncs.com/compatible-mode/v1.
DEFAULT_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
# Qwen3 models can think out loud first. The student only sees the answer.
THINKING = re.compile(r"<think>.*?</think>\s*", re.S)


class QwenError(Exception):
    pass


def api_key():
    return current_app.config.get("QWEN_API_KEY") or ""


def base_url():
    return (current_app.config.get("QWEN_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def model():
    return current_app.config.get("QWEN_MODEL") or "qwen-plus"


def is_live():
    """True once there's somewhere to send questions: a Model Studio key, or the address of your own Qwen server."""
    return bool(api_key() or current_app.config.get("QWEN_BASE_URL"))


def request(payload):
    """POSTs to /chat/completions and returns the JSON. Tests replace this function."""
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key():
        headers["Authorization"] = f"Bearer {api_key()}"
    req = urllib.request.Request(base_url() + "/chat/completions", data=json.dumps(payload).encode(),
                                 method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=current_app.config.get("QWEN_TIMEOUT", 60)) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as err:
        try:
            message = json.loads(err.read().decode())["error"]["message"]
        except Exception:  # noqa: BLE001  (any unreadable error body)
            message = f"Qwen answered {err.code}."
        current_app.logger.warning("Qwen chat failed (%s): %s", err.code, message)
        raise QwenError("The tutor couldn't answer just now. Try again in a moment.") from err
    except (urllib.error.URLError, TimeoutError) as err:
        current_app.logger.warning("Couldn't reach Qwen at %s: %s", base_url(), err)
        raise QwenError("We couldn't reach the tutor. Try again in a moment.") from err


def chat(messages, temperature=0.4, max_tokens=900):
    """Sends [{role, content}, ...] and returns the reply's text."""
    data = request({"model": model(), "messages": messages, "temperature": temperature, "max_tokens": max_tokens})
    try:
        text = data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        current_app.logger.warning("Qwen sent a reply with no message: %s", str(data)[:300])
        raise QwenError("The tutor couldn't answer just now. Try again in a moment.") from None
    text = THINKING.sub("", text).strip()
    if not text:
        raise QwenError("The tutor came back empty. Try asking another way.")
    return text
