#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime, timedelta

# Get the current user's home directory
HOME_DIR = os.path.expanduser('~')

# Configure paths using local directories
BASE_DIR = os.path.join(HOME_DIR, '.directory_monitor')
MONITOR_DIR = os.path.join(BASE_DIR, 'monitored')
LOG_FILE = os.path.join(BASE_DIR, 'directory_monitor.log')

def setup_directories():
    """Set up all necessary directories with appropriate permissions"""
    try:
        # Create base and monitor directories
        os.makedirs(BASE_DIR, exist_ok=True)
        os.makedirs(MONITOR_DIR, exist_ok=True)
        
        print(f"Successfully set up directories:")
        print(f"Base directory: {BASE_DIR}")
        print(f"Monitor directory: {MONITOR_DIR}")
        print(f"Log file will be created at: {LOG_FILE}")
        
        return MONITOR_DIR

    except Exception as e:
        print(f"Error during setup: {str(e)}")
        sys.exit(1)

def create_test_file(directory, day_offset=0):
    """Create a test file in the specified directory"""
    timestamp = datetime.now() + timedelta(days=day_offset)
    filename = f"test_file_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as f:
        f.write(f"Test file created at {timestamp}")
    
    print(f"Created test file: {filename}")
    return filepath

def verify_daemon_logs():
    """Verify that the daemon is logging properly"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                last_lines = f.readlines()[-10:]  # Get last 10 lines
                print("\nLast 10 log entries:")
                for line in last_lines:
                    print(line.strip())
        else:
            print(f"Log file not found at {LOG_FILE}")
    except Exception as e:
        print(f"Error reading log file: {str(e)}")

def run_test():
    """Run the test sequence"""
    try:
        # Setup directories
        monitor_dir = setup_directories()
        
        print("\nStarting test sequence...")
        print("Creating test files for today...")
        today_files = []
        for i in range(3):
            filepath = create_test_file(monitor_dir)
            today_files.append(filepath)
            time.sleep(2)
        
        print("\nCreating test files for tomorrow (simulated)...")
        tomorrow_files = []
        for i in range(3):
            filepath = create_test_file(monitor_dir, day_offset=1)
            tomorrow_files.append(filepath)
            time.sleep(2)
        
        # Verify file creation
        print("\nVerifying created files:")
        all_files = today_files + tomorrow_files
        for filepath in all_files:
            if os.path.exists(filepath):
                print(f"✓ {os.path.basename(filepath)} exists")
            else:
                print(f"✗ {os.path.basename(filepath)} missing")
        
        # Check daemon logs
        print("\nChecking daemon logs...")
        verify_daemon_logs()
        
    except Exception as e:
        print(f"Test error: {str(e)}")
        sys.exit(1)

def cleanup_test_files():
    """Clean up test files"""
    try:
        if os.path.exists(MONITOR_DIR):
            for file in os.listdir(MONITOR_DIR):
                if file.startswith("test_file_"):
                    os.remove(os.path.join(MONITOR_DIR, file))
            print("\nTest files cleaned up successfully")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
    else:
        action = "run"
    
    if action == "run":
        run_test()
    elif action == "cleanup":
        cleanup_test_files()
    elif action == "setup":
        setup_directories()
    else:
        print("Usage: python3 test_daemon.py [run|cleanup|setup]")
        sys.exit(1)