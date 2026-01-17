#!/usr/bin/env python3
"""
Language Translation Module for Jarvis
"""

import requests
import json
import random
import datetime
import os
from googletrans import Translator
import speech_recognition as sr
import pyttsx3

class LanguageTranslator:
    def __init__(self):
        self.translator = Translator()
        self.daily_words_file = "daily_words.json"
        self.learned_words_file = "learned_words.json"
        self.load_daily_words()
        
        # Common language codes
        self.languages = {
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'italian': 'it',
            'portuguese': 'pt',
            'russian': 'ru',
            'chinese': 'zh',
            'japanese': 'ja',
            'korean': 'ko',
            'arabic': 'ar',
            'hindi': 'hi',
            'dutch': 'nl',
            'swedish': 'sv',
            'norwegian': 'no',
            'danish': 'da',
            'finnish': 'fi',
            'polish': 'pl',
            'turkish': 'tr',
            'greek': 'el'
        }
    
    def translate_text(self, text, target_language, source_language='auto'):
        """Translate text to target language"""
        try:
            # Convert language names to codes
            if target_language.lower() in self.languages:
                target_lang = self.languages[target_language.lower()]
            else:
                target_lang = target_language
            
            if source_language.lower() in self.languages:
                source_lang = self.languages[source_language.lower()]
            else:
                source_lang = source_language
            
            # Perform translation
            result = self.translator.translate(text, dest=target_lang, src=source_lang)
            
            return {
                'original': text,
                'translated': result.text,
                'source_language': result.src,
                'target_language': target_lang,
                'confidence': getattr(result, 'confidence', None)
            }
            
        except Exception as e:
            return f"Translation error: {e}"
    
    def detect_language(self, text):
        """Detect the language of given text"""
        try:
            detection = self.translator.detect(text)
            
            # Find language name from code
            lang_name = None
            for name, code in self.languages.items():
                if code == detection.lang:
                    lang_name = name
                    break
            
            return {
                'language_code': detection.lang,
                'language_name': lang_name or detection.lang,
                'confidence': detection.confidence
            }
            
        except Exception as e:
            return f"Language detection error: {e}"
    
    def translate_speech(self, target_language):
        """Listen to speech and translate it"""
        try:
            # Initialize speech recognition
            r = sr.Recognizer()
            
            with sr.Microphone() as source:
                print("Listening for speech to translate...")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=10)
            
            # Recognize speech
            text = r.recognize_google(audio)
            print(f"Recognized: {text}")
            
            # Translate
            translation = self.translate_text(text, target_language)
            
            if isinstance(translation, dict):
                return f"Original: {translation['original']}\nTranslated to {target_language}: {translation['translated']}"
            else:
                return translation
                
        except sr.WaitTimeoutError:
            return "No speech detected within timeout"
        except sr.UnknownValueError:
            return "Could not understand the speech"
        except Exception as e:
            return f"Speech translation error: {e}"
    
    def get_daily_word(self):
        """Get today's word to learn"""
        try:
            today = datetime.date.today().isoformat()
            
            if today in self.daily_words and self.daily_words[today]:
                return self.daily_words[today]
            
            # Generate new daily word
            word_data = self.generate_daily_word()
            self.daily_words[today] = word_data
            self.save_daily_words()
            
            return word_data
            
        except Exception as e:
            return f"Error getting daily word: {e}"
    
    def generate_daily_word(self):
        """Generate a new word to learn"""
        try:
            # Sample words for learning (you can expand this list)
            sample_words = [
                "serendipity", "ephemeral", "wanderlust", "petrichor", "luminous",
                "mellifluous", "ethereal", "quintessential", "ubiquitous", "resilient",
                "eloquent", "magnificent", "tranquil", "harmonious", "brilliant",
                "fascinating", "extraordinary", "remarkable", "incredible", "wonderful"
            ]
            
            word = random.choice(sample_words)
            
            # Get translations in multiple languages
            translations = {}
            for lang_name, lang_code in list(self.languages.items())[:5]:  # First 5 languages
                try:
                    result = self.translator.translate(word, dest=lang_code)
                    translations[lang_name] = result.text
                except:
                    continue
            
            return {
                'word': word,
                'translations': translations,
                'date': datetime.date.today().isoformat()
            }
            
        except Exception as e:
            return {'error': f"Error generating daily word: {e}"}
    
    def add_learned_word(self, word, translation, language):
        """Add a word to learned words list"""
        try:
            learned_words = self.load_learned_words()
            
            word_entry = {
                'word': word,
                'translation': translation,
                'language': language,
                'date_learned': datetime.date.today().isoformat()
            }
            
            learned_words.append(word_entry)
            
            with open(self.learned_words_file, 'w') as f:
                json.dump(learned_words, f, indent=2)
            
            return f"Added '{word}' ({translation} in {language}) to learned words"
            
        except Exception as e:
            return f"Error adding learned word: {e}"
    
    def get_learned_words(self, limit=10):
        """Get recently learned words"""
        try:
            learned_words = self.load_learned_words()
            
            if not learned_words:
                return "No learned words found"
            
            recent_words = learned_words[-limit:]
            
            result = f"Recent learned words ({len(recent_words)}):\n"
            for word_data in recent_words:
                result += f"- {word_data['word']} = {word_data['translation']} ({word_data['language']})\n"
            
            return result
            
        except Exception as e:
            return f"Error getting learned words: {e}"
    
    def load_daily_words(self):
        """Load daily words from file"""
        try:
            if os.path.exists(self.daily_words_file):
                with open(self.daily_words_file, 'r') as f:
                    self.daily_words = json.load(f)
            else:
                self.daily_words = {}
        except:
            self.daily_words = {}
    
    def save_daily_words(self):
        """Save daily words to file"""
        try:
            with open(self.daily_words_file, 'w') as f:
                json.dump(self.daily_words, f, indent=2)
        except Exception as e:
            print(f"Error saving daily words: {e}")
    
    def load_learned_words(self):
        """Load learned words from file"""
        try:
            if os.path.exists(self.learned_words_file):
                with open(self.learned_words_file, 'r') as f:
                    return json.load(f)
            else:
                return []
        except:
            return []
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return "Supported languages: " + ", ".join(self.languages.keys())
    
    def quiz_mode(self):
        """Start a vocabulary quiz"""
        try:
            learned_words = self.load_learned_words()
            
            if len(learned_words) < 3:
                return "You need at least 3 learned words to start a quiz"
            
            # Select random words for quiz
            quiz_words = random.sample(learned_words, min(5, len(learned_words)))
            
            quiz_result = "Vocabulary Quiz:\n"
            for i, word_data in enumerate(quiz_words, 1):
                quiz_result += f"{i}. What does '{word_data['word']}' mean in {word_data['language']}?\n"
                quiz_result += f"   Answer: {word_data['translation']}\n\n"
            
            return quiz_result
            
        except Exception as e:
            return f"Error starting quiz: {e}"

# Global instance
language_translator = LanguageTranslator()

# Convenience functions
def translate_text(text, target_language, source_language='auto'):
    return language_translator.translate_text(text, target_language, source_language)

def detect_language(text):
    return language_translator.detect_language(text)

def translate_speech(target_language):
    return language_translator.translate_speech(target_language)

def get_daily_word():
    return language_translator.get_daily_word()

def add_learned_word(word, translation, language):
    return language_translator.add_learned_word(word, translation, language)

def get_learned_words(limit=10):
    return language_translator.get_learned_words(limit)

def get_supported_languages():
    return language_translator.get_supported_languages()

def start_quiz():
    return language_translator.quiz_mode()