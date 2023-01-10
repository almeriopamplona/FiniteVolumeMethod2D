# *****************************************************************************
# *                     CONTROL PARAMETERS - LID CAVITY                       *
# *****************************************************************************
# * Author: Almério José Venâncio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: parameters of the Lid Cavity numerical solution, using       *
# * Finite Volume Method.                                                     *
# *****************************************************************************
import numpy as np


class ControlParameters:

    def __init__(self):

        self.maxIterations: int
        self.stabilityParamenter: int

        self.nodeNumber: int
        self.nodeNumberY: int
        self.maxNodeNumberX: int
        self.maxNodeNumberY: int
        self.ghostNodeNumberX: int
        self.ghostNodeNumberY: int

        self.meshfilename: str
        self.pressurefilename: str
        self.velocityXfilename: str
        self.velocityYfilename: str
        self.estpressurefilename: str
        self.estvelocityXfilename: str
        self.estvelocityYfilename: str

        self.CFL: float                           # -
        self.PI: float                            # -
        self.length: float                        # m
        self.density: float                       # kg / m ** 3
        self.maxDeltaT: float                     # s
        self.toleranceMass: float                 # -
        self.reynoldsNumber: float                # -
        self.tolerancePressure: float             # -
        self.relaxationConstant: float            # -
        self.kinematicViscosity: float            # Pa * s

        self.finalTime: float                     # s
        self.initialTime: float                   # s

        self.velocityTopX: float                  # m / s
        self.velocityTopY: float                  # m / s
        self.velocityLeftX: float                 # m / s
        self.velocityLeftY: float                 # m / s
        self.velocityRightX: float                # m / s
        self.velocityRightY: float                # m / s
        self.velocityBottomX: float               # m / s
        self.velocityBottomY: float               # m / s

        self.finalPositionX: float                # m
        self.finalPositionY: float                # m
        self.initialPositionX: float              # m
        self.initialPositionY: float              # m

        self.pressureGradientTop: float           # Pa / m
        self.pressureGradientBottom: float        # Pa / m
        self.pressureGradientLeft: float          # Pa / m
        self.pressureGradientRight: float         # Pa / m
            
        PI = np.pi

        # Walls initial conditions:
        # ------------------------

        # velocity:
        self.velocityLeftX = 0.0
        self.velocityLeftY = 0.0
        self.velocityRightX = 0.0
        self.velocityRightY = 0.0

        self.velocityTopX = 1.0
        self.velocityTopY = 0.0
        self.velocityBottomX = 0.0
        self.velocityBottomY = 0.0

        # pressure gradient
        self.pressureGradientLeft = 0.0
        self.pressureGradientRight = 0.0
        self.pressureGradientTop = 0.0
        self.pressureGradientBottom = 0.0

        # Physical properties:
        # -------------------
        self.length = 1.0 # height(y - axis) = length(x - axis)
        self.density = 1.0 / 6.0
        self.reynoldsNumber = 7500.0
        self.kinematicViscosity = \
            (self.velocityTopX * self.length) / self.reynoldsNumber

        # Convergence parameters:
        # ---------------------
        self.maxIterations = 100
        self.toleranceMass = 1.0E-8
        self.tolerancePressure = 1.0E-3
        self.relaxationConstant = 0.8

        # Stability parameter:
        # -------------------
        self.CFL = 0.0054
        self.maxDeltaT = 2E-4
        self.stabilityParamenter = 1   # 0:: uses CFL, 1:: uses maxDeltaT

        # Time domain definitions:
        # ----------------------
        self.finalTime = 660
        self.initialTime = 200

        # Physical domain definitions:
        # ---------------------------
        self.finalPositionX = 1.0
        self.initialPositionX = 0.0

        self.finalPositionY = 1.0
        self.initialPositionY = 0.0

        # Mesh definitions(uniform and structured):
        # -----------------------------------------
        self.nodeNumberX = 128
        self.nodeNumberY = 128
        self.ghostNodeNumberX = 2
        self.ghostNodeNumberY = 2
        self.maxNodeNumberX = self.nodeNumberX + self.ghostNodeNumberX
        self.maxNodeNumberY = self.nodeNumberY + self.ghostNodeNumberY
