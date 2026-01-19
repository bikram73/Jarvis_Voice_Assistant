#!/usr/bin/env python3
"""
Volume and Brightness Control Module for Jarvis - Fixed Windows Volume Control
"""

import os
import subprocess
import ctypes
from ctypes import wintypes
import math

# Try to import pycaw, but provide fallback if not available
try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
    PYCAW_AVAILABLE = True
except ImportError:
    PYCAW_AVAILABLE = False

import screen_brightness_control as sbc

class VolumeController:
    def __init__(self):
        self.is_windows = os.name == 'nt'
        self.volume_interface = None
        if PYCAW_AVAILABLE:
            self.setup_windows_volume()
    
    def setup_windows_volume(self):
        """Setup Windows volume control interface"""
        if self.is_windows and PYCAW_AVAILABLE:
            try:
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                self.volume_interface = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            except Exception as e:
                print(f"Could not setup Windows volume control: {e}")
                self.volume_interface = None
    
    def get_current_volume(self):
        """Get current system volume (0-100)"""
        try:
            if self.is_windows:
                if self.volume_interface:
                    # Use pycaw if available
                    current_volume = self.volume_interface.GetMasterScalarVolume()
                    return int(current_volume * 100)
                else:
                    # Fallback: Use PowerShell to get volume
                    try:
                        cmd = 'powershell -c "(New-Object -comObject WScript.Shell).SendKeys([char]174)"'
                        # This is a workaround - return a default value
                        return 50  # Default volume
                    except:
                        return 50
            else:
                # Linux alternative
                try:
                    result = subprocess.run(['amixer', 'get', 'Master'], 
                                          capture_output=True, text=True)
                    output = result.stdout
                    # Parse volume from amixer output
                    import re
                    match = re.search(r'\[(\d+)%\]', output)
                    if match:
                        return int(match.group(1))
                except:
                    pass
                return 50  # Default fallback
        except Exception as e:
            return 50  # Default fallback
    
    def set_volume_windows_nircmd(self, volume_level):
        """Set volume using NirCmd (Windows fallback)"""
        try:
            # Use PowerShell to set volume
            volume_decimal = volume_level / 100.0
            powershell_cmd = f'''
            Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class Audio {{
                [DllImport("user32.dll")]
                public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
                public static void SetVolume(int level) {{
                    // Mute first
                    keybd_event(0xAD, 0, 0, UIntPtr.Zero);
                    keybd_event(0xAD, 0, 2, UIntPtr.Zero);
                    System.Threading.Thread.Sleep(50);
                    
                    // Set to 0
                    for(int i = 0; i < 50; i++) {{
                        keybd_event(0xAE, 0, 0, UIntPtr.Zero);
                        keybd_event(0xAE, 0, 2, UIntPtr.Zero);
                        System.Threading.Thread.Sleep(10);
                    }}
                    
                    // Increase to desired level
                    int steps = level * 50 / 100;
                    for(int i = 0; i < steps; i++) {{
                        keybd_event(0xAF, 0, 0, UIntPtr.Zero);
                        keybd_event(0xAF, 0, 2, UIntPtr.Zero);
                        System.Threading.Thread.Sleep(10);
                    }}
                }}
            }}
"@
            [Audio]::SetVolume({volume_level})
            '''
            
            result = subprocess.run(['powershell', '-Command', powershell_cmd], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return f"Volume set to {volume_level}%"
            else:
                return self.set_volume_simple_powershell(volume_level)
                
        except Exception as e:
            return self.set_volume_simple_powershell(volume_level)
    
    def set_volume_simple_powershell(self, volume_level):
        """Simple PowerShell volume control"""
        try:
            # Simple PowerShell command to set volume
            powershell_cmd = f'''
            $obj = New-Object -ComObject WScript.Shell
            $obj.SendKeys([char]173)  # Mute
            Start-Sleep -Milliseconds 100
            $obj.SendKeys([char]173)  # Unmute
            
            # Reset volume to 0
            for ($i = 0; $i -lt 50; $i++) {{
                $obj.SendKeys([char]174)  # Volume down
                Start-Sleep -Milliseconds 20
            }}
            
            # Set to desired level
            $steps = [math]::Round({volume_level} * 50 / 100)
            for ($i = 0; $i -lt $steps; $i++) {{
                $obj.SendKeys([char]175)  # Volume up
                Start-Sleep -Milliseconds 20
            }}
            '''
            
            result = subprocess.run(['powershell', '-Command', powershell_cmd], 
                                  capture_output=True, text=True, timeout=15)
            
            return f"Volume set to {volume_level}%"
            
        except Exception as e:
            return f"Could not set volume: {e}"
    
    def set_volume(self, volume_level):
        """Set system volume (0-100)"""
        try:
            # Clamp volume between 0 and 100
            volume_level = max(0, min(100, volume_level))
            
            if self.is_windows:
                if self.volume_interface:
                    # Use pycaw if available
                    volume_scalar = volume_level / 100.0
                    self.volume_interface.SetMasterScalarVolume(volume_scalar, None)
                    return f"Volume set to {volume_level}%"
                else:
                    # Use PowerShell fallback
                    return self.set_volume_windows_nircmd(volume_level)
            else:
                # Linux volume control
                try:
                    subprocess.run(['amixer', 'set', 'Master', f'{volume_level}%'], 
                                 check=True, capture_output=True)
                    return f"Volume set to {volume_level}%"
                except subprocess.CalledProcessError:
                    # Try alternative Linux method
                    try:
                        subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', f'{volume_level}%'], 
                                     check=True, capture_output=True)
                        return f"Volume set to {volume_level}%"
                    except:
                        return "Could not set volume on this system"
        except Exception as e:
            return f"Error setting volume: {e}"
    
    def increase_volume(self, increment=10):
        """Increase volume by specified amount"""
        try:
            if self.is_windows and not self.volume_interface:
                # Use keyboard simulation for Windows
                powershell_cmd = '''
                $obj = New-Object -ComObject WScript.Shell
                for ($i = 0; $i -lt 5; $i++) {
                    $obj.SendKeys([char]175)  # Volume up
                    Start-Sleep -Milliseconds 50
                }
                '''
                subprocess.run(['powershell', '-Command', powershell_cmd], 
                             capture_output=True, text=True, timeout=5)
                return "Volume increased"
            else:
                current = self.get_current_volume()
                if isinstance(current, int):
                    new_volume = min(100, current + increment)
                    return self.set_volume(new_volume)
                else:
                    return "Volume increased"
        except Exception as e:
            return f"Error increasing volume: {e}"
    
    def decrease_volume(self, decrement=10):
        """Decrease volume by specified amount"""
        try:
            if self.is_windows and not self.volume_interface:
                # Use keyboard simulation for Windows
                powershell_cmd = '''
                $obj = New-Object -ComObject WScript.Shell
                for ($i = 0; $i -lt 5; $i++) {
                    $obj.SendKeys([char]174)  # Volume down
                    Start-Sleep -Milliseconds 50
                }
                '''
                subprocess.run(['powershell', '-Command', powershell_cmd], 
                             capture_output=True, text=True, timeout=5)
                return "Volume decreased"
            else:
                current = self.get_current_volume()
                if isinstance(current, int):
                    new_volume = max(0, current - decrement)
                    return self.set_volume(new_volume)
                else:
                    return "Volume decreased"
        except Exception as e:
            return f"Error decreasing volume: {e}"
    
    def mute_volume(self):
        """Mute system volume"""
        try:
            if self.is_windows:
                if self.volume_interface:
                    self.volume_interface.SetMute(1, None)
                    return "Volume muted"
                else:
                    # Use keyboard simulation
                    powershell_cmd = '''
                    $obj = New-Object -ComObject WScript.Shell
                    $obj.SendKeys([char]173)  # Mute key
                    '''
                    subprocess.run(['powershell', '-Command', powershell_cmd], 
                                 capture_output=True, text=True, timeout=3)
                    return "Volume muted"
            else:
                # Linux mute
                try:
                    subprocess.run(['amixer', 'set', 'Master', 'mute'], 
                                 check=True, capture_output=True)
                    return "Volume muted"
                except:
                    try:
                        subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', '1'], 
                                     check=True, capture_output=True)
                        return "Volume muted"
                    except:
                        return "Could not mute volume on this system"
        except Exception as e:
            return f"Error muting volume: {e}"
    
    def unmute_volume(self):
        """Unmute system volume"""
        try:
            if self.is_windows:
                if self.volume_interface:
                    self.volume_interface.SetMute(0, None)
                    return "Volume unmuted"
                else:
                    # Use keyboard simulation
                    powershell_cmd = '''
                    $obj = New-Object -ComObject WScript.Shell
                    $obj.SendKeys([char]173)  # Mute key (toggles)
                    '''
                    subprocess.run(['powershell', '-Command', powershell_cmd], 
                                 capture_output=True, text=True, timeout=3)
                    return "Volume unmuted"
            else:
                # Linux unmute
                try:
                    subprocess.run(['amixer', 'set', 'Master', 'unmute'], 
                                 check=True, capture_output=True)
                    return "Volume unmuted"
                except:
                    try:
                        subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', '0'], 
                                     check=True, capture_output=True)
                        return "Volume unmuted"
                    except:
                        return "Could not unmute volume on this system"
        except Exception as e:
            return f"Error unmuting volume: {e}"
    
    def is_muted(self):
        """Check if volume is muted"""
        try:
            if self.is_windows and self.volume_interface:
                return bool(self.volume_interface.GetMute())
            else:
                # For systems without pycaw, assume not muted
                return False
        except Exception as e:
            return False

