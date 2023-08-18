import numpy as np  # arrays and maths
from scipy import special # for special functions etc
from scipy.special import zeta
from .helpers import simpson  # integrator
from cosmoTransitions.helper_functions import deriv14  # derivatives for arrays


def findWKB(config, l_max, W_inf, a_inf, separate_orders=False):
    r"""Terms in the WKB approximation of determinant

    Full docs in BubbleDet.py.
    """
    R = config.R
    DW = config.Delta_W
    dWR = deriv14(DW, R)
    d2WR = deriv14(dWR, R)
    d3WR = deriv14(d2WR, R)
    m0 = config.m_W_meta
    dim = config.dim
    l_bar = lambda l: (l + dim / 2 - 1)

    """
        Terms that come with l**-1
    """
    l1num=1/2*R*DW #checked

    """
        Terms that come with l**-3
    """
    l3num=-1/8*R**3*DW*(DW+2*m0**2)

    """
        Terms that come with l**-5
    """
    l5num1=1/16*R**5*DW*(3*m0**4+3*m0**2*DW+DW**2)
    l5num2=1/32*(R**5*dWR**2-4*DW**2*R**3-8*DW*R**3*m0**2)

    """
        Terms that come with l**-7
    """
    l7num1=-5/16/8*R**7*DW*(2*m0**2+DW)*(2*m0**4+2*DW*m0**2+DW**2)
    l7num2=1/64*m0**4*60*R**5*DW
    l7num3=0
    l7num4=1/64*(20*DW**3*R**5-5*R**7*DW*dWR**2)
    l7num5=-32/128*R**3*DW*m0**2
    l7num6=1/128*(-R**7*d2WR**2+13*R**5*dWR**2-16*R**3*DW**2)

    """
        Terms that come with l**-9
    """
    l9num1=7/256*R**9*DW*(
        5*m0**8+10*m0**6*DW+10*m0**4*DW**2+5*m0**2*DW**3+DW**4
    )
    l9num2=-560/256*m0**6*R**7*DW
    l9num3=35/256*m0**4*(R**9*dWR**2-24*R**7*DW**2)
    l9num4=70/256*m0**2*(R**9*dWR**2*DW-8*R**7*DW**3)
    l9num5=35/256*(R**9*dWR**2*DW**2-4*R**7*DW**4)
    l9num6=1008/256*m0**4*(R**5*DW)
    l9num7=7/256*m0**2*(R**9*d2WR**2-31*R**7*dWR**2+144*R**5*DW**2)
    l9num8=7/256*(
        -5*R**8*dWR**3 +DW*(R**9*d2WR**2-31*R**7*dWR**2) +48*R**5*DW**3
    )
    l9num9=-64/256*m0**2*(R**3*DW)
    l9num10=1/512*(R**9*d3WR**2-29*R**7*d2WR**2+133*R**5*dWR**2-64*R**3*DW**2)
    """
        All the integrals
    """
    l1Int=simpson(l1num, x=R)
    l3Int=simpson(l3num, x=R)
    l5Int=simpson(l5num1 + l5num2, x=R)
    l7Int = simpson(
        l7num1 + l7num2 + l7num3 + l7num4 + l7num5 + l7num6, x=R
    )
    l9Int = simpson(
        l9num1
        + l9num2
        + l9num3
        + l9num4
        + l9num5
        + l9num6
        + l9num7
        + l9num8
        + l9num9
        + l9num10,
        x=R,
    )

    """
        Improved calculation for non-exponential bounces by doing the integration
        analytically from r=R to r=inf
    """
    if config.massless_Higgs:
        if a_inf == 2:
            raise ValueError("Divergent contribution from large r, {a_inf=}")
        l1Int=l1Int+W_inf/2*R[-1]**(2-a_inf)/(a_inf-2)
        l3Int=l3Int-1/16*R[-1]**(4-2*a_inf)*W_inf**2/(a_inf-2)
        l5Int=l5Int + (
            1/48*R[-1]**(6-3*a_inf)*W_inf**3/(a_inf-2)
            + 1/64*R[-1]**(4-2*a_inf)*W_inf**2*(2+a_inf)
        )


    # Adding appropiate prefactors
    if dim>2:
        WKB1 = np.array([l1Int / l_bar(l) ** 1 for l in range(l_max)])
        WKB3 = np.array([l3Int / l_bar(l) ** 3 for l in range(l_max)])
        WKB5 = np.array([l5Int / l_bar(l) ** 5 for l in range(l_max)])
        WKB7 = np.array([l7Int / l_bar(l) ** 7 for l in range(l_max)])
        WKB9 = np.array([l9Int / l_bar(l) ** 9 for l in range(l_max)])
    else:
        WKB1 = np.array([0] + [l1Int / l_bar(l) ** 1 for l in range(1, l_max)])
        WKB3 = np.array([0] + [l3Int / l_bar(l) ** 3 for l in range(1, l_max)])
        WKB5 = np.array([0] + [l5Int / l_bar(l) ** 5 for l in range(1, l_max)])
        WKB7 = np.array([0] + [l7Int / l_bar(l) ** 7 for l in range(1, l_max)])
        WKB9 = np.array([0] + [l9Int / l_bar(l) ** 9 for l in range(1, l_max)])


    # Contributions from sums
    l1Sum=1/2*l1Int*_NLOWKB_Fac(dim,1)
    l3Sum=1/2*l3Int*_NLOWKB_Fac(dim,3)
    l5Sum=1/2*l5Int*_NLOWKB_Fac(dim,5)
    l7Sum=1/2*l7Int*_NLOWKB_Fac(dim,7)
    l9Sum=1/2*l9Int*_NLOWKB_Fac(dim,9)

    # These are sums that formally diverge, but that are finite in dim-reg
    if dim==2:
        l1Sum=-1/2*l1Int*(2)
    elif dim==3:
        l1Sum=-1/2*l1Int*(4)
    elif dim==4:
        l1Sum=-1/2*l1Int*(3)
        l3Sum=-1/2*l3Int*(3/2)
    elif dim==5:
        l1Sum=-1/2*l1Int*(8/3)
        l3Sum=-1/2*l3Int*(416/675 + np.pi**2/24)
    elif dim==6:
        l1Sum=-1/2*l1Int*(5/2)
        l3Sum=-1/2*l3Int*(829/2592 + zeta(3)/12)
        l5Sum=0
    elif dim==7:
        l1Sum=-1/2*l1Int*(12/5)
        l3Sum=-1/2*l3Int*(0.1810015354923426)
        l5Sum=-1/2*l5Int*(0.07698283370702798)
    elif dim==9:
        l1Sum=-1/2*l1Int*(16/7)
        l3Sum=-1/2*l3Int*(5*np.pi**2/7168 + 3392/27783)
        l5Sum=-1/2*l5Int*(
            5*np.pi**4/21504 - 37*np.pi**2/11520 + 747776/110270727
        )
        l7Sum=-1/2*l7Int*(
            np.pi**6/10752
            - 37*np.pi**4/34560
            + np.pi**2/576
            + 173437952/437664515463
        )

    # Error estimate for WKB, assumed dominated by WKB9
    l9IntHalf = simpson(
        l9num1[::2]
        + l9num2[::2]
        + l9num3[::2]
        + l9num4[::2]
        + l9num5[::2]
        + l9num6[::2]
        + l9num7[::2]
        + l9num8[::2]
        + l9num9[::2]
        + l9num10[::2],
        x=R[::2],
    )
    l9IntErr = abs(l9Int - l9IntHalf) / 7
    WKB_err = l9IntErr * _WKBErr9(dim, l_max)

    # returning results
    if separate_orders:
        return WKB1, WKB3, WKB5, WKB7, WKB9
    else:
        return (
            WKB1 + WKB3 + WKB5 + WKB7 + WKB9,
            WKB_err,
            l1Sum + l3Sum + l5Sum + l7Sum + l9Sum
        )


