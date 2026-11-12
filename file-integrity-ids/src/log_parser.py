import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
log_file = project_folder / "sample_data" / "auth.log"
reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)
alerts_file = reports_folder / "alerts.log"

ip_counts = Counter()
user_counts = Counter()
ip_events = defaultdict(list)
unusual_events = []
new_users = set()
admin_group_users = set()
offending_ips = []

failed_login_pattern = re.compile(
    r"^(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}).*"
    r"Failed password for (?:invalid user )?(\S+) from ([\d.]+)"
)

new_user_pattern = re.compile(r"new user:\s*name=([\w.-]+)")

admin_group_pattern = re.compile(
    r"add ['\"]?([\w.-]+)['\"]? to group ['\"]?(sudo|wheel|administrators)",
    re.IGNORECASE
)


def send_alert(severity, message):
    entry = (
        f"[{datetime.now().isoformat(timespec='seconds')}] "
        f"[{severity}] {message}"
    )

    print(entry)

    with open(alerts_file, "a", encoding="utf-8") as file:
        file.write(entry + "\n")


with open(log_file, "r", encoding="utf-8") as file:
    for line in file:
        failed_match = failed_login_pattern.search(line)

        if failed_match:
            timestamp = datetime.strptime(
                f"2000 {failed_match.group(1)}",
                "%Y %b %d %H:%M:%S"
            )
            username = failed_match.group(2)
            ip_address = failed_match.group(3)

            ip_counts[ip_address] += 1
            user_counts[username] += 1
            ip_events[ip_address].append(timestamp)

            if timestamp.hour >= 22 or timestamp.hour < 6:
                unusual_events.append((timestamp, username, ip_address))

        new_user_match = new_user_pattern.search(line)
        if new_user_match:
            new_users.add(new_user_match.group(1))

        admin_match = admin_group_pattern.search(line)
        if admin_match:
            admin_group_users.add(admin_match.group(1))


print("Failed logins by IP:")
for ip_address, count in ip_counts.items():
    print(f"{ip_address}: {count}")

print("\nFailed logins by username:")
for username, count in user_counts.items():
    print(f"{username}: {count}")

print("\nSecurity alerts:")
alert_found = False

for ip_address, timestamps in ip_events.items():
    timestamps.sort()

    for start in range(len(timestamps)):
        end = start

        while (
            end < len(timestamps)
            and timestamps[end] - timestamps[start] <= timedelta(minutes=2)
        ):
            end += 1

        if end - start >= 5:
            send_alert(
                "HIGH",
                f"{ip_address} had 5 or more failed logins within 2 minutes."
            )
            offending_ips.append(ip_address)
            alert_found = True
            break

for timestamp, username, ip_address in unusual_events:
    send_alert(
        "MEDIUM",
        f"Failed login for {username} from {ip_address} at an unusual hour "
        f"({timestamp.strftime('%H:%M:%S')})."
    )
    alert_found = True

new_admin_users = new_users & admin_group_users

for username in sorted(new_admin_users):
    send_alert(
        "CRITICAL",
        f"New user '{username}' was added to an admin group."
    )
    alert_found = True

print("\nPrevention simulation:")

if offending_ips:
    for ip_address in sorted(set(offending_ips)):
        print(
            f"SIMULATION ONLY: would block {ip_address}. "
            "No firewall command was run."
        )
else:
    print("No IP met the blocking rule.")

if not alert_found:
    print("No security alerts.")