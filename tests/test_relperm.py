import numpy as np

from scalflow.relperm import krw, s_eff


def test_s_eff_basic():
    """Test effective saturation calculation with basic inputs."""
    sw = np.array([0.3, 0.5, 0.7])
    swr = np.float64(0.2)
    snwr = np.float64(0.1)
    result = s_eff(sw, swr, snwr)
    expected = np.array([0.142857, 0.428571, 0.714286])
    np.testing.assert_allclose(result, expected, rtol=1e-5)


def test_krw_basic():
    """Test water relative permeability calculation with basic inputs."""
    s_eff_values = np.array([0.0, 0.5, 1.0])
    krw0 = np.float64(0.8)
    nw = np.float64(2.0)
    result = krw(s_eff_values, krw0, nw)
    expected = np.array([0.0, 0.2, 0.8])
    np.testing.assert_allclose(result, expected, rtol=1e-5)
