#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import syslog

# Get the current user's home directory
HOME_DIR = os.path.expanduser('~')
MONITOR_DIR = os.path.join(HOME_DIR, '.directory_monitor/monitored')

def create_test_files():
    """Create test files with current timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        # Create test files
        filename1 = f"test_file1_{timestamp}.txt"
        filename2 = f"test_file2_{timestamp}.txt"
        
        with open(os.path.join(MONITOR_DIR, filename1), 'w') as f:
            f.write(f"Test file 1 created at {datetime.now()}")
            
        with open(os.path.join(MONITOR_DIR, filename2), 'w') as f:
            f.write(f"Test file 2 created at {datetime.now()}")
            
        # Log to syslog
        syslog.openlog("directory-monitor-test")
        syslog.syslog(syslog.LOG_INFO, f"Created test files: {filename1}, {filename2}")
        
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Error creating test files: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    create_test_files()