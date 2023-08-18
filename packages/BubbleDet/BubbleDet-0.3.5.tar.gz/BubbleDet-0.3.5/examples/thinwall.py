"""
Approach to the thin-wall limit for d=2,3,4.

Comparison to thin-wall results from Konoplich Theor. Math. Phys. 73 (1987)
1286-1295 and Ivanov et al. JHEP 03 (2022) 209, arXiv:2202.04498.
See also Phys.Rev.D 69 (2004) 025009, arXiv:hep-th/030720 and
Phys.Rev.D 72 (2005) 125004, arXiv:hep-th/0511156.
"""
import numpy as np # arrays and maths
import matplotlib.pyplot as plt # plotting
from cosmoTransitions.tunneling1D import SingleFieldInstanton  # bounce
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant

# the dimension, dim = 2, 3 or 4
dim = 4


# Ivanov et al's potential (and Kosowsky et al's), with lambda and v scaled out
def V(phi, Delta):
    return 0.125 * (phi ** 2 - 1) ** 2 + Delta * (phi - 1)


# first derivative of potential
def dV(phi, Delta):
    return 0.5 * phi * (phi ** 2 - 1) + Delta


# second derivative of potential
def ddV(phi, Delta):
    return 0.5 * (3 * phi ** 2 - 1)


# metastable minimum of potential
def phi_true(Delta):
    if Delta > 0:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[0]
    else:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[-1]


# stable minimum of potential
def phi_false(Delta):
    if Delta > 0:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[-1]
    else:
        return np.sort(np.roots([0.5, 0, -0.5, Delta]))[0]


# action in thin-wall regime
def thinwall_action(Delta, dim):
    if dim == 4:
        return (Delta ** (1 - dim) * np.pi ** 2 / 3) * (
            1 - (2 * np.pi ** 2 + 9 / 2) * Delta ** 2
        )
    elif dim == 3:
        return (Delta ** (1 - dim) * 2 ** 5 * np.pi / 3 ** 4) * (
            1 - (9 * np.pi ** 2 / 4 - 1) * Delta ** 2
        )
    elif dim == 2:
        return (Delta ** (1 - dim) * 2 * np.pi / 9) * (
            1 - (3 * np.pi ** 2 - 19 / 2) * Delta ** 2
        )
    else:
        print("thin_wall_action error: dimension <" + str(dim) + ">")
        return float("nan")


 #minus the logarithm of the one-loop determinant in thin-wall regime
def thinwall_log_det(Delta, dim):
    prefactor = (dim / 2) * (
        1 - dim + np.log(6 * thinwall_action(Delta, dim) / np.pi)
    )
    if dim == 4:
        # 54 here agrees with Konoplich, 45 agrees with Ivanov et al.
        # Dunne and Min, and Baacke and Lavrelashvili agree with Konoplich
        expo = Delta ** (1 - dim) * (9 - 2 * np.pi / np.sqrt(3)) / 32
    elif dim == 3:
        expo = Delta ** (1 - dim) * (20 + 9 * np.log(3)) / 54
    elif dim == 2:
        expo = Delta ** (1 - dim) * (-6 + np.pi / np.sqrt(3)) / 6
        prefactor = np.log(Delta / np.pi)
        #See 0209201. I changed their Renormalization scheme to ours
    else:
        print("thinwall_log_det error: dimension <" + str(dim) + ">")
        return float("nan")
    return expo - prefactor


# radius of thin-wall bubble
def thinwall_radius(Delta, dim):
    return (dim - 1) / (3 * Delta) + Delta * (
        6 * np.pi ** 2 - 40 + dim * (26 - 4 * dim - 3 * np.pi ** 2)
    ) / (3 * (dim - 1))


if dim == 2:
    Deltas = np.array(
        [0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015, 0.01]
    )
elif dim == 3:
    Deltas = np.array(
        [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02]
    )
elif dim == 4:
    Deltas = np.array(
        [0.1, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.015]
    )
else:
    raise ValueError(f"Error, results not known for {dim=}")
diffS = []
diffDet = []

print(
    "%-8s %-16s %-16s %-16s %-16s %-16s"
    % ("alpha", "S0", "Delta_S0", "S1", "Delta_S1", "err_S1")
)
for Delta in Deltas:
    # CosmoTransitions object
    ct_obj = SingleFieldInstanton(
        phi_true(Delta),
        phi_false(Delta),
        lambda phi: V(phi, Delta),
        lambda phi: dV(phi, Delta),
        d2V=lambda phi: ddV(phi, Delta),
        alpha=(dim - 1),
    )

    # bounce calculation
    profile = ct_obj.findProfile(
        phitol=1e-12, xtol=1e-12, npoints=2000
    )

    # bounce action
    S0 = ct_obj.findAction(profile)
    diffS0 = abs(S0 - thinwall_action(Delta, dim))

    # creating bubble config instance
    bub_config = BubbleConfig.fromCosmoTransitions(ct_obj, profile)

    # creating particle instance
    higgs = ParticleConfig(
        W_Phi=lambda phi: ddV(phi, Delta),
        spin=0,
        dof_internal=1,
        zero_modes="Higgs",
    )

    # creating bubble determinant instance
    bub_det = BubbleDeterminant(bub_config, [higgs])

    # fluctuation determinant
    S1, S1_err = bub_det.findDeterminant()

    # difference to analytic thin-wall result
    diffS1 = abs(S1 - thinwall_log_det(Delta, dim))

    diffS.append(diffS0 / S0)
    diffDet.append(diffS1 / abs(S1))

    print(
        "%-8.4g %-16.8g %-16.8g %-16.8g %-16.8g %-16.8g"
        % (
            Delta,
            S0,
            diffS0 / S0,
            S1,
            diffS1 / abs(S1),
            S1_err / abs(S1),
        )
    )

DeltasS0 = Deltas ** 4
plt.plot(DeltasS0, diffS, "o", fillstyle="none")
plt.plot([0, DeltasS0[-1]], [0, diffS[-1]])
plt.plot([0, DeltasS0[0]], [0, diffS[0]])
plt.ylabel("$S_0$ relative difference")
plt.xlabel(r"$\Delta^4$")
plt.show()

DeltasS1 = Deltas ** 2
plt.plot(DeltasS1, diffDet, "o", fillstyle="none")
plt.plot([0, DeltasS1[-1]], [0, diffDet[-1]])
plt.plot([0, DeltasS1[0]], [0, diffDet[0]])
plt.ylabel("$S_1$ relative difference")
plt.xlabel(r"$\Delta^2$")
plt.show()
