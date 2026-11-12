import re
from collections import Counter, defaultdict
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
alerts_file = project_folder / "reports" / "alerts.log"

alert_pattern = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2})T[^\]]+\]\s+\[(\w+)\]"
)


def show_dashboard():
    if not alerts_file.exists():
        print("No alerts file found yet. Run a project feature first.")
        return

    daily_counts = defaultdict(Counter)

    with open(alerts_file, "r", encoding="utf-8") as file:
        for line in file:
            match = alert_pattern.search(line)

            if match:
                day = match.group(1)
                severity = match.group(2)
                daily_counts[day][severity] += 1

    if not daily_counts:
        print("No formatted alerts found in the alert file yet.")
        return

    print("\nDAILY ALERT DASHBOARD")

    for day in sorted(daily_counts):
        counts = daily_counts[day]
        total = sum(counts.values())
        severity_summary = ", ".join(
            f"{severity}: {count}"
            for severity, count in sorted(counts.items())
        )
        print(f"{day} | Total: {total} | {severity_summary}")


if __name__ == "__main__":
    show_dashboard()