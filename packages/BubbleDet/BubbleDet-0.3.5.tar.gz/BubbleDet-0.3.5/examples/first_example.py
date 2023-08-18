"""
A first example, scalar vacuum decay in d=4.

The nucleation rate is computed at one-loop order for the classic potential
used in Coleman and Callan's original works, Phys.Rev.D 15 (1977) 2929-2936 and
Phys.Rev.D 16 (1977) 1762-1768.
"""
import numpy as np  # arrays and maths
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant

# dimension
dim = 4

# parameters
msq = 0.25
g = -1
lam = 1


# potential and its derivatives
def V(x):
    return 1 / 2 * msq * x**2 + 1 / 6 * g * x**3 + 1 / 24 * x**4


def dV(x):
    return msq * x + 1 / 2 * g * x**2 + 1 / 6 * x**3


def ddV(x):
    return msq + g * x + 1 / 2 * x**2


# minima
phi_true = (-3 * g + np.sqrt(9 * g**2 - 24 * msq)) / 2
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

# creating particle instance
higgs = ParticleConfig(
    W_Phi=ddV,
    spin=0,
    dof_internal=1,
    zero_modes="Higgs",
)

# creating bubble determinant instance
bub_det = BubbleDeterminant(bub_config, [higgs])

# fluctuation determinant
S1, S1_err = bub_det.findDeterminant()

# printing results
print("S0          :", S0)
print("S1          :", S1)
print("err(S1)     :", S1_err)
