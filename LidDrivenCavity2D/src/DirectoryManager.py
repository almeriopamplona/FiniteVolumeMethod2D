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
        self.__dirPressure: str
        self.__dirVelocityX: str
        self.__dirVelocityY: str
        self.__dirReferences: str
        self.__pressureOutputPath: str
        self.__velocityXOutputPath: str
        self.__velocityYOutputPath: str
        self.__ghiaVelocityVertical: str
        self.__ghiaVelocityHorizontal: str
        self.__agarwalVelocityVertical: str
        self.__agarwalVelocityHorizontal: str
        self.__pressureOutputStreamline: str
        self.__velocityOutputStreamline: str
        self.__velocityXOutputStreamline: str
        self.__velocityYOutputStreamline: str
        

        # Instance:
        # --------------
        super().__init__()

        self.__path = self.__getPath
        self.__dirReports = self.__getDirReports
        self.__dirWarnings = self.__getDirWarnings
        self.__dirReferences = self.__getDirReferences

        self.__dirFigure = self.__getDirFigure
        self.__dirPressure = self.__getDirPressure
        self.__dirVelocityX = self.__getDirVelocityX
        self.__dirVelocityY = self.__getDirVelocityY
        self.__pressureOutputPath = self.__getPressureOutputPath
        self.__velocityXOutputPath = self.__getVelocityXOutputPath
        self.__velocityYOutputPath = self.__getVelocityYOutputPath
        self.__ghiaVelocityVertical = self.__getGhiaVelocityVerticalPath
        self.__ghiaVelocityHorizontal = self.__getGhiaVelocityHorizontalPath
        self.__agarwalVelocityVertical = self.__getAgarwalVelocityVerticalPath
        self.__agarwalVelocityHorizontal = self.__getAgarwalVelocityHorizontalPath
        self.__pressureOutputStreamline = self.__getPressureOutputStreamline
        self.__velocityOuptutStreamline = self.__getVelocityOutputStreamline
        self.__velocityXOutputStreamline = self.__getVelocityXOutputStreamline
        self.__velocityYOutputStreamline = self.__getVelocityYOutputStreamline

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
    def __getDirPressure(self) -> str:
        return self.__dirReports + ct.OS_SEP + ct.DIR_PRESSURE

    @property
    def __getDirVelocityX(self) -> str:
        return self.__dirReports + ct.OS_SEP + ct.DIR_VELOCITYX

    @property
    def __getDirVelocityY(self) -> str:
        return self.__dirReports + ct.OS_SEP + ct.DIR_VELOCITYY

    @property
    def __getDirReferences(self) -> str:
        return self.__dirReports + ct.OS_SEP + ct.DIR_REFERENCES

    @property
    def __getPressureOutputPath(self) -> str:
        return self.__dirPressure + ct.OS_SEP + ct.PRESSURE_OUTPUT + \
            "_{}x{}_Re{}.csv".format(
                self.nodeNumberY, self.nodeNumberX, self.reynoldsNumber)

    @property
    def __getVelocityXOutputPath(self) -> str:
        return self.__dirVelocityX + ct.OS_SEP + ct.VELOCITYX_OUTPUT + \
            "_{}x{}_Re{}.csv".format(
                self.nodeNumberY, self.nodeNumberX, self.reynoldsNumber)

    @property
    def __getVelocityYOutputPath(self) -> str:
        return self.__dirVelocityY + ct.OS_SEP + ct.VELOCITYY_OUTPUT + \
            "_{}x{}_Re{}.csv".format(
                self.nodeNumberY, self.nodeNumberX, self.reynoldsNumber)

    @property
    def __getPressureOutputStreamline(self) -> str:
        return self.__dirFigure + ct.OS_SEP + ct.PRESSURE_OUTPUT + \
            "_{}x{}_Re{}_stream".format(
                self.nodeNumberY, self.nodeNumberX, self.reynoldsNumber)
    
    @property
    def __getVelocityOutputStreamline(self) -> str:
        return self.__dirFigure + ct.OS_SEP + ct.VELOCITY_OUTPUT + \
            "_{}x{}_Re{}_stream".format(
                self.nodeNumberY, self.nodeNumberX, self.reynoldsNumber)
    
    @property
    def __getVelocityXOutputStreamline(self) -> str:
        return self.__dirFigure + ct.OS_SEP + ct.VELOCITYX_OUTPUT + \
            "_{}x{}_Re{}_stream".format(
                self.nodeNumberY, self.nodeNumberX, self.reynoldsNumber)

    @property
    def __getVelocityYOutputStreamline(self) -> str:
        return self.__dirFigure + ct.OS_SEP + ct.VELOCITYY_OUTPUT + \
            "_{}x{}_Re{}_stream".format(
                self.nodeNumberY, self.nodeNumberX, self.reynoldsNumber)

    @property
    def __getGhiaVelocityVerticalPath(self) -> str:
        return self.__dirReferences + ct.OS_SEP + ct.GHIA_VELOCITY_VERTICAL + \
            "Re{}_{}x{}.csv".format(
                int(self.reynoldsNumber), self.nodeNumberY, self.nodeNumberX)

    @property
    def __getGhiaVelocityHorizontalPath(self) -> str:
        return self.__dirReferences + ct.OS_SEP + ct.GHIA_VELOCITY_HORIZONTAL \
            + "Re{}_{}x{}.csv".format(
                int(self.reynoldsNumber), self.nodeNumberY, self.nodeNumberX)

    @property
    def __getAgarwalVelocityVerticalPath(self) -> str:
        return self.__dirReferences + ct.OS_SEP + ct.AGARWAL_VELOCITY_VERTICAL \
            + "Re{}_{}x{}.csv".format(
                int(self.reynoldsNumber), self.nodeNumberY, self.nodeNumberX)

    @property
    def __getAgarwalVelocityHorizontalPath(self) -> str:
        return self.__dirReferences + ct.OS_SEP + \
            ct.AGARWAL_VELOCITY_HORIZONTAL + "Re{}_{}x{}.csv".format(
                int(self.reynoldsNumber), self.nodeNumberY, self.nodeNumberX)

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
            os.makedirs(self.__dirPressure)
            os.makedirs(self.__dirVelocityX)
            os.makedirs(self.__dirVelocityY)

    def __makeWarningDirectory(self):

        if not self.__dirWarningsExists():
            os.makedirs(self.__dirWarnings)

    # ======================================================================== #
    #   PUBLIC METHODS
    # ======================================================================== #
    @property
    def getPressureOutputPath(self) -> str:
        return self.__pressureOutputPath

    @property
    def getVelocityXOutputPath(self) -> str:
        return self.__velocityXOutputPath

    @property
    def getVelocityYOutputPath(self) -> str:
        return self.__velocityYOutputPath

    @property
    def getGhiaVelocityVertPath(self) -> str:
        return self.__ghiaVelocityVertical

    @property
    def getGhiaVelocityHoritPath(self) -> str:
        return self.__ghiaVelocityHorizontal

    @property
    def getAgarwalVelocityVertPath(self) -> str:
        return self.__agarwalVelocityVertical

    @property
    def getAgarwalVelocityHoritPath(self) -> str:
        return self.__agarwalVelocityHorizontal

    @property
    def getPressureOutputStreamline(self) -> str:
        return self.__pressureOutputStreamline

    @property
    def getVelocityOutputStreamline(self) -> str:
        return self.__velocityOutputStreamline
    
    @property
    def getVelocityXOutputStreamline(self) -> str:
        return self.__velocityXOutputStreamline

    @property
    def getVelocityYOutputStreamline(self) -> str:
        return self.__velocityYOutputStreamline

    @property
    def getDirFigure(self) -> str:
        return  self.__dirFigure
