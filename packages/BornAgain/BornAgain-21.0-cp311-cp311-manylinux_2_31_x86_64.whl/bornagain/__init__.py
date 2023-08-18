#  **************************************************************************  #
#   BornAgain: simulate and fit reflection and scattering
#
#   @file      BornAgain/__init__.py
#   @brief     Python extensions of the SWIG-generated Python module bornagain.
#
#   @homepage  http://apps.jcns.fz-juelich.de/BornAgain
#   @license   GNU General Public License v3 or higher (see COPYING)
#   @copyright Forschungszentrum Juelich GmbH 2016
#   @authors   Scientific Computing Group at MLZ (see CITATION, AUTHORS)
#  **************************************************************************  #

version = (21, 0)
version_str = "21.0"

# import all available BornAgain functionality
from .lib import *
