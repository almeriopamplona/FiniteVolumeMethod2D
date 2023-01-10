# *****************************************************************************
# *                     POISSON EQUATION - LID CAVITY                         *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: contains the Poisson Equation discrete form and the pressure *
# * treatment on the boundaries.                                              *
# *****************************************************************************
import numpy as np
from MeshGenerator import MeshGenerator


class PoissonEquation(MeshGenerator):

    def __init__(self):

        super().__init__()

    def getPoissonSolution(
            self, estimateVelocityX: np.array, estimateVelocityY: np.array) -> \
            np.array:

        mnx: int
        mny: int
        poissonSolution: np.array
        verticalDivergent: np.array
        horizontalDivergent: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        poissonSolution = np.zeros((mny, mnx), dtype=np.float)

        horizontalDivergent = self.invDeltaX * (
                estimateVelocityX[1:mny - 1, 1:mnx - 1] -
                estimateVelocityX[1:mny - 1, 0:mnx - 2])

        verticalDivergent = self.invDeltaY * (
                estimateVelocityY[1:mny - 1, 1:mnx - 1] -
                estimateVelocityY[0:mny - 2, 1:mnx - 1])

        stressTerm = \
            horizontalDivergent ** 2 + \
            2 * horizontalDivergent * verticalDivergent + \
            verticalDivergent ** 2

        poissonSolution[1: mny - 1, 1:mnx - 1] = \
            horizontalDivergent + verticalDivergent - stressTerm

        return poissonSolution

    def boundaryConditionsPressure(self, pressure: np.array) -> np.array:

        mnx: int
        mny: int
        pressureTemp: np.array

        mnx = self.maxNodeNumberX - 1
        mny = self.maxNodeNumberY - 1
        pressureTemp = pressure.copy()

        # LEFt WALL
        pressureTemp[:, 0] = pressure[:, 1]
        # BOTTOM WALL
        pressureTemp[0, :] = pressure[1, :]
        # RIGHT WALL
        pressureTemp[:, mnx] = pressure[:, mnx - 1]
        # TOP WALL
        pressureTemp[mny, :] = self.pressureGradientTop

        return pressureTemp

    def solvePoissonEquation(
            self, poissonSolution: np.array, coefficientCenter: float,
            coefficientEast: float, coefficientWest: float,
            coefficientNorth: float, coefficientSouth: float) -> np.array:

        k: int
        mnx: int 
        mny: int  
        maxItera: int

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        maxItera = 100

        estimatePressure = np.zeros((mny, mnx), dtype=np.float)
        temporaryPressure = estimatePressure.copy()

        k = 0
        norm = 0.
        # Newton - Raphson method with under - relaxation:
        for k in range(maxItera + 1):

            estimatePressure[1: mny - 1, 1: mnx - 1] = \
                temporaryPressure[1: mny - 1, 1: mnx - 1] - \
                self.relaxationConstant * (
                    coefficientCenter *
                    temporaryPressure[1:mny - 1, 1:mnx - 1] +
                    coefficientEast * temporaryPressure[1:mny - 1, 2:mnx] +
                    coefficientWest * temporaryPressure[1:mny - 1, 0:mnx - 2] +
                    coefficientNorth * temporaryPressure[2:mny, 1:mnx - 1] +
                    coefficientSouth * temporaryPressure[0:mny - 2, 1:mnx - 1] -
                    poissonSolution[1:mny - 1, 1:mnx - 1]) / coefficientCenter

            norm = np.sqrt(np.sum((estimatePressure - temporaryPressure) ** 2))

            if norm <= self.tolerancePressure:
                # print(
                #     "WARNING:: Pressure converged!, " +
                #     "error = {} and num iter = {}".format(norm, k))
                break

            temporaryPressure = estimatePressure

        # if (k >= maxItera) and (norm > 1.0):
        #     print("WARNING:: Pressure did not converged!, "
        #           "error = {}, num iter = {}".format(norm, k))

        return estimatePressure

    def getMassConservation(
            self, velocityX: np.array, velocityY: np.array) -> float:

        mnx: int
        mny: int
        continuity: float
        massConservation: np.array
        verticalDivergent: np.array
        horizontalDivergent: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        horizontalDivergent = self.invDeltaX * (
            velocityX[1:mny - 1, 1:mnx - 1] - velocityX[1:mny - 1, 0:mnx - 2])

        verticalDivergent = self.invDeltaY * (
            velocityY[1:mny - 1, 1:mnx - 1] - velocityY[0:mny - 2, 1:mnx - 1])

        massConservation = horizontalDivergent + verticalDivergent

        continuity = massConservation.sum()

        return continuity