def _NLOWKB_Fac(dim, a):
    r"""
    Returns  :math:`{\rm deg}(l) \bar{l}^{-a}`` from :math:`l=2` to
    :math:`l=\infty`
    """
    WKBSums = np.array(
        [
            [
                1.289868133696453,
                0.4041138063191886,
                0.1646464674222764,
                0.07385551028673985,
                0.03468612396889828,
                0.01669855476384565,
                0.008154712395888679,
                0.004016785652164429,
                0.001989150255636171,
            ],
            [
                0,
                0.9807155122004697,
                0.2362040516417274,
                0.07463528293908402,
                0.02614633329222761,
                0.009642819642786391,
                0.003661128076527876,
                0.001414776330366322,
                0.0005528785085252943,
            ],
            [
                0,
                0,
                0.3949340668482264,
                0.07705690315959429,
                0.01982323371113819,
                0.005677755143369926,
                0.001718061984449140,
                0.0005367773819228268,
                0.0001711061979443394,
            ],
            [
                0,
                0,
                0,
                0.1091427819109498,
                0.01779791138644508,
                0.003845429671397903,
                0.0009283752121826075,
                0.0002374675933658018,
                0.00006286340823275867,
            ],
            [
                0,
                0,
                0,
                0,
                0.02302878341986023,
                0.003204778109719657,
                0.0005942695689021855,
                0.0001235832329021798,
                0.00002730245535815164,
            ],
            [
                0,
                0,
                0,
                0,
                0,
                0.003936546209219022,
                0.0004746013441527956,
                0.00007674151823083812,
                0.00001397095258711521,
            ],
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0.0005663198589750497,
                0.00005983059447869792,
                0.000008539263717735965,
            ],
            [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0.00007041336847112568,
                0.000006577898215269628,
            ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0.000007716472955632608],
        ]
    )

    if a<2:
        return 0
    else:
        return WKBSums[dim-2][a-2]


def _WKBErr9(dim, L):
    """
    Returns  deg(l) lb ** -9 from l=L to l=inf
    """
    if dim == 2:
        return -(special.polygamma(8, L) / 20160)
    elif dim == 3:
        return special.polygamma(7, L + 1 / 2) / 2520
    elif dim == 4:
        return -(1 / 720) * special.polygamma(6, L + 1)
    elif dim == 5:
        return (
            168 * special.polygamma(5, L + 3 / 2)
            - special.polygamma(7, L + 3 / 2)
        ) / 60480
    elif dim == 6:
        return (
            special.polygamma(6, L + 2) - 30 * special.polygamma(4, L + 2)
        ) / 8640
    elif dim == 7:
        return (
            4480 * special.polygamma(3, L + 5 / 2)
            - 560 * special.polygamma(5, L + 5 / 2)
            + 3 * special.polygamma(7, L + 5 / 2)
        ) / 1612800
    elif dim == 8:
        return (
            -180 * special.polygamma(2, L + 3)
            + 75 * special.polygamma(4, L + 3)
            - 2 * special.polygamma(6, L + 3)
        ) / 129600
    elif dim == 9:
        return (
            107520 * special.polygamma(1, L + 7 / 2)
            - 156800 * special.polygamma(3, L + 7 / 2)
            + 14504 * special.polygamma(5, L + 7 / 2)
            - 75 * special.polygamma(7, L + 7 / 2)
        ) / 270950400
