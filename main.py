import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification

engine = pyttsx3.init()
voices =  engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def command():
    content = " "
    while content == " ":
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language='en-in')
            print("Yor Said.............." + content)
        except Exception as e:
            print("Please try again...")
    return content

def main_process():
    while True:
        request = command().lower()
        if "hello" in request:
            speak("Welcome, How can i help you.")
        elif "play music" in request:
            speak("Playing music")
            song = random.randint(1,3)
            if song == 1:
                webbrowser.open("https://youtu.be/hoNb6HuNmU0?si=3Jc--ryeYl2smgwx")
            elif song == 2:
                webbrowser.open("https://youtu.be/CL1nCRAl8Kk?si=AcYeDNY5q6JoVTCQ")
            elif song == 3:
                webbrowser.open("https://youtu.be/OiLhIuNYxrE?si=K9stohkEmfUL6yR_")
        elif "say time" in request:
            now_time = datetime.datetime.now().strftime("%H : %M")
            speak("Current time is "+ str(now_time))
        elif "say date" in request:
            now_time = datetime.datetime.now().strftime("%d : %m")
            speak("Current date is "+ str(now_time))
        elif "new task" in request:
            task = request.replace("new task", "")
            task = task.strip()
            if task != "":
                speak("Adding task : "+ task)
                with open ("todo.txt", "a") as file:
                    file.write(task + "\n")
        elif "my task" in request:
            with open ("todo.txt", "r") as file:
                speak("Work we have to do today is :" + file.read())
        elif "show work" in request:
            with open ("todo.txt", "r") as file:
                tasks = file.read()
                notification.notify(
                    title = "Today's work",
                    message = tasks
                )

main_process()