# PI-KAN Lid-Driven Cavity Reproducibility Package

This repository contains the Computer Physics Communications reproducibility package for the manuscript:

**Physics-Informed Kolmogorov-Arnold Networks for Efficient Simulation of Lid-Driven Cavity Flow**

The package compares a FastSpline-KAN physics-informed model with baseline
and wide PINN variants for the steady two-dimensional incompressible
lid-driven cavity problem at
`Re = 100, 400, 1000, 5000`.

The archived Kaggle validation outputs are preserved in a clean GitHub layout.
The repository documents the reproduction path and includes deterministic
post-processing scripts for package validation and performance-table
generation.

## Repository Layout

```text
configs/      Full-run configuration files for each Reynolds-number case.
docs/         CPC software notes and response-to-editor text.
data/         Reference Ghia centerline profiles used for validation.
results/      Archived JSON, CSV, PNG, and model checkpoint outputs.
scripts/      Command-line utilities for validation and table generation.
src/          Reusable Python utilities used by scripts/.
```

Important result locations:

```text
results/logs/*_metrics.json
results/logs/*_loss_history.csv
results/figures/*.png
results/models/*.pt
results/reference_validation/error_table.csv
results/reference_validation/runtime_vs_error.csv
results/reference_validation/*_centerline.csv
results/reference_validation/*_centerline_comparison.png
results/tables/performance_table.csv
results/tables/progress_metrics_all.csv
validation_sprint_summary.md
```

## Updated Validation Dataset

The archived validation outputs have been replaced with the Kaggle
FastSpline-KAN / PINN lid-driven cavity benchmark results, including the
Re = 5000 stress-test case. The validation sweep covers:

```text
Re = 100, 400, 1000, 5000
```

Model variants included in the updated result archive:

- FastSpline-KAN medium
- PINN baseline
- PINN wide

Key generated files are organized under:

```text
data/reference/ghia_u_centerline.csv
data/reference/ghia_v_centerline.csv
results/reference_validation/error_table.csv
results/reference_validation/runtime_vs_error.csv
results/reference_validation/*_centerline.csv
results/reference_validation/*_centerline_comparison.png
results/reference_validation/loss_vs_error.png
results/reference_validation/runtime_vs_error.png
results/tables/performance_table.csv
results/tables/progress_metrics_all.csv
results/figures/*_flow_field.png
results/logs/*_loss_history.csv
results/logs/*_metrics.json
results/models/*.pt
validation_sprint_summary.md
```

The reference-validation tables report centerline agreement against the
archived Ghia reference profiles, while the runtime/error summaries compare
training cost and validation accuracy across the three model variants.

## Method Summary

Both networks output the stream function `psi` and pressure `p`. Velocities are recovered by automatic differentiation:

```text
u = dpsi/dy
v = -dpsi/dx
```

The Navier-Stokes residuals are evaluated from the velocity derivatives:

```text
r_x = u*u_x + v*u_y + p_x - nu*(u_xx + u_yy)
r_y = u*v_x + v*v_y + p_y - nu*(v_xx + v_yy)
```

No-slip boundary conditions are imposed on the stationary walls, and unit horizontal velocity is imposed on the moving lid.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Linux or macOS, activate with `source .venv/bin/activate`.

## Quick Test

Run the package integrity check:

```powershell
python scripts/quick_test.py
```

The quick test verifies that the four Reynolds-number configurations are
present, checks the new validation CSV/PNG/model artifacts, and confirms that
`results/tables/performance_table.csv` is synchronized with
`results/logs/*_metrics.json`.

To check one Reynolds-number case:

```powershell
python scripts/quick_test.py --re 100
```

## Regenerate the Performance Table

```powershell
python scripts/generate_performance_table.py
```

This reads all `results/logs/*_metrics.json` files and rewrites:

```text
results/tables/performance_table.csv
```

Optional Markdown and XLSX exports can be written with `--markdown` and
`--xlsx`; CSV generation does not depend on spreadsheet dependencies.

## Validation Checks

The archived configuration files are stored in `configs/re100.json`,
`configs/re400.json`, `configs/re1000.json`, and `configs/re5000.json`.
Each case uses:

```text
n_collocation = 2500
n_boundary = 2500
adam_epochs = 200
lbfgs_max_iter = 1000
grid_n = 100
seed = 42
lid_velocity = 1.0
rho = 1.0
```

For review of the included validation archive, validate each case and
regenerate the derived performance table:

```powershell
python scripts/quick_test.py --re 100
python scripts/quick_test.py --re 400
python scripts/quick_test.py --re 1000
python scripts/quick_test.py --re 5000
python scripts/generate_performance_table.py
```

The resulting table should match the archived validation metrics in
`results/logs/`.

## Outputs

For each model variant and Reynolds number, the repository includes:

- Metric JSON files with runtime, loss, memory, parameter-count, and validation-error quantities.
- Loss-history CSV files.
- Model checkpoints for each variant/Reynolds-number case.
- Centerline velocity-profile CSV files and comparison PNG figures.
- Flow-field PNG figures.
- Reference-validation error and runtime/error summary tables.

## Citation

Please cite this repository using the metadata in `CITATION.cff`.

## License

This repository is distributed under the MIT License. See `LICENSE`.
