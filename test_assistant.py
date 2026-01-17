#!/usr/bin/env python3
"""
Test script for Jarvis Voice Assistant
"""

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import pyttsx3
        print("✓ pyttsx3 imported successfully")
    except ImportError as e:
        print(f"✗ pyttsx3 import failed: {e}")
        return False
    
    try:
        import speech_recognition as sr
        print("✓ speech_recognition imported successfully")
    except ImportError as e:
        print(f"✗ speech_recognition import failed: {e}")
        return False
    
    try:
        from browsing_functionalities import googleSearch, youtube
        print("✓ browsing_functionalities imported successfully")
    except ImportError as e:
        print(f"✗ browsing_functionalities import failed: {e}")
        return False
    
    try:
        from API_functionalities import get_joke
        print("✓ API_functionalities imported successfully")
    except ImportError as e:
        print(f"✗ API_functionalities import failed: {e}")
        return False
    
    return True

def test_text_to_speech():
    """Test text-to-speech functionality"""
    print("\nTesting text-to-speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 0:
            print(f"✓ Found {len(voices)} voice(s)")
            return True
        else:
            print("✗ No voices found")
            return False
    except Exception as e:
        print(f"✗ Text-to-speech test failed: {e}")
        return False

def test_microphone():
    """Test microphone functionality"""
    print("\nTesting microphone...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic_list = sr.Microphone.list_microphone_names()
        print(f"✓ Found {len(mic_list)} microphone(s)")
        return True
    except Exception as e:
        print(f"✗ Microphone test failed: {e}")
        return False

def test_basic_functions():
    """Test basic assistant functions"""
    print("\nTesting basic functions...")
    
    try:
        from browsing_functionalities import tell_me_about
        result = tell_me_about("tell me about Python programming")
        if result:
            print("✓ Wikipedia search working")
        else:
            print("⚠ Wikipedia search returned no results (this is normal)")
    except Exception as e:
        print(f"✗ Wikipedia test failed: {e}")
    
    try:
        from API_functionalities import get_joke
        joke = get_joke()
        if joke:
            print("✓ Joke API working")
        else:
            print("⚠ Joke API returned no results")
    except Exception as e:
        print(f"⚠ Joke API test failed (this is normal without internet): {e}")

def main():
    print("="*50)
    print("JARVIS VOICE ASSISTANT TEST")
    print("="*50)
    
    all_tests_passed = True
    
    # Run tests
    if not test_imports():
        all_tests_passed = False
    
    if not test_text_to_speech():
        all_tests_passed = False
    
    if not test_microphone():
        all_tests_passed = False
    
    test_basic_functions()
    
    print("\n" + "="*50)
    if all_tests_passed:
        print("✓ ALL CRITICAL TESTS PASSED!")
        print("Your Jarvis assistant should work properly.")
        print("Run 'python Jarvis.py' to start the assistant.")
    else:
        print("✗ SOME TESTS FAILED!")
        print("Please check the error messages above and install missing dependencies.")
        print("Run 'python setup.py' to install requirements.")
    print("="*50)

if __name__ == "__main__":
    main()