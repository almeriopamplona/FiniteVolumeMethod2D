# *****************************************************************************
# *                     CONSTANTS - 2D HEAT TRANSFER                          *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: some hard coded variables that are used through the code and *
# * kept here to maintain the code organized.                                 *
# *****************************************************************************

import os
from pathlib import Path

# =========================================================================== #
# MASTER PATH
# =========================================================================== #
OS_SEP = os.sep
PATH = Path(os.getcwd()).absolute().parent.__str__()

# =========================================================================== #
# DIRECTORIES
# =========================================================================== #
DIR_EXECUTABLES = "src"
DIR_REPORTS = "Reports"
DIR_FIGURE = "figure"
DIR_TEMPERATURE = "temperature"
DIR_WARNINGS = DIR_REPORTS + OS_SEP + "Warnings"

# =========================================================================== #
# OUTPUT FILES
# =========================================================================== #
TEMPERATURE_OUTPUT = "temperature"
ANALYTICAL_TEMP_OUTPUT = "temperatureAnalytical"
PROBE_PLOTS = "probePlots"
PROBE1_OUTPUT = "probe1"
PROBE2_OUTPUT = "probe2"
PROBE3_OUTPUT = "probe3"

FILE_SEP = ";"
DECIMAL_SEP = "."

# =========================================================================== #
# CONSTANTS FOR THE MAIS CODE
# =========================================================================== #
EXPLICIT = "explicit"
IMPLICIT = "implicit"
ONE_DIMENSIONAL = "1D"
TWO_DIMENSIONAL = "2D"
THREE_DIMENSIONAL = "3D"
ROBIN_PROBLEM = "ROBIN_PROBLEM"
DIRICHLET_PROBLEM = "DIRICHLET_PROBLEM"

