# Directory Monitor Daemon

A Python daemon that monitors a specified directory for new files and logs when files are added. This project demonstrates the implementation of a Linux daemon process using Python.

## Features

- Monitors a directory for new file additions
- Runs as a background daemon process
- Logs file creation events with timestamps
- Includes test suite for verification
- User-friendly command-line interface
- No root permissions required

## Prerequisites

1. Python 3.x
2. Required Python packages:
   ```bash
   pip3 install python-daemon watchdog
   ```

## Project Structure

```
.
├── directory_monitor_daemon.py  # Main daemon script
├── test_daemon.py              # Test suite
└── README.md                   # This file
```

The daemon creates the following directory structure in your home folder:
```
~/.directory_monitor/
├── monitored/          # Directory being monitored
├── directory_monitor.log   # Log file
└── directory_monitor.pid   # PID file
```

## Installation

1. Clone or download the repository:
   ```bash
   git clone <repository-url>
   cd directory-monitor-daemon
   ```

2. Make the scripts executable:
   ```bash
   chmod +x directory_monitor_daemon.py
   chmod +x test_daemon.py
   ```

3. Install required packages:
   ```bash
   pip3 install python-daemon watchdog
   ```

## Usage

### Initial Setup

Before running the daemon for the first time, set up the required directories:

```bash
python3 test_daemon.py setup
```

### Starting the Daemon

To start the daemon:

```bash
python3 directory_monitor_daemon.py start
```

The daemon will create necessary directories if they don't exist and start monitoring the specified directory.

### Checking Daemon Status

To check if the daemon is running and view recent log entries:

```bash
python3 directory_monitor_daemon.py status
```

### Stopping the Daemon

To stop the daemon:

```bash
python3 directory_monitor_daemon.py stop
```

### Running Tests

To run the test suite (creates test files and verifies monitoring):

```bash
python3 test_daemon.py run
```

### Cleaning Up Test Files

To remove test files created during testing:

```bash
python3 test_daemon.py cleanup
```

## File Locations

- Monitored Directory: `~/.directory_monitor/monitored/`
- Log File: `~/.directory_monitor/directory_monitor.log`
- PID File: `~/.directory_monitor/directory_monitor.pid`

## Log Format

The daemon logs events in the following format:

```
YYYY-MM-DD HH:MM:SS - New file detected: /path/to/file at YYYY-MM-DD HH:MM:SS
```

## Testing with Cron

To automatically test the daemon at specific times using cron:

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add a line to run tests at specific times (e.g., every day at 9 AM and 5 PM):
   ```cron
   0 9,17 * * * /full/path/to/test_daemon.py run
   ```

## Troubleshooting

1. **Daemon won't start**
   - Check if it's already running: `python3 directory_monitor_daemon.py status`
   - Verify permissions: `ls -la ~/.directory_monitor`
   - Check the log file for errors

2. **Permission errors**
   - Ensure your user has write permissions to the `.directory_monitor` directory
   - Run `python3 test_daemon.py setup` to reset directory permissions

3. **Missing log entries**
   - Verify the daemon is running: `python3 directory_monitor_daemon.py status`
   - Check the log file location: `~/.directory_monitor/directory_monitor.log`

4. **PID file exists but daemon not running**
   - Stop the daemon: `python3 directory_monitor_daemon.py stop`
   - If stop fails, manually remove the PID file:
     ```bash
     rm ~/.directory_monitor/directory_monitor.pid
     ```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Python-daemon library
- Watchdog library for file system events
