
from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple
from scipy.fft import fft, fftfreq
from scipy.signal import detrend, welch
from _utils import read_force

if __name__ == "__main__":

    # ------------------------ #
    # INPUTS
    # ------------------------ #

    files_to_be_plotted = [
            #"04_des_with_adjusted_input/grid.1HY",
            #"07_urans_with_512D_mesh/grid.1HY",
            #"08_des_with_respecifybc/grid.1force",
            #"09_urans_with_respecifybc/grid.1force",
            #"17_matching_turb_constant_dt/grid.1force",
            "18_des_5e6/grid.1force",
            "21_urans_5e6/grid.1force",
            ]

    titles = [
            #"DES (no respecifybc)", 
            #"URANS (512D)", 
            #"IDDES", 
            #"URANS",
            #"IDDES (Adj. Turbulence)",
            ]

    labels = [
            "IDDES",
            "URANS",
            ]

    timestep = 6e-3
    time_to_be_skipped = 100

    # select either fft or welch as analytic method
    signal_method = "fft"

    # ------------------------ #
    # PLOTTING
    # ------------------------ #

    fig, axs, = plt.subplots(1, 1,
            figsize=(5,4), 
            squeeze=False, 
            )

    ax = axs[0,0]


    labels = iter(labels)


    for file in files_to_be_plotted:
        label = next(labels)

        # iterations, time, fx, fy, fz
        _, time, lift, _, drag = read_force(file)

        # normalize lift and drag
        lift = 2.0 * lift / 8
        drag = 2.0 * drag / 8

        # compute window
        tdif = np.abs(time - time_to_be_skipped)
        nwindow = tdif.argmin()

        # apply the window
        _lift = lift[nwindow:]
        _drag = drag[nwindow:]
        _time = time[nwindow:]

    
        # run signal analysis and plot results
        n = len(_time)
        lift_f = fft(_lift)
        drag_f = fft(_drag)
        freq = fftfreq(n, timestep)[:n//2]

        # filter out small amplitudes
        threshold = np.max(np.abs(lift_f)) / 1e-5
        bool_array = np.isclose(np.abs(lift_f), np.zeros(lift_f.shape), atol=threshold)

        lift_f = lift_f * bool_array

        # Find maximum frequency (and print to check ...)
        freqid = np.abs(lift_f).argmax()
        print(f"f = {freq[freqid]}")

        # PLOT
        ax.loglog(freq, 2.0/n * np.abs(lift_f[0:n//2]), '-', label=label)
        ax.scatter(freq[freqid], 2.0/n * np.abs(lift_f[freqid]), color='k', zorder=0)
        #ax.loglog(freq, 2.0/n * np.abs(drag_f[0:n//2]), '-', label="Drag")
        ax.text(1.2 * freq[freqid], 2.0/n * np.abs(lift_f[freqid]), f"St={freq[freqid]:.2f}")

        ax.set(
            xlim=[1e-2, 1e2],
            xlabel=r"$f$ [Hz]",
            ylabel=r"$A(c_l)$ [-]",
        )

        # adjust cosmetics
       # ax1.grid(color="silver", linestyle="--", which="major")
       # ax1.grid(color="lightgrey", linestyle=":", which="minor")
       # ax2.grid(color="silver", linestyle="--", which="major")
       # ax2.grid(color="lightgrey", linestyle=":", which="minor")

        ax.grid(which="both", visible=None, color="w")
        ax.legend()


    plt.tight_layout()
    plt.savefig("plot_scientific_writing.pdf")
    plt.show()
