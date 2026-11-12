import hashlib
import json
from datetime import datetime
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
watched_folder = project_folder / "sample_data" / "monitored_files"
baseline_file = project_folder / "sample_data" / "baseline.json"
reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)
alerts_file = reports_folder / "alerts.log"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for block in iter(lambda: file.read(4096), b""):
            sha256.update(block)

    return sha256.hexdigest()


def get_current_files():
    current_files = {}

    for file_path in watched_folder.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(watched_folder))
            current_files[relative_path] = calculate_hash(file_path)

    return current_files


def send_alert(severity, message):
    entry = (
        f"[{datetime.now().isoformat(timespec='seconds')}] "
        f"[{severity}] {message}"
    )

    print(entry)

    with open(alerts_file, "a", encoding="utf-8") as file:
        file.write(entry + "\n")


def create_baseline():
    current_files = get_current_files()
    baseline_file.write_text(json.dumps(current_files, indent=4))
    print(f"Baseline created for {len(current_files)} file(s).")


def check_changes():
    if not baseline_file.exists():
        print("No baseline found. Choose option 1 first.")
        return

    baseline = json.loads(baseline_file.read_text())
    current_files = get_current_files()

    added = current_files.keys() - baseline.keys()
    deleted = baseline.keys() - current_files.keys()
    modified = [
        name
        for name in current_files.keys() & baseline.keys()
        if current_files[name] != baseline[name]
    ]

    if not added and not deleted and not modified:
        print("No changes detected.")
        return

    for name in sorted(added):
        send_alert("MEDIUM", f"New file detected: {name}")

    for name in sorted(modified):
        send_alert("HIGH", f"File modified: {name}")

    for name in sorted(deleted):
        send_alert("HIGH", f"File deleted: {name}")


if __name__ == "__main__":
    print("1. Create or update baseline")
    print("2. Check for file changes")

    choice = input("Choose 1 or 2: ")

    if choice == "1":
        create_baseline()
    elif choice == "2":
        check_changes()
    else:
        print("Please choose 1 or 2.")