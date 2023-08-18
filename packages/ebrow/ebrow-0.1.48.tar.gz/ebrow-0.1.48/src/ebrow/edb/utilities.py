"""
******************************************************************************

    Echoes Data Browser (Ebrow) is a data navigation and report generation
    tool for Echoes.
    Echoes is a RF spectrograph for SDR devices designed for meteor scatter
    Both copyright (C) 2018-2023
    Giuseppe Massimo Bertani gm_bertani(a)yahoo.it

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, http://www.gnu.org/copyleft/gpl.html

*******************************************************************************

"""
import os
import shutil
import numpy as np
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QByteArray
import matplotlib as mp
from matplotlib.colors import ListedColormap
import pandas as pd
import math
import matplotlib.ticker as ticker
from matplotlib.dates import num2date
from pathlib import Path
from .logprint import print

class PrecisionDateFormatter(ticker.Formatter):
    """
    Extend the `matplotlib.ticker.Formatter` class to allow for millisecond
    precision when formatting a tick (in days since the epoch) with a
    `~datetime.datetime.strftime` format string.

    """

    def __init__(self, fmt, precision=3, tz=None):
        """
        Parameters
        ----------
        fmt : str
            `~datetime.datetime.strftime` format string.
        """

        if tz is None:
            from matplotlib.dates import _get_rc_timezone
            tz = _get_rc_timezone()

        self.fmt = fmt
        self.tz = tz
        self.precision = precision

    def __call__(self, x, pos=0):
        # if x == 0:
        #     raise ValueError("PrecisionDateFormatter found a value of 0, which is "
        #                      "an illegal date; this usually occurs because "
        #                      "you have not informed that axis that it is "
        #                      "plotting dates, e.g., with ax.xaxis_date()")

        dt = num2date(x, self.tz)
        ms = dt.strftime("%f")[:self.precision]

        return dt.strftime(self.fmt).format(ms=ms)

    def set_tzinfo(self, tz):
        self.tz = tz


def splitDumpFile(data: QByteArray):
    lineNum = 1
    dataStr = data.data().decode()
    dataLines = dataStr.splitlines()
    mapList = []
    powerList = []
    for line in dataLines:
        cells = line.split()
        if len(cells) >= 3:
            timeMs = float(cells[0])  # int(float(cells[0]) * 1000)
            if len(cells) == 3:
                cells[0] = timeMs
                cells[1] = int(cells[1])
                cells[2] = float(cells[2])
                mapList.append(cells[:3])

            if len(cells) == 7:
                # scan line end
                cells[0] = timeMs
                cells[1] = int(cells[1])
                cells[2] = float(cells[2])
                cells[3] = timeMs
                cells[4] = float(cells[4])
                cells[5] = float(cells[5])
                cells[6] = float(cells[6])
                powerList.append(cells[3:])

    dfMap = pd.DataFrame(mapList, columns=['time', 'frequency', 'S'])
    dfPower = pd.DataFrame(powerList, columns=['time', 'N', 'S', 'diff'])
    # dfPower['time'] = (pd.to_datetime(dfPower['time'], unit='s'))
    dfPower['timestamp'] = (pd.to_datetime(dfPower['time'], unit='s'))
    # dfMap['time'] = dfMap['time'].astype('datetime64')

    return dfMap, dfPower


def castFloatPrecision(value: float, precision: int = 4):
    if value != 0:
        multipliers = [0, 10, 100, 1000, 10e3, 10e4, 10e5, 10e6, 10e7]
        if precision > 8:
            precision = 8
        mult = multipliers[precision]
        v2 = value * mult
        result = int(v2) / mult
        # print ("cast: {} --> {}".format(value, result))
    else:
        result = value
    return result


def clearLayout(layout):
    toDelete = layout.count()
    print("Clearing {} thumbnails".format(toDelete))
    while layout.count() > 0:
        child = layout.takeAt(0)
        if child.widget():
            child.widget().hide()
            child.widget().deleteLater()
            print("deleted child widget")
        elif child.layout():
            clearLayout(child.layout())
            print("deleted child layout")


def notice(title: str, msg: str):
    errorbox = QMessageBox()
    errorbox.setWindowTitle("Echoes data browser")
    errorbox.setText(title + "\n" + msg)
    errorbox.setIcon(QMessageBox.Information)
    errorbox.exec_()


def getColorMap(name: str = 'echoes'):
    # echoes color scale
    echoes = [
        "black",
        "blue",
        "purple",
        "orange",
        "yellow",
        "white"
    ]

    # Colorgramme-like 25 colors scale
    colorgramme = [
        "#000000",
        "#0064fe",
        "#006dfd",
        "#0079f0",
        "#0087fe",
        "#009eff",
        "#00b0ff",
        "#00c6f3",
        "#00eaff",
        "#38fcf5",
        "#4efdd4",
        "#6cfcb8",
        "#83fca1",
        "#a4f892",
        "#b8fc7a",
        "#d1fc68",
        "#f4f96d",
        "#ffe600",
        "#ffc500",
        "#ffae00",
        "#ff9400",
        "#ff8600",
        "#ff7300",
        "#ff6300",
        "#ff1600"
    ]

    cmap = None
    if name == 'echoes':
        colors = echoes
        totColors = len(colors)
    elif name == 'colorgramme':
        colors = colorgramme
        totColors = len(colors)
    else:
        cmap = mp.colormaps[name]
        totColors = cmap.N
        # cmap = mp.colormaps[name]._resample(totColors)

    if cmap is None:
        cmap = ListedColormap(colors, name=name)
    print("name={}, total colors={}".format(name, totColors))
    return cmap


def createCustomColormapsDict():
    myCmaps = dict()

    # matplotlib embedded colormaps
    for key in mp.colormaps.keys():
        # print("key=", key)
        myCmaps[key] = mp.colormaps[key]

    # customized colormaps
    for key in ['echoes', 'colorgramme']:
        cmap = getColorMap(key)
        myCmaps[key] = cmap
    return myCmaps


def fpCmp(val1: float, val2: float, decimals: int):
    multiplier = math.pow(10, decimals)
    i1 = int(val1 * multiplier)
    i2 = int(val2 * multiplier)
    return i2 - i1


def fuzzyCompare(a: float, b: float, tolerance: float):
    diff = math.fabs(a - b)
    percDiff = math.fabs((diff * 100) / a)
    if percDiff > tolerance:
        return 1 if (a > b) else -1
    return 0


def normalize(a: object, beg: float, end: float, default: float):
    b = np.interp(a, (a.min(), a.max()), (beg, end))
    b[np.isnan(b)] = default
    return b


def cleanFolder(folderPath: str, removeEmptyFolders: bool = True):
    for filename in os.listdir(folderPath):
        file_path = os.path.join(folderPath, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path) and removeEmptyFolders:
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            return False
    return True


def mkExportFolder(folderPath: Path):
    return Path.mkdir(folderPath, parents=True, exist_ok=True)


def cryptDecrypt(st: str, key: int) -> str:
    stCrypt = ''
    for i in range(len(st)):
        stCrypt += chr(ord(st[i]) ^ (key >> 8))
    return stCrypt
