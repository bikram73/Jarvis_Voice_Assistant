#!/usr/bin/env python3
"""
System Control Module for Jarvis
"""

import os
import subprocess
import psutil
import ctypes
from ctypes import wintypes
import time
import shutil

class SystemController:
    def __init__(self):
        self.is_windows = os.name == 'nt'
        self.is_locked = False
    
    def lock_screen(self):
        """Lock the computer screen"""
        try:
            if self.is_windows:
                # Windows lock screen
                ctypes.windll.user32.LockWorkStation()
                return "Screen locked successfully"
            else:
                # Linux/Mac alternatives
                try:
                    subprocess.run(['gnome-screensaver-command', '--lock'], check=True)
                    return "Screen locked successfully"
                except:
                    try:
                        subprocess.run(['xdg-screensaver', 'lock'], check=True)
                        return "Screen locked successfully"
                    except:
                        return "Could not lock screen on this system"
        except Exception as e:
            return f"Error locking screen: {e}"
    
    def sleep_system(self):
        """Put the system to sleep"""
        try:
            if self.is_windows:
                # Windows sleep
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return "System going to sleep"
            else:
                # Linux sleep
                try:
                    subprocess.run(['systemctl', 'suspend'], check=True)
                    return "System going to sleep"
                except:
                    try:
                        subprocess.run(['pm-suspend'], check=True)
                        return "System going to sleep"
                    except:
                        return "Could not put system to sleep"
        except Exception as e:
            return f"Error putting system to sleep: {e}"
    
    def hibernate_system(self):
        """Hibernate the system"""
        try:
            if self.is_windows:
                # Windows hibernate
                os.system("shutdown /h")
                return "System hibernating"
            else:
                # Linux hibernate
                try:
                    subprocess.run(['systemctl', 'hibernate'], check=True)
                    return "System hibernating"
                except:
                    try:
                        subprocess.run(['pm-hibernate'], check=True)
                        return "System hibernating"
                    except:
                        return "Could not hibernate system"
        except Exception as e:
            return f"Error hibernating system: {e}"
    
    def empty_recycle_bin(self):
        """Empty the recycle bin/trash"""
        try:
            if self.is_windows:
                # Windows recycle bin
                import winshell
                try:
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                    return "Recycle bin emptied successfully"
                except ImportError:
                    # Fallback method for Windows
                    try:
                        subprocess.run(['PowerShell', '-Command', 
                                      'Clear-RecycleBin -Force'], 
                                     check=True, capture_output=True)
                        return "Recycle bin emptied successfully"
                    except:
                        return "Could not empty recycle bin. You may need to install winshell: pip install winshell"
            else:
                # Linux trash
                trash_dirs = [
                    os.path.expanduser("~/.local/share/Trash/files"),
                    os.path.expanduser("~/.Trash"),
                    "/tmp"
                ]
                
                emptied = False
                for trash_dir in trash_dirs:
                    if os.path.exists(trash_dir):
                        try:
                            for item in os.listdir(trash_dir):
                                item_path = os.path.join(trash_dir, item)
                                if os.path.isdir(item_path):
                                    shutil.rmtree(item_path)
                                else:
                                    os.remove(item_path)
                            emptied = True
                        except:
                            continue
                
                return "Trash emptied successfully" if emptied else "Could not empty trash"
                
        except Exception as e:
            return f"Error emptying recycle bin: {e}"
    
    def get_battery_status(self):
        """Get battery status and percentage"""
        try:
            battery = psutil.sensors_battery()
            
            if battery is None:
                return "No battery found (desktop computer or battery not detected)"
            
            percent = battery.percent
            plugged = battery.power_plugged
            
            # Estimate time remaining
            if hasattr(battery, 'secsleft') and battery.secsleft != psutil.POWER_TIME_UNLIMITED:
                if battery.secsleft != psutil.POWER_TIME_UNKNOWN:
                    hours, remainder = divmod(battery.secsleft, 3600)
                    minutes, _ = divmod(remainder, 60)
                    time_left = f"{int(hours)}h {int(minutes)}m"
                else:
                    time_left = "Unknown"
            else:
                time_left = "Unlimited" if plugged else "Unknown"
            
            status = "Charging" if plugged else "Discharging"
            
            # Battery health indicator
            if percent >= 80:
                health = "Excellent"
            elif percent >= 60:
                health = "Good"
            elif percent >= 40:
                health = "Fair"
            elif percent >= 20:
                health = "Low"
            else:
                health = "Critical"
            
            return f"Battery: {percent}% ({status}), Time remaining: {time_left}, Status: {health}"
            
        except Exception as e:
            return f"Error getting battery status: {e}"
    
    def get_system_info(self):
        """Get basic system information"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # System uptime
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_hours = uptime_seconds // 3600
            
            info = f"System Status - CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent:.1f}%, Uptime: {uptime_hours:.1f}h"
            
            return info
            
        except Exception as e:
            return f"Error getting system info: {e}"
    
    def force_close_application(self, app_name):
        """Force close an application by name"""
        try:
            closed_processes = []
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if app_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        closed_processes.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed_processes:
                return f"Closed applications: {', '.join(closed_processes)}"
            else:
                return f"No running applications found matching '{app_name}'"
                
        except Exception as e:
            return f"Error closing application: {e}"
    
    def list_running_processes(self, limit=10):
        """List top running processes by CPU usage"""
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 0:
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            if not processes:
                return "No active processes found"
            
            result = f"Top {min(limit, len(processes))} processes by CPU usage:\n"
            for i, proc in enumerate(processes[:limit]):
                result += f"{i+1}. {proc['name']} - {proc['cpu_percent']}% CPU\n"
            
            return result.strip()
            
        except Exception as e:
            return f"Error listing processes: {e}"

# Global instance
system_controller = SystemController()

# Convenience functions
def lock_screen():
    return system_controller.lock_screen()

def sleep_system():
    return system_controller.sleep_system()

def hibernate_system():
    return system_controller.hibernate_system()

def empty_recycle_bin():
    return system_controller.empty_recycle_bin()

def get_battery_status():
    return system_controller.get_battery_status()

def get_system_info():
    return system_controller.get_system_info()

def force_close_app(app_name):
    return system_controller.force_close_application(app_name)

def list_processes(limit=10):
    return system_controller.list_running_processes(limit)