"""
Thermal bubble nucleation in scalar Yukawa theory, d=3.

We consider the model Example 1 in Phys.Rev.D 104 (2021) 096015,
arXiv:2108.04377. Utilising high-temperature dimensional reduction at leading
order, we compute the temperature dependence of the thermal nucleation rate at
one-loop order.

Following Phys.Rev.Lett. 46 (1981) 388, and assuming that the scalar damping
rate is small, we compute the dynamical prefactor of the nucleation rate in
terms of the negative eigenvalue of the functional determinant.
"""
import numpy as np  # arrays and maths
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant

# dimension
dim = 3

# zero temperature parameters
s = 0
msq = -1
g = 0.3
lam = 0.1
mf = -0.2
y = 0.3

# dimensional reduction relations at leading order
def params_3d(T):
    return {
        "s3": (s + 1 / 24 * (g + 4 * y * mf) * T ** 2) / np.sqrt(T),
        "m3sq": msq + 1 / 24 * (lam + 4 * y ** 2) * T ** 2,
        "g3": np.sqrt(T) * g,
        "lam3": T * lam
    }


# potential and its derivatives
def VT(x, T):
    p = params_3d(T)
    return (
        p["s3"] * x
        + 1 / 2 * p["m3sq"] * x ** 2
        + 1 / 6 * p["g3"] * x ** 3
        + 1 / 24 * p["lam3"] * x ** 4
    )


def dVT(x, T):
    p = params_3d(T)
    return (
        p["s3"]
        + p["m3sq"] * x
        + 1 / 2 * p["g3"] * x ** 2
        + 1 / 6 * p["lam3"] * x ** 3
    )


def ddVT(x, T):
    p = params_3d(T)
    return (
        + p["m3sq"]
        + p["g3"] * x
        + 1 / 2 * p["lam3"] * x ** 2
    )


# minima
def minima(T):
    p = params_3d(T)
    # soliving for cubic roots with np
    cubic = np.polynomial.polynomial.Polynomial(
        [p["s3"], p["m3sq"], 1 / 2 * p["g3"], 1 / 6 * p["lam3"]]
    )
    x0_list = cubic.roots()
    # removing complex solutions
    x0_real = (x0_list[np.isreal(x0_list)]).real
    # checking number of real solutions
    if len(x0_real) == 1:
        # only one solution
        return x0_real
    elif len(x0_real) == 3:
        # order solutions based on potential
        return x0_real[np.argsort(VT(x0_real, T))]
    else:
        raise ValueError("Neither 1 nor 3 real solutions")


print("%-12s %-12s %-12s %-12s" % ("T", "S0", "-log(A/T^4)", "-log(rate)"))

# running over temperatures
T_max = 8.4
T_min = 7.9
nT = 50 + 1

for T in np.linspace(T_max, T_min, num=nT):

    min_T = minima(T)
    if len(min_T) < 3:
        continue
    else:
        phi_true = min_T[0]
        phi_false = min_T[1]
        V = lambda x: VT(x, T)
        dV = lambda x: dVT(x, T)
        ddV = lambda x: ddVT(x, T)

    # CosmoTransitions object
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
    bub_det = BubbleDeterminant(
        bub_config, higgs, thermal=True
    )

    # full one-loop correction
    S1, S1_err = bub_det.findDeterminant()

    # dynamical part assuming that damping is negligible
    eig_neg, eig_neg_err = bub_det.findNegativeEigenvalue()
    dynamical_prefactor = np.sqrt(abs(eig_neg)) / (2 * np.pi)

    minusLogAOnT4 = S1 + 4 * np.log(T)

    minusLogRate = S0 + minusLogAOnT4

    # printing results
    print("%-12g %-12g %-12g %-12g" % (T, S0, minusLogAOnT4, minusLogRate))
