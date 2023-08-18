"""
One-loop correction to the kink mass, in d=1.

We compare to the analytic result of Phys.Rev.D 10 (1974) 4130-4138,
for the kink mass in the symmetry-breaking phi**4 potential.
"""
import numpy as np
import matplotlib.pyplot as plt
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant


# Dashen et al's potential, with m^2 and lambda scaled out
def V(phi):
    return -0.5 * phi**2 + 0.25 * phi**4


# first derivative of potential
# minima are at +/- 1, maximum at 0
def dV(phi):
    return -phi + phi**3


# second derivative of potential
def ddV(phi):
    return -1 + 3 * phi**2


# exact 0 and 1-loop mass, Eq. (3.10) in Dashen et al
M_analytic = 2 * np.sqrt(2) / 3
dM_analytic = 1 / 2 / np.sqrt(6) - 3 / np.pi / np.sqrt(2)

# contrsucting our custom bounce
dim = 1
xmin = 0
xmax = 10
xkink = (xmax + xmin) / 2
npoints = 1000
dx = (xmax - xmin) / (npoints - 1)

# we are calling this R, but really it is just x
R = np.arange(0, npoints) * dx + xmin
arg = (R - xkink) / np.sqrt(2)
Phi = np.tanh(arg)
dPhi = 1 / np.cosh(arg) / np.sqrt(2)

# creating bubble config instance
bub_config = BubbleConfig(
    V=V,
    phi_metaMin=1,  # phi on right
    R=R,
    Phi=Phi,
    dim=1,
    dV=dV,
    d2V=ddV,
)

# creating particle instance
higgs = ParticleConfig(
    W_Phi=ddV,
    spin=0,
    dof_internal=1,
    zero_modes="Higgs",
)

# creating bubble determinant instance
bub_det = BubbleDeterminant(bub_config, higgs)

log_phi_inf, log_phi_inf_err = bub_det.findLogPhiInfinity()
ddphi_0 = dV(Phi[0]) / dim
m0 = np.sqrt(ddV(1))
dM = -(dim / 2) / m0 * (
    (dim / 2 - 1) * np.log(2 * np.pi) + np.log(abs(ddphi_0)) + log_phi_inf
)
dM_err = (dim / 2) / m0 * log_phi_inf_err

# printing results
print("Kink one-loop mass:")
print(
    "%-12s %-12s %-12s %-12s"
    % ("Numerical", "Error", "Analytical", "Difference")
)
print(
    "%-12g %-12g %-12g %-12g"
    % (
        dM,
        dM_err,
        dM_analytic,
        abs(dM - dM_analytic),
    )
)
