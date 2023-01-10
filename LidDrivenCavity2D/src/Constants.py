# *****************************************************************************
# *                          CONSTANTS - LID CAVITY                           *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: contains constant variables.                                 *
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
DIR_PRESSURE = "pressure"
DIR_VELOCITYX = "velocityX"
DIR_VELOCITYY = "velocityY"
DIR_REFERENCES = "references"
DIR_WARNINGS = DIR_REPORTS + OS_SEP + "Warnings"

# =========================================================================== #
#
# =========================================================================== #
PRESSURE_OUTPUT = "pressure"
VELOCITY_OUTPUT = "velocity"
VELOCITYX_OUTPUT = "velocityX"
VELOCITYY_OUTPUT = "velocityY"
GHIA_VELOCITY_VERTICAL = "ghiaVelocityVertical"
GHIA_VELOCITY_HORIZONTAL = "ghiaVelocityHorizontal"
AGARWAL_VELOCITY_VERTICAL = "AgarwalVelocityVertical"
AGARWAL_VELOCITY_HORIZONTAL = "AgarwalVelocityHorizontal"

FILE_SEP = ";"
DECIMAL_SEP = "."
