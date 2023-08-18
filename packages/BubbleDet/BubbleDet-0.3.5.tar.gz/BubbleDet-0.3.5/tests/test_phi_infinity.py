import pytest  # for tests
import numpy as np  # arrays and maths
from BubbleDet import BubbleConfig, ParticleConfig, BubbleDeterminant
from .conftest import bubbleConfig_scaleless, ddV_scaleless


@pytest.mark.parametrize(
    "dim, Lambda, RScale",
    [
        (3, 1, 5),
        (3, 10, 10),
        (3, 0.1, 20),
        (4, 1, 5),
        (4, 10, 10),
        (4, 0.1, 20),
        (6, 1, 5),
        (6, 10, 10),
        (6, 0.1, 20),
    ],
)
def test_findLogPhiInfinity_scaleless(dim, Lambda, RScale):
    """
    Tests logPhiInfinity for the scaleless potential, where the exact solution
    is known.
    """
    bubble = bubbleConfig_scaleless(dim, Lambda, RScale)
    higgs = ParticleConfig(W_Phi=lambda phi: ddV_scaleless(dim, phi, Lambda))
    bd = BubbleDeterminant(bubble, higgs)
    res, err = bd.findLogPhiInfinity()
    if dim == 3:
        analytic = np.log((12 / Lambda / np.pi ** 2) ** 0.25 * RScale ** 0.5)
    elif dim == 4:
        analytic = np.log((8 / Lambda) ** 0.5 * RScale)
    elif dim == 6:
        analytic = np.log(12 / Lambda * RScale ** 2)
    assert res == pytest.approx(analytic, rel=0.001)
