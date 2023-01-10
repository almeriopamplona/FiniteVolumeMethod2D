# *****************************************************************************
# *                          ANALYTICAL SOLUTION                              *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# *                                 T_n                                       *
# *                        + ------------------ +                             *
# *                        |                    |                             *
# *                        |                    |                             *
# *                  T_w   |                    |  T_e                        *
# *                        |                    |                             *
# *                        |                    |                             *
# *                        + ------------------ +                             *
# *                                 T_s                                       *
# *****************************************************************************
import time
import numpy as np
import pandas as pd
from Solid import Solid
from PostProcess import PostProcess


class AnalyticalSolver(PostProcess):

    def solveDirichletPlate(self, solid: Solid):

        i: int
        j: int
        k: int
        Lx: float
        Ly: float
        mnx: int
        mny: int
        SUM: float
        beta: float
        maxIter: int
        axisX: np.array
        axisY: np.array
        tempEast: float
        tempWest: float
        tempNorth: float
        tempSouth: float
        outputTemperature: pd.DataFrame
        temperatureFieldSpace: np.array

        solid.temperature = self.setBoundaryConditions(solid)
        temperatureFieldSpace = np.zeros(solid.temperature.shape, dtype=float)
        Lx = solid.length
        Ly = solid.width
        maxIter = 1000
        mnx = solid.maxNodeNumberX
        mny = solid.maxNodeNumberY

        axisX = np.linspace(
            self.initialPositionX - self.deltaX,
            self.finalPositionX + self.deltaX, mnx)
        axisY = np.linspace(
            self.initialPositionY - self.deltaY,
            self.finalPositionY + self.deltaY, mny)

        start = time.time()

        for i in range(1, mny - 1):
            for j in range(1, mnx - 1):

                tempSouth = 0.
                for k in range(1, maxIter):
                    beta = k * np.pi / Lx

                    SUM = (2 * solid.tempSouth / np.pi) * \
                        (((-1) ** (k + 1) + 1) / k) * (
                        -np.sinh(beta * axisY[i]) / np.tanh(beta * Ly) +
                        np.cosh(beta * axisY[i])) * np.sin(beta * axisX[j])

                    if ~np.isnan(SUM) and ~np.isinf(SUM):
                        tempSouth += SUM

                tempEast = 0.
                for k in range(1, maxIter):
                    beta = k * np.pi / Ly

                    SUM = (2 * solid.tempEast / np.pi) * \
                        (((-1)**(k+1) + 1) / k) * np.sinh(beta * axisX[j]) * \
                        np.sin(beta * axisY[i]) / np.sinh(beta * Lx)

                    if ~np.isnan(SUM) and ~np.isinf(SUM):
                        tempEast += SUM

                tempNorth = 0.
                for k in range(1, maxIter):
                    beta = k * np.pi / Lx

                    SUM = (2 * solid.tempNorth / np.pi) * \
                        (((-1)**(k+1) + 1) / k) * np.sinh(beta * axisY[i]) * \
                        np.sin(beta * axisX[j]) / np.sinh(beta * Ly)

                    if ~np.isnan(SUM) and ~np.isinf(SUM):
                        tempNorth += SUM

                tempWest = 0.
                for k in range(1, maxIter):
                    beta = k * np.pi / Ly

                    SUM = (2 * solid.tempWest / np.pi) * \
                        (((-1)**(k+1) + 1) / k) * (
                        -np.sinh(beta * axisX[j]) / np.tanh(beta * Lx) +
                        np.cosh(beta * axisX[j])) * np.sin(beta * axisY[i])

                    if ~np.isnan(SUM) and ~np.isinf(SUM):
                        tempWest += SUM

                temperatureFieldSpace[i, j] = tempSouth + tempEast + \
                    tempNorth + tempWest

        solid.temperature[1:mny-1, 1:mnx-1] = \
            temperatureFieldSpace[1:mny-1, 1:mnx-1]

        outputTemperature = pd.DataFrame(data={
            "x": solid.coordinateX,
            "y": solid.coordinateY,
            "temperature": solid.temperature[1:mny - 1, 1:mnx - 1].reshape(
                solid.coordinateX.shape)
        })

        self.saveOutputs(outputTemperature, self.getAnalyticalSolutionPath)

        end = time.time()

        print("Elapsed time: {}".format(end - start))

    @staticmethod
    def setBoundaryConditions(solid: Solid) -> np.array:

        mnx: int
        mny: int
        temperatureFieldAux: np.array

        mnx = solid.maxNodeNumberX
        mny = solid.maxNodeNumberY
        temperatureFieldAux = solid.temperature.copy()

        # BOTTOM:
        temperatureFieldAux[0, :] = solid.tempSouth
        # EAST
        temperatureFieldAux[:, mnx - 1] = solid.tempEast
        # TOP
        temperatureFieldAux[mny - 1, :] = solid.tempNorth
        # WEST
        temperatureFieldAux[:, 0] = solid.tempWest

        return temperatureFieldAux
