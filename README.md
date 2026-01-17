# Jarvis Voice Assistant

A Python-based voice assistant that can perform various tasks through voice commands.

## Features

- **Voice Recognition**: Understands and responds to voice commands
- **Text-to-Speech**: Speaks responses back to you
- **Web Browsing**: Opens websites, searches Google and YouTube
- **Task Management**: Add and view tasks in a todo list
- **Time & Date**: Get current time and date
- **Music**: Play random music from YouTube
- **News**: Get latest news headlines (requires API key)
- **Weather**: Get weather information (requires API key)
- **Wikipedia**: Get information about topics
- **Jokes**: Tell random jokes
- **System Control**: Shutdown, restart, or exit
- **Speed Test**: Check internet speed
- **Maps**: Open Google Maps for locations

### 🆕 NEW FEATURES

#### 📸 Screenshot & Screen Recording
- **Take Screenshots**: Capture screen with custom names
- **Screen Recording**: Record screen with audio support
- **File Management**: List and organize captures
- **Custom Naming**: Save with personalized filenames

#### 📥 Download Manager
- **File Downloads**: Download files from any URL with progress tracking
- **YouTube Downloader**: Download videos and audio from YouTube
- **Progress Monitoring**: Track download status and progress
- **Organized Storage**: Automatic file organization

#### 🌍 Language Translation
- **Text Translation**: Translate text between 20+ languages
- **Speech Translation**: Listen and translate spoken words
- **Language Detection**: Automatically detect source language
- **Daily Word Learning**: Learn new words with translations
- **Vocabulary Quiz**: Test your learned words
- **Multi-language Support**: English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Turkish, Greek

## Quick Start

1. **Install Dependencies**:
   ```bash
   python setup.py
   ```

2. **Run the Assistant**:
   ```bash
   python Jarvis.py
   ```

## Manual Setup

1. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** (optional but recommended):
   - Edit the `.env` file
   - Replace placeholder values with your actual API keys
   - Get keys from:
     - [News API](https://newsapi.org/)
     - [WolframAlpha](https://developer.wolframalpha.com/)
     - [OpenWeatherMap](https://openweathermap.org/api)
     - [TMDB](https://www.themoviedb.org/settings/api)

## Voice Commands

### Basic Commands
- "Hello" / "Hi" - Greet the assistant
- "Say time" - Get current time
- "Say date" - Get current date
- "Tell me a joke" - Hear a random joke
- "Exit" / "Offline" - Close the assistant

### Web & Search
- "Google search [query]" - Search on Google
- "Play [song/video]" - Search and play on YouTube
- "Tell me about [topic]" - Get Wikipedia information
- "Open [website]" - Open predefined websites
- "Map [location]" - Open Google Maps

### Task Management
- "New task [task description]" - Add a new task
- "My task" - Hear your tasks
- "Show work" - Display tasks in notification

### Information
- "News" - Get latest headlines (requires API key)
- "Weather" - Get current weather (requires API key)
- "Weather in [city]" - Get weather for specific city
- "Speed test" - Check internet speed

### System
- "Shutdown" - Shutdown computer
- "Restart" - Restart computer
- "Play music" - Play random music
- "Exit" / "Offline" - Close assistant

### 🆕 NEW VOICE COMMANDS

#### 📸 Screenshot & Recording
- "Take screenshot" - Capture current screen
- "Take screenshot name [custom_name]" - Screenshot with custom name
- "Start recording" - Begin screen recording
- "Start recording with audio" - Record screen with audio
- "Start recording name [custom_name]" - Recording with custom name
- "Stop recording" - End current recording
- "List screenshots" - Show all screenshots
- "List recordings" - Show all recordings

#### 📥 Download Commands
- "Download file from [URL]" - Download any file
- "Download YouTube video" - Download video from YouTube
- "Download YouTube audio" - Download audio from YouTube
- "Download status" - Check download progress
- "List downloads" - Show downloaded files

#### 🌍 Translation Commands
- "Translate [text] to [language]" - Translate text
- "Translate speech to [language]" - Translate spoken words
- "Detect language" - Identify language of text
- "Daily word" / "Word of the day" - Learn new vocabulary
- "Learned words" / "My words" - Review learned words
- "Vocabulary quiz" / "Word quiz" - Test your knowledge
- "Supported languages" - List available languages

#### Example Commands:
- "Take screenshot name meeting_notes"
- "Start recording with audio name presentation"
- "Translate hello world to spanish"
- "Daily word"
- "Download YouTube audio"

## Files Structure

- `Jarvis.py` - Main assistant with full features
- `main.py` - Basic version without API dependencies
- `browsing_functionalities.py` - Web browsing functions
- `API_functionalities.py` - API-based features
- `screenshot_recorder.py` - 📸 Screenshot and screen recording module
- `download_manager.py` - 📥 File and YouTube download manager
- `language_translator.py` - 🌍 Translation and language learning module
- `websites.py` - Predefined website URLs
- `speach.py` - Speech recognition testing
- `assistant_name.txt` - Assistant name configuration
- `todo.txt` - Task storage file
- `daily_words.json` - Daily vocabulary words
- `learned_words.json` - User's learned vocabulary
- `screenshots/` - Directory for saved screenshots
- `recordings/` - Directory for screen recordings
- `downloads/` - Directory for downloaded files

## Troubleshooting

### Microphone Issues
- Ensure microphone is connected and working
- Check microphone permissions
- Try running `python speach.py` to test speech recognition

### Voice Issues
- If no voice output, check system audio
- Try changing voice in the code (voices[0] instead of voices[1])

### API Features Not Working
- Check if API keys are correctly set in `.env` file
- Verify API keys are valid and have proper permissions
- Check internet connection

### Installation Issues
- Make sure you have Python 3.7+ installed
- For PyAudio issues on Windows, try: `pip install pipwin && pipwin install pyaudio`
- For Linux, install: `sudo apt-get install python3-pyaudio`

## Requirements

- Python 3.7+
- Working microphone
- Internet connection
- Speakers/headphones for audio output

## Contributing

Feel free to contribute by:
- Adding new voice commands
- Improving error handling
- Adding new features
- Fixing bugs

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with Python and various open-source libraries
- Uses Google Translate API for translation features
- Powered by speech recognition and text-to-speech technologies
- Screen recording capabilities using OpenCV
- YouTube downloading via yt-dlp

## Disclaimer

This software is provided "as is" without warranty. Users are responsible for complying with applicable laws and terms of service when using download and translation features.