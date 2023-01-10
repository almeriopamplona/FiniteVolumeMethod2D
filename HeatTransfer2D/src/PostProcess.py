import numpy as np
import pandas as pd
import Constants as ct
from matplotlib import pyplot, cm
from MeshGenerator import MeshGenerator
from DirectoryManager import DirectoryManager


class PostProcess(DirectoryManager, MeshGenerator):

    def __init__(self):
        super().__init__()

    @staticmethod
    def saveOutputs(dataframe: pd.DataFrame, filename: str) -> None:
        dataframe.to_csv(
            filename, sep=ct.FILE_SEP, header=True, index=False,
            decimal=ct.DECIMAL_SEP, encoding='utf-8')

    @staticmethod
    def readOutput(filename: str) -> pd.DataFrame:
        dataframe: pd.DataFrame

        dataframe = pd.read_csv(
            filename, sep=ct.FILE_SEP, decimal=ct.DECIMAL_SEP)

        return dataframe

    def plotTemperatureDistribution(
            self, fileFormat: str = 'jpg', fileDpi: int = 1000) -> None:

        filename: str

        temperatureDf: pd.DataFrame

        axisX: np.ndarray
        axisY: np.ndarray
        temperature: np.ndarray
        coordinatesX: np.ndarray
        coordinatesY: np.ndarray

        temperatureDf = self.readOutput(self.getTemperatureOutputPath)
        # temperatureDf = self.readOutput(self.getAnalyticalSolutionPath)

        nx = self.nodeNumberX
        ny = self.nodeNumberY
        axisX = np.linspace(self.initialPositionX, self.finalPositionX, nx)
        axisY = np.linspace(self.initialPositionY, self.finalPositionY, ny)
        coordinatesX, coordinatesY = np.meshgrid(axisX, axisY)

        temperature = temperatureDf["temperature"].to_numpy().reshape((ny, nx))

        pyplot.figure(figsize=(20, 13), dpi=fileDpi)
        pyplot.contourf(
            coordinatesX, coordinatesY, temperature, alpha=0.5, cmap=cm.jet)
        filename = self.getTemperatureOutputStreamline
        cbar = pyplot.colorbar()
        cbar.ax.tick_params(labelsize=40)
        pyplot.contour(coordinatesX, coordinatesY, temperature, cmap=cm.jet)
        pyplot.xlabel('x (m)', fontsize=40)
        pyplot.ylabel('y (m)', fontsize=40)
        pyplot.tick_params(axis='both', labelsize=40)
        pyplot.savefig(
            filename + "." + fileFormat, dpi=fileDpi, format=fileFormat)
        pyplot.savefig(filename + "." + "pdf", dpi=fileDpi, format="pdf")
        pyplot.show()

    def plotProbesEvolution(self) -> None:

        time: np.array
        dpi_m: np.float
        probe1: np.array
        probe2: np.array
        probe3: np.array
        filename: str
        probe1Df: pd.DataFrame
        probe2Df: pd.DataFrame
        probe3Df: pd.DataFrame

        filename = self.getProbesPlotPath

        probe1Df = self.readOutput(self.getProbe1OutputPath)
        probe2Df = self.readOutput(self.getProbe2OutputPath)
        probe3Df = self.readOutput(self.getProbe3OutputPath)

        time = probe1Df["t"].to_numpy()
        probe1 = probe1Df["probe"].to_numpy()
        probe2 = probe2Df["probe"].to_numpy()
        probe3 = probe3Df["probe"].to_numpy()

        dpi_m = 1000
        pyplot.figure(num=2, figsize=(14, 11), dpi=dpi_m)
        pyplot.style.use('classic')
        pyplot.plot(
            time, probe1, color='black', linestyle='-', linewidth=2.5,
            label="probe 1 (0.01, 0.000)")
        pyplot.plot(
            time, probe2, color='red', linestyle='-', linewidth=2.5,
            label="probe 2 (0.01, 0.005)")
        pyplot.plot(
            time, probe3, color='magenta', linestyle='-', linewidth=2.5,
            label="probe 3 (0.01, 0.010)")
        pyplot.xlabel('t (s)', fontsize=35)
        pyplot.ylabel(r'T ($^{\circ}$C)', fontsize=35)
        # pyplot.axis([-0.1, 1.1, -0.1, 1.1])
        pyplot.tick_params(axis='both', labelsize=35)
        pyplot.tick_params(axis='both', labelsize=35)
        pyplot.legend(loc="upper left", frameon=False, ncol=1, fontsize=30)
        pyplot.grid()
        pyplot.savefig(filename + ".pdf", dpi=dpi_m, format='pdf')
        pyplot.show()
        pyplot.close()

    def plotDataComparison(self, fileFormat: str = 'pdf', fileDpi: int =
            1000):

        filename: str

        pressureDf: pd.DataFrame
        velocityXDf: pd.DataFrame
        velocityYDf: pd.DataFrame

        velocityX: np.ndarray
        velocityY: np.ndarray
        coordinatesX: np.ndarray
        coordinatesY: np.ndarray

        filenameCompY = self.getDirFigure + ct.OS_SEP + \
            "ComparisonAxisY_{}x{}".format(
                self.nodeNumberX, self.nodeNumberY)

        filenameCompX= self.getDirFigure + ct.OS_SEP + \
            "ComparisonAxisX_{}x{}".format(
                self.nodeNumberX, self.nodeNumberY)

        tempAnalyticalDf = self.readOutput(self.getAnalyticalSolutionPath)
        tempNumericalDf = self.readOutput(self.getTemperatureOutputPath)

        nx = self.nodeNumberX
        ny = self.nodeNumberY
        axisX = np.linspace(self.initialPositionX, self.finalPositionX, nx)
        axisY = np.linspace(self.initialPositionY, self.finalPositionY, ny)
        coordinatesX, coordinatesY = np.meshgrid(axisX, axisY)

        tempAnalytical = tempAnalyticalDf['temperature'].to_numpy().reshape(
            (ny, nx))
        tempNumerical = tempNumericalDf['temperature'].to_numpy().reshape(
            (ny, nx))

        L2_error_norm = np.sum((tempAnalytical - tempNumerical)**2)
        L2_norm = np.sum(tempAnalytical**2)

        l2_error = np.sqrt(L2_error_norm/L2_norm)

        relativeError = np.divide(
            abs(tempAnalytical - tempNumerical), abs(tempAnalytical),
            out=np.zeros(tempAnalytical.shape, dtype=float),
            where=tempAnalytical!=0)

        l1_error = np.mean(relativeError, where=relativeError<1)

        print("L2-Error: {}".format(l2_error))
        print("L1-Error: {}".format(l1_error))

        positionX = \
            (coordinatesX[0,:] > 0.01 - self.deltaX) & \
            (coordinatesX[0,:] < 0.01 + self.deltaX)

        positionY = \
            (coordinatesY[:, 0] > 0.005 - self.deltaY) & \
            (coordinatesY[:, 0] < 0.005 + self.deltaY)

        axisY = coordinatesY[:, positionX].mean(axis=1)
        axisX = coordinatesX[positionY, :].mean(axis=0)
        tempNumericalX = tempNumerical[:, positionX].mean(axis=1)
        tempNumericalY = tempNumerical[positionY, :].mean(axis=0)

        tempAnalyticalX = tempAnalytical[:, positionX].mean(axis=1)
        tempAnalyticalY = tempAnalytical[positionY, :].mean(axis=0)

        indices = np.arange(0, 255, 4)

        pyplot.figure(num=1, figsize=(18,14), dpi=fileDpi)
        pyplot.style.use('classic')
        pyplot.plot(tempNumericalX, axisY, color='black', linestyle='-',
            linewidth=2, label='FVM')
        pyplot.plot(np.take(tempAnalyticalX, indices),
            np.take(axisY, indices), color='red', linestyle='',
            marker="o", markersize=8, markeredgecolor='red',
            label='Analytical')
        pyplot.xlabel(r"$T$ ($^{\circ}$C)", fontsize=40)
        pyplot.ylabel(r"$y$ (m)", fontsize=40)
        pyplot.tick_params(axis='both', labelsize=40)
        pyplot.legend(loc='lower right', frameon=False, ncol=1, fontsize=40)
        pyplot.grid()
        pyplot.savefig(filenameCompY + "." + fileFormat, dpi=fileDpi,
            format=fileFormat)

        pyplot.figure(num=2, figsize=(17, 14), dpi=fileDpi)
        pyplot.style.use('classic')
        pyplot.plot(axisX, tempNumericalY, color='black', linestyle='-', linewidth=2,
                 label='FVM')
        pyplot.plot(np.take(axisX, indices), np.take(tempAnalyticalY, indices),
            color='red', linestyle='', marker="o", markersize=8,
            markeredgecolor='red', label='Analytical')
        pyplot.ylabel(r"$T$ ($^{\circ}$C)", fontsize=40)
        pyplot.xlabel(r"$x$ (m)", fontsize=40)
        pyplot.tick_params(axis='both', labelsize=40)
        pyplot.legend(loc='lower left', frameon=False, ncol=1, fontsize=40)
        pyplot.grid()
        pyplot.savefig(filenameCompX + "." + fileFormat, dpi=fileDpi,
            format=fileFormat)

    def plotProfiles(self, fileFormat: str = 'pdf', fileDpi: int =1000):

        filename: str

        pressureDf: pd.DataFrame
        velocityXDf: pd.DataFrame
        velocityYDf: pd.DataFrame

        velocityX: np.ndarray
        velocityY: np.ndarray
        coordinatesX: np.ndarray
        coordinatesY: np.ndarray

        filenameCompY = self.getDirFigure + ct.OS_SEP + \
            "profileCenterAxisY_{}x{}".format(
                self.nodeNumberX, self.nodeNumberY)

        filenameCompX= self.getDirFigure + ct.OS_SEP + \
            "profileCenterAxisX_{}x{}".format(
                self.nodeNumberX, self.nodeNumberY)

        tempNumericalDf = self.readOutput(self.getTemperatureOutputPath)

        nx = self.nodeNumberX
        ny = self.nodeNumberY
        axisX = np.linspace(self.initialPositionX, self.finalPositionX, nx)
        axisY = np.linspace(self.initialPositionY, self.finalPositionY, ny)
        coordinatesX, coordinatesY = np.meshgrid(axisX, axisY)

        tempNumerical = tempNumericalDf['temperature'].to_numpy().reshape(
            (ny, nx))

        positionCenterX = \
            (coordinatesX[0,:] > 0.01 - self.deltaX) & \
            (coordinatesX[0,:] < 0.01 + self.deltaX)

        positionSourceX = \
            (coordinatesX[0, :] > 0.0055 - self.deltaX) & (
             coordinatesX[0, :] < 0.0055 + self.deltaX)

        positionY = \
            (coordinatesY[:, 0] > 0.005 - self.deltaY) & \
            (coordinatesY[:, 0] < 0.005 + self.deltaY)

        axisCenterY = coordinatesY[:, positionCenterX].mean(axis=1)
        axisSourceY = coordinatesY[:, positionSourceX].mean(axis=1)
        axisX = coordinatesX[positionY, :].mean(axis=0)
        tempNumericalCenterX = tempNumerical[:, positionCenterX].mean(axis=1)
        tempNumericalSourceX = tempNumerical[:, positionSourceX].mean(axis=1)
        tempNumericalY = tempNumerical[positionY, :].mean(axis=0)

        pyplot.figure(num=1, figsize=(18,14), dpi=fileDpi)
        pyplot.style.use('classic')
        pyplot.plot(tempNumericalCenterX, axisCenterY, color='black',
            linestyle='-', linewidth=2, label='geometrical center')
        pyplot.plot(tempNumericalSourceX, axisSourceY,
            color='red', linestyle='', marker="o", markersize=8,
            markeredgecolor='red', label='source center')
        pyplot.xlabel(r"$T$ ($^{\circ}$C)", fontsize=40)
        pyplot.ylabel(r"$y$ (m)", fontsize=40)
        pyplot.tick_params(axis='both', labelsize=40)
        pyplot.legend(loc='upper right', frameon=False, ncol=1, fontsize=40)
        pyplot.grid()
        pyplot.savefig(filenameCompY + "." + fileFormat, dpi=fileDpi,
            format=fileFormat)

        pyplot.figure(num=2, figsize=(17, 14), dpi=fileDpi)
        pyplot.style.use('classic')
        pyplot.plot(
            axisX, tempNumericalY, color='black', linestyle='-', linewidth=2)
        pyplot.ylabel(r"$T$ ($^{\circ}$C)", fontsize=40)
        pyplot.xlabel(r"$x$ (m)", fontsize=40)
        pyplot.tick_params(axis='both', labelsize=40)
        pyplot.grid()
        pyplot.savefig(filenameCompX + "." + fileFormat, dpi=fileDpi,
            format=fileFormat)
