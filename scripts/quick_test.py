"""Quick integrity test for the CPC reproducibility package."""

from __future__ import annotations

import argparse
import csv
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from pikan_lid_driven_cavity.performance_table import generate_performance_tables


DEFAULT_REYNOLDS_NUMBERS = [100, 400, 1000, 5000]
METHOD_PREFIXES = {"PI-KAN": "pi_kan", "PINN": "pinn"}


def _require(path: Path, missing: list[Path]) -> None:
    if not path.exists():
        missing.append(path)


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--re",
        type=int,
        choices=DEFAULT_REYNOLDS_NUMBERS,
        action="append",
        dest="reynolds_numbers",
        help="Limit checks to one Reynolds number. Repeat to check multiple cases.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    reynolds_numbers = args.reynolds_numbers or DEFAULT_REYNOLDS_NUMBERS
    missing: list[Path] = []

    for reynolds in reynolds_numbers:
        _require(REPO_ROOT / "configs" / f"re{reynolds}.json", missing)
        for method, prefix in METHOD_PREFIXES.items():
            _require(REPO_ROOT / "results" / "logs" / f"{prefix}_re{reynolds}_metrics.json", missing)
            _require(REPO_ROOT / "results" / "logs" / f"{prefix}_re{reynolds}_loss_history.csv", missing)
            _require(REPO_ROOT / "results" / "data" / f"{prefix}_re{reynolds}_fields.npz", missing)
            _require(REPO_ROOT / "results" / "tables" / f"{prefix}_re{reynolds}_centerlines.csv", missing)
            _require(REPO_ROOT / "results" / "figures" / f"{prefix}_flow_field_re{reynolds}.png", missing)
            _require(REPO_ROOT / "results" / "figures" / f"{prefix}_all_fields_re{reynolds}.png", missing)
            _require(REPO_ROOT / "results" / "figures" / f"{prefix}_centerlines_re{reynolds}.png", missing)
            _require(REPO_ROOT / "results" / "figures" / f"{prefix}_loss_history_re{reynolds}.png", missing)
            if method == "PI-KAN":
                _require(REPO_ROOT / "results" / "logs" / f"pikan_re{reynolds}_bspline_stats.json", missing)
                _require(REPO_ROOT / "results" / "figures" / f"pikan_bspline_diagnostics_re{reynolds}.png", missing)

    _require(REPO_ROOT / "results" / "logs" / "environment_info.json", missing)
    _require(REPO_ROOT / "results" / "tables" / "performance_table.csv", missing)

    if missing:
        print("Missing required package files:")
        for path in missing:
            print(f"  {path.relative_to(REPO_ROOT)}")
        return 1

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_output = Path(tmp_dir)
        generate_performance_tables(
            REPO_ROOT / "results" / "logs",
            tmp_output,
            markdown=False,
            xlsx=False,
        )
        generated = _csv_rows(tmp_output / "performance_table.csv")

    archived = _csv_rows(REPO_ROOT / "results" / "tables" / "performance_table.csv")
    if generated != archived:
        print("results/tables/performance_table.csv is not synchronized with results/logs/*_metrics.json")
        print("Run: python scripts/generate_performance_table.py")
        return 1

    cases = ", ".join(f"Re={reynolds}" for reynolds in reynolds_numbers)
    print(f"Quick test passed for {cases}: configs, metrics, field data, figures, and generated table are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
