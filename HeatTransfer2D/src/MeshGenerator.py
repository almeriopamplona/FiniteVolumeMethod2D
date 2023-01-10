# *****************************************************************************
# *                    MESH GENERATOR - 2D HEAT TRANSFER                      *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: generates the mesh parameters and coordinates.               *
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
        self.nodeHeatSourceEnd1: float
        self.nodeHeatSourceStart1: float
        self.nodeHeatSourceEnd2: float
        self.nodeHeatSourceStart2: float

        self.deltaT, self.deltaX, self.deltaY, self.timeSize, \
            self.spaceSizeX, self.spaceSizeY = self.getMeshParameters()

        self.time = self.getTimeVector()
        self.invDeltaX = 1. / self.deltaX
        self.invDeltaY = 1. / self.deltaY
        self.coordinateX, self.coordinateY = self.getCoordinates()

        self.nodeHeatSourceEnd1, self.nodeHeatSourceStart1, \
            self.nodeHeatSourceEnd2, self.nodeHeatSourceStart2 = \
            self.getSourceNodes()

    def getMeshParameters(self) -> tuple:

        deltaT: float
        deltaX: float
        deltaY: float
        timeSize: int
        tempDeltaT: float
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
        tempDeltaT = 1E-3

        if self.stabilityParamenter == 0:

            tempDeltaT = \
                self.CFL * deltaX * deltaY / \
                (self.diffusivity * deltaY + self.diffusivity * deltaX)

        elif self.stabilityParamenter == 1:

            tempDeltaT = self.maxDeltaT

        else:
            print("ERROR:: define a proper stability parameter!")
            exit()

        maxDeltaT = self.CFL * deltaX * deltaY / (
                    self.diffusivity * deltaY + self.diffusivity * deltaX)

        timeSize = int(np.ceil(
            (self.finalTime - self.initialTime) / tempDeltaT))

        deltaT = (self.finalTime - self.initialTime) / (timeSize - 1)

        print("deltaT: {}, max deltaT: {}, Number of Time Steps: {}".format(
            deltaT, maxDeltaT, timeSize))

        return deltaT, deltaX, deltaY, timeSize, spaceSizeX, spaceSizeY

    def getSourceNodes(self) -> tuple:

        axis: np.array
        nodeHeatSourceEnd2: int
        nodeHeatSourceEnd1: int
        nodeHeatSourceStart1: int
        nodeHeatSourceStart2: int

        nodeHeatSourceEnd2 = 0
        nodeHeatSourceEnd1 = 0
        nodeHeatSourceStart1 = 0
        nodeHeatSourceStart2 = 0

        axisX = np.linspace(
            self.initialPositionX, self.finalPositionX, self.nodeNumberX)

        for i in range(self.nodeNumberX):
            if self.heatSourcePositionStart1 <= axisX[i] \
                    <= self.heatSourcePositionEnd1:
                nodeHeatSourceStart1 = i+1
                break

        for i in range(self.nodeNumberX):
            if self.heatSourcePositionStart1 <= axisX[i] \
                    <= self.heatSourcePositionEnd1:
                nodeHeatSourceEnd1 = i+1

        for i in range(self.nodeNumberX):
            if self.heatSourcePositionStart2 <= axisX[i] \
                    <= self.heatSourcePositionEnd2:
                nodeHeatSourceStart2 = i+1
                break

        for i in range(self.nodeNumberX):
            if self.heatSourcePositionStart2 <= axisX[i] \
                    <= self.heatSourcePositionEnd2:
                nodeHeatSourceEnd2 = i+1

        return nodeHeatSourceEnd1, nodeHeatSourceStart1, nodeHeatSourceEnd2, \
            nodeHeatSourceStart2

    def getProbePosition(
            self, positionX: np.float, positionY: np.float) -> tuple:

        axisX = np.linspace(
            self.initialPositionX, self.finalPositionX, self.nodeNumberX)
        axisY = np.linspace(
            self.initialPositionY, self.finalPositionY, self.nodeNumberY)

        lowerBoundX = positionX - self.deltaX
        upperBoundX = positionX + self.deltaX

        lowerBoundY = positionY - self.deltaY
        upperBoundY = positionY + self.deltaY

        lowerPositionX = 0
        lowerPositionY = 0
        upperPositionX = 0
        upperPositionY = 0

        k = 0
        for i in range(self.nodeNumberX):
            if lowerBoundX <= axisX[i] <= upperBoundX and k == 0:
                lowerPositionX = i
                k += 1
            elif lowerBoundX <= axisX[i] <= upperBoundX and k > 0:
                upperPositionX = i

        k = 0
        for j in range(self.nodeNumberY):
            if lowerBoundY <= axisY[j] <= upperBoundY and k == 0:
                lowerPositionY = j
                k += 1
            elif lowerBoundY <= axisY[j] <= upperBoundY and k > 0:
                upperPositionY = j

        return lowerPositionX, upperPositionX, lowerPositionY, upperPositionY

    def getTimeVector(self) -> np.array:

        time: np.array

        time = np.linspace(
            self.initialTime, self.finalTime, self.timeSize)

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

    def getMeshgrid(self):

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY
        axisX = np.linspace(self.initialPositionX, self.finalPositionX, mnx)
        axisY = np.linspace(self.initialPositionY, self.finalPositionY, mny)

        coordinatesX, coordinatesY = np.meshgrid(axisX, axisY)

        return coordinatesX, coordinatesY
