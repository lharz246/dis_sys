#!/usr/bin/env python3
import sys
import time
import os
import signal
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import daemon
import daemon.pidfile
import lockfile
import syslog

# Get the current user's home directory
HOME_DIR = os.path.expanduser('~')
BASE_DIR = os.path.join(HOME_DIR, '.directory_monitor')
MONITOR_DIR = os.path.join(BASE_DIR, 'monitored')
PID_FILE = os.path.join(BASE_DIR, 'directory_monitor.pid')

# Create necessary directories
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(MONITOR_DIR, exist_ok=True)

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        syslog.openlog("directory-monitor", syslog.LOG_PID)
        
    def on_created(self, event):
        if not event.is_directory:
            syslog.syslog(syslog.LOG_INFO, f"File created: {os.path.basename(event.src_path)}")
            
    def on_modified(self, event):
        if not event.is_directory:
            syslog.syslog(syslog.LOG_INFO, f"File modified: {os.path.basename(event.src_path)}")
            
    def on_deleted(self, event):
        if not event.is_directory:
            syslog.syslog(syslog.LOG_INFO, f"File deleted: {os.path.basename(event.src_path)}")
            
    def on_moved(self, event):
        if not event.is_directory:
            syslog.syslog(syslog.LOG_INFO, f"File renamed: {os.path.basename(event.src_path)} to {os.path.basename(event.dest_path)}")

def monitor_directory():
    if not os.path.exists(MONITOR_DIR):
        syslog.syslog(syslog.LOG_ERR, f"Monitor directory {MONITOR_DIR} does not exist!")
        sys.exit(1)
    
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITOR_DIR, recursive=False)
    
    try:
        syslog.syslog(syslog.LOG_INFO, f"Starting directory monitor for: {MONITOR_DIR}")
        observer.start()
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
        syslog.syslog(syslog.LOG_INFO, "Monitor stopped by user")
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Error in monitor_directory: {str(e)}")
        observer.stop()
        raise
    finally:
        observer.join()

def run_daemon():
    context = daemon.DaemonContext(
        working_directory=MONITOR_DIR,
        umask=0o002,
        pidfile=daemon.pidfile.PIDLockFile(PID_FILE),
        detach_process=True
    )
    
    with context:
        monitor_directory()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} [start|stop|status]".format(sys.argv[0]))
        sys.exit(1)

    command = sys.argv[1].lower()
    syslog.openlog("directory-monitor", syslog.LOG_PID)
    
    if command == "start":
        try:
            syslog.syslog(syslog.LOG_INFO, "Starting directory monitor daemon")
            run_daemon()
        except lockfile.AlreadyLocked:
            print("Daemon is already running")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting daemon: {str(e)}")
            syslog.syslog(syslog.LOG_ERR, f"Error starting daemon: {str(e)}")
            sys.exit(1)
            
    elif command == "stop":
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            os.remove(PID_FILE)
            syslog.syslog(syslog.LOG_INFO, "Daemon stopped")
            print("Daemon stopped")
        except FileNotFoundError:
            print("Daemon not running (PID file not found)")
            sys.exit(1)
        except ProcessLookupError:
            print("Daemon not running (process not found)")
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
            sys.exit(1)
        except Exception as e:
            print(f"Error stopping daemon: {str(e)}")
            syslog.syslog(syslog.LOG_ERR, f"Error stopping daemon: {str(e)}")
            sys.exit(1)
            
    elif command == "status":
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read())
            # Check if process is running
            os.kill(pid, 0)
            print(f"Daemon is running with PID {pid}")
            print("\nLast log entries:")
            os.system("sudo grep 'directory-monitor' /var/log/messages | tail -n 5")
        except FileNotFoundError:
            print("Daemon not running (PID file not found)")
        except ProcessLookupError:
            print("Daemon not running (process not found)")
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
        except Exception as e:
            print(f"Error checking daemon status: {str(e)}")
    else:
        print("Unknown command. Use 'start', 'stop', or 'status'")
        sys.exit(1)