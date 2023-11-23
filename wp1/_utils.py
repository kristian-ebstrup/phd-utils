# A collection of (local) utility scripts for reading force files.
import numpy as np
from typing import Tuple

def read_force(filepath: str) -> Tuple[np.ndarray, ...]:
    # Reads a force file, and outputs the results in a tuple of ndarrays.
    # 
    # Depending on whether it's a 2D or 3D force file, it sas the following columns:
    #    
    #    :: 2D ::
    #    nstep time fdx fdy fx fy mz
    #
    #    :: 3D ::
    #    nstep time fdx fdy fdz fx fy fz mx my mz mdx mdy mdz
    #
    # The code automatically selects based on the amount of columns.

    data = np.loadtxt(filepath)

    iterations = data[:,0]
    time = data[:,1]

    match data.shape[1]:
        case 7:
            fx = data[:,4]
            fy = data[:,5]

            return (iterations, time, fx, fy)
        case 14:
            fx = data[:,5]
            fy = data[:,6]
            fz = data[:,7]

            return (iterations, time, fx, fy, fz)

    raise ValueError(
            f"Unknown file structure! Expected 7 or 14 columns, found {data.shape[1]}"
            )


def read_hy(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # Reads a HY file, and outputs the results in a tuple of ndArrays.
    # 
    # The .*HY file has the following columns:
    #    nstep (x1 fx fy fz) (x2 fx fy fz) ... (xn fx fy fz)
    #
    # I.e. every set of four columns (past the first) is a data-point.

    data = np.loadtxt(filepath)

    iterations = data[:,0]
    positions = data[:, 1::4]
    fx = data[:, 2::4]
    fy = data[:, 3::4]
    fz = data[:, 4::4]

    return (iterations, positions, fx, fy, fz)


def read_py(filepath: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    # Reads a PY file, and outputs the results in a tuple of ndArrays.
    # 
    # The .*PY file has the following columns:
    #    slice_nr, x, y, z, pres, fric, gamma, yp, pres_ave, fric_ave, gamma_ave, yp_ave
    #
    # I.e. every line is a separate point.

    data = np.loadtxt(filepath)

    slice_nr = data[:,0]
    x = data[:,1]
    y = data[:,2]
    z = data[:,3]
    pr = data[:,5]
    sf = data[:,5]

    return (slice_nr, x, y, z, pr, sf)
