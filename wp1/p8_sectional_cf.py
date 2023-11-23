from cycler import cycler
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, MultipleLocator
import numpy as np
from scipy.fft import ifft, fft, fftfreq
from _utils import read_py

if __name__ == "__main__":

    # ------------------------ #
    # INPUTS
    # ------------------------ #

    files_to_be_plotted = [
            "08_2D_8E6_DES",
            "09_2D_8E6_DES_TRANSITION",
            ]

    titles = [
            "2D, 8E6, IDDES",
            "2D, 8E6, IDDES, Drela-Giles Transition",
            ]

    # ------------------------ #
    # PLOTTING
    # ------------------------ #
    default_cycler = cycler(color=['r', 'g', 'b', 'y']) 
    plt.rc('axes', prop_cycle=default_cycler)

    fig, axs, = plt.subplots(
            len(files_to_be_plotted), 1,
            figsize=(5,8), 
            squeeze=False, 
            #subplot_kw={'projection': 'polar'}
            )

    # enable easy iterating through axes and labels
    axs_iter = iter(axs[:,0])
    title_iter = iter(titles)

    # define dummy variable for legend plotting
    _leg = None

    for file in files_to_be_plotted:
        # append filetype
        file = f"{file}/grid.1PY"

        # get the next active elements
        ax = next(axs_iter)
        title = next(title_iter)

        # read the py file
        slices, x, y, z, pr, sf = read_py(file)

        # get angle (cylindrical coordinates)
        theta = np.arctan(z / np.abs(x - 0.5))

        # shift it by +pi/2
        theta = theta + np.pi / 2.0

        # convert to degs...
        theta = theta * 180 / np.pi

        # amount of indices per slice = ncells of cylinder
        cidx = 256

        # get amount of slices
        nslices = int(slices[-1])

        # plot each slice ...
        for i in range(0,nslices+1):
            # compute index ranges for the slice
            i0 = i*cidx
            i1 = (i+1)*cidx

            # get upper and lower parts of the cylinder separately
            uppertheta = np.append(theta[3*i1//4:i1+1], theta[i0:i1//4+1])
            uppersf = np.append(sf[3*i1//4:i1+1], sf[i0:i1//4+1])
            lowertheta = theta[i1//4:3*i1//4+1]
            lowersf = sf[i1//4:3*i1//4+1]

            # PLOT
            ax.plot(uppertheta, uppersf, label="upper")
            ax.plot(lowertheta, lowersf, label="lower")


        # adjust cosmetics
        ax.set(
                xlabel=r"$\theta$ [deg]",
                ylabel=r"$c_f$",
                title=f"{title}",
            )

        # set xaxis in multiples of pi
        #ax.xaxis.set_major_formatter(FuncFormatter(
        #   lambda val,pos: '{:.0g}$\pi$'.format(val/np.pi) if val !=0 else '0'
        #))
        #ax.xaxis.set_major_locator(MultipleLocator(base=0.25*np.pi))

        ax.grid(color="silver", linestyle="--", which="major")
        ax.grid(color="lightgrey", linestyle=":", which="minor")

        # include a legend only on the first plot
        if not _leg:
            _leg = ax.legend(ncols=1,loc='best')
        
        # disable grid
        #ax.grid(False)

    plt.tight_layout()
    #plt.savefig("p6_sectional_phases.pdf")
    plt.show()
