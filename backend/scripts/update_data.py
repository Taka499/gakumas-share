#!/usr/bin/env python3
"""Main script to update game data from Google Sheet."""

import subprocess
import sys
from pathlib import Path


def run_script(script_name: str) -> bool:
    """Run a Python script and return success status."""
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name

    try:
        print(f"Running {script_name}...")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name} failed:")
        print(e.stdout)
        print(e.stderr)
        return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False


def main():
    """Update all game data."""
    print("🚀 Starting data update process...")
    print("=" * 50)

    # Step 1: Download CSV files
    if not run_script("download_csv.py"):
        print("Failed to download CSV files. Aborting.")
        sys.exit(1)

    print()

    # Step 2: Convert CSV to JSON
    if not run_script("csv_to_json.py"):
        print("Failed to convert CSV to JSON. Aborting.")
        sys.exit(1)

    print()
    print("🎉 Data update completed successfully!")
    print("The latest game data has been downloaded and processed.")


if __name__ == "__main__":
    main()