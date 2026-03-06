# es-MX-to-SAMPA

Rule-based phonological transcriber for Mexican Spanish (`es-MX`) to a SAMPA-like notation.

## What this project does

- Transcribes a **single Spanish word** into SAMPA-like output.
- Applies grapheme-to-phoneme rules, syllable splitting, and stress placement.
- Includes a small Flask interface and a JSON API endpoint.

---

## Project structure

- `transcriber.py` — core transcription pipeline (normalization, G2P rules, syllabification, stress).
- `resources.py` — linguistic constants, phoneme maps, and lexical overrides.
- `flask_instance.py` — Flask app (web form + API + health endpoints).
- `index.html` — local Flask template UI.
- `test_transcriber.py` — pytest-based transcription tests.
- `edge_cases.py` — hard/disputed words under manual review.
- `requirements.txt` — Python dependencies.
- `Procfile` — deployment start command (Render/Heroku-style platforms).

---

## Local setup

## 1) Install dependencies

```bash
py -3 -m pip install -r requirements.txt
```

## 2) Run tests

```bash
py -3 -m pytest -q
```

## 3) Run local web app

```bash
py -3 flask_instance.py
```

Open:

- `http://127.0.0.1:5000/`

Health check:

- `http://127.0.0.1:5000/health`

---

## API usage

### Endpoint

`POST /api/transcribe`

### Request body

```json
{ "word": "hola" }
```

### Response

```json
{ "transcription": "'o.la" }
```

### Example (PowerShell)

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:5000/api/transcribe" -ContentType "application/json" -Body '{"word":"hola"}'
```

---

## Deployment (Render)

This repo is deployment-ready for Render.

- Build command:

```bash
pip install -r requirements.txt
```

- Start command:

```bash
gunicorn flask_instance:app
```

Health endpoint for checks:

- `/health`

---

## Notes on transcription policy

- The system is rule-based (not ML-driven).
- Some areas (especially Nahuatl-origin `<x>` behavior) use explicit lexical/contextual handling.
- `edge_cases.py` is the place to keep difficult or disputed forms out of the core test set.

---

## Roadmap ideas

- Expand curated test corpus (toward 300+ words).
- Add stricter linguistic validation layers for syllabification.
- Optional future ML backoff model for unstable grapheme contexts (`x`-focused).

---

## License

This project is licensed under the **MIT License**. See [`LICENSE`](./LICENSE).
