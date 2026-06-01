"""Regenerate performance tables from archived metric JSON files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from pikan_lid_driven_cavity.performance_table import generate_performance_tables


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--metrics-dir",
        type=Path,
        default=REPO_ROOT / "results" / "logs",
        help="Directory containing *_metrics.json files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO_ROOT / "results" / "tables",
        help="Directory where performance_table.* files are written.",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Also write performance_table.md.",
    )
    parser.add_argument(
        "--xlsx",
        action="store_true",
        help="Also write performance_table.xlsx.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    written = generate_performance_tables(
        args.metrics_dir,
        args.output_dir,
        markdown=args.markdown,
        xlsx=args.xlsx,
    )
    for path in written:
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
