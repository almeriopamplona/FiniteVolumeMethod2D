import numpy as np
from MeshGenerator import MeshGenerator


class PoissonEquation(MeshGenerator):

    def __init__(self):

        super().__init__()

    def getPoissonMatrix(self) -> np.array:

        i: int
        k: int
        nx: int
        ny: int
        coefficientEast: float
        coefficientWest: float
        coefficientNorth: float
        coefficientSouth: float
        coefficientCenter: float
        coefficientMatrix: np.array

        nx = self.nodeNumberX ** 2
        ny = self.nodeNumberX ** 2

        coefficientEast = self.deltaT / self.deltaX ** 2
        coefficientWest = self.deltaT / self.deltaX ** 2
        coefficientNorth = self.deltaT / self.deltaY ** 2
        coefficientSouth = self.deltaT / self.deltaY ** 2
        coefficientCenter = \
            -2.0 * self.deltaT * (self.deltaX ** 2 + self.deltaY ** 2) / \
            (self.deltaX ** 2 * self.deltaY ** 2)

        coefficientMatrix = np.zeros((ny, nx), dtype=np.float)

        # Two - dimensional phenomenon:
        for i in (ny ** 2):
            k = i + 1
            # LEFTWALL
            if np.mod(k, nx) == 1:
                # BOTTOM
                if k <= nx:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientWest + coefficientSouth
                    coefficientMatrix[i, i + 1] = coefficientEast
                    coefficientMatrix[i, i + 3] = coefficientNorth
                # TOP
                elif k >= nx ** 2 - nx + 1:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientWest + coefficientNorth
                    coefficientMatrix[i, i + 1] = coefficientEast
                    coefficientMatrix[i, i - 3] = coefficientSouth
                    # INTERIOR
                else:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientWest
                    coefficientMatrix[i, i + 1] = coefficientEast
                    coefficientMatrix[i, i + 3] = coefficientNorth
                    coefficientMatrix[i, i - 3] = coefficientSouth

            # INTERIOR
            if (np.mod(k, nx) > 1) and (np.mod(i, nx) < nx):
                # BOTTOM
                if k <= nx:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientSouth
                    coefficientMatrix[i, i + 1] = coefficientEast
                    coefficientMatrix[i, i - 1] = coefficientWest
                    coefficientMatrix[i, i + 3] = coefficientNorth
                # TOP
                elif k >= nx ** 2 - nx + 1:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientNorth
                    coefficientMatrix[i, i + 1] = coefficientEast
                    coefficientMatrix[i, i - 1] = coefficientWest
                    coefficientMatrix[i, i - 3] = coefficientSouth
                # INTERIOR
                else:
                    coefficientMatrix[i, i] = coefficientCenter
                    coefficientMatrix[i, i + 1] = coefficientEast
                    coefficientMatrix[i, i - 1] = coefficientWest
                    coefficientMatrix[i, i + 3] = coefficientNorth
                    coefficientMatrix[i, i - 3] = coefficientSouth

            # RIGHT WALL
            if np.mod(k, nx) == 0:
                # BOTTOM
                if k <= nx:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientEast + coefficientSouth
                    coefficientMatrix[i, i - 1] = coefficientWest
                    coefficientMatrix[i, i + 3] = coefficientNorth
                # TOP
                elif k >= nx ** 2 - nx + 1:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientEast + coefficientNorth
                    coefficientMatrix[i, i - 1] = coefficientWest
                    coefficientMatrix[i, i - 3] = coefficientSouth
                # INTERIOR
                else:
                    coefficientMatrix[i, i] = \
                        coefficientCenter + coefficientNorth
                    coefficientMatrix[i, i - 1] = coefficientWest
                    coefficientMatrix[i, i + 3] = coefficientNorth
                    coefficientMatrix[i, i - 3] = coefficientSouth

        return coefficientMatrix

    def getPoissonVector(self) -> np.array:

        i: int
        k: int
        nx: int
        ny: int
        numFluidElements: int

        coefficientEast: float
        coefficientWest: float
        coefficientNorth: float
        coefficientSouth: float
        coefficientCenter: float
        coefficientMatrix: np.array

        nx = self.nodeNumberX ** 2
        ny = self.nodeNumberX ** 2

        coefficientEast = self.deltaT / self.deltaX ** 2
        coefficientWest = self.deltaT / self.deltaX ** 2
        coefficientNorth = self.deltaT / self.deltaY ** 2
        coefficientSouth = self.deltaT / self.deltaY ** 2
        coefficientCenter = \
            -2.0 * self.deltaT * (self.deltaX ** 2 + self.deltaY ** 2) / \
            (self.deltaX ** 2 * self.deltaY ** 2)

        numFluidElements = 5

        coefficientVector = np.zeros((ny * numFluidElements), dtype=np.float)

        k = 0
        # Two - dimensional phenomenon:
        for i in (1, ny ** 2 + 1):
            # LEFT WALL
            if np.mod(i, nx) == 1:
                # BOTTOM
                if i <= nx:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientWest + coefficientSouth
                    coefficientVector[k + 1] = coefficientEast
                    coefficientVector[k + 3] = coefficientNorth

                    k = k + numFluidElements
                # TOP
                elif i >= nx ** 2 - nx + 1:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientWest + coefficientNorth
                    coefficientVector[k + 1] = coefficientEast
                    coefficientVector[k + 4] = coefficientSouth

                    k = k + numFluidElements
                # INTERIOR
                else:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientWest
                    coefficientVector[k + 1] = coefficientEast
                    coefficientVector[k + 3] = coefficientNorth
                    coefficientVector[k + 4] = coefficientSouth

                    k = k + numFluidElements

            # INTERIOR
            if (np.mod(i, nx) > 1) and (np.mod(i, nx) < nx):
                # BOTTOM
                if i <= nx:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientSouth
                    coefficientVector[k + 1] = coefficientEast
                    coefficientVector[k + 2] = coefficientWest
                    coefficientVector[k + 3] = coefficientNorth

                    k = k + numFluidElements
                # TOP
                elif i >= nx ** 2 - nx + 1:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientNorth
                    coefficientVector[k + 1] = coefficientEast
                    coefficientVector[k + 2] = coefficientWest
                    coefficientVector[k + 4] = coefficientSouth

                    k = k + numFluidElements
                # INTERIOR
                else:
                    coefficientVector[k] = coefficientCenter
                    coefficientVector[k + 1] = coefficientEast
                    coefficientVector[k + 1] = coefficientWest
                    coefficientVector[k + 3] = coefficientNorth
                    coefficientVector[k + 4] = coefficientSouth

                    k = k + numFluidElements

            # RIGHT WALL
            if np.mod(i, nx) == 0:
                # BOTTOM
                if i <= nx:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientEast + coefficientSouth
                    coefficientVector[k + 2] = coefficientWest
                    coefficientVector[k + 3] = coefficientNorth

                    k = k + numFluidElements
                # TOP
                elif i >= nx ** 2 - nx + 1:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientEast + coefficientNorth
                    coefficientVector[k + 2] = coefficientWest
                    coefficientVector[k + 4] = coefficientSouth

                    k = k + numFluidElements
                # INTERIOR
                else:
                    coefficientVector[k] = \
                        coefficientCenter + coefficientNorth
                    coefficientVector[k + 2] = coefficientWest
                    coefficientVector[k + 3] = coefficientNorth
                    coefficientVector[k + 4] = coefficientSouth

                    k = k + numFluidElements

        return coefficientVector

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
        nx: int   # number of nodes
        ny: int   # number of nodes
        mnx: int  # max number of nodes
        mny: int  # max number of nodes
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
