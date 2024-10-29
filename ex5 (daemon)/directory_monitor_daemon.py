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

# Get the current user's home directory
HOME_DIR = os.path.expanduser('~')

# Configure paths using local directories
BASE_DIR = os.path.join(HOME_DIR, '.directory_monitor')
MONITOR_DIR = os.path.join(BASE_DIR, 'monitored')
LOG_FILE = os.path.join(BASE_DIR, 'directory_monitor.log')
PID_FILE = os.path.join(BASE_DIR, 'directory_monitor.pid')

# Create necessary directories
os.makedirs(BASE_DIR, exist_ok=True)
os.makedirs(MONITOR_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class FileEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logging.info(f"New file detected: {event.src_path} at {timestamp}")

def monitor_directory():
    # Verify the monitored directory exists
    if not os.path.exists(MONITOR_DIR):
        logging.error(f"Monitor directory {MONITOR_DIR} does not exist!")
        sys.exit(1)
    
    # Initialize the file system observer and event handler
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, MONITOR_DIR, recursive=False)
    
    try:
        logging.info(f"Starting directory monitor daemon for: {MONITOR_DIR}")
        observer.start()
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        observer.stop()
        logging.info("Directory monitor daemon stopped")
    except Exception as e:
        logging.error(f"Error in monitor_directory: {str(e)}")
        observer.stop()
        raise
    
    observer.join()

def run_daemon():
    # Context manager for daemonization
    context = daemon.DaemonContext(
        working_directory=MONITOR_DIR,
        umask=0o002,
        pidfile=daemon.pidfile.PIDLockFile(PID_FILE),
        detach_process=True
    )
    
    # Open the context and run the monitor
    with context:
        monitor_directory()

def verify_environment():
    """Verify that all necessary files and directories exist with correct permissions"""
    try:
        # Check monitor directory
        if not os.path.exists(MONITOR_DIR):
            print(f"Error: Monitor directory {MONITOR_DIR} does not exist!")
            return False
            
        # Verify write permissions
        if not os.access(MONITOR_DIR, os.W_OK):
            print(f"Error: No write permission for {MONITOR_DIR}")
            return False
        if not os.access(os.path.dirname(LOG_FILE), os.W_OK):
            print(f"Error: No write permission for {os.path.dirname(LOG_FILE)}")
            return False
        if not os.access(os.path.dirname(PID_FILE), os.W_OK):
            print(f"Error: No write permission for {os.path.dirname(PID_FILE)}")
            return False
            
        return True
    except Exception as e:
        print(f"Error during environment verification: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} [start|stop|status]".format(sys.argv[0]))
        sys.exit(1)

    command = sys.argv[1].lower()
    
    if command == "start":
        if not verify_environment():
            print("Environment verification failed. Please check directory permissions.")
            sys.exit(1)
        try:
            print(f"Starting daemon. Monitor directory: {MONITOR_DIR}")
            print(f"Log file: {LOG_FILE}")
            print(f"PID file: {PID_FILE}")
            run_daemon()
        except lockfile.AlreadyLocked:
            print("Daemon is already running")
            sys.exit(1)
        except Exception as e:
            print(f"Error starting daemon: {str(e)}")
            sys.exit(1)
    
    elif command == "stop":
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read())
            os.kill(pid, signal.SIGTERM)
            os.remove(PID_FILE)
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
            sys.exit(1)
    
    elif command == "status":
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read())
            # Check if process is running
            os.kill(pid, 0)  # This will raise an error if process is not running
            print(f"Daemon is running with PID {pid}")
            # Show last few log entries
            try:
                with open(LOG_FILE, 'r') as f:
                    last_lines = f.readlines()[-5:]
                print("\nLast 5 log entries:")
                for line in last_lines:
                    print(line.strip())
            except FileNotFoundError:
                print("Log file not found")
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