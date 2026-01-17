#!/usr/bin/env python3
"""
Test the specific translation command that was failing
"""

import pyttsx3
from language_translator import translate_text

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

def test_translation_command():
    """Test the exact translation command that was failing"""
    
    print("="*60)
    print("TESTING TRANSLATION COMMAND FIX")
    print("="*60)
    
    # Simulate the exact command: "translate my name is Vikram to Hindi"
    request = "translate my name is vikram to hindi"
    
    print(f"User said: '{request}'")
    print("Processing translation command...")
    
    # This is the new logic from Jarvis.py
    if "translate" in request:
        try:
            if "to" in request:
                # Parse the translation request
                parts = request.split("to")
                if len(parts) >= 2:
                    text_part = parts[0].replace("translate", "").strip()
                    target_lang = parts[1].strip()
                    
                    print(f"Text to translate: '{text_part}'")
                    print(f"Target language: '{target_lang}'")
                    
                    if text_part:
                        # Translate the extracted text
                        result = translate_text(text_part, target_lang)
                        if isinstance(result, dict):
                            response = f"Translation: {result['original']} means {result['translated']} in {target_lang}"
                            speak(response)
                            print(f"✅ SUCCESS: {response}")
                        else:
                            speak(str(result))
                            print(f"Translation result: {result}")
                    else:
                        speak(f"Please provide text to translate to {target_lang}")
                else:
                    speak("Please specify the target language. For example: translate hello to spanish")
            else:
                speak("Please specify the target language. For example: translate hello to spanish")
        except Exception as e:
            speak("Sorry, I couldn't perform the translation")
            print(f"❌ Translation error: {e}")

if __name__ == "__main__":
    test_translation_command()