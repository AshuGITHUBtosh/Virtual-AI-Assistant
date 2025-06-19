import requests
import subprocess
import speech_recognition as sr  # 👈 Added for voice input

# === CONFIG ===
API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information...
->  Respond with 'general_emotional ( query )' if a query can be answered by a llm model (conversational ai chatbot) and it looks like the user is sad...
->  Respond with 'general_blush ( query )' if a query can be answered by a llm model (conversational ai chatbot) and the query looks like if the query is flirty or the user is praising you
-> Respond with 'realtime ( query )' if it requires up-to-date info...
-> Respond with 'open (application name)' if it is asking to open an app...
-> Respond with 'close (application name)' if it is asking to close one...
-> Respond with 'play (song name)' for playing songs...
-> Respond with 'generate image (prompt)' if it is asking to generate an image...
-> Respond with 'reminder (datetime + message)' to set a reminder...
-> Respond with 'system (task)' for volume, mute, etc...
-> Respond with 'content (topic)' if the query wants content generation like code or emails...
-> Respond with 'google search (topic)' or 'youtube search (topic)'...
-> Respond with 'exit' if the query is a goodbye...
-> If undecidable or unrelated, respond with 'general (query)'.
"""

def classify_query(query):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
        "temperature": 0.3
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        decision = result["choices"][0]["message"]["content"].strip()
        return decision
    else:
        return f"Error {response.status_code}: {response.text}"

def handle_decision(decision):
    if decision.startswith("general ("):
        query = decision[len("general ("):-1]
        subprocess.run(["python", "genral_chat.py", query])


    elif decision.startswith("general_emotional ("):
        query = decision[len("general ("):-1]
        subprocess.run(["python", "genral_emotional.py", query])


    elif decision.startswith("general_blush ("):
        query = decision[len("general ("):-1]
        subprocess.run(["python", "genral_blush.py", query])

    elif decision.startswith("content ("):
        query = decision[len("content ("):-1]
        subprocess.run(["python", "coding_chat.py", query])


    elif decision.startswith("open ("):
        query = decision[len("open ("):-1]
        subprocess.run(["python", "system.py", query])

    elif decision.startswith("youtube play ("):
        query = decision[len("open ("):-1]
        subprocess.run(["python", "system.py", query])

    elif decision.startswith("youtube search ("):
        query = decision[len("open ("):-1]
        subprocess.run(["python", "system.py", query])

    elif decision.startswith("exit"):
        print("Exiting. Goodbye!")
        exit(0)

    else:
        print("Decision:", decision)

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak your query:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"❌ Could not request results; {e}")
        return ""

if __name__ == "__main__":
    print("=== Decision Maker (Groq LLaMA-3) ===")
    print("Speak your query (say 'exit' to quit):\n")

    while True:
        try:
            user_query = get_voice_input().strip()
            if not user_query:
                continue

            if user_query.lower() in ("exit", "quit"):
                print("Exiting. Goodbye!")
                break

            decision = classify_query(user_query)
            handle_decision(decision)

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
