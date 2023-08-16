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
import calendar
import os
import re
import os.path
import time
from pathlib import Path
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QHBoxLayout, QScrollArea, QSpacerItem, QSizePolicy, QInputDialog
from PyQt5.QtCore import Qt

# from .mainwindow import MainWindow
from .nestedpie import NestedPie
from .heatmap import Heatmap
from .hm_rmob import HeatmapRMOB
from .bg_rmob import BargraphRMOB
from .bargraph import Bargraph
from .statplot import StatPlot
from .pandasmodel import PandasModel
from .utilities import notice, cryptDecrypt, mkExportFolder
from .logprint import print, fprint

class Stats:
    STTW_TABLES = 0
    STTW_DIAGRAMS = 1

    TAB_DAILY_BY_DAY = 0
    TAB_DAILY_BY_HOUR = 1
    TAB_DAILY_BY_10M = 2
    TAB_SESSIONS_REGISTER = 3
    TAB_RMOB_MONTH = 4

    GRAPH_PLOT = 0
    GRAPH_HEATMAP = 1
    GRAPH_BARS = 2
    GRAPH_PIE = 3

    filterDesc = {'OVER': "Overdense event", 'UNDER': "Underdense event",
                  'FAKE ESD': "Fake event (ESD)", 'FAKE CAR1': "Fake event (Carrier#1)",
                  'FAKE CAR2': "Fake event (Carrier#2)", 'FAKE SAT': "Fake event (Saturation)",
                  'FAKE LONG': "Event lasting too long", 'HI LOS': 'Headed echo',
                  "ACQ ACT": "Acquisition active"}

    def __init__(self, parent, ui, settings):
        self._bakClass = None
        self._ui = ui
        self._parent = parent
        self._settings = settings
        self._dataSource = None
        self._diagram = None
        self._plot = None
        self._spacer = None
        self._RMOBupdating = False
        self._classFilter = ''
        self._classFilterRMOB = "OVER,UNDER,ACQ ACT"
        self._zoom = 1.0
        self._dataFrame = None
        self._exportDir = Path(self._parent.exportDir, "statistics")
        mkExportFolder(self._exportDir)
        self._currentColormap = self._settings.readSettingAsString('currentColormapStat')
        self._RMOBclient = self._settings.readSettingAsString('RMOBclient')
        self._ui.cbCmaps_2.setCurrentText(self._currentColormap)
        self._showValues = self._settings.readSettingAsBool('showValues')
        self._ui.chkShowValues.setChecked(self._showValues)

        self._showGrid = self._settings.readSettingAsBool('showGridStat')
        self._ui.chkGrid_2.setChecked(self._showGrid)
        self._getClassFilter()
        self._ui.lwTabs.setCurrentRow(0)
        self._ui.lwDiags.setCurrentRow(0)

        self._ui.chkOverdense_2.clicked.connect(self._setClassFilter)
        self._ui.chkUnderdense_2.clicked.connect(self._setClassFilter)
        self._ui.chkFakeEsd_2.clicked.connect(self._setClassFilter)
        self._ui.chkFakeCar1_2.clicked.connect(self._setClassFilter)
        self._ui.chkFakeCar2_2.clicked.connect(self._setClassFilter)
        self._ui.chkFakeSat_2.clicked.connect(self._setClassFilter)
        self._ui.chkFakeLong_2.clicked.connect(self._setClassFilter)
        self._ui.chkLOSfilter_2.clicked.connect(self._setClassFilter)
        self._ui.chkAcqActive_2.clicked.connect(self._setClassFilter)
        self._ui.chkAll_2.clicked.connect(self._toggleCheckAll)
        self._ui.lwTabs.currentRowChanged.connect(self._tabChanged)
        self._ui.pbRefresh_2.clicked.connect(self._updateTabGraph)

        self._ui.twStats.currentChanged.connect(self.updateTabStats)
        self._ui.cbCmaps_2.textActivated.connect(self._cmapChanged)
        self._ui.twStats.currentChanged.connect(self._updateTabGraph)
        self._ui.pbStatTabExp.clicked.connect(self._exportPressed)
        self._ui.pbRMOB.clicked.connect(self.updateRMOBfiles)
        self._ui.chkGrid_2.clicked.connect(self._toggleGrid)
        self._ui.chkShowValues.clicked.connect(self._toggleValues)
        self._showDiagramSettings(False)
        self._showColormapSetting(False)

    def updateTabStats(self):
        if self._ui.twMain.currentIndex() == self._parent.TWMAIN_STATISTICS:
            if self._ui.twStats.currentIndex() == self.STTW_TABLES:
                self._ui.lwDiags.hide()
                # self._ui.pbRMOB.setVisible(True)
                self._showDiagramSettings(False)

            if self._ui.twStats.currentIndex() == self.STTW_DIAGRAMS:
                self._ui.lwDiags.show()
                self._showDiagramSettings(True)
            self._updateTabGraph()

    def updateSummaryPlot(self, filters: str):
        self._parent.busy(True)
        os.chdir(self._parent.workingDir)
        self._bakClass = self._classFilter
        self._classFilter = filters
        self._ui.lwTabs.setCurrentRow(self.TAB_DAILY_BY_DAY)
        self._ui.lwDiags.setCurrentRow(self.GRAPH_PLOT)
        self._ui.twStats.setCurrentIndex(self.STTW_DIAGRAMS)
        self.showDataDiagram()
        self._classFilter = self._bakClass

        # title = self._ui.lwTabs.currentItem().text()
        # title = title.lower().replace(' ', '_')
        title = 'summary_by_day'
        className = type(self._plot).__name__
        pngName = 'stat-' + title + '-' + className + '.png'
        self._plot.saveToDisk(pngName)
        self._parent.updateStatusBar("Generated  {}".format(pngName))
        self._ui.lbStatFilename.setText(pngName)
        self._parent.busy(False)
        return pngName

    def updateRMOBfiles(self, sendOk: bool = True):
        self._parent.busy(True)
        os.chdir(self._parent.workingDir)
        self._RMOBupdating = True
        self._dataSource = self._parent.dataSource
        self._ui.twStats.setCurrentIndex(self.STTW_TABLES)
        df = self._dataSource.getADpartialFrame(self._parent.fromDate, self._parent.toDate)

        df2 = self._dataSource.makeDaily(df, self._parent.fromDate, self._parent.toDate, dtRes='H',
                                         filters=self._classFilterRMOB, totalRow=False, totalColumn=False)

        dfRMOB, monthNr, year = self._dataSource.makeRMOB(df2, lastOnly=True)
        filePrefix, txtFileName, dfMonth = self._generateRMOBtableFile(dfRMOB, year, monthNr)

        # the files prefix is stored for reporting purposes
        self._settings.writeSetting('RMOBfilePrefix', filePrefix)

        self._ui.lwTabs.setCurrentRow(self.TAB_RMOB_MONTH)
        self._ui.lwDiags.setCurrentRow(self.GRAPH_HEATMAP)
        self._ui.twStats.setCurrentIndex(self.STTW_DIAGRAMS)
        self.showDataDiagram()
        heatmapFileName = self._generateRMOBgraphFile()
        
        self._ui.lwDiags.setCurrentRow(self.GRAPH_BARS)
        self.showDataDiagram()
        bargraphFileName = self._generateRMOBgraphFile()

        # the heatmap, having aspect ratio about squared
        # does not need to cut away the padding
        hmPix = QPixmap(heatmapFileName).scaled(300, 220, transformMode=Qt.SmoothTransformation)
        hmPix.save("heatmap.jpg")

        # the bargraph instead is half-tall and the padding above
        # and below the graph must be cut away, so the height
        # is scaled taller than needed, to be cut away while drawing
        barPix = QPixmap(bargraphFileName).scaled(260, 110,
                                                  transformMode=Qt.SmoothTransformation)
        barPix.save("bargraph.jpg")

        logoPix = QPixmap(":/echoes_transparent").scaled(48, 48, transformMode=Qt.SmoothTransformation)
        # logoPix = QPixmap(":/rts").scaled(48, 48, transformMode=Qt.SmoothTransformation)
        nf = QFont('Arial', 9, -1, False)
        bf = QFont('Arial', 9, 200, True)
        pixRMOB = QPixmap(700, 220)
        pixRMOB.fill(Qt.white)
        p = QPainter()
        if p.begin(pixRMOB):
            p.drawPixmap(400, 0, hmPix)
            p.drawPixmap(100, 110, barPix)
            p.setPen(Qt.black)

            p.setFont(bf)

            x = 5
            p.drawText(x, 15, "Observer: ")
            p.drawText(x, 30, "Country: ")
            p.drawText(x, 45, "City: ")
            p.drawText(x, 60, "Antenna: ")
            p.drawText(x, 75, "RF preamp: ")
            p.drawText(x, 90, "Obs.Method: ")
            p.drawText(x, 105, "Computer: ")

            x = 200
            p.drawText(x, 15, "Location: ")
            p.drawText(x, 30, "          ")
            p.drawText(x, 45, "Frequency: ")
            p.drawText(x, 60, "Az.:")
            p.drawText(x + 70, 60, "El.:")
            p.drawText(x, 75, "Receiver: ")

            p.setFont(nf)
            x = 90
            p.drawText(x, 15, "{}".format(self._settings.readSettingAsString('owner')[:16]))
            p.drawText(x, 30, "{}".format(self._settings.readSettingAsString('country')[:16]))
            p.drawText(x, 45, "{}".format(self._settings.readSettingAsString('city')[:20]))
            p.drawText(x, 60, "{}".format(self._settings.readSettingAsString('antenna')[:16]))
            p.drawText(x, 75, "{}".format(self._settings.readSettingAsString('preamplifier')[:15]))
            p.drawText(x, 90, "{}".format("Echoes 0.51++ Data Browser v.{}").format(self._parent.version))
            p.drawText(x, 105, "{}".format(self._settings.readSettingAsString('computer')[:50]))

            x = 275
            p.drawText(x, 15, "{}".format(self._settings.readSettingAsString('longitude')[:12]))
            p.drawText(x, 30, "{}".format(self._settings.readSettingAsString('latitude')[:12]))
            p.drawText(x, 45, "{} Hz".format(self._settings.readSettingAsString('frequencies')[:14]))
            p.drawText(x - 40, 60, "{}°".format(self._settings.readSettingAsString('antAzimuth')))
            p.drawText(x + 20, 60, "{}°".format(self._settings.readSettingAsString('antElevation')))
            p.drawText(x, 75, "{}".format(self._settings.readSettingAsString('receiver')[:18]))

           
            p.setFont(bf)
            ts = time.strptime(self._parent.toDate, "%Y-%m-%d")
            headDate = time.strftime("%B %d, %Y", ts)
            p.drawText(10, 130, headDate)
            p.drawText(10, 145, "Hourly counts:")
            p.drawPixmap(10, 160, logoPix)
            p.end()

            # os.chdir(self._exportDir)
            os.chdir(self._parent.workingDir)
            jpgFileName = filePrefix + ".jpg"
            if pixRMOB.save(jpgFileName):
                print("{} generated".format(jpgFileName))
                if self._RMOBclient != 'UNKNOWN' and len(self._RMOBclient) > 0:
                    goSend = False
                    if sendOk:
                        if self._parent.batchRMOB:
                            goSend = True
                        elif self._parent.confirmMessage("RMOB data generation", "Send these data to RMOB ftp server?"):
                            goSend = True

                        if goSend and sendOk:
                            cmd = "{} {} {}".format(self._RMOBclient, txtFileName, jpgFileName)
                            print("Sending files to RMOB.org: ", cmd)
                            ret = os.system(cmd)
                            if ret == 0:
                                self._parent.updateStatusBar("Sending successful")
                            else:
                                self._parent.infoMessage("Failed sending files to RMOB.org",
                                                         "command={}, returned={}".format(cmd, ret))
                    else:
                        self._parent.updateStatusBar("Files NOT SENT to RMOB.org")

        self._RMOBupdating = False
        self._parent.busy(False)
        return dfMonth, heatmapFileName, bargraphFileName

    def showDataTable(self):
        self._parent.busy(True)
        self._ui.gbClassFilter_2.show()
        self._ui.gbDiagrams_2.hide()
        self._dataSource = self._parent.dataSource
        row = self._ui.lwTabs.currentRow()
        # self._ui.pbRMOB.setEnabled(False)
        if self._classFilter == '':
            # nothing to show
            self._parent.infoMessage('Statistic diagrams:',
                                     'No class filters set, nothing to show')
            self._parent.busy(False)
            return

        df = self._dataSource.getADpartialFrame(self._parent.fromDate, self._parent.toDate)

        if row == self.TAB_DAILY_BY_DAY:
            self._dataFrame = self._dataSource.dailyByClassification(df, self._classFilter, self._parent.fromDate,
                                                                     self._parent.toDate, totalRow=True,
                                                                     totalColumn=True)
            model = PandasModel(self._dataFrame)
            self._ui.tvTabs.setModel(model)

        if row == self.TAB_DAILY_BY_HOUR:
            self._dataFrame = self._dataSource.makeDaily(df, self._parent.fromDate, self._parent.toDate, dtRes='H',
                                                         filters=self._classFilter)
            model = PandasModel(self._dataFrame)
            self._ui.tvTabs.setModel(model)

        if row == self.TAB_DAILY_BY_10M:
            self._dataFrame = self._dataSource.makeDaily(df, self._parent.fromDate, self._parent.toDate, dtRes='10T',
                                                         filters=self._classFilter)
            self._dataFrame = self._dataSource.splitAndStackDataframe(self._dataFrame, maxColumns=24)
            model = PandasModel(self._dataFrame)
            self._ui.tvTabs.setModel(model)

        if row == self.TAB_SESSIONS_REGISTER:
            # filters not applicable here
            self._ui.gbClassFilter_2.hide()
            self._dataFrame = self._dataSource.getASpartialFrame(self._parent.fromDate, self._parent.toDate)
            model = PandasModel(self._dataFrame)
            self._ui.tvTabs.setModel(model)

        if row == self.TAB_RMOB_MONTH:
            # self._ui.pbRMOB.setEnabled(True)
            df2 = self._dataSource.makeDaily(df, self._parent.fromDate, self._parent.toDate, dtRes='H',
                                             filters=self._classFilterRMOB, totalRow=False,
                                             totalColumn=False)
            self._dataFrame, monthName, year = self._dataSource.makeRMOB(df2)

            model = PandasModel(self._dataFrame)
            self._ui.tvTabs.setModel(model)

        self._parent.busy(False)

    def showDataDiagram(self):
        dataFrame = None
        self._parent.busy(True)
        self._ui.gbDiagrams_2.show()
        self._dataSource = self._parent.dataSource
        px = plt.rcParams['figure.dpi']  # from inches to pixels
        self._showColormapSetting(False)
        tableRow = self._ui.lwTabs.currentRow()
        graphRow = self._ui.lwDiags.currentRow()

        # maximum length of time axis in days for each kind of graph
        maxCoverages = [
            # [self.GRAPH_PLOT]
            [
                366,  # daily counts by day
                15,  # daily counts by hour
                7,  # daily counts by 10min
                0,  # session table, no graphics
                1,  # RMOB month, current day only
                0,  # undefined
                0,  # undefined
                0,  # undefined

            ],

            # [self.GRAPH_HEATMAP]
            [
                366,  # daily counts by day
                90,  # daily counts by hour
                31,  # daily counts by 10min
                0,  # session table, no graphics
                31,  # RMOB month
                0,  # undefined
                0,  # undefined
                0,  # undefined

            ],

            # [GRAPH_BARS]
            [
                366,  # bargraph by day
                15,  # bargraph by hour
                7,  # bargraph by 10m
                0,  # session table, no graphics
                1,  # RMOB month, current day only
                0,  # undefined
                0,  # undefined
                0,  # undefined
            ],

            # [GRAPH_PIE]
            [
                366,  # daily counts by classification, covers up to 1 year
                0,  # undefined
                0,  # undefined
                0,  # undefined
                0,  # undefined
                0,  # undefined
                0,  # undefined
                0,  # undefined
            ]
        ]

        cov = maxCoverages[graphRow][tableRow]

        if cov == 0:
            # nothing to show
            self._parent.infoMessage('Statistic diagrams;',
                                     'Combination table/graph not implemented')
            self._parent.busy(False)
            return

        if self._classFilter == '':
            # nothing to show
            self._parent.infoMessage('Statistic diagrams:',
                                     'No class filters set, nothing to show')
            self._parent.busy(False)
            return

        if self._parent.coverage > cov and tableRow != self.TAB_RMOB_MONTH:
            self._parent.busy(False)
            notice("Notice", "This graph cannot display {} days, please reduce the day coverage and "
                             "retry".format(self._parent.coverage))
            return

        # removing previously shown graph
        layout = self._ui.wContainer.layout()
        scroller = None
        inchWidth = 0
        inchHeight = 0
        fullScale = 10000  # init value
        if layout is None:
            layout = QHBoxLayout()
        else:
            layout.removeWidget(self._diagram)
            layout.removeItem(self._spacer)

        if graphRow == self.GRAPH_PLOT:
            # classic plot
            sp = None
            dfAuto = self._dataSource.getADpartialFrame(self._parent.fromDate, self._parent.toDate)
            if tableRow == self.TAB_RMOB_MONTH:
                # only the latest day
                dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.toDate, self._parent.toDate, dtRes='H',
                                                       filters=self._classFilter, totalRow=False, totalColumn=False)
                series = self._dataSource.tableTimeSeries(dataFrame, columns=range(0, 24))
                # the figure width is calculated in order to make visible the smallest possible bar (width=0.01")
                # one per each hour of a day. So for each day showed, 0.24" are needed
                hours = len(series.index)
                inchWidth = (0.24 * hours * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                sp = StatPlot(series, self._settings, inchWidth, inchHeight, 'hour', self._showValues, self._showGrid)

            if tableRow == self.TAB_DAILY_BY_HOUR:
                dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate, dtRes='H',
                                                       filters=self._classFilter, totalRow=False, totalColumn=False)
                series = self._dataSource.tableTimeSeries(dataFrame, columns=range(0, 24))
                # the figure width is calculated in order to make visible the smallest possible bar (width=0.01")
                # one per each hour of a day. So for each day showed, 0.24" are needed
                hours = len(series.index)
                inchWidth = (0.24 * hours * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                sp = StatPlot(series, self._settings, inchWidth, inchHeight, 'hour', self._showValues, self._showGrid)

            if tableRow == self.TAB_DAILY_BY_10M:
                dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate, dtRes='10T',
                                                       filters=self._classFilter, totalRow=False, totalColumn=False)
                series = self._dataSource.tableTimeSeries(dataFrame, columns=range(0, 144))

                # the figure width is calculated in order to make visible the smallest possible bar (width=0.01")
                # six per each hour of a day. So for each day showed, 1.44" are needed
                tenmin = len(series.index)
                hours = tenmin / 6
                inchWidth = (1.44 * hours * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                sp = StatPlot(series, self._settings, inchWidth, inchHeight, '10m', self._showValues, self._showGrid)

            if tableRow == self.TAB_DAILY_BY_DAY:
                dataFrame = self._dataSource.dailyByClassification(dfAuto, self._classFilter, self._parent.fromDate,
                                                                   self._parent.toDate, totalRow=False,
                                                                   totalColumn=True)

                df = dataFrame
                series = df['Total'].squeeze()
                days = len(series.index)
                inchWidth = (0.2 * days * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                sp = StatPlot(series, self._settings, inchWidth, inchHeight, 'day', self._showValues, self._showGrid)

            canvas = sp.widget()
            scroller = QScrollArea()
            pixWidth = int(px * inchWidth)
            pixHeight = int(px * inchHeight)
            if pixWidth > 65535:
                pixWidth = 65535
            if pixHeight > 65535:
                pixHeight = 65535
            canvas.setMinimumSize(QSize(pixWidth, pixHeight))
            scroller.setWidget(canvas)
            layout.addWidget(scroller)
            self._plot = sp

        elif graphRow == self.GRAPH_HEATMAP:
            cg = None
            self._showColormapSetting(True)
            cmap = self._parent.cmapDict[self._currentColormap]

            # retrieve the data to be shown
            dfAuto = self._dataSource.getADpartialFrame(self._parent.fromDate, self._parent.toDate)

            if tableRow == self.TAB_DAILY_BY_DAY:
                dataFrame = self._dataSource.dailyByClassification(dfAuto, self._classFilter, self._parent.fromDate,
                                                                   self._parent.toDate, totalRow=False,
                                                                   totalColumn=False)

                inchWidth = ((0.30 * len(self._classFilter)) * self._zoom) / px  # classes on horizontal axis
                inchHeight = ((0.30 * self._parent.coverage) * self._zoom)  # days in vertical axis

                if dataFrame is not None:
                    cg = Heatmap(dataFrame, self._settings, inchWidth, inchHeight, cmap, self._showValues,
                                 self._showGrid)
                    canvas = cg.widget()
                    pixWidth = int(px * inchWidth)
                    pixHeight = int(px * inchHeight)
                    if pixWidth > 65535:
                        pixWidth = 65535
                    if pixHeight > 65535:
                        pixHeight = 65535
                    canvas.setMinimumSize(QSize(pixWidth, pixHeight))
                    scroller = QScrollArea()
                    scroller.setWidget(canvas)
                    layout.addWidget(scroller)
                    self._spacer = QSpacerItem(40, 20, QSizePolicy.Minimum)
                    layout.addItem(self._spacer)

            elif tableRow == self.TAB_RMOB_MONTH:
                df2 = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate,
                                                 dtRes='H',
                                                 filters=self._classFilterRMOB, totalRow=False,
                                                 totalColumn=False)

                dataFrame, monthNr, year = self._dataSource.makeRMOB(df2)
                fullScale = dataFrame.max(axis=None)
                # override is only for GUI, the HeatmapRMOB always behaves so
                overrideCmap = "colorgramme"
                self._showColormapSetting(True, overrideCmap)
                cmap = self._parent.cmapDict[overrideCmap]
                overrideShowValues = False
                self._ui.chkShowValues.setChecked(overrideShowValues)

                if dataFrame is not None:
                    inchWidth = (0.20 * 31)  # fixed 31 days, zoom ignored
                    inchHeight = (self._ui.wContainer.height()) / px  # 24h from pixels to inches, zoom ignored
                    inchHeight /= 3
                    cg = HeatmapRMOB(dataFrame, self._settings, inchWidth, inchHeight, cmap)
                    canvas = cg.widget()
                    pixWidth = int(px * inchWidth)
                    pixHeight = int(px * inchHeight)
                    if pixWidth > 65535:
                        pixWidth = 65535
                    if pixHeight > 65535:
                        pixHeight = 65535
                    canvas.setMinimumSize(QSize(pixWidth, pixHeight))
                    scroller = QScrollArea()
                    scroller.setWidget(canvas)
                    layout.addWidget(scroller)
                    self._spacer = QSpacerItem(40, 20, QSizePolicy.Minimum)
                    layout.addItem(self._spacer)

            else:
                inchWidth = ((0.30 * self._parent.coverage) * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # 24h from pixels to inches

                if tableRow == self.TAB_DAILY_BY_HOUR:
                    dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate,
                                                           dtRes='H',
                                                           filters=self._classFilter, totalRow=False,
                                                           totalColumn=False)
                if tableRow == self.TAB_DAILY_BY_10M:
                    dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate,
                                                           dtRes='10T',
                                                           filters=self._classFilter, totalRow=False,
                                                           totalColumn=False)
                    inchHeight *= 3  # 144 intervals 10m each - needs 6 times the vertical space

                if dataFrame is not None:
                    cg = Heatmap(dataFrame, self._settings, inchWidth, inchHeight, cmap, self._showValues,
                                 self._showGrid)
                    canvas = cg.widget()
                    pixWidth = int(px * inchWidth)
                    pixHeight = int(px * inchHeight)
                    if pixWidth > 65535:
                        pixWidth = 65535
                    if pixHeight > 65535:
                        pixHeight = 65535
                    canvas.setMinimumSize(QSize(pixWidth, pixHeight))

                    scroller = QScrollArea()
                    scroller.setWidget(canvas)
                    layout.addWidget(scroller)
                    self._spacer = QSpacerItem(40, 20, QSizePolicy.Minimum)
                    layout.addItem(self._spacer)
            self._plot = cg

        elif graphRow == self.GRAPH_BARS:
            # bargraphs
            bg = None
            dfAuto = self._dataSource.getADpartialFrame(self._parent.fromDate, self._parent.toDate)
            if tableRow == self.TAB_RMOB_MONTH:
                # first considers all data to find the colormap fullScale
                df2 = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate,
                                                 dtRes='H',
                                                 filters=self._classFilterRMOB, totalRow=False,
                                                 totalColumn=False)
                fullScale = df2.max().max()

                # the bargraph in fact considers only the latest day
                dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.toDate, self._parent.toDate, dtRes='H',
                                                       filters=self._classFilterRMOB, totalRow=False, totalColumn=False)

                series = self._dataSource.tableTimeSeries(dataFrame, columns=range(0, 24))
                # the figure width is calculated in order to make visible the smallest possible bar (width=0.01")
                # one per each hour of a day. So for each day showed, 0.24" are needed
                hours = len(series.index)
                inchWidth = (0.025 * hours)  # zoom is ignored
                # inchHeight = (self._ui.wContainer.height()) / px  # from  pixels to inches, zoom ignored
                maxVal = series.values.max(initial=0)
                inchHeight = maxVal * 0.02

                # override is only for GUI, the BargraphRMOB always behaves so
                overrideShowValues = False
                self._ui.chkShowValues.setChecked(overrideShowValues)
                overrideShowGrid = False
                self._ui.chkGrid_2.setChecked(overrideShowGrid)
                overrideCmap = "colorgramme"
                self._showColormapSetting(True, overrideCmap)
                cmap = self._parent.cmapDict[overrideCmap]

                bg = BargraphRMOB(series, self._settings, inchWidth, inchHeight, cmap, fullScale)

            if tableRow == self.TAB_DAILY_BY_HOUR:
                dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate, dtRes='H',
                                                       filters=self._classFilter, totalRow=False, totalColumn=False)
                series = self._dataSource.tableTimeSeries(dataFrame, columns=range(0, 24))
                # the figure width is calculated in order to make visible the smallest possible bar (width=0.01")
                # one per each hour of a day. So for each day showed, 0.24" are needed
                hours = len(series.index)
                inchWidth = (0.24 * hours * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                bg = Bargraph(series, self._settings, inchWidth, inchHeight, 'hour', self._showValues, self._showGrid)

            if tableRow == self.TAB_DAILY_BY_10M:
                dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate, dtRes='10T',
                                                       filters=self._classFilter, totalRow=False, totalColumn=False)
                series = self._dataSource.tableTimeSeries(dataFrame, columns=range(0, 144))

                # the figure width is calculated in order to make visible the smallest possible bar (width=0.01")
                # six per each hour of a day. So for each day showed, 1.44" are needed
                tenmin = len(series.index)
                hours = tenmin / 6
                inchWidth = (1.44 * hours * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                bg = Bargraph(series, self._settings, inchWidth, inchHeight, '10m', self._showValues, self._showGrid)

            if tableRow == self.TAB_DAILY_BY_DAY:
                # dataFrame = self._dataSource.makeDaily(dfAuto, self._parent.fromDate, self._parent.toDate, dtRes='D',
                #                                      filters=self._classFilter, totalRow=False, totalColumn=False)
                dataFrame = self._dataSource.dailyByClassification(dfAuto, self._classFilter, self._parent.fromDate,
                                                                   self._parent.toDate, totalRow=False,
                                                                   totalColumn=True)

                df = dataFrame
                series = df['Total'].squeeze()
                days = len(series.index)
                inchWidth = (0.2 * days * self._zoom)
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                bg = Bargraph(series, self._settings, inchWidth, inchHeight, 'day', self._showValues, self._showGrid)

            canvas = bg.widget()
            scroller = QScrollArea()
            pixWidth = int(px * inchWidth)
            pixHeight = int(px * inchHeight)
            if pixWidth > 65535:
                pixWidth = 65535
            if pixHeight > 65535:
                pixHeight = 65535
            canvas.setMinimumSize(QSize(pixWidth, pixHeight))

            scroller.setWidget(canvas)
            layout.addWidget(scroller)
            self._plot = bg

        elif graphRow == self.GRAPH_PIE:
            if tableRow == self.TAB_DAILY_BY_DAY:
                # pie chart by classification, shows only the filtered classes
                df = self._dataSource.totalsByClassification(self._classFilter, self._parent.fromDate,
                                                             self._parent.toDate)
                inchWidth = (self._ui.wContainer.width() * self._zoom) / px
                inchHeight = (self._ui.wContainer.height() * self._zoom) / px  # from  pixels to inches
                pie = NestedPie(df, self._settings, inchWidth, inchHeight)
                canvas = pie.widget()
                scroller = QScrollArea()
                pixWidth = int(px * inchWidth)
                pixHeight = int(px * inchHeight)
                if pixWidth > 65535:
                    pixWidth = 65535
                if pixHeight > 65535:
                    pixHeight = 65535
                canvas.setMinimumSize(QSize(pixWidth, pixHeight))

                scroller.setWidget(canvas)
                layout.addWidget(scroller)
            self._plot = pie

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._ui.wContainer.setLayout(layout)
        self._diagram = scroller
        self._parent.busy(False)

    def _getClassFilter(self):
        self._parent.busy(True)
        self._classFilter = self._settings.readSettingAsString('classFilterStat')
        idx = 0
        for tag in self._parent.filterTags:
            isCheckTrue = tag in self._classFilter
            self._parent.filterCheckStats[idx].setChecked(isCheckTrue)
            idx += 1
        self._parent.busy(False)

    def _setClassFilter(self):
        self._parent.busy(True)
        classFilter = ''
        idx = 0
        for check in self._parent.filterCheckStats:
            if check.isChecked():
                classFilter += self._parent.filterTags[idx] + ','
            idx += 1

        if classFilter != '':
            classFilter = classFilter[0:-1]  # discards latest comma+space

        self._classFilter = classFilter
        self._settings.writeSetting('classFilterStat', self._classFilter)
        self._parent.updateStatusBar("Filtering statistic data by classification: {}".format(self._classFilter))
        self._parent.busy(False)

    def _updateTabGraph(self):
        if self._ui.twStats.currentIndex() == self.STTW_TABLES:
            self.showDataTable()
        if self._ui.twStats.currentIndex() == self.STTW_DIAGRAMS:
            self.showDataDiagram()
        self._ui.lbStatFilename.setText("undefined")

    def _toggleCheckAll(self):
        self._ui.chkOverdense_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkUnderdense_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkFakeEsd_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkFakeCar1_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkFakeCar2_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkFakeSat_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkFakeLong_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkLOSfilter_2.setChecked(self._ui.chkAll_2.isChecked())
        self._ui.chkAcqActive_2.setChecked(self._ui.chkAll_2.isChecked())
        self._setClassFilter()

    def _cmapChanged(self, newCmapName):
        self._currentColormap = newCmapName
        print("selected colormap: ", newCmapName)

    def _showDiagramSettings(self, show: bool):
        self._ui.gbSettings_2.setVisible(show)

    def _showColormapSetting(self, show: bool, overrideCmap: str = None):
        self._ui.lbCmap_2.setVisible(show)
        self._ui.cbCmaps_2.setVisible(show)
        self._ui.cbCmaps_2.setEnabled(True)
        if overrideCmap is not None:
            self._ui.cbCmaps_2.setCurrentText(overrideCmap)
        else:
            self._ui.cbCmaps_2.setCurrentText(self._currentColormap)

    def _exportPressed(self, checked):
        self._parent.checkExportDir(self._exportDir)
        pngName = None
        # progressive number to make the exported files unique
        now = datetime.now()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        prog = "-{}".format((now - midnight).seconds)
        if os.path.exists(self._exportDir):
            os.chdir(self._exportDir)
            if self._ui.twStats.currentIndex() == self.STTW_TABLES:
                # the displayed table is exported as csv
                title = self._ui.lwTabs.currentItem().text() + prog
                self._dataFrame.style.set_caption(title)
                row = self._ui.lwTabs.currentRow()
                if row == self.TAB_SESSIONS_REGISTER:
                    defaultComment = "{}\nfrom {} to {},\n{} sessions in total\n\n".format(
                        title, self._parent.fromDate, self._parent.toDate, self._parent.covID)

                else:
                    filters = ''
                    fList = self._classFilter.split(',')
                    for f in fList:
                        filters += " -> {}\n".format(self.filterDesc[f], '\n')
                    defaultComment = "{}\nfrom {} to {},\n{} events in total\n\nactive filters:\n{}".format(
                        title, self._parent.fromDate, self._parent.toDate, self._parent.covID, filters)

                self._parent.busy(False)
                comment = QInputDialog.getMultiLineText(self._parent, "Export statistic table",
                                                        "Comment\n(please enter further considerations, if needed):",
                                                        defaultComment)
                self._parent.busy(True)
                title = title.lower().replace(' ', '_')
                if 'sessions' in title:
                    # resolution not applicable on sessions table
                    csvName = 'stat-' + title + '-NA-Table.csv'
                else:
                    csvName = 'stat-' + title + '-Table.csv'

                self._dataFrame.to_csv(csvName, index=True, sep=self._settings.dataSeparator())
                self._parent.updateStatusBar("Exported  {}".format(csvName))
                self._ui.lbStatFilename.setText(csvName)
                if len(comment[0]) > 0:
                    if 'sessions' in title:
                        # resolution not applicable on sessions table
                        commentsName = 'comments-' + title + '-NA-Table.txt'
                    else:
                        commentsName = 'comments-' + title + '-Table.txt'

                    with open(commentsName, 'w') as txt:
                        txt.write(comment[0])
                        txt.close()
                        self._parent.updateStatusBar("Exported  {}".format(commentsName))
                        self._ui.lbCommentsFilename.setText(commentsName)

            if self._ui.twStats.currentIndex() == self.STTW_DIAGRAMS:
                title = self._ui.lwTabs.currentItem().text() + prog

                filters = ''
                fList = self._classFilter.split(',')
                for f in fList:
                    filters += " -> {}\n".format(self.filterDesc[f], '\n')
                defaultComment = "{}\nfrom {} to {},\n{} events in total\n\nactive filters:\n{}".format(
                    title, self._parent.fromDate, self._parent.toDate, self._parent.covID, filters)

                self._parent.busy(False)
                comment = QInputDialog.getMultiLineText(self._parent, "Export statistic diagram",
                                                        "Comment\n(please enter further considerations, if needed):",
                                                        defaultComment)
                self._parent.busy(True)
                title = title.lower().replace(' ', '_')
                className = type(self._plot).__name__
                pngName = 'stat-' + title + '-' + className + '.png'
                self._plot.saveToDisk(pngName)
                self._parent.updateStatusBar("Exported  {}".format(pngName))
                self._ui.lbStatFilename.setText(pngName)
                if len(comment[0]) > 0:
                    commentsName = 'comments-' + title + '-' + className + '.txt'
                    commentsName = commentsName.replace(' ', '_')
                    with open(commentsName, 'w') as txt:
                        txt.write(comment[0])
                        txt.close()
                        self._parent.updateStatusBar("Exported  {}".format(commentsName))
                        self._ui.lbCommentsFilename.setText(commentsName)

            os.chdir(self._parent.workingDir)
        self._parent.busy(False)
        return pngName

    def _generateRMOBgraphFile(self):
        pngName = None
        self._parent.busy(True)
        os.chdir(self._parent.workingDir)
        if self._ui.twStats.currentIndex() == self.STTW_TABLES:
            # the displayed table is exported as csv
            title = self._ui.lwTabs.currentItem().text()
            self._dataFrame.style.set_caption(title)
            title = title.lower().replace(' ', '_')
            csvName = 'stat-' + title + '.csv'
            self._dataFrame.to_csv(csvName, index=True, sep=self._settings.dataSeparator())
            self._parent.updateStatusBar("Generated  {}".format(csvName))
            self._ui.lbStatFilename.setText(csvName)

        if self._ui.twStats.currentIndex() == self.STTW_DIAGRAMS:
            title = self._ui.lwTabs.currentItem().text()
            title = title.lower().replace(' ', '_')
            className = type(self._plot).__name__
            pngName = 'stat-' + title + '-' + className + '.png'
            self._plot.saveToDisk(pngName)
            self._parent.updateStatusBar("Generated  {}".format(pngName))
            self._ui.lbStatFilename.setText(pngName)

        self._parent.busy(False)
        return pngName

    def _generateRMOBtableFile(self, dfRMOB: pd.DataFrame, year: int, monthNr: int):
        self._parent.busy(True)
        os.chdir(self._parent.workingDir)
        # RMOB data format is similar to hourly counts table, without the rightmost column (row totals)
        # and bottom row (column totals)
        owner = self._settings.readSettingAsString('owner').split(' ')
        filePrefix = "{}_{:02d}{}".format(owner[0], monthNr, year)
        filename = filePrefix + "rmob.TXT"
        monthName = calendar.month_abbr[monthNr].lower()
        dfRMOB.index.name = monthName
        dfRMOB.replace(-1, '??? ', inplace=True)
        dfRMOB.to_csv(filename, sep='|', lineterminator='|\r\n', float_format="{: 4d}")
        self._parent.updateStatusBar("Exported  {}".format(filename))
        self._ui.lbStatFilename.setText(filename)

        # after counts, the station informations are appended to each file

        # converts the sexagesimal coordinates format (DEG° MIN' SEC'') to Cologramme format
        # (3 digits zero filled DEG°, MINSEC as 2+2 digits, i.e. 51° 28' 38'' ==> 051°2838 N)
        latDeg = self._settings.readSettingAsString('latitudeDeg')
        elems = [int(x) for x in re.split('°|\'|"', latDeg) if x != '']
        latDeg = "{:03}°{:02}{:02}".format(elems[0], elems[1], elems[2])
        latDeg += ' N' if elems[0] >= 0 else ' S'
        longDeg = self._settings.readSettingAsString('longitudeDeg')
        elems = [int(x) for x in re.split('°|\'|"', longDeg) if x != '']
        longDeg = "{:03}°{:02}{:02}".format(elems[0], elems[1], elems[2])
        longDeg += ' E' if elems[0] >= 0 else ' W'
        with open(filename, 'a') as f:
            fprint("[Observer]{}".format(self._settings.readSettingAsString('owner')), file=f)
            fprint("[Country]{}".format(self._settings.readSettingAsString('country')), file=f)
            fprint("[City]{}".format(self._settings.readSettingAsString('city')), file=f)
            fprint("[Longitude]{}".format(longDeg), file=f)
            fprint("[Latitude ]{}".format(latDeg), file=f)
            fprint("[Longitude GMAP]{}".format(self._settings.readSettingAsString('longitude')), file=f)
            fprint("[Latitude GMAP]{}".format(self._settings.readSettingAsString('latitude')), file=f)
            fprint("[Frequencies]{}".format(self._settings.readSettingAsString('frequencies')), file=f)
            fprint("[Antenna]{}".format(self._settings.readSettingAsString('antenna')), file=f)
            fprint("[Azimut Antenna]{}".format(self._settings.readSettingAsString('antAzimuth')), file=f)
            fprint("[Elevation Antenna]{}".format(self._settings.readSettingAsString('antElevation')), file=f)
            fprint("[Pre-Amplifier]{}".format(self._settings.readSettingAsString('preamplifier')), file=f)
            fprint("[Receiver]{}".format(self._settings.readSettingAsString('receiver')), file=f)
            fprint("[Observing Method]{}".format("Echoes 0.51++ Data Browser v.{}").format(self._parent.version), file=f)
            fprint("[Computer Type]{}".format(self._settings.readSettingAsString('computer')), file=f)
            fprint("[Remarks]{}".format(self._settings.readSettingAsString('notes')), file=f)
            fprint("[Soft FTP]Echoes FTP client v.{}".format(self._parent.version), file=f)
            fprint("[E]{}".format(cryptDecrypt(self._settings.readSettingAsString('email'), 2503)), file=f)
        self._parent.busy(False)
        return filePrefix, filename, dfRMOB

    def _toggleGrid(self, state):
        self._showGrid = (state != 0)
        self._settings.writeSetting('showGridStat', self._showGrid)

    def _toggleValues(self, state):
        self._showValues = (state != 0)
        self._settings.writeSetting('showValues', self._showValues)

    def _tabChanged(self, row):
        if row == self.TAB_RMOB_MONTH or row == self.TAB_SESSIONS_REGISTER:
            # RMOB data use an hardcoded filt, including only
            # non-fake events
            self._ui.gbClassFilter_2.setEnabled(False)
            self._ui.gbSettings_2.setEnabled(False)
        else:
            self._ui.gbClassFilter_2.setEnabled(True)
            self._ui.gbSettings_2.setEnabled(True)
        # self._updateTabGraph()
