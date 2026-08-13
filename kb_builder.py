#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from kb.builder import build_site

def main() -> None:
    parser = argparse.ArgumentParser(description="IT Knowledge Base Builder")
    parser.add_argument("--docs", type=Path, default=Path("./docs"), help="Path to markdown docs directory")
    parser.add_argument("--output", type=Path, default=Path("./output"), help="Path to output directory")
    args = parser.parse_args()

    try:
        build_site(args.docs, args.output)
    except KeyboardInterrupt:
        print("\n[INFO] Build cancelled by user.")
        sys.exit(130)

if __name__ == "__main__":
    main()
