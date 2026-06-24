#!/usr/bin/env python3
"""
Batch convert files to Markdown using MarkItDown (library) or fallback to the `markitdown` CLI.
Usage:
  python scripts/batch_convert.py [source_path] [--out OUT_DIR] [--recursive]
Examples:
  python scripts/batch_convert.py . --out md_output --recursive
  python scripts/batch_convert.py example.pdf
"""

from __future__ import annotations
import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

# Unset broken proxy vars to avoid connection errors
for _key in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
    os.environ.pop(_key, None)

DEFAULT_EXTS = [
    ".pdf", ".docx", ".doc", ".pptx", ".ppt",
    ".xlsx", ".xls", ".csv", ".html", ".htm",
    ".epub", ".ipynb", ".msg", ".txt",
]


def convert_with_lib(src: Path, dst: Path) -> None:
    from markitdown import MarkItDown

    md = MarkItDown(enable_plugins=False)
    res = md.convert(str(src))
    text = getattr(res, "text_content", None) or getattr(res, "text", None) or str(res)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def convert_with_cli(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["markitdown", str(src), "-o", str(dst)], check=True)


def _check_markitdown() -> bool:
    """Check if markitdown is available (lib or CLI)."""
    try:
        from markitdown import MarkItDown  # noqa: F401
        return True
    except ImportError:
        try:
            subprocess.run(["markitdown", "--help"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


def try_convert(src: Path, dst: Path) -> Tuple[bool, str]:
    try:
        convert_with_lib(src, dst)
        return True, "lib"
    except Exception as lib_err:
        try:
            convert_with_cli(src, dst)
            return True, "cli"
        except Exception as cli_err:
            return False, f"lib error: {lib_err}; cli error: {cli_err}"


def find_files(root: Path, exts: List[str], recursive: bool) -> List[Path]:
    if root.is_file():
        return [root]
    if recursive:
        return [p for p in root.rglob("*") if p.suffix.lower() in exts and p.is_file()]
    else:
        return [p for p in root.iterdir() if p.suffix.lower() in exts and p.is_file()]


def parse_exts(csv: str) -> List[str]:
    return [e if e.startswith(".") else f".{e}" for e in (csv.split(",") if csv else DEFAULT_EXTS)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch convert files to Markdown using MarkItDown")
    parser.add_argument("source", nargs="?", default=".", help="Source file or folder (default: current folder)")
    parser.add_argument("--out", "-o", default="", help="Output folder (default: same folder as source files)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Recurse into subfolders")
    parser.add_argument("--exts", default=",".join([e.lstrip('.') for e in DEFAULT_EXTS]), help="Comma-separated extensions (no dot), e.g. pdf,docx,xlsx")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    out_root = Path(args.out).expanduser().resolve() if args.out else None
    recursive = args.recursive
    exts = parse_exts(args.exts)
    exts = [e.lower() for e in exts]

    if not _check_markitdown():
        print("markitdown is not installed. Run: pip install 'markitdown[all]'")
        return 2

    files = find_files(source, exts, recursive)
    if not files:
        print(f"No matching files found. Supported extensions: {', '.join(exts)}")
        return 1

    total = len(files)
    success_count = 0

    for idx, src in enumerate(files, start=1):
        try:
            if out_root:
                rel = src.relative_to(source) if source.is_dir() else Path(src.name)
                dst = out_root.joinpath(rel).with_suffix(".md")
            else:
                dst = src.with_suffix(".md")

            ok, info = try_convert(src, dst)
            if ok:
                success_count += 1
                print(f"[{idx}/{total}] Converted: {src} -> {dst} ({info})")
            else:
                print(f"[{idx}/{total}] Failed: {src} -> {dst} ({info})")
        except Exception as e:
            print(f"[{idx}/{total}] Error processing {src}: {e}")

    print(f"\nFinished. {success_count}/{total} files converted.")
    if success_count != total:
        print("Some files failed. See messages above. If MarkItDown is not installed, run: pip install 'markitdown[all]' or use the CLI tool 'markitdown'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
