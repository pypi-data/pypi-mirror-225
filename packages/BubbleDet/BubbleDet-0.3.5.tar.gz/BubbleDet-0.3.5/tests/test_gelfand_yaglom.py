import pytest  # for tests
import os  # for path names
import numpy as np  # arrays and maths
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant
from .conftest import profile_object, ddV4

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)


@pytest.mark.parametrize(
    "dim, alpha, l",
    [
        (4, 0.7, 0),
        (4, 0.7, 2),
        (4, 0.7, 5),
        (4, 0.7, 10),
        (4, 0.7, 19),
        (4, 0.7, 39),
        (4, 0.7, 59),
        (4, 0.7, 79),
        (4, 0.7, 99),
    ],
)
def test_findGelfandYaglomTl_4d(cosmo_transitions_V4, dim, alpha, l):
    """
    Tests that the Tl, computed using the Gelfand-Yaglom method agree
    with Fig. 6 of Phys.Rev.D 72 (2005) 125004, arXiv:hep-th/0511156.
    """
    ct_prof = profile_object(cosmo_transitions_V4, dim, alpha)
    bubble = BubbleConfig.fromCosmoTransitions(cosmo_transitions_V4, ct_prof)
    higgs = ParticleConfig(W_Phi=lambda phi: ddV4(phi, alpha))
    bd = BubbleDeterminant(bubble, higgs)
    res, err, TlD = bd.findGelfandYaglomTl(higgs, l)
    data_dm = np.loadtxt(dir_path + "/data/dunne_min_fig6_alpha0.7")
    index = np.where(data_dm[:, 0] == l + 1)
    assert np.log(abs(res)) == pytest.approx(data_dm[index, 1][0], abs=0.01)
