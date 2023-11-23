from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import numpy as np
from scipy.fft import ifft, fft, fftfreq
from _utils import read_hy

if __name__ == "__main__":

    # ------------------------ #
    # INPUTS
    # ------------------------ #

    files_to_be_plotted = [
            "02_8D_5E6_DES",
            "05_4D_5E6_DES",
            "06_2D_5E6_DES",
            ]

    titles = [
            "8D, 5E6, IDDES",
            "4D, 5E6, IDDES",
            "2D, 5E6, IDDES",
            ]

    timestep = 6e-3

    time_to_be_skipped = 100

    # ------------------------ #
    # PLOTTING
    # ------------------------ #

    fig, axs, = plt.subplots(
            len(files_to_be_plotted), 1,
            figsize=(5,8), 
            squeeze=False, 
            #subplot_kw={'projection': 'polar'}
            )

    # enable easy iterating through axes and labels
    axs_iter = iter(axs[:,0])
    title_iter = iter(titles)

    # fix positions ...
    ylim_iter = iter([8.0, 4.0, 2.0])

    # define dummy variable for legend plotting
    _leg = None

    for file in files_to_be_plotted:
        # append filetype
        file = f"{file}/grid.1HY"

        # get the next active elements
        ax = next(axs_iter)
        title = next(title_iter)
        ylim = next(ylim_iter)

        # iterations, pos, fx, fy, fz
        iterations, positions, lift, _, drag = read_hy(file)

        # get length of spanwise element
        dy = positions[0,1] - positions[0,0]

        # normalize lift and drag
        lift = 2.0 * lift / dy
        drag = 2.0 * drag / dy

        # compute time from iterations
        time = iterations * timestep

        # filter transients , ,
        tdif = np.abs(time - time_to_be_skipped)
        nwindow = tdif.argmin()
    
        # prepare empty array
        phase_at_max_amp = []

        # compute and plot ffts for all sections
        for sid, _ in enumerate(positions[0,:]):
            # apply the window
            _lift = lift[nwindow:, sid]
            _drag = drag[nwindow:, sid]
            _time = time[nwindow:]

            # compute and apply means as detrend
            _lift = np.mean(_lift) - _lift
            _drag = np.mean(_drag) - _drag
            
            # FFTs
            _dt = _time[1] - _time[0]
            n = len(_time)
            lift_fft = fft(_lift)
            drag_fft = fft(_drag)
            freq = fftfreq(n, _dt)[:n//2]

            # PHASE
            # filter out small amplitudes
            threshold = np.max(np.abs(lift_fft)) / 1e-5
            bool_array = np.isclose(np.abs(lift_fft), np.zeros(lift_fft.shape), atol=threshold)

            lift_fft = lift_fft * bool_array

            # filter out near-rigid frequncies
            threshold = 4e-1
            bool_array = freq > threshold

            lift_fft = lift_fft[:n//2] * bool_array

            # compute phases
            phase = np.arctan2(lift_fft.imag, lift_fft.real)

            # Find maximum frequency (and print to check ...)
            freqid = np.abs(lift_fft).argmax()
            print(f"f = {freq[freqid]}")

            # Add phase at max frequency to array (in rads)
            phase_at_max_amp.append(phase[freqid])# * 180.0 / np.pi)


        # PLOT
        ax.plot(phase_at_max_amp, positions[0,:],'ok', markerfacecolor="white")


        # adjust cosmetics
        ax.set(
                xlim=[-np.pi, np.pi],
                ylim=[0, ylim],
                xlabel=r"$\phi$",
                ylabel=r"$y/D$",
                title=f"{title}",
            )

        # set xaxis in multiples of pi
        ax.xaxis.set_major_formatter(FuncFormatter(
           lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0'
        ))
        ax.xaxis.set_major_locator(MultipleLocator(base=0.25*np.pi))

        ax.grid(color="silver", linestyle="--", which="major")
        ax.grid(color="lightgrey", linestyle=":", which="minor")

        # include a legend only on the first plot
        if not _leg:
            _leg = ax.legend(ncols=4,loc='upper center', bbox_to_anchor=(0.5, -0.05))
        
        # disable grid
        #ax.grid(False)

    plt.tight_layout()
    plt.savefig("p6_sectional_phases.pdf")
    plt.show()
