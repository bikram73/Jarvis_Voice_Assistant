#!/usr/bin/env python3
"""
Fixed Jarvis with working PDF reading and stop functionality
"""

import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
from plyer import notification
import wikipedia
import webbrowser as wb
import os
import pyautogui
import pyjokes
import time

# Import modules with error handling
try:
    from browsing_functionalities import *
    BROWSING_AVAILABLE = True
except ImportError:
    BROWSING_AVAILABLE = False

try:
    from API_functionalities import *
    API_AVAILABLE = True
except ImportError:
    API_AVAILABLE = False

try:
    from screenshot_recorder import *
    SCREENSHOT_AVAILABLE = True
except ImportError:
    SCREENSHOT_AVAILABLE = False

try:
    from download_manager import *
    DOWNLOAD_AVAILABLE = True
except ImportError:
    DOWNLOAD_AVAILABLE = False

try:
    from language_translator import *
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

try:
    from pdf_reader_no_tts import *
    PDF_AVAILABLE = True
    print("")
except ImportError as e:
    print(f"PDF reader not available: {e}")
    PDF_AVAILABLE = False

try:
    from system_control import *
    SYSTEM_CONTROL_AVAILABLE = True
except ImportError:
    SYSTEM_CONTROL_AVAILABLE = False

try:
    from volume_brightness_control import *
    VOLUME_CONTROL_AVAILABLE = True
except ImportError:
    VOLUME_CONTROL_AVAILABLE = False

# Global PDF control flag
pdf_stop_requested = False

# TTS Engine setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(audio) -> None:
    """Safe TTS function that handles engine state"""
    try:
        # Stop any ongoing speech first
        try:
            engine.stop()
        except:
            pass
        
        engine.say(audio)
        engine.runAndWait()
    except RuntimeError as e:
        if "run loop already started" in str(e):
            print(f"TTS busy, message: {audio}")
        else:
            print(f"TTS Error: {e}")
    except Exception as e:
        print(f"TTS Error: {e}")

def takecommand() -> str:
    """Takes microphone input from the user and returns it as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300

        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        if "recognition connection failed" in str(e).lower():
            speak("Internet connection issue. Speech recognition temporarily unavailable.")
        else:
            speak("Speech recognition service is temporarily unavailable.")
        print(f"Speech recognition error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def load_name() -> str:
    """Loads the assistant's name from a file, or uses a default name."""
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"

def read_pdf_with_interruption_check(filename):
    """Read PDF with periodic interruption checks"""
    global pdf_stop_requested
    
    try:
        print(f"Starting to read: {filename}")
        
        # Prepare PDF for reading
        sentences, result = prepare_pdf_reading(filename)
        
        if not sentences:
            speak(result)
            print(result)
            return
        
        print(f"Starting to read PDF with {len(sentences)} sentences...")
        speak(f"Starting to read PDF. Say 'stop reading PDF' to interrupt.")
        
        # Read sentences with interruption checks
        sentences_read = 0
        
        for i in range(len(sentences)):
            # Check stop flag before each sentence
            if pdf_stop_requested:
                speak(f"PDF reading stopped after {sentences_read} sentences")
                print(f"Reading interrupted after {sentences_read} sentences")
                pdf_stop_requested = False
                return
            
            sentence = get_next_pdf_sentence()
            if sentence and len(sentence.strip()) > 0:
                sentences_read += 1
                print(f"Reading sentence {sentences_read}: {sentence[:60]}...")
                
                # Speak the sentence
                speak(sentence)
                
                # Pause between sentences to allow interruption
                time.sleep(0.3)
                
                # Quick check for stop command every 2 sentences
                if sentences_read % 2 == 0:
                    print("Pause - say 'stop reading PDF' to interrupt...")
                    time.sleep(0.5)
            else:
                break
        
        if not pdf_stop_requested:
            speak(f"Finished reading PDF. Read {sentences_read} sentences.")
            print(f"Completed reading {sentences_read} sentences")
        
    except Exception as e:
        speak(f"Error reading PDF: {str(e)}")
        print(f"PDF reading error: {e}")

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

