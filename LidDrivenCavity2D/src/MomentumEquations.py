# *****************************************************************************
# *                     MOMENTUM EQUATIONS - LID CAVITY                       *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: contains the discrete form of the Navier-Stokes equations    * 
# * and the velocity field treatment on the boundaries.                       *
# *****************************************************************************
import numpy as np
from MeshGenerator import MeshGenerator


class MomentumEquations(MeshGenerator):

    def __init__(self):
        super().__init__()

    def boundaryConditionVelocityX(self, velocityX: np.array) -> np.array:
        mnx: int
        mny: int
        velocityTempX: np.array

        mnx = self.maxNodeNumberX - 1
        mny = self.maxNodeNumberY - 1
        velocityTempX = velocityX.copy()

        # TOP
        velocityTempX[mny, :] = \
            2 * self.velocityTopX - velocityTempX[mny - 1, :]
        # BOTTOM
        velocityTempX[0, :] = - velocityTempX[1, :]
        # LEFT WALL
        velocityTempX[:, 0] = self.velocityLeftX
        # RIGHT WALL
        velocityTempX[:, mnx - 1] = self.velocityRightX

        return velocityTempX

    def boundaryConditionEstVelocityX(
            self, estimateVelocityX: np.array) -> np.array:
        mnx: int
        velocityTempX: np.array

        mnx = self.maxNodeNumberX - 1
        velocityTempX = estimateVelocityX.copy()

        # LEFT WALL
        velocityTempX[:, 0] = self.velocityLeftX
        # RIGHT WALL
        velocityTempX[:, mnx - 1] = self.velocityRightX

        return velocityTempX

    def boundaryConditionVelocityY(self, velocityY: np.array) -> np.array:
        mnx: int
        mny: int
        velocityTempX: np.array

        mnx = self.maxNodeNumberX - 1
        mny = self.maxNodeNumberY - 1
        velocityTempY = velocityY.copy()

        # LEFT WALL
        velocityTempY[:, 0] = - velocityY[:, 1]
        # RIGHT WALL
        velocityTempY[:, mnx] = - velocityY[:, mnx - 1]
        # TOP WALL
        velocityTempY[mny - 1, :] = self.velocityTopY
        # BOTTOM WALL
        velocityTempY[0, :] = self.velocityBottomY

        return velocityTempY

    def boundaryConditionEstVelocityY(
            self, estimateVelocityY: np.array) -> np.array:
        mny: int
        velocityTempX: np.array

        mny = self.maxNodeNumberY
        velocityTempY = estimateVelocityY.copy()

        # TOP WALL
        velocityTempY[mny - 1, :] = self.velocityTopY
        # BOTTOM WALL
        velocityTempY[0, :] = self.velocityBottomY

        return velocityTempY

    def solveMomentumAxisX(
            self, pressure: np.array, velocityX: np.array, velocityY: np.array,
            estimateVelocityX: np.array, coefficientPressureX: float,
            coefficientDiffusionX: float, coefficientDiffusionY: float,
            coefficientConvectionX: float, coefficientConvectionY: float) -> \
            np.array:
        mnx: int
        mny: int
        velocityTempX: np.array

        diffusionX: np.array
        diffusionY: np.array
        convectionX: np.array
        convectionY: np.array
        pressureGradient: np.array
        velocitySurfaceEastX: np.array
        velocitySurfaceWestX: np.array
        velocitySurfaceNorthX: np.array
        velocitySurfaceSouthX: np.array
        velocitySurfaceNorthY: np.array
        velocitySurfaceSouthY: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY
        velocityTempX = estimateVelocityX.copy()

        pressureGradient = coefficientPressureX * (
                pressure[1:mny - 1, 2:mnx] - pressure[1:mny - 1, 1:mnx - 1])

        velocitySurfaceEastX = \
            velocityX[1:mny - 1, 2:mnx] + \
            velocityX[1:mny - 1, 1:mnx - 1]
        velocitySurfaceWestX = \
            velocityX[1:mny - 1, 0:mnx - 2] + \
            velocityX[1:mny - 1, 1:mnx - 1]
        velocitySurfaceNorthX = \
            velocityX[2:mny, 1:mnx - 1] + \
            velocityX[1:mny - 1, 1:mnx - 1]
        velocitySurfaceSouthX = \
            velocityX[0:mny - 2, 1:mnx - 1] + \
            velocityX[1:mny - 1, 1:mnx - 1]

        velocitySurfaceNorthY = \
            velocityY[1:mny - 1, 2:mnx] + \
            velocityY[1:mny - 1, 1:mnx - 1]
        velocitySurfaceSouthY = \
            velocityY[0:mny - 2, 2:mnx] + \
            velocityY[0:mny - 2, 1:mnx - 1]

        convectionX = coefficientConvectionX * (
                velocitySurfaceEastX * velocitySurfaceEastX -
                velocitySurfaceWestX * velocitySurfaceWestX)

        convectionY = coefficientConvectionY * (
                velocitySurfaceNorthX * velocitySurfaceNorthY -
                velocitySurfaceSouthX * velocitySurfaceSouthY)

        diffusionX = coefficientDiffusionX * (
                velocityX[1:mny - 1, 2:mnx] - 2 *
                velocityX[1:mny - 1, 1:mnx - 1] +
                velocityX[1:mny - 1, 0:mnx - 2])

        diffusionY = coefficientDiffusionY * (
                velocityX[2:mny, 1:mnx - 1] - 2 *
                velocityX[1:mny - 1, 1:mnx - 1] +
                velocityX[0: mny - 2, 1:mnx - 1])

        velocityTempX[1:mny - 1, 1:mnx - 1] = \
            velocityX[1:mny - 1, 1:mnx - 1] - pressureGradient - \
            convectionX - convectionY + diffusionX + diffusionY

        return velocityTempX

    def solveMomentumAxisY(
            self, pressure: np.array, velocityX: np.array, velocityY: np.array,
            estimateVelocityY: np.array, coefficientPressureY: float,
            coefficientDiffusionX: float, coefficientDiffusionY: float,
            coefficientConvectionX: float, coefficientConvectionY: float) -> \
            np.array:
        mnx: int
        mny: int
        velocityTempX: np.array

        diffusionX: np.array
        diffusionY: np.array
        convectionX: np.array
        convectionY: np.array
        pressureGradient: np.array
        velocitySurfaceEastX: np.array
        velocitySurfaceWestX: np.array
        velocitySurfaceEastY: np.array
        velocitySurfaceWestY: np.array
        velocitySurfaceNorthY: np.array
        velocitySurfaceSouthY: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY
        velocityTempY = estimateVelocityY.copy()

        pressureGradient = coefficientPressureY * (
                pressure[2:mny, 1:mnx - 1] - pressure[1:mny - 1, 1: mnx - 1])

        velocitySurfaceEastY = \
            velocityY[1:mnx - 1, 2:mnx] + \
            velocityY[1:mny - 1, 1:mnx - 1]
        velocitySurfaceWestY = \
            velocityY[1:mny - 1, 0:mnx - 2] + \
            velocityY[1:mny - 1, 1:mnx - 1]
        velocitySurfaceNorthY = \
            velocityY[2:mny, 1:mnx - 1] + \
            velocityY[1:mny - 1, 1:mnx - 1]
        velocitySurfaceSouthY = \
            velocityY[0:mny - 2, 1:mnx - 1] + \
            velocityY[1:mny - 1, 1:mnx - 1]

        velocitySurfaceEastX = \
            velocityX[2:mny, 1:mnx - 1] + velocityX[1:mny - 1, 1:mnx - 1]
        velocitySurfaceWestX = \
            velocityX[2:mny, 0:mnx - 2] + velocityX[1:mny - 1, 0:mnx - 2]

        convectionX = coefficientConvectionX * (
                velocitySurfaceEastY * velocitySurfaceEastX -
                velocitySurfaceWestY * velocitySurfaceWestX)

        convectionY = coefficientConvectionY * (
                velocitySurfaceNorthY * velocitySurfaceNorthY -
                velocitySurfaceSouthY * velocitySurfaceSouthY)

        diffusionX = coefficientDiffusionX * (
                velocityY[1:mny - 1, 2:mnx] - 2 *
                velocityY[1:mny - 1, 1:mnx - 1] +
                velocityY[1:mny - 1, 0:mnx - 2])

        diffusionY = coefficientDiffusionY * (
                velocityY[2:mny, 1:mnx - 1] - 2 *
                velocityY[1:mny - 1, 1:mnx - 1] +
                velocityY[0:mny - 2, 1:mnx - 1])

        velocityTempY[1:mny - 1, 1:mnx - 1] = \
            velocityY[1:mny - 1, 1:mnx - 1] - pressureGradient - \
            convectionX - convectionY + diffusionX + diffusionY

        return velocityTempY

    def getCollocatedVelocities(
            self, velocityX: np.array, velocityY: np.array) -> tuple:
        mnx: int
        mny: int
        collocatedVelocityX: np.array
        collocatedVelocityY: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        collocatedVelocityX = np.zeros((mny, mny), dtype=np.float)
        collocatedVelocityY = np.zeros((mny, mny), dtype=np.float)

        collocatedVelocityX[:, 1:mnx - 1] = \
            .5 * (velocityX[:, 1:mnx - 1] + velocityX[:, 0:mnx - 2])

        collocatedVelocityY[1:mny - 1, :] = \
            .5 * (velocityY[1:mny - 1, :] + velocityY[0:mny - 2, :])

        collocatedVelocityX = \
            self.boundaryConditionVelocityX(collocatedVelocityX)

        collocatedVelocityY = \
            self.boundaryConditionVelocityY(collocatedVelocityY)

        return collocatedVelocityX, collocatedVelocityY
