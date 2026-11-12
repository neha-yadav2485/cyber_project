import subprocess
import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
integrity_script = project_folder / "src" / "integrity.py"
log_parser_script = project_folder / "src" / "log_parser.py"
dashboard_script = project_folder / "src" / "dashboard.py"


def show_menu():
    while True:
        print("\nFILE INTEGRITY MONITOR AND LOG ANALYZER")
        print("1. Check monitored files")
        print("2. Analyze sample login logs")
        print("3. View daily alert dashboard")
        print("4. Exit")

        choice = input("Choose 1, 2, 3, or 4: ")

        if choice == "1":
            subprocess.run(
                [sys.executable, str(integrity_script)],
                cwd=project_folder
            )
        elif choice == "2":
            subprocess.run(
                [sys.executable, str(log_parser_script)],
                cwd=project_folder
            )
        elif choice == "3":
            subprocess.run(
                [sys.executable, str(dashboard_script)],
                cwd=project_folder
            )
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    show_menu()