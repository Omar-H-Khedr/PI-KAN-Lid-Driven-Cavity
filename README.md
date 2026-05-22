# Physics-Informed Kolmogorov-Arnold Networks for Lid-Driven Cavity Flow

This package contains a reproducible Kaggle-generated software snapshot for the manuscript:

**Physics-Informed Kolmogorov-Arnold Networks for Efficient Simulation of Lid-Driven Cavity Flow**

## Purpose

The code compares:

- PI-KAN using `pykan`
- Baseline PINN using a PyTorch multilayer perceptron

for the 2D steady incompressible lid-driven cavity flow at Reynolds numbers:

[100, 400, 1000, 5000]

## Formulation

The networks output the stream function psi and pressure p. Velocities are recovered as:

- u = dpsi/dy
- v = -dpsi/dx

The Navier-Stokes residual is computed using direct automatic differentiation of u and v:

- r_x = u*u_x + v*u_y + p_x - nu*(u_xx + u_yy)
- r_y = u*v_x + v*v_y + p_y - nu*(v_xx + v_yy)

Boundary conditions impose no-slip on all walls and unit horizontal velocity on the moving top lid.

## Run mode

FULL_RUN = True

- If FULL_RUN = False, the notebook uses a quick test setting.
- If FULL_RUN = True, the notebook uses manuscript-style settings.

## Numerical settings in this run

- Collocation points: 2500
- Boundary points: 2500
- Adam epochs: 200
- L-BFGS max iterations: 1000
- Evaluation grid: 100 x 100
- Device: cuda
- KAN available: True

## Outputs

The package generates:

- `logs/*_metrics.json`
- `logs/*_loss_history.csv`
- `tables/performance_table.csv`
- `tables/performance_table.md`
- `tables/performance_table.xlsx`
- `data/*_fields.npz`
- `figures/*`
- `docs/software_section.md`
- `docs/response_to_editor.md`

## Notes for CPC submission

For the final CPC revision, run with `FULL_RUN = True`, verify that the generated figures and tables match the manuscript, then upload the code to GitHub and archive a versioned release on Zenodo.
