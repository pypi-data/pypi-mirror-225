# The Laplacian matrix in spherical coordinates, accurate to fourth order in dr
from numpy import zeros, concatenate, array


def LaplacianFourthOrder(R, dim, BC):
    '''
    Constructs the Laplacian matrix in spherical coordinates. At fourth order,
    there are five diagonals to this matrix, which are returned in an array.
    The Laplacian assumes zero derivative at R[0]=0 and the other boundary
    condition at R[-1] is set by the argument BC:
    True: zero derivative,
    False: zero value.
    R is an array containing the discrete radial points of the bounce solution
    starting from 0.
    dim is the dimensionality.
    '''
    n = len(R)

    diags = [zeros(n-2), zeros(n-1), zeros(n), zeros(n-1), zeros(n-2)]

    '''
    Iterations proceed regarding the Laplacian as (3-by-3 example)

    i=0:
    xxx--
    oooo-
    ooooo
    -oooo
    --ooo

    i=1:
    xxx--
    xxxx-
    ooooo
    -oooo
    --ooo

    i=2:
    xxx--
    xxxx-
    xxxxx
    -oooo
    --ooo

    ...

    i=n-2:
    xxx--
    xxxx-
    xxxxx
    -xxxx
    --ooo

    i=n-1:
    xxx--
    xxxx-
    xxxxx
    -xxxx
    --xxx
    '''

    i = 0

    second_der = derivatives(R, i, BC)

    diags[2][i] = dim * second_der[0]
    diags[3][i] = dim * second_der[1]
    diags[4][i] = dim * second_der[2]

    i = 1

    first_der, second_der = derivatives(R, i, BC)
    dimInvR = (dim-1)/R[i]

    diags[1][i-1] = second_der[0] + dimInvR*first_der[0]
    diags[2][i] = second_der[1] + dimInvR*first_der[1]
    diags[3][i] = second_der[2] + dimInvR*first_der[2]
    diags[4][i] = second_der[3] + dimInvR*first_der[3]

    for i in range(2, n-2):
        first_der, second_der = derivatives(R, i, BC)
        dimInvR = (dim-1)/R[i]

        diags[0][i-2] = second_der[0] + dimInvR*first_der[0]
        diags[1][i-1] = second_der[1] + dimInvR*first_der[1]
        diags[2][i] = second_der[2] + dimInvR*first_der[2]
        diags[3][i] = second_der[3] + dimInvR*first_der[3]
        diags[4][i] = second_der[4] + dimInvR*first_der[4]


    i = n-2
    first_der, second_der = derivatives(R, i, BC)
    dimInvR = (dim-1)/R[i]

    diags[0][i-2] = second_der[0] + dimInvR*first_der[0]
    diags[1][i-1] = second_der[1] + dimInvR*first_der[1]
    diags[2][i] = second_der[2] + dimInvR*first_der[2]
    diags[3][i] = second_der[3] + dimInvR*first_der[3]

    i = n-1
    first_der, second_der = derivatives(R, i, BC)
    dimInvR = (dim-1)/R[i]

    diags[0][i-2] = second_der[0] + dimInvR*first_der[0]
    diags[1][i-1] = second_der[1] + dimInvR*first_der[1]
    diags[2][i] = second_der[2] + dimInvR*first_der[2]

    return diags


def derivatives(r, i, BC):
    """
    Returns the first derivative and the second derivative at the radius r[i].
    For r[0]=0, the function only returns the second derivative,
    because the first derivative is always zero.
    """
    n = len(r)
    if 1<i<n-2:
        R = r[i-2:i+3]
    elif i == 0:
        R = concatenate(([-r[2],-r[1]], r[i:i+3]))
    elif i == 1:
        R = concatenate(([-r[1]], r[i-1:i+3]))
    elif i == n-2:
        R = concatenate((r[i-2:i+2], [2*r[-1] - r[-2]]))
    elif i == n-1:
        R = concatenate((r[i-2:i+1], [2*r[-1] - r[-2]]))

    d0 = R[2] - R[0]
    d1 = R[2] - R[1]
    d2 = R[3] - R[2]

    id0 = 1/d0
    id1 = 1/d1
    id2 = 1/d2

    id01 = 1/(d0 - d1)
    id02 = 1/(d0 + d2)

    id12 = 1/(d1 + d2)

    if i < n-1:
        d3 = R[4] - R[2]
        id3 = 1/d3

        d4 = d0 * d1 * d2 * d3

        id03 = 1/(d0 + d3)
        id13 = 1/(d1 + d3)
        id23 = 1/(d2 - d3)

        c0 = d4 * id01 * id02 * id03 * id0 * id0
        c1 = -d4 * id01 * id12 * id13 * id1 * id1
        c2 = id0 + id1 - id2 - id3
        c3 = -d4 * id02 * id12 * id23 * id2 * id2
        c4 = d4 * id03 * id13 * id23 * id3 * id3

        b0 = d4 * id01 * id02 * id03 * id0 * id0 * (id1 - id2 - id3)
        b1 = d4 * id01 * id12 * id13 * id1 * id1 * (-id0 + id2 + id3)
        b2 = id0*id1 + id2*id3 - id0*id2 - id1*id2 - id0*id3 - id1*id3
        b3 = d4 * id23 * id12 * id02 * id2 * id2 * (id3 - id1 - id0)
        b4 = d4 * id23 * id13 * id03 * id3 * id3 * (-id2 + id1 + id0)

        if 1<i<n-2:
            return array([c0, c1, c2, c3, c4]), 2*array([b0, b1, b2, b3, b4])
        elif i == 1:
            return array([c1, c2+c0, c3, c4]), 2*array([b1, b2+b0, b3, b4])
        elif i == 0:
            return 2*array([b2, b3+b1, b4+b0])
        elif i == n-2:
            if BC=='Neumann':
                return array([c0, c1, c2, c3+c4]), 2*array([b0, b1, b2, b3+b4])
            elif BC=='Dirichlet':
                return array([c0, c1, c2, c3]), 2*array([b0, b1, b2, b3])
            else:
                raise RuntimeWarning(
                    """\n\tInvalid boundary condition at infinity given for negative eigenmode.
                    Code uses Neumann.\n"""
                )
                return array([c0, c1, c2, c3+c4]), 2*array([b0, b1, b2, b3+b4])

    else:
        d3  = d0 * d1 * d2

        c0 = d3 * id01 * id02 * id0 * id0
        c1 = -d3 * id01 * id12 * id1 * id1
        c2 = id0 + id1 - id2

        b0 = - (d1-d2) * id01 * id02 * id0
        b1 = (d0-d2) * id01 * id12 * id1
        b2 = id0*id1 - id0*id2 - id1*id2

        if BC=='Neumann':
            c3 = d3 * id02 * id12 * id2 * id2
            b3 = (d0+d1) * id12 * id02 * id2
            return array([c0, c1, c2+c3]), 2*array([b0, b1, b2+b3])
        elif BC=='Dirichlet':
            return array([c0, c1, c2]), 2*array([b0, b1, b2])
        else:
            raise RuntimeWarning(
                """\n\tInvalid boundary condition at infinity given for negative eigenmode.
                Code uses Neumann.\n""",
            )
            c3 = d3 * id02 * id12 * id2 * id2
            b3 = (d0+d1) * id12 * id02 * id2
            return array([c0, c1, c2+c3]), 2*array([b0, b1, b2+b3])
