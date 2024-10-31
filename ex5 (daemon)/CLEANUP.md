# Cleanup Instructions

Instructions for cleaning up the system after using the Directory Monitor Daemon.

## 🧹 Cleanup Steps

### 1. Stop the Daemon
```bash
# Stop the daemon if it's running
./directory_monitor_daemon.py stop

# Verify it's stopped
./directory_monitor_daemon.py status
```

### 2. Remove Cron Jobs
```bash
# Open crontab
crontab -e

# Remove or comment out the lines containing:
# /path/to/test_monitor.py
```

### 3. Remove Generated Files
```bash
# Remove the .directory_monitor folder and its contents
rm -rf ~/.directory_monitor
```

### 4. Uninstall RSyslog
```bash
# For Fedora/Nobara/RHEL
sudo systemctl stop rsyslog
sudo systemctl disable rsyslog
sudo dnf remove rsyslog

# For Debian/Ubuntu
sudo systemctl stop rsyslog
sudo systemctl disable rsyslog
sudo apt remove rsyslog
```

### 5. Remove Python Dependencies
```bash
pip uninstall python-daemon watchdog
```

### 6. Clean up Log Files
```bash
# Note: Only do this if you're sure you don't need these logs
sudo rm -f /var/log/messages
```

## ✔️ Verification

### 1. Verify RSyslog is Removed
```bash
systemctl status rsyslog
# Should show "not found" or similar
```

### 2. Verify Cron Jobs
```bash
crontab -l
# Should not show any test_monitor.py entries
```

### 3. Check for Remaining Files
```bash
ls ~/.directory_monitor
# Should show "No such file or directory"
```

## ⚠️ Important Notes

- Make sure to backup any important logs before removing them
- If you're using rsyslog for other purposes, you might want to keep it installed
- Some system services might depend on rsyslog; check carefully before removal
- If you want to keep rsyslog but remove only our daemon's logs:
  ```bash
  sudo grep -v "directory-monitor" /var/log/messages > /tmp/messages.tmp
  sudo mv /tmp/messages.tmp /var/log/messages
  ```

## 💡 Restoring Default System Logging

If you need system logging functionality, your system will likely fall back to using `journald`, which is the default on many modern Linux distributions.

To verify system logging is still working:
```bash
# Check journald status
systemctl status systemd-journald

# View system logs using journalctl
journalctl -f
```

## 🔄 Restoring Original Cron Configuration

If you modified any existing cron jobs, make sure to restore them to their original state:

1. If you backed up your crontab:
```bash
# Restore from backup if you made one
crontab crontab_backup
```

2. If you didn't back up, just remove the test entries:
```bash
crontab -e
# Manually remove any lines related to test_monitor.py
```

3. Verify your cron configuration:
```bash
crontab -l
```