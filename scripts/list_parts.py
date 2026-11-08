import json
import os
from pathlib import Path


def main():
    # Source directory (read-only)
    source_dir = Path(r"E:\buildcores-open-db\open-db")
    
    # Destination directory
    output_dir = Path("data/lists")

    if not source_dir.exists():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    # Ensure the destination folder exists without touching the source directory
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Scanning components in: {source_dir}\n")

    # Iterate through every folder inside open-db
    for folder in sorted(source_dir.iterdir()):
        if not folder.is_dir():
            continue

        part_names = []

        # Read every .json file inside this folder (read-only mode)
        for json_file in sorted(folder.glob("*.json")):
            try:
                with open(json_file, mode="r", encoding="utf-8") as f:
                    data = json.load(f)

                # Extract the name from the metadata field
                metadata = data.get("metadata", {})
                name = metadata.get("name")

                if name:
                    part_names.append(str(name).strip())
            except Exception as e:
                print(f"Warning: Failed to read {json_file.name}: {e}")

        # Destination file: data/lists/<folder_name>.txt
        output_file = output_dir / f"{folder.name}.txt"

        # Write part names (one per line) into the output file
        with open(output_file, mode="w", encoding="utf-8") as f:
            for name in part_names:
                f.write(f"{name}\n")

        # Print how many parts the folder has
        print(f"{folder.name}: {len(part_names)} parts -> {output_file}")

    print("\nDone! All lists have been generated in data/lists.")


if __name__ == "__main__":
    main()