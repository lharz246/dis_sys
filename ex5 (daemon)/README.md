
## 📋 Prerequisites

1. Python 3.x
2. Python dependencies:
```bash
pip install python-daemon watchdog
```

3. rsyslog (usually pre-installed on Linux systems):
```bash

4. Start rsyslog if it's not already running:
```bash
sudo systemctl start rsyslog
sudo systemctl enable rsyslog  # To start at boot
```

## 🚀 Installation

1. Clone or copy the files to your system:
   - `directory_monitor_daemon.py` (main daemon)
   - `test_monitor.py` (test script)

2. Make the scripts executable:
```bash
chmod +x directory_monitor_daemon.py test_monitor.py
```

## 🔧 Directory Structure

The daemon automatically creates this structure:
```
~/.directory_monitor/
├── monitored/     # Monitored directory
└── directory_monitor.pid  # Daemon PID file
```

## 📖 Using the Daemon

### Starting the Daemon
```bash
./directory_monitor_daemon.py start
```

### Checking Status
```bash
./directory_monitor_daemon.py status
```

### Stopping the Daemon
```bash
./directory_monitor_daemon.py stop
```

## 🧪 Testing the Daemon

### Manual Testing
1. Start the daemon:
```bash
./directory_monitor_daemon.py start
```

2. In another terminal, monitor the logs:
```bash
sudo tail -f /var/log/messages | grep "directory-monitor"
```

3. Create some test files:
```bash
touch ~/.directory_monitor/monitored/test1.txt
echo "Hello" > ~/.directory_monitor/monitored/test2.txt
mv ~/.directory_monitor/monitored/test1.txt ~/.directory_monitor/monitored/test1_renamed.txt
rm ~/.directory_monitor/monitored/test2.txt
```

### Automated Testing
1. Run the test script:
```bash
./test_monitor.py
```

### Scheduled Testing with Cron
1. Open crontab:
```bash
crontab -e
```

2. Add these lines to run tests twice a day:
```cron
# Run test at 10:00 AM and 4:00 PM every day
0 10,16 * * * /full/path/to/test_monitor.py
```

## 📊 Viewing Logs

### View Recent Logs
```bash
sudo tail -n 10 /var/log/messages | grep "directory-monitor"
```

### Filter Logs by Date
```bash
# October 31st logs
sudo grep "Oct 31.*directory-monitor" /var/log/messages

# November 1st logs
sudo grep "Nov  1.*directory-monitor" /var/log/messages
```

### Follow Logs in Real-Time
```bash
sudo tail -f /var/log/messages | grep "directory-monitor"
```

### View All Daemon Logs
```bash
sudo grep "directory-monitor" /var/log/messages
```

## 📋 Monitored Events

The daemon logs the following events:
- 📝 File creation
- ✏️ File modification
- 🔄 File renaming
- 🗑️ File deletion

Each event is logged with:
- Timestamp
- Event type
- Filename
- Daemon process PID
