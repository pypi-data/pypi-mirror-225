import numpy as np  # arrays and maths
from scipy.special import gamma # special functions
from .helpers import simpson # integrator
from cosmoTransitions.helper_functions import deriv14  # derivatives for arrays


def findDerivativeExpansion(config, NLO=False):
    r"""Derivative expansion of determinant

    Full docs in BubbleDet.py.
    """
    if config.zero_modes.lower() != "none":
        raise ValueError("Derivative expansion requires absence of zero modes")
    d = config.dim
    R = config.R
    mu = config.renormalisation_scale
    angles = 2 * np.pi ** (d / 2) / gamma(d / 2)
    measure = angles * R ** (d - 1)
    offset =  1e-16 / R[-1] ** 2 # to prevent 1/0
    W_offset = config.W + offset

    # constructing integrand at LO
    integrand = config.W ** (d / 2)
    integrand *= 1 / (4 * np.pi) ** (d / 2)
    if d % 2 == 0:  # even dimensions
        n = d // 2
        harmonic = np.sum([1 / h for h in range(1, n + 1)])
        integrand *= -1 / 2 * (-1) ** n / gamma(n + 1)
        eps_term = - 2 / (d - 1) if config.spin == 1 else 0
        integrand *= harmonic + np.log(mu**2 / W_offset) + eps_term
    else:  # odd dimensions
        integrand *= -1 / 2 * gamma(-d / 2)
    if config.spin == 1:
        integrand *= (d - 1) # massive vector degrees of freedom
    # integrating
    integrand *= measure
    S1 = simpson(integrand, x=R)
    S1_half = simpson(integrand[::2], x=R[::2])
    S1_err = abs(S1 - S1_half) / 7

    if NLO:
        if d == 2:
            raise ValueError("Derivative expansion diverges at NLO in d=2")
        # constructing integrand at NLO
        integrand = deriv14(config.W, R) ** 2 * W_offset ** (d / 2 - 3)
        integrand *= 1 / (4 * np.pi) ** (d / 2)
        if d % 2 == 0 and d > 5:  # even dimensions
            n = d // 2
            harmonic = np.sum([1 / h for h in range(1, (n - 3) + 1)])
            integrand *= -1 / 24 * (-1) ** n / gamma((n - 3) + 1)
            eps_term = - 2 / (d - 1) if config.spin == 1 else 0
            integrand *= harmonic + np.log(mu**2 / W_offset) + eps_term
        else:  # odd dimensions
            integrand *= gamma(3 - d / 2) / 24
        if config.spin == 1:
            integrand *= (d - 1) # massive vector degrees of freedom
        # integrating
        integrand *= measure
        S1_NLO = simpson(integrand, x=R)
        S1_NLO_half = simpson(integrand[::2], x=R[::2])
        S1_NLO_err = abs(S1_NLO - S1_NLO_half) / 7
        S1 += S1_NLO
        S1_err += S1_NLO_err

    # returning result
    return S1, S1_err
