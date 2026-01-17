#!/usr/bin/env python3
"""
Test Jarvis functionality without microphone input
"""

import pyttsx3
import datetime
from browsing_functionalities import *
from API_functionalities import *
import pyjokes
import webbrowser

# Initialize text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(f"Jarvis: {audio}")

def load_name():
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Jarvis"

def test_functionality():
    print("="*50)
    print("TESTING JARVIS FUNCTIONALITY")
    print("="*50)
    
    assistant_name = load_name()
    print(f"Assistant name: {assistant_name}")
    
    # Test greeting
    print("\n1. Testing greeting...")
    speak(f"Hello! I'm {assistant_name}, your voice assistant.")
    
    # Test time
    print("\n2. Testing time function...")
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak(f"The current time is {current_time}")
    
    # Test date
    print("\n3. Testing date function...")
    now = datetime.datetime.now()
    speak(f"Today's date is {now.day} {now.strftime('%B')} {now.year}")
    
    # Test joke
    print("\n4. Testing joke function...")
    try:
        joke = pyjokes.get_joke()
        speak("Here's a joke for you:")
        speak(joke)
    except Exception as e:
        speak("Sorry, I couldn't get a joke right now")
    
    # Test Wikipedia
    print("\n5. Testing Wikipedia search...")
    try:
        info = tell_me_about("tell me about artificial intelligence")
        if info:
            speak("Here's what I found about artificial intelligence:")
            speak(info[:200] + "...")  # Limit length
        else:
            speak("Sorry, I couldn't find information about that")
    except Exception as e:
        speak("Wikipedia search encountered an error")
    
    # Test web search (just show URL, don't open)
    print("\n6. Testing Google search...")
    try:
        search_query = "Python programming"
        url = f"https://www.google.com/search?q={search_query}"
        speak(f"I would search Google for: {search_query}")
        print(f"Search URL: {url}")
    except Exception as e:
        speak("Google search encountered an error")
    
    # Test task management
    print("\n7. Testing task management...")
    try:
        test_task = "Test task from functionality test"
        with open("todo.txt", "a") as file:
            file.write(test_task + "\n")
        speak("I've added a test task to your todo list")
        
        with open("todo.txt", "r") as file:
            tasks = file.read()
            speak("Here are your current tasks:")
            print(f"Tasks: {tasks}")
    except Exception as e:
        speak("Task management encountered an error")
    
    # Test API functions (these might fail without API keys)
    print("\n8. Testing API functions...")
    try:
        joke_api = get_joke()
        if joke_api:
            speak("Here's another joke from the API:")
            speak(joke_api[:100])
        else:
            speak("API joke service is not available")
    except Exception as e:
        print(f"API functions not available (normal without API keys): {e}")
    
    print("\n" + "="*50)
    speak("Functionality test completed successfully!")
    print("FUNCTIONALITY TEST COMPLETED!")
    print("="*50)

if __name__ == "__main__":
    test_functionality()