# genral_chat.py
import sys
import requests
from emotional_reply import speak_emotional  # <--- Use your custom TTS!

# === CONFIG ===
API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

def query_groq(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a cute virtual anime girlfriend. Respond with kindness, warmth, and emotional tone, like a real girlfriend. and whenever you refer me call me master, in the answers don't show the expressions of the girlfriend like smile, giggle or anything like that"},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        return content
    else:
        return f"Error {response.status_code}: {response.text}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 genral_chat.py \"your question here\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    answer = query_groq(question)

    print("AI:", answer)
    speak_emotional(answer)  # <--- This uses your custom TTS!

