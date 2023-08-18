import pytest  # for tests
import numpy as np  # arrays and maths
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant
from .conftest import profile_object


@pytest.mark.parametrize(
    "dim, alpha, g",
    [
        (2, 0.5, 4),
        (3, 0.5, 4),
        (4, 0.5, 4),
        (5, 0.5, 4),
        (6, 0.5, 4),
        (7, 0.5, 4),
    ],
)
def test_findDerivativeExpansion_V4(cosmo_transitions_V4, dim, alpha, g):
    """
    Tests that the derivative expansion agrees with the full result when
    the fluctuating particle is much heavier than the Higgs.
    """
    ct_prof = profile_object(cosmo_transitions_V4, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V4, ct_prof)
    gauge = ParticleConfig(
        W_Phi=lambda phi: g**2 * phi**2,
        spin=1,
        zero_modes="None",
    )
    bd = BubbleDeterminant(bubble, gauge, gauge_groups=["U1", "None"])
    S1, err = bd.findDeterminant()
    S1_DE, S1_DE_err = bd.findDerivativeExpansion(gauge)
    assert S1_DE == pytest.approx(S1, rel=0.02)


@pytest.mark.parametrize(
    "dim, alpha, g",
    [
        (2, 0.5, 4),
        (3, 0.5, 4),
        (4, 0.5, 4),
        (5, 0.5, 4),
        (6, 0.5, 4),
        (7, 0.5, 4),
    ],
)
def test_findDerivativeExpansion_V6(cosmo_transitions_V6, dim, alpha, g):
    """
    Tests that the derivative expansion agrees with the full result when
    the fluctuating particle is much heavier than the Higgs.
    """
    ct_prof = profile_object(cosmo_transitions_V6, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V6, ct_prof)
    gauge = ParticleConfig(
        W_Phi=lambda phi: g**2 * phi**2,
        spin=1,
        zero_modes="None",
    )
    bd = BubbleDeterminant(bubble, gauge, gauge_groups=["U1", "None"])
    S1, err = bd.findDeterminant()
    S1_DE, S1_DE_err = bd.findDerivativeExpansion(gauge)
    assert S1_DE == pytest.approx(S1, rel=0.02)
