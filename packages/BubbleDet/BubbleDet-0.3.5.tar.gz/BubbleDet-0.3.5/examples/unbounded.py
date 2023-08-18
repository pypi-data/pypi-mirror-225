"""
Vacuum decay in an unbounded -phi**4 potential in d=4.

For each orbital quantum number, comparison is made to the analytic results of
Phys.Rev.D 97 (2018) 5, 056006, arXiv:1707.08124.
"""
import numpy as np
import matplotlib.pyplot as plt
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant


# unbounded potential, with negative phi^4 coefficient
def V(phi, Lambda):
    return -0.25 * Lambda * phi**4


# first derivative of potential
def dV(phi, Lambda):
    return -Lambda * phi**3


# second derivative of potential
def ddV(phi, Lambda):
    return -3 * Lambda * phi**2


# exact determinant
def det_analyticL(l):
    return l * (l - 1) / (l + 2) / (l + 3)


Lambda=0.1;
RScale=0.1;
dim=4;
#Creating our custom bounce
rmin=0
rmax=50;
npoints=40000;
step=(rmax-rmin)/(npoints-1)

R=np.arange(0,npoints)*step+rmin
Phi=np.sqrt(8/Lambda)*RScale/(RScale**2+R**2)

# creating bubble config instance
bub_config = BubbleConfig(
    phi_metaMin=0.0,
    V=lambda phi: V(phi, Lambda),
    dV=lambda phi: dV(phi, Lambda),
    d2V=lambda phi: ddV(phi, Lambda),
    dim=dim,
    R=R,
    Phi=Phi,
    massless_Higgs=True,
)

# creating particle instance
higgs = ParticleConfig(
    W_Phi=lambda phi: ddV(phi, Lambda),
    spin=0,
    dof_internal=1,
    zero_modes="Higgs",
)

# creating bubble determinant instance
bub_det = BubbleDeterminant(
    bub_config, higgs, renormalisation_scale=1 / RScale
)

# printing headers
print("Unbounded potential:")
print("%-4s %-12s %-12s %-12s" % ("l", "Numerical", "Analytical", "Difference"))

l_max = 100
diffDet = []
S1_list, S1_err_list = bub_det.findDeterminant()
for l in range(2, 50):
    det, err, deriv = bub_det.findGelfandYaglomTl(higgs, l, 10**-4, 10**-5)
    det_analytic = det_analyticL(l)

    diffS1 = abs(det - det_analytic)
    diffDet.append(diffS1 / det)
    print("%-4d %-12g %-12g %-12g" % (l, det, det_analytic, diffS1))

DeltasS1 = np.arange(2, 50)
plt.plot(DeltasS1, diffDet, "o", fillstyle="none")
plt.ylabel("$S_1$ relative difference")
plt.xlabel("$l$")
plt.show()
