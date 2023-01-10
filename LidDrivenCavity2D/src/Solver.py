# *****************************************************************************
# *                           SOLVER - LID CAVITY                             *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: contains the main algorithm to solve the lid-driven cavity   *
# * problem.                                                                  *
# *****************************************************************************

import time
import pandas as pd
from Fluid import Fluid
from PostProcess import PostProcess


class Solver(PostProcess):

    def __init__(self):

        super().__init__()

    def solveCavity(self, fluid: Fluid):

        coefficientPressureX = self.deltaT * self.invDeltaY
        coefficientPressureY = self.deltaT * self.invDeltaY
        coefficientDiffusionX = \
            self.deltaT / (self.reynoldsNumber * self.deltaX ** 2)
        coefficientDiffusionY = \
            self.deltaT / (self.reynoldsNumber * self.deltaY ** 2)
        coefficientConvectionX = 0.25 * self.deltaT * self.invDeltaX
        coefficientConvectionY = 0.25 * self.deltaT * self.invDeltaY

        # Constants of the pressure coupling equation

        coefficientEast = self.deltaT * self.invDeltaX ** 2
        coefficientWest = self.deltaT * self.invDeltaX ** 2
        coefficientNorth = self.deltaT * self.invDeltaY ** 2
        coefficientSouth = self.deltaT * self.invDeltaY ** 2
        coefficientCenter = (-2.0 * self.deltaT *
                             (self.deltaX ** 2 + self.deltaY ** 2) /
                             (self.deltaX ** 2 * self.deltaY ** 2))

        fluid.velocityX = fluid.boundaryConditionVelocityX(fluid.velocityX)

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY
        
        #
        # Dataframe structures to save velocities at each time step. The goal
        # is to track each state and then make a video.
        #
        # outputPressure = pd.DataFrame(
        #     data={
        #         "x": fluid.coordinateX, "y": fluid.coordinateY,
        #         "t0": fluid.pressure[1:mny - 1, 1:mnx - 1].reshape(
        #             fluid.coordinateX.shape)})
        #
        # outputVelocityX = pd.DataFrame(
        #     data={
        #         "x": fluid.coordinateX, "y": fluid.coordinateY,
        #         "t0": fluid.velocityX[1:mny - 1, 1:mnx - 1].reshape(
        #             fluid.coordinateX.shape)})
        #
        # outputVelocityY = pd.DataFrame(
        #     data={
        #         "x": fluid.coordinateX, "y": fluid.coordinateY,
        #         "t0": fluid.velocityY[1:mny - 1, 1:mnx - 1].reshape(
        #             fluid.coordinateX.shape)})
        
        pressureDf = self.readOutput(self.getPressureOutputPath)
        velocityXDf = self.readOutput(self.getVelocityXOutputPath)
        velocityYDf = self.readOutput(self.getVelocityYOutputPath)

        fluid.pressure[1:mny - 1, 1:mnx - 1] = \
            pressureDf["pressure"].to_numpy().reshape((mny-2, mnx-2))
        fluid.velocityX[1:mny - 1, 1:mnx - 1] = \
            velocityXDf["velocityStaggered"].to_numpy().reshape((mny-2, mnx-2))
        fluid.velocityY[1:mny - 1, 1:mnx - 1] = velocityYDf[
            "velocityStaggered"].to_numpy().reshape((mny - 2, mnx - 2))

        initial = time.time()
        for t in range(self.timeSize):

            fluid.estimateVelocityX = fluid.solveMomentumAxisX(
                fluid.pressure, fluid.velocityX, fluid.velocityY,
                fluid.estimateVelocityX, coefficientPressureX,
                coefficientDiffusionX, coefficientDiffusionY,
                coefficientConvectionX, coefficientConvectionY)

            fluid.estimateVelocityY = fluid.solveMomentumAxisY(
                fluid.pressure, fluid.velocityX, fluid.velocityY,
                fluid.estimateVelocityY, coefficientPressureY,
                coefficientDiffusionX, coefficientDiffusionY,
                coefficientConvectionX, coefficientConvectionY)

            fluid.estimateVelocityX = \
                fluid.boundaryConditionEstVelocityX(fluid.estimateVelocityX)

            fluid.estimateVelocityY = \
                fluid.boundaryConditionEstVelocityY(fluid.estimateVelocityY)

            fluid.poissonSolution = fluid.getPoissonSolution(
                fluid.estimateVelocityX, fluid.estimateVelocityY)

            fluid.estimatePressure = fluid.solvePoissonEquation(
                fluid.poissonSolution, coefficientCenter, coefficientEast,
                coefficientWest, coefficientNorth, coefficientSouth)

            fluid.velocityX, fluid.velocityY, fluid.pressure = \
                fluid.forwardEulerMethod(
                    fluid.pressure, fluid.velocityX, fluid.velocityY,
                    fluid.estimatePressure, fluid.estimateVelocityX,
                    fluid.estimateVelocityY, coefficientPressureX,
                    coefficientPressureY)

            fluid.velocityX = \
                fluid.boundaryConditionVelocityX(fluid.velocityX)

            fluid.velocityY = \
                fluid.boundaryConditionVelocityY(fluid.velocityY)

            fluid.pressure = \
                fluid.boundaryConditionsPressure(fluid.pressure)

            fluid.continuity = fluid.getMassConservation(
                fluid.velocityX, fluid.velocityY)

            if fluid.continuity > self.toleranceMass:
                print("ERROR:: Mass balance did not conserved! " +
                      "continuity = {}".format(fluid.continuity))
                exit()

            #
            # tracking things, if you want to make a video 
            #
            # outputPressure["t{}".format(t+1)] = \
            #     fluid.pressure[1:mny - 1, 1:mnx - 1].reshape(
            #         fluid.coordinateX.shape)
            #
            # velocityX, velocityY = fluid.getCollocatedVelocities(
            #     fluid.velocityX, fluid.velocityY)
            #
            # outputVelocityX["t{}".format(t+1)] = \
            #     velocityX[1:mny - 1, 1:mnx - 1].reshape(
            #         fluid.coordinateX.shape)
            # outputVelocityY["t{}".format(t+1)] = \
            #     velocityY[1:mny - 1, 1:mnx - 1].reshape(
            #         fluid.coordinateX.shape)

        velocityX, velocityY = \
            fluid.getCollocatedVelocities(fluid.velocityX, fluid.velocityY)

        outputPressure = pd.DataFrame(data={
            "x": fluid.coordinateX,
            "y": fluid.coordinateY,
            "pressure": fluid.pressure[1:mny - 1, 1:mnx - 1].reshape(
                fluid.coordinateX.shape)
        })

        outputVelocityX = pd.DataFrame(data={
            "x": fluid.coordinateX,
            "y": fluid.coordinateY,
            "velocityX": velocityX[1:mny - 1, 1:mnx - 1].reshape(
                fluid.coordinateX.shape),
            "velocityStaggered": fluid.velocityX[1:mny - 1, 1:mnx - 1].reshape(
                fluid.coordinateX.shape)
        })

        outputVelocityY = pd.DataFrame(data={
            "x": fluid.coordinateX,
            "y": fluid.coordinateY,
            "velocityY": velocityY[1:mny - 1, 1:mnx - 1].reshape(
                fluid.coordinateX.shape),
            "velocityStaggered": fluid.velocityY[1:mny - 1, 1:mnx - 1].reshape(
                fluid.coordinateX.shape)
        })

        self.saveOutputs(outputPressure, self.getPressureOutputPath)
        self.saveOutputs(outputVelocityX, self.getVelocityXOutputPath)
        self.saveOutputs(outputVelocityY, self.getVelocityYOutputPath)

        final = time.time()
        print("Elapsed time: {}".format(final - initial))
