# *****************************************************************************
# *                     TIME INTEGRATION - LID CAVITY                         *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: contains time integration algorithms.                        *
# *****************************************************************************

import numpy as np
from MeshGenerator import MeshGenerator


class TimeIntegration(MeshGenerator):

    def __int__(self):

        super().__init__()

    def forwardEulerMethod(
            self, pressure: np.array, velocityX: np.array, velocityY: np.array,
            estimatePressure: np.array, estimateVelocityX: float,
            estimateVelocityY: float, coefficientPressureX: float,
            coefficientPressureY: float) -> tuple:

        mnx: int
        mny: int

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        pressure[1:mny - 1, 1:mnx - 1] = \
            estimatePressure[1:mny - 1, 1:mnx - 1] + \
            pressure[1:mny - 1, 1:mnx - 1]

        velocityX[1:mny - 1, 1:mnx - 1] = \
            estimateVelocityX[1:mny - 1, 1:mnx - 1] - coefficientPressureX * (
                estimatePressure[1:mny - 1, 2:mnx] -
                estimatePressure[1:mny - 1, 1:mnx - 1])

        velocityY[1:mny - 1, 1:mnx - 1] = \
            estimateVelocityY[1:mny - 1, 1:mnx - 1] - coefficientPressureY * (
                estimatePressure[2:mny, 1:mnx - 1] -
                estimatePressure[1:mny - 1, 1:mnx - 1])

        return velocityX, velocityY, pressure
