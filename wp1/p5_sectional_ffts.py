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
            #"08_des_with_respecifybc/grid.1HY",
            #"09_urans_with_respecifybc/grid.1HY",
            #"17_matching_turb_constant_dt/grid.1HY",
            "21_urans_5e6/grid.2HY",
            "18_des_5e6/grid.2HY",
            #"20_urans_1e5/grid.1HY",
            #"19_des_1e5/grid.1HY",
            ]

    sections_to_be_plotted = [25, 50, 75]

    titles = [
            #"DES (no respecifybc)", 
            #"URANS (512D)", 
            #"DES", 
            #"URANS",
            #"DES (Adj. Turb)",
            "URANS (Re=5e6)",
            "IDDES (Re=5e6)",
            "URANS (Re=1e5)",
            "IDDES (Re=1e5)",
            ]

    timestep = 6e-3

    time_to_be_skipped = 20

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
            sharex=True,
            )

    # enable easy iterating through axes and labels
    axs1_iter = iter(axs1[:,0])
    axs2_iter = iter(axs2[:,0])
    title_iter = iter(titles)

    # define dummy variable for legend plotting
    _leg = None

    # define dummy variable for limits
    _lim = None

    for file in files_to_be_plotted:
        # get the next active elements
        ax1 = next(axs1_iter)
        ax2 = next(axs2_iter)
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
    
        # compute and plot ffts for all input sections
        for sid in sections_to_be_plotted:        
            # apply the window
            _lift = lift[nwindow:, sid]
            _drag = drag[nwindow:, sid]
            _time = time[nwindow:]

            # compute and apply means as detrend
            #_lift = np.mean(_lift) - _lift
            #_drag = np.mean(_drag) - _drag
            
            # FFTs
            _dt = _time[1] - _time[0]
            n = len(_time)
            lift_f = fft(_lift)
            drag_f = fft(_drag)
            freq = fftfreq(n, _dt)[:n//2]

            # Mean development...
            mu_lift = [np.mean(_lift[0:i]) for i, _ in enumerate(_lift)]
            mu_drag = [np.mean(_drag[0:i]) for i, _ in enumerate(_drag)]

            # PLOT
            ax1.plot(_time, _lift, label=r"$c_l$")
            ax1.plot(_time, _drag, label=r"$c_d$")
            ax1.plot(_time, mu_lift, ':', label=r"$\overline{c_l}(t)$")
            ax1.plot(_time, mu_drag, ':', label=r"$\overline{c_d}(t)$")
            ax2.loglog(freq, 2.0/n * np.abs(lift_f[0:n//2]), '-', markerfacecolor="None", label=f"Y={positions[0,sid]:.2f}")


        # adjust cosmetics
        ax1.set(
                #xlim=[0, 1],
                xlabel=r"$tU/D$",
                ylabel=r"normalized forces",
                title=f"{title}",
            )
        ax2.set(
                #xlim=[0, 1],
                xlabel=r"$f$",
                ylabel=r"$A$",
                title=f"{title}",
            )

        ax1.grid(color="silver", linestyle="--", which="major")
        ax1.grid(color="lightgrey", linestyle=":", which="minor")
        ax2.grid(color="silver", linestyle="--", which="major")
        ax2.grid(color="lightgrey", linestyle=":", which="minor")

        # include a legend only on the first plot
        if not _leg:
            _leg = ax1.legend(ncols=4,loc='upper center', bbox_to_anchor=(0.5, 1.20))
            _leg = ax2.legend(ncols=4,loc='upper center', bbox_to_anchor=(0.5, 1.20))
        
        if not _lim:
            _lim = ax1.get_xlim()
        else:
            ax1.set_xlim(_lim)

        # disable grid
        #ax.grid(False)

    plt.tight_layout()
#    plt.savefig("p6_spans.pdf")
    plt.show()
