# *****************************************************************************
# *                       MESH GENERATOR - LID CAVITY                         *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: generates the mesh parameters and coordinates.               *                                                  *
# *****************************************************************************

import numpy as np
from ControlParameters import ControlParameters


class MeshGenerator(ControlParameters):

    def __init__(self):

        super().__init__()

        self.time: np.array
        self.deltaT: float
        self.deltaX: float
        self.deltaY: float
        self.timeSize: int
        self.invDeltaX: float
        self.invDeltaY: float
        self.spaceSizeX: int
        self.spaceSizeY: int
        self.coordinateX: np.array
        self.coordinateY: np.array

        self.deltaT, self.deltaX, self.deltaY, self.timeSize, \
            self.spaceSizeX, self.spaceSizeY = self.getMeshParameters()

        self.time = self.getTimeVector()
        self.invDeltaX = 1. / self.deltaX
        self.invDeltaY = 1. / self.deltaY
        self.coordinateX, self.coordinateY = self.getCoordinates()

    def getMeshParameters(self) -> tuple:

        deltaT: float
        deltaX: float
        deltaY: float
        timeSize: int
        spaceSizeX: int
        spaceSizeY: int

        # space allocations
        deltaX = \
            (self.finalPositionX - self.initialPositionX) / \
            (self.nodeNumberX - 1)
        deltaY = \
            (self.finalPositionY - self.initialPositionY) / \
            (self.nodeNumberY - 1)

        spaceSizeX = self.maxNodeNumberX * self.maxNodeNumberY
        spaceSizeY = self.maxNodeNumberX * self.maxNodeNumberY

        # time allocations
        if self.stabilityParamenter == 0:

            tempDeltaT = \
                self.CFL * deltaX * deltaY / \
                (self.velocityTopX * deltaY + self.velocityTopX * deltaX)

        elif self.stabilityParamenter == 1:

            tempDeltaT = self.maxDeltaT

        else:
            print("ERROR:: define a proper stability parameter!")
            exit()

        timeSize = int(np.ceil(
            (self.finalTime - self.initialTime) / tempDeltaT))

        deltaT = (self.finalTime - self.initialTime) / (timeSize - 1)

        print("deltaT {}, Number of Time Steps: {}".format(deltaT, timeSize))

        return deltaT, deltaX, deltaY, timeSize, spaceSizeX, spaceSizeY

    def getTimeVector(self) -> np.array:

        time: np.array

        time = np.arange(
            self.initialTime, self.finalTime, self.deltaT, dtype=float)

        return time

    def getCoordinates(self) -> tuple:

        j: int
        i: int
        nx: int
        ny: int
        rows: int
        coordinatesX: np.array
        coordinatesY: np.array

        nx = self.nodeNumberX
        ny = self.nodeNumberY

        rows = ny * nx

        coordinatesX = np.zeros((rows,), dtype=float)
        coordinatesY = np.zeros((rows,), dtype=float)

        for j in range(rows):
            coordinatesX[j] = \
                self.initialPositionX + self.deltaX * np.mod(j, nx)

        k = 0
        for i in range(rows):
            coordinatesY[i] = \
                self.initialPositionY + self.deltaY * k

            if np.mod(i, nx) == 0:
                k += 1

        return coordinatesX, coordinatesY
