"""
Symmetry breaking vacuum decay in d=4.

For simplicity, we consider that the tree-level potential admits two minima with
a barrier between. We thus include a phi**6 operator, following for example
Phys.Rev.D 102 (2020) 8, 085001, arXiv:2006.04886.
"""
import numpy as np  # arrays and maths
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant

# dimension
dim = 4

# symmetry groups
G = ['U1']
H = ['None']

# parameters
msq = 1
lam = -0.15
gsq_list = np.arange(0.01, 2.01, 0.01)
c6 = 0.01


# potential and its derivatives
def V(x, msq, lam, c6):
    return 1 / 2 * msq * x**2 + 1 / 2 * lam * x**4 + 1 / 32 * c6 * x**6


def dV(x, msq, lam, c6):
    return msq * x + 2 * lam * x**3 + 3 / 16 * c6 * x**5


def ddV(x, msq, lam, c6):
    return msq + 6 * lam * x**2 + 15 / 16 * c6 * x**4

def dVonPhi(x, msq, lam, c6):
    return msq + 2 * lam * x**2 + 3 / 16 * c6 * x**4


# minima
def phi_true(msq, lam, c6):
    return 2*np.sqrt((-4*lam + np.sqrt(16*lam**2 - 3*c6*msq))/c6)/np.sqrt(3)


def phi_false(msq, lam, c6):
    return 0


# critical mass
def msq_critical(lam, c6):
    return 4 * lam**2 / c6


print("%-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s %-12s" % \
        ("msq", "lam", "c6", "gsq", "mH/mW", "S0", "S1H", "S1Ga", "S1Go", "S1"))

# running over parameters
for gsq in gsq_list:

    # get masses
    phi_f = phi_false(msq, lam, c6)
    phi_t = phi_true(msq, lam, c6)
    mH_f = np.sqrt(ddV(phi_f, msq, lam, c6))
    mH_t = np.sqrt(ddV(phi_t, msq, lam, c6))
    mW_t = np.sqrt(gsq * phi_t**2)

    # CosmoTransitions object
    ct_obj = SingleFieldInstanton(
        phi_true(msq, lam, c6),
        phi_false(msq, lam, c6),
        lambda x: V(x, msq, lam, c6),
        lambda x: dV(x, msq, lam, c6),
        d2V=lambda x: ddV(x, msq, lam, c6),
        alpha=(dim - 1),
    )

    # bounce calculation
    profile = ct_obj.findProfile()

    # bounce action
    S0 = ct_obj.findAction(profile)

    # creating bubble config instance
    bub_config = BubbleConfig.fromCosmoTransitions(ct_obj, profile)

    # creating particle instances
    higgs = ParticleConfig(
        W_Phi=lambda x: ddV(x, msq, lam, c6),
        spin=0,
        dof_internal=1,
        zero_modes="Higgs",
    )
    goldstone = ParticleConfig(
        W_Phi=lambda x: dVonPhi(x, msq, lam, c6),
        spin=0,
        dof_internal=1,
        zero_modes="Goldstone",
    )
    gauge = ParticleConfig(
        W_Phi=lambda x: gsq * x**2,
        spin=1,
        dof_internal=1,
        zero_modes="None",
    )

    # creating bubble determinant instance
    bub_det = BubbleDeterminant(bub_config, [higgs, goldstone, gauge])

    # Higgs fluctuation determinant
    S1_list, S1_err_list = bub_det.findDeterminant(full=True)
    S1_list[0] += 2 * np.log(msq) # units for Higgs determinant
    S1H, S1Go, S1Ga = S1_list

    S1tot = np.sum(S1_list)

    # printing results
    print("%-12g %-12g %-12g %-12g %-12g %-12g %-12g %-12g %-12g %-12g" % \
            (msq, lam, c6, gsq, mH_t / mW_t, S0, S1H, S1Ga, S1Go, S1tot))
