#!/usr/bin/env python3
"""Export markdown to DOCX through pandoc."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export markdown to DOCX with pandoc.")
    parser.add_argument("--input", required=True, help="Input markdown file")
    parser.add_argument("--output", required=True, help="Output .docx file path")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
    if input_path.suffix.lower() != ".md":
        raise SystemExit(f"Input must be a markdown file: {input_path}")
    if output_path.suffix.lower() != ".docx":
        raise SystemExit(f"Output must use .docx suffix: {output_path}")

    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise SystemExit(
            "pandoc is not installed. Install pandoc first, then rerun this command."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [pandoc, str(input_path), "-o", str(output_path)]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"pandoc export failed: {exc}") from exc

    print(f"Exported DOCX: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
