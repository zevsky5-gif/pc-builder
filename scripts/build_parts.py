import json
import os
import sys
from pathlib import Path

OPEN_DB_DIR = Path(r"E:\buildcores-open-db\open-db")
INPUT_FILE = Path("data/selected_parts.json")
OUTPUT_FILE = Path("data/parts.json")


def main():
    if not INPUT_FILE.exists():
        print(f"Error: Input file not found at '{INPUT_FILE}'", file=sys.stderr)
        sys.exit(1)

    if not OPEN_DB_DIR.exists():
        print(f"Error: OpenDB directory not found at '{OPEN_DB_DIR}'", file=sys.stderr)
        sys.exit(1)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        selected_parts = json.load(f)

    grouped_parts = {}
    unmatched = {}

    for part_type, names in selected_parts.items():
        grouped_parts[part_type] = []
        folder = OPEN_DB_DIR / part_type

        if not folder.is_dir():
            print(f"Warning: Directory not found for part type '{part_type}' at '{folder}'")
            unmatched[part_type] = list(names)
            continue

        # Index all JSON files in the category folder by metadata.name (read-only)
        name_to_content = {}
        for file_path in folder.glob("*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                name = data.get("metadata", {}).get("name")
                if name:
                    name_to_content[name] = data
                    # Also keep stripped fallback if needed
                    stripped = name.strip()
                    if stripped not in name_to_content:
                        name_to_content[stripped] = data
            except (json.JSONDecodeError, OSError):
                continue

        missing = []
        for name in names:
            if name in name_to_content:
                grouped_parts[part_type].append(name_to_content[name])
            elif name.strip() in name_to_content:
                grouped_parts[part_type].append(name_to_content[name.strip()])
            else:
                missing.append(name)

        if missing:
            unmatched[part_type] = missing

    # Write results to data/parts.json
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(grouped_parts, f, indent=2, ensure_ascii=False)

    print(f"Successfully wrote matching parts to '{OUTPUT_FILE}'.")

    # Report unmatched names
    total_unmatched = sum(len(items) for items in unmatched.values())
    if total_unmatched > 0:
        print("\nCould not match the following part names:")
        for part_type, missing_list in unmatched.items():
            print(f"\n[{part_type}] ({len(missing_list)} unmatched):")
            for name in missing_list:
                print(f"  - {name}")
    else:
        print("All part names were successfully matched.")


if __name__ == "__main__":
    main()