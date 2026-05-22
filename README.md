# PI-KAN Lid-Driven Cavity Reproducibility Package

This repository contains the Computer Physics Communications reproducibility package for the manuscript:

**Physics-Informed Kolmogorov-Arnold Networks for Efficient Simulation of Lid-Driven Cavity Flow**

The package compares a physics-informed Kolmogorov-Arnold network (PI-KAN, using `pykan`) with a baseline physics-informed neural network (PINN, using a PyTorch multilayer perceptron) for the steady two-dimensional incompressible lid-driven cavity problem at
`Re = 100, 400, 1000, 5000`.

The scientific method and archived Kaggle full-run outputs are preserved. This repository conversion reorganizes the files, documents the reproduction path, and adds deterministic post-processing scripts for package validation and performance-table generation.

## Repository Layout

```text
configs/      Full-run configuration files for each Reynolds-number case.
docs/         CPC software notes and response-to-editor text.
results/      Archived JSON, CSV, NPZ, PNG, XLSX, and model outputs.
scripts/      Command-line utilities for validation and table generation.
src/          Reusable Python utilities used by scripts/.
```

Important result locations:

```text
results/logs/*_metrics.json
results/logs/*_loss_history.csv
results/data/*_fields.npz
results/figures/*.png
results/tables/performance_table.csv
results/tables/*_centerlines.csv
```

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

The quick test verifies that the four Reynolds-number configurations are present, checks the archived JSON/CSV/NPZ/PNG outputs, and confirms that `results/tables/performance_table.csv` is generated from `results/logs/*_metrics.json`.

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
results/tables/performance_table.md
results/tables/performance_table.xlsx
```

The XLSX export is written when the optional spreadsheet dependencies from `requirements.txt` are installed; CSV generation does not depend on them.

## Full-Run Reproduction Instructions

The archived full-run settings are stored in `configs/re100.json`, `configs/re400.json`, `configs/re1000.json`, and `configs/re5000.json`. Each case uses:

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

For CPC review of the included full-run archive, validate each case and regenerate the derived performance table:

```powershell
python scripts/quick_test.py --re 100
python scripts/quick_test.py --re 400
python scripts/quick_test.py --re 1000
python scripts/quick_test.py --re 5000
python scripts/generate_performance_table.py
```

The resulting table should match the archived full-run metrics in `results/logs/`. The original Kaggle run used the environment recorded in `results/logs/environment_info.json`.

## Outputs

For each method and Reynolds number, the repository includes:

- Metric JSON files with runtime, loss, memory, optimizer, and flow-summary quantities.
- Loss-history CSV files.
- Structured-grid field data in NPZ format.
- Centerline velocity-profile CSV files.
- Flow-field, centerline, loss-history, and diagnostic PNG figures.

The PI-KAN cases also include B-spline diagnostic JSON/PNG outputs.

## Citation

Please cite this repository using the metadata in `CITATION.cff`.

## License

This repository is distributed under the MIT License. See `LICENSE`.
