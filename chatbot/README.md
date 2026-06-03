# Simple Gemini-style Chatbot

This is a tiny Python chatbot that calls a Gemini/Generative Language API-style endpoint.

Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and set your `API_KEY` (and optionally `MODEL` or `ENDPOINT`).

3. Run the chatbot:

```bash
python chatbot.py
```

Or send a one-shot prompt:

```bash
python chatbot.py "Hello, who are you?"
```

Notes

- The script constructs a default endpoint for Google Generative Language APIs:
  `https://generativelanguage.googleapis.com/v1beta2/models/{MODEL}:generate`.
- If your provider requires an API key query parameter rather than bearer tokens, set `API_KEY` and the script will attach it as `?key=` if no bearer token is present.
- Adjust `TEMPERATURE` and `MAX_OUTPUT_TOKENS` in your `.env` as needed.
