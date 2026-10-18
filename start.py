"""Start Graphite SAT on your computer.

    python start.py        (on Mac, use python3 if python isn't found)

Keep this terminal open while you use the site. Press Ctrl+C to stop it.
"""
import importlib.util
import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND = ROOT / "backend"
SITE = ROOT / "website" / "site"
PORTS = [8000, 8080, 5050, 5000]  # 5000 is last: on Macs, AirPlay Receiver often uses it


def say(text):
    print(f"\n  {text}", flush=True)


def stop(text):
    say(text)
    sys.exit(1)


if sys.version_info < (3, 10):
    stop(f"Graphite SAT needs Python 3.10 or newer. This is Python {sys.version.split()[0]}. "
         "Install a newer Python from python.org, then run this again.")

if not BACKEND.joinpath("app").exists():
    stop("Can't find the backend folder. Run this from the sat-courseprep folder, and run "
         "'git pull' if you downloaded the project before the backend was added.")

if importlib.util.find_spec("flask") is None:
    say("Installing Flask, the web framework Graphite SAT runs on...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    except subprocess.CalledProcessError:
        stop(f"Couldn't install Flask. Try running this yourself: {sys.executable} -m pip install flask")

# Encryption for photos and messages (cryptography) and photo resizing (Pillow).
for module, package in (("cryptography", "cryptography"), ("PIL", "pillow")):
    if importlib.util.find_spec(module) is None:
        say(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            stop(f"Couldn't install {package}. Try running this yourself: {sys.executable} -m pip install -r requirements.txt")

if not SITE.joinpath("index.html").exists():
    say("Building the website pages...")
    if importlib.util.find_spec("PIL") is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    subprocess.check_call([sys.executable, str(ROOT / "website" / "build.py")])


def port_is_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return True
        except OSError:
            return False


wanted = os.environ.get("PORT")
candidates = [int(wanted)] if wanted else PORTS
port = next((p for p in candidates if port_is_free(p)), None)
if port is None:
    stop(f"Ports {', '.join(map(str, candidates))} are all in use. Close other servers, or set PORT to a free number.")

url = f"http://127.0.0.1:{port}"
os.environ.setdefault("BASE_URL", url)
sys.path.insert(0, str(BACKEND))
from app import create_app  # noqa: E402  (imported after the checks above)

app = create_app()
say(f"Graphite SAT is running. Open {url} in your browser.")
say("Keep this terminal open while you use the site. Press Ctrl+C to stop.\n")
app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)
