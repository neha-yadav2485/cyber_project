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
- No extra Python packages required

## Project structure

```text
file-integrity-ids/
├── reports/
│   ├── images/
│   └── alerts.log
├── sample_data/
│   ├── monitored_files/
│   │   ├── notes.txt
│   │   ├── settings.json
│   │   └── users.csv
│   ├── auth_attack_backup.log
│   ├── auth.log
│   └── baseline.json
├── src/
│   ├── integrity.py
│   ├── log_parser.py
│   └── main.py
└── README.md
```

## Run the project

Open a terminal in the main `file-integrity-ids` folder and run:

```powershell
python src/main.py
```

Choose **1** to check monitored files or **2** to analyze the sample login log.

## Create or reset the file baseline

In the main menu, choose **1**. In the file monitor menu, choose **1** to create or update the baseline. This saves the current monitored files as the reference.

Choose **2** in the file monitor menu to compare files with the saved baseline. Changing, adding, or deleting a file inside `sample_data/monitored_files/` should create an alert.

Reset the baseline only when you want the current files to become the new reference.

## Test the login log analyzer

The sample `sample_data/auth.log` contains example records for repeated failed logins, an unusual-hour attempt, and a new administrator account. Choose **2** in the main menu to analyze these records.

To check a normal case, temporarily replace the contents of `auth.log` with two ordinary-hour failed login records. The program should count them without triggering the repeated-login or unusual-hour alerts.

The original attack sample is saved as `sample_data/auth_attack_backup.log`. Restore it to `sample_data/auth.log` after the normal-case check.

## Alerts and screenshots

Alerts appear in the terminal and are appended to `reports/alerts.log`.

Save project screenshots in `reports/images/`. Keep screenshots outside `sample_data/monitored_files/`, because that folder is used for file-change monitoring.

The prevention message is for demonstration only. The program does not block an IP address.

## Limitations

- The log parser is designed for the sample Linux-style SSH log format used in this project.
- The sample log is simulated data. This Windows demo does not read live Linux authentication logs.
- The unusual-hour rule is a simple example and may need adjustment for a real environment.
- A file change can be detected only after a baseline has been created.

## Ethical use

Use this project with your own files and sample logs, or systems for which you have permission. Do not monitor another person’s device or logs without permission.

## References

The project uses Python standard-library modules, including `hashlib`, `json`, `pathlib`, `re`, `collections`, `datetime`, and `subprocess`. No third-party code or packages are required.