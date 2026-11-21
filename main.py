#!/usr/bin/env python3
"""Copy the shipped entry.png to the make.fun output directory.

Stdlib only, deterministic. Never deletes the output directory.
Usage: python3 main.py
  (MAKEFUN_OUTPUT_DIR env var overrides the default /output.)
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    src_hash = sha256(SRC)
    dst_hash = sha256(dst)
    if src_hash != dst_hash:
        print(f"ERROR: sha256 mismatch src={src_hash} dst={dst_hash}", file=sys.stderr)
        return 1
    size = os.path.getsize(dst)
    print(f"wrote {dst} {size} bytes sha256={dst_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
