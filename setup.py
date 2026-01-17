#!/usr/bin/env python3
"""
Setup script for Jarvis Voice Assistant
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False

def check_microphone():
    """Check if microphone is available"""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("✓ Microphone detected and working!")
            return True
    except Exception as e:
        print(f"✗ Microphone issue: {e}")
        print("Please ensure you have a working microphone connected.")
        return False

def setup_env_file():
    """Guide user through setting up API keys"""
    print("\n" + "="*50)
    print("API KEYS SETUP")
    print("="*50)
    print("To use all features, you'll need to get API keys from:")
    print("1. News API: https://newsapi.org/")
    print("2. WolframAlpha: https://developer.wolframalpha.com/")
    print("3. OpenWeatherMap: https://openweathermap.org/api")
    print("4. TMDB: https://www.themoviedb.org/settings/api")
    print("\nEdit the .env file and replace 'your_api_key_here' with your actual keys.")
    print("Note: The assistant will work without API keys, but some features will be limited.")

def main():
    print("="*50)
    print("JARVIS VOICE ASSISTANT SETUP")
    print("="*50)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please check the error messages above.")
        return
    
    # Check microphone
    if not check_microphone():
        print("Warning: Microphone issues detected. Voice recognition may not work properly.")
    
    # Setup environment file
    setup_env_file()
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print("To start Jarvis, run: python Jarvis.py")
    print("For basic functionality without API keys, run: python main.py")

if __name__ == "__main__":
    main()