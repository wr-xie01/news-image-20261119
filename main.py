#!/usr/bin/env python3
"""make.fun entry point: place the pre-rendered image in the output dir.

The image is entry.png beside this file, drawn by generate_image.py
(a newspaper front page summing up Thursday 19 November 2026).
The grader runs this with no network; all it does is copy the file.

Local check (stands in for /output):

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
LIMIT = 1048576  # 1 MiB: the bounty caps the image at this size


def run():
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    source = BASE / "entry.png"
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    size = target.stat().st_size
    if size > LIMIT:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB limit")
    print(f"wrote entry.png ({size} bytes)")


if __name__ == "__main__":
    run()
