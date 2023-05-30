# Post-processing scripts
General scripts used for varying post-processing purposes saved here for posterity, barebones documentation, and ease of sharing with colleagues.

# EllipSys
- `rst2pv.sh`
  - All-in-one script for going from EllipSys2D restart files to a `.p3d`-metafile for timeseries-animating in Paraview. `generate_p3d.py` is embedded for portability, and thus not required.
  - **Dependencies**: A compiled EllipSys2D postprocessor, and ParaView if visualization is desired.
  - [Simple tutorial for set-up and use found here](#rst2pv).
- `generate_p3d.py`
  - Generates a `.p3d`-metafile using all `grid_*.f` and `grid_*.nam` (i.e. post-processed) files.
  - **Dependencies**: None

# Tutorials
Select tutorials for setting up and using these utility scripts, mainly intended for making it easier to share with colleagues.

## <a name="#rst2pv"></a>rst2pv
`rst2pv` is an all-in-one script which is able to handle postprocessing of all `grid.RST` files, generation of a `.p3d` meta-file for ParaView, automatic running of ParaView with the `.p3d` file loaded, and even running ParaView with a (ParaView) Python script for easing repeated identical visualization.

### Set-up
To set-up this script, it is necessary to change the two paths `POSTPROCESSOR` and `PARAVIEW` to your own (EllipSys) postprocessor and ParaView binaries:

```bash
...

# ============================================ #
# PATH INPUTS
# ============================================ #
# path to postprocessor and paraview
POSTPROCESSOR="$HOME/git/ellipsys/ellipsys2d/Executables/postprocessor"
PARAVIEW="$HOME/ParaView-5.11.0-MPI-Linux-Python3.9-x86_64/bin/paraview"

...
```

Note that if you're using PyEllipsys, `rst2pv` does not support shared objects `.so`, so make sure the postprocessor is compiled as a binary.

For easy access, an alias (or more specifically, a function to allow passing of flags) can be set-up to avoid having to drag the script around. As an example, add the following to your `.bashrc` or `.bash_aliases` files:
```bash
rst2pv() {
  *YOUR_PATH_TO_RST2PV*/rst2pv.sh "$@"
}
```
Thus to call `rst2pv.sh`, one can simply input the following in the terminal while being in the same directory as your `grid.RST` files by calling 

```bash
rst2pv -FLAGS
```

in the terminal.



### Options
`rst2pv` supports five different flags:

| Flag | Name | Description |
| ---- | ---- | ----------- |
| `-p` | postprocess | enables post-processing of the `grid.RST` files. |
| `-g` | generate | enables the generation of the `.p3d` meta-file needed for ParaView.
| `-t` | temporal | sets the postprocessing to look for `grid.RST.0?.*` files |
| `-v` | visualize | enables starting up ParaView and loading the `.p3d` meta-file. |
| `-s` | script | enables starting up ParaView using a ParaView Python script (e.g. generated using the `Trace` option). Requires the script to be in the same folder as `rst2pv.sh`. If an invalid script is given, a list of all scripts with format `pv_*.py` are given. |