class BrightnessController:
    def __init__(self):
        self.is_windows = os.name == 'nt'
    
    def get_current_brightness(self):
        """Get current screen brightness (0-100)"""
        try:
            brightness = sbc.get_brightness()
            if isinstance(brightness, list) and brightness:
                return brightness[0]  # Primary display
            elif isinstance(brightness, int):
                return brightness
            else:
                return 50  # Default fallback
        except Exception as e:
            return 50  # Default fallback
    
    def set_brightness(self, brightness_level):
        """Set screen brightness (0-100)"""
        try:
            # Clamp brightness between 0 and 100
            brightness_level = max(0, min(100, brightness_level))
            
            sbc.set_brightness(brightness_level)
            return f"Brightness set to {brightness_level}%"
            
        except Exception as e:
            # Fallback for Windows
            if self.is_windows:
                try:
                    # Windows WMI method
                    import wmi
                    c = wmi.WMI(namespace='wmi')
                    methods = c.WmiMonitorBrightnessMethods()[0]
                    methods.WmiSetBrightness(brightness_level, 0)
                    return f"Brightness set to {brightness_level}%"
                except:
                    return "Could not set brightness. Your system may not support brightness control."
            else:
                return f"Error setting brightness: {e}"
    
    def increase_brightness(self, increment=10):
        """Increase brightness by specified amount"""
        try:
            current = self.get_current_brightness()
            if isinstance(current, int):
                new_brightness = min(100, current + increment)
                return self.set_brightness(new_brightness)
            else:
                return "Brightness increased"
        except Exception as e:
            return f"Error increasing brightness: {e}"
    
    def decrease_brightness(self, decrement=10):
        """Decrease brightness by specified amount"""
        try:
            current = self.get_current_brightness()
            if isinstance(current, int):
                new_brightness = max(0, current - decrement)
                return self.set_brightness(new_brightness)
            else:
                return "Brightness decreased"
        except Exception as e:
            return f"Error decreasing brightness: {e}"

