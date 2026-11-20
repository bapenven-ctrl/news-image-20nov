#!/usr/bin/env python3
"""news-image-20261120 entry: "The World in One Page — Friday 20 November 2026".

The deliverable is entry.png, a one-page illustrated news sheet of Friday
20 November 2026 (49 stories, all dated that day). This entrypoint simply
copies the pre-rendered sheet into the directory named by MAKEFUN_OUTPUT_DIR
(or ./output). Standard library only.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    with open(SRC, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit(f"{SRC} is not a PNG file")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(HERE, "output"))
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
