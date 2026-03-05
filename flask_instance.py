"""Flask entrypoint for the Spanish-to-SAMPA web interface.

This module wires HTTP routes to the transcription engine exposed by
``transcriber.transcriber`` and renders the single-page HTML template.
"""

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import sys

import transcriber

# ``template_folder='.'`` keeps compatibility with the current project layout,
# where ``index.html`` lives at repository root.
app = Flask(__name__, template_folder='.')

# CORS is restricted to your public site origins for /api/* routes.
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://isalgadog.net",
                "https://www.isalgadog.net",
                "http://localhost:3000",
                "http://127.0.0.1:5500",
            ]
        }
    },
)


def get_transcription(word: str) -> str:
    """Return the phonological transcription for a given input word.

    Args:
        word: Raw token submitted by the user.

    Returns:
        A SAMPA-like transcription string produced by the core transcriber.
    """
    return transcriber.transcriber(word)


@app.route('/api/transcribe', methods=['POST'])
def api_transcribe():
    """JSON API endpoint for remote frontend clients.

    Expected payload:
        {"word": "..."}
    """
    data = request.get_json(silent=True) or {}
    word = str(data.get('word', '')).strip()

    if not word:
        return jsonify({"error": "word is required"}), 400

    transcription_result = get_transcription(word)
    return jsonify({"transcription": transcription_result})


@app.route('/health')
@app.route('/healthCheck')
@app.route('/healtCheck')
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
        word = request.form['word']
        transcription_result = get_transcription(word)
        return render_template('index.html', transcriptionResult=transcription_result, word=word)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    # Enable Flask debug mode only when ``debug`` is explicitly passed.
    debug = 'debug' in sys.argv
    app.run(debug=debug)
