import sys
import numpy as np
from scipy import special
from math import log, exp, sqrt  # for quicker single computations
from scipy.optimize import curve_fit  # for phi(infinity)


def findLogPhiInfinity(bubble, tail=0.007, log_phi_inf_tol=0.001):
    r"""Constant :math:`\log\phi_\infty` in asyptotics of background field

    Full docs in BubbleDet.py.
    """

    if bubble.massless_Higgs:
        return _logPhiInfMasslessHiggs(bubble)

    estimate1, error1 = _logPhiInfinityMainMethod(
        bubble,
        tail,
        log_phi_inf_tol,
    )

    estimate2, error2 = _geometricRadialLogPhiInf(bubble, bubble.m_Higgs_meta)

    if estimate2 == 0 or error2 == np.inf:
        new_tol = np.inf
    else:
        new_tol = error2 / estimate2

    estimate3, error3 = _logPhiInfinityMainMethod(bubble, tail, new_tol)

    # Ordered with a preference on the extrapolating method
    estimates = [estimate1, estimate3, estimate2]
    errors = [error1, error3, error2]

    smallestError = errors.index(min(errors))

    return estimates[smallestError], errors[smallestError]


def _logPhiInfinityMainMethod(bubble, tail, log_phi_inf_tol):

    [
        deviationsFromQuadratic,
        logPhiInfs,
        errsFromBCs,
    ] = _getFitPoints(bubble, tail, log_phi_inf_tol)

    if logPhiInfs is None:
        return None, np.inf

    # First fitting a quadratic through the points to get a proper
    # error estimate for the linear fit.
    log_phi_infinity_quad, pcov = curve_fit(
        lambda x, phi_inf, a, b: b * x**2 + a * x + phi_inf,
        deviationsFromQuadratic,
        logPhiInfs,
        sigma=errsFromBCs,
    )
    errsFromQuad = np.abs(
        log_phi_infinity_quad[2] * np.array(deviationsFromQuadratic) ** 2
    )

    errs = np.sqrt(np.power(errsFromQuad, 2) + np.power(errsFromBCs, 2))

    # Finally fitting the linear behavior to obtain the correct value.
    log_phi_infinity, pcov = curve_fit(
        lambda x, phi_inf, a: a * x + phi_inf,
        deviationsFromQuadratic,
        logPhiInfs,
        sigma=errs,
        absolute_sigma=True,
    )

    return log_phi_infinity[0], max(
        np.sqrt(pcov[0][0]),
        abs(log_phi_infinity[0] - log_phi_infinity_quad[0]),
    )


def findPhiInfinityUnbounded(bubble):
    """
    Only a crude estimate for now
    """
    return bubble.R[-1] ** (bubble.dim - 2) * bubble.Phi[-1]


def _getFitPoints(bubble, tail, log_phi_inf_tol):
    R = bubble.R
    phi = bubble.Phi
    phi_meta = bubble.phi_metaMin

    Vmeta = bubble.V(phi_meta)
    VFullList = bubble.V(phi)
    Vlist = VFullList - Vmeta

    d2V_m = bubble.m_Higgs_meta**2
    phi_redef = phi - phi_meta
    quadVlist = 0.5 * d2V_m * np.power(phi_redef, 2)

    DeltaVlist = np.abs(Vlist - quadVlist)

    lastAllowedIndex = len(phi) - 2

    phi_midpoint = 0.5 * (bubble.Phi[0] + bubble.Phi[-1])
    firstAllowedIndex = np.argmin(abs(bubble.Phi - phi_midpoint))

    if quadVlist[firstAllowedIndex] == 0:
        maxProportionalDeviation = np.inf
    else:
        maxProportionalDeviation = (
            DeltaVlist[firstAllowedIndex] / quadVlist[firstAllowedIndex]
        )

    # Set the tail so that it is possible to find the points
    if 8 * tail > maxProportionalDeviation:
        tail = maxProportionalDeviation / 8

    # Loop attempts to get the fit points until not possible to get 4
    while lastAllowedIndex - 3 >= firstAllowedIndex:
        [
            fitDeviationsFromQuadratic,
            fitLogPhiInfs,
            fitLogPhiInfBCErrs,
            lastAllowedIndex,
            success,
        ] = _tryGetFitPoints(
            bubble,
            tail,
            DeltaVlist,
            quadVlist,
            Vmeta,
            firstAllowedIndex,
            lastAllowedIndex,
            log_phi_inf_tol,
        )

        if success:
            return [
                fitDeviationsFromQuadratic,
                fitLogPhiInfs,
                fitLogPhiInfBCErrs,
            ]

    return [None, None, None]


