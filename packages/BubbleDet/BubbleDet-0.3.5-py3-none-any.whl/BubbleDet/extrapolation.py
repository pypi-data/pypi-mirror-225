# tools for extrapolation
import numpy as np  # arrays and maths
import sys # for stderr
from scipy.special import gamma # to try to help with cancellations
from scipy.optimize import curve_fit # for fitting


def richardson_extrapolation(a_n, order_max=6):
    r"""Performs Richardson extrapolation

    This function performs Richardson extrapolation to accelerate the
    convergence of a series, with coefficients :math:`a_n`. Our implementation
    follows Section 8.1 of Bender and Orszag's book [BO]_. Given the partial sums
    :math:`A_n=\sum_{k=0}^{n-1}a_k`, the order :math:`N` Richardson
    extrapolation :math:`R_N` takes the form

    .. math::
      R_N = \sum_{k=0}^{N} \frac{A_{n+k} (n+k)^N (-1)^{k+N}}{k! (N-k)!}.

    This function automatically picks the order for Richardson extrapolation,
    up to order_max, so as to minimise both errors from higher order terms,
    and from floating point arithmetic.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    order_max : int, optional
        Maximum order of extrapolation, greater than or equal to 0.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The estimated error in the result.

    References
    ----------
    .. [BO] Bender, C. M., Orszag, S., and Orszag, S. A. (1999). Advanced
            mathematical methods for scientists and engineers I: Asymptotic
            methods and perturbation theory (Vol. 1). Springer Science &
            Business Media.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import richardson_extrapolation
    >>> a_n = np.array([1 / (n + 1) ** 2 for n in range(10)])
    >>> res, err = richardson_extrapolation(a_n)
    (1.6449259364244426, 1.9065728906753066e-05)
    >>> np.pi ** 2 / 6
    1.6449340668482264
    """
    # same as np.sum(a_n) at order 0
    res_0, err_0, err_n_0 = richardson_extrapolation_static(a_n, 0)
    res, err, err_n = richardson_extrapolation_static(a_n, 1)
    if abs(res - res_0) < err:
        return res_0, max(err_0, err_n_0)
    r = 2
    while r <= order_max:
        res_r, err_r, err_n_r = richardson_extrapolation_static(a_n, r)
        r += 1
        if err_r < abs(res - res_0) / 5 and abs(res_r - res) < abs(res - res_0):
            res_0, err_0 = res, err
            res, err, err_n = res_r, err_r, err_n_r
        else:
            break
    return res, max(err, err_n_r, abs(res - res_0))


def richardson_extrapolation_static(a_n, order):
    r"""Performs Richardson extrapolation to fixed order

    For more details see :func:`richardson_extrapolation`.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    order : int
        Order of extrapolation, greater than or equal to 0.

    Returns
    -------
    res : float
        The result of extrapolation.
    err_float : float
        The estimated error from floating point arithmetic.
    err_n : float
        The estimated error from missing higher order terms.

    Notes
    -----
    At high orders, large cancellations occur, so floating point precision
    may not be enough. Recommend keeping order less than about 6.

    """
    n_max = len(a_n)
    n_min = n_max - order - 1
    if n_min < 0:
        print("richardson_extrapolation_static error: order", order, "too high",
            file=sys.stderr)
        return np.sum(a_n), float('nan'), float('nan')
    # constructing partial sums
    A_n = np.zeros(order + 1)
    for i in range(n_min + 1):
        A_n[0] += a_n[i]
    for k in range(1, order + 1):
        A_n[k] = A_n[k - 1] + a_n[n_min + k]
    # doing extrapolation
    res = 0.0
    max_factor = 1
    for k in range(order + 1):
        factor = (
            np.power(-1, (order + k) % 2)
            * np.power(n_min + k, order)
            / gamma(k + 1)
            / gamma(order - k + 1)
        )
        max_factor = max(max_factor, abs(factor))
        res += factor * A_n[k]
    # floating point error estimate
    err_float = max_factor * (order + 1) * abs(res) / 1e16
    # error estimate from missing higher-order terms
    err_n = abs(res) / np.power(n_max, order + 1)
    return res, err_float, err_n


def partial_sums(a_n):
    r"""Constructs all partial sums

    Given series coefficients :math:`a_n`, computes

    .. math::
      A_n = \sum_{j=0}^{n-1} a_j.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.

    Returns
    -------
    A_n : array

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import partial_sums
    >>> a_n = np.array([1 / 2 ** (n + 1) for n in range(5)])
    [0.5, 0.25, 0.125, 0.0625, 0.03125]
    >>> A_n = partial_sums(a_n)
    [0.5, 0.75, 0.875, 0.9375, 0.96875]
    """
    n = len(a_n)
    A_n = np.zeros(n)
    A_n[0] = a_n[0]
    for k in range(1, n):
        A_n[k] = A_n[k - 1] + a_n[k]
    return A_n


