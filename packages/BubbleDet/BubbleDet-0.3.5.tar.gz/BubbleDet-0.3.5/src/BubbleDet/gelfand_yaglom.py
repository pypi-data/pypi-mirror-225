import sys
import numpy as np  # arrays and maths
from scipy.integrate import solve_ivp  # integrators
from scipy import special  # special functions
from .helpers import derivative  # derivatives for callable functions


def findGelfandYaglomTl(config, l, rmin=1e-4, gy_tol=1e-6):
    r""":math:`T=\psi/\psi_{\rm FV}` for given :math:`l`

    Full docs in BubbleDet.py.
    """
    # set up
    m0 = config.m_W_meta
    if config.m_max <= 0:
        R_scale = config.r_mid
    else:
        R_scale = min(1 / config.m_max, config.r_mid)
    R_min = rmin * R_scale
    R_max = config.R[-1]
    dim = config.dim
    DW_interp = config.Delta_W_interp
    # Taylor expanding for first step, from 0 to R_min
    phi0 = config.Phi[0]
    dV0 = config.dV(phi0)
    dW_Phi0 = derivative(
        config.W_Phi, phi0, dx=config.phi_eps
    )
    d2T0 = DW_interp(0) / (dim + 2 * l)
    d2W0 = dV0 / dim * dW_Phi0
    d4T0 = (3 / (dim + 2 * l + 2)) * (
        -4 * m0**2 * DW_interp(0) / (dim + 2 * l) ** 2
        + DW_interp(0) ** 2 / (dim + 2 * l)
        + d2W0
    )
    T0_R_min = 1 + 1 / 2 * d2T0 * R_min**2 + 1 / 24 * d4T0 * R_min**4
    T1_R_min = 0 + d2T0 * R_min + 1 / 6 * d4T0 * R_min**3
    # solving initial value problem
    sol = solve_ivp(
        lambda R, T: [
            T[1],
            -_UFactor(dim, l, m0, R) * T[1] + DW_interp(R) * T[0],
        ],
        [R_min, R_max],
        [T0_R_min, T1_R_min],
        method="RK45",
        rtol=gy_tol,
        max_step=0.2 * R_scale,
    )  # methods: RK45, RK23, DOP853, Radau, BDF, LSODA
    if sol["status"] != 0:
        print(
            "solve_ivp integration error, status =",
            sol["status"],
            file=sys.stderr,
        )
        return np.nan, np.nan
    # asigning solution
    RT = sol["t"]
    T = sol["y"][0, :]
    TD = sol["y"][1, :] #the derivative at the outer boundary
    res = T[-1]
    # estimating error in solution
    err = max(
        R_scale * abs(T[-1] - T[-2]) / abs(RT[-1] - RT[-2]),
        gy_tol * abs(res),
        abs(res) / len(config.R) ** 4,
        abs(res) * (R_min / R_scale) ** 5,
    )
    return res, err, TD[-1]


def findGelfandYaglomFl(config, l, rmin=1e-4, gy_tol=1e-6):
    r""":math:`F=\log(\psi/\psi_{\rm FV})` for given :math:`l`

    Full docs in BubbleDet.py.
    """
    # set up
    m0 = config.m_W_meta
    if config.m_max <= 0:
        R_scale = config.r_mid
    else:
        R_scale = min(1 / config.m_max, config.r_mid)
    R_min = rmin * R_scale
    R_max = config.R[-1]
    dim = config.dim
    DW_interp = config.Delta_W_interp
    # Taylor expanding for first step, from 0 to R_min
    phi0 = config.Phi[0]
    dV0 = config.dV(phi0)
    dW_Phi0 = derivative(
        config.W_Phi, phi0, dx=config.phi_eps
    )
    d2F0 = DW_interp(0) / (dim + 2 * l)
    d2W0 = dV0 / dim * dW_Phi0
    d4F0 = (3 / (dim + 2 * l + 2)) * (
        -4 * m0**2 * DW_interp(0) / (dim + 2 * l) ** 2
        - 2 * DW_interp(0) ** 2 / (dim + 2 * l) ** 2
        + d2W0
    )
    F0_R_min = 1 / 2 * d2F0 * R_min**2 + 1 / 24 * d4F0 * R_min**4
    F1_R_min = d2F0 * R_min + 1 / 6 * d4F0 * R_min**3
    # solving initial value problem
    sol = solve_ivp(
        lambda R, F: [
            F[1],
            -_UFactor(dim, l, m0, R) * F[1] - F[1] ** 2 + DW_interp(R),
        ],
        [R_min, R_max],
        [F0_R_min, F1_R_min],
        method="RK45",
        rtol=gy_tol,
        max_step=0.2 * R_scale,
    )  # methods: RK45, RK23, DOP853, Radau, BDF, LSODA
    if sol["status"] != 0:
        print(
            "solve_ivp integration error, status =",
            sol["status"],
            file=sys.stderr,
        )
        return np.nan, np.nan
    # asigning solution
    RF = sol["t"]
    F = sol["y"][0, :]
    res = F[-1]
    # estimating error in solution
    err = max(
        R_scale * abs(F[-1] - F[-2]) / abs(RF[-1] - RF[-2]),
        gy_tol * abs(res),
        abs(res) / len(config.R) ** 4,
        abs(res) * (R_min / R_scale) ** 5,
    )
    return res, err

def _UFactor(dim, l, m, r):
    r"""
    :math:`U` factor in ode for :math:`T=\psi/psi_{\rm FV}``.
        .. math::
            T'' + U T' - W T = 0

    Parameters
    ----------
    dim : int
        Dimension.
    l : int
        Orbital quantum number.
    m : float
        Mass.
    r : float
        Radial coordinate.

    Returns
    -------
    U : float
        The value of :math:`U` evaluated at the given radius.
    """
    x = m * r
    if dim == 1:
        if x < 1e-12:
            return 2 / r
        else:
            return 2 * m / np.tanh(x)
    elif x < 1e-12:
        return (dim - 1 + 2 * l) / r
    elif x**2 < 0.01 * (2 * l**2 + 5 * l + 3):
        return (2 * m) * (
            ((-1 + dim) / 2 + l) / x
            + x / (dim + 2 * l)
            - x**3 / ((dim + 2 * l) ** 2 * (2 + dim + 2 * l))
            + (2 * x**5)
            / ((dim + 2 * l) ** 3 * (2 + dim + 2 * l) * (4 + dim + 2 * l))
            - ((12 + 5 * dim + 10 * l) * x**7)
            / (
                (dim + 2 * l) ** 4
                * (2 + dim + 2 * l) ** 2
                * (4 + dim + 2 * l)
                * (6 + dim + 2 * l)
            )
        )
    else:
        return (2 * m) * (
            (l + (dim - 1) / 2) / x
            + special.iv(dim / 2 + l, x) / special.iv(dim / 2 - 1 + l, x)
        )
