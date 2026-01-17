#!/usr/bin/env python3
"""
Download Manager Module for Jarvis
"""

import requests
import os
import threading
from urllib.parse import urlparse
import yt_dlp
import time
from pathlib import Path

class DownloadManager:
    def __init__(self):
        self.downloads = {}
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
    
    def download_file(self, url, filename=None, progress_callback=None):
        """Download a file from URL with progress tracking"""
        try:
            # Parse URL to get filename if not provided
            if not filename:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = "downloaded_file"
            
            filepath = os.path.join(self.download_dir, filename)
            
            # Start download in thread
            download_id = len(self.downloads) + 1
            self.downloads[download_id] = {
                'url': url,
                'filename': filename,
                'filepath': filepath,
                'status': 'starting',
                'progress': 0,
                'size': 0,
                'downloaded': 0
            }
            
            thread = threading.Thread(
                target=self._download_worker,
                args=(download_id, url, filepath, progress_callback)
            )
            thread.start()
            
            return f"Started download #{download_id}: {filename}"
            
        except Exception as e:
            return f"Error starting download: {e}"
    
    def _download_worker(self, download_id, url, filepath, progress_callback):
        """Worker thread for downloading files"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            self.downloads[download_id]['size'] = total_size
            self.downloads[download_id]['status'] = 'downloading'
            
            downloaded = 0
            
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        
                        # Update progress
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            self.downloads[download_id]['progress'] = progress
                            self.downloads[download_id]['downloaded'] = downloaded
                            
                            if progress_callback:
                                progress_callback(download_id, progress, downloaded, total_size)
            
            self.downloads[download_id]['status'] = 'completed'
            
        except Exception as e:
            self.downloads[download_id]['status'] = f'error: {e}'
    
    def download_youtube_video(self, url, quality='best', audio_only=False):
        """Download YouTube video or audio"""
        try:
            download_id = len(self.downloads) + 1
            
            # Configure yt-dlp options
            ydl_opts = {
                'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [lambda d: self._youtube_progress_hook(download_id, d)],
            }
            
            if audio_only:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            else:
                ydl_opts['format'] = quality
            
            # Initialize download tracking
            self.downloads[download_id] = {
                'url': url,
                'type': 'youtube_audio' if audio_only else 'youtube_video',
                'status': 'starting',
                'progress': 0,
                'title': 'Unknown'
            }
            
            # Start download in thread
            thread = threading.Thread(
                target=self._youtube_download_worker,
                args=(download_id, url, ydl_opts)
            )
            thread.start()
            
            content_type = "audio" if audio_only else "video"
            return f"Started YouTube {content_type} download #{download_id}"
            
        except Exception as e:
            return f"Error starting YouTube download: {e}"
    
    def _youtube_download_worker(self, download_id, url, ydl_opts):
        """Worker thread for YouTube downloads"""
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Get video info first
                info = ydl.extract_info(url, download=False)
                self.downloads[download_id]['title'] = info.get('title', 'Unknown')
                
                # Download
                ydl.download([url])
                self.downloads[download_id]['status'] = 'completed'
                
        except Exception as e:
            self.downloads[download_id]['status'] = f'error: {e}'
    
    def _youtube_progress_hook(self, download_id, d):
        """Progress hook for YouTube downloads"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.downloads[download_id]['progress'] = progress
                self.downloads[download_id]['status'] = 'downloading'
        elif d['status'] == 'finished':
            self.downloads[download_id]['progress'] = 100
            self.downloads[download_id]['status'] = 'processing'
    
    def get_download_status(self, download_id=None):
        """Get status of downloads"""
        try:
            if download_id:
                if download_id in self.downloads:
                    download = self.downloads[download_id]
                    return f"Download #{download_id}: {download['status']} - {download.get('progress', 0):.1f}%"
                else:
                    return f"Download #{download_id} not found"
            else:
                if not self.downloads:
                    return "No downloads found"
                
                status_list = []
                for dl_id, download in self.downloads.items():
                    status = f"#{dl_id}: {download['status']} - {download.get('progress', 0):.1f}%"
                    status_list.append(status)
                
                return "Downloads: " + ", ".join(status_list)
                
        except Exception as e:
            return f"Error getting download status: {e}"
    
    def list_downloaded_files(self):
        """List all downloaded files"""
        try:
            if not os.path.exists(self.download_dir):
                return "No downloads directory found"
            
            files = os.listdir(self.download_dir)
            if not files:
                return "No downloaded files found"
            
            return f"Downloaded files ({len(files)}): " + ", ".join(files)
            
        except Exception as e:
            return f"Error listing files: {e}"
    
    def cancel_download(self, download_id):
        """Cancel a download (basic implementation)"""
        try:
            if download_id in self.downloads:
                self.downloads[download_id]['status'] = 'cancelled'
                return f"Download #{download_id} cancelled"
            else:
                return f"Download #{download_id} not found"
        except Exception as e:
            return f"Error cancelling download: {e}"

# Global instance
download_manager = DownloadManager()

# Convenience functions
def download_file(url, filename=None):
    return download_manager.download_file(url, filename)

def download_youtube_video(url, quality='best'):
    return download_manager.download_youtube_video(url, quality, audio_only=False)

def download_youtube_audio(url):
    return download_manager.download_youtube_video(url, audio_only=True)

def get_download_status(download_id=None):
    return download_manager.get_download_status(download_id)

def list_downloads():
    return download_manager.list_downloaded_files()

def cancel_download(download_id):
    return download_manager.cancel_download(download_id)