import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plot_hy(filepath: str):
    # Reads the timesteps in a .1HY file, and plots them in an animation.
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

    plt.style.use("ggplot")

    fig, ax = plt.subplots()
    l1, = ax.plot(fx[0,:], positions[0, :], label="fx")
    l2, = ax.plot(fy[0,:], positions[0, :], label="fy")
    l3, = ax.plot(fz[0,:], positions[0, :], label="fz")
    ax.legend()
    ax.grid("gainsboro")


    def animate(i):
        l1.set_xdata(fx[i,:])
        l2.set_xdata(fy[i,:])
        l3.set_xdata(fz[i,:])
        return l1, l2, l3

    ani = animation.FuncAnimation(
            fig, animate, interval=20, blit=True, save_count=50)

    plt.show()



if __name__ == "__main__":
    plot_hy("01_urans/grid.1HY")
