"""
Convergence of the WKB approximation for large orbital quantum number.

The WKB approximation reproduces the correct behaviour for the functional
determinant at large orbital quantum number. We show how the WKB approximation
converges, and how higher orders in the WKB approximation speed up the rate of
convergence.
"""
import numpy as np  # arrays and maths
import matplotlib.pyplot as plt # plotting
from scipy.optimize import curve_fit # fitting curve to results
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant


# for fits
def linear(x, a, b):
    return x * a + b


# parameters
dim = 4
msq = 1
g = -3
lam = 3 * 0.5

# potential and its derivatives
def V(x):
    return 1 / 2 * msq * x**2 + 1 / 6 * g * x**3 + lam / 24 * x**4


def dV(x):
    return msq * x + 1 / 2 * g * x**2 + lam / 6 * x**3


def ddV(x):
    return msq + g * x + lam / 2 * x**2


# minima
phi_true = (-3 * g + np.sqrt(9 * g**2 - 24 * msq * lam)) / 2 / lam
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
profile = ct_obj.findProfile(
    xtol=1e-12,
    phitol=1e-12,
    npoints=1000,
    rmin=1e-5,
    rmax=1e5,
)

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
bub_det = BubbleDeterminant(bub_config, higgs, thermal=True)

# getting WKB results
l_min = 2
l_max = 100
l_list = np.arange(l_min, l_max)

lnTl_WKB, lnTl_WKB3, lnTl_WKB5, lnTl_WKB7, lnTl_WKB9 = bub_det.findWKB(
    higgs,
    l_max,
    separate_orders=True,
)
diff = np.zeros(l_max - 2)
diff_NLO3 = np.zeros(l_max - 2)
diff_NLO5 = np.zeros(l_max - 2)
diff_NLO7 = np.zeros(l_max - 2)
diff_NLO9 = np.zeros(l_max - 2)
# running over l
print(
    "%-8s %-16s %-16s %-16s %-16s %-16s %-16s"
    % (
        "l",
        "lnTl",
        "diff_WKB_LO",
        "diff_WKB_NLO",
        "diff_WKB_N2LO",
        "diff_WKB_N3LO",
        "diff_WKB_N4LO",
    )
)
for l in l_list:
    Tl, Tl_err = bub_det.findGelfandYaglomTl(higgs, l, rmin=1e-5, gy_tol=1e-12)
    lnTl = np.log(Tl)
    lnTl_err = Tl_err / abs(Tl)
    diff[l - l_min] = abs(lnTl - lnTl_WKB[l]) / abs(lnTl)
    diff_NLO3[l - l_min] = abs(lnTl - lnTl_WKB[l] - lnTl_WKB3[l]) / abs(lnTl)
    diff_NLO5[l - l_min] = abs(
        lnTl - lnTl_WKB[l] - lnTl_WKB3[l] - lnTl_WKB5[l]
    ) / abs(lnTl)
    diff_NLO7[l - l_min] = abs(
        lnTl - lnTl_WKB[l] - lnTl_WKB3[l] - lnTl_WKB5[l] - lnTl_WKB7[l]
    ) / abs(lnTl)
    diff_NLO9[l - l_min] = abs(
        lnTl
        - lnTl_WKB[l]
        - lnTl_WKB3[l]
        - lnTl_WKB5[l]
        - lnTl_WKB7[l]
        - lnTl_WKB9[l]
    ) / abs(lnTl)
    print(
        "%-8d %-16.8g %-16.8g %-16.8g %-16.8g %-16.8g %-16.8g"
        % (
            l,
            lnTl,
            diff[l - l_min],
            diff_NLO3[l - l_min],
            diff_NLO5[l - l_min],
            diff_NLO7[l - l_min],
            diff_NLO9[l - l_min],
        )
    )

# plotting
plt.plot(l_list, diff, "bo", fillstyle="none", label=r"WKB $l^{-1}$")
plt.plot(l_list, diff_NLO3, "ro", fillstyle="none", label=r"WKB $l^{-3}$")
plt.plot(l_list, diff_NLO5, "ko", fillstyle="none", label=r"WKB $l^{-5}$")
plt.plot(l_list, diff_NLO7, "mo", fillstyle="none", label=r"WKB $l^{-7}$")
plt.plot(l_list, diff_NLO9, "yo", fillstyle="none", label=r"WKB $l^{-9}$")
plt.ylabel(r"$\log T_l$ relative difference")
plt.xlabel(r"$l$")
plt.xscale("log")
plt.yscale("log")
plt.title("dim = " + str(dim))
plt.legend(loc="best")
plt.tight_layout()
plt.show()
