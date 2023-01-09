import numpy as np
from TimeIntegration import TimeIntegration
from PoissonEquation import PoissonEquation
from MomentumEquations import MomentumEquations


class Fluid(MomentumEquations, PoissonEquation, TimeIntegration):

    def __init__(self):

        super().__init__()

        self.pressure: np.array
        self.velocityX: np.array
        self.velocityY: np.array
        self.continuity: float
        self.poissonSolution: np.array
        self.estimatePressure: np.array
        self.estimateVelocityX: np.array
        self.estimateVelocityY: np.array

        mnx = self.maxNodeNumberX
        mny = self.maxNodeNumberY

        self.pressure = np.zeros((mny, mnx), dtype=np.float)
        self.velocityX = np.zeros((mny, mnx), dtype=np.float)
        self.velocityY = np.zeros((mny, mnx), dtype=np.float)
        self.continuity = 0.0
        self.poissonSolution = np.zeros((mny, mnx), dtype=np.float)
        self.estimatePressure = np.zeros((mny, mnx), dtype=np.float)
        self.estimateVelocityX = np.zeros((mny, mnx), dtype=np.float)
        self.estimateVelocityY = np.zeros((mny, mnx), dtype=np.float)
