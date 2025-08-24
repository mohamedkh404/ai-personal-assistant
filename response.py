import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import openai
import webbrowser
import datetime
import os

# ====== إعداد الصوت ======
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ====== إعداد OpenAI ======
openai.api_key = "PUT_YOUR_API_KEY_HERE"

def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {e}"

# ====== أوامر النظام البسيطة ======
def execute_command(command):
    command = command.lower()
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Current time is {now}")
    elif "open chrome" in command:
        speak("Opening Google Chrome")
        os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")
    else:
        # أي سؤال عام يرسل للـ OpenAI
        answer = ask_openai(command)
        speak(answer)
        chat_log.insert(tk.END, "Assistant: " + answer + "\n\n")

# ====== التعرف على الصوت ======
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        chat_log.insert(tk.END, "Listening...\n")
        chat_log.update()
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            chat_log.insert(tk.END, "You: " + command + "\n")
            execute_command(command)
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Could not request results; check your network.")

# ====== واجهة المستخدم ======
root = tk.Tk()
root.title("AI Personal Assistant")
root.geometry("500x500")

chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

btn_listen = tk.Button(root, text="🎤 Speak", command=listen)
btn_listen.pack(pady=5)

root.mainloop()