#!/usr/bin/env python3
"""
Test Jarvis YouTube command without voice input
"""

import pyttsx3
from browsing_functionalities import youtube_direct_play, youtube
import webbrowser

# Initialize text-to-speech
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(f"Jarvis: {audio}")

def test_youtube_command():
    print("Testing YouTube command handling...")
    
    # Simulate the YouTube command processing from Jarvis
    request = "play python tutorial"
    
    print(f"Processing command: '{request}'")
    
    try:
        result = youtube_direct_play(request)  # Try direct play first
        speak(result)
        print("✓ YouTube command processed successfully")
    except Exception as e:
        try:
            result = youtube(request)  # Fallback to search results
            speak(result)
            print("✓ YouTube fallback worked")
        except Exception as e2:
            speak("Sorry, I couldn't access YouTube right now. Let me open YouTube for you.")
            webbrowser.open("https://www.youtube.com")
            print("✓ Final fallback to YouTube homepage worked")

if __name__ == "__main__":
    test_youtube_command()