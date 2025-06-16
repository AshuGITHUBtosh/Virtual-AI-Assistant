import openai

# Point OpenAI client to LM Studio's local server
openai.api_base = "http://localhost:1234/v1"
openai.api_key = "lm-studio"  # dummy key, required but not checked

def chat_with_model():
    print("Welcome to your LM Studio assistant! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        try:
            response = openai.ChatCompletion.create(
                model="codellama-7b-instruct",  # Make sure this matches your LM Studio model name
                messages=[
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7
            )
            print("AI:", response['choices'][0]['message']['content'].strip())
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    chat_with_model()
