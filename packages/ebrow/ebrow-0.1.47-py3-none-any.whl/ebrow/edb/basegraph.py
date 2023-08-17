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
import matplotlib as mp
import matplotlib.pyplot as plt

from .settings import Settings
from .logprint import print

mp.use('Qt5Agg')


class BaseGraph:
    def __init__(self, settings: Settings, target: str = None):
        self._settings = settings
        self._target = target
        self.setFont(self._target)
        self._canvas = None

    def widget(self):
        return self._canvas

    def saveToDisk(self, fileName):
        pix = self._canvas.grab()
        pix.save(fileName)

    def setFont(self, target: str = None):
        SMALL_SIZE = self._settings.readSettingAsInt('fontSize')
        if target == 'RMOB':
            SMALL_SIZE = 20
            if os.name == 'nt':
                plt.rc('font',
                       size=SMALL_SIZE,
                       family='Arial',
                       weight=100,
                       style='normal'
                       )  # controls default text font attributes
            else:
                plt.rc('font',
                       size=SMALL_SIZE,
                       family='Helvetica',
                       weight=100,
                       style='normal'
                       )  # controls default text font attributes

        else:
            plt.rc('font',
                   size=SMALL_SIZE,
                   family=self._settings.readSettingAsString('fontFamily'),
                   weight='bold' if 'Bold' in self._settings.readSettingAsString('fontStyle') else 'normal',
                   style='italic' if 'Italic' in self._settings.readSettingAsString('fontStyle') else 'normal'
                   )  # controls default text font attributes

        MEDIUM_SIZE = SMALL_SIZE + 4
        BIGGER_SIZE = MEDIUM_SIZE + 6

        plt.rc('axes', titlesize=MEDIUM_SIZE)  # fontsize of the axes title
        plt.rc('axes', labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
        plt.rc('xtick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('ytick', labelsize=SMALL_SIZE)  # fontsize of the tick labels
        plt.rc('legend', fontsize=MEDIUM_SIZE)  # legend fontsize
        plt.rc('figure', titlesize=BIGGER_SIZE, titleweight='bold')  # fontsize of the figure title

        plt.rcParams['savefig.pad_inches'] = 0
