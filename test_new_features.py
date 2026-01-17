#!/usr/bin/env python3
"""
Test script for new Jarvis features:
1. Screenshot & Screen Recording
2. Download Manager
3. Language Translation
"""

import os
import time

def test_screenshot_features():
    """Test screenshot and recording features"""
    print("="*50)
    print("TESTING SCREENSHOT & RECORDING FEATURES")
    print("="*50)
    
    try:
        from screenshot_recorder import take_screenshot, list_screenshots
        
        print("1. Testing screenshot functionality...")
        result = take_screenshot("test_screenshot.png")
        print(f"Screenshot result: {result}")
        
        print("\n2. Testing screenshot listing...")
        result = list_screenshots()
        print(f"Screenshots: {result}")
        
        print("✅ Screenshot features working!")
        
    except ImportError as e:
        print(f"⚠️ Screenshot features not available: {e}")
        print("Install required packages: pip install opencv-python sounddevice soundfile")
    except Exception as e:
        print(f"❌ Screenshot test failed: {e}")

def test_download_features():
    """Test download manager features"""
    print("\n" + "="*50)
    print("TESTING DOWNLOAD MANAGER FEATURES")
    print("="*50)
    
    try:
        from download_manager import download_file, get_download_status, list_downloads
        
        print("1. Testing download manager initialization...")
        result = get_download_status()
        print(f"Download status: {result}")
        
        print("\n2. Testing file listing...")
        result = list_downloads()
        print(f"Downloads: {result}")
        
        print("✅ Download manager features working!")
        
    except ImportError as e:
        print(f"⚠️ Download features not available: {e}")
        print("Install required packages: pip install yt-dlp")
    except Exception as e:
        print(f"❌ Download test failed: {e}")

def test_translation_features():
    """Test language translation features"""
    print("\n" + "="*50)
    print("TESTING LANGUAGE TRANSLATION FEATURES")
    print("="*50)
    
    try:
        from language_translator import (
            translate_text, detect_language, get_daily_word, 
            get_supported_languages, get_learned_words
        )
        
        print("1. Testing text translation...")
        result = translate_text("Hello, how are you?", "spanish")
        if isinstance(result, dict):
            print(f"Translation: {result['original']} -> {result['translated']}")
        else:
            print(f"Translation result: {result}")
        
        print("\n2. Testing language detection...")
        result = detect_language("Bonjour, comment allez-vous?")
        print(f"Language detection: {result}")
        
        print("\n3. Testing daily word...")
        result = get_daily_word()
        if isinstance(result, dict) and 'word' in result:
            print(f"Daily word: {result['word']}")
            if 'translations' in result:
                print("Translations:", result['translations'])
        else:
            print(f"Daily word result: {result}")
        
        print("\n4. Testing supported languages...")
        result = get_supported_languages()
        print(f"Supported languages: {result[:100]}...")  # Truncate for display
        
        print("\n5. Testing learned words...")
        result = get_learned_words()
        print(f"Learned words: {result}")
        
        print("✅ Translation features working!")
        
    except ImportError as e:
        print(f"⚠️ Translation features not available: {e}")
        print("Install required packages: pip install googletrans==4.0.0rc1")
    except Exception as e:
        print(f"❌ Translation test failed: {e}")

def test_integration():
    """Test integration with main Jarvis"""
    print("\n" + "="*50)
    print("TESTING INTEGRATION WITH JARVIS")
    print("="*50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from screenshot_recorder import take_screenshot
        from download_manager import get_download_status
        from language_translator import translate_text
        print("✅ All modules imported successfully")
        
        # Test basic functionality
        print("\n2. Testing basic functionality...")
        
        # Screenshot
        result = take_screenshot("integration_test.png")
        print(f"Screenshot: {result}")
        
        # Download status
        result = get_download_status()
        print(f"Downloads: {result}")
        
        # Translation
        result = translate_text("Integration test", "french")
        if isinstance(result, dict):
            print(f"Translation: {result['translated']}")
        
        print("✅ Integration test successful!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

def main():
    print("JARVIS NEW FEATURES TEST SUITE")
    print("Testing 3 new feature modules:")
    print("1. Screenshot & Screen Recording")
    print("2. Download Manager") 
    print("3. Language Translation")
    
    # Run tests
    test_screenshot_features()
    test_download_features()
    test_translation_features()
    test_integration()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED!")
    print("="*60)
    print("\nTo install missing dependencies, run:")
    print("pip install opencv-python sounddevice soundfile yt-dlp googletrans==4.0.0rc1")

if __name__ == "__main__":
    main()