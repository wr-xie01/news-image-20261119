#!/usr/bin/env python3
"""make.fun entry: copy the pre-rendered news image to the output dir.

The image is entry.png beside this file, drawn by generate_image.py
(a newspaper front page summing up Thursday 19 November 2026).
The grader runs this program with no network; it only copies the file.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT_DIR, "entry.png")
shutil.copyfile(src, dst)
# Gate limits for this bounty: a whole PNG or JPEG, at most 1 MiB and
# at most 1024 by 1024 pixels. Fail loudly here rather than shipping
# an entry the sealed scorer would reject.
size = os.path.getsize(dst)
assert size <= 1048576, f"entry.png is {size} bytes, over the 1 MiB limit"
print(f"wrote entry.png ({size} bytes)")
