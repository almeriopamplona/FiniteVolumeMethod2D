import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import Constants as ct
from matplotlib import pyplot, cm
from MeshGenerator import MeshGenerator
from DirectoryManager import DirectoryManager
from matplotlib.animation import PillowWriter
# from mpl_toolkits.mplot3d import Axes3D


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

    def plotStreamlines(
            self, background: str, fileFormat: str = 'jpg', fileDpi: int =
            1000) -> None:

        filename: str

        pressureDf: pd.DataFrame
        velocityXDf: pd.DataFrame
        velocityYDf: pd.DataFrame

        axisX: np.ndarray
        axisY: np.ndarray
        pressure: np.ndarray
        velocityX: np.ndarray
        velocityY: np.ndarray
        coordinatesX: np.ndarray
        coordinatesY: np.ndarray

        filename = "DummyFile"

        pressureDf = self.readOutput(self.getPressureOutputPath)
        velocityXDf = self.readOutput(self.getVelocityXOutputPath)
        velocityYDf = self.readOutput(self.getVelocityYOutputPath)

        nx = self.nodeNumberX
        ny = self.nodeNumberY
        axisX = np.linspace(self.initialPositionX, self.finalPositionX, nx)
        axisY = np.linspace(self.initialPositionY, self.finalPositionY, ny)
        coordinatesX, coordinatesY = np.meshgrid(axisX, axisY)

        pressure = pressureDf["pressure"].to_numpy().reshape((ny, nx))
        velocityX = velocityXDf['velocityX'].to_numpy().reshape((ny, nx))
        velocityY = velocityYDf['velocityY'].to_numpy().reshape((ny, nx))

        pyplot.figure(figsize=(7, 6.5), dpi=fileDpi)

        if background == "pressure":
            pyplot.contourf(coordinatesX, coordinatesY, pressure, alpha=0.5,
                            cmap=cm.jet)
            filename = self.getPressureOutputStreamline

        elif background == "velocityX":
            pyplot.contourf(coordinatesX, coordinatesY, velocityX, alpha=0.5,
                            cmap=cm.jet)
            filename = self.getVelocityXOutputStreamline

        elif background == "velocityY":
            pyplot.contourf(coordinatesX, coordinatesY, velocityY, alpha=0.5,
                            cmap=cm.jet)
            filename = self.getVelocityYOutputStreamline
        
        elif background == "velocity":
            velocity = np.sqrt(velocityX**2 + velocityY**2)
            pyplot.contourf(coordinatesX, coordinatesY, velocity, alpha=0.5,
                            cmap=cm.jet)
            filename = self.getVelocityOutputStreamline
        else:
            print(
                "ERROR:: your background choice must be: 'pressure', "
                + "'velocityX' or 'velocityY'")
            exit()

        pyplot.colorbar()
        # pyplot.contour(X, Y, velocityX, cmap=cm.jet)
        pyplot.streamplot(
            coordinatesX, coordinatesY, velocityX, velocityY, color='k')
        pyplot.xlabel('X', fontsize=24)
        pyplot.ylabel('Y', fontsize=24)
        plt.tick_params(axis='both', labelsize=18)
        pyplot.axis([-0.05, 1.05,-0.05, 1.05])
        pyplot.savefig(
            filename + "." + fileFormat, dpi=fileDpi, format=fileFormat)

    def plotDataComparison(self, fileFormat: str = 'pdf', fileDpi: int =
            1000):

        filenameCompY: str
        filenameCompX: str

        pressureDf: pd.DataFrame
        velocityXDf: pd.DataFrame
        velocityYDf: pd.DataFrame

        velocityX: np.ndarray
        velocityY: np.ndarray
        coordinatesX: np.ndarray
        coordinatesY: np.ndarray

        filenameCompY = self.getDirFigure + ct.OS_SEP + \
            "ComparisonVelocityYRe{}_{}x{}".format(
                self.reynoldsNumber, self.nodeNumberX, self.nodeNumberY)

        filenameCompX= self.getDirFigure + ct.OS_SEP + \
            "ComparisonVelocityXRe{}_{}x{}".format(
                self.reynoldsNumber, self.nodeNumberX, self.nodeNumberY)

        velocityXDf = self.readOutput(self.getVelocityXOutputPath)
        velocityYDf = self.readOutput(self.getVelocityYOutputPath)
        ghiaVelocityXDf = self.readOutput(self.getGhiaVelocityVertPath)
        ghiaVelocityYDf = self.readOutput(self.getGhiaVelocityHoritPath)
        # agarwalVelocityXDf = self.readOutput(self.getAgarwalVelocityVertPath)
        # agarwalVelocityYDf = self.readOutput(self.getAgarwalVelocityHoritPath)

        nx = self.nodeNumberX
        ny = self.nodeNumberY
        axisX = np.linspace(self.initialPositionX, self.finalPositionX, nx)
        axisY = np.linspace(self.initialPositionY, self.finalPositionY, ny)
        coordinatesX, coordinatesY = np.meshgrid(axisX, axisY)

        velocityX = velocityXDf['velocityX'].to_numpy().reshape((ny, nx))
        velocityY = velocityYDf['velocityY'].to_numpy().reshape((ny, nx))

        positionX = \
            (coordinatesX[0,:] > 0.5 - self.deltaX) & \
            (coordinatesX[0,:] < 0.5 + self.deltaX)

        positionY = \
            (coordinatesY[:, 0] > 0.5 - self.deltaY) & \
            (coordinatesY[:, 0] < 0.5 + self.deltaY)

        axisY = coordinatesY[:, positionX].mean(axis=1)
        axisX = coordinatesX[positionY, :].mean(axis=0)
        velocityX= velocityX[:, positionX].mean(axis=1)
        velocityY = velocityY[positionY, :].mean(axis=0)

        ghiaAxisY = ghiaVelocityXDf['y'].to_numpy()
        ghiaAxisX = ghiaVelocityYDf['x'].to_numpy()
        # agarwalAxisY = agarwalVelocityXDf['y'].to_numpy()
        # agarwalAxisX = agarwalVelocityYDf['x'].to_numpy()

        ghiaVelocityY = ghiaVelocityYDf['velocity'].to_numpy()
        ghiaVelocityX = ghiaVelocityXDf['velocity'].to_numpy()
        # agarwalVelocityY = agarwalVelocityYDf['velocity'].to_numpy()
        # agarwalVelocityX = agarwalVelocityXDf['velocity'].to_numpy()

        Agarwal = 'Agarwal(1981)'
        NallasamyPrasad = "Nallasamy & Prasad (1977)"

        plt.figure(num=1, figsize=(14,14))
        pyplot.style.use('classic')
        plt.plot(velocityX, axisY, color='black', linestyle='-',
            linewidth=2, label='FVM')
        plt.plot(ghiaVelocityX, ghiaAxisY, color='red', linestyle='',
            marker="o", markersize=8, markeredgecolor='red',
            label='Ghia (1982)')
        # plt.plot(agarwalVelocityX, agarwalAxisY, color='magenta', linestyle='',
        #          marker="s", linewidth=2, markersize=8,
        #          markeredgecolor='magenta', label=Agarwal)
        plt.xlabel(r"$u$ / $U_{lid}$ (-)", fontsize=40)
        plt.ylabel(r"$y$ / $L$ (-)", fontsize=40)
        plt.tick_params(axis='both', labelsize=40)
        plt.legend(loc='lower right', frameon=False, ncol=1, fontsize=40)
        plt.grid()
        pyplot.savefig(filenameCompY + "." + fileFormat, dpi=fileDpi,
            format=fileFormat)
        # plt.show()

        plt.figure(num=2, figsize=(17, 14))
        pyplot.style.use('classic')
        plt.plot(axisX, velocityY, color='black', linestyle='-', linewidth=2,
                 label='FVM')
        plt.plot(ghiaAxisX, ghiaVelocityY, color='red', linestyle='',
                 marker="o", markersize=8, markeredgecolor='red',
                 label='Ghia (1982)')
        # plt.plot(agarwalAxisX, agarwalVelocityY, color='magenta',
        #            linestyle='',
        #          marker="s", linewidth=2, markersize=8,
        #          markeredgecolor='magenta', label=NallasamyPrasad)
        plt.ylabel(r"$v$ / $U_{lid}$ (-)", fontsize=40)
        plt.xlabel(r"$x$ / $L$ (-)", fontsize=40)
        plt.tick_params(axis='both', labelsize=40)
        plt.legend(loc='lower left', frameon=False, ncol=1, fontsize=40)
        plt.grid()
        pyplot.savefig(filenameCompX + "." + fileFormat, dpi=fileDpi,
            format=fileFormat)
        #plt.show()

    def makeVideo(self):

        filename: str
        nx: int
        ny: int
        axisX: np.array
        axisY: np.array
        velocity: np.array
        velocityX: np.array
        velocityY: np.array
        coordinatesX: np.array
        coordinatesY: np.array
        pressureDf: pd.DataFrame
        velocityXDf: pd.DataFrame
        velocityYDf: pd.DataFrame

        # pressureDf = self.readOutput(self.getPressureOutputPath)
        velocityXDf = self.readOutput(self.getVelocityXOutputPath)
        velocityYDf = self.readOutput(self.getVelocityYOutputPath)

        nx = self.nodeNumberX
        ny = self.nodeNumberY
        axisX = np.linspace(self.initialPositionX, self.finalPositionX, nx)
        axisY = np.linspace(self.initialPositionY, self.finalPositionY, ny)
        coordinatesX, coordinatesY = np.meshgrid(axisX, axisY)

        fig = pyplot.figure(6, (10, 10))
        metadata = dict(title="Cavity", artist="Almerio")
        writer = PillowWriter(fps=60, metadata=metadata)

        with writer.saving(fig, "video.gif", 100):
            for j in range(0, self.timeSize, 10):
                time = "t{}".format(j)
                pyplot.style.use('classic')
                velocityX = velocityXDf[time].to_numpy().reshape((ny, nx))
                velocityY = velocityYDf[time].to_numpy().reshape((ny, nx))
                velocity = np.sqrt(velocityX**2 + velocityY**2)
                pyplot.contourf(
                    coordinatesX, coordinatesY, velocity, alpha=0.5,
                    cmap=cm.jet)
                pyplot.streamplot(
                    coordinatesX, coordinatesY, velocityX, velocityY, color='k')
                pyplot.xlabel('X')
                pyplot.ylabel('Y')
                pyplot.tick_params(axis='both', labelsize=24)
                pyplot.axis([0.0, 1, 0.0, 1.0])
                writer.grab_frame()
                pyplot.cla()
