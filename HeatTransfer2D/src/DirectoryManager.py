# *****************************************************************************
# *                  DIRECTORY MANAGER  - 2D HEAT TRANSFER                    *
# *****************************************************************************
# * Author: Almerio Jose Venancio Pains Soares Pamplona                       *
# * E-mail: almeriopamplona@gmail.com                                         *
# *****************************************************************************
# * Description: class responsible for creating directories, file paths and   *
# * keep important paths.                                                     *
# *****************************************************************************
import os
import Constants as ct
from ControlParameters import ControlParameters


class DirectoryManager(ControlParameters):

    def __init__(self):

        # Declarations:
        # ----------
        self.__path: str
        self.__dirReports: str
        self.__createdLog: bool
        self.__dirWarnings: str
        self.__dirFigure: str
        self.__dirTemperature: str
        self.__temperatureOutputPath: str
        self.__analyticalSolutionPath: str
        self.__temperatureOutputStreamline: str

        self.__probe1Output: str
        self.__probe2Output: str
        self.__probe3Output: str
        self.__probePlotsPath: str

        # Instance:
        # --------------
        super().__init__()

        self.__path = self.__getPath
        self.__dirReports = self.__getDirReports
        self.__dirWarnings = self.__getDirWarnings

        self.__dirFigure = self.__getDirFigure
        self.__dirTemperature = self.__getDirTemperature
        self.__temperatureOutputPath = self.__getTemperatureOutputPath
        self.__analyticalSolutionPath = self.__getAnalayticalPath
        self.__temperatureOutputStreamline = \
            self.__getTemperatureOutputStreamline

        self.__probe1Output = self.__getProbe1OutputPath
        self.__probe2Output = self.__getProbe2OutputPath
        self.__probe3Output = self.__getProbe3OutputPath
        self.__probePlotsPath = self.__getProbePlotsPath

        self.__makeDirectories()

    # ======================================================================== #
    # PRIVATE METHODS                                                          #
    # ======================================================================== #

    # ------------------------------------------------------------------------ #
    # CONDITIONALS                                                             #
    # ------------------------------------------------------------------------ #
    def __dirReportExists(self) -> bool:
        return os.path.exists(self.__dirReports)

    def __dirWarningsExists(self) -> bool:
        return os.path.exists(self.__dirWarnings)

    # ------------------------------------------------------------------------ #
    # PRIVATE INTERNAL GETTERS                                                 #
    # ------------------------------------------------------------------------ #
    @property
    def __getPath(self) -> str:
        return ct.PATH

    @property
    def __getDirReports(self) -> str:
        return self.__path + ct.OS_SEP + ct.DIR_REPORTS

    @property
    def __getDirWarnings(self) -> str:
        return self.__path + ct.OS_SEP + ct.DIR_WARNINGS

    @property
    def __getDirFigure(self) -> str:
        return self.__dirReports + ct.OS_SEP + ct.DIR_FIGURE

    @property
    def __getDirTemperature(self) -> str:
        return self.__dirReports + ct.OS_SEP + ct.DIR_TEMPERATURE

    @property
    def __getTemperatureOutputPath(self) -> str:
        return self.__dirTemperature + ct.OS_SEP + ct.TEMPERATURE_OUTPUT + \
            "_{}_{}_{}x{}.csv".format(
                self.problemType, self.solutionMethod,self.nodeNumberY,
                self.nodeNumberX)

    @property
    def __getProbe1OutputPath(self) -> str:
        return self.__dirTemperature + ct.OS_SEP + ct.PROBE1_OUTPUT + \
            "_{}_{}_{}x{}.csv".format(
                self.problemType, self.solutionMethod,self.nodeNumberY,
                self.nodeNumberX)

    @property
    def __getProbe2OutputPath(self) -> str:
        return self.__dirTemperature + ct.OS_SEP + ct.PROBE2_OUTPUT + \
            "_{}_{}_{}x{}.csv".format(
                self.problemType, self.solutionMethod,self.nodeNumberY,
                self.nodeNumberX)

    @property
    def __getProbe3OutputPath(self) -> str:
        return self.__dirTemperature + ct.OS_SEP + ct.PROBE3_OUTPUT + \
            "_{}_{}_{}x{}.csv".format(
                self.problemType, self.solutionMethod,self.nodeNumberY,
                self.nodeNumberX)

    @property
    def __getTemperatureOutputStreamline(self) -> str:
        return self.__dirFigure + ct.OS_SEP + ct.TEMPERATURE_OUTPUT + \
            "_{}_{}_{}x{}".format(
                self.problemType, self.solutionMethod,self.nodeNumberY,
                self.nodeNumberX)

    @property
    def __getProbePlotsPath(self) -> str:
        return self.__dirFigure + ct.OS_SEP + ct.PROBE_PLOTS + \
            "_{}_{}_{}x{}".format(
                self.problemType, self.solutionMethod,self.nodeNumberY,
                self.nodeNumberX)

    @property
    def __getAnalayticalPath(self) -> str:
        return self.__dirTemperature + ct.OS_SEP + ct.ANALYTICAL_TEMP_OUTPUT + \
            "_{}x{}.csv".format(self.nodeNumberY, self.nodeNumberX)

    # ------------------------------------------------------------------------ #
    # MAKING DIRECTORIES                                                       #
    # ------------------------------------------------------------------------ #
    def __makeDirectories(self):
        self.__makeReportDirectory()
        self.__makeWarningDirectory()

    def __makeReportDirectory(self):

        if not self.__dirReportExists():
            os.makedirs(self.__dirReports)
            os.makedirs(self.__dirFigure)
            os.makedirs(self.__dirTemperature)

    def __makeWarningDirectory(self):

        if not self.__dirWarningsExists():
            os.makedirs(self.__dirWarnings)

    # ======================================================================== #
    #   PUBLIC METHODS
    # ======================================================================== #
    @property
    def getTemperatureOutputPath(self) -> str:
        return self.__temperatureOutputPath

    @property
    def getAnalyticalSolutionPath(self) -> str:
        return self.__analyticalSolutionPath

    @property
    def getTemperatureOutputStreamline(self) -> str:
        return self.__temperatureOutputStreamline

    @property
    def getProbe1OutputPath(self) -> str:
        return self.__probe1Output

    @property
    def getProbe2OutputPath(self) -> str:
        return self.__probe2Output

    @property
    def getProbe3OutputPath(self) -> str:
        return self.__probe3Output

    @property
    def getProbesPlotPath(self) -> str:
        return self.__probePlotsPath

    @property
    def getDirFigure(self) -> str:
        return  self.__dirFigure