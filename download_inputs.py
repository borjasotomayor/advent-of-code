#!/usr/bin/env python3
"""
Download Advent of Code puzzle inputs using the advent-of-code-data library.
Run from the root of the repository.

Requires an AoC session token — provide it in one of two ways:
  - Set the AOC_SESSION environment variable, or
  - Run `aocd --configure` to save it persistently to ~/.config/aocd/token
"""

import re
import sys
import time
from pathlib import Path

import aocd

DELAY_SECONDS = 1.5


def main():
    repo_root = Path(__file__).parent
    downloaded = 0
    skipped = 0
    errors = 0

    for year_dir in sorted(repo_root.glob("20[0-9][0-9]")):
        year = int(year_dir.name)

        for day_file in sorted(year_dir.glob("day[0-9][0-9].py")):
            day = int(re.search(r"day(\d+)", day_file.name).group(1))
            input_file = year_dir / "input" / f"{day:02d}.in"

            if input_file.exists():
                skipped += 1
                continue

            print(f"Downloading {year} day {day:02d}...", end=" ", flush=True)
            try:
                data = aocd.get_data(year=year, day=day)
                input_file.parent.mkdir(parents=True, exist_ok=True)
                input_file.write_text(data)
                print("done")
                downloaded += 1
                time.sleep(DELAY_SECONDS)
            except Exception as e:
                print(f"error: {e}", file=sys.stderr)
                errors += 1

    print(f"\nDownloaded: {downloaded}  Skipped (already present): {skipped}  Errors: {errors}")


if __name__ == "__main__":
    main()
