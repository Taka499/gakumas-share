#!/usr/bin/env python3
"""Download CSV files from the Gakumas Data Google Sheet."""

import sys
import requests
from pathlib import Path

# Google Sheet ID from the gakumas-tools repository
SHEET_ID = "19E3wGFhnmcK9jdP8dTIFo0_XUx1jCqYGvzzGAXQqaq4"

# Sheet names and their corresponding GIDs (sheet tab IDs)
SHEETS = {
    "idols": "44649913",
    "p_idols": "838844762",
    "p_items": "620279571",
    "skill_cards": "642288621",
    "stages": "1709146721",
    "customizations": "1994527852",
}


def get_csv_url(sheet_name: str, gid: str) -> str:
    """Generate CSV download URL for a specific sheet."""
    base_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export"
    return f"{base_url}?format=csv&gid={gid}"


def download_csv(sheet_name: str, gid: str, output_dir: Path) -> bool:
    """Download a single CSV file from the Google Sheet."""
    url = get_csv_url(sheet_name, gid)
    output_path = output_dir / f"{sheet_name}.csv"

    try:
        print(f"Downloading {sheet_name}.csv...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Check if response contains actual CSV data
        content = response.content.decode('utf-8')
        if content.strip().startswith('<') or 'html' in content.lower():
            print(f"❌ Received HTML instead of CSV for {sheet_name}")
            return False

        with open(output_path, "w", encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Downloaded {sheet_name}.csv")
        return True
    except requests.RequestException as e:
        print(f"❌ Failed to download {sheet_name}.csv: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error downloading {sheet_name}.csv: {e}")
        return False


def main():
    """Download all CSV files from the Google Sheet."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    csv_dir = project_root / "data" / "csv"

    # Create CSV directory if it doesn't exist
    csv_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading CSV files to: {csv_dir}")
    print("=" * 50)

    success_count = 0
    total_count = len(SHEETS)

    for sheet_name, gid in SHEETS.items():
        if download_csv(sheet_name, gid, csv_dir):
            success_count += 1

    print("=" * 50)
    print(
        f"Download complete: {success_count}/{total_count} files downloaded successfully"
    )

    if success_count < total_count:
        print(
            "Some downloads failed. Please check your internet connection and try again."
        )
        sys.exit(1)
    else:
        print("All files downloaded successfully!")


if __name__ == "__main__":
    main()