def fit_extrapolation(a_n, drop_orders=0):
    r"""Performs extrapolation based on polynomial fitting

    For a series with index :math:`n`, the function fits a polynomial
    :math:`p` in :math:`1/(n+1)` to the partial sums
    :math:`A_n=\sum_{k=0}^{n-1}a_k`,

    .. math::
      p = \sum_{k=0}^{N} \frac{c_k}{(n+1)^k},

    where here the order of the polynomial is :math:`N`. After fitting, the
    extrapolation to :math:`n\to \infty` is given by :math:`c_0`.

    This function automatically picks the polynomial order for the fit, to
    ensure a good fit without overfitting. To do so, it minimises the
    :math:`\chi^2` per degree of freedom in the fit.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    drop_orders: int, optional
        Powers of :math:`1/n` to drop.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The fit error in the result, i.e. the square root of the diagonal
        element of the covariance matrix.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import fit_extrapolation
    >>> a_n = np.array([1 / (n + 1) ** 2 for n in range(10)])
    >>> res, err = fit_extrapolation(a_n)
    (1.6449345845688652, 6.277329652778687e-08)
    >>> np.pi ** 2 / 6
    1.6449340668482264
    """
    A_n = partial_sums(a_n)
    inv_n = np.array([1 / (i + 1) for i in range(len(A_n))])
    fit, cov, order_best, chi_sq_reduced_best = best_poly_fit(
        inv_n, A_n, drop_orders=drop_orders
    )
    return fit[0], np.sqrt(cov[0, 0])


def best_poly_fit(x, y, order_min=0, order_max=6, drop_orders=0):
    r"""Finds polynomial fit with smallest :math:`\chi^2/\text{dof}`

    Performs all possible polynomial fits in the range [order_min, order_max],
    and choses that with smallest :math:`\chi^2/\text{dof}`.

    Uses scipy.optimize.curve_fit to perform the fitting.

    Parameters
    ----------
    x : array_like
    y : array_like

    Returns
    -------
    fit : array
        The fit parameters.
    cov : 2D array
        The covariance matrix.
    order_best: int
        The optimal polynomial order.
    chi_sq_reduced_best: float
        The value of :math:`\chi^2/\text{dof}` for the optimal fit.
    """
    # checking that dof >= 1
    n = len(x)
    o_min = min(order_min, order_max)
    o_max = max(order_min, order_max)
    o_max = max(min(o_max, n - 2), 0)
    o_min = min(max(0, o_min), o_max)
    # fitting a constant first
    order_best = o_min
    fit, cov = curve_fit(
        lambda x, *coeffs: poly_fn(x, *coeffs, drop_orders=drop_orders),
        x, y, p0=np.ones(order_best + 1)
    )
    # goodness of fit
    dof = n - (order_best + 1)
    chi_sq = np.sum((y - poly_fn(x, *fit, drop_orders=drop_orders)) ** 2)
    chi_sq_reduced_best = chi_sq / dof
    # comparing to higher order polynomials
    for order in range(1, o_max + 1):
        popt, pcov = curve_fit(
            lambda x, *coeffs: poly_fn(x, *coeffs, drop_orders=drop_orders),
            x, y, p0=np.ones(order + 1)
        )
        # goodness of fit
        n = len(x)
        dof = n - (order + 1)
        chi_sq = np.sum((y - poly_fn(x, *popt, drop_orders=drop_orders)) ** 2)
        chi_sq_reduced = chi_sq / dof
        if chi_sq_reduced < chi_sq_reduced_best:
            chi_sq_reduced_best = chi_sq_reduced
            order_best = order
            fit, cov = popt, pcov
    return fit, cov, order_best, chi_sq_reduced_best


def poly_fn(x, *coeffs, drop_orders=0):
    r"""Polynomial function from coefficients.

    A general polynomial function, of the appropriate form for
    scipy.optimize.curve_fit, with coefficients as parameters.

    A simple wrapper for the numpy polynomial implementation.
    Includes functionality to set some monomials to zero.

    Parameters
    ----------
    x : float
    *coeffs : floats

    Returns
    -------
    p(x) : float
        The polynomial function evaluated at x.
    """
    n_shifted_coeffs = len(coeffs) + drop_orders
    shifted_coeffs = np.zeros(n_shifted_coeffs)
    shifted_coeffs[0] = coeffs[0]
    for i in range(1, len(coeffs)):
        shifted_coeffs[drop_orders + i] = coeffs[i]
    p = np.polynomial.polynomial.Polynomial(shifted_coeffs)
    return p(x)


