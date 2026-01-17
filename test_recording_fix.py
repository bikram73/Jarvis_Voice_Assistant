#!/usr/bin/env python3
"""
Test screen recording functionality
"""

import pyttsx3
from screenshot_recorder import start_recording, stop_recording

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

def test_recording_commands():
    """Test screen recording commands"""
    
    print("="*60)
    print("TESTING SCREEN RECORDING COMMANDS")
    print("="*60)
    
    # Test 1: Start recording command
    print("\n1. Testing 'start recording' command...")
    request = "start recording"
    
    if "start recording" in request or "record screen" in request or "screen record" in request:
        try:
            with_audio = "with audio" in request or "audio" in request
            print(f"Audio recording: {with_audio}")
            
            result = start_recording(with_audio=with_audio)
            speak(result)
            print(f"✅ Recording started: {result}")
            
            # Wait a moment then stop
            import time
            print("Recording for 3 seconds...")
            time.sleep(3)
            
            # Stop recording
            result = stop_recording()
            speak(result)
            print(f"✅ Recording stopped: {result}")
            
        except Exception as e:
            speak("Sorry, I couldn't start recording")
            print(f"❌ Recording error: {e}")
    
    # Test 2: Start recording with audio
    print("\n2. Testing 'start recording with audio' command...")
    request = "start recording with audio"
    
    if "start recording" in request or "record screen" in request or "screen record" in request:
        try:
            with_audio = "with audio" in request or "audio" in request
            print(f"Audio recording: {with_audio}")
            
            result = start_recording(with_audio=with_audio)
            speak("Started recording with audio for test")
            print(f"✅ Recording with audio started: {result}")
            
            # Stop immediately for test
            import time
            time.sleep(1)
            result = stop_recording()
            speak("Test recording stopped")
            print(f"✅ Recording stopped: {result}")
            
        except Exception as e:
            speak("Sorry, I couldn't start recording with audio")
            print(f"❌ Recording with audio error: {e}")

if __name__ == "__main__":
    test_recording_commands()