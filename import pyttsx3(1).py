import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import smtplib
import pyautogui
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from translate import Translator
import pyjokes
import threading
import os

# Initialize the pyttsx3 engine for text-to-speech
engine = pyttsx3.init('sapi5')
translator = Translator(from_lang="English", to_lang="Hindi")

# Function to speak the given text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to take a screenshot
def take_screenshot():
    pic = pyautogui.screenshot()
    pic.save('screenshot.png')
    speak("Screenshot taken")

# Function to wish the user based on the time of day
def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 6:
        speak("Good night")
    elif 6 <= hour < 12:
        speak("Good morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am your assistant. How may I help you?")

# Function to listen to the user's command
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Say that again please...")
            return None

# Function to send an email
def send_email(to, content):
    try:
        EMAIL = os.getenv('EMAIL')
        PASSWORD = os.getenv('EMAIL_PASSWORD')
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to, content)
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I could not send the email.")

# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    print(joke)

# Main function to handle user commands
def assistant_main():
    wish_me()

    while True:
        query = take_command()
        if query is None:
            continue

        # Wikipedia search
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace('wikipedia', '')
            try:
                results = wikipedia.summary(query, sentences=2)
                speak('According to Wikipedia:')
                speak(results)
            except Exception as e:
                speak("Sorry, I couldn't fetch the Wikipedia results.")

        # Open websites
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://google.com")
        elif 'open github' in query:
            webbrowser.open("https://github.com")

        # Tell the time
        elif 'the time' in query:
            str_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {str_time}")

        # Send email
        elif 'email' in query:
            speak("What should I say?")
            content = take_command()
            speak("Who should I send it to?")
            to = input("Enter recipient email: ")  # Replace with a GUI input if needed
            send_email(to, content)

        # Translate text
        elif 'translate' in query:
            speak("What text should I translate?")
            text_to_translate = take_command()
            if text_to_translate:
                translation = translator.translate(text_to_translate)
                speak(translation)
                print(translation)

        # Take a screenshot
        elif 'screenshot' in query:
            take_screenshot()

        # Tell a joke
        elif 'joke' in query:
            tell_joke()

        # Exit command
        elif 'shutdown' in query or 'exit' in query:
            speak("Shutting down. Goodbye!")
            break

# GUI setup using tkinter
def setup_gui():
    root = tk.ThemedTk()
    root.set_theme('radiance')
    root.title("Voice Assistant")
    root.geometry("400x350")

    lbl = ttk.Label(root, text="Welcome to the Voice Assistant", wraplength=300, font=("Arial", 12))
    lbl.pack(pady=10)

    run_button = ttk.Button(root, text="Run Assistant", command=lambda: threading.Thread(target=assistant_main).start())
    run_button.pack(pady=10)

    exit_button = ttk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()