"""Jupyter extensions for querying and interacting with Anzo
"""

__author__ = """Cambridge Semantics"""
__email__ = ""
__version__ = "2.0.0"

from .anzo_magics import AnzoMagics
from .arrow_flight_magics import FlightMagics

def load_ipython_extension(ipython):
    """
    Gets executed by Jupyter when you run this in a cell:

        %load_ext anzo_jupyter

    This will load all of the magics that are found in this library.
    """

    ipython.register_magics(AnzoMagics)
    ipython.register_magics(FlightMagics)
