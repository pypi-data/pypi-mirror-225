import numpy as np

# Fits from Eur.Phys.J.C 82 (2022) 2, 173, arXiv:2104.11804 [hep-ph].
def f_fit(alpha, A, B, C, D, E, F):
    return (
        A
        + B * alpha
        + C * alpha ** 2
        + D / (1 - alpha)
        + E / (1 - alpha) ** 2
        + F / (1 - alpha) ** 3
    )


def S0_V4_fit(alpha):
    return f_fit(alpha, 7.24, 5.68, 0, 10.4, 1.25, 0)
    #return f_fit(alpha, 7.24, 5.68, 0, 272 * np.pi / 81, 32 * np.pi / 81, 0)


def S0_V6_fit(alpha):
    return f_fit(alpha, 1.76, -0.142, 0, 12.6, 4.19, 0)


def SH1_V4_fit(alpha):
    return f_fit(alpha, 0.213, 4.86, -9.56, 3.97, 0.505, 8.78e-4)
    #return f_fit(alpha, 0.213, 4.86, -9.56, 3.97, 0.505, 0)


def SH1_V6_fit(alpha):
    if alpha <= 0.8:
        return f_fit(alpha, -2.65, 5.32, 0, 0.533, 1.25, -0.845)
    else:
        return f_fit(alpha, 5.30, -28.8, 0, 8.14, 0.119, -0.765)


def SG1_V4_fit(alpha):
    return f_fit(alpha, 0.895, 1.08, -1.84, 1.51, 0.469, 0.0329)
    #return f_fit(alpha, 0.895, 1.08, -1.84, 1.51, 0.469, 8 / 243)


def SG1_V6_fit(alpha):
    if alpha <= 0.8:
        return f_fit(alpha, -0.289, -0.155, 0, -0.5441, 0.424, 0.106)
    else:
        return f_fit(alpha, -0.0839, -1.70, 0, 0.304, 0.296, 0.113)


def omega_V4_fit(alpha):
    return (1 - alpha) * (
        2.39
        - 0.854 * alpha
        + 2.42 * alpha ** 2
        - 9.67 * alpha ** 3
        + 5.85 * alpha ** 4
    )


def omega_V6_fit(alpha):
    if alpha <= 0.6:
        return (1 - alpha) * (
            15.2
            - 75.5 * alpha
            + 163 * alpha ** 2
            - 167 * alpha ** 3
            + 65.6 * alpha ** 4
        )
    else:
        return (1 - alpha) * (
            8.81
            - 30.7 * alpha
            + 46.0 * alpha ** 2
            - 33.4 * alpha ** 3
            + 9.31 * alpha ** 4
        )
