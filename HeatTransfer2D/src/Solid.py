import numpy as np
from EnergyEquations import EnergyEquations

class Solid(EnergyEquations):

    def __init__(self):
        super().__init__()

        self.temperature: np.array
        self.energyBalance: np.float64

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        self.temperature = \
            self.initialTemperature * np.ones((mny, mnx), dtype=np.float64)

        self.energyBalance = 0.
