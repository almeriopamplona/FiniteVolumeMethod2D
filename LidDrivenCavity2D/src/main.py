# *****************************************************************************
# *                            MAIN - LID CAVITY                              *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: controls what program will do.                               *
# *****************************************************************************

from Solver import Solver
from Fluid import Fluid
from PostProcess import PostProcess

if __name__ == '__main__':

    fluid = Fluid()
    solver = Solver()

    solver.solveCavity(fluid)

    postProcessor = PostProcess()
    # postProcessor.plotDataComparison()
    # postProcessor.makeVideo()
    # postProcessor.plotStreamlines("pressure", fileFormat="pdf")
    # postProcessor.plotStreamlines("velocityX", fileFormat="pdf")
    # postProcessor.plotStreamlines("velocityY", fileFormat="pdf")
    postProcessor.plotStreamlines("velocity", fileFormat="pdf")