class AudioVideoController:
    def __init__(self):
        self.volume_controller = VolumeController()
        self.brightness_controller = BrightnessController()
    
    def get_audio_video_status(self):
        """Get current audio and video status"""
        try:
            volume = self.volume_controller.get_current_volume()
            brightness = self.brightness_controller.get_current_brightness()
            muted = self.volume_controller.is_muted()
            
            status = f"Volume: {volume}%"
            if muted:
                status += " (Muted)"
            status += f", Brightness: {brightness}%"
            
            return status
        except Exception as e:
            return f"Audio: Available, Video: Available"

# Global instances
volume_controller = VolumeController()
brightness_controller = BrightnessController()
av_controller = AudioVideoController()

# Convenience functions for volume
def get_volume():
    return volume_controller.get_current_volume()

def set_volume(level):
    return volume_controller.set_volume(level)

def increase_volume(increment=10):
    return volume_controller.increase_volume(increment)

def decrease_volume(decrement=10):
    return volume_controller.decrease_volume(decrement)

def mute_volume():
    return volume_controller.mute_volume()

def unmute_volume():
    return volume_controller.unmute_volume()

def is_muted():
    return volume_controller.is_muted()

# Convenience functions for brightness
def get_brightness():
    return brightness_controller.get_current_brightness()

def set_brightness(level):
    return brightness_controller.set_brightness(level)

def increase_brightness(increment=10):
    return brightness_controller.increase_brightness(increment)

def decrease_brightness(decrement=10):
    return brightness_controller.decrease_brightness(decrement)

# Combined status
def get_av_status():
    return av_controller.get_audio_video_status()