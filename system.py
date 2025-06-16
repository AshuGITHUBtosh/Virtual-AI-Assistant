import os
import webbrowser
import urllib.parse
import sys

def open_app(command: str):
    command = command.lower().strip()

    # === YouTube Specific Logic ===
    if "play" in command and "youtube" in command:
        query = command.split("play")[1].split("on youtube")[0].strip()
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        print(f"🎬 Playing '{query}' on YouTube...")
        webbrowser.open(url)

    elif "search" in command and "youtube" in command:
        query = command.split("search")[1].split("on youtube")[0].strip()
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        print(f"🔍 Searching '{query}' on YouTube...")
        webbrowser.open(url)

    elif "youtube" in command:
        webbrowser.open("https://www.youtube.com")

    # === Google Search ===
    elif "search" in command and "google" in command:
        query = command.split("search")[1].split("on google")[0].strip()
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        print(f"🔍 Searching '{query}' on Google...")
        webbrowser.open(url)

    elif "google" in command:
        webbrowser.open("https://www.google.com")

    # === Gmail ===
    elif "gmail" in command:
        webbrowser.open("https://mail.google.com")

    # === System Apps ===
    elif "notepad" in command:
        os.system("start notepad")
    elif "calculator" in command:
        os.system("start calc")
    elif "cmd" in command or "command prompt" in command:
        os.system("start cmd")
    elif "paint" in command:
        os.system("start mspaint")

    # === Other Installed Apps ===
    elif "chrome" in command:
        os.system("start chrome")
    elif "vscode" in command or "code" in command:
        os.system("start code")
    elif "spotify" in command:
        os.system("start spotify")

    else:
        print(f"❌ Could not understand command: {command}")

# ✅ Main execution from command-line argument
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗ Usage: python system.py <command>")
        sys.exit(1)

    # Join all command-line arguments into a single string
    command = " ".join(sys.argv[1:])
    open_app(command)
