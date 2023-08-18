import pytest  # for tests
import numpy as np  # arrays and maths
from scipy.special import gamma  # gamma function
from scipy.integrate import simps  # integrators
from cosmoTransitions.tunneling1D import SingleFieldInstanton # bounce equation
from BubbleDet import BubbleConfig


# EIKR's potential
def V4(phi, alpha):
    return 1 / 2 * phi**2 - 1 / 2 * phi**3 + 1 / 8 * alpha * phi**4


# first derivative of potential
def dV4(phi, alpha):
    return phi - 3 / 2 * phi**2 + 1 / 2 * alpha * phi**3


# second derivative of potential
def ddV4(phi, alpha):
    return 1 - 3 * phi + 3 / 2 * alpha * phi**2


# Goldstone mass squared
def dV4onPhi(phi, alpha):
    return 1 - 3 / 2 * phi + 1 / 2 * alpha * phi**2


# metastable minimum of potential
def phi_false_V4(alpha):
    return 0


# stable minimum of potential
def phi_true_V4(alpha):
    return (3 + np.sqrt(9 - 8 * alpha)) / (2 * alpha)


@pytest.fixture
def cosmo_transitions_V4(dim, alpha):
    return SingleFieldInstanton(
        phi_true_V4(alpha),
        phi_false_V4(alpha),
        lambda phi: V4(phi, alpha),
        lambda phi: dV4(phi, alpha),
        d2V=lambda phi: ddV4(phi, alpha),
        alpha=(dim - 1),
    )


# -phi^4 + phi^6 potential
def V6(phi, alpha):
    return 1 / 2 * phi**2 - 1 / 4 * phi**4 + 1 / 32 * alpha * phi**6


# first derivative of potential
def dV6(phi, alpha):
    return phi - phi**3 + 3 / 16 * alpha * phi**5


# second derivative of potential
def ddV6(phi, alpha):
    return 1 - 3 * phi**2 + 15 / 16 * alpha * phi**4


# Goldstone mass squared
def dV6onPhi(phi, alpha):
    return 1 - phi**2 + 3 / 16 * alpha * phi**4


# metastable minimum of potential
def phi_false_V6(alpha):
    return 0


# stable minimum of potential
def phi_true_V6(alpha):
    return 2 / np.sqrt(2 - np.sqrt(4 - 3 * alpha))


@pytest.fixture
def cosmo_transitions_V6(dim, alpha):
    return SingleFieldInstanton(
        phi_true_V6(alpha),
        phi_false_V6(alpha),
        lambda phi: V6(phi, alpha),
        lambda phi: dV6(phi, alpha),
        d2V=lambda phi: ddV6(phi, alpha),
        alpha=(dim - 1),
    )


def profile_object(cosmo_transitions_object, dim, alpha):
    return cosmo_transitions_object.findProfile(
        xtol=1e-9,
        phitol=1e-9,
        npoints=500,
        rmin=1e-4,
        rmax=1e4,
    )


# scaleless potential, with negative phi^a coefficient
def V_scaleless(phi, dim, Lambda):
    a = (2 * dim) // (dim - 2)
    return - Lambda * phi**a / a


# first derivative of potential
def dV_scaleless(phi, dim, Lambda):
    a = (2 * dim) // (dim - 2)
    return -Lambda * phi**(a - 1)


# second derivative of potential
def ddV_scaleless(phi, dim, Lambda):
    a = (2 * dim) // (dim - 2)
    return -(a - 1) * Lambda * phi**(a - 2)


def bubbleConfig_scaleless(dim, Lambda, RScale):
    if dim not in [3, 4, 6]:
        raise ValueError("{dim=} not in [3, 4, 6]")
    rmin = 0
    rmax = RScale * 50
    npoints = 1000
    step = (rmax - rmin) / (npoints - 1)
    r = rmin + step * np.arange(0, npoints)
    if dim == 3:
        Phi = (3 / Lambda)**0.25 * np.sqrt(RScale / (RScale**2 + r**2))
    elif dim == 4:
        Phi = np.sqrt(8 / Lambda) * RScale / (RScale**2 + r**2)
    elif dim == 6:
        Phi = 24 / Lambda * (RScale / (RScale**2 + r**2))**2
    return BubbleConfig(
        phi_metaMin=0,
        V=lambda phi: V_scaleless(phi, dim, Lambda),
        dV=lambda phi: dV_scaleless(phi, dim, Lambda),
        d2V=lambda phi: ddV_scaleless(phi, dim, Lambda),
        dim=dim,
        massless_Higgs=True,
        scaleless=True,
        R=r,
        Phi=Phi,
    )
