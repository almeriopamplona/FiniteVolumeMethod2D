from Solid import Solid
from Solver import Solver
from AnalyticalSolver import AnalyticalSolver
from PostProcess import PostProcess

if __name__ == '__main__':

    # solid = Solid()
    # solver = Solver()
    # analyticalSolver = AnalyticalSolver()
    postProcessor = PostProcess()

    # analyticalSolver.solveDirichletPlate(solid)
    # solver.solve2DDirichletProblem(solid)
    # solver.solve2DRobinProblem(solid)

    postProcessor.plotTemperatureDistribution()
    # postProcessor.plotProbesEvolution()
    # postProcessor.plotDataComparison()
    # postProcessor.plotProfiles()
