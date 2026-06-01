"""Build performance tables from archived metric JSON files."""

from __future__ import annotations

import csv
import json
import warnings
from pathlib import Path
from typing import Iterable


PERFORMANCE_COLUMNS = [
    "re",
    "variant",
    "family",
    "n_parameters",
    "training_time_seconds",
    "final_training_loss",
    "lbfgs_closure_calls",
    "peak_gpu_memory_mb",
]

VARIANT_ORDER = {
    "fast_spline_kan_medium": 0,
    "pinn_baseline": 1,
    "pinn_wide": 2,
}


def load_metric_records(metrics_dir: Path) -> list[dict[str, object]]:
    """Load one row per ``*_metrics.json`` file."""
    metrics_dir = Path(metrics_dir)
    if not metrics_dir.exists():
        raise FileNotFoundError(f"Metrics directory does not exist: {metrics_dir}")

    records: list[dict[str, object]] = []
    for path in sorted(metrics_dir.glob("*_metrics.json")):
        with path.open("r", encoding="utf-8") as handle:
            metric = json.load(handle)
        records.append({column: metric.get(column) for column in PERFORMANCE_COLUMNS})

    if not records:
        raise FileNotFoundError(f"No *_metrics.json files found in: {metrics_dir}")

    records.sort(
        key=lambda row: (
            int(row["re"]),
            VARIANT_ORDER.get(str(row["variant"]), 99),
            str(row["variant"]),
        )
    )
    return records


def write_csv(records: Iterable[dict[str, object]], output_path: Path) -> Path:
    """Write the canonical CSV performance table."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PERFORMANCE_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    return output_path


def _format_markdown_value(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def write_markdown(records: Iterable[dict[str, object]], output_path: Path) -> Path:
    """Write a lightweight Markdown version of the performance table."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = [[_format_markdown_value(record[column]) for column in PERFORMANCE_COLUMNS] for record in records]
    widths = [
        max(len(column), *(len(row[index]) for row in rows))
        for index, column in enumerate(PERFORMANCE_COLUMNS)
    ]

    header = "| " + " | ".join(column.ljust(widths[index]) for index, column in enumerate(PERFORMANCE_COLUMNS)) + " |"
    rule = "| " + " | ".join("-" * widths[index] for index in range(len(PERFORMANCE_COLUMNS))) + " |"
    body = [
        "| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |"
        for row in rows
    ]

    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join([header, rule, *body]) + "\n")
    return output_path


def write_xlsx(records: Iterable[dict[str, object]], output_path: Path) -> Path:
    """Write an Excel table when pandas/openpyxl are available."""
    import pandas as pd

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records, columns=PERFORMANCE_COLUMNS).to_excel(output_path, index=False)
    return output_path


def generate_performance_tables(
    metrics_dir: Path,
    output_dir: Path,
    *,
    markdown: bool = False,
    xlsx: bool = False,
) -> list[Path]:
    """Generate performance table files from metric JSON files."""
    records = load_metric_records(metrics_dir)
    output_dir = Path(output_dir)

    written = [write_csv(records, output_dir / "performance_table.csv")]
    if markdown:
        written.append(write_markdown(records, output_dir / "performance_table.md"))
    if xlsx:
        try:
            written.append(write_xlsx(records, output_dir / "performance_table.xlsx"))
        except ModuleNotFoundError as exc:
            warnings.warn(
                f"Skipping XLSX export because optional dependency is missing: {exc.name}",
                RuntimeWarning,
                stacklevel=2,
            )
    return written
