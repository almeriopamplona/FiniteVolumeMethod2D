# *****************************************************************************
# *                    ENERGY EQUATIONS - 2D HEAT TRANSFER                    *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: class responsible for solving the energy equations on a      *
# * solid plate with two external heat sources. There is the explicit         *
# * formulation of the finite volume method (FVM) and the implicit form. One  *
# * solves the implicit form using the Newton-Raphson method with an under-   *
# * relaxation constant.                                                      *
# *****************************************************************************
import numpy as np
from MeshGenerator import MeshGenerator


class EnergyEquations(MeshGenerator):

    def __init__(self):

        super().__init__()

    def solveEnergyEquationsExplicit(
            self, temperature: np.array, diffusionCoeffX: np.float64,
            diffusionCoeffY: np.float64):

        mnx: np.int64
        mny: np.int64
        diffusionX: np.array
        diffusionY: np.array
        estimateTemperature: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        estimateTemperature = temperature.copy()

        diffusionX = diffusionCoeffX * (
            temperature[1:mny-1, 2:mnx] - 2 * temperature[1:mny-1, 1:mnx-1] +
            temperature[1:mny-1, 0:mnx-2])

        diffusionY = diffusionCoeffY * (
            temperature[2:mny, 1:mnx-1] - 2 * temperature[1:mny-1, 1:mnx-1] +
            temperature[0:mny-2, 1:mnx-1])

        estimateTemperature[1:mny-1, 1:mnx-1] = \
            temperature[1:mny-1, 1:mnx-1] + diffusionX + diffusionY

        return estimateTemperature

    def solveEnergyEquationsImplicitRobin(
            self, solid, coefficientCenter: np.float64,
            diffusionCoeffX: np.float64, diffusionCoeffY: np.float64,
            boundSource: np.float64, boundCenterX: np.float64,
            boundCenterY: np.float64, boundExternalX: np.float64,
            boundExternalY: np.float64) -> np.array:

        k: np.int64
        mnx: np.int64
        mny: np.int64
        norm: np.float
        centerDiffusion: np.array
        partialDiffusionX: np.array
        partialDiffusionY: np.array
        estimateTemperature: np.array
        temporaryTemperature: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        estimateTemperature = solid.temperature.copy()
        temporaryTemperature = solid.temperature.copy()

        k = 0
        norm = 0.0

        for k in range(self.maxIterations + 1):

            partialDiffusionX = diffusionCoeffX * (
                    temporaryTemperature[1:mny-1, 2:mnx] +
                    temporaryTemperature[1:mny-1, 0:mnx-2])

            partialDiffusionY = diffusionCoeffY * (
                    temporaryTemperature[2:mny, 1:mnx-1] +
                    temporaryTemperature[0:mny-2, 1:mnx-1])

            centerDiffusion = coefficientCenter * \
                temporaryTemperature[1:mny-1, 1:mnx-1]

            estimateTemperature[1:mny-1, 1:mnx-1] = \
                temporaryTemperature[1:mny-1, 1:mnx-1] - \
                self.relaxationConstant * (
                    centerDiffusion - partialDiffusionX - partialDiffusionY -
                    solid.temperature[1:mny-1, 1:mnx-1]) / coefficientCenter

            norm = np.sqrt(
                ((estimateTemperature - temporaryTemperature) ** 2).sum())

            if 0 < norm <= self.iterTolerance:
                # print(
                #     "WARNING:: Temperature converged!, " +
                #     "error = {} and num iter = {}".format(norm, k))
                break

            temporaryTemperature = estimateTemperature

            temporaryTemperature = self.boundariesConditionsDirichlet(
                temporaryTemperature, solid)

            temporaryTemperature = self.boundariesConditions(
                temporaryTemperature, boundSource, boundCenterX, boundCenterY,
                boundExternalX, boundExternalY)

        # if (k >= self.maxIterations) and (norm > 1.0):
        #     print(
        #         "WARNING:: Temperature did not converged!, "
        #         "error = {}, num iter = {}".format(norm, k))

        return estimateTemperature

    def solveEnergyEquationsImplicitDirichlet(
            self, solid, coefficientCenter: np.float64,
            diffusionCoeffX: np.float64, diffusionCoeffY: np.float64) -> \
            np.array:

        k: np.int64
        mnx: np.int64
        mny: np.int64
        norm: np.float
        centerDiffusion: np.array
        partialDiffusionX: np.array
        partialDiffusionY: np.array
        estimateTemperature: np.array
        temporaryTemperature: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        estimateTemperature = solid.temperature.copy()
        temporaryTemperature = solid.temperature.copy()

        k = 0
        norm = 0.0

        for k in range(self.maxIterations + 1):

            partialDiffusionX = diffusionCoeffX * (
                    temporaryTemperature[1:mny-1, 2:mnx] +
                    temporaryTemperature[1:mny-1, 0:mnx-2])

            partialDiffusionY = diffusionCoeffY * (
                    temporaryTemperature[2:mny, 1:mnx-1] +
                    temporaryTemperature[0:mny-2, 1:mnx-1])

            centerDiffusion = coefficientCenter * \
                temporaryTemperature[1:mny-1, 1:mnx-1]

            estimateTemperature[1:mny-1, 1:mnx-1] = \
                temporaryTemperature[1:mny-1, 1:mnx-1] - \
                self.relaxationConstant * (
                    centerDiffusion - partialDiffusionX - partialDiffusionY -
                    solid.temperature[1:mny-1, 1:mnx-1]) / coefficientCenter

            norm = np.sqrt(
                ((estimateTemperature - temporaryTemperature) ** 2).sum())

            if 0 < norm <= self.iterTolerance:
                # print(
                #     "WARNING:: Temperature converged!, " +
                #     "error = {} and num iter = {}".format(norm, k))
                break

            temporaryTemperature = estimateTemperature

            temporaryTemperature = self.boundariesConditionsDirichlet(
                temporaryTemperature, solid)

        # if (k >= self.maxIterations) and (norm > 1.0):
        #     print(
        #         "WARNING:: Temperature did not converged!, "
        #         "error = {}, num iter = {}".format(norm, k))

        return estimateTemperature

    def boundariesConditions(
            self, temperature: np.array, boundSource: np.float64,
            boundCenterX: np.float64, boundCenterY: np.float64,
            boundExternalX: np.float64, boundExternalY: np.float64) -> np.array:

        mnx: np.int64
        mny: np.int64
        temperatureAux: np.ndarray

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        he1 = self.nodeHeatSourceEnd1
        he2 = self.nodeHeatSourceEnd2
        hs1 = self.nodeHeatSourceStart1
        hs2 = self.nodeHeatSourceStart2

        temperatureAux = temperature.copy()

        # TOP SURFACE
        temperatureAux[mny - 1, 1:mnx-1] = \
            boundCenterY * temperatureAux[mny - 2, 1:mnx-1] + \
            boundExternalY * self.environmentTemperature
        # LEFT SURFACE
        temperatureAux[1:mny-1, 0] = \
            boundCenterX * temperatureAux[1:mny-1, 1] + \
            boundExternalX * self.environmentTemperature
        # RIGHT SURFACE
        temperatureAux[1:mny-1, mnx - 1] = \
            boundCenterX * temperatureAux[1:mny-1, mnx - 2] + \
            boundExternalX * self.environmentTemperature
        # BOTTOM SURFACE
        temperatureAux[0, 1:hs1] = \
            boundCenterY * temperatureAux[1, 1:hs1] + \
            boundExternalY * self.environmentTemperature

        temperatureAux[0, hs1: he1 + 1] = \
            boundSource + temperatureAux[1, hs1: he1 + 1]

        temperatureAux[0, he1 + 1: hs2] = \
            boundCenterY * temperatureAux[1, he1 + 1: hs2] + \
            boundExternalY * self.environmentTemperature

        temperatureAux[0, hs2: he2 + 1] = \
            boundSource + temperatureAux[1, hs2: he2 + 1]

        temperatureAux[0, he2 + 1:-1] = \
            boundCenterY * temperatureAux[1, he2 + 1:-1] + \
            boundExternalY * self.environmentTemperature

        return temperatureAux

    @staticmethod
    def boundariesConditionsDirichlet(
            temperatureField: np.array, solid) -> np.array:

        mnx: int
        mny: int
        temperatureFieldAux: np.array

        mnx = solid.maxNodeNumberX
        mny = solid.maxNodeNumberY
        temperatureFieldAux = temperatureField.copy()

        # BOTTOM:
        temperatureFieldAux[0, :] = solid.tempSouth
        # EAST
        temperatureFieldAux[:, mnx - 1] = solid.tempEast
        # TOP
        temperatureFieldAux[mny - 1, :] = solid.tempNorth
        # WEST
        temperatureFieldAux[:, 0] = solid.tempWest

        return temperatureFieldAux

    def setSourceConditions(
            self, temperature: np.array, boundSource: np.float64,
            boundCenterY: np.float64, boundExternalY: np.float64) -> np.array:

        mnx: np.int64
        mny: np.int64
        temperatureAux: np.ndarray

        he1 = self.nodeHeatSourceEnd1
        he2 = self.nodeHeatSourceEnd2
        hs1 = self.nodeHeatSourceStart1
        hs2 = self.nodeHeatSourceStart2

        temperatureAux = temperature.copy()

        # BOTTOM SURFACE
        temperatureAux[0, 1:hs1] = \
            boundCenterY * temperatureAux[1, 1:hs1] + \
            boundExternalY * self.environmentTemperature

        temperatureAux[0, hs1:he1+1] = \
            boundSource + temperatureAux[1, hs1:he1+1]

        temperatureAux[0, he1+1:hs2] = \
            boundCenterY * temperatureAux[1, he1+1: hs2] + \
            boundExternalY * self.environmentTemperature

        temperatureAux[0, hs2: he2+1] = \
            boundSource + temperatureAux[1, hs2: he2 + 1]

        temperatureAux[0, he2+1:-1] = \
            boundCenterY * temperatureAux[1, he2+1:-1] + \
            boundExternalY * self.environmentTemperature

        return temperatureAux

    def getEnergyBalance(
            self, temperature: np.array, conductionCoeffX: np.float64,
            conductionCoeffY: np.float64) -> np.float64:

        mnx: int
        mny: int
        energyBalance: np.float64

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY
        he1 = self.nodeHeatSourceEnd1
        he2 = self.nodeHeatSourceEnd2
        hs1 = self.nodeHeatSourceStart1
        hs2 = self.nodeHeatSourceStart2

        # TOP SURFACE
        energyBalanceTop = conductionCoeffY * (
            temperature[mny-1, 1:mnx-1] - temperature[mny-2, 1:mnx-1]).mean()

        # LEFT SURFACE
        energyBalanceLeft = conductionCoeffX * (
            temperature[1:mny-1, 0] - temperature[1:mny-1, 1]).mean()

        # RIGHT SURFACE
        energyBalanceRight = conductionCoeffX * (
            temperature[1:mny-1, mnx-1] - temperature[1:mny-1, mnx-2]).mean()

        # BOTTOM SURFACE
        energyBalanceBottom = conductionCoeffY * (
            temperature[0, 1:hs1] - temperature[1, 1:hs1]).mean()

        energyBalanceBottom += conductionCoeffY * (
                temperature[0, hs1:he1+1] - temperature[1, hs1:he1+1]).mean()

        energyBalanceBottom += conductionCoeffY * (
                temperature[0, he1+1:hs2] - temperature[1, he1+1:hs2]).mean()

        energyBalanceBottom += conductionCoeffY * (
                temperature[0, hs2:he2+1] - temperature[1, hs2:he2+1]).mean()

        energyBalanceBottom += conductionCoeffY * (
                temperature[0, he2+1:-1] - temperature[1, he2+1:-1]).mean()

        energyBalance = energyBalanceBottom + energyBalanceTop \
            + energyBalanceRight + energyBalanceLeft

        return energyBalance
