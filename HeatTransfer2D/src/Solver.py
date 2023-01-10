# *****************************************************************************
# *                        SOLVER - 2D HEAT TRANSFER                          *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: some hard coded variables that are used through the code and *
# * kept here to maintain the code organized.                                 *
# *****************************************************************************
import time
import numpy as np
import pandas as pd
import Constants as ct
from Solid import Solid
from PostProcess import PostProcess


class Solver(PostProcess):

    def __init__(self):

        super().__init__()

    def solve2DDirichletProblem(self, solid: Solid) -> None:

        probe1: np.array
        probe2: np.array
        probe3: np.array
        timeVector: np.array
        diffusionCoeffX: np.float64
        diffusionCoeffY: np.float64

        start = time.time()

        # Energy Equations' constants:
        # ---------------------------
        diffusionCoeffX = \
            solid.diffusivity * solid.deltaT * solid.invDeltaX ** 2
        diffusionCoeffY = \
            solid.diffusivity * solid.deltaT * solid.invDeltaY ** 2

        coefficientCenter = 1 + 2 * solid.diffusivity * solid.deltaT * (
            solid.deltaX ** 2 + solid.deltaY ** 2) * solid.invDeltaX ** 2 * \
            solid.invDeltaY ** 2

        conductionCoeffX = solid.conductivity * solid.invDeltaX
        conductionCoeffY = solid.conductivity * solid.invDeltaY

        # ------------------------------------------------------------------- #
        # INITIAL AND BOUNDARY CONDITIONS                                     #
        # ------------------------------------------------------------------- #
        solid.temperature = solid.boundariesConditionsDirichlet(
            solid.temperature, solid)

        # ------------------------------------------------------------------- #
        # START PROBES                                                        #
        # ------------------------------------------------------------------- #
        probe1 = np.zeros((solid.timeSize,), dtype=np.float64)
        probe2 = np.zeros((solid.timeSize,), dtype=np.float64)
        probe3 = np.zeros((solid.timeSize,), dtype=np.float64)

        timeVector = solid.getTimeVector()

        positionsProbe1 = solid.getProbePosition(0.01, 0.000)
        positionsProbe2 = solid.getProbePosition(0.01, 0.005)
        positionsProbe3 = solid.getProbePosition(0.01, 0.010)

        # ------------------------------------------------------------------- #
        # SOLVE DE HEAT TRANSFER PROBLEMS                                     #
        # ------------------------------------------------------------------- #

        if self.solutionMethod == ct.EXPLICIT:

            for t in range(solid.timeSize):

                solid.temperature = solid.solveEnergyEquationsExplicit(
                    solid.temperature, diffusionCoeffX, diffusionCoeffY)

                solid.temperature = solid.boundariesConditionsDirichlet(
                    solid.temperature, solid)

                probe1[t] = solid.temperature[
                            positionsProbe1[2]:positionsProbe1[3] + 1,
                            positionsProbe1[0]:positionsProbe1[1] + 1].mean()
                probe2[t] = solid.temperature[
                            positionsProbe2[2]:positionsProbe2[3] + 1,
                            positionsProbe2[0]:positionsProbe2[1] + 1].mean()
                probe3[t] = solid.temperature[
                            positionsProbe3[2]:positionsProbe3[3] + 1,
                            positionsProbe3[0]:positionsProbe3[1] + 1].mean()

                solid.energyBalance = solid.getEnergyBalance(
                    solid.temperature, conductionCoeffX, conductionCoeffY)

        elif self.solutionMethod == ct.IMPLICIT:

            for t in range(solid.timeSize):
                solid.temperature = solid.solveEnergyEquationsImplicitDirichlet(
                    solid, coefficientCenter, diffusionCoeffX,
                    diffusionCoeffY)

                solid.temperature = solid.boundariesConditionsDirichlet(
                    solid.temperature, solid)

                probe1[t] = solid.temperature[
                            positionsProbe1[2]:positionsProbe1[3] + 1,
                            positionsProbe1[0]:positionsProbe1[1] + 1].mean()
                probe2[t] = solid.temperature[
                            positionsProbe2[2]:positionsProbe2[3] + 1,
                            positionsProbe2[0]:positionsProbe2[1] + 1].mean()
                probe3[t] = solid.temperature[
                            positionsProbe3[2]:positionsProbe3[3] + 1,
                            positionsProbe3[0]:positionsProbe3[1] + 1].mean()

                solid.energyBalance = solid.getEnergyBalance(
                    solid.temperature, conductionCoeffX, conductionCoeffY)

        else:
            print("ERROR:: Choose the right type of method!")
            exit()

        mnx = solid.maxNodeNumberX
        mny = solid.maxNodeNumberY

        outputTemperature = pd.DataFrame(data={
            "x": solid.coordinateX,
            "y": solid.coordinateY,
            "temperature": solid.temperature[1:mny - 1, 1:mnx - 1].reshape(
                solid.coordinateX.shape)})

        outputProbe1 = pd.DataFrame(data={"t": timeVector, "probe": probe1})
        outputProbe2 = pd.DataFrame(data={"t": timeVector, "probe": probe2})
        outputProbe3 = pd.DataFrame(data={"t": timeVector, "probe": probe3})

        self.saveOutputs(outputTemperature, self.getTemperatureOutputPath)
        self.saveOutputs(outputProbe1, self.getProbe1OutputPath)
        self.saveOutputs(outputProbe2, self.getProbe2OutputPath)
        self.saveOutputs(outputProbe3, self.getProbe3OutputPath)

        end = time.time()

        print("Elapsed time: {}".format(end - start))

    def solve2DRobinProblem(self, solid: Solid) -> None:

        probe1: np.array
        probe2: np.array
        probe3: np.array
        timeVector: np.array
        boundSource: np.float64
        boundCenterX: np.float64
        boundCenterY: np.float64
        boundExternalX: np.float64
        boundExternalY: np.float64
        diffusionCoeffX: np.float64
        diffusionCoeffY: np.float64
        coefficientCenter: np.float64
        conductionCoeffX: np.float64
        conductionCoeffY: np.float64

        start = time.time()

        # ------------------------------------------------------------------- #
        # Numerical constants                                                 #
        # ------------------------------------------------------------------- #

        # Boundaries' constants:
        # ---------------------
        boundSource = solid.heatSource * solid.deltaY / solid.conductivity
        boundCenterX = \
            (2 * solid.conductivity - solid.convection * solid.deltaX) / \
            (2 * solid.conductivity + solid.convection * solid.deltaX)
        boundCenterY = \
            (2 * solid.conductivity - solid.convection * solid.deltaY) / \
            (2 * solid.conductivity + solid.convection * solid.deltaY)
        boundExternalX = 2 * solid.conductivity * solid.deltaX / \
            (2 * solid.conductivity + solid.convection * solid.deltaX)
        boundExternalY = 2 * solid.conductivity * solid.deltaY / \
            (2 * solid.conductivity + solid.convection * solid.deltaY)

        # Energy Equations' constants:
        # ---------------------------
        diffusionCoeffX = solid.diffusivity * solid.deltaT * solid.invDeltaX**2
        diffusionCoeffY = solid.diffusivity * solid.deltaT * solid.invDeltaY**2

        coefficientCenter = 1 + 2 * solid.diffusivity * solid.deltaT * (
            solid.deltaX**2 + solid.deltaY**2) * solid.invDeltaX**2 * \
            solid.invDeltaY**2

        conductionCoeffX = solid.conductivity * solid.invDeltaX
        conductionCoeffY = solid.conductivity * solid.invDeltaY

        # ------------------------------------------------------------------- #
        # INITIAL AND BOUNDARY CONDITIONS                                     #
        # ------------------------------------------------------------------- #
        solid.temperature = solid.setSourceConditions(
            solid.temperature, boundSource, boundCenterY, boundExternalY)

        # ------------------------------------------------------------------- #
        # START PROBES                                                        #
        # ------------------------------------------------------------------- #
        probe1 = np.zeros((solid.timeSize,), dtype=np.float64)
        probe2 = np.zeros((solid.timeSize,), dtype=np.float64)
        probe3 = np.zeros((solid.timeSize,), dtype=np.float64)

        timeVector = solid.getTimeVector()

        positionsProbe1 = solid.getProbePosition(0.01, 0.000)
        positionsProbe2 = solid.getProbePosition(0.01, 0.005)
        positionsProbe3 = solid.getProbePosition(0.01, 0.010)

        # ------------------------------------------------------------------- #
        # SOLVE DE HEAT TRANSFER PROBLEMS                                     #
        # ------------------------------------------------------------------- #

        if self.solutionMethod == ct.EXPLICIT:

            for t in range(solid.timeSize):

                solid.temperature = solid.solveEnergyEquationsExplicit(
                    solid.temperature, diffusionCoeffX, diffusionCoeffY)

                solid.temperature = solid.boundariesConditions(
                    solid.temperature, boundSource, boundCenterX, boundCenterY,
                    boundExternalX, boundExternalY)

                probe1[t] = solid.temperature[
                    positionsProbe1[2]:positionsProbe1[3] + 1,
                    positionsProbe1[0]:positionsProbe1[1] + 1].mean()
                probe2[t] = solid.temperature[
                    positionsProbe2[2]:positionsProbe2[3] + 1,
                    positionsProbe2[0]:positionsProbe2[1] + 1].mean()
                probe3[t] = solid.temperature[
                    positionsProbe3[2]:positionsProbe3[3] + 1,
                    positionsProbe3[0]:positionsProbe3[1] + 1].mean()

                solid.energyBalance = solid.getEnergyBalance(
                    solid.temperature, conductionCoeffX, conductionCoeffY)

                # if solid.energyBalance > solid.heatBalanceTolerance:
                #     print(print("ERROR:: energy balance did not conserved! " +
                #           "continuity = {}".format(solid.energyBalance)))
                #     exit()

        elif self.solutionMethod == ct.IMPLICIT:

            for t in range(solid.timeSize):
                solid.temperature = solid.solveEnergyEquationsImplicitRobin(
                    solid, coefficientCenter, diffusionCoeffX,
                    diffusionCoeffY, boundSource, boundCenterX, boundCenterY,
                    boundExternalX, boundExternalY)

                solid.temperature = solid.boundariesConditions(
                    solid.temperature, boundSource, boundCenterX, boundCenterY,
                    boundExternalX, boundExternalY)

                probe1[t] = solid.temperature[
                    positionsProbe1[2]:positionsProbe1[3] + 1,
                    positionsProbe1[0]:positionsProbe1[1] + 1].mean()
                probe2[t] = solid.temperature[
                    positionsProbe2[2]:positionsProbe2[3] + 1,
                    positionsProbe2[0]:positionsProbe2[1] + 1].mean()
                probe3[t] = solid.temperature[
                    positionsProbe3[2]:positionsProbe3[3] + 1,
                    positionsProbe3[0]:positionsProbe3[1] + 1].mean()

                solid.energyBalance = solid.getEnergyBalance(
                    solid.temperature, conductionCoeffX, conductionCoeffY)

                # if solid.energyBalance > solid.heatBalanceTolerance:
                #     print(print("ERROR:: energy balance did not conserved! " +
                #           "continuity = {}".format(solid.energyBalance)))
                #     exit()
        else:
            print("ERROR:: Choose the right type of method!")
            exit()

        mnx = solid.maxNodeNumberX
        mny = solid.maxNodeNumberY

        outputTemperature = pd.DataFrame(
            data={
                "x": solid.coordinateX,
                "y": solid.coordinateY,
                "temperature": solid.temperature[1:mny - 1, 1:mnx - 1].reshape(
                    solid.coordinateX.shape)})

        outputProbe1 = pd.DataFrame(data={"t": timeVector, "probe": probe1})
        outputProbe2 = pd.DataFrame(data={"t": timeVector, "probe": probe2})
        outputProbe3 = pd.DataFrame(data={"t": timeVector, "probe": probe3})

        self.saveOutputs(outputTemperature, self.getTemperatureOutputPath)
        self.saveOutputs(outputProbe1, self.getProbe1OutputPath)
        self.saveOutputs(outputProbe2, self.getProbe2OutputPath)
        self.saveOutputs(outputProbe3, self.getProbe3OutputPath)

        end = time.time()

        print("Elapsed time: {}".format(end - start))
