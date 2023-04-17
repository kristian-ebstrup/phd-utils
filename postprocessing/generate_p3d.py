#!/usr/bin/Aenv python
# Simple script to generate a .p3d file for input in ParaView
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
