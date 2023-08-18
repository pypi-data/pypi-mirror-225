# import libraries
import numpy as np  # arrays and maths
from scipy import special  # special functions
from cosmoTransitions.helper_functions import deriv14  # derivatives for arrays

# import local files
from .group_volumes import group_volume
from .extrapolation import (
    fit_extrapolation,
    shanks_extrapolation,
    epsilon_extrapolation,
)
from .configs import BubbleConfig, ParticleConfig, DeterminantConfig
from .phi_infinity import findLogPhiInfinity, findPhiInfinityUnbounded, findWInf
from .negative_eigenvalue import findNegativeEigenvalue
from .wkb import findWKB
from .gelfand_yaglom import findGelfandYaglomTl, findGelfandYaglomFl
from .renormalisation import findRenormalisationTerm
from .derivative_expansion import findDerivativeExpansion


class BubbleDeterminant:
    r"""Class for computing functional determinants.

    The main class of the BubbleDet package.

    Parameters for initialisation below.

    Parameters
    ----------
    bubble : BubbleConfig
        Object describing the background field.
    particles : list of ParticleConfig
        List of ParticleConfig objects, describing the fluctuating particles.
    renormalisation_scale : float, optional
        The renormalisation scale in the :math:`\text{MS}` bar scheme. If
        `None`, set to the mass of the nucleating field.
    gauge_groups : list, optional
        List of unbroken and broken gauge groups.
    thermal : boole, optional
        If True, includes the thermal dynamical prefactor. Default is False.
    """
    def __init__(
        self,
        bubble,
        particles,
        renormalisation_scale=None,
        gauge_groups=None,
        thermal=False,
    ):
        # assigning member variables
        self.bubble = bubble
        try:
            self.n_particles = len(particles)
            self.particles = particles
        except:
            self.n_particles = 1
            self.particles = [particles]
        # construct determinant configs
        self.configs = []
        for particle in self.particles:
            config = DeterminantConfig(
                bubble,
                particle,
                renormalisation_scale=renormalisation_scale,
                gauge_groups=gauge_groups,
                thermal=thermal,
            )
            self.configs.append(config)

    def findDeterminant(
        self,
        rmin=1e-4,
        l_max=None,
        tail=0.007,
        log_phi_inf_tol=0.001,
        eig_tol=1e-4,
        gy_tol=1e-6,
        extrapolation="epsilon",
        full=False,
    ):
        r"""Full determinant

        This function computes the determinant for the full multi-particle case.
        Mathematically, the return value is the sum of single-particle
        determinants,

        .. math::
            \texttt{findDeterminant()} =
                \sum_{\texttt{particle}}
                \texttt{findSingleDeterminant(particle)}.

        The particles summed over are those in the initialisation of the
        BubbleDeterminant object. Additional parameters and metaparameters are
        as for the single-particle case.

        Parameters
        ----------
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.
        l_max : int, optional
            The maximum value of the orbital quantum number. If :py:data:`None`,
            then this value is estimated based on the radius of the bubble and
            the Compton wavelength of the fluctuating field.
        tail : float, optional
            A parameter determining the fraction of the bubble to consider when
            fitting for the asymptotic behaviour.
        gy_tol : float, optional
            Relative tolerance for solving initial value problem.
        extrapolation: {\"epsilon\", \"shanks\", \"fit\"}, optional
            Method for extrapolating to :math:`l_\text{max}\to\infty`.

        Returns
        -------
        res : float
            The result of computing the full determinant.
        err : float
            Estimated error in the result.
        """
        S1_list = np.zeros(self.n_particles)
        err_list = np.zeros(self.n_particles)

        for i_particle in range(self.n_particles):
            particle = self.particles[i_particle]
            S1_list[i_particle], err_list[i_particle] = \
                self.findSingleDeterminant(
                    particle=particle,
                    rmin=rmin,
                    l_max=l_max,
                    tail=tail,
                    log_phi_inf_tol=log_phi_inf_tol,
                    eig_tol=eig_tol,
                    gy_tol=gy_tol,
                    extrapolation=extrapolation,
                )

        if full:
            return S1_list, err_list
        else:
            return np.sum(S1_list), np.sum(err_list)

    def findSingleDeterminant(
        self,
        particle,
        rmin=1e-4,
        l_max=None,
        tail=0.007,
        log_phi_inf_tol=0.001,
        gy_tol=1e-6,
        eig_tol=1e-4,
        extrapolation="epsilon",
        full=False,
    ):
        r"""Single particle determinant

        The functional determinant is the one-loop correction to the action
        induced by fluctuations of a field. It is also the statistical part of
        the bubble nucleation rate.

        The computation factorises based on orbital quantum number, :math:`l`.
        For each value of :math:`l`, the functional determinant is computed
        using the Gelfand-Yaglom method. This is carried out for
        :math:`l\in [0, l_\text{max}]`, and then extrapolated to
        :math:`l_\text{max} \to \infty`.

        Mathematically, the return value is

        .. math::
            \texttt{findSingleDeterminant(particle)} &= \\
                \frac{n}{2}\text{dof}(d,s)&
                \log\frac{\det {'} (-\nabla^2 + W(r))}{\det (-\nabla^2 + W(\infty))}
                    - \log \mathcal{V} \mathcal{J},

        where the dash denotes that zero eigenvalues have been dropped from the
        first term (if present). Their effect is captured by the Jacobian
        :math:`\mathcal{J}` and volume :math:`\mathcal{V}` factors. The volume
        factor is only included for finite internal groups. The factors
        :math:`n` and :math:`\text{dof}(d,s)` are the number of internal
        and spin degrees of freedom respectively. Ultraviolet divergences are
        regulated in the :math:`\text{MS}` bar scheme.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.
        l_max : int, optional
            The maximum value of the orbital quantum number. If :py:data:`None`,
            then this value is estimated based on the radius of the bubble and
            the Compton wavelength of the fluctuating field.
        tail : float, optional
            A parameter determining the fraction of the bubble to consider when
            fitting for the asymptotic behaviour.
        gy_tol : float, optional
            Relative tolerance for solving initial value problem.
        extrapolation: {\"epsilon\", \"shanks\", \"fit\"}, optional
            Method for extrapolating to :math:`l_\text{max}\to\infty`.

        Returns
        -------
        res : float
            The result of computing the single particle determinant.
        err : float
            Estimated error in the result.
        """
        # getting relevant determinant config
        config = self.__getParticleConfig(particle)
        # setup
        phi = config.Phi
        R = config.R
        dim = config.dim
        mu = config.renormalisation_scale
        truncate = True if l_max == None else False

        # range of l to sum over
        l_mR = self.__lMassRadius(particle)
        l_max_act = self.__chooseLmax(particle, l_max)


        #extracting the asymptotic value of the field
        log_phi_inf, log_phi_inf_err = self.findLogPhiInfinity(
                tail, log_phi_inf_tol
        )
        # extracting asymptotic behaviour of W for massless bounces
        if config.massless_Higgs:
            # We fit, for large R,
            # log(DW) = W_exp * log(phi) + W_pot
            W_exp, W_const = findWInf(config.Phi, config.Delta_W)

            # We can rewrite this as W~W_inf r**-a_inf
            # by using the asymptotic behaviour of phi
            a_inf = W_exp * (dim - 2)
            coeff = special.gamma(dim / 2 - 1) * 2 ** (dim / 2 - 2)
            W_inf = W_const * np.power(coeff * np.exp(log_phi_inf), W_exp)
        else:
            a_inf = 0
            W_inf = 1

        # constructing WKB part
        WKB, WKB_err, WKB_Sum = self.findWKB(particle, l_max_act, W_inf, a_inf)

        #zero modes
        if config.zero_modes.lower() == "higgs":
            # helper variables
            ddphi_0 = config.dV(phi[0]) / dim
            if ddphi_0 >= 0: # can happen if thin-wall bubble inaccurate
                  ddphi_0 = deriv14(config.dPhi, R)[0]
            # l = 0 contribution, modulused
            if config.scaleless:
                zero_mode_0 = (dim - 2) / 2 * phi[0] + R[0] * config.dPhi[0]
                S1_l0 = -(1 / 2) * (
                    (dim / 2 - 1) * np.log(2 * np.pi)
                    + log_phi_inf
                    + np.log(zero_mode_0)
                    + np.log((dim - 2) / 2)
                )
                err_l0 = (1 / 2) * log_phi_inf_err
            else:
                Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(particle, 0, rmin, gy_tol)
                S1_l0 = 0.5 * np.log(abs(Tl))
                err_l0 = 0.5 * Tl_err / abs(Tl)

            # l = 1 contribution
            S1_l1 = -(dim / 2) * (
                (dim / 2 - 1) * np.log(2 * np.pi)
                + log_phi_inf
                + np.log(abs(ddphi_0))
            )
            err_l1 = (dim / 2) * log_phi_inf_err
        elif config.zero_modes.lower() == "goldstone":
            # l = 0 contribution
            phi_0 = phi[0]
            S1_l0 = -(1 / 2) * (
                (dim / 2 - 1) * np.log(2 * np.pi)
                + np.log(abs(phi_0))
                + log_phi_inf
            )
            err_l0 = 0.5 * log_phi_inf_err
            # l = 1 contribution
            Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(particle, 1, rmin, gy_tol)
            S1_l1 = 0.5 * self.__degeneracy(dim, 1) * np.log(Tl)
            err_l1 = 0.5 * self.__degeneracy(dim, 1) * Tl_err / Tl
        else: # no zero modes
            # l = 0 contribution
            Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(particle, 0, rmin, gy_tol)
            S1_l0 = 0.5 * np.log(Tl)
            err_l0 = 0.5 * Tl_err / Tl
            # l = 1 contribution
            Tl, Tl_err, Tl_D = self.findGelfandYaglomTl(particle, 1, rmin, gy_tol)
            S1_l1 = 0.5 * self.__degeneracy(dim, 1) * np.log(Tl)
            err_l1 = 0.5 * self.__degeneracy(dim, 1) * Tl_err / Tl

        # l >= 2 contribution
        S1_array = np.zeros(l_max_act - 2)
        err_array = np.zeros(l_max_act - 2)
        for l in range(2, l_max_act):
            deg_factor = 0.5 * self.__degeneracy(dim, l)

            if config.massless_Higgs:
                Tl, Tl_err,Tl_D = self.findGelfandYaglomTl(particle,l, rmin, gy_tol)
                Fl=np.log(self.__findGelfandYaglomAsymptotic(l,dim,R[-1],W_inf,a_inf,Tl,Tl_D))
                Fl_err=0
            else:
                Fl, Fl_err = self.findGelfandYaglomFl(particle, l, rmin, gy_tol)

            S1_array[l - 2] = deg_factor * (Fl - WKB[l])
            err_array[l - 2] = deg_factor * Fl_err

            # checking if can break early
            if truncate and self.__testTruncate(
                    l, l_mR, S1_array, err_array, WKB, WKB_err
                ):
                np.resize(S1_array, l)
                np.resize(err_array, l)
                #print(f"l_max reduced to {l}, {l_mR=}.")
                break
        err_lsum = np.sqrt(np.sum(err_array ** 2))

        # extrapolation
        if extrapolation.lower() == "epsilon":
            S1_lsum, err_extrap = epsilon_extrapolation(S1_array)
        elif extrapolation.lower() == "shanks":
            S1_lsum, err_extrap = shanks_extrapolation(S1_array)
        elif extrapolation.lower() == "fit":
            drop_orders = 7 + 1 - dim if dim < 7 + 1 else 0
            S1_lsum, err_extrap = fit_extrapolation(
                S1_array, drop_orders=drop_orders
            )
        else:
            S1_lsum = np.sum(S1_array)
            err_extrap = abs(S1_lsum) / len(S1_array)

        # take the maximum error- just an estimate
        err_lsum = max(err_lsum, err_extrap, WKB_err)

        # renormalisation-scale-dependent contribution
        S1_renorm, S1_renormEps, err_renorm = self.findRenormalisationTerm(
            particle
        )

        # putting the sum together

        S1 = S1_l0 + S1_l1 + S1_lsum + S1_renorm + WKB_Sum
        err = err_l0 + err_l1 + err_lsum + err_renorm

        # degrees of freedom
        S1 *= self.__dofSpin(particle) * config.dof_internal
        err *= self.__dofSpin(particle) * config.dof_internal
        if config.spin == 1:
            S1 += -2 * S1_renormEps

        # volume of broken gauge group
        if (
            config.gauge_groups is not None
            and config.zero_modes.lower() == "goldstone"
        ):
            group_volume = self.__groupVolumeFactor(particle)
            S1 += -np.log(group_volume)

        # dynamical prefactor in thermal case
        if config.thermal and config.zero_modes.lower() == "higgs":
            eig_neg, eig_neg_err = self.findNegativeEigenvalue(eig_tol)
            S1 -= np.log(np.sqrt(abs(eig_neg)) / (2 * np.pi))
            err += 0.5 * eig_neg_err / abs(eig_neg)

        # returning final result
        return S1, err

    def findGelfandYaglomTl(self, particle, l, rmin=1e-4, gy_tol=1e-6):
        r""":math:`T=\psi/\psi_{\rm FV}` for given :math:`l`

        This function solves the ode:

        .. math::
            T'' + U T' - \Delta W T = 0,

        as part of Gelfand-Yaglom method to compute functional determinants.
        Here dash denotes a derivative with respect to the radial coordinate
        :math:`r`.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        l : int
            Orbital quantum number.
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.
        gy_tol : float, optional
            Relative tolerance for solving initial value problem.

        Returns
        -------
        res : float
            The result :math:`T(r_\text{max})`.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findGelfandYaglomTl(config, l, rmin, gy_tol)

    def findGelfandYaglomFl(self, particle, l, rmin=1e-4, gy_tol=1e-6):
        r""":math:`F=\log(\psi/\psi_{\rm FV})` for given :math:`l`

        This function solves the ode:

        .. math::
            F'' + (F')^2+U F' - \Delta W = 0,

        as part of Gelfand-Yaglom method to compute functional determinants.
        Here dash denotes a derivative with respect to the radial coordinate
        :math:`r`.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        l : int
            Orbital quantum number.
        rmin : float, optional
            Size of first step out from the orgin, relative to Compton
            wavelength.
        gy_tol : float, optional
            Relative tolerance for solving initial value problem.

        Returns
        -------
        res : float
            The result :math:`F(r_\text{max})`.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findGelfandYaglomFl(config, l, rmin, gy_tol)

    @staticmethod
    def __findGelfandYaglomAsymptotic(l, d, rmax,Winf,ainf, T0,T0D):
        r"""Solves ode for :math:`T=\psi/\psi_{\rm FV}`

        .. math::
            T'' + U T' - W T = 0,

        as part of Gelfand-Yaglom method to compute functional determinants.
        Here dash denotes a derivative with respect to the radial coordinate
        :math:`r`. This method calculates, analytically, the solution when the
        bounce that does not vanish expoentially for large r.


        Parameters
        ----------
        l : int
            Orbital quantum number.

        rmax : float
            The matching radius

        m : float
            The value of W*rmax**-4

        T0: float
            the value of Tl at r=rmax

        T0D: float
            the value of Tl' at r=rmax

        Returns
        -------
        res : float
            The result :math:`T(inf)`.

        """
        # set up

        alphaHelp=(2-d - 2*l )/(ainf - 2) #order of the bessel functions
        argHelp=-2*rmax**(1 - ainf/2.)*np.sqrt(Winf+0j)/(-2 + ainf) #argument of the bessel functions
        WinfHelp=(Winf+0j)**((-2 + d + 2*l)/(2.*(-2 + ainf))) #prefactor
        RinfHelp=rmax**((2 - d  - 2*l)/2.) #prefactor depning on rmax

        #When solve the full ODE we get two free constants that we have to fix to match the value and the derivative
        #of Tl at r=rmax

        #A1 and A2 are the functions multiplying the c1 and c2 constants
        A1=RinfHelp*WinfHelp*special.kv(alphaHelp,argHelp)
        A2=RinfHelp*WinfHelp*special.iv(-alphaHelp,argHelp)

        #B1 and B2 are the derivatives of A1 respectively A2
        B1=-(d  + 2*l - 2)/2*RinfHelp/rmax*WinfHelp*special.kv(alphaHelp,argHelp)
        B1+= -RinfHelp*WinfHelp/2*rmax**(-ainf/2)*np.sqrt(Winf+0j)*(special.kv(-1-alphaHelp,argHelp)+special.kv(1-alphaHelp,argHelp,))
        B2=-(d  + 2*l - 2)/2*RinfHelp/rmax*WinfHelp*special.iv(-alphaHelp,argHelp)
        B2+=RinfHelp*WinfHelp/2*rmax**(-ainf/2)*np.sqrt(Winf+0j)*(special.iv(-1-alphaHelp,argHelp)+special.iv(1-alphaHelp,argHelp))



        #Only the c1 constant contribute to the r=inf value of Tl
        c1=-((B2*T0 - A2*T0D)/(A2*B1 - A1*B2))

        #The prefactor is the asymptotic value of A1
        Tinf=np.real(c1*((-1+0j)**((-2 + d + 2*l)/(-2 + ainf))*(-2 + ainf)**((-2 + d + 2*l)/(-2 + ainf))
            *special.gamma((-2 + d + 2*l)/(-2 + ainf)))/2.)

        if Tinf<0.0:
            raise ValueError("Negative determinant. Choose a smaller lmax or provide a more accurate profile.")

        return Tinf

    def findRenormalisationTerm(self, particle):
        r"""Renormalisation scale dependent part of determinant

        Such terms are only nonzero in even dimensions. The present
        implementation gives the nonzero results for :math:`d = 2, 4, 6`.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the renormalisation term.

        Returns
        -------
        res : float
            The renormalisation scale dependent term.
        resEps : float
            The additional finite renormalisation scale dependent term which
            arises due to factors of :math:`d/\epsilon` for vector fields.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findRenormalisationTerm(config)

    def findWKB(self, particle, l_max, Winf, ainf, separate_orders=False):
        r"""Terms in the WKB approximation of determinant

        This function uses a WKB approximation to approximate the functional
        determinant for large partial waves l. Our implementation is an
        higher-orders generalization of [GO]_.

        The routine solves the differential equation

        .. math::
            \Psi''(x)=(x^2 W(e^x)+\overline{l}^2)\Psi(x)

        in powers of :math:`\overline{l}`, where :math:`r=e^x`; for the
        false-vacuum solution :math:`m_0=0`.

        Sums of the form

        .. math::
            \sum_{l=2}^{\infty}{\rm deg}(d,l)\overline{l}^{-a}

        are also returned, where

        .. math::
            {\rm deg}(d,l) =
                \frac{(d+2 l-2) \Gamma (d+l-2)}{\Gamma (d-1) \Gamma (l+1)}.

        If :math:`d=2n-2\epsilon`, these sums contain :math:`\epsilon` poles
        if :math:`2n-2-a=-1`. In cases when this happens findWKB replaces the
        sum with

        .. math::
            {\rm deg}(d,1)+\frac{1}{2}{\rm deg}(d,l)

        The divergent sum

        .. math::
            \sum_{l=0}^{\infty}{\rm deg}(d,l)\overline{l}^{-a}

        is instead returned by :py:data:`findRenormalisationTerm`.


        If the sum is finite in dimensional regularization the code returns

        .. math::
            \lim_{\epsilon \rightarrow 0}
                \sum_{l=0}^{\infty}{\rm deg}(d,l)\overline{l}^{-a}.

        Parameters
        ----------
        particle : ParticleConfig
            The particle for which to compute the determinant.
        l_max : int
            Maximum orbital quantum number.
        separate_orders : boole, optional
            If True returns the terms in the WKB expansion at each power of
            :math:`1/l` separately. Default is False.

        Returns
        -------
        WKB : float
           The ratio of determinants
           :math:`\log \frac{\Psi(\infty)}{\Psi_{FV}(\infty)}` up to
           :math:`l^{-9}`.

        WKB_err : float
           Estimated error on :py:data:`WKB`.

        WKBSum : float
            The sum
            :math:`\frac{1}{2}\sum_{l=2}^{\infty}{\rm deg}(d,l)\log\frac{\Psi(\infty)}{\Psi_{FV}(\infty)}`
            within the WKB approximation.

        References
        ----------
        .. [GO] Gerald V. Dunne,  Jin Hur, Choonkyu Lee,  Hyunsoo Min.
            Instanton determinant with arbitrary quark mass: WKB phase-shift
            method and derivative expansion, Phys.Lett.B 600 (2004) 302-313
        """
        config = self.__getParticleConfig(particle)
        return findWKB(config, l_max, Winf, ainf, separate_orders)

    def findNegativeEigenvalue(self, eig_tol=1e-4):
        r"""Negative eigenvalue in Higgs determinant

        In continuum notation, the eigenvalue equation takes the form

        .. math::
            \left[-\frac{\partial^2}{\partial r^2}
            -\frac{(d - 1)}{r}\frac{\partial}{\partial r}
            + W(r)\right] \chi(r) = \lambda \chi(r),

        and for bubble nucleation, or vacuum decay, this operator has a single
        negative eigenvalue, some finite number of zero eigenvalues and an
        infinite number of positive eigenvalues.

        Here, we use the finite difference matrix representation of the
        differential operator accurate to :math:`1/N_{\rm points}^4`, with two
        different boundary conditions, \"Neumann\" and \"Dirichlet\", at the maximal
        numerical radius.

        The leading, :math:`1/N_{\rm points}^4` numerical error
        is extrapolated away using a fit to direct numerical estimates of the
        eigenvalue, and the residual error is estimated. The different boundary
        conditions provide additional information for the error estimation, appended
        to the residual numerical error.


        Parameters
        ----------
        eig_tol : float, optional
            Relative tolerance for the direct numerical eigenvalues used for the
            extrapolation.

        Returns
        -------
        res : float
            The value of the negative eigenvalue.
        err : float
            Estimated error in the result.

        """
        return findNegativeEigenvalue(self.bubble, eig_tol)

    def findLogPhiInfinity(self, tail=0.007, log_phi_inf_tol=0.001):
        r"""Constant :math:`\log\phi_\infty` in asyptotics of background field

        We fit for the unknown constant :math:`\phi_\infty` in the asymptotic
        behavior of the numerical bubble profile,

        .. math::
            \phi(r) \sim \phi_{\mathrm{F}}
            + \phi_\infty \frac{K_{d/2 - 1}(m r)}{(m r)^{d/2 - 1}},

        assuming the potential has a positive mass term in the false vacuum,
        :math:`\phi = \phi_{\mathrm{F}}`.

        First, we find four approximate values for the asymptotic behavior of
        the numerical bubble profile. Then, we extrapolate linearly from these
        values to a more precise and robust value than obtainable directly from
        the numerical bubble solution.

        If the bubble profile is precise near the false vacuum, i.e. at large
        radii, the argument tail can be decreased from the default of 0.015,
        which can then be used to increase the precision of the result. This
        corresponds to performing the linear extrapolation with points closer to
        the false vacuum, and correspondingly closer to the end of the profile.
        However, note that the default setting is already very precise and works
        well with the default settings of the CosmoTransitions package set in
        this package. A more detailed description for the tail parameter can be
        found from the correspoding article.

        Parameters
        ----------
        tail : float, optional
            A parameter determining the chosen bubble-tail points for fitting
            the asymptotic behaviour. Shrinking tail :math:`\to 0` corresponds
            to :math:`r\to \infty` for the chosen points.
        log_phi_inf_tol : float, optional
            A parameter determining an accuracy goal for the error caused by
            choosing points that are close to the end of the numerical bubble
            profile, < result * log_phi_inf_tol. If the goal cannot be met, it
            is lowered with an internal algorithm.

        Returns
        -------
        res : float
            The value of :math:`\log\phi_\infty`.
        err : float
            Estimated error in the result.

        """
        return findLogPhiInfinity(self.bubble, tail, log_phi_inf_tol)

    def findDerivativeExpansion(self, particle, NLO=False):
        r"""Derivative expansion of determinant

        The derivative expansion is an expansion in a ratio of length scales,
        which in turn can be related to a ratio of masses: the mass of the
        background scalar divided by the mass of the fluctuating field.

        The leading order (LO) and next-to-leading order (NLO) of the expansion
        are

        .. math::
            \int \mathrm{d}^d x \underbrace{\left[
                V_{(1)}(\phi_\text{b}) - V_{(1)}(\phi_\text{F})
                \right]}_\text{LO}
            + \int \mathrm{d}^d x \underbrace{\left[
                \frac{1}{2} Z_{(1)}(\phi_\text{b})
                    \nabla_\mu\phi_\text{b}\nabla_\mu\phi_\text{b}
                \right]}_\text{NLO},

        where :math:`V_{(1)}` and :math:`Z_{(1)}` are the heavy particle's
        contribution to the one-loop effective potential and field
        normalisation factor.

        The expansion is carried out to leading order, i.e. the potential
        approximation.

        Parameters
        ----------
        particle : ParticleConfig
            The heavy particle for which to carry out the derivative expansion.
        NLO : boole, optional
            If True, the derivative expansion is carried out to
            next-to-leading order, otherwise at leading order.

        Returns
        -------
        S1 : float
            The result within the derivative expasion.
        err : float
            Estimated error in the result.

        """
        config = self.__getParticleConfig(particle)
        return findDerivativeExpansion(config, NLO)

    def __dofSpin(self, particle):
        r"""
        Returns number of spin degrees of freedom for the given particle.
        """
        if particle.spin == 0:
            return 1
        elif particle.spin == 1:
            return self.bubble.dim - 1
        else:
            raise ValueError("Particle spin must be in [0, 1]")

    def __lMassRadius(self, particle):
        r"""
        Calculates product of mass and radius for determinant, to give the
        natural order of :math:`l`.
        """
        config = self.__getParticleConfig(particle)
        # natural scale for l is m*R, where m is largest relevant mass scale
        return int(config.m_max * config.r_mid)

    def __chooseLmax(self, particle, l_max=None):
        r"""
        Method for choosing a sensible value of :math:`l_\text{max}`.
        """
        if l_max is not None:
            return l_max
        l_mR = self.__lMassRadius(particle)
        n_mR_min = 3 if self.bubble.dim < 6 else 4
        l_max_min = 25 if self.bubble.dim < 6 else 33
        l_max_act = max(l_max_min, n_mR_min * l_mR)
        #print(f"{l_max_act=}, {l_mR=}")
        if l_max_act > 1e3:
            raise RuntimeWarning(f"findDeterminant error: {l_max_act=} > 1000")
        return l_max_act

    def __testTruncate(self, l, l_mR, S1_array, S1_err, WKB, WKB_err):
        r"""
        Method to decide whether or not to truncate the sum over :math:`l`
        early, i.e. before reaching :math:`l_\text{max}`.
        """
        n_mR_min = 2 if self.bubble.dim < 6 else 3
        l_max_min = 15 if self.bubble.dim < 6 else 20
        l_max_trunc = max(l_max_min, n_mR_min * l_mR)
        if l > l_max_trunc:
            deg_factor = 0.5 * self.__degeneracy(self.bubble.dim, l)
            dWKB = abs(S1_array[l - 2] / WKB[l]) / deg_factor
            dWKB_minus_10 = (
                abs(S1_array[l - 12] / WKB[l - 10])
                / self.__degeneracy(self.bubble.dim, l - 10)
            )
            WKB_err = deg_factor * abs(WKB[l]) * 1e-15
            # checking if can break early
            return (
                S1_err[l - 2] > abs(S1_array[l - 2]) or
                WKB_err > abs(S1_array[l - 2]) or
                (l > 20 and dWKB > dWKB_minus_10)
            )

    def __groupVolumeFactor(self, particle):
        r"""Calculates the volume of the broken group.

        For a symmetry-breaking pattern where G breaks down to H, the volume of
        the broken coset group is

        .. math::
            {\rm Vol}(G / H) = \frac{{\rm Vol}(G)}{{\rm Vol}(H)}.
        """
        config = self.__getParticleConfig(particle)
        group_volume = 1
        for k in config.gauge_groups[0]:
            group_volume *= group_volume(k)

        unbroken_volume = 1
        for k in config.gauge_groups[1]:
            unbroken_volume *= group_volume(k)

        return group_volume / unbroken_volume

    def __getParticleConfig(self, particle):
        if particle in self.particles:
            i_particle = self.particles.index(particle)
            return self.configs[i_particle]
        else:
            raise ValueError(
                f"Unknown ParticleConfig: {particle} not in {self.particles}"
            )

    @staticmethod
    def __degeneracy(dim, l):
        r"""
        Degeneracy of modes with fixed :math:`d` and :math:`l`.
        """
        if l == 0 or dim == 1:
            return 1
        elif dim == 3:
            return 2 * l + 1
        elif dim == 4:
            return (l + 1) ** 2
        elif dim == 2:
            return 2
        else:
            return (2 * l + dim - 2) / special.beta(l + 1, dim - 3) / (dim - 3) / (dim - 2)
