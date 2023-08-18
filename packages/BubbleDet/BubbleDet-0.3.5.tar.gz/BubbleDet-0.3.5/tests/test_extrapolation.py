import pytest # for tests
import numpy as np # for log
from scipy.special import zeta # zeta function
from BubbleDet.extrapolation import ( # to test
    richardson_extrapolation,
    fit_extrapolation,
    shanks_extrapolation,
    epsilon_extrapolation,
)


@pytest.mark.parametrize("power, length", [(2, 31)])
def test_richardson_extrapolation(power, length):
    """
    See Bender and Orszag, Chapter 8, Table 8.4.
    """
    zeta_list = [1 / (i + 1) ** power for i in range(length)]
    res, err = richardson_extrapolation(zeta_list)
    assert res == pytest.approx(zeta(power), rel=1e-8)


@pytest.mark.parametrize("power, length", [(2, 31)])
def test_fit_extrapolation(power, length):
    """
    Same test as for Richardson extrapolation, but fit extrapolation is less
    accurate.
    """
    zeta_list = [1 / (i + 1) ** power for i in range(length)]
    res, err = fit_extrapolation(zeta_list)
    assert res == pytest.approx(zeta(power), rel=1e-6)


@pytest.mark.parametrize("length", [25])
def test_shanks_extrapolation(length):
    """
    See Bender and Orszag, Chapter 8, Table 8.2.
    """
    ln2_list = [(-1) ** i / (i+1) for i in range(length)]
    res, err = shanks_extrapolation(ln2_list)
    assert res == pytest.approx(np.log(2), rel=1e-8)


@pytest.mark.parametrize("length", [21])
def test_epsilon_extrapolation(length):
    """
    See Graves-Morris et al., Table 1.
    """
    arctan_list = [4 * (-1) ** i / (2*i+1) for i in range(length)]
    res, err = epsilon_extrapolation(arctan_list, False)
    assert res == pytest.approx(np.pi, rel=1e-12)
