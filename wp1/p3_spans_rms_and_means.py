from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np

#plt.rcParams.update({
#    "text.usetex": True,
#    "font.family": "Helvetica",
#    "axes.prop_cycle": cycler(color=["#3288BD","#66C2A5","#D53E4F"],linestyle=["-","--",":"]),
#    "axes.facecolor": (1.0, 1.0, 1.0, 1.0),
#    "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),
#})

def plot_span(filepath: str, axs, label=[]):
    data = np.loadtxt(filepath)

    # The .1HY file has the following columns:
    #    nstep (x1 fx fy fz) (x2 fx fy fz) ... (xn fx fy fz)
    #
    # I.e. every set of four columns (past the first) is a data-point.
    
    iterations = data[:,0]
    positions = data[:, 1::4]
    fx = data[:, 2::4]
    fy = data[:, 3::4]
    fz = data[:, 4::4]

    if not label:
        label = filepath

    # normalize
    fx = 2.0*fx
    fy = 2.0*fy
    fz = 2.0*fz

    axs[0].plot(fx.std(axis=0)[1:], positions[0,1:], label=label)
    axs[1].plot(fz.mean(axis=0)[1:], positions[0,1:], label=label)


if __name__ == "__main__":

    #plt.style.use("ggplot")

    fig, axs = plt.subplots(1, 2, sharey=True, figsize=(10,6))

    # Plot 2D comparison
    data = np.loadtxt("99_2d_stationary/grid.1force")
    lift = data[-5000:,5]
    drag = data[-5000:,4]

    # normalize
    lift = 2.0*lift
    drag = 2.0*drag

    # mean and std
    lift = lift.std()
    drag = drag.mean()

    axs[0].plot([lift, lift], [0, 8], label=r"URANS (2D)")
    axs[1].plot([drag, drag], [0, 8], label=r"URANS (2D)")
    
    plot_span("09_urans_with_respecifybc/grid.1HY", axs, r"URANS (8D)")
    plot_span("10_urans_with_respecifybc_with_512D_mesh/grid.1HY", axs, r"URANS (512D)")
    #plot_span("16_3e6_old_turb/grid.1HY", axs, r"te_inlet=1.d-2, omega_inlet=1.d6 (Re=3.6e6)")
    #plot_span("15_3e6_new_turb/grid.1HY", axs, r"te_inlet=1.d-8, omega_inlet=1.d1 (Re=3.6e6)")

    #axs[1].plot([0.42, 0.42], [0, 8], label=r"Viré et al (Re$=3.6\times10^6$)")

    axs[0].set(
            xlabel=r"rms($c_l$)",
            ylabel=r"$y/D$",
            #title=r"Spanwise lift and drag contributions",
        )
    #axs[0].legend(ncols=4,loc='upper center', bbox_to_anchor=(0.5, -0.05))
    axs[1].legend(ncols=1,loc='upper center', bbox_to_anchor=(0.5, -0.10))
    #axs[0].grid(color="gainsboro", linestyle="--")

    axs[1].set(
            xlabel=r"$\overline{c_d}$",
            #ylabel=r"$y/D$",
        )
    #axs[1].legend()
    #axs[1].grid(color="gainsboro", linestyle="--")

    axs[0].grid(color="silver", linestyle="--", which="major")
    axs[0].grid(color="lightgrey", linestyle=":", which="minor")
    axs[1].grid(color="silver", linestyle="--", which="major")
    axs[1].grid(color="lightgrey", linestyle=":", which="minor")

    plt.tight_layout()
#    plt.savefig("p6_spans.pdf")
    plt.show()
