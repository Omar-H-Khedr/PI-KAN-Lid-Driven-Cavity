## Software Implementation and Reproducibility

A reproducible Python implementation was prepared for the present study. The software package contains the PI-KAN solver, the baseline PINN solver, training routines, post-processing scripts, loss-history export, field-data export, centerline-profile extraction, and performance-table generation.

Both models output the stream function and pressure. The velocity field is recovered by automatic differentiation as u = dpsi/dy and v = -dpsi/dx. The Navier-Stokes residuals are evaluated using direct automatic differentiation of the velocity components, including u_x, u_y, v_x, v_y, u_xx, u_yy, v_xx, and v_yy. This avoids relying on manually simplified derivative expressions and improves reproducibility of the physics-informed implementation.

The software records wall-clock training time, final loss, Adam and L-BFGS settings, L-BFGS closure calls, process-level peak CPU memory, optional CUDA peak memory, maximum velocity magnitude, approximate primary vortex location, centerline velocity profiles, and field data on a structured grid.

The implementation uses Python, PyTorch, pykan, NumPy, pandas, Matplotlib, and psutil. The repository includes a requirements file and a README file explaining how to reproduce the Reynolds-number cases Re = 100, 400, 1000, and 5000. The final public version should be made available through GitHub and archived on Zenodo to provide a permanent DOI-linked software release.
