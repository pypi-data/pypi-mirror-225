import numpy as np  # arrays and maths
from scipy.sparse import diags  # for negative eigenvalue
from scipy.sparse.linalg import eigs  # for negative eigenvalue
from .laplacian import LaplacianFourthOrder


def findNegativeEigenvalue(bubble, eig_tol=1e-4):
    r"""Negative eigenvalue in the determinant

    Full docs in BubbleDet.py.
    """
    #Computing the eigenvalues with different boundary conditions
    negEigvalNeumann, errorNeumann = _findNegativeEigenvalueWithBCs(
        bubble, eig_tol=eig_tol, BC="Neumann"
    )

    negEigvalDirichlet, errorDirichlet = _findNegativeEigenvalueWithBCs(
        bubble, eig_tol=eig_tol, BC="Dirichlet"
    )

    possibleExtrema = [
        negEigvalNeumann + errorNeumann,
        negEigvalNeumann - errorNeumann,
        negEigvalDirichlet + errorDirichlet,
        negEigvalDirichlet - errorDirichlet,
    ]

    extrema = [np.amin(possibleExtrema), np.amax(possibleExtrema)]

    return (extrema[0] + extrema[1]) / 2, (extrema[1] - extrema[0]) / 2


def _findNegativeEigenvalueWithBCs(bubble, eig_tol=1e-4, BC="Neumann"):
    r"""
    Yields the negative eigenvalue of the bounce with a chosen boundary condition,
    BC. If BC=\"Neumann\", the boundary condition at :math:`R=R_{\rm max}`
    is a zero derivative, if \"Dirichlet\" a zero value.
    """
    # Computing single eigenvalues with differing accuracies
    nEVals = [
        _singleNegativeEigenvalue(bubble, eig_tol=eig_tol, BC=BC, frac=1),
        _singleNegativeEigenvalue(bubble, eig_tol=eig_tol, BC=BC, frac=2),
        _singleNegativeEigenvalue(bubble, eig_tol=eig_tol, BC=BC, frac=3),
    ]

    # Extrapolation to npoints->infinity leveraging the fourth-order nature
    # using frac=1, 2
    bestApprox = (16 * nEVals[0] - nEVals[1]) / 15
    # using frac=2, 3
    anotherApprox = (81 * nEVals[1] - 16 * nEVals[2]) / 65

    return bestApprox, np.abs(bestApprox - anotherApprox)


def _singleNegativeEigenvalue(
    bubble, eig_tol=1e-4, returnFunction=False, BC="Neumann", frac=1
):
    r"""
    Yields the negative eigenvalue of the bounce and the eigenfunction if
    returnFunction, with order :math:`1/N_{\rm points}^4` accuracy. If
    BC=\"Neumann\", the boundary condition at :math:`R=R_{\rm max}`
    is a zero derivative, if \"Dirichlet\" a zero value.
    """
    # potentially skipping values
    R = bubble.R[::frac]
    Phi = bubble.Phi[::frac]
    dPhi = bubble.dPhi[::frac]

    # constructing matrix operator
    negKinDiagonals = LaplacianFourthOrder(R, bubble.dim, BC)
    diagonals = [-negKinDiagonal for negKinDiagonal in negKinDiagonals]
    potDiag = [bubble.d2V(Phi[i]) for i in range(len(R))]
    diagonals[2] = diagonals[2] + potDiag
    hessian = diags(diagonals, [-2, -1, 0, 1, 2])

    # initial guess
    if bubble.dim > 2:
        guess = np.multiply(R, dPhi)
    else:
        guess = np.array(Phi) + np.multiply(R, dPhi)

    # Finds the eigenvalue (and the vector [returnFunction])
    if not returnFunction:
        return eigs(
            hessian,
            k=1,
            sigma=0,
            which="SR",
            v0=guess,
            tol=eig_tol,
            return_eigenvectors=False,
        )[0].real
    else:
        w, v = eigs(hessian, k=1, sigma=0, which="SR", v0=guess, tol=eig_tol)
        v = np.transpose(v)[0].real
        return w[0].real, v
