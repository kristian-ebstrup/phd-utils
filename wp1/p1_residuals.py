#!/usr/bin/env/ python3
# ---------------------- #
# POST-PROCESSING OF CONVERGENCE
# Author: Kristian Ebstrup
# Email: kreb@dtu.dk
# Date: 21/04/2023
# ---------------------- #
import numpy as np
import matplotlib.pyplot as plt
import glob
import re
from collections import deque

# --------------------- #
# SELECT DATA
# --------------------- #
paths = [
#        "08_des_with_respecifybc",
#        "09_urans_with_respecifybc",
        #"10_changing_dt",
        #"11_constant_dt",
#        "12_adj_eq_iter",
#        "13_adj_neq_iter",
#        "14_adj_nsub_neq_iter",
#        "15_3e6_new_turb",
#        "16_3e6_old_turb",
        "07_8D_GRID_DEPENDENCY",
        ]
print(f'''Files to be plotted:
  {paths}''')

#title = r"(Residuals) URANS, respecifybc xy, Re = $5\times10^6$)"
#title = r"(Residuals) URANS, no respecifybc, Re = $5\times10^6$)"
#title = r"(Residuals) DES, respecifybc xy, Re = $5\times10^6$)"
#title = r"(Residuals) DES, no respecifybc, Re = $5\times10^6$)"
title = r""

# --------------------- #
# MESH POINTS FOR COMPUTING ABSOLUTE RESIDUALS
# --------------------- #
# number of points: 256x256x256
ncells = 256**3

