"""
Derivative expansion

Showing the convergence of the derivative expansion for a heavy scalar field.
"""
import numpy as np  # arrays and maths
import matplotlib.pyplot as plt  # plots
from scipy.optimize import curve_fit  # fitting
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant

# dimension
dim = 4
print(f"dim = {dim}")

# Lagrangian parameters
msq = 1
lam = -0.15
gsq_list = np.array([2 ** i for i in range(-4, 5)])
c6 = 0.01

# spin of heavy particle
spin = 0


# potential and its derivatives
def V(x, msq, lam, c6):
    return 1 / 2 * msq * x**2 + 1 / 2 * lam * x**4 + 1 / 32 * c6 * x**6


def dV(x, msq, lam, c6):
    return msq * x + 2 * lam * x**3 + 3 / 16 * c6 * x**5


def ddV(x, msq, lam, c6):
    return msq + 6 * lam * x**2 + 15 / 16 * c6 * x**4


# minima
def phi_true(msq, lam, c6):
    return 2*np.sqrt((-4*lam + np.sqrt(16*lam**2 - 3*c6*msq))/c6)/np.sqrt(3)


def phi_false(msq, lam, c6):
    return 0


# critical mass
def msq_critical(lam, c6):
    return 4 * lam**2 / c6


# for fitting
def line(x, a, b):
    return a + b * x


msq_ratio_list = np.zeros(len(gsq_list))
res_list = np.zeros(len(gsq_list))
diff_LO_list = np.zeros(len(gsq_list))
diff_NLO_list = np.zeros(len(gsq_list))
err_list = np.zeros(len(gsq_list))

print(
    "%-12s %-12s %-12s %-12s %-12s %-12s %-12s"
    % ("gsq", "mH/mW", "S0", "S1_heavy", "diff_LO", "diff_NLO", "err")
)

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

# creating bubble config
bub_config = BubbleConfig.fromCosmoTransitions(ct_obj, profile)

# masses that don't depend on g
phi_f = phi_false(msq, lam, c6)
phi_t = phi_true(msq, lam, c6)
mPhi_f = np.sqrt(ddV(phi_f, msq, lam, c6))
mPhi_t = np.sqrt(ddV(phi_t, msq, lam, c6))

# running over parameters
for i in range(len(gsq_list)):

    gsq = gsq_list[i]

    # heavy mass
    mChi_t = np.sqrt(gsq * phi_t**2)

    # creating heavy field particle instance
    heavy = ParticleConfig(
        W_Phi=lambda x: gsq * x**2,
        spin=spin,
        dof_internal=1,
        zero_modes="None",
    )

    # creating bubble determinant instance
    bub_det_heavy = BubbleDeterminant(bub_config, heavy)

    # Heavy field fluctuation determinant
    S1_heavy, S1_heavy_err = bub_det_heavy.findDeterminant()

    # derivative expansion
    S1_heavy_LO, S1_heavy_LO_err = bub_det_heavy.findDerivativeExpansion(
        heavy, NLO=False
    )
    S1_heavy_NLO, S1_heavy_NLO_err = bub_det_heavy.findDerivativeExpansion(
        heavy, NLO=True
    )

    diff_LO = (S1_heavy_LO - S1_heavy) / abs(S1_heavy)
    diff_NLO = (S1_heavy_NLO - S1_heavy) / abs(S1_heavy)
    err = max(
        abs(S1_heavy_err / S1_heavy),
        abs(S1_heavy_LO_err / S1_heavy_LO),
        abs(S1_heavy_NLO_err / S1_heavy_NLO),
    )

    # assigning lists
    msq_ratio_list[i] = (mPhi_t / mChi_t) ** 2
    res_list[i] = S1_heavy
    diff_LO_list[i] = diff_LO
    diff_NLO_list[i] = diff_NLO
    err_list[i] = err

    # printing results
    print(
        "%-12g %-12g %-12g %-12g %-12g %-12g %-12g"
        % (gsq, mPhi_t / mChi_t, S0, S1_heavy, diff_LO, diff_NLO, err)
    )

popt, pcov = curve_fit(
    line, np.log(msq_ratio_list[2:]), np.log(abs(diff_LO_list[2:]))
)
fit_curve = np.exp(line(np.log(msq_ratio_list), *popt))
fit_label = "y = %3g + %3g * x" % (popt[0], popt[1])
plt.plot(msq_ratio_list, fit_curve, "-", label=fit_label)

popt, pcov = curve_fit(
    line, np.log(msq_ratio_list[2:]), np.log(abs(diff_NLO_list[2:]))
)
fit_curve = np.exp(line(np.log(msq_ratio_list), *popt))
fit_label = "y = %3g + %3g * x" % (popt[0], popt[1])
plt.plot(msq_ratio_list, fit_curve, "-", label=fit_label)

plt.plot(
    msq_ratio_list, abs(diff_LO_list), "k+", fillstyle="none", label="LO"
)
plt.plot(
    msq_ratio_list, abs(diff_NLO_list), "ko", fillstyle="none", label="NLO"
)

plt.xscale("log")
plt.yscale("log")
plt.title("Derivative expansion, $d = " + str(dim) + "$")
plt.ylabel(r"$\Delta S_1 / S_1$")
plt.xlabel(r"$m_\phi^2/m_\chi^2$")
plt.legend(loc="best")
plt.tight_layout()
plt.show()
