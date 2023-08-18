"""
BornAgain collection of standard simulation setups.
"""
import bornagain as ba
from bornagain import deg, angstrom


def sas(sample, npix):
    """
    Returns a standard simulation in small-angle scattering geometry.
    Incident beam is almost horizontal.
    """
    beam = ba.Beam(1, 1*angstrom, 1e-8*deg)
    det = ba.SphericalDetector(npix, 10*deg, 0, 0)
    return ba.ScatteringSimulation(beam, sample, det)