# --------------------- #
# PROCESS AND PLOT
# --------------------- #
print(
    """
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# POSTPROCESSING .OUT FILES                                   #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
"""
)
for path in paths:
    # --------------------- #
    # PREPARE FIGURE
    # --------------------- #
    fig, axs = plt.subplots(2,1)

    print("# ============================== #")
    print("# EXTRACTING DATA                #")
    print("# ============================== #")

    # glob folders
    file_pattern: str = f"mpi_*.out"
    files: list[str] = glob.glob(f"{path}/{file_pattern}")
    files.sort()
    print(f"Found {len(files)} using {file_pattern} file pattern")

    # initiate iterations
    n = []

    # initiate residual norms
    unorm = []
    vnorm = []
    wnorm = []
    pnorm = []
    tenorm = []
    sdnorm = []

    # initiate relative residuals
    urel = []
    vrel = []
    wrel = []
    prel = []
    terel = []
    sdrel = []

    # initiate absolute residuals
    uabs = []
    vabs = []
    wabs = []
    pabs = []
    teabs = []
    sdabs = []

    # initiate trackers
    stime = 0
    tracker_ctime = []
    tracker_stime = []
    tracker_glvl = []

    # struct:
    # [dt, glvl, n, nsub, nstepp, t, ures, vres, pres, tkeres, disres]
    for file in files:
        # go through file, extracting relevant information
        print(f"    Reading {file} ...")
        with open(file) as f:
            iter_lines = iter(f.readlines())
            for line in iter_lines:
                # split at whitespace OR = OR :
                _line: list[str] = re.split(r"\s+|=|:", line)

                # filter out inevitable empty entries from the RegEx
                words: list[str] = list(filter(None, _line))

                # if words is empty, make a dummy array to avoid errors
                if not bool(words):
                    words = [""]

                # depending on first word, do different things
                match words[0]:
                    case "Grid":
                        # get current grid level
                        #glvl = int(words[-1])
                        continue
                    case "n":
                        # [dt, glvl, n, nsub, nstepp,
                        #           t, ures, vres, wres, pres, tkeres, disres]
                        iter_words = iter(words)
                        while (word := next(iter_words, None)) is not None:
                            # go through each word and match
                            match word:
                                case "n":
                                    n.append(int(next(iter_words)))
                                case "nsub":
                                    continue
                                    #data[data_idx, 3] = int(next(iter_words))
                                case "nstepp":
                                    continue
                                    #data[data_idx, 4] = int(next(iter_words))
                                case "t":
                                    stime = float(next(iter_words))
                                    #data[data_idx, 5] = float(next(iter_words))
                                case "log(res)":
                                    # ures, vres, pres, tkeres, disres
                                    if not uabs: 
                                        urel.append(float(next(iter_words)))
                                        vrel.append(float(next(iter_words)))
                                        wrel.append(float(next(iter_words)))
                                        prel.append(float(next(iter_words)))
                                        terel.append(float(next(iter_words)))
                                        sdrel.append(float(next(iter_words)))
                                    else:
                                        urel.append(float(next(iter_words)))
                                        vrel.append(float(next(iter_words)))
                                        wrel.append(float(next(iter_words)))
                                        prel.append(float(next(iter_words)))
                                        terel.append(float(next(iter_words)))
                                        sdrel.append(float(next(iter_words)))

                                        uabs.append(10**(urel[-1]) * unorm[-1] / ncells)
                                        vabs.append(10**(vrel[-1]) * vnorm[-1] / ncells)
                                        wabs.append(10**(wrel[-1]) * wnorm[-1] / ncells)
                                        pabs.append(10**(prel[-1]) * pnorm[-1] / ncells)
                                        teabs.append(10**(terel[-1]) * tenorm[-1] / ncells)
                                        sdabs.append(10**(sdrel[-1]) * sdnorm[-1] / ncells)

                    # get the residuals
                    case "Residual":
                        match words[-2]:
                            case "U-velocity":
                                unorm.append(float(words[-1]))
                                # apply norms here if not applied yet
                                if not uabs:
                                    for _res in urel:
                                        uabs.append(10**(_res) * unorm[-1] / ncells)
                            case "V-velocity":
                                vnorm.append(float(words[-1]))
                                # apply norms here if not applied yet
                                if not vabs:
                                    for _res in vrel:
                                        vabs.append(10**(_res) * vnorm[-1] / ncells)
                            case "W-velocity":
                                wnorm.append(float(words[-1]))
                                # apply norms here if not applied yet
                                if not wabs:
                                    for _res in wrel:
                                        wabs.append(10**(_res) * wnorm[-1] / ncells)
                            case "Pressure":
                                pnorm.append(float(words[-1]))
                                # apply norms here if not applied yet
                                if not pabs:
                                    for _res in prel:
                                        pabs.append(10**(_res) * pnorm[-1] / ncells)
                            case "energy":
                                tenorm.append(float(words[-1]))
                                # apply norms here if not applied yet
                                if not teabs:
                                    for _res in terel:
                                        teabs.append(10**(_res) * tenorm[-1] / ncells)
                            case "dissipation":
                                sdnorm.append(float(words[-1]))
                                # apply norms here if not applied yet
                                if not sdabs:
                                    for _res in sdrel:
                                        sdabs.append(10**(_res) * sdnorm[-1] / ncells)
                    # "Time" can indicate the remaining lines starts with "n", if it's the
                    # time for Grid 1, and we're not interested in those.
                    case "Time":
                        # append compute time to tracker
                        tracker_ctime.append(float(words[-1]))

                        # append glvl to tracker
                        tracker_glvl.append(float(words[-2]))

                        # append sim time to tracker, and reset
                        tracker_stime.append(stime)

                        # if final "Time" (i.e. glvl 1), consume the iterator
                        if words[-2] == "1":
                            deque(iter_lines, maxlen=0)

    print()
    print("==============COMPUTE STATS================")
    print()
    print(f"In total:")
    print(f"   Number of grid levels: {len(tracker_glvl)}")
    print(f"   Total compute time: {sum(tracker_ctime)/60} min")
    print(f"   Total sim time: {tracker_stime[-1]} s")
    print(f"   Compute time per sim time: {sum(tracker_ctime)/tracker_stime[-1]}")
    print()
    print(f"Distributed onto grid levels:")
    for i, _ in enumerate(tracker_glvl):
        # select from the trackers
        _glvl = tracker_glvl[i]
        _ctime = tracker_ctime[i]
        if i == 0:
            _stime = tracker_stime[i]
        else:
            _stime = tracker_stime[i] - tracker_stime[i-1]

        # print the selected values
        print(f"    Grid level: {_glvl}")
        print(f"        Compute time: {_ctime/60} min")
        print(f"        Sim time: {_stime} s")
        print(f"        Compute time per sim time: {_ctime/_stime}")
        print()
    print("===========================================")

    axs[0].plot(n, urel, label="u")
    axs[0].plot(n, vrel, label="v")
    axs[0].plot(n, wrel, label="w")
    axs[0].plot(n, prel, label="p")
    axs[0].plot(n, terel, label="tke")
    axs[0].plot(n, sdrel, label="sd")
    axs[1].plot(n, np.log10(uabs))
    axs[1].plot(n, np.log10(vabs))
    axs[1].plot(n, np.log10(wabs))
    axs[1].plot(n, np.log10(pabs))
    axs[1].plot(n, np.log10(teabs))
    axs[1].plot(n, np.log10(sdabs))

    axs[0].set(
            #xlabel=r"$y/D$",
            ylabel=r"log(normalized res)",
            title=title,
        )
    axs[0].legend(ncols=6,loc='upper center', bbox_to_anchor=(0.5, -0.10))

    axs[1].set(
            xlabel=r"iterations",
            ylabel=r"log(res)",
        )
    #axs[1].legend()

    axs[0].grid(color="silver", linestyle="--", which="major")
    axs[0].grid(color="lightgrey", linestyle=":", which="minor")
    axs[1].grid(color="silver", linestyle="--", which="major")
    axs[1].grid(color="lightgrey", linestyle=":", which="minor")

    axs[0].set_title(f"{path}")


    plt.tight_layout()
#    plt.savefig("p6_spans.pdf")
    plt.show()




