import pytest  # for tests
import numpy as np  # arrays and maths
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant
from .conftest import profile_object, ddV4, ddV6
from .data.ekstedt_fits import (  # 3d results
    omega_V4_fit,
    omega_V6_fit,
)

@pytest.mark.parametrize(
    "dim, alpha",
    [
        (3, 0.05),
        (3, 0.1),
        (3, 0.3),
        (3, 0.5),
        (3, 0.7),
        (3, 0.9),
    ],
)
def test_findNegativeEigenvalue_V4_3d(cosmo_transitions_V4, dim, alpha):
    """
    Tests that the negative eigenvalue agrees with Eq. (6.10) in
    Eur.Phys.J.C 82 (2022) 2, 173, arXiv:2104.11804 [hep-ph].
    """
    ct_prof = profile_object(cosmo_transitions_V4, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V4, ct_prof)
    higgs = ParticleConfig(W_Phi=lambda phi: ddV4(phi, alpha))
    bd = BubbleDeterminant(bubble, higgs)
    eig, err = bd.findNegativeEigenvalue()
    assert eig == pytest.approx(-omega_V4_fit(alpha), rel=0.01)


@pytest.mark.parametrize(
    "dim, alpha",
    [
        (3, 0.05),
        (3, 0.1),
        (3, 0.3),
        (3, 0.5),
        (3, 0.7),
        (3, 0.9),
    ],
)
def test_findNegativeEigenvalue_V6_3d(cosmo_transitions_V6, dim, alpha):
    """
    Tests that the negative eigenvalue agrees with Eq. (6.19) in
    Eur.Phys.J.C 82 (2022) 2, 173, arXiv:2104.11804 [hep-ph].
    """
    ct_prof = profile_object(cosmo_transitions_V6, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V6, ct_prof)
    higgs = ParticleConfig(W_Phi=lambda phi: ddV6(phi, alpha))
    bd = BubbleDeterminant(bubble, higgs)
    eig, err = bd.findNegativeEigenvalue()
    assert eig == pytest.approx(-omega_V6_fit(alpha), rel=0.05)
