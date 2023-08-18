import numpy as np  # arrays and maths
from scipy import interpolate  # interpolation
from cosmoTransitions.helper_functions import deriv14  # derivatives for arrays
from .helpers import derivative # derivatives for callable functions


class ParticleConfig:
    r"""Particle configuration for fluctuations.

    A simple class holding attributes of a particle as relevant for calculations
    of functional determinants.

    Parameters for initialisation below.

    Parameters
    ----------
    W_Phi : function
        Function :math:`W(\phi)`, should take a float and return one.
    spin : {0, 1}, optional
        Particle spin, :math:`s`, currently restricted to [0, 1]. Default
        is 0.
    dof_internal : int, optional
        Number of internal degrees of freedom, :math:`n`. Default is 1.
    zero_modes : {\"Higgs\", \"Goldstone\", \"None\"}, optional
        String determining type of zero modes. Default is
        :py:data:`\"Higgs\"`.

    """
    SPIN_OPTIONS = [0, 1]
    ZERO_MODES_OPTIONS = ["higgs", "goldstone", "none"]

    def __init__(
        self, W_Phi, spin=0, dof_internal=1, zero_modes="Higgs",
    ):
        ParticleConfig.__validate_input(W_Phi, spin, dof_internal, zero_modes)
        self.W_Phi = W_Phi
        self.spin = spin
        self.dof_internal = dof_internal
        self.zero_modes = zero_modes

    @staticmethod
    def __validate_input(W_Phi, spin, dof_internal, zero_modes):
        """
        Checks zero modes input name is allowed.
        """
        if spin not in ParticleConfig.SPIN_OPTIONS:
            raise ValueError(
                f"spin must be in {ParticleConfig.SPIN_OPTIONS}"
            )
        if zero_modes.lower() not in ParticleConfig.ZERO_MODES_OPTIONS:
            raise ValueError(
                f"zero_modes must be in {ParticleConfig.ZERO_MODES_OPTIONS}"
            )


class BubbleConfig:
    r"""Bubble configuration for background field.

    Stores the dimension, the potential :math:`V(\phi)` and the background field
    as a function of the radius :math:`\phi(r)`.

    Parameters for initialisation below.

    Parameters
    ----------
    V : function
        Potential function :math:`V(\phi)`.
    phi_metaMin : float
        Location of metastable minimum.
    R : array_like
        Array of radial points, monotonically increasing.
    Phi : array_like
        Array of values for the bubble profile :math:`\phi(r)`,
        corresponding to the radial points :py:data:`R`.
    dim : int
        The dimension. The bubble profile has :math:`O({\rm dim})` symmetry.
    phi_eps : float, optional
        Small value with which to take numerical derivatives with respect
        to the field.
    dV : function, optional
        First derivative of potential with respect to the field
        :math:`V'(\phi)`.
    d2V :function, optional
        Second derivative of potential with respect to the field
        :math:`V''(\phi)`.
    dPhi : array_like, optional
        Array of values for the radial derivative of the bubble profile
        :math:`\phi '(r)`, corresponding to the radial points :py:data:`R`.
    massless_Higgs : bool, optional
        True if Higgs is massless in the metastable phase. Default is False.
    scaleless: bool, optional
        True if the potential is classically scaleless.
    """

    def __init__(
        self,
        V,
        phi_metaMin,
        R,
        Phi,
        dim,
        phi_eps=1e-3,
        dV=None,
        d2V=None,
        dPhi=None,
        massless_Higgs=False,
        scaleless=False,
    ):
        self.dim = int(dim + 0.5)
        self.phi_metaMin = phi_metaMin
        self.phi_eps = phi_eps
        self.V = V
        self.R = R
        self.Phi = Phi
        if dV is None:
            self.dV = lambda phi: derivative(self.V, phi, dx=phi_eps)
        else:
            self.dV = dV
        if d2V is None:
            if dV is None:
                self.d2V = lambda phi: derivative(self.V, phi, dx=phi_eps, n=2)
            else:
                self.d2V = lambda phi: derivative(self.dV, phi, dx=phi_eps)
        else:
            self.d2V = d2V
        if dPhi is None:
            self.dPhi = deriv14(Phi, R)
        else:
            self.dPhi = dPhi
        # mass in metastable phase
        self.m_Higgs_meta = np.sqrt(self.d2V(self.phi_metaMin))
        # radial midpoint
        phi_midpoint = 0.5 * (self.Phi[0] + self.Phi[-1])
        i_midpoint = np.argmin(abs(self.Phi - phi_midpoint))
        self.r_mid = self.R[i_midpoint]
        self.massless_Higgs = massless_Higgs
        self.scaleless=scaleless

    @classmethod
    def fromCosmoTransitions(
        cls,
        single_field_instanton,
        profile,
        massless_Higgs=False,
        scaleless=False,
    ):
        """Initialisation from CosmoTransitions objects.

        Called as a class function.

        Parameters
        ----------
        single_field_instanton : SingleFieldInstanton
            SingleFieldInstanton class object, from CosmoTransitions.
        profile : Profile
            Profile class object, from CosmoTransitions.
        massless_Higgs : bool, optional
            True if Higgs is massless in the metastable phase. Default is False.

        Returns
        -------
        cls : BubbleConfig
            An object of the BubbleConfig class.
        """
        return cls(
            single_field_instanton.V,
            single_field_instanton.phi_metaMin,
            profile.R,
            profile.Phi,
            int(single_field_instanton.alpha + 1 + 0.5),
            phi_eps=single_field_instanton.phi_eps,
            dV=single_field_instanton.dV,
            d2V=single_field_instanton.d2V,
            dPhi=profile.dPhi,
            massless_Higgs=massless_Higgs,
            scaleless=scaleless,
        )


