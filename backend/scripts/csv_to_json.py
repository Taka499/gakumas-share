#!/usr/bin/env python3
"""Convert CSV files to JSON format."""

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List


def convert_value(value: str) -> Any:
    """Convert string values to appropriate Python types."""
    # Handle boolean values
    if value.upper() == "TRUE":
        return True
    elif value.upper() == "FALSE":
        return False

    # Handle empty strings
    if value == "":
        return None

    # Try to convert to integer
    try:
        return int(value)
    except ValueError:
        pass

    # Try to convert to float
    try:
        return float(value)
    except ValueError:
        pass

    # Return as string if no conversion is possible
    return value


def csv_to_json(csv_path: Path, json_path: Path) -> bool:
    """Convert a single CSV file to JSON."""
    try:
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            data = []

            for row in reader:
                # Convert values to appropriate types
                converted_row = {
                    key: convert_value(value) for key, value in row.items()
                }
                data.append(converted_row)

        # Write JSON file
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, separators=(',', ':'))

        return True
    except Exception as e:
        print(f"❌ Error converting {csv_path.name}: {e}")
        return False


def main():
    """Convert all CSV files to JSON."""
    # Get directories
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    csv_dir = project_root / "data" / "csv"
    json_dir = project_root / "data" / "json"

    # Create JSON directory if it doesn't exist
    json_dir.mkdir(parents=True, exist_ok=True)

    # List of data types to process
    data_types = [
        "idols",
        "p_idols",
        "p_items",
        "skill_cards",
        "stages",
        "customizations"
    ]

    print(f"Converting CSV files from: {csv_dir}")
    print(f"Output JSON files to: {json_dir}")
    print("=" * 50)

    success_count = 0

    for data_type in data_types:
        csv_path = csv_dir / f"{data_type}.csv"
        json_path = json_dir / f"{data_type}.json"

        if not csv_path.exists():
            print(f"⚠️  Skipping {data_type}: CSV file not found")
            continue

        print(f"Converting {data_type}.csv to {data_type}.json...")

        if csv_to_json(csv_path, json_path):
            print(f"✅ Converted {data_type}")
            success_count += 1

    print("=" * 50)
    print(f"Conversion complete: {success_count} files processed successfully")


if __name__ == "__main__":
    main()