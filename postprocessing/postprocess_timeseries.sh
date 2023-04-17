#!/bin/bash
# ============================================ #
# Bash script for automated post-processing of
# many EllipSys restart files for time-series
# generation.
#
# Author: Kristian Ebstrup
# Email: kreb@dtu.dk
# ============================================ #

# path to postprocessor and paraview
POSTPROCESSOR="$HOME/git/ellipsys/ellipsys2d/Executables/postprocessor"
PARAVIEW="ParaView-5.11.0-MPI-Linux-Python3.9-x86_64/bin/paraview"

# initialization of flags
flag_postprocess=false
flag_generate_p3d=false
flag_paraview=false

# flag handling
while getopts "pgv" opt; do
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
  flag_postprocessor=true
fi

# get source directory while saving original directory
ORIGINAL_DIR=$(pwd)
SOURCE_DIR=${BASH_SOURCE_DIR[0]}

if $flag_postprocessor; then
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
    echo "Post-processing $file ..."
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
fi

if $flag_generate_p3d; then
  echo "Preparing .p3d file with timeseries (timeseries.p3d)..." 
  python $SOURCE_DIR/generate_p3d.py
  echo "Timeseries ready."
fi

if $flag_paraview; then
  echo "Starting up ParaView with timeseries..."
  $PARAVIEW timeseries.p3d
fi
