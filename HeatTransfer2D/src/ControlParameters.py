# *****************************************************************************
# *                 CONTROL PARAMETERS - 2D HEAT TRANSFER                     *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: parameters of the 2D heat transfer numerical solution,       *
# using Finite Volume Method.                                                 *
# *****************************************************************************
import numpy as np
import Constants as ct


class ControlParameters:

    def __init__(self):
        self.maxIterations: np.int64
        self.stabilityParamenter: np.int64

        self.nodeNumber: np.int64
        self.nodeNumberY: np.int64
        self.maxNodeNumberX: np.int64
        self.maxNodeNumberY: np.int64
        self.ghostNodeNumberX: np.int64
        self.ghostNodeNumberY: np.int64

        self.CFL: np.float64  # -
        self.PI: np.float64  # -
        self.width: np.float64  # m
        self.length: np.float64  # m
        self.convection: np.float64  # W / (m**2 * K)
        self.diffusivity: np.float64  # m**2 / s
        self.conductivity: np.float64  # W / (m * K)
        self.maxDeltaT: np.float64  # s
        self.iterTolerance: np.float64  # -
        self.relaxationConstant: np.float64  # -

        self.finalTime: np.float64  # s
        self.initialTime: np.float64  # s

        self.heatSource: np.float64  # W / m**2
        self.initialTemperature: np.float64
        self.environmentTemperature: np.float64  # K

        self.finalPositionX: np.float64  # m
        self.finalPositionY: np.float64  # m
        self.initialPositionX: np.float64  # m
        self.initialPositionY: np.float64  # m

        self.heatSourcePositionEnd1: np.float64
        self.heatSourcePositionStart1: np.float64

        self.heatSourcePositionEnd2: np.float64
        self.heatSourcePositionStart2: np.float64

        self.solutionMethod: str

        self.PI = np.pi

        # Solution method:
        # ---------------
        self.problemType = ct.ROBIN_PROBLEM
        self.solutionMethod = ct.EXPLICIT  # 1: explicit; 2: implicit
        self.problemDimension = ct.TWO_DIMENSIONAL
        # Physical properties:
        # -------------------
        self.width = 0.01
        self.length = 0.02
        self.convection = 20.0
        self.diffusivity = 3.95E-6
        self.conductivity = 14.9
        self.heatSource = 5.0E4

        if self.problemType == ct.DIRICHLET_PROBLEM:

            self.initialTemperature = 0.0

            if self.problemDimension == ct.ONE_DIMENSIONAL:
                self.tempWest = 0.
                self.tempEast = 0.
            elif self.problemDimension == ct.TWO_DIMENSIONAL:
                self.tempWest = 75.
                self.tempEast = 50.
                self.tempNorth = 100.
                self.tempSouth = 25.
            elif self.problemDimension == ct.THREE_DIMENSIONAL:
                self.tempWest = 0.
                self.tempEast = 30.
                self.tempNorth = 0.
                self.tempSouth = 0.
                self.tempTop = 0
                self.tempbBottom = 0.
            else:
                print("ERROR:: Choose the right dimension!")
                exit()

        else:
            self.initialTemperature = 30.0 #+ 273.15
            self.environmentTemperature = 30.0 #+ 273.15

        # Convergence parameters:
        # ---------------------
        self.maxIterations = 100
        self.iterTolerance = 1.0E-3
        self.relaxationConstant = 1
        self.heatBalanceTolerance = 1.0E-4

        # Stability parameter:
        # -------------------
        self.CFL = 0.5
        self.maxDeltaT = 1E-4
        self.stabilityParamenter = 1  # 0:: uses CFL, 1:: uses maxDeltaT

        # Time domain definitions:
        # ----------------------
        self.finalTime = 60.0
        self.initialTime = 0.0

        # Physical domain definitions:
        # ---------------------------
        self.finalPositionX = 0.02
        self.initialPositionX = 0.0

        self.finalPositionY = 0.01
        self.initialPositionY = 0.0

        self.heatSourcePositionEnd1 = 0.008
        self.heatSourcePositionStart1 = 0.003

        self.heatSourcePositionEnd2 = 0.017
        self.heatSourcePositionStart2 = 0.012

        # Mesh definitions(uniform and structured):
        # -----------------------------------------
        self.nodeNumberX = 256
        self.nodeNumberY = 256
        self.ghostNodeNumberX = 2
        self.ghostNodeNumberY = 2
        self.maxNodeNumberX = self.nodeNumberX + self.ghostNodeNumberX
        self.maxNodeNumberY = self.nodeNumberY + self.ghostNodeNumberY
