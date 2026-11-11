import json
from pathlib import Path

PART_TYPES = [
    "CPU",
    "CPUCooler",
    "Motherboard",
    "GPU",
    "RAM",
    "Storage",
    "PSU",
    "PCCase",
]

INPUT_PATH = Path("data/parts.json")
OUTPUT_PATH = Path("data/samples.json")


def make_samples():
    if not INPUT_PATH.exists():
        print(f"Error: {INPUT_PATH} does not exist.")
        return

    # Read parts.json in read-only mode to ensure it remains unchanged
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        parts_data = json.load(f)

    samples = {}
    found_types = []
    missing_types = []

    for part_type in PART_TYPES:
        entries = parts_data.get(part_type)

        # Check if the part type exists and has at least one entry
        if isinstance(entries, list) and len(entries) > 0:
            samples[part_type] = entries[0]
            found_types.append(part_type)
        elif entries is not None and not isinstance(entries, list):
            samples[part_type] = entries
            found_types.append(part_type)
        else:
            missing_types.append(part_type)

    # Ensure the output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write samples out with readable indentation
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(samples, f, indent=4)

    # Report found and missing types
    print("=== Part Types Report ===")
    print("Found:")
    if found_types:
        for pt in found_types:
            print(f"  [+] {pt}")
    else:
        print("  (none)")

    print("\nMissing:")
    if missing_types:
        for pt in missing_types:
            print(f"  [-] {pt}")
    else:
        print("  (none)")

    print(f"\nSamples successfully saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    make_samples()