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
import matplotlib.pyplot as plt
from pathlib import Path
from math import isnan

from PyQt5.QtWidgets import QHBoxLayout, QScrollArea, QLabel, QWidget, QInputDialog, QAbstractItemView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt, QSortFilterProxyModel, QItemSelectionModel

from .thumbnails_browser import ThumbnailsBrowser
from .powerplot import PowerPlot
from .mapplot import MapPlot
from .mapplot3d import MapPlot3D
from .pandasmodel import PandasModel
from .utilities import splitDumpFile, mkExportFolder
from .logprint import print

class ScreenShots:
    SSTW_CHRONO = 0
    SSTW_THUMBNAILS = 1
    SSTW_SSHOT = 2
    SSTW_POWER = 3
    SSTW_CMAP = 4
    SSTW_3D = 5
    SSTW_DETAILS = 6

    def __init__(self, parent, ui, settings):
        self._ui = ui
        self._parent = parent
        self._settings = settings
        self._screenShot = None
        self._powerPlot = None
        self._cmap2Dplot = None
        self._per3Dplot = None
        self._currentObj = None
        self._utcDate = None
        self._plot = None
        self._dfDetails = None
        self._dfChrono = None
        self._classFilter = ''
        self._sides = ['+XY', '+XZ', '+YZ', '-XY', '-XZ', '-YZ', ]
        self._aspects = [[90, -90], [0, -90], [0, 0], [-90, 90], [0, 90], [0, 180]]
        self._sideIdx = 0
        self._container = None
        self._pixWidth = 0
        self._pixHeight = 0
        self._px = plt.rcParams['figure.dpi']  # from inches to pixels
        self._exportDir = Path(self._parent.exportDir, "events")
        mkExportFolder(self._exportDir)
        self._currentColormap = self._settings.readSettingAsString('currentColormap')
        self._ui.cbCmaps.setCurrentText(self._currentColormap)

        if self._parent.currentID == 0:
            self._ui.lbID.setText('Nothing selected')
            self._ui.lbDaily.setText('------')
            self._ui.lbThisDay.setText('------')

        self._ui.lbID.setText('ID# ' + str(self._parent.currentID))
        self._ui.lbDaily.setText('Daily# ' + str(self._parent.currentDailyNr))
        self._getClassFilter()
        self._vMinMaxEnable(False)
        self._3dEnable(False)
        self._cmapEnable(False)
        self._tbs = None

        self._ui.lbSide.setText(self._sides[self._sideIdx])

        self._linkedSliders = self._settings.readSettingAsBool('linkedSliders')
        self._ui.chkLinked.setChecked(self._linkedSliders)

        self._showGrid = self._settings.readSettingAsBool('showGrid')
        self._ui.chkGrid.setChecked(self._showGrid)

        self._hZoom = self._settings.readSettingAsFloat('horizontalZoom')
        self._ui.hsHzoom.setValue(int(self._hZoom * 10))
        self._ui.lbHzoom.setNum(self._hZoom)

        self._vZoom = self._settings.readSettingAsFloat('verticalZoom')
        self._ui.hsVzoom.setValue(int(self._vZoom * 10))
        self._ui.lbVzoom.setNum(self._vZoom)

        self._azimuth = self._settings.readSettingAsInt('3Dazimuth')
        self._ui.hsAzimuth.setValue(self._azimuth)
        self._ui.lbAzimuth.setNum(self._azimuth)

        self._elevation = self._settings.readSettingAsInt('3Delevation')
        self._ui.hsElevation.setValue(self._elevation)
        self._ui.lbElevation.setNum(self._elevation)

        side = 0
        for plane in self._aspects:
            if self._azimuth == plane[1] and self._elevation == plane[0]:
                self._ui.lbSide.setText(self._sides[side])
                break
            side += 1

        self._plotVmax = self._settings.DBFS_RANGE_MAX
        self._ui.hsVmax.setMinimum(self._settings.DBFS_RANGE_MIN)
        self._ui.hsVmax.setMaximum(self._settings.DBFS_RANGE_MAX)
        self._ui.hsVmax.setValue(self._plotVmax)
        self._ui.lbVmax.setNum(self._plotVmax)

        self._plotVmin = self._settings.DBFS_RANGE_MIN
        self._ui.hsVmin.setMinimum(self._settings.DBFS_RANGE_MIN)
        self._ui.hsVmin.setMaximum(self._settings.DBFS_RANGE_MAX)
        self._ui.hsVmin.setValue(self._plotVmin)
        self._ui.lbVmin.setNum(self._plotVmin)

        self._ui.twShots.setTabEnabled(self.SSTW_THUMBNAILS, False)
        self._ui.twShots.setTabEnabled(self.SSTW_SSHOT, False)
        self._ui.twShots.setTabEnabled(self.SSTW_POWER, False)
        self._ui.twShots.setTabEnabled(self.SSTW_CMAP, False)
        self._ui.twShots.setTabEnabled(self.SSTW_3D, False)

        self.refresh()
        self._ui.chkOverdense.clicked.connect(self._setClassFilter)
        self._ui.chkUnderdense.clicked.connect(self._setClassFilter)
        self._ui.chkFakeEsd.clicked.connect(self._setClassFilter)
        self._ui.chkFakeCar1.clicked.connect(self._setClassFilter)
        self._ui.chkFakeCar2.clicked.connect(self._setClassFilter)
        self._ui.chkFakeSat.clicked.connect(self._setClassFilter)
        self._ui.chkFakeLong.clicked.connect(self._setClassFilter)
        self._ui.chkLOSfilter.clicked.connect(self._setClassFilter)
        self._ui.chkLinked.clicked.connect(self._toggleLinkedCursors)
        self._ui.chkGrid.clicked.connect(self._toggleGrid)
        self._ui.rbOverdense.clicked.connect(self._changeClassification)
        self._ui.rbUnderdense.clicked.connect(self._changeClassification)
        self._ui.rbLOSfilter.clicked.connect(self._changeClassification)
        self._ui.rbFakeEsd.clicked.connect(self._changeClassification)
        self._ui.rbFakeCar1.clicked.connect(self._changeClassification)
        self._ui.rbFakeCar2.clicked.connect(self._changeClassification)
        self._ui.rbFakeSat.clicked.connect(self._changeClassification)
        self._ui.rbFakeLong.clicked.connect(self._changeClassification)
        self._ui.twShots.currentChanged.connect(self.updateTabEvents)
        self._ui.hsVmin.valueChanged.connect(self._changePlotVmin)
        self._ui.hsVmax.valueChanged.connect(self._changePlotVmax)
        self._ui.hsHzoom.valueChanged.connect(self._changeHzoom)
        self._ui.hsVzoom.valueChanged.connect(self._changeVzoom)
        self._ui.hsAzimuth.valueChanged.connect(self._changeAzimuth)
        self._ui.hsElevation.valueChanged.connect(self._changeElevation)

        self._ui.pbRefresh.clicked.connect(self._refreshPressed)
        self._ui.pbReset.clicked.connect(self._resetPressed)
        self._ui.pbSide.clicked.connect(self._sidePressed)
        self._ui.cbCmaps.textActivated.connect(self._cmapChanged)
        self._ui.chkAll.clicked.connect(self._toggleCheckAll)
        self._ui.pbShotExp.clicked.connect(self._exportPressed)

    def updateTabEvents(self):
        self._parent.busy(True)

        if self._parent.currentID == 0:
            self._ui.lbID.setText('Nothing selected')
            self._ui.lbDaily.setText('------')
            self._ui.lbThisDay.setText('------')
        else:
            self._ui.lbID.setText('ID# ' + str(self._parent.currentID))

        if self._ui.twMain.currentIndex() == self._parent.TWMAIN_EVENTS:
            if self._currentObj is not None:
                self._currentObj = None
            if self._ui.twShots.currentIndex() == self.SSTW_CHRONO:
                self._plotSettingsEnable(False)
                self._vMinMaxEnable(False)
                self._3dEnable(False)
                self._cmapEnable(False)
                self.displayChronological()
                self._currentObj = None
            if self._ui.twShots.currentIndex() == self.SSTW_THUMBNAILS:
                self._plotSettingsEnable(False)
                self._vMinMaxEnable(False)
                self._3dEnable(False)
                self._cmapEnable(False)
                doReload = self.browseThumbnails()
                self.refresh(self._parent.currentIndex, doReload)
            if self._ui.twShots.currentIndex() == self.SSTW_SSHOT:
                self._plotSettingsEnable(True)
                self._vMinMaxEnable(False)
                self._3dEnable(False)
                self._cmapEnable(False)
                self.displayScreenshot()
                self._currentObj = self._screenShot
            if self._ui.twShots.currentIndex() == self.SSTW_POWER:
                self._plotSettingsEnable(True)
                self._vMinMaxEnable(False)
                self._3dEnable(False)
                self._cmapEnable(False)
                self.displayPowerPlot()
                self._currentObj = self._powerPlot
            if self._ui.twShots.currentIndex() == self.SSTW_CMAP:
                self._plotSettingsEnable(True)
                self._vMinMaxEnable(True)
                self._3dEnable(False)
                self._cmapEnable(True)
                self.displayMapPlot()
                self._currentObj = self._cmap2Dplot
            if self._ui.twShots.currentIndex() == self.SSTW_3D:
                self._plotSettingsEnable(True)
                self._vMinMaxEnable(True)
                self._3dEnable(True)
                self._cmapEnable(True)
                self.displayMapPlot3D()
                self._currentObj = self._per3Dplot
            if self._ui.twShots.currentIndex() == self.SSTW_DETAILS:
                self._plotSettingsEnable(False)
                self._vMinMaxEnable(False)
                self._3dEnable(False)
                self._cmapEnable(False)
                self.displayDetails()
                self._currentObj = None
        self._parent.busy(False)

    def getCoverage(self, selfAdjust: bool = False):
        (fromDate, toDate, fromId, toId) = self._parent.dataSource.idCoverage(self._parent.fromDate,
                                                                              self._parent.toDate, selfAdjust)
        if isnan(fromId) or isnan(toId):
            print("not enough data to cover the given range {} - {}".format(
                self._parent.fromDate, self._parent.toDate))
            if not selfAdjust:
                return False
            else:
                print("fixing range to cover all known data")
                (fromDate, toDate, fromId, toId) = self._parent.dataSource.idCoverage(self._parent.fromDate,
                                                                                      self._parent.toDate,
                                                                                      selfAdjust=True)

        self._parent.fromId = fromId
        self._parent.toId = toId
        self._parent.fromDate = fromDate
        self._parent.toDate = toDate

        if self._parent.currentID == 0:
            self._ui.lbID.setText('Nothing selected')
            self._ui.lbDaily.setText('------')
            self._ui.lbThisDay.setText('------')
        else:
            self._ui.lbID.setText('ID# ' + str(self._parent.currentID))
            self._ui.lbThisDay.setText(fromDate)
            if self._parent.currentDate is not None:
                self._ui.lbThisDay.setText(self._parent.currentDate)

        self.getDailyCoverage()
        self._ui.tvChrono.clicked.connect(self._selectEvent)
        self._ui.twShots.setCurrentIndex(self.SSTW_CHRONO)
        return True

    def getDailyCoverage(self):
        if self._parent.currentID == 0:
            self._ui.lbID.setText('Nothing selected')
            self._ui.lbDaily.setText('------')
            self._ui.lbThisDay.setText('------')
        else:
            self._parent.toDailyNr = self._parent.dataSource.dailyCoverage(self._parent.currentDate)
            if self._parent.toDailyNr != '':
                self._ui.lbDaily.setText('Daily# ' + str(self._parent.currentDailyNr))
                if len(self._parent.filteredIDs) > 0:
                    self._parent.currentID = self._parent.filteredIDs[self._parent.currentIndex]
                    self._ui.lbID.setText('ID# ' + str(self._parent.currentID))
                    return True
        return False

    def browseThumbnails(self):
        self._parent.busy(True)
        self._ui.chkDatExport.show()
        refreshNeeded = False
        if self._tbs is None:
            self._tbs = ThumbnailsBrowser(self._parent, self, self._ui)
            refreshNeeded = True

        if self._tbs.selectID(self._parent.currentID):
            refreshNeeded = True

        self._parent.busy(False)
        return refreshNeeded

    def displayChronological(self):
        # called when the chronological table gets updated
        self._parent.busy(True)
        self._ui.chkDatExport.hide()
        df = self._parent.dataSource.getADpartialCompositeFrame(self._parent.fromDate, self._parent.toDate,
                                                                self._classFilter)
        self._dfChrono = df
        model = PandasModel(df)
        self._ui.tvChrono.setModel(model)
        self._utcDate = self._parent.currentDate
        if self._parent.currentID > 0:
            self._findEvent(self._parent.currentID)
        self._parent.busy(False)

    def displayScreenshot(self):
        if self._parent.currentID > 0:
            self._parent.busy(True)
            self._ui.chkDatExport.show()
            name, data, dailyNr, self._utcDate = self._parent.dataSource.extractShotData(self._parent.currentID)
            if data is not None:
                print("displayScreenshot(currentId={}) {}".format(self._parent.currentID, name))
                layout = self._ui.wSsContainer.layout()
                if layout is None:
                    layout = QHBoxLayout()
                else:
                    layout.removeWidget(self._screenShot)

                self._ui.lbShotFilename.setText(name)
                self._ui.lbDaily.setText('Daily# ' + str(self._parent.currentDailyNr))
                # inchWidth, inchHeight = self._calcFigSizeInch(self._ui.wSsContainer)
                scroller = QScrollArea()
                ss = QLabel()
                pix = QPixmap()
                pix.loadFromData(data)
                self._pixWidth = int(pix.size().width() * self._hZoom)
                self._pixHeight = int(pix.size().height() * self._vZoom)
                newSize = QSize(self._pixWidth, self._pixHeight)
                pix = pix.scaled(newSize, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
                ss.setPixmap(pix)
                scroller.setWidget(ss)
                layout.addWidget(scroller)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                self._ui.wSsContainer.setLayout(layout)
                scroller.ensureVisible(int(self._pixWidth / 2), int(self._pixHeight / 2))
                self._screenShot = scroller
                self._parent.busy(False)
        else:
            self._parent.infoMessage("Ebrow", "No selected events to show")
            layout = self._ui.wSsContainer.layout()
            if layout is not None:
                layout.removeWidget(self._screenShot)




    def displayPowerPlot(self):
        if self._parent.currentID > 0:
            # self._parent.busy(True, spinner=False)  # spinner seems not updated while plotting
            self._ui.chkDatExport.show()
            name, data, dailyNr, self._utcDate = self._parent.dataSource.extractDumpData(self._parent.currentID)
            if data is None:
                self._parent.infoMessage("Display power plot", "The selected event has no dump file associated")
                return
            dfMap, dfPower = splitDumpFile(data)
            dfPower = dfPower.set_index('timestamp')
            print("displayPowerPlot(currentId={}) {}".format(self._parent.currentID, name))
            layout = self._ui.wPowerContainer.layout()
            if layout is None:
                layout = QHBoxLayout()
            else:
                layout.removeWidget(self._powerPlot)

            self._ui.lbShotFilename.setText(name)
            self._ui.lbDaily.setText('Daily# ' + str(self._parent.currentDailyNr))
            inchWidth, inchHeight = self._calcFigSizeInch(self._ui.wPowerContainer)
            xLocBaseSecs = int(5.0 / self._hZoom)
            if xLocBaseSecs == 0:
                xLocBaseSecs = 1
            yMinTicks = int(10 * self._vZoom)
            self._plot = PowerPlot(dfPower, name, self._settings, inchWidth, inchHeight, xLocBaseSecs, yMinTicks,
                                   self._showGrid)
            scroller = QScrollArea()
            canvas = self._plot.widget()
            canvas.setMinimumSize(QSize(self._pixWidth, self._pixHeight))
            scroller.setWidget(canvas)
            layout.addWidget(scroller)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            self._ui.wPowerContainer.setLayout(layout)
            self._powerPlot = scroller
            # self._parent.busy(False)
        else:
            self._parent.infoMessage("Ebrow", "No selected events to show")
            layout = self._ui.wPowerContainer.layout()
            if layout is not None:
                layout.removeWidget(self._powerPlot)

    def displayMapPlot(self):
        if self._parent.currentID > 0:
            # self._parent.busy(True, spinner=False) # spinner seems not updated while plotting
            self._ui.chkDatExport.show()
            name, data, dailyNr, self._utcDate = self._parent.dataSource.extractDumpData(self._parent.currentID)
            if data is None:
                self._parent.infoMessage("Display map plot", "The selected event has no dump file associated")
                return
            dfMap, dfPower = splitDumpFile(data)
            dfMap = dfMap.set_index('time')
            dfPower = dfPower.set_index('time')
            print("displayMapPlot(currentId={}) {}".format(self._parent.currentID, name))
            layout = self._ui.wCmap2Dcontainer.layout()
            if layout is None:
                layout = QHBoxLayout()
            else:
                layout.removeWidget(self._cmap2Dplot)

            self._ui.lbShotFilename.setText(name)
            self._ui.lbDaily.setText('Daily# ' + str(self._parent.currentDailyNr))
            inchWidth, inchHeight = self._calcFigSizeInch(self._ui.wCmap2Dcontainer)
            hzTickRanges = [1000, 500, 500, 500, 200, 200, 200, 200, 100, 100]
            tickEveryHz = hzTickRanges[int(self._hZoom - 1)]
            secTickRanges = [5, 2, 2, 1, 1, 0.5, 0.5, 0.2, 0.2, 0.1]
            tickEverySecs = secTickRanges[int(self._vZoom - 1)]
            cmap = self._parent.cmapDict[self._currentColormap]
            self._plot = MapPlot(dfMap, dfPower, self._settings, inchWidth, inchHeight, cmap, name, self._plotVmin,
                                 self._plotVmax,
                                 tickEveryHz,
                                 tickEverySecs, self._showGrid)
            minV, maxV = self._plot.getMinMax()
            if self._plotVmin < minV:
                self._ui.hsVmin.setValue(int(minV))
                self._ui.lbPowerFrom.setNum(self._plotVmin)
            if self._plotVmax > maxV:
                self._ui.hsVmax.setValue(int(maxV))
                self._ui.lbPowerTo.setNum(self._plotVmax)
            scroller = QScrollArea()
            canvas = self._plot.widget()
            canvas.setMinimumSize(QSize(self._pixWidth, self._pixHeight))
            scroller.setWidget(canvas)
            layout.addWidget(scroller)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            scroller.ensureVisible(int(self._pixWidth / 2), int(self._pixHeight / 2))
            self._ui.wCmap2Dcontainer.setLayout(layout)
            self._cmap2Dplot = scroller
            # self._parent.busy(False)
        else:
            self._parent.infoMessage("Ebrow", "No selected events to show")
            layout = self._ui.wCmap2Dcontainer.layout()
            if layout is not None:
                layout.removeWidget(self._cmap2Dplot)

    def displayMapPlot3D(self):
        if self._parent.currentID > 0:
            # self._parent.busy(True, spinner=False)  # spinner seems not updated while plotting
            self._ui.chkDatExport.show()
            name, data, dailyNr, self._utcDate = self._parent.dataSource.extractDumpData(self._parent.currentID)
            if data is None:
                self._parent.infoMessage("Display map plot 3D", "The selected event has no dump file associated")
                return
            dfMap, dfPower = splitDumpFile(data)
            dfMap = dfMap.set_index('time')
            dfPower = dfPower.set_index('time')
            print("displayMapPlot3D(currentId={}) {}".format(self._parent.currentID, name))
            layout = self._ui.wPer3Dcontainer.layout()
            if layout is None:
                layout = QHBoxLayout()
            else:
                layout.removeWidget(self._per3Dplot)

            self._ui.lbShotFilename.setText(name)
            self._ui.lbDaily.setText('Daily# ' + str(self._parent.currentDailyNr))
            inchWidth, inchHeight = self._calcFigSizeInch(self._ui.wPer3Dcontainer)
            hzTickRanges = [1000, 500, 500, 500, 200, 200, 200, 200, 100, 100]
            tickEveryHz = hzTickRanges[int(self._hZoom - 1)]
            secTickRanges = [5, 2, 2, 1, 1, 0.5, 0.5, 0.2, 0.2, 0.1]
            tickEverySecs = secTickRanges[int(self._vZoom - 1)]
            cmap = self._parent.cmapDict[self._currentColormap]
            self._plot = MapPlot3D(dfMap, dfPower, self._settings, inchWidth, inchHeight, cmap, name, self._plotVmin,
                                   self._plotVmax,
                                   tickEveryHz,
                                   tickEverySecs, self._showGrid)
            min, max = self._plot.getMinMax()
            if self._plotVmin < min:
                self._ui.hsVmin.setValue(int(min))
                self._ui.lbPowerFrom.setNum(self._plotVmin)
            if self._plotVmax > max:
                self._ui.hsVmax.setValue(int(max))
                self._ui.lbPowerTo.setNum(self._plotVmax)

            scroller = QScrollArea()
            canvas = self._plot.widget()
            canvas.setMinimumSize(QSize(self._pixWidth, self._pixHeight))
            scroller.setWidget(canvas)
            layout.addWidget(scroller)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            scroller.ensureVisible(int(self._pixWidth / 2), int(self._pixHeight / 2))
            self._ui.wPer3Dcontainer.setLayout(layout)
            self._per3Dplot = scroller
            self._plot.rotate(self._azimuth, self._elevation)
            # self._parent.busy(False)
        else:
            self._parent.infoMessage("Ebrow", "No selected events to show")
            layout = self._ui.wPer3Dcontainer.layout()
            if layout is not None:
                layout.removeWidget(self._per3Dplot)

    def displayDetails(self):
        if self._parent.currentID == 0:
            self._parent.infoMessage("Ebrow", "No selected events to show")
            return
        # self._parent.busy(True)
        self._ui.chkDatExport.hide()
        df = self._parent.dataSource.getEventData(self._parent.currentID)
        df.set_axis(['RAISE', 'PEAK', 'FALL'], axis=1)  # , inplace=True)
        df.set_axis(['UTC time', 'Upper threshold (calculated)', 'Lower threshold (calculated)', 'S', 'Average S',
                     'N', 'S-N', 'Average S-N', 'Peak frequency [Hz]', 'Standard deviation', 'Event lasting [ms]',
                     'Event lasting [scans]', 'Frequency shift [Hz]', 'Echo area', 'Interval area', 'Peaks count',
                     'LOS speed [m/s]', 'Scan lasting [ms]', 'S-N (begin scan)', 'S-N (end scan)', 'Classification',
                     'Screenshot filename', 'Plot filename'],
                    axis=0)  # , inplace=True)

        # data patching:
        # classification is known only at falling edge, so it should not appear under RAISE and PEAK columns
        df.iat[20, 0] = ''
        df.iat[20, 1] = ''

        model = PandasModel(df)
        self._ui.tvShotDetails.setModel(model)
        self._ui.tvShotDetails.setStyleSheet("color: rgb(0,255,0);  font: 10pt \"Gauge\";")
        self._ui.tvShotDetails.resizeColumnsToContents()
        self._updateClassification()
        self._dfDetails = df
        # self._parent.busy(False)

    def _updateClassification(self):
        self._parent.busy(True)
        # clas = self._parent.dataSource.getEventClassification(self._parent.currentID)
        clas = self._parent.classifications.loc[self._parent.currentID, 'classification']
        print("classification: ", clas)
        if clas == 'OVER':
            self._ui.rbOverdense.setChecked(True)
        if clas == 'UNDER':
            self._ui.rbUnderdense.setChecked(True)
        if clas == 'HI LOS':
            self._ui.rbLOSfilter.setChecked(True)
        if clas == 'FAKE ESD':
            self._ui.rbFakeEsd.setChecked(True)
        if clas == 'FAKE CAR1':
            self._ui.rbFakeCar1.setChecked(True)
        if clas == 'FAKE CAR2':
            self._ui.rbFakeCar2.setChecked(True)
        if clas == 'FAKE SAT':
            self._ui.rbFakeSat.setChecked(True)
        if clas == 'FAKE LONG':
            self._ui.rbFakeLong.setChecked(True)
        self._parent.busy(False)

    def _changeClassification(self):
        self._parent.busy(True)
        changed = False
        if self._ui.rbOverdense.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'OVER'
            changed = True

        if self._ui.rbUnderdense.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'UNDER'
            changed = True

        if self._ui.rbLOSfilter.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'HI LOS'
            changed = True

        if self._ui.rbFakeEsd.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'FAKE ESD'
            changed = True

        if self._ui.rbFakeCar1.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'FAKE CAR1'
            changed = True

        if self._ui.rbFakeCar2.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'FAKE CAR2'
            changed = True

        if self._ui.rbFakeSat.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'FAKE SAT'
            changed = True

        if self._ui.rbFakeLong.isChecked():
            self._parent.classifications.loc[self._parent.currentID, 'classification'] = 'FAKE LONG'
            changed = True

        if changed:
            # fix bug currentId out of range
            self._parent.classChanges[self._parent.currentID] = True
            self._ui.pbSave.setEnabled(True)

        self._parent.busy(False)

    def _getClassFilter(self):
        self._parent.busy(True)
        self._classFilter = self._settings.readSettingAsString('classFilter')
        idx = 0
        for tag in self._parent.filterTags:
            isCheckTrue = tag in self._classFilter
            self._parent.filterChecks[idx].setChecked(isCheckTrue)
            idx += 1
        self._parent.busy(False)

    def _setClassFilter(self):
        self._parent.busy(True)
        classFilter = ''
        idx = 0
        for check in self._parent.filterChecks:
            if check.isChecked():
                classFilter += self._parent.filterTags[idx] + ','
            idx += 1

        if classFilter != '':
            self._classFilter = classFilter[0:-1]  # discards latest comma+space
        else:
            self._classFilter = ''

        self._settings.writeSetting('classFilter', self._classFilter)
        self._parent.busy(False)

    def _findEvent(self, evId):
        """

        :param date:
        :param evId:
        :param dailyNr:
        :return:
        """

        # deselect the current event in case it's no more visibile due
        # to a change of filtering or date out of coverage
        self._parent.filteredIDs, self._parent.filteredDailies = \
            self._parent.dataSource.getFilteredIDsOfTheDay(self._parent.currentDate, self._classFilter)
        if len(self._parent.filteredIDs) == 0:
            self._parent.filteredIDs = []
            self._parent.filteredDailies = []

        if self._parent.filteredIDs == [] or self._parent.currentID not in self._parent.filteredIDs:
            self._parent.currentIndex = -1
            self._parent.currentID = 0
            self._parent.currentDailyNr = 0
            self._ui.lbID.setText('Nothing selected')
            self._ui.lbDaily.setText('------')
            self._ui.lbThisDay.setText('------')
            self._ui.twShots.setTabEnabled(self.SSTW_DETAILS, False)
            print("no filtered events to show")
            return

        # if ok, selects the correct row
        pandasModel = self._ui.tvChrono.model()
        proxy = QSortFilterProxyModel()
        proxy.setSourceModel(pandasModel)
        evIdStr = str(evId)
        proxy.setFilterKeyColumn(0)
        proxy.setFilterFixedString(evIdStr)
        # now the proxy only contains rows that match the given evId (must be only one)
        matchingIndex = proxy.mapToSource(proxy.index(0, 0))
        if matchingIndex.isValid():
            self._ui.tvChrono.scrollTo(matchingIndex, QAbstractItemView.EnsureVisible)
            selModel = self._ui.tvChrono.selectionModel()
            selModel.select(matchingIndex, QItemSelectionModel.Select|QItemSelectionModel.Rows)
            self._selectEvent(0)


    def _selectEvent(self, idx):
        # called when the user clicks on a chrono table row
        # gets the indexes of all the selected cells in the clicked row
        modelIndexList = self._ui.tvChrono.selectedIndexes()
        if len(modelIndexList) > 0:
            # the event Id is in the first (leftmost) cell
            cellIndex = modelIndexList[0]
            pandasModel = cellIndex.model()
            cId = pandasModel.data(cellIndex, Qt.DisplayRole)
            if cId is not None:
                self._ui.lbID.setText("ID#"+cId)
                cId = int(cId)
                self._parent.currentID = cId
                # its daily number is in the second cell
                cellIndex = modelIndexList[1]
                cDaily = pandasModel.data(cellIndex, Qt.DisplayRole)
                if cDaily is not None:
                    self._ui.lbDaily.setText("Daily#"+cDaily)
                    cDaily = int(cDaily)
                    self._parent.currentDailyNr = cDaily
                    # finally, its date is in the third cell
                    cellIndex = modelIndexList[2]
                    cDate = pandasModel.data(cellIndex, Qt.DisplayRole)
                    if cDate is not None:
                        self._ui.lbThisDay.setText(cDate)
                        self._parent.currentDate = cDate
                        # if self.getDailyCoverage():
                        # self.refresh(0, True)
                        self._parent.updateStatusBar(
                            "Selected ID: {},  the event {} of day: {}".format(
                                self._parent.currentID, self._parent.currentDailyNr, self._parent.currentDate))
                        self._settings.writeSetting('currentDate', self._parent.currentDate)

                        self._parent.filteredIDs, self._parent.filteredDailies = \
                            self._parent.dataSource.getFilteredIDsOfTheDay(self._parent.currentDate, self._classFilter)
                        if len(self._parent.filteredIDs) == 0:
                            self._parent.filteredIDs = []
                            self._parent.filteredDailies = []

                        if self._parent.filteredIDs == [] or self._parent.currentID not in self._parent.filteredIDs:
                            self._parent.currentIndex = -1
                            self._parent.currentID = 0
                            self._parent.currentDailyNr = 0
                            self._ui.lbID.setText('Nothing selected')
                            self._ui.lbDaily.setText('------')
                            self._ui.lbThisDay.setText('------')
                            print("no filtered events to show")
                            return

                        # index in list of filtered IDs
                        try:
                            self._parent.currentIndex = self._parent.filteredIDs.index(self._parent.currentID)
                        except (IndexError, ValueError):
                            self._parent.currentIndex = -1

                        # update data bar
                        df = self._parent.dataSource.getEventData(self._parent.currentID)
                        self._ui.lbShotFilename.setText(str(df.iloc[21, 2]))
                        self._ui.lbTime.setText(df.iloc[0, 0])  # utc_time,RAISE
                        self._ui.lbLasting.setText(str(df.iloc[10, 2] / 1000) + " s")  # lasting_ms,FALL
                        self._ui.lbClass.setText(df.iloc[20, 2])  # classification,FALL
                        self._ui.lbDaily.setText('Daily# ' + str(self._parent.currentDailyNr))

                        # checks if the current event carries image data
                        eventHasShots = False
                        eventHasDumps = False
                        shotName, shotBytes, dailyNr, utcDate = self._parent.dataSource.extractShotData(cId)
                        if shotName is not None:
                            eventHasShots = True

                        dumpName, dumpBytes, dailyNr, utcDate = self._parent.dataSource.extractDumpData(cId)
                        if dumpName is not None:
                            eventHasDumps = True

                        self._ui.twShots.setTabEnabled(self.SSTW_THUMBNAILS, eventHasShots)
                        self._ui.twShots.setTabEnabled(self.SSTW_SSHOT, eventHasShots)
                        self._ui.twShots.setTabEnabled(self.SSTW_POWER, eventHasDumps)
                        self._ui.twShots.setTabEnabled(self.SSTW_CMAP, eventHasDumps)
                        self._ui.twShots.setTabEnabled(self.SSTW_3D, eventHasDumps)
                        self._ui.twShots.setTabEnabled(self.SSTW_DETAILS, self._parent.currentID > 0)

    def _refreshPressed(self, checked):
        if self._ui.twShots.currentIndex() == self.SSTW_THUMBNAILS:
            self._parent.busy(True)
            self._parent.updateStatusBar("Filtering daily events by classification: {}".format(self._classFilter))
            self.refresh(self._parent.currentIndex, True)
            self._selectEvent(0)
            self._parent.busy(False)
        else:
            # self.refresh(self._parent.currentIndex, False)
            self.updateTabEvents()

        if self._ui.twShots.currentIndex() == self.SSTW_3D:
            self._azimuth = self._plot.getAzimuth()
            self._elevation = self._plot.getElevation()

    def _sidePressed(self, checked):
        self._sideIdx += 1
        if self._sideIdx >= len(self._sides):
            self._sideIdx = 0
        self._ui.lbSide.setText(self._sides[self._sideIdx])
        self._elevation = self._aspects[self._sideIdx][0]
        self._azimuth = self._aspects[self._sideIdx][1]
        self._ui.lbAzimuth.setNum(self._azimuth)
        self._ui.hsAzimuth.setValue(self._azimuth)
        self._ui.lbElevation.setNum(self._elevation)
        self._ui.hsElevation.setValue(self._elevation)
        self._plot.rotate(self._azimuth, self._elevation)
        print("{} current azimuth:{}°, elevation:{}°".format(self._sideIdx, self._azimuth, self._elevation))

    def _resetPressed(self, checked):
        self._linkedSliders = False
        self._settings.writeSetting('linkedSliders', self._linkedSliders)
        self._ui.chkLinked.setChecked(self._linkedSliders)
        self._ui.hsVmin.setValue(self._settings.DBFS_RANGE_MIN)
        self._ui.hsVmax.setValue(self._settings.DBFS_RANGE_MAX)
        self._ui.hsHzoom.setValue(int(self._settings.ZOOM_DEFAULT * 10))
        self._ui.hsVzoom.setValue(int(self._settings.ZOOM_DEFAULT * 10))
        self._refreshPressed(True)

    def refresh(self, selectIndex=-1, doReload=True):
        if self._parent.dataSource is None:
            return

        self._parent.filteredIDs, self._parent.filteredDailies = \
            self._parent.dataSource.getFilteredIDsOfTheDay(self._parent.currentDate, self._classFilter)
        if len(self._parent.filteredIDs) == 0 or selectIndex == -1:
            self._parent.filteredIDs = []
            self._parent.filteredDailies = []
            self._parent.currentIndex = -1
            self._parent.currentID = 0
            self._parent.currentDailyNr = 0
            if self._tbs is not None:
                self._tbs.reloadDailyThumbs()
        else:
            self._parent.currentIndex = selectIndex
            try:
                self._parent.currentID = self._parent.filteredIDs[self._parent.currentIndex]
                self._parent.currentDailyNr = self._parent.filteredDailies[self._parent.currentIndex]

            except IndexError:
                self._parent.currentID = 0
                self._parent.currentDailyNr = 0
                self._ui.lbID.setText('Nothing selected')
                self._ui.lbDaily.setText('------')
                self._ui.lbThisDay.setText('------')
                print("no filtered events to show as thumbnail")

            if self._tbs is not None and doReload:
                self._tbs.reloadDailyThumbs()

    def _toggleCheckAll(self):
        self._ui.chkOverdense.setChecked(self._ui.chkAll.isChecked())
        self._ui.chkUnderdense.setChecked(self._ui.chkAll.isChecked())
        self._ui.chkFakeEsd.setChecked(self._ui.chkAll.isChecked())
        self._ui.chkFakeCar1.setChecked(self._ui.chkAll.isChecked())
        self._ui.chkFakeCar2.setChecked(self._ui.chkAll.isChecked())
        self._ui.chkFakeSat.setChecked(self._ui.chkAll.isChecked())
        self._ui.chkFakeLong.setChecked(self._ui.chkAll.isChecked())
        self._ui.chkLOSfilter.setChecked(self._ui.chkAll.isChecked())
        self._setClassFilter()

    def _changePlotVmin(self, newValue):
        if self._plotVmax > newValue:
            delta = (newValue - self._plotVmin)
            # if self._linkedSliders:
            #     if (self._plotVmax + delta) > self.DBFS_RANGE_MAX:
            #         self._plotVmax = self.DBFS_RANGE_MAX
            #         self._ui.hsVmin.setValue(self._plotVmin)
            #         newValue = self._plotVmin
            #     else:
            #         self._plotVmax += delta
            self._plotVmin = newValue
            self._ui.lbVmin.setText("{} dBfs".format(self._plotVmin))
            self._ui.lbVmax.setText("{} dBfs".format(self._plotVmax))
            self._ui.hsVmax.setValue(self._plotVmax)
        else:
            self._ui.hsVmin.setValue(self._plotVmin)

    def _changePlotVmax(self, newValue):
        if self._plotVmin < newValue:
            delta = (newValue - self._plotVmax)

            # if self._linkedSliders:
            #     if (self._plotVmin + delta) < self.DBFS_RANGE_MIN:
            #         self._plotVmin = self.DBFS_RANGE_MIN
            #         self._ui.hsVmax.setValue(self._plotVmax)
            #         newValue = self._plotVmax
            #     else:
            #         self._plotVmin += delta
            self._plotVmax = newValue
            self._ui.lbVmin.setText("{} dBfs".format(self._plotVmin))
            self._ui.lbVmax.setText("{} dBfs".format(self._plotVmax))
            self._ui.hsVmin.setValue(self._plotVmin)
        else:
            self._ui.hsVmax.setValue(self._plotVmax)

    def _changeHzoom(self, newValue):
        self._ui.hsVzoom.blockSignals(True)
        newValue /= 10
        delta = (newValue - self._hZoom)
        if self._linkedSliders:
            if self._settings.ZOOM_MIN <= (self._vZoom + delta) <= self._settings.ZOOM_MAX:
                self._vZoom += delta
            elif (self._vZoom + delta) < self._settings.ZOOM_MIN:
                self._vZoom = self._settings.ZOOM_MIN
            elif (self._vZoom + delta) > self._settings.ZOOM_MAX:
                self._vZoom = self._settings.ZOOM_MAX

        self._hZoom = newValue
        self._settings.writeSetting('horizontalZoom', self._hZoom)
        self._ui.hsVzoom.setValue(int(self._vZoom * 10))
        self._ui.lbHzoom.setText("{} X".format(self._hZoom))
        self._ui.lbVzoom.setText("{} X".format(self._vZoom))
        if self._plot is not None:
            inchWidth, inchHeight = self._calcFigSizeInch(self._container)
            canvas = self._plot.widget()
            canvas.resize(self._pixWidth, self._pixHeight)
            self._plot.zoom(inchWidth, inchHeight)
        else:
            self.updateTabEvents()

        if self._currentObj is not None:
            self._currentObj.ensureVisible(int(self._pixWidth / 2), int(self._pixHeight / 2))
        self._ui.hsVzoom.blockSignals(False)

    def _changeVzoom(self, newValue):
        self._ui.hsHzoom.blockSignals(True)
        newValue /= 10
        delta = (newValue - self._vZoom)
        if self._linkedSliders:
            if self._settings.ZOOM_MIN <= (self._hZoom + delta) <= self._settings.ZOOM_MAX:
                self._hZoom += delta
            elif (self._hZoom + delta) < self._settings.ZOOM_MIN:
                self._hZoom = self._settings.ZOOM_MIN
            elif (self._hZoom + delta) > self._settings.ZOOM_MAX:
                self._hZoom = self._settings.ZOOM_MAX
            self._ui.hsHzoom.setValue(int(self._hZoom * 10))

        self._vZoom = newValue
        self._settings.writeSetting('verticalZoom', self._vZoom)
        self._ui.lbHzoom.setText("{} X".format(self._hZoom))
        self._ui.lbVzoom.setText("{} X".format(self._vZoom))

        if self._plot is not None:
            inchWidth, inchHeight = self._calcFigSizeInch(self._container)
            canvas = self._plot.widget()
            # canvas.resize(QSize(self._pixWidth, self._pixHeight))
            canvas.resize(self._pixWidth, self._pixHeight)
            self._plot.zoom(inchWidth, inchHeight)
        else:
            self.updateTabEvents()

        if self._currentObj is not None:
            self._currentObj.ensureVisible(int(self._pixWidth / 2), int(self._pixHeight / 2))
        self._ui.hsHzoom.blockSignals(False)

    def _changeAzimuth(self, newValue):
        self._azimuth = self._plot.getAzimuth()
        self._elevation = self._plot.getElevation()
        if self._azimuth != newValue:
            self._azimuth = newValue
            self._settings.writeSetting('3Dazimuth', self._azimuth)
            self._ui.lbAzimuth.setText("{}°".format(self._azimuth))
            self._plot.rotate(self._azimuth, self._elevation)

    def _changeElevation(self, newValue):
        self._azimuth = self._plot.getAzimuth()
        self._elevation = self._plot.getElevation()
        if self._elevation != newValue:
            self._elevation = newValue
            self._settings.writeSetting('3Delevation', self._elevation)
            self._ui.lbElevation.setText("{}°".format(self._elevation))
            self._plot.rotate(self._azimuth, self._elevation)

    def _toggleLinkedCursors(self, state):
        self._linkedSliders = (state != 0)
        self._settings.writeSetting('linkedCursors', self._linkedSliders)

    def _toggleGrid(self, state):
        self._showGrid = (state != 0)
        self._settings.writeSetting('showGrid', self._showGrid)

    def _cmapChanged(self, newCmapName):
        self._currentColormap = newCmapName
        self._settings.writeSetting('currentColormap', self._currentColormap)
        print("selected colormap: ", newCmapName)

    def _plotSettingsEnable(self, enable=True):
        self._ui.gbPlotSettings.setVisible(enable)

    def _vMinMaxEnable(self, enable=True):
        self._ui.hsVmin.setVisible(enable)
        self._ui.hsVmax.setVisible(enable)
        self._ui.lbVmin.setVisible(enable)
        self._ui.lbVmax.setVisible(enable)
        self._ui.lbTxtVmin.setVisible(enable)
        self._ui.lbTxtVmax.setVisible(enable)
        self._ui.lbTxtPowerRange.setVisible(enable)
        self._ui.lbPowerFrom.setVisible(enable)
        self._ui.lbPowerTo.setVisible(enable)
        self._ui.lbTxtToPower.setVisible(enable)
        self._ui.lbTxtDbfs.setVisible(enable)
        self._ui.lbTxtVrange.setVisible(enable)

    def _3dEnable(self, enable=True):
        self._ui.gb3Dview.setVisible(enable)
        # self._ui.chkLinked.setChecked(enable)
        # self._ui.chkLinked.setEnabled(not enable)
        # self._linkedSliders = enable

    def _cmapEnable(self, enable=True):
        self._ui.cbCmaps.setVisible(enable)
        self._ui.lbCmap.setVisible(enable)

    def _calcFigSizeInch(self, container: QWidget):
        self._container = container
        containerWidth = container.width()
        containerHeight = container.height()
        self._pixWidth = int(containerWidth * self._hZoom)
        self._pixHeight = int(containerHeight * self._vZoom)
        if self._pixWidth > 65535:
            self._pixWidth = 65535
        if self._pixHeight > 65535:
            self._pixHeight = 65535
        inchWidth = self._pixWidth / self._px
        inchHeight = self._pixHeight / self._px
        return inchWidth, inchHeight

    def _exportPressed(self, checked):
        self._parent.checkExportDir(self._exportDir)
        if self._ui.twShots.currentIndex() == self.SSTW_CHRONO:
            # chronological events table
            if self._dfChrono is not None:
                os.chdir(self._exportDir)
                filename = "chronological_{}_to_{}.csv".format(self._parent.fromDate, self._parent.toDate)
                # since dfChrono is a mixed numeric/text table, to_csv() cannot convert
                # the decimal point, so we need to convert all dfChrono cells to string values
                # and then replace the dot with comma if required before saving as csv
                self._dfChrono = self._dfChrono.astype(str)
                if self._settings.decimalPoint() == ',':
                    # european decimal separator
                    self._dfChrono = self._dfChrono.applymap(self._replaceDecimalPoint)
                self._dfChrono.to_csv(filename, sep=self._settings.dataSeparator(),
                                      decimal=self._settings.decimalPoint())

                defaultComment = "chronological table of events, covering from {} to {}".format(self._parent.fromDate,
                                                                                                self._parent.toDate)

                comment = QInputDialog.getMultiLineText(self._parent, "Export chronological table",
                                                        "Comment\n(please enter further considerations, if needed):",
                                                        defaultComment)
                self._parent.busy(True)
                if len(comment[0]) > 0:
                    title = filename.replace('.csv', '')
                    commentsName = 'comments_' + title + '.txt'
                    with open(commentsName, 'w') as txt:
                        txt.write(comment[0])
                        txt.close()
                        self._parent.updateStatusBar("Exported  {}".format(commentsName))
                        self._ui.lbCommentsFilename.setText(commentsName)

                os.chdir(self._parent.workingDir)

        elif self._ui.twShots.currentIndex() == self.SSTW_THUMBNAILS:
            # the export is related to all the screenshots listed as thumbnails
            # and their DAT files if the related box is checked
            os.chdir(self._exportDir)
            count = 0
            for id in self._parent.filteredIDs:
                shotName, shotData, dailyNr, utcDate = self._parent.dataSource.extractShotData(id)
                if shotName is not None and shotData is not None:
                    with open(shotName, 'wb') as png:
                        png.write(shotData)
                        png.close()
                        self._parent.updateStatusBar("Exported  {}".format(shotName))
                        count += 1
                if self._ui.chkDatExport.isChecked():
                    datName, datData, dailyNr, utcDate = self._parent.dataSource.extractDumpData(id)
                    if datName is not None and datData is not None:
                        with open(datName, 'wb') as dat:
                            dat.write(datData)
                            dat.close()
                            self._parent.updateStatusBar(" Exported  {}".format(datName))

            if self._ui.chkDatExport.isChecked():
                self._parent.infoMessage("Ebrow", "Exported {} screenshot files and related data".format(count))
            else:
                self._parent.infoMessage("Ebrow", "Exported {} screenshot files".format(count))
            os.chdir(self._parent.workingDir)

        elif self._ui.twShots.currentIndex() == self.SSTW_SSHOT:
            # exports the displayed screenshot and its DAT file if the related box is checked
            os.chdir(self._exportDir)
            shotName, shotData, dailyNr, utcDate = self._parent.dataSource.extractShotData(self._parent.currentID)
            if shotName is not None and shotData is not None:
                with open(shotName, 'wb') as png:
                    png.write(shotData)
                    png.close()
                    self._parent.updateStatusBar("Exported  {}".format(shotName))
                if self._ui.chkDatExport.isChecked():
                    datName, datData, dailyNr, utcDate = self._parent.dataSource.extractDumpData(self._parent.currentID)
                    if datName is not None and datData is not None:
                        with open(datName, 'wb') as dat:
                            dat.write(datData)
                            dat.close()
                            self._parent.updateStatusBar(" Exported  {}".format(datName))

                self._parent.busy(False)
                defaultComment = "{}, event#{} screenshot".format(utcDate, dailyNr)

                comment = QInputDialog.getMultiLineText(self._parent, "Export screenshot",
                                                        "Comment\n(please enter further considerations, if needed):",
                                                        defaultComment)
                self._parent.busy(True)
                if len(comment[0]) > 0:
                    title = shotName.replace('.png', '')
                    commentsName = 'comments_' + title + '.txt'
                    with open(commentsName, 'w') as txt:
                        txt.write(comment[0])
                        txt.close()
                        self._parent.updateStatusBar("Exported  {}".format(commentsName))
                        self._ui.lbCommentsFilename.setText(commentsName)
            os.chdir(self._parent.workingDir)
        elif self._ui.twShots.currentIndex() == self.SSTW_DETAILS:
            # event details table
            if self._dfDetails is not None:
                os.chdir(self._exportDir)
                filename = self._ui.lbShotFilename.text()
                filename = filename.replace('.png', '.csv')
                filename = filename.replace('autoshot_', 'details_')

                shotName, shotData, dailyNr, utcDate = self._parent.dataSource.extractShotData(self._parent.currentID)

                # since dfDetails is a mixed numeric/text table, to_csv() cannot convert
                # the decimal point, so we need to convert all dfDetails cells to string values
                # and then replace the dot with comma if required before saving as csv
                self._dfDetails = self._dfDetails.astype(str)
                if self._settings.decimalPoint() == ',':
                    # european decimal separator
                    self._dfDetails = self._dfDetails.applymap(self._replaceDecimalPoint)
                self._dfDetails.to_csv(filename, sep=self._settings.dataSeparator(),
                                       decimal=self._settings.decimalPoint())

                defaultComment = "{}, event#{} details".format(utcDate, dailyNr)

                comment = QInputDialog.getMultiLineText(self._parent, "Export event details",
                                                        "Comment\n(please enter further considerations, if needed):",
                                                        defaultComment)
                self._parent.busy(True)
                if len(comment[0]) > 0:
                    title = filename.replace('.csv', '')
                    commentsName = 'comments_' + title + '.txt'
                    with open(commentsName, 'w') as txt:
                        txt.write(comment[0])
                        txt.close()
                        self._parent.updateStatusBar("Exported  {}".format(commentsName))
                        self._ui.lbCommentsFilename.setText(commentsName)

                os.chdir(self._parent.workingDir)

        else:
            os.chdir(self._exportDir)
            filename = self._ui.lbShotFilename.text()
            prefixes = [None, None, None, 'power_profile', 'image2d', 'image3d', None]
            headings = [None, None, None, "Power profile", "2D power plot", "3D power plot", None]

            prefix = prefixes[self._ui.twShots.currentIndex()]

            if prefix is not None:
                heading = headings[self._ui.twShots.currentIndex()]

                datName, datData, dailyNr, utcDate = self._parent.dataSource.extractDumpData(self._parent.currentID)
                defaultComment = "{} of event {}, detected on {}\n".format(heading, dailyNr, utcDate)
                min, max = self._plot.getMinMax()
                defaultComment += "Total dynamic range from {} to {} dBfs\n".format(min, max)
                defaultComment += "Visible dynamic range from {} to {} dBfs\n".format(self._plotVmin, self._plotVmax)
                defaultComment += "Horizontal zoom: {}X, vertical zoom: {}X\n".format(self._hZoom, self._vZoom)
                defaultComment += "Colormap used: {}\n".format(self._ui.cbCmaps.currentText())
                if prefix == 'image3d':
                    defaultComment += "Azimuth: {}°, Elevation: {}°\n".format(self._azimuth, self._elevation)
                    defaultComment += "Visible planes: {}\n".format(self._sides[self._sideIdx])

                # exports the displayed diagram and its DAT file if the related box is checked
                title = filename.replace('dump', prefix)
                filename = title.replace('.dat', '.png')
                title = title.replace('.dat', '')
                self._plot.saveToDisk(filename)
                self._parent.updateStatusBar("Exported  {}".format(filename))
                if self._ui.chkDatExport.isChecked():

                    if datName is not None and datData is not None:
                        datName = datName.replace('dump', prefix)
                        self._plot.savePlotDataToDisk(datName)
                        self._parent.updateStatusBar(" Exported  {}".format(datName))

                self._parent.busy(False)
                comment = QInputDialog.getMultiLineText(self._parent, "Export {}".format(prefix),
                                                        "Comment\n(please enter further considerations, if needed):",
                                                        defaultComment)
                self._parent.busy(True)
                if len(comment[0]) > 0:
                    commentsName = 'comments_' + title + '.txt'
                    with open(commentsName, 'w') as txt:
                        txt.write(comment[0])
                        txt.close()
                        self._parent.updateStatusBar("Exported  {}".format(commentsName))
                        self._ui.lbCommentsFilename.setText(commentsName)
            os.chdir(self._parent.workingDir)

        self._parent.busy(False)

    def _replaceDecimalPoint(self, cell):
        if '.PNG' in cell or '.DAT' in cell or '.png' in cell or '.dat' in cell:
            return cell
        return cell.replace('.', ',')