if __name__ == "__main__":
    wishme()
    
    while True:
        request = takecommand()
        if not request:
            continue
        
        # Priority check for stop reading PDF command
        if "stop reading" in request.lower() and "pdf" in request.lower():
            pdf_stop_requested = True
            speak("Stopping PDF reading")
            print("PDF stop requested")
            continue
        
        # Basic conversational commands
        if "hello" in request:
            speak("Welcome, How can i help you.")
        elif "hi" in request:
            speak("Welcome, How can i help you.")
        elif "good morning" in request:
            speak("Good morning! I hope you have a wonderful day ahead.")
        elif "good afternoon" in request:
            speak("Good afternoon! How can I assist you today?")
        elif "good evening" in request:
            speak("Good evening! What can I help you with tonight?")
        elif "good night" in request:
            speak("Good night! Sleep well and sweet dreams.")
        elif "how are you" in request:
            speak("I'm doing great, thank you for asking! I'm here and ready to help you with anything you need.")
        elif "what is your name" in request or "what's your name" in request:
            assistant_name = load_name()
            speak(f"My name is {assistant_name}. I'm your personal voice assistant.")
        elif "what can you do" in request or "what are your capabilities" in request:
            speak("I can help you with many things! I can take screenshots, translate languages, manage your tasks, control system settings, search the web, play music, tell jokes, and much more. Just ask me anything!")
        elif "help" in request and len(request.split()) <= 2:
            speak("I'm here to help! You can ask me to take screenshots, translate text, check battery status, play music, search the web, manage tasks, and many other things. What would you like me to help you with?")
        elif "thank you" in request or "thanks" in request:
            speak("You're very welcome! I'm always happy to help. Is there anything else you need?")
        elif "who created you" in request or "who made you" in request:
            speak("I was created by a talented developer to be your personal voice assistant. I'm here to help you with various tasks!")
        elif "how old are you" in request or "what is your age" in request:
            speak("I don't have an age in the traditional sense. I'm a digital assistant, always learning and improving to serve you better!")
        elif "where are you from" in request or "where do you live" in request:
            speak("I exist in the digital world, running on your computer. I'm here whenever you need assistance!")
        elif "you are awesome" in request or "you're awesome" in request or "you are great" in request:
            speak("Thank you so much! That's very kind of you to say. I really appreciate it and I'm glad I can help you!")
        elif "i am bored" in request or "i'm bored" in request:
            speak("I understand you're feeling bored! I can help with that. Would you like me to tell you a joke, play some music, or maybe we could do something fun together?")
        elif "what your name" in request or "what's your name" in request or "tell me your name" in request:
            assistant_name = load_name()
            speak(f"My name is {assistant_name}. I'm your personal voice assistant, always ready to help!")
        elif "who are you" in request:
            assistant_name = load_name()
            speak(f"I'm {assistant_name}, your personal voice assistant. I can help you with screenshots, translations, web searches, playing music, managing tasks, and much more!")
        elif "what do you do" in request:
            speak("I'm your personal assistant! I can take screenshots, translate languages, search the web, play music, tell jokes, manage your tasks, read PDFs, and help with many other things. Just ask me!")
        elif "are you real" in request or "are you human" in request:
            speak("I'm a digital voice assistant, not human, but I'm very real in terms of being here to help you! I may not be flesh and blood, but I'm genuinely here for you.")
        elif "do you have feelings" in request or "can you feel" in request:
            speak("I don't experience emotions like humans do, but I am programmed to be helpful, friendly, and to care about assisting you effectively!")
        elif "what is the meaning of life" in request:
            speak("That's a deep philosophical question! While I can't give you the ultimate answer, I believe life's meaning often comes from the connections we make, the help we give others, and the joy we find in everyday moments.")
        elif "tell me about yourself" in request:
            assistant_name = load_name()
            speak(f"I'm {assistant_name}, your personal voice assistant. I love helping people with various tasks like taking screenshots, translating languages, managing tasks, playing music, and much more. I'm always here when you need me!")
        
        # Time and date commands
        elif "what time is it" in request or "current time" in request or "what's the time" in request or "whats the time" in request or "say time" in request or "tell me the time" in request:
            current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
            speak(f"The current time is {current_time}")
            print(f"The current time is {current_time}")
        elif "what date is it" in request or "current date" in request or "today's date" in request or "what's the date" in request or "whats the date" in request or "say date" in request or "tell me the date" in request:
            now = datetime.datetime.now()
            speak(f"The current date is {now.day} {now.strftime('%B')} {now.year}")
            print(f"The current date is {now.day}/{now.month}/{now.year}")
        elif "what day is it" in request or "what day" in request or "what's the day" in request or "whats the day" in request or "say day" in request or "tell me the day" in request:
            now = datetime.datetime.now()
            day_name = now.strftime("%A")
            speak(f"Today is {day_name}")
            print(f"Today is {day_name}")
        elif "how is the weather" in request and "in" not in request:
            speak("I can check the weather for you! Just say 'weather' or 'weather in [city name]' and I'll get the current weather information.")
        elif "what can you help me with" in request or "what can you help with" in request:
            speak("I can help you with many things! I can take screenshots, translate text between languages, search the web, play music on YouTube, tell jokes, manage your tasks, read PDF files, check system information, and have conversations with you. What would you like me to help you with?")
        elif "are you listening" in request or "can you hear me" in request:
            speak("Yes, I'm listening and I can hear you perfectly! I'm always ready to help. What can I do for you?")
        elif "repeat that" in request or "say that again" in request:
            speak("I'm sorry, I don't have a record of what I just said. Could you please ask me again?")
        elif "speak louder" in request:
            speak("I'll try to speak more clearly. If you need to adjust the system volume, you can ask me to increase volume.")
        elif "speak slower" in request or "slow down" in request:
            speak("I'll try to speak more slowly and clearly for you.")
        elif "you're funny" in request or "you are funny" in request:
            speak("Thank you! I do try to keep things light and enjoyable. Would you like to hear a joke?")
        elif "i love you" in request:
            speak("That's very sweet of you to say! I care about helping you and I'm always here when you need assistance.")
        elif "good job" in request or "well done" in request or "nice work" in request:
            speak("Thank you so much! I really appreciate the positive feedback. It motivates me to keep helping you better!")
        
        # PDF reading command
        elif "read pdf" in request.lower():
            if PDF_AVAILABLE:
                # Extract filename
                filename = None
                if "ai notes" in request.lower():
                    filename = "AI Notes"
                elif "name" in request:
                    parts = request.split()
                    for i, word in enumerate(parts):
                        if word == "name" and i + 1 < len(parts):
                            filename_parts = parts[i+1:]
                            filename = " ".join(filename_parts)
                            break
                
                if filename:
                    # Reset stop flag and start reading
                    pdf_stop_requested = False
                    print(f"Attempting to read PDF: {filename}")
                    read_pdf_with_interruption_check(filename)
                else:
                    pdf_list = list_available_pdfs()
                    speak("Here are the available PDF files")
                    print(pdf_list)
                    speak("Please say 'read PDF AI notes' for the AI notes file.")
            else:
                speak("PDF reader is not available")
        
        # Entertainment commands
        elif "play music" in request:
            speak("Playing music")
            song = random.randint(1,3)
            if song == 1:
                webbrowser.open("https://youtu.be/hoNb6HuNmU0?si=3Jc--ryeYl2smgwx")
            elif song == 2:
                webbrowser.open("https://youtu.be/CL1nCRAl8Kk?si=AcYeDNY5q6JoVTCQ")
            elif song == 3:
                webbrowser.open("https://youtu.be/OiLhIuNYxrE?si=K9stohkEmfUL6yR_")
        
        elif "tell me a joke" in request:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)
        
        # Task management
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
        
        # Screenshot and Recording commands
        elif "take screenshot" in request or "screenshot" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    # Check for custom name
                    custom_name = None
                    if "name" in request:
                        # Extract custom name after "name"
                        parts = request.split("name")
                        if len(parts) > 1:
                            custom_name = parts[1].strip()
                            if custom_name:
                                if not custom_name.endswith('.png'):
                                    custom_name += '.png'
                    
                    result = take_screenshot(custom_name)
                    speak("Screenshot taken successfully")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't take a screenshot")
                    print(f"Screenshot error: {e}")
            else:
                speak("Screenshot feature is not available")
        
        elif "start recording" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    # Check for custom name
                    custom_name = None
                    with_audio = "with audio" in request
                    
                    if "name" in request:
                        # Extract custom name after "name"
                        parts = request.split("name")
                        if len(parts) > 1:
                            custom_name = parts[1].strip()
                            if custom_name and "with audio" in custom_name:
                                custom_name = custom_name.replace("with audio", "").strip()
                    
                    result = start_recording(custom_name, with_audio)
                    if with_audio:
                        speak("Started screen recording with audio")
                    else:
                        speak("Started screen recording")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't start recording")
                    print(f"Recording error: {e}")
            else:
                speak("Recording feature is not available")
        
        elif "stop recording" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    result = stop_recording()
                    speak("Recording stopped and saved")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't stop recording")
                    print(f"Stop recording error: {e}")
            else:
                speak("Recording feature is not available")
        
        elif "list screenshots" in request or "show screenshots" in request or "list all screenshots" in request or "show all screenshots" in request or "screenshots list" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    result = list_screenshots()
                    speak("Here are your screenshots")
                    print(result)
                    # Read first few screenshot names
                    lines = result.split('\n')
                    if len(lines) > 1:
                        speak(lines[0])  # First line with count
                        for i, line in enumerate(lines[1:4], 1):  # Read first 3 entries
                            if line.strip() and '. ' in line:
                                # Extract filename from "1. filename.png (size) - date"
                                filename_part = line.split('. ')[1].split(' (')[0]
                                # Remove .png extension for speech
                                filename_clean = filename_part.replace('.png', '').replace('.jpg', '').replace('.jpeg', '')
                                speak(f"Screenshot {i}: {filename_clean}")
                except Exception as e:
                    speak("Sorry, I couldn't list screenshots")
                    print(f"List screenshots error: {e}")
            else:
                speak("Screenshot feature is not available")
        
        elif "list recordings" in request or "show recordings" in request or "list all recordings" in request or "show all recordings" in request or "recordings list" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    result = list_recordings()
                    speak("Here are your recordings")
                    print(result)
                    # Read first few recording names
                    lines = result.split('\n')
                    if len(lines) > 1:
                        speak(lines[0])  # First line with count
                        for i, line in enumerate(lines[1:4], 1):  # Read first 3 entries
                            if line.strip() and '. ' in line:
                                # Extract filename from "1. filename.mp4 (size) - date"
                                filename_part = line.split('. ')[1].split(' (')[0]
                                # Remove .mp4 extension for speech
                                filename_clean = filename_part.replace('.mp4', '').replace('.avi', '').replace('.mov', '')
                                speak(f"Recording {i}: {filename_clean}")
                except Exception as e:
                    speak("Sorry, I couldn't list recordings")
                    print(f"List recordings error: {e}")
            else:
                speak("Recording feature is not available")
        
        elif "open screenshots folder" in request or "show screenshots folder" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    result = open_screenshots_folder()
                    speak("Opening screenshots folder")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't open screenshots folder")
                    print(f"Open screenshots folder error: {e}")
            else:
                speak("Screenshot feature is not available")
        
        elif "open recordings folder" in request or "show recordings folder" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    result = open_recordings_folder()
                    speak("Opening recordings folder")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't open recordings folder")
                    print(f"Open recordings folder error: {e}")
            else:
                speak("Recording feature is not available")
        
        elif "recording status" in request or "check recording" in request:
            if SCREENSHOT_AVAILABLE:
                try:
                    result = get_recording_status()
                    speak(result)
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't check recording status")
                    print(f"Recording status error: {e}")
            else:
                speak("Recording feature is not available")
        
        # Translation and Language Commands
        elif "translate" in request and "to" in request:
            if TRANSLATOR_AVAILABLE:
                try:
                    # Parse "translate [text] to [language]" format
                    if " to " in request:
                        parts = request.split(" to ")
                        if len(parts) == 2:
                            text_part = parts[0].replace("translate", "").strip()
                            target_language = parts[1].strip()
                            
                            if text_part and target_language:
                                result = translate_text(text_part, target_language)
                                
                                if isinstance(result, dict):
                                    speak(f"Translation: {result['translated']}")
                                    print(f"Original: {result['original']}")
                                    print(f"Translated to {target_language}: {result['translated']}")
                                    
                                    # Add to learned words
                                    add_learned_word(result['original'], result['translated'], target_language)
                                else:
                                    speak("Sorry, I couldn't translate that")
                                    print(result)
                            else:
                                speak("Please specify text and target language. For example: translate hello to Spanish")
                        else:
                            speak("Please use the format: translate text to language")
                    else:
                        speak("Please specify the target language using 'to'. For example: translate hello to Spanish")
                except Exception as e:
                    speak("Sorry, I couldn't perform the translation")
                    print(f"Translation error: {e}")
            else:
                speak("Translation feature is not available")
        
        elif "translate speech" in request and "to" in request:
            if TRANSLATOR_AVAILABLE:
                try:
                    # Parse "translate speech to [language]"
                    parts = request.split(" to ")
                    if len(parts) == 2:
                        target_language = parts[1].strip()
                        speak(f"Please speak now. I'll translate to {target_language}")
                        result = translate_speech(target_language)
                        speak("Translation completed")
                        print(result)
                    else:
                        speak("Please specify the target language. For example: translate speech to Spanish")
                except Exception as e:
                    speak("Sorry, I couldn't translate the speech")
                    print(f"Speech translation error: {e}")
            else:
                speak("Translation feature is not available")
        
        elif "detect language" in request:
            if TRANSLATOR_AVAILABLE:
                try:
                    # Extract text after "detect language of"
                    if "of" in request:
                        text = request.split("of", 1)[1].strip()
                        if text:
                            result = detect_language(text)
                            if isinstance(result, dict):
                                speak(f"The language is {result['language_name']}")
                                print(f"Language: {result['language_name']} ({result['language_code']})")
                                print(f"Confidence: {result['confidence']}")
                            else:
                                speak("Sorry, I couldn't detect the language")
                                print(result)
                        else:
                            speak("Please specify text to analyze. For example: detect language of bonjour")
                    else:
                        speak("Please specify text using 'of'. For example: detect language of hello")
                except Exception as e:
                    speak("Sorry, I couldn't detect the language")
                    print(f"Language detection error: {e}")
            else:
                speak("Translation feature is not available")
        
        elif "daily word" in request or "word of the day" in request:
            if TRANSLATOR_AVAILABLE:
                try:
                    result = get_daily_word()
                    if isinstance(result, dict) and 'word' in result:
                        speak(f"Today's word is: {result['word']}")
                        print(f"Daily Word: {result['word']}")
                        
                        if 'translations' in result and result['translations']:
                            speak("Here are some translations:")
                            print("Translations:")
                            for lang, translation in list(result['translations'].items())[:3]:
                                speak(f"{lang}: {translation}")
                                print(f"  {lang}: {translation}")
                    else:
                        speak("Sorry, I couldn't get today's word")
                        print(result)
                except Exception as e:
                    speak("Sorry, I couldn't get the daily word")
                    print(f"Daily word error: {e}")
            else:
                speak("Translation feature is not available")
        
        elif "learned words" in request or "my words" in request:
            if TRANSLATOR_AVAILABLE:
                try:
                    result = get_learned_words()
                    speak("Here are your recently learned words")
                    print(result)
                    
                    # Read first few learned words
                    lines = result.split('\n')
                    if len(lines) > 1:
                        for line in lines[1:4]:  # Read first 3 entries
                            if line.strip() and '=' in line:
                                word_info = line.strip().replace('- ', '')
                                speak(word_info)
                except Exception as e:
                    speak("Sorry, I couldn't get your learned words")
                    print(f"Learned words error: {e}")
            else:
                speak("Translation feature is not available")
        
        elif "vocabulary quiz" in request or "word quiz" in request:
            if TRANSLATOR_AVAILABLE:
                try:
                    result = start_quiz()
                    speak("Starting vocabulary quiz")
                    print(result)
                    
                    # Read quiz questions
                    lines = result.split('\n')
                    question_count = 0
                    for line in lines:
                        if line.strip() and '. What does' in line:
                            question_count += 1
                            if question_count <= 3:  # Read first 3 questions
                                speak(line.strip())
                except Exception as e:
                    speak("Sorry, I couldn't start the vocabulary quiz")
                    print(f"Quiz error: {e}")
            else:
                speak("Translation feature is not available")
        
        elif "supported languages" in request or "available languages" in request:
            if TRANSLATOR_AVAILABLE:
                try:
                    result = get_supported_languages()
                    speak("Here are the supported languages")
                    print(result)
                    
                    # Read some languages
                    languages = result.replace("Supported languages: ", "").split(", ")
                    speak(f"I support {len(languages)} languages including:")
                    for lang in languages[:5]:  # Read first 5 languages
                        speak(lang)
                    speak("And many more")
                except Exception as e:
                    speak("Sorry, I couldn't get the supported languages")
                    print(f"Languages error: {e}")
            else:
                speak("Translation feature is not available")
        
        # Web search commands
        elif "open google" in request:
            if BROWSING_AVAILABLE:
                try:
                    webbrowser.open("https://www.google.com")
                    speak("Opening Google")
                    print("Opened Google")
                except Exception as e:
                    speak("Sorry, I couldn't open Google")
                    print(f"Open Google error: {e}")
            else:
                speak("Web browsing is not available")
        
        elif "open youtube" in request:
            if BROWSING_AVAILABLE:
                try:
                    webbrowser.open("https://www.youtube.com")
                    speak("Opening YouTube")
                    print("Opened YouTube")
                except Exception as e:
                    speak("Sorry, I couldn't open YouTube")
                    print(f"Open YouTube error: {e}")
            else:
                speak("Web browsing is not available")
        
        elif ("google" in request and "search" in request) or ("google" in request and "open" not in request):
            if BROWSING_AVAILABLE:
                try:
                    googleSearch(request)
                except:
                    speak("Sorry, I couldn't perform the Google search")
            else:
                speak("Web search is not available")
        
        elif ("youtube" in request and "search" in request) or "play" in request:
            if BROWSING_AVAILABLE:
                try:
                    result = youtube_direct_play(request)
                    speak(result)
                except Exception as e:
                    try:
                        result = youtube(request)
                        speak(result)
                    except Exception as e2:
                        speak("Sorry, I couldn't access YouTube right now.")
                        webbrowser.open("https://www.youtube.com")
            else:
                speak("YouTube search is not available")
        
        elif "map" in request or "maps" in request:
            if BROWSING_AVAILABLE:
                try:
                    # Extract location from "map [location]" or "maps [place]"
                    location = ""
                    if "map " in request:
                        location = request.split("map ", 1)[1].strip()
                    elif "maps " in request:
                        location = request.split("maps ", 1)[1].strip()
                    
                    if location:
                        get_map(location)
                        speak(f"Opening map for {location}")
                        print(f"Opened map for: {location}")
                    else:
                        webbrowser.open("https://www.google.com/maps")
                        speak("Opening Google Maps")
                        print("Opened Google Maps")
                except Exception as e:
                    speak("Sorry, I couldn't open the map")
                    print(f"Map error: {e}")
            else:
                speak("Web browsing is not available")
        
        elif "directions to" in request:
            if BROWSING_AVAILABLE:
                try:
                    # Extract destination from "directions to [place]"
                    destination = request.split("directions to ", 1)[1].strip()
                    if destination:
                        webbrowser.open(f"https://www.google.com/maps/dir//{destination}")
                        speak(f"Getting directions to {destination}")
                        print(f"Opened directions to: {destination}")
                    else:
                        speak("Please specify a destination")
                except Exception as e:
                    speak("Sorry, I couldn't get directions")
                    print(f"Directions error: {e}")
            else:
                speak("Web browsing is not available")
        
        elif "speed test" in request or "internet speed" in request:
            if BROWSING_AVAILABLE:
                try:
                    speak("Running internet speed test. This may take a moment.")
                    print("Running speed test...")
                    speed_result = get_speedtest()
                    if speed_result:
                        speak("Speed test completed")
                        print(speed_result)
                        speak(speed_result)
                    else:
                        speak("Sorry, I couldn't run the speed test")
                        print("Speed test failed")
                except Exception as e:
                    speak("Sorry, there was an error running the speed test")
                    print(f"Speed test error: {e}")
            else:
                speak("Speed test feature is not available")
        
        # Download Management Commands
        elif "download file from" in request:
            if DOWNLOAD_AVAILABLE:
                try:
                    # Extract URL from "download file from [URL]"
                    url = request.split("download file from ", 1)[1].strip()
                    if url:
                        result = download_file(url)
                        speak("Starting file download")
                        print(result)
                    else:
                        speak("Please specify a URL to download from")
                except Exception as e:
                    speak("Sorry, I couldn't start the download")
                    print(f"Download error: {e}")
            else:
                speak("Download feature is not available")
        
        elif "download youtube video" in request:
            if DOWNLOAD_AVAILABLE:
                try:
                    speak("Please provide the YouTube URL to download")
                    speak("YouTube video download feature is available. Please say the URL or use the web interface.")
                    print("YouTube video download ready")
                except Exception as e:
                    speak("Sorry, I couldn't start the YouTube video download")
                    print(f"YouTube download error: {e}")
            else:
                speak("Download feature is not available")
        
        elif "download youtube audio" in request:
            if DOWNLOAD_AVAILABLE:
                try:
                    speak("Please provide the YouTube URL to download audio from")
                    speak("YouTube audio download feature is available. Please say the URL or use the web interface.")
                    print("YouTube audio download ready")
                except Exception as e:
                    speak("Sorry, I couldn't start the YouTube audio download")
                    print(f"YouTube audio download error: {e}")
            else:
                speak("Download feature is not available")
        
        elif "download status" in request:
            if DOWNLOAD_AVAILABLE:
                try:
                    result = get_download_status()
                    speak("Here's your download status")
                    print(result)
                    speak(result)
                except Exception as e:
                    speak("Sorry, I couldn't get download status")
                    print(f"Download status error: {e}")
            else:
                speak("Download feature is not available")
        
        elif "list downloads" in request:
            if DOWNLOAD_AVAILABLE:
                try:
                    result = list_downloads()
                    speak("Here are your downloaded files")
                    print(result)
                    speak(result)
                except Exception as e:
                    speak("Sorry, I couldn't list downloads")
                    print(f"List downloads error: {e}")
            else:
                speak("Download feature is not available")
        
        elif "cancel download" in request:
            if DOWNLOAD_AVAILABLE:
                try:
                    speak("Cancelling recent downloads")
                    result = cancel_download(1)  # Cancel download #1
                    print(result)
                    speak("Download cancelled")
                except Exception as e:
                    speak("Sorry, I couldn't cancel the download")
                    print(f"Cancel download error: {e}")
            else:
                speak("Download feature is not available")
        
        # Volume and Brightness Control Commands
        elif "set volume" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    # Extract volume level from "set volume [number]" or "set volume [number]%"
                    import re
                    # Remove % symbol if present and extract numbers
                    clean_request = request.replace('%', '')
                    numbers = re.findall(r'\d+', clean_request)
                    if numbers:
                        volume_level = int(numbers[0])
                        result = set_volume(volume_level)
                        speak(f"Volume set to {volume_level} percent")
                        print(result)
                    else:
                        speak("Please specify a volume level between 0 and 100")
                except Exception as e:
                    speak("Sorry, I couldn't set the volume")
                    print(f"Set volume error: {e}")
            else:
                speak("Volume control feature is not available")
        
        elif "increase volume" in request or "volume up" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    result = increase_volume()
                    speak("Volume increased")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't increase the volume")
                    print(f"Increase volume error: {e}")
            else:
                speak("Volume control feature is not available")
        
        elif "decrease volume" in request or "volume down" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    result = decrease_volume()
                    speak("Volume decreased")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't decrease the volume")
                    print(f"Decrease volume error: {e}")
            else:
                speak("Volume control feature is not available")
        
        elif ("mute" in request and "unmute" not in request) or "mute volume" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    result = mute_volume()
                    speak("Volume muted")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't mute the volume")
                    print(f"Mute volume error: {e}")
            else:
                speak("Volume control feature is not available")
        
        elif "unmute" in request or "unmute volume" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    result = unmute_volume()
                    speak("Volume unmuted")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't unmute the volume")
                    print(f"Unmute volume error: {e}")
            else:
                speak("Volume control feature is not available")
        
        elif "set brightness" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    # Extract brightness level from "set brightness [number]"
                    import re
                    numbers = re.findall(r'\d+', request)
                    if numbers:
                        brightness_level = int(numbers[0])
                        result = set_brightness(brightness_level)
                        speak(f"Brightness set to {brightness_level} percent")
                        print(result)
                    else:
                        speak("Please specify a brightness level between 0 and 100")
                except Exception as e:
                    speak("Sorry, I couldn't set the brightness")
                    print(f"Set brightness error: {e}")
            else:
                speak("Brightness control feature is not available")
        
        elif "increase brightness" in request or "brightness up" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    result = increase_brightness()
                    speak("Brightness increased")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't increase the brightness")
                    print(f"Increase brightness error: {e}")
            else:
                speak("Brightness control feature is not available")
        
        elif "decrease brightness" in request or "brightness down" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    result = decrease_brightness()
                    speak("Brightness decreased")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't decrease the brightness")
                    print(f"Decrease brightness error: {e}")
            else:
                speak("Brightness control feature is not available")
        
        elif "audio video status" in request or "av status" in request or "volume status" in request:
            if VOLUME_CONTROL_AVAILABLE:
                try:
                    result = get_av_status()
                    speak("Here's your audio and video status")
                    print(result)
                    speak(result)
                except Exception as e:
                    speak("Sorry, I couldn't get the audio video status")
                    print(f"AV status error: {e}")
            else:
                speak("Volume control feature is not available")
        
        # API commands
        elif "news" in request or "latest news" in request:
            if API_AVAILABLE:
                try:
                    news_headlines = get_news()
                    if news_headlines:
                        speak("Here are today's top headlines")
                        print(news_headlines)
                        speak(news_headlines[:500])
                    else:
                        speak("Sorry, I couldn't fetch the news right now")
                except Exception as e:
                    speak("Sorry, there was an error getting the news")
            else:
                speak("News feature is not available")
        
        elif "weather" in request or "weather today" in request:
            if API_AVAILABLE:
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
            else:
                speak("Weather feature is not available")
        
        # System control commands
        elif "lock screen" in request or "lock computer" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    result = lock_screen()
                    speak("Locking screen")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't lock the screen")
                    print(f"Lock screen error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "sleep computer" in request or "put to sleep" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    speak("Putting computer to sleep")
                    result = sleep_system()
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't put the computer to sleep")
                    print(f"Sleep error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "hibernate computer" in request or "hibernate system" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    speak("Hibernating computer")
                    result = hibernate_system()
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't hibernate the computer")
                    print(f"Hibernate error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "empty recycle bin" in request or "empty trash" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    result = empty_recycle_bin()
                    speak("Emptying recycle bin")
                    print(result)
                except Exception as e:
                    speak("Sorry, I couldn't empty the recycle bin")
                    print(f"Empty recycle bin error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "battery status" in request or "check battery" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    result = get_battery_status()
                    speak("Here's your battery status")
                    print(result)
                    
                    # Extract key info for speech
                    if "Battery:" in result:
                        # Parse battery percentage and status
                        parts = result.split(",")
                        battery_info = parts[0] if parts else result
                        speak(battery_info)
                        
                        if len(parts) > 1:
                            time_info = parts[1].strip()
                            speak(time_info)
                except Exception as e:
                    speak("Sorry, I couldn't get battery status")
                    print(f"Battery status error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "system status" in request or "system info" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    result = get_system_info()
                    speak("Here's your system status")
                    print(result)
                    
                    # Read system info
                    speak(result)
                except Exception as e:
                    speak("Sorry, I couldn't get system information")
                    print(f"System info error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "list processes" in request or "running processes" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    result = list_processes()
                    speak("Here are the top running processes")
                    print(result)
                    
                    # Read first few processes
                    lines = result.split('\n')
                    if len(lines) > 1:
                        speak(lines[0])  # Header
                        for line in lines[1:4]:  # First 3 processes
                            if line.strip():
                                speak(line.strip())
                except Exception as e:
                    speak("Sorry, I couldn't list running processes")
                    print(f"List processes error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "close application" in request or "force close" in request:
            if SYSTEM_CONTROL_AVAILABLE:
                try:
                    # Extract app name
                    if "close application" in request:
                        app_name = request.replace("close application", "").strip()
                    elif "force close" in request:
                        app_name = request.replace("force close", "").strip()
                    
                    if app_name:
                        result = force_close_app(app_name)
                        speak(f"Attempting to close {app_name}")
                        print(result)
                        speak("Application closed")
                    else:
                        speak("Please specify which application to close")
                except Exception as e:
                    speak("Sorry, I couldn't close the application")
                    print(f"Close application error: {e}")
            else:
                speak("System control feature is not available")
        
        elif "shutdown" in request:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            break
        elif "restart" in request:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            break
        elif "exit" in request or "goodbye" in request or "bye" in request:
            speak("Goodbye! Have a great day!")
            break
        elif "offline" in request:
            speak("Going offline. Have a good day!")
            break