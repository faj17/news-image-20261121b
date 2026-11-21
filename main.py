"""The World Today — Saturday, 21 November 2026.

A tiny, dependency-free generator for the make.fun news-image-20261121
bounty. It ships one artefact: ``entry.png``, a newspaper front page that
sums up the day's world news in a single image.

Stories on the front page (all real, reported on 20-21 November 2026):

1.  The International Court of Justice finds Myanmar guilty of genocide
    against the Rohingya — the first time an international court has ever
    found a state guilty of genocide.
2.  Russia launches one of the war's largest overnight barrages on
    Ukraine — about 400 drones and 110 missiles — and Russian missiles
    crash in south-eastern Poland, which Warsaw flags as a provocation.
3.  The US Senate rejects the Iran war-powers resolution by 51-48.
4.  COP31 climate talks in Turkey enter their crucial final stage, with
    fossil fuels and climate finance at the centre of the negotiations.
5.  Cyclonic Storm Akvan crosses the Odisha coast near Gopalpur, bringing
    strong winds and heavy rain.
6.  JPMorgan Chase, Visa and Mastercard report cyberattacks on
    third-party vendors; the firms say their core payment networks are
    unaffected.
7.  The Council of the EU adopts EUR 1 billion in military aid for
    Ukraine, and the UK pledges more than 1,000 drones in a
    GBP 260 million package.
8.  Brazil's imprisoned former president Jair Bolsonaro is taken to
    hospital with severe abdominal pain.

What this script does
---------------------
It locates ``entry.png`` next to this file, checks that it really is a
1024x1024 PNG no larger than 1 MiB, copies it byte-for-byte into the
output directory, and then re-reads the copy to confirm the SHA-256
digest matches the original. Nothing is downloaded, nothing is rendered
here — the image itself is the entry.

Usage::

    MAKEFUN_OUTPUT_DIR=out python3 main.py
    python3 main.py --output out --verbose

Python 3.13, standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_png_size(path: Path) -> tuple[int, int]:
    """Read width and height from a PNG's IHDR chunk.

    Raises ValueError when the file is not a PNG or its header is
    truncated. Only the first 33 bytes are read, so this is cheap.
    """
    with path.open("rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_MAGIC:
        raise ValueError(f"{path}: not a PNG file (bad magic bytes)")
    chunk_len, chunk_type = struct.unpack(">I4s", header[8:16])
    if chunk_type != b"IHDR" or chunk_len != 13:
        raise ValueError(f"{path}: first chunk is not a valid IHDR")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def check_entry(path: Path, verbose: bool = False) -> tuple[int, str]:
    """Validate the entry image; return (size in bytes, sha256)."""
    if not path.is_file():
        raise FileNotFoundError(f"entry image not found: {path}")
    size = path.stat().st_size
    if size > MAX_BYTES:
        raise ValueError(
            f"{path}: {size} bytes exceeds the 1 MiB limit ({MAX_BYTES})"
        )
    width, height = read_png_size(path)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"{path}: {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    digest = sha256_of(path)
    if verbose:
        print(f"validated {path} ({width}x{height}, {size} bytes)", file=sys.stderr)
    return size, digest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Copy the 21 November 2026 front-page image to the output dir."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="output directory (overrides MAKEFUN_OUTPUT_DIR, default /output)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print progress notes to stderr",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    source = Path(__file__).resolve().parent / "entry.png"
    try:
        size, digest = check_entry(source, verbose=args.verbose)
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out_dir = Path(
        args.output or os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    )
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "entry.png"
        shutil.copyfile(source, target)
        copied_digest = sha256_of(target)
    except OSError as exc:
        print(f"error: cannot write output: {exc}", file=sys.stderr)
        return 1

    if copied_digest != digest:
        print(
            "error: SHA-256 mismatch after copy "
            f"(source {digest}, copy {copied_digest})",
            file=sys.stderr,
        )
        return 1

    width, height = read_png_size(target)
    print(f"output: {target}")
    print(f"bytes: {size}")
    print(f"dimensions: {width}x{height}")
    print(f"sha256: {copied_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
