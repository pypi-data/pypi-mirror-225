# Volumes of common Lie group manifolds
import numpy as np  # maths
import re  # string manipulations


def group_volume(group_name):
    r"""Computes group volumes.

    Applies to the simple Lie groups SU(N), U(N), SO(N) and SP(N).

    Parameters
    ----------
    group_name : string
        Name of group, e.g. \"U2\" or \"SO3\".

    Returns
    -------
    volume : float
        The volume of the group.

    Examples
    --------
    >>> from BubbleDet.group_volumes import group_volume
    >>> group_volume("U1")
    6.283185307179586

    """
    if group_name == "None" or group_name is None:
        return 1
    group = re.split(r"(\d+)", group_name)
    if group[0] == "SU":
        return __SU(int(group[1]))
    elif group[0] == "U":
        return __U(int(group[1]))
    elif group[0] == "SO":
        return __SO(int(group[1]))
    elif group[0] == "SP":
        return __SP(int(group[1]))
    else:
        raise ValueError("Group not supported")


def __SU(n):
    """Calculates the volume of SU(n)"""
    fac1 = np.sqrt(n * 2 ** (n - 1)) * np.pi ** ((n - 1) * (n + 2) / 2)
    fac2 = 1
    for k in range(1, n):
        fac2 *= np.math.factorial(k)
    return fac1 / fac2


def __U(n):
    """Calculates the volume of U(n)"""
    fac1 = np.sqrt(n * 2 ** (n + 1)) * np.pi ** (n * (n + 1) / 2)
    fac2 = 1
    for k in range(1, n):
        fac2 *= np.math.factorial(k)
    return fac1 / fac2


def __SO(n):
    """Calculates the volume of SO(n)"""
    if n % 2 == 0:
        m = round(n / 2)
        fac1 = 2 ** (m - 1) * (2 * np.pi) ** (m**2)
        fac2 = 1
        for k in range(1, m):
            fac2 *= np.math.factorial(2 * k)
    else:
        m = round((n - 1) / 2)
        fac1 = 2**m * (2 * np.pi) ** (m * (m + 1))
        fac2 = 1
        for k in range(1, m):
            fac2 *= np.math.factorial(2 * k + 1)
    return fac1 / fac2


def __SP(n):
    """Calculates the volume of SP(n)"""
    m = round(n)
    fac = 1
    for k in range(1, m + 1):
        fac *= 2 * np.pi ** (2 * k) / np.math.factorial(2 * k - 1)
    return fac
