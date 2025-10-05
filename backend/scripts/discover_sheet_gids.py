#!/usr/bin/env python3
"""Discover Google Sheet GIDs (sheet tab IDs) for the Gakumas Data spreadsheet."""

import json
import sys
from urllib.request import urlopen
from urllib.error import URLError

# Google Sheet ID from the gakumas-tools repository
SHEET_ID = "19E3wGFhnmcK9jdP8dTIFo0_XUx1jCqYGvzzGAXQqaq4"

def discover_sheet_gids():
    """Discover all sheet names and their GIDs using Google Sheets API."""
    # Use the public Google Sheets API to get sheet metadata
    # This works for public sheets without authentication
    api_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=sheets.properties"

    try:
        print(f"Discovering sheet GIDs for spreadsheet: {SHEET_ID}")
        print("=" * 60)

        with urlopen(api_url) as response:
            data = json.loads(response.read().decode())

        sheets = data.get('sheets', [])
        if not sheets:
            print("No sheets found in the spreadsheet.")
            return {}

        sheet_mapping = {}
        for sheet in sheets:
            properties = sheet.get('properties', {})
            sheet_name = properties.get('title', 'Unknown')
            sheet_gid = properties.get('sheetId', 0)

            print(f"Sheet: '{sheet_name}' -> GID: {sheet_gid}")
            sheet_mapping[sheet_name.lower().replace(' ', '_')] = str(sheet_gid)

        print("=" * 60)
        print(f"Found {len(sheets)} sheets total")

        return sheet_mapping

    except URLError as e:
        print(f"❌ Failed to access Google Sheets API: {e}")
        print("Note: This might happen if the spreadsheet is not public.")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse API response: {e}")
        return {}
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return {}

def generate_download_script(sheet_mapping):
    """Generate the download script with discovered GIDs."""
    if not sheet_mapping:
        print("Cannot generate download script - no sheet GIDs discovered.")
        return

    print("\nGenerated SHEETS dictionary for download_csv.py:")
    print("=" * 60)
    print("SHEETS = {")
    for sheet_name, gid in sheet_mapping.items():
        print(f'    "{sheet_name}": "{gid}",')
    print("}")

def main():
    """Main function to discover sheet GIDs."""
    sheet_mapping = discover_sheet_gids()

    if sheet_mapping:
        generate_download_script(sheet_mapping)

        # Save to a JSON file for later use
        output_file = "sheet_gids.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sheet_mapping, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Sheet GIDs saved to: {output_file}")
    else:
        print("\n❌ Failed to discover sheet GIDs")
        sys.exit(1)

if __name__ == "__main__":
    main()