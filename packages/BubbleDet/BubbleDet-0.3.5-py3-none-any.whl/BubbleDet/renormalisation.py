import numpy as np  # arrays and maths
from scipy import special # integrator, special functions
from .helpers import simpson  # integrator
from cosmoTransitions.helper_functions import deriv14  # derivatives for arrays


def findRenormalisationTerm(config):
    r"""Renormalisation scale dependent part of determinant

    Full docs in BubbleDet.py.
    """
    dim = config.dim
    R = config.R
    DW = config.Delta_W
    m0 = config.m_W_meta
    dWR = deriv14(DW, R)
    mu = config.renormalisation_scale


    if dim % 2 == 1:
        # no renormalisation in odd dimensions
        return 0, 0, 0
    elif dim == 2:
        integrand = [0] + list(
            (0.5 * R[1:] * DW[1:]) * (np.log(mu / 2 * R[1:]) + np.euler_gamma)
        )
        # Epsilon terms
        integrandEps=[0] + list(
            (0.5 * R[1:] * DW[1:])*1/2
        )
    elif dim == 4:
        integrand = [0] + list(
            (-1 / 16 * R[1:] ** 3 * DW[1:]) * (DW[1:] + 2 * m0 ** 2)
            * (np.log(mu / 2 * R[1:]) + np.euler_gamma + 1)
        )
        # Epsilon terms
        integrandEps=[0] + list(
            (-1 / 16 * R[1:] ** 3 * DW[1:]) * (DW[1:] + 2 * m0 ** 2)*1/2
        )
    elif dim == 6:
        # These two terms come from the l**-5 terms
        #The first term is the constant-field contribution
        #The second term comes from derivative-corrections to the effective action
        integrand1 = [0] + list(
          1/2*(1 / 16 * R[1:] ** 5 * DW[1:]) * (3*m0**4 + 3*m0**2*DW[1:] + DW[1:]**2)
            *1/12*(np.log(mu / 2 * R[1:]) + np.euler_gamma +143/216-special.zeta(3))
        )
        integrand2 = [0] + list(
          1/2*(1/32*R[1:]**5*dWR[1:]**2)
            *1/12*(np.log(mu / 2 * R[1:]) + np.euler_gamma +143/216-special.zeta(3))
        )
        integrand = np.array(integrand1) + np.array(integrand2)
        # Epsilon terms
        integrandEps1 = [0] + list(
             1/2*(1 / 16 * R[1:] ** 5 * DW[1:])
             * (3*m0**4 + 3*m0**2*DW[1:] + DW[1:]**2)
             * (1/24)
        )
        integrand2Eps = [0] + list(1/2*(1/32*R[1:]**5*dWR[1:]**2)*1/24)
        integrandEps = np.array(integrandEps1) + np.array(integrand2Eps)
    elif dim % 2 == 0:
        raise NotImplementedError(
            f"findRenormalisationTerm error: {dim=} not implemented"
            )

    res = simpson(integrand, x=R)
    res_half = simpson(np.array(integrand)[::2], x=R[::2])
    err = abs((res - res_half) / 7)
    resEps = simpson(integrandEps, x=R)

    return res, resEps, err
