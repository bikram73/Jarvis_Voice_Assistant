#!/usr/bin/env python3
"""
Screenshot and Screen Recording Module for Jarvis - Enhanced Version
"""

import pyautogui
import cv2
import numpy as np
import datetime
import os
import threading
import time
from PIL import Image
import subprocess
import sys

class ScreenCapture:
    def __init__(self):
        self.recording = False
        self.video_writer = None
        self.recording_thread = None
        self.current_recording_file = None
        self.recording_start_time = None
        
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
    
    def start_screen_recording(self, filename=None, with_audio=False):
        """Start screen recording that continues until stopped"""
        try:
            if self.recording:
                return "Recording is already in progress. Say 'stop recording' to end it."
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if not filename:
                filename = f"recording_{timestamp}.mp4"
            elif not filename.endswith('.mp4'):
                filename = f"{filename}.mp4"
            
            # Create recordings directory if it doesn't exist
            os.makedirs("recordings", exist_ok=True)
            self.current_recording_file = os.path.join("recordings", filename)
            
            # Get screen dimensions
            screen_size = pyautogui.size()
            
            # Define codec and create VideoWriter
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.video_writer = cv2.VideoWriter(
                self.current_recording_file, fourcc, 20.0, screen_size
            )
            
            if not self.video_writer.isOpened():
                return "Error: Could not initialize video writer"
            
            self.recording = True
            self.recording_start_time = time.time()
            
            # Start recording in a separate thread
            self.recording_thread = threading.Thread(target=self._record_screen_continuously)
            self.recording_thread.daemon = True
            self.recording_thread.start()
            
            return f"Started recording to {self.current_recording_file}. Say 'stop recording' to end."
            
        except Exception as e:
            return f"Error starting recording: {e}"
    
    def _record_screen_continuously(self):
        """Continuously record screen until stopped"""
        frame_count = 0
        
        try:
            while self.recording:
                # Capture screen
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                # Write frame to video
                self.video_writer.write(frame)
                frame_count += 1
                
                # Show recording indicator every 100 frames (about 5 seconds at 20fps)
                if frame_count % 100 == 0:
                    elapsed_time = int(time.time() - self.recording_start_time)
                    minutes = elapsed_time // 60
                    seconds = elapsed_time % 60
                    print(f"🔴 Recording... {minutes:02d}:{seconds:02d} - {frame_count} frames captured")
                
                # Control frame rate (20 FPS)
                time.sleep(0.05)
                
        except Exception as e:
            print(f"Recording error: {e}")
            self.recording = False
        
        print(f"Recording thread ended. Total frames: {frame_count}")
    
    def stop_screen_recording(self):
        """Stop the current screen recording"""
        try:
            if not self.recording:
                return "No recording in progress"
            
            # Stop recording
            self.recording = False
            
            # Wait for recording thread to finish
            if self.recording_thread and self.recording_thread.is_alive():
                self.recording_thread.join(timeout=5)
            
            # Release video writer
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
            
            # Calculate recording duration
            if self.recording_start_time:
                duration = int(time.time() - self.recording_start_time)
                minutes = duration // 60
                seconds = duration % 60
                duration_str = f"{minutes:02d}:{seconds:02d}"
            else:
                duration_str = "unknown"
            
            result_file = self.current_recording_file
            self.current_recording_file = None
            self.recording_start_time = None
            
            return f"Recording stopped and saved to {result_file}. Duration: {duration_str}"
            
        except Exception as e:
            return f"Error stopping recording: {e}"
    
    def get_recording_status(self):
        """Get current recording status"""
        if self.recording:
            elapsed_time = int(time.time() - self.recording_start_time) if self.recording_start_time else 0
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            return f"🔴 Currently recording: {minutes:02d}:{seconds:02d} - File: {os.path.basename(self.current_recording_file)}"
        else:
            return "No recording in progress"
    
    def list_screenshots(self):
        """List all screenshots with details"""
        try:
            screenshots_dir = "screenshots"
            if not os.path.exists(screenshots_dir):
                return "No screenshots directory found. Take a screenshot first!"
            
            files = []
            for file in os.listdir(screenshots_dir):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    filepath = os.path.join(screenshots_dir, file)
                    # Get file size and creation time
                    size = os.path.getsize(filepath)
                    size_mb = size / (1024 * 1024)
                    creation_time = os.path.getctime(filepath)
                    creation_date = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M")
                    
                    files.append({
                        'name': file,
                        'size_mb': size_mb,
                        'date': creation_date
                    })
            
            if not files:
                return "No screenshots found in the screenshots directory"
            
            # Sort by creation time (newest first)
            files.sort(key=lambda x: x['date'], reverse=True)
            
            result = f"📸 Found {len(files)} screenshots:\n"
            for i, file_info in enumerate(files[:10], 1):  # Show latest 10
                result += f"{i}. {file_info['name']} ({file_info['size_mb']:.1f}MB) - {file_info['date']}\n"
            
            if len(files) > 10:
                result += f"... and {len(files) - 10} more files"
            
            return result.strip()
            
        except Exception as e:
            return f"Error listing screenshots: {e}"
    
    def list_recordings(self):
        """List all recordings with details"""
        try:
            recordings_dir = "recordings"
            if not os.path.exists(recordings_dir):
                return "No recordings directory found. Start a recording first!"
            
            files = []
            for file in os.listdir(recordings_dir):
                if file.lower().endswith(('.mp4', '.avi', '.mov')):
                    filepath = os.path.join(recordings_dir, file)
                    # Get file size and creation time
                    size = os.path.getsize(filepath)
                    size_mb = size / (1024 * 1024)
                    creation_time = os.path.getctime(filepath)
                    creation_date = datetime.datetime.fromtimestamp(creation_time).strftime("%Y-%m-%d %H:%M")
                    
                    files.append({
                        'name': file,
                        'size_mb': size_mb,
                        'date': creation_date
                    })
            
            if not files:
                return "No recordings found in the recordings directory"
            
            # Sort by creation time (newest first)
            files.sort(key=lambda x: x['date'], reverse=True)
            
            result = f"🎥 Found {len(files)} recordings:\n"
            for i, file_info in enumerate(files[:10], 1):  # Show latest 10
                result += f"{i}. {file_info['name']} ({file_info['size_mb']:.1f}MB) - {file_info['date']}\n"
            
            if len(files) > 10:
                result += f"... and {len(files) - 10} more files"
            
            return result.strip()
            
        except Exception as e:
            return f"Error listing recordings: {e}"
    
    def open_screenshots_folder(self):
        """Open the screenshots folder in file explorer"""
        try:
            screenshots_dir = os.path.abspath("screenshots")
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)
            
            if sys.platform == "win32":
                os.startfile(screenshots_dir)
            elif sys.platform == "darwin":
                subprocess.run(["open", screenshots_dir])
            else:
                subprocess.run(["xdg-open", screenshots_dir])
            
            return f"Opened screenshots folder: {screenshots_dir}"
        except Exception as e:
            return f"Error opening screenshots folder: {e}"
    
    def open_recordings_folder(self):
        """Open the recordings folder in file explorer"""
        try:
            recordings_dir = os.path.abspath("recordings")
            if not os.path.exists(recordings_dir):
                os.makedirs(recordings_dir)
            
            if sys.platform == "win32":
                os.startfile(recordings_dir)
            elif sys.platform == "darwin":
                subprocess.run(["open", recordings_dir])
            else:
                subprocess.run(["xdg-open", recordings_dir])
            
            return f"Opened recordings folder: {recordings_dir}"
        except Exception as e:
            return f"Error opening recordings folder: {e}"

# Global instance
screen_capture = ScreenCapture()

# Convenience functions
def take_screenshot(filename=None):
    return screen_capture.take_screenshot(filename)

def start_recording(filename=None, with_audio=False):
    return screen_capture.start_screen_recording(filename, with_audio)

def stop_recording():
    return screen_capture.stop_screen_recording()

def get_recording_status():
    return screen_capture.get_recording_status()

def list_screenshots():
    return screen_capture.list_screenshots()

def list_recordings():
    return screen_capture.list_recordings()

def open_screenshots_folder():
    return screen_capture.open_screenshots_folder()

def open_recordings_folder():
    return screen_capture.open_recordings_folder()