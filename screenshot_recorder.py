#!/usr/bin/env python3
"""
Screenshot and Screen Recording Module for Jarvis
"""

import pyautogui
import cv2
import numpy as np
import datetime
import os
import threading
import time
from PIL import Image
import sounddevice as sd
import soundfile as sf

class ScreenCapture:
    def __init__(self):
        self.recording = False
        self.video_writer = None
        self.audio_data = []
        self.sample_rate = 44100
        
    def take_screenshot(self, filename=None):
        """Take a screenshot and save it"""
        try:
            if not filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            # Create screenshots directory if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            filepath = os.path.join("screenshots", filename)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            return f"Screenshot saved as {filepath}"
            
        except Exception as e:
            return f"Error taking screenshot: {e}"
    
    def start_screen_recording(self, filename=None, with_audio=True):
        """Start screen recording with optional audio"""
        try:
            if self.recording:
                return "Recording is already in progress"
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if not filename:
                filename = f"recording_{timestamp}.mp4"
            
            # Create recordings directory if it doesn't exist
            os.makedirs("recordings", exist_ok=True)
            self.video_filepath = os.path.join("recordings", filename)
            self.audio_filepath = os.path.join("recordings", f"audio_{timestamp}.wav")
            
            # Get screen dimensions
            screen_size = pyautogui.size()
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.video_writer = cv2.VideoWriter(
                self.video_filepath, fourcc, 20.0, screen_size
            )
            
            self.recording = True
            self.with_audio = with_audio
            
            # Start recording threads
            self.video_thread = threading.Thread(target=self._record_video)
            self.video_thread.start()
            
            if with_audio:
                self.audio_thread = threading.Thread(target=self._record_audio)
                self.audio_thread.start()
            
            return f"Started recording to {self.video_filepath}"
            
        except Exception as e:
            return f"Error starting recording: {e}"
    
    def stop_screen_recording(self):
        """Stop screen recording"""
        try:
            if not self.recording:
                return "No recording in progress"
            
            self.recording = False
            
            # Wait for threads to finish
            if hasattr(self, 'video_thread'):
                self.video_thread.join()
            
            if hasattr(self, 'audio_thread') and self.with_audio:
                self.audio_thread.join()
                # Save audio
                if self.audio_data:
                    audio_array = np.concatenate(self.audio_data, axis=0)
                    sf.write(self.audio_filepath, audio_array, self.sample_rate)
            
            # Release video writer
            if self.video_writer:
                self.video_writer.release()
            
            return f"Recording stopped and saved to {self.video_filepath}"
            
        except Exception as e:
            return f"Error stopping recording: {e}"
    
    def _record_video(self):
        """Internal method to record video frames"""
        while self.recording:
            try:
                # Capture screen
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Write frame
                self.video_writer.write(frame)
                
                # Control frame rate
                time.sleep(0.05)  # 20 FPS
                
            except Exception as e:
                print(f"Video recording error: {e}")
                break
    
    def _record_audio(self):
        """Internal method to record audio"""
        def audio_callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())
        
        try:
            with sd.InputStream(callback=audio_callback, 
                              samplerate=self.sample_rate, 
                              channels=2):
                while self.recording:
                    time.sleep(0.1)
        except Exception as e:
            print(f"Audio recording error: {e}")
    
    def list_screenshots(self):
        """List all screenshots"""
        try:
            if not os.path.exists("screenshots"):
                return "No screenshots directory found"
            
            files = os.listdir("screenshots")
            screenshots = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg'))]
            
            if not screenshots:
                return "No screenshots found"
            
            return f"Found {len(screenshots)} screenshots: " + ", ".join(screenshots)
            
        except Exception as e:
            return f"Error listing screenshots: {e}"
    
    def list_recordings(self):
        """List all recordings"""
        try:
            if not os.path.exists("recordings"):
                return "No recordings directory found"
            
            files = os.listdir("recordings")
            recordings = [f for f in files if f.endswith(('.mp4', '.avi'))]
            
            if not recordings:
                return "No recordings found"
            
            return f"Found {len(recordings)} recordings: " + ", ".join(recordings)
            
        except Exception as e:
            return f"Error listing recordings: {e}"

# Global instance
screen_capture = ScreenCapture()

# Convenience functions
def take_screenshot(filename=None):
    return screen_capture.take_screenshot(filename)

def start_recording(filename=None, with_audio=True):
    return screen_capture.start_screen_recording(filename, with_audio)

def stop_recording():
    return screen_capture.stop_screen_recording()

def list_screenshots():
    return screen_capture.list_screenshots()

def list_recordings():
    return screen_capture.list_recordings()