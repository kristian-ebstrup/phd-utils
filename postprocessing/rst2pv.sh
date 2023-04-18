#!/bin/bash
# ============================================ #
# Bash script for automated post-processing of
# many EllipSys restart files for time-series
# generation.
#
# Make sure to change the path inputs based
# on your own cases.
#
# Author: K. Ebstrup
# Email: kreb@dtu.dk
# ============================================ #


# ============================================ #
# PATH INPUTS
# ============================================ #
# path to postprocessor and paraview
POSTPROCESSOR="$HOME/git/ellipsys/ellipsys2d/Executables/postprocessor"
PARAVIEW="$HOME/ParaView-5.11.0-MPI-Linux-Python3.9-x86_64/bin/paraview"


# ============================================ #
# EMBEDDED PYTHON SCRIPT
# ============================================ #
function generate_p3d {
  python - << EOF
#!/usr/bin/env python
# Small script to generate a .p3d file for input in ParaView
# Author: Kristian Ebstrup
# Email: kreb@dtu.dk
from glob import glob

# resulting filename
p3dname: str = "timeseries.p3d"

# get list of .f-files and .xyz-files
f = sorted(glob("*.f"))
xyz = sorted(glob("*.xyz"))

# initialize arbitrary starting time
t: int = 0

with open(p3dname, "w") as file:
    # first input function-names
    file.write('{\n  "function-names": ')
    file.write(
        '[\n    "u",\n    "v",\n    "w",\n    "p",\n    "vis",\n    "vorticity",\n    "normal",\n    "ko2_tke",\n    "ko2_omega",\n    ],\n'
    )

    # then filenames using f-string
    file.write('    "filenames": [\n')
    for i, _ in enumerate(f):
        file.write(
            f'        {{ "time" : {t}, "xyz" : "{xyz[i]}", "function" : "{f[i]}" }},\n'
        )

        # increment t by one to ensure paraview understands the series
        t += 1

    # wrap up filenames and file
    file.write("    ]\n")
    file.write("}")
EOF
}


# ============================================ #
# INITIALIZATION
# ============================================ #
# get source directory while saving original directory
ORIGINAL_DIR=$(pwd)
SOURCE_DIR=$( dirname ${BASH_SOURCE[0]} )

# initialization of flags
flag_postprocess=false
flag_generate_p3d=false
flag_paraview=false
flag_paraview_script=false

# flag handling
while getopts "pgvs:" opt; do
  case $opt in
    p )
      echo "Enabled post-processing of restart files"
      flag_postprocess=true 
      ;;
    g )
      echo "Enabled .p3d generation"
      flag_generate_p3d=true
      ;;
    v )
      echo "Enabled visualization in ParaView"
      flag_paraview=true
      ;;
    s )
      echo "Enabled automatic script when loading ParaView."
      flag_paraview=true
      flag_paraview_script=true
      PARAVIEW_SCRIPT=${OPTARG}
      PARAVIEW_SCRIPT_PATH="${SOURCE_DIR}/${PARAVIEW_SCRIPT}"
      if [ -f "${PARAVIEW_SCRIPT_PATH}" ]; then
        echo "Selected script: $PARAVIEW_SCRIPT"
      else
        echo "===== PATH INPUT ERROR ====="
        echo "MSG: Didn't find $PARAVIEW_SCRIPT. These are the available scripts:"
        ls -1 ${SOURCE_DIR}/pv_*.py | xargs -n 1 basename
        echo "FIX: Make sure your script is located in ${SOURCE_DIR}."
        exit
      fi
      ;;
    ? ) 
      echo "script usage: $(basename $0) [-p] [-g] [-v], where" >&2
      echo "    -p    enables post-processing of restart files"
      echo "    -g    enables .p3d generation using generate_p3d.py"
      echo "    -v    enables visualization in ParaView"
      exit 1
      ;;
  esac
done

if [ $OPTIND = 1 ]; then
  echo "No options given. Only running post-processing."
  flag_postprocess=true
fi


# ============================================ #
# POSTPROCESS
# ============================================ #
if $flag_postprocess; then
  # check if postprocessor path is valid
  if [ ! -f "$POSTPROCESSOR" ]; then
    echo "===== PATH INPUT ERROR ====="
    echo "MSG: Path $POSTPROCESSOR invalid"
    echo "FIX: Make sure the path is correctly defined in the script."
    exit 1
  fi

  # ensure we're in the original directory
  cd $ORIGINAL_DIR

  # check if grid.X2D and grid.T2D exists; do not change these paths.
  PATH_X2D="./grid.X2D"
  PATH_T2D="./grid.T2D"
  echo "Looking for grid.X2D and grid.T2D in current folder..."
  if [ -f "$PATH_X2D" ]; then
    echo "Found grid.X2D!"
  else
    echo "Didn't find grid.X2D. Terminating!"
    exit
  fi
  if [ -f "$PATH_T2D" ]; then
    echo "Found grid.T2D!"
  else
    echo "Didn't find grid.T2D. Terminating!"
    exit
  fi

  # get filelist
  echo "Getting list of restart files with extensions..."
  files=`ls ./grid.RST.*.*`

  # save default Internal Field Separator to allow string splitting
  _IFS=$IFS

  # iterate through each file
  for file in $files
  do
    # rename RST.01 file to grid.rst
    echo -ne "Post-processing $file ...      "\\r
    mv $file grid.rst
    
    # call postprocessor
    printf "grid\n" | $POSTPROCESSOR > /dev/null
    
    # set IFS to '.' to allow extracting iteration number
    IFS='.'

    # extract iteration number from filename
    read -a str_arr <<< "$file"
    iter_num=${str_arr[-1]}

    # return IFS to default to avoid breaking stuff
    IFS=$_IFS

    # shuffle files around for posterity
    mv grid.rst $file
    mv grid.f grid_$iter_num.f
    mv grid.xyz grid_$iter_num.xyz
  done
  # linebreak to avoid overwriting the processing echo when moving on
  echo ""
fi

# ============================================ #
# P3D GENERATION
# ============================================ #
if $flag_generate_p3d; then
  echo "Preparing .p3d file with timeseries (timeseries.p3d)..." 
  # embedded python script for portability; identical to generate_p3d.py
  generate_p3d
  echo "Timeseries ready."
fi

# ============================================ #
# RUN PARAVIEW
# ============================================ #
if $flag_paraview; then
  if [ ! -f "$PARAVIEW" ]; then
    echo "===== PATH INPUT ERROR ====="
    echo "MSG: Path $PARAVIEW invalid"
    echo "FIX: Make sure the path is correctly defined in the script."
  fi

  echo "Starting up ParaView with timeseries..."
  if $flag_paraview_script; then
    echo "Loading with script '${PARAVIEW_SCRIPT_PATH}' ..."
    $PARAVIEW --script=${PARAVIEW_SCRIPT_PATH}
  else
    echo "Loading without script ..."
    $PARAVIEW timeseries.p3d
  fi
fi

