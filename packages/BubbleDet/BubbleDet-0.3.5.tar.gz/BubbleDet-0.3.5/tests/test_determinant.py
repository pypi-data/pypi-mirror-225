import pytest  # for tests
import os  # for path names
import numpy as np  # arrays and maths
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant
from .data.ekstedt_fits import (  # 3d results
    SH1_V4_fit,
    SG1_V4_fit,
    SH1_V6_fit,
    SG1_V6_fit,
)
from .data.scaleless_results import S1_scaleless # scaleless results
from .conftest import (
    profile_object,
    ddV4,
    dV4onPhi,
    ddV6,
    dV6onPhi,
    bubbleConfig_scaleless,
    ddV_scaleless,
)


real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)


@pytest.mark.parametrize(
    "dim, alpha",
    [
        (3, 0.3),
        (3, 0.5),
        (3, 0.7),
        (3, 0.9),
        (3, 0.95),
    ],
)
def test_findDeterminant_Higgs_V4_3d(cosmo_transitions_V4, dim, alpha):
    """
    Tests that the one-loop determinant agrees with Table 1 in
    Eur.Phys.J.C 82 (2022) 2, 173, arXiv:2104.11804 [hep-ph].
    """
    ct_prof = profile_object(cosmo_transitions_V4, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V4, ct_prof)
    higgs = ParticleConfig(W_Phi=lambda phi: ddV4(phi, alpha))
    bd = BubbleDeterminant(bubble, higgs)
    S1, err = bd.findDeterminant()
    assert S1 == pytest.approx(SH1_V4_fit(alpha), rel=0.01)


@pytest.mark.parametrize(
    "dim, alpha",
    [
        (3, 0.3),
        (3, 0.5),
        (3, 0.7),
        (3, 0.9),
        (3, 0.95),
    ],
)
def test_findDeterminant_Higgs_V6_3d(cosmo_transitions_V6, dim, alpha):
    """
    Tests that the one-loop determinant agrees with Table 2 in
    Eur.Phys.J.C 82 (2022) 2, 173, arXiv:2104.11804 [hep-ph].
    """
    ct_prof = profile_object(cosmo_transitions_V6, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V6, ct_prof)
    higgs = ParticleConfig(W_Phi=lambda phi: ddV6(phi, alpha))
    bd = BubbleDeterminant(bubble, higgs)
    S1, err = bd.findDeterminant()
    assert S1 == pytest.approx(SH1_V6_fit(alpha), rel=0.05)


@pytest.mark.parametrize(
    "dim, alpha",
    [
        (3, 0.3),
        (3, 0.5),
        (3, 0.7),
        (3, 0.9),
        (3, 0.95),
    ],
)
def test_findDeterminant_Goldstone_V4_3d(cosmo_transitions_V4, dim, alpha):
    """
    Tests that the one-loop determinant agrees with Table 1 in
    Eur.Phys.J.C 82 (2022) 2, 173, arXiv:2104.11804 [hep-ph].
    """
    ct_prof = profile_object(cosmo_transitions_V4, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V4, ct_prof)
    goldstone = ParticleConfig(
        W_Phi=lambda phi: dV4onPhi(phi, alpha),
        zero_modes="Goldstone",
    )
    bd = BubbleDeterminant(bubble, goldstone)
    S1, err = bd.findDeterminant()
    assert S1 == pytest.approx(SG1_V4_fit(alpha), rel=0.01)


@pytest.mark.parametrize(
    "dim, alpha",
    [
        (3, 0.3),
        (3, 0.5),
        (3, 0.7),
        (3, 0.9),
        (3, 0.95),
    ],
)
def test_findDeterminant_Goldstone_V6_3d(cosmo_transitions_V6, dim, alpha):
    """
    Tests that the one-loop determinant agrees with Table 2 in
    Eur.Phys.J.C 82 (2022) 2, 173, arXiv:2104.11804 [hep-ph].
    """
    ct_prof = profile_object(cosmo_transitions_V6, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V6, ct_prof)
    goldstone = ParticleConfig(
        W_Phi=lambda phi: dV6onPhi(phi, alpha),
        zero_modes="Goldstone",
    )
    bd = BubbleDeterminant(bubble, goldstone)
    S1, err = bd.findDeterminant()
    assert S1 == pytest.approx(SG1_V6_fit(alpha), rel=0.01)


@pytest.mark.parametrize(
    "dim, alpha",
    [
        (4, 0.05),
        (4, 0.1),
        (4, 0.3),
        (4, 0.5),
        (4, 0.7),
        (4, 0.9),
        (4, 0.95),
    ],
)
def test_findDeterminant_Higgs_V4_4d(cosmo_transitions_V4, dim, alpha):
    """
    Tests that the one-loop determinant agrees with Table 1 in
    Phys.Rev.D 69 (2004) 025009, arXiv:hep-th/0307202.
    """
    ct_prof = profile_object(cosmo_transitions_V4, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V4, ct_prof)
    higgs = ParticleConfig(W_Phi=lambda phi: ddV4(phi, alpha))
    bd = BubbleDeterminant(bubble, higgs)
    S1, err = bd.findDeterminant()
    S0 = cosmo_transitions_V4.findAction(ct_prof)
    res = S1 + (dim / 2) * np.log(S0 / 2 / np.pi)
    data_bl = np.loadtxt(dir_path + "/data/baacke_lavrelashvili_table1")
    index = np.where(abs(data_bl[:, 0] - alpha) < 1e-12)[0]
    assert res == pytest.approx(data_bl[index, 3][0], rel=0.01)


@pytest.mark.parametrize(
    "dim, Lambda, RScale",
    [
        (3, 0.1, 1),
        (4, 0.1, 1),
        (6, 0.1, 1),
    ],
)
def test_findDeterminant_Higgs_scaleless(dim, Lambda, RScale):
    """
    Tests bubble_det for a scaleless potential in four dimensions.
    """
    bubble = bubbleConfig_scaleless(dim, Lambda, RScale)
    higgs = ParticleConfig(
        W_Phi=lambda phi: ddV_scaleless(phi, dim, Lambda),
        spin=0,
        dof_internal=1,
        zero_modes="Higgs",
    )
    mu = 1 / RScale
    bd = BubbleDeterminant(bubble, higgs, renormalisation_scale=mu)
    res, err = bd.findDeterminant()
    analytic = S1_scaleless(dim, Lambda, RScale, mu)
    assert res == pytest.approx(analytic, rel=0.01)
