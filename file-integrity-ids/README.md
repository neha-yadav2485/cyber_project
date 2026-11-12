# File Integrity Monitor and Log Analyzer

A Python host-based intrusion detection project that checks selected files for changes and analyzes sample login logs for suspicious activity.

## Features

- Creates a baseline using SHA-256 file fingerprints.
- Reports files that were added, modified, or deleted.
- Counts failed login attempts by IP address and username.
- Alerts when one IP has five or more failed logins within two minutes.
- Flags failed login attempts between 10:00 PM and 6:00 AM.
- Detects sample log records showing a new user added to an administrator group.
- Saves timestamped alerts with severity in `reports/alerts.log`.
- Simulates a response to repeated login failures. It does not block traffic.
- Shows alert totals and recent alerts in a local Streamlit dashboard.

## Project structure

```text
cyber_project/
├── reports/
│   ├── images/
│   └── alerts.log
├── sample_data/
│   ├── monitored_files/
│   │   ├── notes.txt
│   │   ├── settings.json
│   │   └── users.csv
│   ├── auth.log
│   ├── auth_attack_backup.log
│   └── baseline.json
├── src/
│   ├── dashboard.py
│   ├── dashboard_app.py
│   ├── integrity.py
│   ├── log_parser.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Requirements and setup

- Python
- Visual Studio Code or another code editor

Install the required packages from the main project folder:

```powershell
python -m pip install -r requirements.txt
```

## Run the command-line menu

From the main project folder, run:

```powershell
python src/main.py
```

The menu lets you check monitored files, analyze the sample login log, or view the command-line dashboard.

## Run the Streamlit dashboard

From the main project folder, run:

```powershell
python -m streamlit run src/dashboard_app.py --server.address 127.0.0.1
```

The dashboard opens in your browser. Keep the terminal open while using it. Press `Ctrl+C` in the terminal to stop it.

The Streamlit dashboard reads alert records from `reports/alerts.log`. It displays alerts already saved by the project; it does not monitor files by itself.

## Create or reset the file baseline

In the command-line menu, choose **1**. In the file monitor menu, choose **1** to create or update the baseline.

Choose **2** in the file monitor menu to compare the current files with the saved baseline. Changes to files inside `sample_data/monitored_files/` should be reported.

Reset the baseline only when you want the current files to become the new reference.

## Test the login log analyzer

The sample `sample_data/auth.log` contains example records for repeated failed logins, an unusual-hour attempt, and a new administrator account. Choose **2** in the command-line menu to analyze them.

To check a normal case, temporarily replace the contents of `auth.log` with two ordinary-hour failed login records. The program should count them without triggering the repeated-login or unusual-hour alerts.

The original attack sample is saved as `sample_data/auth_attack_backup.log`. Restore it to `sample_data/auth.log` after the normal-case check.

## Alerts and screenshots

Alerts appear in the terminal and are appended to:

```text
reports/alerts.log
```

Save project screenshots in `reports/images/`. Keep screenshots outside `sample_data/monitored_files/`, which is the folder used for file-change monitoring.

The prevention message is a simulation. The program does not run a firewall command or block an IP address.

## Limitations

- The log parser is designed for the sample Linux-style SSH log format used in this project.
- The sample log is simulated data; this Windows demo does not read live Linux authentication logs.
- The unusual-hour rule is a simple example and may need adjustment for a real environment.
- A file change can be detected only after a baseline has been created.
- The Streamlit dashboard runs locally and displays the alerts currently saved in `reports/alerts.log`.

## Ethical use

Use this project with your own files and sample logs, or systems for which you have permission. Do not monitor another person's device or logs without permission.

## References

- Python standard-library modules used: `hashlib`, `json`, `pathlib`, `re`, `collections`, `datetime`, and `subprocess`