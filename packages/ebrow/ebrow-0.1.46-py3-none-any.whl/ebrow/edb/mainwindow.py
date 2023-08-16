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
import time
from datetime import datetime
from pathlib import Path

from pyqtspinner import WaitingSpinner
from PyQt5.QtCore import Qt, QDate, QEvent, QTimer
from PyQt5.QtGui import QColor, QFontDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

# from splash import SplashWindow
from .ui_mainwindow import Ui_ebrowWindow
from .settings import Settings
from .datasource import DataSource
from .screenshots import ScreenShots
from .rtsconfig import RTSconfig
from .stats import Stats
from .prefs import Prefs
from .utilities import createCustomColormapsDict, cleanFolder
from .reports import Report
from .logprint import print, logPrintVerbose

APPVERSION = "0.1.x"


class MainWindow(QMainWindow):
    TWMAIN_DB = 0
    TWMAIN_EVENTS = 1
    TWMAIN_STATISTICS = 2
    TWMAIN_RTS = 3
    TWMAIN_REPORT = 4
    TWMAIN_PREFS = 5
    WINDOW_TITLE = "Echoes Data Browser"

    def __init__(self, app: QApplication, batchRMOB: bool = False, batchReport: bool = False, verboseLog: bool = True):
        super(MainWindow, self).__init__()

        self.app = app
        self.version = APPVERSION
        self.toDate = None
        self.fromDate = None
        self.dataSource = None
        self.filteredIDs = None
        self.filteredDailies = None
        self.currentDate = None
        self.covDays = None

        self.covID = 0
        self.currentIndex = -1  # index in filteredIDs to get the currentID
        self.busyCount = 0
        self.currentID = 0
        self.currentDailyNr = 0
        self.toDailyNr = 0
        self.fromId = 0
        self.toId = 0
        self.coverage = 0
        self.quitting = False
        logPrintVerbose(verboseLog)

        self.cmapDict = createCustomColormapsDict()
        self.batchRMOB = batchRMOB
        self.batchReport = batchReport
        
        self._fontDB = QFontDatabase()
        self._fontDB.addApplicationFont(":/resources/fonts/Gauge-Regular.ttf");
        self._fontDB.addApplicationFont(":/resources/fonts/Gauge-Heavy.ttf");
        self._ui = Ui_ebrowWindow()
        self._ui.setupUi(self)
        self._splash = None
        self._tabScreenshots = None
        self._tabStats = None
        self._tabRTS = None
        self._tabReport = None
        self._tabPrefs = None
        self._cleanExportReq = False

        # list of events which class will be updated by pressing the DB update button
        self.classChanges = list()
        self.classifications = None
        self._ui.pbSave.setEnabled(False)
        self._ui.pbClassReset.setEnabled(False)

        self.appPath = os.path.dirname(os.path.realpath(__file__))

        self._spinner = WaitingSpinner(
            self,
            roundness=52,
            fade=12,
            radius=90,
            lines=60,
            line_length=10,
            line_width=4,
            speed=0.3,
            color=QColor("powderblue")
        )

        self.filterTags = ['OVER', 'UNDER', 'FAKE ESD', 'FAKE CAR1', 'FAKE CAR2', 'FAKE SAT', 'FAKE LONG', 'HI LOS',
                           'ACQ ACT']
        self.filterChecks = [self._ui.chkOverdense, self._ui.chkUnderdense, self._ui.chkFakeEsd, self._ui.chkFakeCar1,
                             self._ui.chkFakeCar2, self._ui.chkFakeSat, self._ui.chkFakeLong, self._ui.chkLOSfilter,
                             self._ui.chkLOSfilter]  # last one is doubled and unused but these 2 lists must have same length

        self.filterCheckStats = [self._ui.chkOverdense_2, self._ui.chkUnderdense_2, self._ui.chkFakeEsd_2,
                                 self._ui.chkFakeCar1_2, self._ui.chkFakeCar2_2, self._ui.chkFakeSat_2,
                                 self._ui.chkFakeLong_2, self._ui.chkLOSfilter_2, self._ui.chkAcqActive_2]

        self.filterCheckReport = [self._ui.chkOverdense_3, self._ui.chkUnderdense_3, self._ui.chkFakeEsd_3,
                                  self._ui.chkFakeCar1_3, self._ui.chkFakeCar2_3, self._ui.chkFakeSat_3,
                                  self._ui.chkFakeLong_3, self._ui.chkLOSfilter_3]

        self._ui.lbVersion.setText(APPVERSION)
        self._ui.gbSrvExport.setVisible(False)
        self.workingDir = Path(Path.home(), Path("ebrow"))
        self.exportDir = Path(self.workingDir, "exports")
        self._iniFilePath = str(Path(self.workingDir, "ebrow.ini"))
        self._settings = Settings(self._iniFilePath)
        self._settings.load()
        windowGeometry = self._settings.readSettingAsObject('geometry')
        self.setGeometry(windowGeometry)
        (self.fromDate, self.toDate) = self._settings.coverage()
        self.fromQDate = QDate().fromString(self.fromDate, 'yyyy-MM-dd')
        self.toQDate = QDate().fromString(self.toDate, 'yyyy-MM-dd')
        self._ui.dtFrom.setDate(self.fromQDate)
        self._ui.dtTo.setDate(self.toQDate)
        Path.mkdir(self.workingDir, parents=True, exist_ok=True)
        self.updateStatusBar("working directory {} ok ".format(self.workingDir))
        Path.mkdir(self.exportDir, parents=True, exist_ok=True)

        os.chdir(self.workingDir)
        self._ui.pbOpen.clicked.connect(self._openDataSource)
        self._ui.pbReload.clicked.connect(self._reloadDataSource)
        self._ui.pbSave.clicked.connect(self._updateDataSource)
        self._ui.pbClassReset.clicked.connect(self._resetClassifications)
        self._ui.pbQuit.clicked.connect(self._quit)
        self._ui.twMain.currentChanged.connect(self._handleTabChanges)

        # the following tabs remain hidden until a db is opened:
        self._ui.twMain.setTabVisible(1, False)  # Screenshots
        self._ui.twMain.setTabVisible(2, False)  # Statistics
        self._ui.twMain.setTabVisible(3, False)  # RTS config
        self._ui.twMain.setTabVisible(4, False)  # Report
        self._initTimer = QTimer()
        self._initTimer.timeout.connect(self.postInit)
        self._initTimer.start(2000)
        if not (batchRMOB or batchReport):
            # self._splash = SplashWindow(self, ":/splashscreen")
            # self._splash.show()
            pass

    # public methods:

    def checkExportDir(self, checkThisDir):
        if not self._cleanExportReq:
            self._cleanExportReq = True
            if not os.listdir(checkThisDir):
                self.updateStatusBar("export directory {} ok".format(checkThisDir))
            else:
                self.updateStatusBar("export directory {} not empty".format(checkThisDir))
                if not (self.batchRMOB or self.batchReport):
                    result = QMessageBox.question(self, self.WINDOW_TITLE,
                                                  "Export directory not empty, delete content before usage?")
                    if result == QMessageBox.StandardButton.Yes:
                        if cleanFolder(str(checkThisDir)):
                            self.updateStatusBar("export directory {} cleaned".format(checkThisDir))

    def eventFilter(self, obj, event):
        if self._settings.readSettingAsBool('tooltipDisabled'):
            if event.type() == QEvent.ToolTip:
                return True

        return super(MainWindow, self).eventFilter(obj, event)

    def postInit(self):
        """
        initialization tasks executed after the main window has been shown
        @return:
        """
        print("post-initialization")
        self._initTimer.stop()

        # the following tabs remain hidden until a db is opened:
        self._ui.twMain.setTabVisible(1, False)  # Screenshots
        self._ui.twMain.setTabVisible(2, False)  # Statistics
        self._ui.twMain.setTabVisible(3, False)  # RTS config
        self._ui.twMain.setTabVisible(4, False)  # Report
        self.updateStatusBar("Creating tabs")
        self._tabScreenshots = ScreenShots(self, self._ui, self._settings)
        self._tabStats = Stats(self, self._ui, self._settings)
        self._tabRTS = RTSconfig(self, self._ui, self._settings)
        self._tabPrefs = Prefs(self, self._ui, self._settings)
        self._tabReport = Report(self, self._ui, self._settings)

        self._ui.lbVersion.setText(APPVERSION)
        self.currentDate = self._settings.readSettingAsString('currentDate')

        # updates the selected range
        # to cover the current month until today
        today = datetime.today()
        if self.batchRMOB:
            self._ui.dtFrom.setDate(QDate(today.year, today.month, 1))
        else:
            dateFrom = self._settings.readSettingAsString('dateFrom')
            qdateFrom = QDate().fromString(dateFrom, 'yyyy-MM-dd')
            self._ui.dtFrom.setDate(qdateFrom)

        self._ui.dtTo.setDate(QDate(today.year, today.month, today.day))

        self.updateStatusBar("Loading database file")
        self._openDataSource(noGUI=True)
        if self._ui.chkAutosave.isChecked() is True:
            self.updateStatusBar("Self saving the database file after classifications")
            self._updateDataSource()

        if self.batchRMOB:
            self.updateStatusBar("Self updating and sending RMOB files (--rmob specified)")
            self.getRMOBdata()
            self.close()
        elif self.batchReport:
            self.updateStatusBar("Self generating report (--report specified)")
            self._tabReport.updateTabReport()
            self.close()
        else:
            if self._splash:
                self._splash.end()
        # self._parent.checkExportDir(self._exportDir)
        self.busy(False, force=True)

    def getRMOBdata(self, sendOk: bool = True):
        # automatic export of RMOB file
        # for runtime and reporting
        return self._tabStats.updateRMOBfiles(sendOk)

    def getSummaryPlot(self, filters):
        # automatic creation of summary plot
        # for reporting
        return self._tabStats.updateSummaryPlot(filters)

    def closeEvent(self, event):
        # closing the window with the X button
        self._quit()
        event.accept()

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        '''
        if self._tabScreenshots is not None:
            self._tabScreenshots.updateThumbnails()
        '''

    def busy(self, wantBusy: bool, force: bool = False, spinner: bool = True):
        if wantBusy:
            if self.busyCount == 0:
                # disable all pushbuttons when waiting
                self.updateStatusBar("Busy")
                self._ui.pbShotExp.setEnabled(False)
                self._ui.pbStatTabExp.setEnabled(False)
                self._ui.pbCfgTabExp.setEnabled(False)
                self._ui.pbRMOB.setEnabled(False)
                self._ui.pbRefresh.setEnabled(False)
                self._ui.pbRefresh_2.setEnabled(False)
                self._ui.pbRefresh_3.setEnabled(False)
                self._ui.pbReportXLSX.setEnabled(False)
                self._ui.pbReportHTML.setEnabled(False)
                self._ui.pbReset.setEnabled(False)
                self._ui.pbSave.setEnabled(False)
                self._ui.pbReload.setEnabled(False)
                self._ui.pbOpen.setEnabled(False)
                self._ui.pbClassReset.setEnabled(False)
                self._ui.dtFrom.setEnabled(False)
                self._ui.dtTo.setEnabled(False)
                if spinner and self._spinner is not None:
                    self._spinner.start()
                    self._spinner.raise_()
                else:
                    QApplication.setOverrideCursor(Qt.WaitCursor)
            self.busyCount += 1
            print("Busy [{}]".format(self.busyCount))
        else:
            if self.busyCount > 0:
                self.busyCount -= 1
                if self.busyCount == 0 or force:
                    self.busyCount = 0
                    self.updateStatusBar("Ready")
                    # self.updateStatusBar("Ready (force={})".format(force))
                    self._ui.pbShotExp.setEnabled(True)
                    self._ui.pbStatTabExp.setEnabled(True)
                    self._ui.pbCfgTabExp.setEnabled(True)
                    self._ui.pbRMOB.setEnabled(True)
                    self._ui.pbRefresh.setEnabled(True)
                    self._ui.pbRefresh_2.setEnabled(True)
                    self._ui.pbRefresh_3.setEnabled(True)
                    self._ui.pbReportXLSX.setEnabled(True)
                    self._ui.pbReportHTML.setEnabled(True)
                    self._ui.pbReset.setEnabled(True)
                    self._ui.pbSave.setEnabled(True)
                    self._ui.pbReload.setEnabled(True)
                    self._ui.pbOpen.setEnabled(True)
                    self._ui.pbClassReset.setEnabled(True)
                    self._ui.dtFrom.setEnabled(True)
                    self._ui.dtTo.setEnabled(True)
                    if spinner and self._spinner is not None:
                        self._spinner.stop()
                    QApplication.restoreOverrideCursor()
                else:
                    pass
                    # print("Still busy [{}]".format(self.busyCount))
        self.app.processEvents()
        time.sleep(0.1)

    def updateStatusBar(self, text):
        print(text)
        s = "{} - {}".format(datetime.now(), text)
        self._ui.pteStatus.appendPlainText(s)
        self._ui.lbStatus.setText(text)
        if self.dataSource is not None:
            todayIDs = self.dataSource.getIDsOfTheDay(self.currentDate)
            if todayIDs is not None and todayIDs is not []:
                self._ui.lbTotal.setNum(self.covID)
                self._ui.lbDate.setText(self.currentDate)
                self._ui.lbCurDaily.setNum(self.toDailyNr)
                self._ui.lbCurFiltered.setNum(len(self.filteredIDs))
        if self.app is not None:
            self.app.processEvents()

    def infoMessage(self, notice: str, msg: str):
        self.busy(False, force=True)
        errorbox = QMessageBox()
        errorbox.setWindowTitle(self.WINDOW_TITLE)
        errorbox.setText(str(notice) + '\n' + str(msg))
        errorbox.setIcon(QMessageBox.Information)
        errorbox.exec_()

    def confirmMessage(self, notice: str, msg: str):
        self.busy(False, force=True)
        errorbox = QMessageBox()
        errorbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        errorbox.setWindowTitle(self.WINDOW_TITLE)
        errorbox.setText(str(notice) + '\n' + str(msg))
        errorbox.setIcon(QMessageBox.Question)
        button = errorbox.exec_()
        return button == QMessageBox.Ok

    # protected methods:

    def _handleTabChanges(self):
        idx = self._ui.twMain.currentIndex()
        if idx == self.TWMAIN_EVENTS:
            self._tabScreenshots.updateTabEvents()
        if idx == self.TWMAIN_STATISTICS:
            self._tabStats.updateTabStats()
        if idx == self.TWMAIN_RTS:
            self._tabRTS.updateTabRTSconfig()
        if idx == self.TWMAIN_PREFS:
            self._tabPrefs.updateTabPrefs()
        if idx == self.TWMAIN_REPORT:
            self._tabReport.updateTabReport()

    def _getCoverage(self):
        if self.dataSource is None:
            return

        qDateFrom = self._ui.dtFrom.date()
        qDateTo = self._ui.dtTo.date()
        defaultDate = self._settings.readSettingAsString('currentDate')
        defaultQDate = QDate().fromString(defaultDate, 'yyyy-MM-dd')

        self.fromDate = qDateFrom.toString("yyyy-MM-dd")
        self.toDate = qDateTo.toString("yyyy-MM-dd")
        self.coverage = qDateFrom.daysTo(qDateTo) + 1
        self.covDays = list()
        date = qDateFrom
        for day in range(0, self.coverage):
            dateStr = date.toString("yyyy-MM-dd")
            self.filteredIDs, self.filteredDailies = self.dataSource.getFilteredIDsOfTheDay(dateStr)
            if len(self.filteredIDs) > 0:
                self.covDays.append(dateStr)
                if defaultDate == '' or not qDateFrom <= defaultQDate <= qDateTo:
                    # if default date is invalid
                    self.currentDate = dateStr  # takes by default the most recent date with images
            date = date.addDays(1)

        self.updateStatusBar("coverage {} days, from {} to {}:".format(self.coverage, self.fromDate, self.toDate))
        self.filteredIDs, self.filteredDailies = self.dataSource.getFilteredIDsOfTheDay(self.currentDate)
        self._ui.lbCovFrom.setText(self.fromDate)
        self._ui.lbCovTo.setText(self.toDate)
        self._settings.writeSetting('dateFrom', self.fromDate)
        self._settings.writeSetting('dateTo', self.toDate)
        if self._tabScreenshots.getCoverage() is False:
            self._tabScreenshots.getCoverage(selfAdjust=True)
            dt = time.strptime(self.fromDate, "%Y-%m-%d")
            self._ui.dtFrom.setDate(QDate(dt.tm_year, dt.tm_mon, dt.tm_mday))
            dt = time.strptime(self.toDate, "%Y-%m-%d")
            self._ui.dtTo.setDate(QDate(dt.tm_year, dt.tm_mon, dt.tm_mday))
            # FIXME: recursion max 1 loop
            self._getCoverage()
            self.updateStatusBar("Fixed day coverage from {} to {}, total {} IDs, from {} to {}:".format(
                self.fromDate, self.toDate, self.covID, self.fromId, self.toId))
            return

        self.covID = (self.toId - self.fromId) + 1
        self.updateStatusBar("coverage {} IDs, from {} to {}:".format(self.covID, self.fromId, self.toId))

    def _quit(self):
        if not self.quitting:
            self.quitting = True
            if not (self.batchRMOB or self.batchReport):
                self._updateDataSource()
            self.dataSource.closeFile()
            self._settings.writeSetting('geometry', self.geometry())
            qDateFrom = self._ui.dtFrom.date()
            qDateTo = self._ui.dtTo.date()
            self.fromDate = qDateFrom.toString("yyyy-MM-dd")
            self.toDate = qDateTo.toString("yyyy-MM-dd")
            self._settings.writeSetting('dateFrom', self.fromDate)
            self._settings.writeSetting('dateTo', self.toDate)
            self._settings.save()
            if not (self.batchRMOB or self.batchReport):
                self.close()

    def _updateDataSource(self):
        print("_updateDataSource()")
        if self.dataSource is not None:
            if True in self.classChanges:
                if (self._settings.readSettingAsBool('autosaving')
                        or
                        self.confirmMessage("Warning - updated classifications",
                                            "Press OK to update the database file on disk, Cancel to skip")):
                    self.busy(True)
                    if self._overrideClassifications():
                        self.updateStatusBar("Saving classifications in DB...")
                        if self.dataSource.updateFile():
                            self.updateStatusBar("Classifications saved in DB")
                            self.classChanges = [False] * (self.fromId + self.covID)
                            self.busy(False)
                            return True
                    self.busy(False)

            elif self.dataSource.dataChanged():
                if (self._settings.readSettingAsBool('autosaving')
                        or self.confirmMessage("Warning - cleared classifications",
                                               "Press OK to update the database file on disk, Cancel to skip")):

                    self.updateStatusBar("Clearing classifications in DB...")
                    self.busy(True)
                    if self.dataSource.updateFile():
                        self.updateStatusBar("Classifications reset in DB")
                        self.classChanges = [False] * (self.fromId + self.covID)
                        self.busy(False)
                        return True
                    self.busy(False)
        print("No changes to be saved in DB")
        return False

    def _reloadDataSource(self):
        self._openDataSource(noGUI=True)

    def _resetClassifications(self):
        if self.confirmMessage("Warning",
                               "Press OK to reset all classifications, Cancel to skip.\n To clear the classifications"
                               " on disk too, press Update Data Source button afterwards."):
            self.busy(True)
            self.updateStatusBar("Clearing all classifications in memory")
            self.dataSource.resetClassifications()
            self.updateStatusBar("Done. Press Update Data Source to reset classifications on DB file also.")
            self.busy(False)

    def _overrideClassifications(self):
        """
        updates the classifications in automatic_data dataframe
        with manual overrides, if any
        :return:
        """
        self.busy(True)
        self.updateStatusBar("Updating classifications on DB...")
        idx = 0
        updated = 0
        for xchg in self.classChanges:
            if xchg is True:
                self.dataSource.setEventClassification(idx, self.classifications.loc[idx, 'classification'])
            idx += 1
            updated += 1
        self.updateStatusBar("{} classifications ready, including manual overrides".format(updated - 1))
        # self._ui.pbSave.setEnabled(False)
        # self._ui.pbClassReset.setEnabled(False)
        self.busy(False)
        return True

    def _openDataSource(self, noGUI: bool = False):
        """

        @param noGUI:
        @return:
        """
        self.busy(True)

        try:
            self._ui.dtFrom.dateChanged.disconnect()
            self._ui.dtTo.dateChanged.disconnect()
        except TypeError:
            pass

        self.dataSource = DataSource(self, self._settings)
        dbOk = False
        name = self._settings.readSettingAsString('lastDBfilePath')

        if name is not None and noGUI:
            # automatic database opening at startup
            dbFile = self.dataSource.openFile(name)
            if dbFile is None:
                self.updateStatusBar("Failed opening stored database file {}".format(name))
            else:
                dbOk = True

        if not noGUI:
            # database opening required by the user via GUI
            if self.dataSource.openFileDialog() is None:
                self.updateStatusBar("Failed opening new database file")

            else:
                dbOk = True

        (qDateFrom, qDateTo) = self.dataSource.QDateCoverage()
        if dbOk and (qDateFrom is None or qDateTo is None):
            dbOk = False

        if dbOk:
            # self._ui.dtFrom.blockSignals(True)
            # self._ui.dtTo.blockSignals(True)
            self._ui.lbDBfilename.setText("{} ".format(self.dataSource.name()))
            if not (self.fromQDate >= qDateFrom and self.toQDate <= qDateTo):
                # if the current interval is not included in data source coverage
                # the interval is reinitialized from data source
                self._ui.dtFrom.setDate(qDateFrom)
                self._ui.dtTo.setDate(qDateTo)

            self._getCoverage()
            self._ui.twMain.setTabVisible(1, True)  # Screenshots
            self._ui.twMain.setTabVisible(2, True)  # Plots
            self._ui.twMain.setTabVisible(3, True)  # Statistics
            self._ui.twMain.setTabVisible(4, True)  # Report
            self._ui.dtFrom.dateChanged.connect(self._getCoverage)
            self._ui.dtTo.dateChanged.connect(self._getCoverage)

            if len(self.filteredIDs) > 0:
                self.currentID = self.filteredIDs[self.currentIndex]
                self.currentDailyNr = self.filteredDailies[self.currentIndex]
            self.updateStatusBar("DB: {}".format(self.dataSource.fullPath()))
            self._settings.writeSetting('lastDBfilePath', self.dataSource.fullPath())
            self.updateStatusBar("Opening ok, performing classifications...")
            self.classChanges = [False] * (self.fromId + self.covID)
            self.dataSource.classifyEvents(self.fromId, self.toId)
            self._ui.pbSave.setEnabled(True)
            self._ui.pbClassReset.setEnabled(True)
            # initialize the editable classifications list

            self.classifications = self.dataSource.getEventClassifications(self.fromId, self.toId)
            self.updateStatusBar("Classifications loaded")
        else:
            # the following tabs remain hidden until a db is opened:
            self._ui.twMain.setTabVisible(1, False)  # Screenshots
            self._ui.twMain.setTabVisible(2, False)  # Statistics
            self._ui.twMain.setTabVisible(3, False)  # RTS config
        self.busy(False)
