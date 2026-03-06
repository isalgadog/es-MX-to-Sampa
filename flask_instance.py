"""Flask entrypoint for the Spanish-to-SAMPA web interface.

This module wires HTTP routes to the transcription engine exposed by
``transcriber.transcriber`` and renders the single-page HTML template.
"""

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys

import transcriber

# ``template_folder='.'`` keeps compatibility with the current project layout,
# where ``index.html`` lives at repository root.
app = Flask(__name__, template_folder='.')

# Basic request-size protection for API/form payloads.
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024  # 2 KB

# Limit abuse by source IP at application level.
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per hour"],
)

# CORS policy comes from env var to avoid hardcoding dev origins in public code.
# Example:
#   CORS_ORIGINS=https://isalgadog.net,https://www.isalgadog.net
cors_origins_raw = os.getenv("CORS_ORIGINS", "https://isalgadog.net,https://www.isalgadog.net")
cors_origins = [origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()]

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": cors_origins,
        }
    },
)

MAX_WORD_LENGTH = 64


@app.after_request
def add_security_headers(response):
    """Add baseline security headers for defense-in-depth."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


def get_transcription(word: str) -> str:
    """Return the phonological transcription for a given input word.

    Args:
        word: Raw token submitted by the user.

    Returns:
        A SAMPA-like transcription string produced by the core transcriber.
    """
    return transcriber.transcriber(word)


@app.route('/api/transcribe', methods=['POST'])
@limiter.limit("30 per minute")
def api_transcribe():
    """JSON API endpoint for remote frontend clients.

    Expected payload:
        {"word": "..."}
    """
    data = request.get_json(silent=True) or {}
    word = str(data.get('word', '')).strip()

    if not word:
        return jsonify({"error": "word is required"}), 400

    if len(word) > MAX_WORD_LENGTH:
        return jsonify({"error": f"word too long (max {MAX_WORD_LENGTH} chars)"}), 400

    transcription_result = get_transcription(word)
    return jsonify({"transcription": transcription_result})


@app.route('/health')
def health_check():
    """Lightweight liveness probe used by external health checks."""
    return "ok", 200


@app.route('/', methods=['GET', 'POST'])
def home():
    """Render the home page and optionally process a submitted word.

    GET requests render the form-only page.
    POST requests look for ``word`` in form data, run transcription, and
    re-render the same template with both the original word and result.
    """
    if request.method == 'GET':
        return render_template('index.html')

    if 'word' in request.form:
        word = request.form['word'].strip()
        if len(word) > MAX_WORD_LENGTH:
            return render_template('index.html', transcriptionResult="Palabra demasiado larga", word=word)

        transcription_result = get_transcription(word)
        return render_template('index.html', transcriptionResult=transcription_result, word=word)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    # Enable Flask debug mode only when ``debug`` is explicitly passed.
    debug = 'debug' in sys.argv
    app.run(debug=debug)
