import sys
import subprocess
import webbrowser
import os

def open_app(app_name):
    try:
        subprocess.Popen(app_name.lower())  # simplistic approach
    except Exception as e:
        print("Error opening app:", e)

def close_app(app_name):
    try:
        os.system(f"pkill {app_name.lower()}")  # for Linux
    except Exception as e:
        print("Error closing app:", e)

def control_system(task):
    if task == "volume up":
        os.system("amixer -D pulse sset Master 10%+")
    elif task == "volume down":
        os.system("amixer -D pulse sset Master 10%-")
    elif task == "mute":
        os.system("amixer -D pulse sset Master mute")
    elif task == "unmute":
        os.system("amixer -D pulse sset Master unmute")
    else:
        print("Unknown system task")

def search_google(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def search_youtube(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def handle_command(command):
    if command.startswith("open "):
        app = command[5:]
        open_app(app)
    elif command.startswith("close "):
        app = command[6:]
        close_app(app)
    elif command.startswith("system "):
        task = command[7:]
        control_system(task)
    elif command.startswith("google search "):
        search_google(command[14:])
    elif command.startswith("youtube search "):
        search_youtube(command[15:])
    else:
        print("Unknown command")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 automation.py \"command here\"")
        sys.exit(1)

    cmd = " ".join(sys.argv[1:])
    handle_command(cmd)
