import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL", "gemini-1.5-flash")  # Default to a valid Gemini model
ENDPOINT = os.getenv("ENDPOINT")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
MAX_OUTPUT_TOKENS = int(os.getenv("MAX_OUTPUT_TOKENS", "512"))

# 1. Corrected to modern Gemini endpoint and method
if not ENDPOINT:
    ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

# 2. Clean headers (No Bearer token for AI Studio keys!)
HEADERS = {"Content-Type": "application/json"}

def generate(prompt_text):
    # 3. Corrected Gemini payload structure
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }],
        "generationConfig": {
            "temperature": TEMPERATURE,
            "maxOutputTokens": MAX_OUTPUT_TOKENS
        }
    }

    # 4. Correctly pass the API key as a query parameter
    params = {}
    if API_KEY:
        params["key"] = API_KEY

    try:
        resp = requests.post(ENDPOINT, headers=HEADERS, params=params, json=payload, timeout=30)
    except Exception as e:
        return f"Request error: {e}"

    if resp.status_code != 200:
        body = resp.text or ""
        snippet = body.strip().replace('\n', ' ')[:200]
        return f"API error {resp.status_code}: {snippet}"

    try:
        data = resp.json()
    except Exception:
        return resp.text

    # 5. Corrected parser for Gemini's JSON response structure
    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        # Fallback if structure varies or blocked by safety filters
        try:
            text = json.dumps(data, ensure_ascii=False)
        except Exception:
            text = str(data)

    return text

def repl():
    print("Simple Gemini chatbot. Type 'quit' or 'exit' to stop.")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue
        if user.lower() in ("quit", "exit"):
            break
        reply = generate(user)
        print("Bot:", reply)

def one_shot(args):
    prompt = " ".join(args)
    print(generate(prompt))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        one_shot(sys.argv[1:])
    else:
        repl()