import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
from browsing_functionalities import *
from API_functionalities import *
from screenshot_recorder import *
from download_manager import *
from language_translator import *
import wikipedia
import webbrowser as wb
import os
import pyautogui
import pyjokes

engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  
else:
    engine.setProperty('voice', voices[0].id)  # Fallback to first voice
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()

def time() -> None:
    """Tells the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(current_time)
    print("The current time is", current_time)


def date() -> None:
    """Tells the current date."""
    now = datetime.datetime.now()
    speak("The current date is")
    speak(f"{now.day} {now.strftime('%B')} {now.year}")
    print(f"The current date is {now.day}/{now.month}/{now.year}")

def wishme() -> None:
    """Greets the user based on the time of day."""
    speak("Welcome back, sir!")
    print("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
        print("Good evening!")
    else:
        speak("Good night, see you tomorrow.")

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    print(f"{assistant_name} at your service. Please tell me how may I assist you.")

def takecommand() -> str:
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1

        try:
            audio = r.listen(source, timeout=5)  # Listen with a timeout
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
        return None
    except Exception as e:
        speak(f"An error occurred: {e}")
        print(f"Error: {e}")
        return None

def load_name() -> str:
    """Loads the assistant's name from a file, or uses a default name."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"  # Default name


if __name__ == "__main__":
    wishme()
    while True:
        request = takecommand()
        if not request:
            continue
        if "hello" in request:
            speak("Welcome, How can i help you.")
        elif "hi" in request:
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
            time()
        elif "say date" in request:
            date()
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
        elif "tell me a joke" in request:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        elif "news" in request:
            try:
                news_headlines = get_news()
                if news_headlines:
                    speak("Here are today's top headlines")
                    print(news_headlines)
                    speak(news_headlines[:500])  # Limit to avoid too long speech
                else:
                    speak("Sorry, I couldn't fetch the news right now")
            except Exception as e:
                speak("Sorry, there was an error getting the news")

        elif "weather" in request:
            try:
                if "in" in request:
                    city = request.split("in")[-1].strip()
                    weather_info = get_weather(city)
                else:
                    weather_info = get_weather()
                
                if weather_info:
                    speak("Here's the weather information")
                    speak(weather_info)
                    print(weather_info)
                else:
                    speak("Sorry, I couldn't get the weather information")
            except Exception as e:
                speak("Sorry, there was an error getting the weather")

        elif "tell me about" in request:
            try:
                info = tell_me_about(request)
                if info:
                    speak(info)
                    print(info)
                else:
                    speak("Sorry, I couldn't find information about that topic")
            except Exception as e:
                speak("Sorry, there was an error getting that information")

        elif "open" in request:
            try:
                result = open_specified_website(request)
                if result:
                    speak("Opening the website")
                else:
                    speak("Sorry, I don't know that website")
            except Exception as e:
                speak("Sorry, there was an error opening the website")

        elif "speed test" in request:
            try:
                speak("Running speed test, please wait...")
                speed_info = get_speedtest()
                if speed_info:
                    speak(speed_info)
                    print(speed_info)
                else:
                    speak("Sorry, couldn't run the speed test")
            except Exception as e:
                speak("Sorry, there was an error running the speed test")

        elif "shutdown" in request:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break
            
        elif "restart" in request:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break
            
        elif "offline" in request or "exit" in request:
            speak("Going offline. Have a good day!")
            break

        elif ("google" in request and "search" in request) or ("google" in request and "how to" in request) or "google" in request:
            googleSearch(request)
        elif ("youtube" in request and "search" in request) or "play" in request or ("how to" in request and "youtube" in request):
            try:
                result = youtube_direct_play(request)  # Try direct play first
                speak(result)
            except Exception as e:
                try:
                    result = youtube(request)  # Fallback to search results
                    speak(result)
                except Exception as e2:
                    speak("Sorry, I couldn't access YouTube right now. Let me open YouTube for you.")
                    webbrowser.open("https://www.youtube.com")

        elif "distance" in request or "map" in request:
            get_map(request)

        # Screenshot and Recording Commands
        elif "take screenshot" in request or "screenshot" in request:
            try:
                if "name" in request:
                    # Extract custom name from request
                    name_part = request.split("name")[-1].strip()
                    if name_part:
                        filename = f"{name_part.replace(' ', '_')}.png"
                        result = take_screenshot(filename)
                    else:
                        result = take_screenshot()
                else:
                    result = take_screenshot()
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't take a screenshot")

        elif "start recording" in request or "record screen" in request or "screen record" in request:
            try:
                with_audio = "with audio" in request or "audio" in request
                if "name" in request:
                    name_part = request.split("name")[-1].strip()
                    if name_part:
                        filename = f"{name_part.replace(' ', '_')}.mp4"
                        result = start_recording(filename, with_audio)
                    else:
                        result = start_recording(with_audio=with_audio)
                else:
                    result = start_recording(with_audio=with_audio)
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't start recording")
                print(f"Recording error: {e}")

        elif "stop recording" in request:
            try:
                result = stop_recording()
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't stop recording")

        elif "list screenshots" in request:
            try:
                result = list_screenshots()
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't list screenshots")

        elif "list recordings" in request:
            try:
                result = list_recordings()
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't list recordings")

        # Download Manager Commands
        elif "download file" in request:
            try:
                # Extract URL from request (basic implementation)
                speak("Please provide the URL to download")
                # In a real implementation, you'd get the URL from speech
                speak("Download feature ready. Use: download file from [URL]")
            except Exception as e:
                speak("Sorry, I couldn't start the download")

        elif "download youtube video" in request or "download video" in request:
            try:
                speak("Please provide the YouTube URL to download")
                # In a real implementation, you'd extract URL from speech
                speak("YouTube video download feature ready")
            except Exception as e:
                speak("Sorry, I couldn't download the video")

        elif "download youtube audio" in request or "download audio" in request:
            try:
                speak("Please provide the YouTube URL to download audio")
                speak("YouTube audio download feature ready")
            except Exception as e:
                speak("Sorry, I couldn't download the audio")

        elif "download status" in request:
            try:
                result = get_download_status()
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't get download status")

        elif "list downloads" in request:
            try:
                result = list_downloads()
                speak(result)
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't list downloads")

        # Language Translation Commands
        elif "translate" in request:
            try:
                if "to" in request:
                    # Parse the translation request
                    parts = request.split("to")
                    if len(parts) >= 2:
                        text_part = parts[0].replace("translate", "").strip()
                        target_lang = parts[1].strip()
                        
                        if text_part:
                            # Translate the extracted text
                            result = translate_text(text_part, target_lang)
                            if isinstance(result, dict):
                                response = f"Translation: {result['original']} means {result['translated']} in {target_lang}"
                                speak(response)
                                print(response)
                            else:
                                speak(str(result))
                        else:
                            speak(f"Please provide text to translate to {target_lang}")
                    else:
                        speak("Please specify the target language. For example: translate hello to spanish")
                else:
                    speak("Please specify the target language. For example: translate hello to spanish")
            except Exception as e:
                speak("Sorry, I couldn't perform the translation")
                print(f"Translation error: {e}")

        elif "detect language" in request:
            try:
                speak("Please provide text to detect language")
                speak("Language detection feature ready")
            except Exception as e:
                speak("Sorry, I couldn't detect the language")

        elif "daily word" in request or "word of the day" in request:
            try:
                word_data = get_daily_word()
                if isinstance(word_data, dict) and 'word' in word_data:
                    speak(f"Today's word is: {word_data['word']}")
                    if 'translations' in word_data:
                        for lang, translation in list(word_data['translations'].items())[:3]:
                            speak(f"In {lang}: {translation}")
                else:
                    speak("Sorry, I couldn't get today's word")
            except Exception as e:
                speak("Sorry, I couldn't get the daily word")

        elif "learned words" in request or "my words" in request:
            try:
                result = get_learned_words()
                speak("Here are your recently learned words")
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't get your learned words")

        elif "vocabulary quiz" in request or "word quiz" in request:
            try:
                result = start_quiz()
                speak("Starting vocabulary quiz")
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't start the quiz")

        elif "supported languages" in request:
            try:
                result = get_supported_languages()
                speak("Here are the supported languages")
                print(result)
            except Exception as e:
                speak("Sorry, I couldn't get supported languages")