def _tryGetFitPoints(
    bubble,
    tail,
    DeltaVlist,
    quadVlist,
    Vmeta,
    firstAllowedIndex,
    lastAllowedIndex,
    log_phi_inf_tol,
):

    fitDeviationsFromQuadratic = []
    fitLogPhiInfs = []
    fitLogPhiInfBCErrs = []
    firstFitIndex = 0

    tailVar = tail
    tailMultiple = 1

    for i in range(lastAllowedIndex, firstAllowedIndex - 1, -1):

        if not _validTailPoint(
            tailVar, DeltaVlist, quadVlist, Vmeta, tailMultiple, i
        ):
            return [None, None, None, i - 1, False]

        proportionalDeviation = DeltaVlist[i] / quadVlist[i]

        if proportionalDeviation >= tailMultiple * tailVar:
            fitDeviationsFromQuadratic.append(proportionalDeviation)

            if tailMultiple == 1:
                firstFitIndex = i
            else:
                (
                    logPhiInfEstimate,
                    logPhiInfBCErr,
                ) = _directEstimateForLogPhiInfinity(bubble, i)

                if logPhiInfBCErr > np.abs(logPhiInfEstimate) * log_phi_inf_tol:
                    return [None, None, None, i - 1, False]

                fitLogPhiInfs.append(logPhiInfEstimate)
                fitLogPhiInfBCErrs.append(logPhiInfBCErr)

            if len(fitDeviationsFromQuadratic) == 4:
                (
                    logPhiInfEstimate,
                    logPhiInfBCErr,
                ) = _directEstimateForLogPhiInfinity(bubble, firstFitIndex)

                fitLogPhiInfs.insert(0, logPhiInfEstimate)
                fitLogPhiInfBCErrs.insert(0, logPhiInfBCErr)

                return [
                    fitDeviationsFromQuadratic,
                    fitLogPhiInfs,
                    fitLogPhiInfBCErrs,
                    lastAllowedIndex,
                    True,
                ]

            tailVar = proportionalDeviation / tailMultiple
            tailMultiple += 1

    return [None, None, None, i - 1, False]


def _directEstimateForLogPhiInfinity(bubble, index):
    Delta_phi = bubble.Phi[index] - bubble.phi_metaMin
    Delta_r = bubble.R[index] - bubble.R[-1]
    m0 = bubble.m_Higgs_meta

    # The estimate by a direct fit
    logPhiInf = log(np.abs(Delta_phi)) - _logPhiAsymptotic(
        bubble.dim, m0, bubble.R[index]
    )

    # A conservative error estimate due to the boundary conditions
    errBCs = abs(log(1 - exp(-2 * m0 * abs(Delta_r))))

    return logPhiInf, errBCs


def _validTailPoint(tail, DeltaVlist, quadVlist, Vmeta, tailMultiple, i):
    # The preceding point mustn't be exactly at the metastable phase
    if quadVlist[i + 1] == 0:
        return False

    # The tail must be receding from the metastable field value
    if quadVlist[i + 1] >= quadVlist[i]:
        return False

    # There can be large floating-point errors due to double cancellation
    #   in the potentials.
    if abs(Vmeta * 1e-13 / quadVlist[i] / tail) > 1:
        return False

    # The proportional deviations from the quadratic potential must be
    #   monotonously growing on the bubble tail.
    propDev = DeltaVlist[i] / quadVlist[i]

    prevPropDev = DeltaVlist[i + 1] / quadVlist[i + 1]
    if prevPropDev >= propDev:
        return False

    # The tail is assumed to be dense enough compared to the tail parameter
    #   that it shouldn't jump over multiples of the tail.
    #   This catches possible numerical inaccuracies in the calculation of
    #   the potential, which are intractable for the package.
    if tailMultiple > 1:
        if propDev >= (tailMultiple + 1) * tail:
            return False

    return True


