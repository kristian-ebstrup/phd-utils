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
            # "07_8D_GRID_DEPENDENCY/grid.1force",
            # "07_8D_GRID_DEPENDENCY/grid.2force",
            "08_2D_8E6_DES/grid.1force",
            "09_2D_8E6_DES_TRANSITION/grid.1force",
            ]

    titles = [
            "No Transition",
            "Transition",
            ]

    timestep = 6e-3
    time_to_be_skipped = 100

    # select either fft or welch as analytic method
    signal_method = "fft"

    # ------------------------ #
    # PLOTTING
    # ------------------------ #

    fig1, axs1, = plt.subplots(
            len(files_to_be_plotted), 1,
            figsize=(5,8), 
            squeeze=False, 
            )

    fig2, axs2, = plt.subplots(
            len(files_to_be_plotted), 1,
            figsize=(5,8), 
            squeeze=False, 
            )

    # enable easy iterating through axes and labels
    axs1_iter = iter(axs1[:,0])
    axs2_iter = iter(axs2[:,0])
    title_iter = iter(titles)

    # define dummy variable for legend plotting
    _leg = None

    for file in files_to_be_plotted:
        # append filetype
        #file = f"{file}/grid.1force"

        # get the next active elements
        ax1 = next(axs1_iter)
        ax2 = next(axs2_iter)
        title = next(title_iter)

        # iterations, time, fx, fy, fz
        _, time, lift, _, drag = read_force(file)

        # normalize lift and drag
        lift = 2.0 * lift / 2
        drag = 2.0 * drag / 2

        # compute window
        tdif = np.abs(time - time_to_be_skipped)
        nwindow = tdif.argmin()

        # apply the window
        _lift = lift[nwindow:]
        _drag = drag[nwindow:]
        _time = time[nwindow:]

        # compute and apply means as detrend
        #_lift = np.mean(_lift) - _lift
        #_drag = np.mean(_drag) - _drag
    
        # run signal analysis and plot results
        match signal_method:

            case "fft":
                # Mean development...
                mu_lift = [np.mean(_lift[0:i]) for i, _ in enumerate(_lift)]
                mu_drag = [np.mean(_drag[0:i]) for i, _ in enumerate(_drag)]

                n = len(_time)
                lift_f = fft(_lift)
                drag_f = fft(_drag)
                freq = fftfreq(n, timestep)[:n//2]

                # PLOT
                ax1.plot(_time, _lift, label=r"$c_l$")
                ax1.plot(_time, _drag, label=r"$c_d$")
                ax1.plot(_time, mu_lift, label=r"$\overline{c_l}(t)$")
                ax1.plot(_time, mu_drag, label=r"$\overline{c_d}(t)$")
                ax2.loglog(freq, 2.0/n * np.abs(lift_f[0:n//2]), 'k-', label="Lift")
                ax2.loglog(freq, 2.0/n * np.abs(drag_f[0:n//2]), '-', color="darkgrey", label="Drag")


                # filter out small amplitudes
                threshold = np.max(np.abs(lift_f)) / 1e-5
                bool_array = np.isclose(np.abs(lift_f), np.zeros(lift_f.shape), atol=threshold)

                lift_f = lift_f * bool_array

                # also filter out near-rigid frequncies
                threshold = 3e-1
                bool_array = freq > threshold

                lift_f = lift_f[0:n//2] * bool_array

                # Find maximum frequency (and print to check ...)
                freqid = np.abs(lift_f).argmax()
                print(f"f = {freq[freqid]}")

                ax2.scatter(freq[freqid], 2.0/n * np.abs(lift_f[freqid]), color='k', zorder=0)
                #ax.loglog(freq, 2.0/n * np.abs(drag_f[0:n//2]), '-', label="Drag")
                ax2.text(1.2 * freq[freqid], 2.0/n * np.abs(lift_f[freqid]), f"St={freq[freqid]:.2f}")


                # Do the same for drag ...
                threshold = np.max(np.abs(drag_f)) / 1e-5
                bool_array = np.isclose(np.abs(drag_f), np.zeros(drag_f.shape), atol=threshold)

                drag_f = drag_f * bool_array

                # also filter out near-rigid frequncies
                threshold = 3e-1
                bool_array = freq > threshold

                drag_f = drag_f[0:n//2] * bool_array

                freqid = np.abs(drag_f).argmax()
                print(f"f = {freq[freqid]}")

                ax2.scatter(freq[freqid], 2.0/n * np.abs(drag_f[freqid]), color='darkgrey', zorder=1)
                #ax.loglog(freq, 2.0/n * np.abs(drag_f[0:n//2]), '-', label="Drag")
                ax2.text(1.2 * freq[freqid], 2.0/n * np.abs(drag_f[freqid]), f"St={freq[freqid]:.2f}", color='darkgrey')

                ax1.set(
                    #xlim=[0, 1],
                    xlabel=r"$tU/D$",
                    ylabel=r"normalized loads",
                    title=f"{title}",
                )

                ax2.set(
                    xlim=[1e-2, 1e2],
                    xlabel=r"$f$ [Hz]",
                    ylabel=r"$A$",
                    title=f"{title}",
                )


            case "welch":
                sampling_freq = 1 / timestep
                freq, lift_psd = welch(_lift, sampling_freq)
                freq, drag_psd = welch(_drag, sampling_freq)

                # PLOT
                ax.loglog(freq, lift_psd, '-', label="Lift")
                ax.loglog(freq, drag_psd, '-', label="Drag")
                ax.set(
                    #xlim=[0, 1],
                    xlabel=r"$f$ [Hz]",
                    ylabel=r"PSD [1/Hz]",
                    title=f"{title}",
                )

        # adjust cosmetics
        ax1.grid(color="silver", linestyle="--", which="major")
        ax1.grid(color="lightgrey", linestyle=":", which="minor")
        ax2.grid(color="silver", linestyle="--", which="major")
        ax2.grid(color="lightgrey", linestyle=":", which="minor")

        # include a legend only on the first plot
        if not _leg:
            _leg = ax1.legend(ncols=1,loc='upper right')
            _leg = ax2.legend(ncols=1,loc='upper right')
        

    plt.tight_layout()
    #plt.savefig("p2_integrated_ffts.pdf")
    plt.show()
