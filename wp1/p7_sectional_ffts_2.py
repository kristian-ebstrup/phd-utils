from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import ifft, fft, fftfreq
from _utils import read_hy

if __name__ == "__main__":

    # ------------------------ #
    # INPUTS
    # ------------------------ #

    files_to_be_plotted = [
            #"04_des_with_adjusted_input/grid.1HY",
            #"07_urans_with_512D_mesh/grid.1HY",
            "08_des_with_respecifybc/grid.1HY",
            "09_urans_with_respecifybc/grid.1HY",
            #"15_3e6_new_turb/grid.1HY",
            #"16_3e6_old_turb/grid.1HY",
            ]

    titles = [
            #"DES (no respecifybc)", 
            #"URANS (512D)", 
            "DES", 
            "URANS",
            #"alternative turb",
            #"default turb",
            ]

    timestep = 6e-3

    time_to_be_skipped = 50

    # ------------------------ #
    # PLOTTING
    # ------------------------ #

    fig, axs, = plt.subplots(
            2, 1,
            figsize=(6,6), 
            squeeze=False, 
            sharex=True,
            )

    # enable easy iterating through axes and labels
    axs_iter = iter(axs[:,0])
    title_iter = iter(titles)

    # define dummy variable for legend plotting
    _leg = None

    for file in files_to_be_plotted:
        # get the next active elements
        ax = next(axs_iter)
        title = next(title_iter)

        # iterations, pos, fx, fy, fz
        iterations, positions, lift, _, drag = read_hy(file)


        # get length of spanwise element
        dy = positions[0,1] - positions[0,0]

        # normalize lift and drag
        lift = 2.0 * lift / dy
        drag = 2.0 * drag / dy

        # compute time from iterations
        time = iterations * timestep

        # filter transients
        tdif = np.abs(time - time_to_be_skipped)
        nwindow = tdif.argmin()

        # prepare 
    
        # compute ffts for all sections

        # apply the window
        _lift = lift[nwindow:, :]
        _drag = drag[nwindow:, :]
        _time = time[nwindow:]

            
        # FFTs
        _dt = _time[1] - _time[0]
        n = len(_time)
        
        freq_fft = fftfreq(n, _dt)[:n//2]
        lift_fft = np.empty(_lift.shape, dtype=np.complex_)
        drag_fft = np.empty(_drag.shape, dtype=np.complex_)

        for sid in range(_lift.shape[1]):
            # detrend
            _lift[:, sid] = np.mean(_lift[:, sid]) - _lift[:, sid]
            _drag[:, sid] = np.mean(_drag[:, sid]) - _drag[:, sid]

            # compute ffts
            lift_fft[:, sid] = fft(_lift[:, sid])
            drag_fft[:, sid] = fft(_drag[:, sid])


        # identify largest amplitudes, and their frequency, and plot that
        # frequency for all sections

        _temp = 2.0/n * np.abs(lift_fft[0:n//2])
        _idx = _temp.argsort(axis=0)

        # select frequencies ...
        freq_idx = _idx[-3:,0]

        # add nearest freq to St at 0.33Hz (URANS)
        #st_idx = np.array([abs(_f - 0.33) for _f in freq_fft]).argmin()
        #freq_idx = np.append(freq_idx, st_idx)

        # PLOT
        for fid in freq_idx:
            ax.plot(2.0/n * np.abs(lift_fft[fid, :]), positions[0,:], label=r"$\omega/\omega_0$="+f"{freq_fft[fid]:.2f}")


        # adjust cosmetics
        ax.set(
                xlabel=r"$A$ ($c_l$)",
                ylabel=r"$y/D$",
                title=f"{title}",
            )

        ax.grid(color="silver", linestyle="--", which="major")
        ax.grid(color="lightgrey", linestyle=":", which="minor")

        # include a legend only on the first plot
        if not _leg:
            _leg = ax.legend(ncols=4,loc='upper center', bbox_to_anchor=(0.5, -0.05))
        
        # disable grid
        #ax.grid(False)

    plt.tight_layout()
#    plt.savefig("p6_spans.pdf")
    plt.show()
