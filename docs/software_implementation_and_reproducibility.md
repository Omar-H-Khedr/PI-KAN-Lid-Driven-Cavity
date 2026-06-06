# Software Implementation and Reproducibility

This repository contains the CPC reproducibility package for the PI-KAN and PINN lid-driven cavity study. The conversion from the Kaggle-generated archive preserves the scientific method and the full-run outputs, while organizing the package into a conventional GitHub layout with documented validation and post-processing commands.

## Numerical Formulation

The study solves the steady two-dimensional incompressible lid-driven cavity problem. Both neural solvers output the stream function `psi` and pressure `p`. The velocity field is recovered by automatic differentiation:

```text
u = dpsi/dy
v = -dpsi/dx
```

The momentum residuals are evaluated directly from automatic differentiation of the velocity components:

```text
r_x = u*u_x + v*u_y + p_x - nu*(u_xx + u_yy)
r_y = u*v_x + v*v_y + p_y - nu*(v_xx + v_yy)
```

This formulation avoids manually simplified derivative expressions and keeps the physics-informed residual evaluation reproducible.

## Models

The package compares:

- PI-KAN, implemented with `pykan`.
- PINN, implemented as a PyTorch multilayer perceptron baseline.

Both models use the same physics-informed training objective, boundary-condition treatment, collocation sampling scale, optimizer sequence, and evaluation grid for a given Reynolds-number case.

## Full-Run Configuration

The full-run cases are described by:

```text
configs/re100.json
configs/re400.json
configs/re1000.json
configs/re5000.json
```

Each configuration records the Reynolds number, viscosity, collocation-point count, boundary-point count, Adam epochs, L-BFGS iteration limit, evaluation-grid size, seed, lid velocity, and density.

The archived Kaggle run used the environment recorded in:

```text
results/logs/environment_info.json
```

## Archived Outputs

The repository keeps all generated JSON, CSV, NPZ, and PNG outputs under `results/`:

```text
results/logs/       Metrics, loss histories, B-spline diagnostics, environment record.
results/data/       Structured-grid field data in NPZ format.
results/figures/    Flow fields, centerlines, loss histories, and diagnostics.
results/tables/     Performance table and centerline CSV files.
results/model/      Saved model snapshot from the original package.
```

The metric JSON files record wall-clock training time, final loss, optimizer settings, L-BFGS closure calls, process-level peak CPU memory, CUDA peak memory when available, maximum speed, approximate primary vortex location, and paths to the associated outputs.

## Deterministic Post-Processing

The performance table is generated from the metric JSON files:

```powershell
python scripts/generate_performance_table.py
```

This command rewrites:

```text
results/tables/performance_table.csv
results/tables/performance_table.md
results/tables/performance_table.xlsx
```

The CSV output is the canonical derived table. The XLSX output is regenerated when the spreadsheet dependencies listed in `requirements.txt` are installed.

The quick integrity test verifies that the package is complete and that the CSV performance table is synchronized with the metric JSON files:

```powershell
python scripts/quick_test.py
```

Per-case checks can be run with `--re`, for example:

```powershell
python scripts/quick_test.py --re 100
```

## Reproducibility Statement

The conversion performed for this repository does not change the numerical formulation, the training settings, or the archived scientific outputs. It provides a clean file layout, citation and license metadata, reproducibility documentation, and scripts for validating the included full-run archive and regenerating derived performance tables.
