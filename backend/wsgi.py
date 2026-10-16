"""Entry point for hosts: gunicorn wsgi:app

To run on your own computer, use start.py in the main folder instead: python start.py
"""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"\n  Graphite is running. Open http://127.0.0.1:{port} in your browser. Press Ctrl+C to stop.\n", flush=True)
    app.run(host="127.0.0.1", port=port, debug=not app.config["IS_PRODUCTION"], use_reloader=False)
