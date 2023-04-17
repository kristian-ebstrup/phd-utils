# Post-processing scripts
General scripts used for varying post-processing purposes saved here for posterity, barebones documentation, and ease of sharing with colleagues.

# EllipSys
- `postprocess_timeseries.sh`
  - All-in-one script for going from EllipSys2D restart files to a `.p3d`-metafile for timeseries-animating in Paraview.
  - **Dependencies**: `generate_p3d.py`
- `generate_p3d.py`
  - Generates a `.p3d`-metafile using all `grid_*.f` and `grid_*.nam` (i.e. post-processed) files.
  - **Dependencies**: None
