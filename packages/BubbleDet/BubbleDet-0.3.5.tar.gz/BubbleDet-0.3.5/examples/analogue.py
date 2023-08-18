"""
Analogue false vacuum decay in d=2.

We adopt a trigonometric potential, as relevant to cold atom setups for
analogue false vacuum decay. Our potential and parameter choices follow
Phys.Rev.D 107 (2023) 8, 083509, arXiv:2204.11867.
"""
import numpy as np  # arrays and maths
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant

# dimension
dim = 2

# parameters
lam = 2
msq = 1
v0sq_list = np.linspace(2, 10, num=9)


# potential and its derivatives
def V(x):
    xx = x / v0
    return msq * v0 ** 2 * (np.cos(xx) - 1 + lam ** 2 / 2 * np.sin(xx) ** 2)


def dV(x):
    xx = x / v0
    return msq * v0 * (-np.sin(xx) + lam ** 2 * np.cos(xx) * np.sin(xx))


def ddV(x):
    xx = x / v0
    return msq * (-np.cos(xx) + lam ** 2 * (1 - 2 * np.sin(xx) ** 2))


# creating particle instance
higgs = ParticleConfig(
    W_Phi=ddV,
    spin=0,
    dof_internal=1,
    zero_modes="Higgs",
)


print("%-12s %-12s %-12s" % ("v0^2", "S0", "S1"))

for v0sq in v0sq_list:
    # parameters
    v0 = np.sqrt(v0sq)

    # minima
    phi_true = np.pi * v0
    phi_false = 0

    # nucleation object
    ct_obj = SingleFieldInstanton(
        phi_true,
        phi_false,
        V,
        dV,
        d2V=ddV,
        alpha=(dim - 1),
    )

    # bounce calculation
    profile = ct_obj.findProfile()

    # bounce action
    S0 = ct_obj.findAction(profile)

    # creating bubble config instance
    bub_config = BubbleConfig.fromCosmoTransitions(ct_obj, profile)

    # creating bubble determinant instance
    bub_det = BubbleDeterminant(bub_config, [higgs])

    # fluctuation determinant
    S1, S1_err = bub_det.findDeterminant()

    # printing results
    print("%-12g %-12g %-12g" % (v0sq, S0, S1))
