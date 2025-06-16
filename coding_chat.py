import sys
import requests

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
            {
                "role": "system",
                "content": (
                    "You are an expert programming assistant. Only answer programming-related questions. "
                    "Return clean, syntactically correct, and efficient code. Do not explain anything unless asked. "
                    "Do not include greetings or say things like 'Sure' or 'Here's your code'. Just output the code."
                )
            },
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.3
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
        print("Usage: python coding_chat.py \"your coding question here\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    answer = query_groq(question)
    print("AI:", answer)
