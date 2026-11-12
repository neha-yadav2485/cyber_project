# File Integrity Monitor and Log Analyzer

A small Python host-based intrusion detection project. It checks selected files for changes and analyzes sample login logs for suspicious activity.

## Features

- Creates a baseline using SHA-256 file fingerprints.
- Reports files that were added, modified, or deleted.
- Counts failed login attempts by IP address and username.
- Alerts when one IP has five or more failed logins within two minutes.
- Flags failed login attempts between 10:00 PM and 6:00 AM.
- Detects sample log records showing a new user added to an administrator group.
- Saves alerts with severity and time in `reports/alerts.log`.
- Prints a prevention simulation. It does not run firewall commands or block traffic.

## Requirements

- Python installed
- Visual Studio Code or another code editor
- No extra Python packages are required

## Project folders

```text
file-integrity-ids/
├── src/
│   ├── main.py
│   ├── integrity.py
│   └── log_parser.py
├── sample_data/
│   ├── auth.log
│   ├── baseline.json
│   └── monitored_files/
├── reports/
│   └── alerts.log
└── README.md
```

## Run the project

Open a terminal in the main project folder and run:

```powershell
python src/main.py
```

Choose **1** to check monitored files or **2** to analyze the sample login log.

## Create or reset the file baseline

In the main menu, choose **1**, then choose **1** again in the file monitor menu. This saves the current files as the baseline.

Choose **2** in the file monitor menu to compare files with the saved baseline. Changing, adding, or deleting a monitored file should create an alert.

Reset the baseline only when you want the current files to become the new reference.

## Test the login log analyzer

The sample `auth.log` contains example records for repeated failed logins, an unusual-hour attempt, and a sample new administrator account. Choose **2** in the main menu to analyze them.

To check a normal case, temporarily replace the sample log with two ordinary-hour failed login records. The program should count them without triggering the repeated-login or unusual-hour alerts. Restore the original sample log after the check.

## Alert output

Alerts appear in the terminal and are appended to:

```text
reports/alerts.log
```

The prevention message is for demonstration only. The program does not block an IP address.

## Limitations

- The log parser is designed for the sample Linux-style SSH log format used in this project.
- The sample log is simulated data; this Windows demo does not read live Linux authentication logs.
- The unusual-hour rule is a simple example and may need to be adjusted for a real environment.
- A file change can be detected only after a baseline has been created.

## Ethical use

Use this project with your own files and sample logs, or systems for which you have permission. Do not use it to monitor someone else’s device or logs without permission.

## References

The project uses Python standard-library modules, including `hashlib`, `json`, `pathlib`, `re`, `collections`, `datetime`, and `subprocess`. No third-party code or packages are required.