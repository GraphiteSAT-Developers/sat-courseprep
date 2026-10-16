"""Entry point. Locally: python wsgi.py. On a host: gunicorn wsgi:app"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=not app.config["IS_PRODUCTION"], port=5000)