class DeterminantConfig:
    r"""
    Combines one BubbleConfig and one ParticleConfig class.
    """
    def __init__(
        self,
        bubble,
        particle,
        renormalisation_scale=None,
        gauge_groups=None,
        thermal=False,
    ):
        r"""Initialisation

        Takes one BubbleConfig and one ParticleConfig instance. Provides the
        necessary configuration data for a single particle determinant.

        Parameters
        ----------
        bubble : BubbleConfig
            Class describing the background field.
        particle : ParticleConfig
            Class describing the fluctuating particle.
        renormalisation_scale : float
            The renormalisation scale in the :math:`\text{MS}` bar scheme. If
            `None`, set to the mass of the nucleating field.
        gauge_groups : list, optional
            List of unbroken and broken gauge groups.
        thermal : boole, optional
            If True, includes the thermal dynamical prefactor. Default is False.
        """
        # unpacking bubble
        self.dim = bubble.dim
        self.phi_metaMin = bubble.phi_metaMin
        self.phi_eps = bubble.phi_eps
        self.V = bubble.V
        self.R = bubble.R
        self.Phi = bubble.Phi
        self.dV = bubble.dV
        self.d2V = bubble.d2V
        self.dPhi = bubble.dPhi
        self.m_Higgs_meta = bubble.m_Higgs_meta
        self.r_mid = bubble.r_mid
        self.massless_Higgs = bubble.massless_Higgs
        self.scaleless=bubble.scaleless

        # unpacking particle
        self.W_Phi = particle.W_Phi
        self.spin = particle.spin
        self.dof_internal = particle.dof_internal
        self.zero_modes = particle.zero_modes

        # initialising derived quantities from combination
        self.W = self.W_Phi(self.Phi)
        self.W_inf = self.W_Phi(self.phi_metaMin)
        self.Delta_W = self.W - self.W_inf
        self.Delta_W_interp = interpolate.interp1d(
            self.R, self.Delta_W, kind="cubic"
        )
        self.m_W_meta = np.sqrt(self.W_Phi(self.phi_metaMin))
        self.m_max = np.sqrt(max(max(self.W), self.m_Higgs_meta**2))

        # setting renormalisation scale
        if renormalisation_scale is None:
            if bubble.m_Higgs_meta > 0:
                self.renormalisation_scale = bubble.m_Higgs_meta
            else:
                self.renormalisation_scale = 1
        else:
            self.renormalisation_scale = renormalisation_scale

        # assigning additional flags etc
        self.gauge_groups = gauge_groups
        self.thermal = thermal
