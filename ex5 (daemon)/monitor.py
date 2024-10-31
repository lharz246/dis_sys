#!/usr/bin/env python3
import sys
import time
import logging
import os
import signal
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import daemon
import daemon.pidfile
import lockfile

#create necessary directories
HOME_DIR = os.path.expanduser('~')
BASE_DIR = os.path.join(HOME_DIR, '.directory_monitor')
MONITOR_DIR = os.path.join(BASE_DIR, 'monitored')
PID_FILE = os.path.join(BASE_DIR, 'directory_monitor.pid')
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(MONITOR_DIR, exist_ok=True)

# logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  
    ]
)

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_moved_src = None
        self.last_moved_time = None

    #various actions to be monitored
    def on_created(self, event):
        if not event.is_directory:
            print(f"\n💫 New file created: {os.path.basename(event.src_path)}")
            
    def on_modified(self, event):
        if not event.is_directory:
            print(f"\n📝 File modified: {os.path.basename(event.src_path)}")
            
    def on_deleted(self, event):
        if not event.is_directory:
            print(f"\n🗑️  File deleted: {os.path.basename(event.src_path)}")

    def on_moved(self, event):
        if not event.is_directory:
            old_name = os.path.basename(event.src_path)
            new_name = os.path.basename(event.dest_path)
            print(f"\n🔄 File renamed: {old_name} ➜ {new_name}")

def monitor_directory():
    if not os.path.exists(MONITOR_DIR):
        print(f"Monitor directory {MONITOR_DIR} does not exist!")
        sys.exit(1)
    
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITOR_DIR, recursive=False)
    
    try:
        print(f"\n🔍 Monitoring directory: {MONITOR_DIR}")
        print("Events that will be monitored:")
        print("  💫 File creation")
        print("  📝 File modification")
        print("  🗑️  File deletion")
        print("  🔄 File renaming")
        print("\nWaiting for file events... (Press Ctrl+C to stop)\n")
        observer.start()
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Monitoring stopped")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        observer.stop()
        raise
    
    observer.join()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} [start|stop|status]".format(sys.argv[0]))
        sys.exit(1)

    command = sys.argv[1].lower()
    
    if command == "start":
        try:
            print("Starting file monitor...")
            monitor_directory()
        except Exception as e:
            print(f"Error starting monitor: {str(e)}")
            sys.exit(1)
            
    elif command == "stop":
        print("To stop monitoring, press Ctrl+C")
        
    else:
        print("Usage: python3 monitor.py start")
        sys.exit(1)