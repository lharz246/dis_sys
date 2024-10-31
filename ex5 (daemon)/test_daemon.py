#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timedelta
import syslog

# Get the current user's home directory
HOME_DIR = os.path.expanduser('~')
BASE_DIR = os.path.join(HOME_DIR, '.directory_monitor')
MONITOR_DIR = os.path.join(BASE_DIR, 'monitored')

def create_test_file(day_offset=0):
    """Create a test file with a specific date offset"""
    timestamp = datetime.now() + timedelta(days=day_offset)
    filename = f"test_file_{timestamp.strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(MONITOR_DIR, filename)
    
    try:
        with open(filepath, 'w') as f:
            f.write(f"Test file created at {timestamp}")
        
        syslog.syslog(syslog.LOG_INFO, f"Test script created file: {filename}")
        return filepath
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Error creating test file: {str(e)}")
        return None

def run_test():
    """Run the test sequence"""
    syslog.openlog('directory-monitor-test', syslog.LOG_PID, syslog.LOG_DAEMON)
    
    try:
        # Create today's test files
        syslog.syslog(syslog.LOG_INFO, "Creating test files for today")
        for i in range(3):
            create_test_file()
        
        # Create tomorrow's test files (simulated)
        syslog.syslog(syslog.LOG_INFO, "Creating test files for tomorrow (simulated)")
        for i in range(3):
            create_test_file(day_offset=1)
            
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Error during test: {str(e)}")
    finally:
        syslog.closelog()

def cleanup_old_files():
    """Clean up test files older than 2 days"""
    try:
        for file in os.listdir(MONITOR_DIR):
            if file.startswith("test_file_"):
                filepath = os.path.join(MONITOR_DIR, file)
                file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                if datetime.now() - file_time > timedelta(days=2):
                    os.remove(filepath)
                    syslog.syslog(syslog.LOG_INFO, f"Cleaned up old test file: {file}")
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        command = "run"
    
    if command == "run":
        run_test()
    elif command == "cleanup":
        cleanup_old_files()
    else:
        print("Usage: python3 test_daemon.py [run|cleanup]")
        sys.exit(1)