def shanks_extrapolation(a_n, order=6, truncate=True):
    r"""Performs iterated Shanks extrapolation

    This function performs an iterated Shanks transform, to accelerate the
    convergence of a series, with coefficients :math:`a_n`. Our implementation
    follows Section 8.1 of Bender and Orszag's book [BO]_. Given the partial
    sums :math:`A_n=\sum_{k=0}^{n-1}a_k`, a single Shanks transform takes the
    form

    .. math::
      S(A_n) = \frac{A_{n+1}A_{n-1} - A_n^2}{A_{n+1} + A_{n-1} - 2A_n}.

    This operation can be iterated to further accelerate convergence. However,
    at high orders, large cancellations occur, and with standard Python floating
    point precision the best relative accuracy which can be achieved by
    iteration is about 1e-8.

    The return value of this function is the last element of
    :math:`S^\text{order}(A_n)`.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    order: int, optional
        Number of iterations.
    truncate : boole, optional
        If True, truncates algorithm where floating point errors become
        important.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The estimated error from floating point artithmetic.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import shanks_extrapolation
    >>> a_n = np.array([1 / (n + 1) ** 2 for n in range(10)])
    >>> res, err = shanks_extrapolation(a_n)
    (1.6357502037479885, 0.0008240093298663709)
    >>> np.pi ** 2 / 6
    1.6449340668482264
    """
    order_max = min(order, (len(a_n) - 1) // 2)
    SA_n = partial_sums(a_n)
    for s in range(order_max):
        # floating point error estimate
        err_float = abs(SA_n[-1] + SA_n[-3] - 2 * SA_n[-2])
        if truncate and err_float < 1e-8 * abs(SA_n[-1]):
            print(f"Shanks order truncated at order={s}", file=sys.stderr)
            break
        # transform
        SA_n = shanks_static(SA_n)
    return SA_n[-1], err_float


def shanks_static(A_n):
    r"""Performs single Shanks trasform.

    For more details see :func:`shanks_extrapolation`, which iterates this
    function.

    Parameters
    ----------
    A_n : array_like
        Series partial sums.

    Returns
    -------
    res : array
        The result of a Shanks transform. The array is shorter than A_n by 2.

    """
    SA_n = np.zeros(len(A_n) - 2)
    for n in range(len(A_n) - 2):
        n_An = n + 1
        SA_n[n] = (A_n[n_An + 1] * A_n[n_An - 1] - A_n[n_An] ** 2) / (
            A_n[n_An + 1] + A_n[n_An - 1] - 2 * A_n[n_An]
        )
    return SA_n


def epsilon_extrapolation(a_n, truncate=True):
    r"""Performs extrapolation using the epsilon algorithm

    The epsilon algorithm is closely related to the iterated Shanks algorithm,
    but has some superior properties for floating point numbers. In particular,
    its relative accuracy is not bounded by the square root of the floating
    point error, but can exaust the accuracy of floating point numbers. For an
    overview of the epsilon algorithm, see [GM]_.

    Parameters
    ----------
    a_n : array_like
        Series coefficients.
    truncate : boole, optional
        If True, truncates algorithm where floating point errors start to become
        large.

    Returns
    -------
    res : float
        The result of extrapolation.
    err : float
        The estimated error in the extrapolation.

    References
    ----------
    .. [GM] Graves-Morris, P.R., Roberts, D.E. and Salam, A., 2000. The epsilon
            algorithm and related topics. Journal of Computational and Applied
            Mathematics, 122(1-2), pp.51-80.

    Examples
    --------
    >>> import numpy as np
    >>> from BubbleDet.extrapolation import epsilon_extrapolation
    >>> a_n = np.array([(-1) ** n / (n+1) for n in range(10)])
    >>> res, err = epsilon_extrapolation(a_n)
    (0.6931471424877166, 1.898666642796698e-07)
    >>> np.log(2)
    0.6931471805599453
    """
    n = len(a_n)
    A_n = partial_sums(a_n)
    # initialising epsilon_-1 and epsilon_0
    epsilon_previous = np.zeros(n)
    epsilon_current = A_n
    # best current result, and error estimate
    res = A_n[-1]
    err = abs(a_n[-1])
    # k_max largest odd number <=n
    k_max = n if n % 2 == 1 else n - 1
    for k in range(1, k_max):
        epsilon_next = np.zeros(n - k)
        for j in range(n - k):
            # testing for 1 / 0
            if epsilon_current[j + 1] - epsilon_current[j] == 0:
                return res, err
            # testing for large floating-point cancellations
            float_rel_err = 1e-16 * (
                0.5 * abs(epsilon_current[j + 1] + epsilon_current[j])
                / abs(epsilon_current[j + 1] - epsilon_current[j])
            )
            if truncate and res != 0 and float_rel_err > err / abs(res):
                return res, err
            # non-trivial part of algorithm
            epsilon_next[j] = (
                epsilon_previous[j + 1]
                + 1 / (epsilon_current[j + 1] - epsilon_current[j])
            )
        # storing 3 epsilons at a time
        epsilon_previous = epsilon_current
        epsilon_current = epsilon_next
        # best current result, and error estimate
        if k % 2 == 0:
            err = abs(epsilon_current[-1] - res)
            res = epsilon_current[-1]
            if err == 0:
                break
    return res, err
