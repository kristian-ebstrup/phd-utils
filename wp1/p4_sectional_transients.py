from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple
from _utils import read_hy

if __name__ == "__main__":

    # ------------------------ #
    # INPUTS
    # ------------------------ #

    files_to_be_plotted = [
            #"02_8D_5E6_DES",
            #"05_4D_5E6_DES",
            #"06_2D_5E6_DES",
            "08_2D_8E6_DES",
            "09_2D_8E6_DES_TRANSITION",
            ]

    titles = [
            #"8D, 5E6, IDDES",
            #"4D, 5E6, IDDES",
            "2D, 8E6, No Transition",
            "2D, 8E6, Transition",
            ]

    timestep = 6e-3

    # ------------------------ #
    # PLOTTING
    # ------------------------ #
    figh = len(files_to_be_plotted)

    fig, axs, = plt.subplots(
            len(files_to_be_plotted), 1,
            figsize=(8.4,3 * figh), 
            squeeze=False,
            )

    # enable easy iterating through the axes and titles
    ax_iter = iter(axs[:,0])
    title_iter = iter(titles)

    # fix positions ...
    ylim_iter = iter([2.0, 2.0])

    cs = None
    for file in files_to_be_plotted:
        # append filetype
        file = f"{file}/grid.1HY"

        # get the next active axis and title
        ax = next(ax_iter)
        title = next(title_iter)
        ylim = next(ylim_iter)

        # iterations, pos, fx, fy, fz
        iterations, positions, lift, _, drag = read_hy(file)

        # get length of spanwise element
        dy = positions[0,1] - positions[0,0]

        # normalize lift and drag (note: force per unit span)
        lift = 2.0 * lift / dy / 8
        drag = 2.0 * drag / dy / 8
        
        print(np.mean(np.mean(drag)))


        # compute time from iterations
        time = iterations * timestep

        # prepare meshgrid
        x = time
        y = positions[0,:]
        x, y = np.meshgrid(x, y)
        z = lift.T

        # plot meshgrid
        cvals = ax.contourf(x, y, z, cmap="RdBu", extend="both")
        cbar = fig.colorbar(cvals, format="%1.1f", ax=ax)
        cbar.ax.set_ylabel(r"$c_l$")

        # adjust cosmetics
        ax.set(
                xlabel=r"$tU/D$",
                ylabel=r"$y/D$",
                xlim=[100, 140],
                ylim=[0, ylim],
                title=f"{title}",
            )

        # disable grid
        ax.grid(False)

    #axs[0,0].set(xlabel=None)

    plt.tight_layout()
    plt.savefig("p4_sectional_transients.pdf")
    plt.show()