def _logPhiAsymptotic(dim, m, r):
    r"""
    Logarithm of the asymptotic behaviour of field, as :math:`m R\to\infty`,
    up to the coefficient :math:`\phi_\infty`.
    """
    if m != 0:
        return (
            np.log(special.kve(dim / 2 - 1, m * r))
            - m * r
            - (dim / 2 - 1) * np.log(r)
            + (dim / 2 - 1) * np.log(m)
        )
    else:
        dRed = dim / 2 - 1
        return (
            special.gammaln(dRed)
            + (dRed - 1) * np.log(2)
            - 2 * dRed * np.log(r)
        )


def _geometricRadialLogPhiInf(bubble, mass):
    phi = bubble.Phi - bubble.phi_metaMin
    phiMid = 0.5 * (phi[0] + phi[-1])
    iMid = np.argmin(abs(phi - phiMid))
    rMid = bubble.R[iMid]
    rLast = bubble.R[-1]
    rFitsAnalytic = [
        (rMid * rMid * rLast) ** (1 / 3),
        (rMid * rLast) ** (1 / 2),
        (rMid * rLast * rLast) ** (1 / 3),
    ]
    rFits, phiFits = _geometricRadialFitPoints(
        bubble.R,
        phi,
        rFitsAnalytic,
    )
    estimates = _crudeLogValues(bubble, rFits, phiFits, mass)
    value = estimates[1]
    error = max(abs(estimates[0] - value), abs(estimates[2] - value))
    return value, error


def _geometricRadialFitPoints(r, phi, rFitsAnalytic):
    rFits = []
    phiFits = []
    for rFitAnalytic in rFitsAnalytic:
        iFit = np.argmin(abs(r - rFitAnalytic))
        rFits.append(r[iFit])
        phiFits.append(phi[iFit])
    return rFits, phiFits


def _crudeLogValues(bubble, rFits, phiFits, mass):
    estimates = []
    for i in range(3):
        estimate = np.log(np.abs(phiFits[i])) - _logPhiAsymptotic(
            bubble.dim, mass, rFits[i]
        )
        estimates.append(estimate)
    return estimates


def _logPhiInfMasslessHiggs(bubble):
    tValue, tError = _tailFitMasslessHiggsLogPhiInf(bubble)
    gValue, gError = _geometricRadialLogPhiInf(bubble, 0)
    if gError > tError:
        return tValue, tError
    else:
        return gValue, gError


def _tailFitMasslessHiggsLogPhiInf(bubble):
    popt, pcov = curve_fit(
        lambda r, phi_inf, Delta_phi: _tailFuncMasslessHiggs(
            r, phi_inf, Delta_phi, bubble.dim
        ),
        bubble.R[-5:],
        (bubble.Phi - bubble.phi_metaMin)[-5:],
    )
    linearValue = popt[0]
    if linearValue <= 0:
        return np.nan, np.inf
    value = np.log(linearValue)
    directErr = np.sqrt(pcov[0, 0])
    invTailBehavior = 1 / _tailFuncMasslessHiggs(bubble.R[-1], 1, 0, bubble.dim)
    constErr = invTailBehavior * (np.abs(popt[1]) + np.sqrt(pcov[1, 1]))
    linearError = directErr + constErr
    if linearError >= linearValue:
        return value, np.inf
    else:
        error = abs(np.log(1 - linearError / linearValue))
        return value, error


def _tailFuncMasslessHiggs(r, phi_inf, Delta_phi, dim):
    const = special.gamma(dim / 2 - 1) * 2 ** (dim / 2 - 2)
    return phi_inf * const * np.power(r, 2 - dim) + Delta_phi


# Finding the asymptotic value for W


def findWInf(phi, DW):
    aValue, constValue = _tailFitMasslessW(phi, DW)
    return aValue, constValue


def _tailFuncWSign(phi, a, const):
    return const * np.power(phi, a)


def _tailFuncW(phi, a, const):
    return a * np.log(np.abs(phi)) + const


def _tailFitMasslessW(phi, DW):

    # First we fit the absolute value to find the exponent
    DW_log = np.log(np.abs(DW))
    popt, pcov = curve_fit(
        lambda phi, a, const: _tailFuncW(phi, a, const),
        phi[-5:],
        DW_log[-5:],
    )
    aValue, aErr = popt[0], np.sqrt(pcov[0, 0])

    # We now find the coupling
    popt, pcov = curve_fit(
        lambda phi, const: _tailFuncWSign(phi, aValue, const),
        phi[-5:],
        DW[-5:],
    )
    constValue, constErr = popt[0], np.sqrt(pcov[0, 0])

    return aValue, constValue
