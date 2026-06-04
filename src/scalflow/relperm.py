import numpy as np
import numpy.typing as npt


def s_eff(
    sw: npt.NDArray[np.float64], swr: np.float64, snwr: np.float64
) -> npt.NDArray[np.float64]:
    r"""Calculate the effective wetting phase saturation.

    Parameters
    ----------
    sw : npt.NDArray[np.float64]
        Wetting phase saturation array.
    swr : np.float64
        Residual wetting phase saturation.
    snwr : np.float64
        Residual non-wetting phase saturation.

    Returns
    -------
    npt.NDArray[np.float64]
        Effective wetting phase saturation array.

    Notes
    -----
    The effective saturation ($S_{eff}$) is calculated using the formula:

    $$S_{eff} = \frac{S_w - S_{wr}}{1 - S_{wr} - S_{nwr}}$$

    where:

    - $S_w$: Wetting phase saturation.
    - $S_{wr}$: Residual wetting phase saturation.
    - $S_{nwr}$: Residual non-wetting phase saturation.
    """
    s_eff_array = (sw - swr) / (1 - swr - snwr)

    return s_eff_array


def krw(
    s_eff: npt.NDArray[np.float64], krw0: np.float64, nw: np.float64
) -> npt.NDArray[np.float64]:
    r"""Calculate the relative permeability of the wetting phase.

    Parameters
    ----------
    s_eff : npt.NDArray[np.float64]
        Effective wetting phase saturation array.
    krw0 : np.float64
        Endpoint relative permeability for the wetting phase.
    nw : np.float64
        Corey exponent for the wetting phase.

    Returns
    -------
    npt.NDArray[np.float64]
        Relative permeability of the wetting phase array.

    Notes
    -----
    The relative permeability of the wetting phase ($k_{rw}$) is calculated using the
    Corey model:

    $$k_{rw} = k_{rw0} \cdot S_{eff}^{n_w}$$

    where:

    - $k_{rw0}$ is the endpoint relative permeability for the wetting phase.
    - $S_{eff}$ is the effective wetting phase saturation.
    - $n_w$ is the Corey exponent for the wetting phase.
    """
    krw_array = krw0 * s_eff**nw

    return krw_array
