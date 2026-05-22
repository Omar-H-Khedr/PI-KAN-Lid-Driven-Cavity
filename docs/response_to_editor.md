Dear Professor Hazel,

Thank you for your assessment of our manuscript and for highlighting the Computer Physics Communications requirement concerning software implementation, performance details, and software availability.

We have revised the manuscript to address this point. A new section entitled "Software Implementation and Reproducibility" has been added. This section describes the implementation of the PI-KAN solver and the baseline PINN solver, the stream-function formulation, the Navier-Stokes residual calculation, the training workflow, the dependencies, the output files, and the performance-measurement procedure.

We have also prepared a reproducible software package containing the source code, configuration information, training scripts, post-processing routines, loss-history files, field-data exports, centerline velocity profiles, and performance-table generation. The software records wall-clock time, final loss, peak memory usage, optimizer settings, and grid-based flow-field outputs for each Reynolds-number case.

The final version of the code will be made publicly available through GitHub and archived through Zenodo to ensure long-term reproducibility and accessibility.

Sincerely,
Omar Khedr
on behalf of all authors
