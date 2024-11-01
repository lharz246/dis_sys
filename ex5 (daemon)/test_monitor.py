import os
import sys
from datetime import datetime, timedelta
import syslog
import time

# Get the current user's home directory
HOME_DIR = os.path.expanduser('~')
MONITOR_DIR = os.path.join(HOME_DIR, '.directory_monitor/monitored')

def create_test_files(day_number=0):
    """Create test files with timestamp"""
    current_time = datetime.now() + timedelta(days=day_number)
    timestamp = current_time.strftime('%Y%m%d_%H%M%S')
    
    try:
        filename = f"test_file_day{day_number}_{timestamp}.txt"
        filepath = os.path.join(MONITOR_DIR, filename)
        
        with open(filepath, 'w') as f:
            f.write(f"Test file created for day {day_number} at {current_time}")
            

        time.sleep(1)
        with open(filepath, 'a') as f:
            f.write("\nModified the file")
            

        new_filename = f"renamed_day{day_number}_{timestamp}.txt"
        new_filepath = os.path.join(MONITOR_DIR, new_filename)
        os.rename(filepath, new_filepath)

        time.sleep(1)
        os.remove(new_filepath)
        
    
        syslog.openlog("directory-monitor-test")
        syslog.syslog(syslog.LOG_INFO, f"Completed test sequence for day {day_number}")
        
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, f"Error in test sequence: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Test for "today"
    create_test_files(0)
    
    # Wait a bit between tests
    time.sleep(2)
    
    # Test for "tomorrow"
    create_test_files(1)
    
    print("Test sequences completed. Check logs with:")
    print("sudo grep 'directory-monitor' /var/log/messages | sort")