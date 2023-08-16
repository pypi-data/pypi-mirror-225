"""
******************************************************************************

    Echoes Data Browser (Ebrow) is a data navigation and report generation
    tool for Echoes.
    Echoes is a RF spectrograph for SDR devices designed for meteor scatter.

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
import time
import calendar
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
from math import isnan
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlError, QSqlTableModel
from PyQt5.QtWidgets import QFileDialog, qApp
from PyQt5.QtCore import QDir, QDate, qUncompress, QMetaType

from .utilities import fpCmp, fuzzyCompare, castFloatPrecision
from .logprint import print


class CustomDataFrame(pd.DataFrame):
    def __init__(self, df):
        super().__init__(df)
        self.numberformat = self.format

    def format(self, column, format_):
        return pd.DataFrame(self[column]).astype(float).applymap(format_.format)


class DataSource:
    connectionProg = 0

    DBFS_RANGE_MIN = -150.0
    DBFS_RANGE_MAX = 20.0

    def __init__(self, parent, settings):
        self._parent = parent
        self._dsPath = None
        self._connectName = None
        self._workingDir = None
        self._db = None  # database handle
        self._adf = None  # automatic_data dataframe
        self._sdf = None  # automatic_sessions dataframe
        self._DBchangedInMemory = False
        self._settings = settings
        # pd.set_option('display.precision', 4)

    def _getDailyNrFromID(self, eventId: int):
        """
        Returns the date and the daily number of the given
        event ID

        @param eventId:
        @return: dailyNr, utcDate
        """
        if self._adf is not None:
            dailyNr = \
                self._adf.loc[
                    (self._adf['id'] == eventId) & (self._adf['event_status'] == 'Fall'), 'daily_nr'].to_list()[0]
            utcDate = \
                self._adf.loc[
                    (self._adf['id'] == eventId) & (self._adf['event_status'] == 'Fall'), 'utc_date'].to_list()[0]
            if dailyNr is not None and utcDate is not None:
                # skips the rowid
                return dailyNr, utcDate
        return None, None

    def _loadAutoDataTable(self):
        """
        Extracts automatic_data from DB to a dataframe
        @return:
        """
        if self._db is not None:
            q = QSqlQuery(self._db)
            select = "SELECT * FROM automatic_data "
            result = q.exec(select)
            if result:
                dataDict = dict()
                q.first()
                columnList = list()
                firstRaiseFound = False
                while q.isValid():
                    qApp.processEvents()
                    rec = q.record()
                    if len(dataDict.keys()) == 0:
                        # the first row is the header
                        for col in range(0, rec.count()):
                            qApp.processEvents()
                            columnName = rec.fieldName(col)
                            columnList.append(columnName)
                            dataDict[columnName] = list()
                    for col in range(0, rec.count()):
                        qApp.processEvents()
                        columnName = columnList[col]
                        field = rec.field(col)
                        val = field.value()
                        varType = field.type()
                        if varType == QMetaType.Double or varType == QMetaType.Float:
                            val = castFloatPrecision(val, 4)

                        # discard the first records until finds a raising front
                        if columnName == 'event_status':
                            if firstRaiseFound is False and val != 'Raise':
                                continue
                            else:
                                firstRaiseFound = True
                        if val == '0':
                            val = 0
                        dataDict[columnName].append(val)
                    q.next()
                self._adf = pd.DataFrame(dataDict)
                self._adf.set_index('id')
                self._adf.sort_index(inplace=True, ascending=True)
            e = QSqlError(q.lastError())
            print("DataSource._loadAutoDataTable() ", e.text())

    def _saveAutoDataTable(self):
        """

        :return:
        """
        if self._db is not None and self._adf is not None and self._DBchangedInMemory is True:
            # ids = self._adf.loc[:,'id'].to_list()
            columns = self._adf.columns.to_list()
            self._adf = self._adf.reset_index()
            self._db.transaction()
            for index, row in self._adf.iterrows():
                qApp.processEvents()
                # print("index={}  id={} status={}".format(index, row['id'], row['event_status']))
                cmd = "UPDATE automatic_data SET "
                for col in columns:
                    qApp.processEvents()
                    if type(row[col]) is str:
                        cmd += "{} = '{}', ".format(col, row[col])
                    else:
                        cmd += "{} = {}, ".format(col, row[col])
                cmd = cmd[0:-2]  # chops final comma and space
                cmd += " WHERE id={} AND event_status='{}'".format(row['id'], row['event_status'])
                # print("cmd=", cmd)
                q = QSqlQuery(self._db)
                result = q.exec(cmd)
                if result <= 0:
                    e = QSqlError(q.lastError())
                    print("DataSource._saveAutoDataTable() ", e.text())
                    self._db.rollback()
                    return False
            print("commit")
            self._db.commit()
            self._DBchangedInMemory = False
            return True
        return False

    def _loadAutoSessionTable(self):
        """
        Extracts automatic_sessions from DB to a dataframe
        @return:
        """
        if self._db is not None:
            q = QSqlQuery(self._db)
            select = "SELECT * FROM automatic_sessions "
            result = q.exec(select)
            if result:
                dataDict = dict()
                q.first()
                columnList = list()
                while q.isValid():
                    qApp.processEvents()
                    rec = q.record()
                    if len(dataDict.keys()) == 0:
                        # the first row is the header
                        for col in range(0, rec.count()):
                            qApp.processEvents()
                            columnName = rec.fieldName(col)
                            columnList.append(columnName)
                            dataDict[columnName] = list()
                    for col in range(0, rec.count()):
                        qApp.processEvents()
                        columnName = columnList[col]
                        val = rec.field(col).value()
                        if val == '0':
                            val = 0
                        dataDict[columnName].append(val)
                    q.next()
                df = pd.DataFrame(dataDict)
                df.set_index('id')
                df.sort_index(inplace=True, ascending=True)
                # creates datetime columns from string datetimes
                df['start_DT'] = pd.to_datetime(df['start_dt'])
                df['end_DT'] = pd.to_datetime(df['living_dt']).fillna(df['start_DT'])

                # then calculate timedeltas on all supported time resolutions
                df = df.drop(columns=['start_dt', 'living_dt', 'end_dt', 'delta_min'])
                # hide the active session (cause 0)
                # df = df[df.cause != 0]

                df['delta_min'] = ((df['end_DT'] - df['start_DT']) / pd.Timedelta(minutes=1)).astype(int)
                df['delta_10min'] = ((df['end_DT'] - df['start_DT']) / pd.Timedelta(minutes=10)).astype(int)
                df['delta_hour'] = ((df['end_DT'] - df['start_DT']) / pd.Timedelta(hours=1)).astype(int)
                df['delta_days'] = ((df['end_DT'] - df['start_DT']) / pd.Timedelta(days=1)).astype(int)

                self._sdf = df
            e = QSqlError(q.lastError())
            print("DataSource._loadAutoSessionTable() ", e.text())

    def timestamp2datetime(self, timestamp_ms: str):
        return datetime.strptime(timestamp_ms, '%d/%m/%Y;%H:%M:%S.%f')

    def name(self):
        filePath = Path(self._dsPath)
        return filePath.name

    def stem(self):
        filePath = Path(self._dsPath)
        return filePath.stem


    def fullPath(self):
        return self._dsPath

    def connection(self):
        return self._connectName

    def reopenFile(self):
        self.closeFile()
        DataSource.connectionProg += 1
        print("creating new database connection")
        self._connectName = "EBROW_CONN#{}".format(DataSource.connectionProg)
        self._db = QSqlDatabase.addDatabase("QSQLITE", self._connectName)
        self._db.setDatabaseName(self._dsPath)
        print("reopening database")
        if self._db.open():
            self._loadAutoDataTable()
            self._loadAutoSessionTable()
            return self._db

        print("error reopening database ", self._dsPath)
        self.closeFile()
        return None

    def openFile(self, fileDBpath):
        """
        @param fileDBpath:
        @return:
        """
        if fileDBpath is not None:
            self.closeFile()
            self._workingDir = QDir.current()
            self._dsPath = fileDBpath
            DataSource.connectionProg += 1
            self._connectName = "EBROW_CONN#{}".format(DataSource.connectionProg)
            self._db = QSqlDatabase.addDatabase("QSQLITE", self._connectName)
            self._db.setDatabaseName(self._dsPath)
            if self._db.open():
                self._loadAutoDataTable()
                self._loadAutoSessionTable()
                return self._db

            print("error opening database ", self._dsPath)
            self.closeFile()
            return None

    def openFileDialog(self):
        """

        @return:
        """
        self.closeFile()
        self._workingDir = QDir.current()
        fileDialog = QFileDialog()
        fileDialog.setWindowTitle("Open Data Source")
        fileDialog.setNameFilter("Echoes database (*.sqlite3)")
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        fileDialog.setDirectory(self._workingDir)
        if fileDialog.exec():
            urls = fileDialog.selectedUrls()
            return self.openFile(fileDialog.selectedFiles()[0])

        print("error opening database ", self._dsPath)
        self.closeFile()
        return None

    def updateFile(self):
        if self._adf is not None and self._DBchangedInMemory:
            print("updating automatic_data table")
            self._saveAutoDataTable()
            return True
        return False

    def closeFile(self):
        if self._db is not None:
            print("closing database and connection")
            self._db.close()
            self._db.removeDatabase(self._dsPath)
            self._db = None
            self._connectName = None
            return True
        return False

    def QDateCoverage(self) -> (QDate, QDate):
        """

        @return:
        """
        qDateFrom = None
        qDateTo = None
        if self._adf is not None:
            dateSeries = self._adf['utc_date']

            dateFrom = dateSeries.min()
            dateTo = dateSeries.max()
            qDateFrom = QDate.fromString(dateFrom, "yyyy-MM-dd")
            qDateTo = QDate.fromString(dateTo, "yyyy-MM-dd")
        return qDateFrom, qDateTo

    def idCoverage(self, dateFrom: str, dateTo: str, selfAdjust: bool = False) -> (str, str, str, str):
        idFrom = 0
        idTo = 0
        if self._adf is not None:
            idsFrom = self._adf.loc[(self._adf['utc_date'] == dateFrom), 'id']
            idsTo = self._adf.loc[(self._adf['utc_date'] == dateTo), 'id']
            idFrom = idsFrom.min()
            idTo = idsTo.max()
            if selfAdjust:
                # automatically fix exceeding bounds
                if isnan(idFrom) or isnan(idTo):
                    dateFrom = min(self._adf['utc_date'])
                    dateTo = max(self._adf['utc_date'])
                    idsFrom = self._adf.loc[(self._adf['utc_date'] == dateFrom), 'id']
                    idsTo = self._adf.loc[(self._adf['utc_date'] == dateTo), 'id']
                    idFrom = idsFrom.min()
                    idTo = idsTo.max()
        return dateFrom, dateTo, idFrom, idTo

    def dailyCoverage(self, date: str) -> int:
        maxDaily = 0
        if self._adf is not None:
            dailySeries = self._adf.loc[(self._adf['utc_date'] == date), 'daily_nr']
            maxDaily = dailySeries.max()
        return maxDaily

    def tableModel(self, name):
        """
        Returns the QSqlTableModel of the given DB table
        @param name:
        @return:
        """
        m = QSqlTableModel(None, self._db)
        m.setTable(name)
        m.select()
        return m

    def dailyByClassification(self, df: pd.DataFrame, filters: str, dateFrom: str = None, dateTo: str = None,
                              totalRow: bool = True, totalColumn: bool = True) -> pd.DataFrame:
        """
        @param df: 
        @param filters: 
        @param dateFrom: 
        @param dateTo: 
        @return: 
        @param totalColumn:
        @param totalRow:
        """

        df.set_index('id')

        # keeps only "Fall" records
        df = df.loc[(df['event_status'] == 'Fall')].copy()

        # daily frequency
        dtRange = pd.date_range(dateFrom, dateTo, freq='D')
        dtSeries = dtRange.to_series()
        dtList = [x.strftime('%Y-%m-%d') for x in dtSeries.to_list()]

        # calculate the daily totals by class
        filterList = filters.split(',')
        classList = filterList
        if 'ACQ ACT' in classList:
            classList.remove('ACQ ACT')
        countsList = []
        for cl in classList:
            qApp.processEvents()
            # keeps only the rows with the required classification
            fdf = df.loc[(df['classification'] == cl)].copy()
            # keeps only the rows with the required date
            countDict = dict()
            for dt in dtList:
                qApp.processEvents()
                tempDf = fdf.loc[(fdf['utc_date'] == dt)].copy()
                countDict[dt] = tempDf.shape[0]
                if countDict[dt] == 0 and 'ACQ ACT' in filterList:
                    # check if zero because no events or because acq stopped:
                    if self.acqWasRunning(dt, 86400) is False:
                        countDict[dt] = -1  # acquisition was stopped

            countSeries = pd.Series(countDict)
            countsList.append(countSeries)
        newDf = pd.concat(countsList, axis=1)
        if totalRow:
            # adds a row with the totals of all columns
            newDf.loc['Total'] = newDf.sum(numeric_only=True)
        if totalColumn:
            # adds a column with the totals of all rows
            newDf['Total'] = newDf.sum(axis=1)
            classList.append('Total')
        newDf.columns = classList
        return newDf

    def totalsByClassification(self, filters: str) -> pd.DataFrame:
        """

        @param filters
        @return:
        """

        totalsDf = None
        if self._adf is not None:
            ids = dict()
            counts = dict()
            filterList = filters.split(',')
            for cat in filterList:
                qApp.processEvents()
                ids[cat] = self._adf.loc[self._adf['classification'].isin([cat]), 'id'].unique()
                counts[cat] = ids[cat].size
            totalsDf = pd.DataFrame(counts)
        return totalsDf

    def totalsUnclassified(self) -> pd.DataFrame:
        """
        @return:
        """

        totalsDf = None
        if self._adf is not None:
            ids = self._adf.loc[:, 'id'].unique()
            return ids.size
        return 0

    def loadTableConfig(self, name: str, rev: int) -> pd.DataFrame:
        """
        Extracts a configuration table
        @param name:
        @param rev:
        @return: dataframe
        """
        if self._db is not None:
            q = QSqlQuery(self._db)
            select = "SELECT * FROM {} WHERE id={}".format(name, rev)
            result = q.exec(select)
            if result:
                dataDict = dict()
                q.first()
                columnList = list()
                if not q.isValid():
                    # if no record indexed by rev is present, takes the youngest record
                    select = "SELECT * FROM {0} WHERE ID = (SELECT MAX(ID) FROM {0})".format(name)
                    q.exec(select)
                    q.first()

                while q.isValid():
                    qApp.processEvents()
                    rec = q.record()
                    if len(dataDict.keys()) == 0:
                        # the first row is the header
                        for col in range(0, rec.count()):
                            qApp.processEvents()
                            columnName = rec.fieldName(col)
                            columnList.append(columnName)
                            dataDict[columnName] = list()
                    for col in range(0, rec.count()):
                        qApp.processEvents()
                        columnName = columnList[col]
                        val = rec.field(col).value()
                        if val == '0':
                            val = 0
                        dataDict[columnName].append(val)
                    q.next()
                return pd.DataFrame(dataDict)

            e = QSqlError(q.lastError())
            print("DataSource.tableConfig() ", e.text())

    def getCfgRevisionFromID(self, eventId: int):
        """
        Returns the RTS configuration revision of the given
        event ID

        @param eventId:
        @return: RTS configuration revision number
        """
        revision = None
        if self._adf is not None:
            revision = self._adf.loc[eventId, 'revision']
        return revision

    def getCfgRevisions(self) -> list:
        """
        Returns a list of RTS configuration revisions occurred in the selected period
        @return: list of revision numbers
        """
        revision = None
        if self._adf is not None:
            revision = self._adf['revision'].unique()
        return revision

    def getIDsOfTheDay(self, date: str):
        """
        Returns a list of event IDs happened in the given day
        @param date:
        @return:
        """
        ids = None
        if self._adf is not None:
            # TODO: ordinare per ID
            ids = self._adf.loc[(self._adf['utc_date'] == date), 'id'].unique().tolist()
        return ids

    def getFilteredIDsOfTheDay(self, date: str, filtClass: str = '', withImagesOnly: bool = False):
        """
        Returns a list of event IDs happened in the given day
        filtered by classification.  Two lists are returned:
        ids and daily numbers
        @param date:
        @param filtClass:
        @return:
        """
        ids = []
        dailies = []
        if len(filtClass) > 0 and self.isDateInRange(date):
            filtList = filtClass.split(',')
            df = self._adf.loc[
                (self._adf['utc_date'] == date) & (self._adf['classification'].isin(filtList)), ['id', 'daily_nr']]

            # TODO: ordinare per ID
            if df is not None:
                ids = df['id'].unique().tolist()
                dailies = df['daily_nr'].unique().tolist()

            if withImagesOnly:
                # discards event and daily ids of events having no image data associated
                toDiscard = list()
                for idx in range(0, len(ids)):
                    cId = int(ids[idx])
                    cDaily = int(dailies[idx])
                    shotName, shotBytes, dailyNr, utcDate = self.extractShotData(cId)
                    if shotName is None:
                        dumpName, dumpBytes, dailyNr, utcDate = self.extractDumpData(cId)
                        if dumpName is None:
                            toDiscard.append((cId, cDaily))
                            continue
                if len(toDiscard) > 0:
                    print("getFilteredIDsOfTheDay() discarding {} events without images".format(len(toDiscard)))
                    for cId, cDaily in toDiscard:
                        ids.remove(cId)
                        dailies.remove(cDaily)
        return ids, dailies

    def extractShotData(self, eventId: int):
        """
        returns the filename and screenshot of the given event ID
        returns also its daily number and date when happened
        @param eventId:
        @return: shotName, shotBytes, dailyNr, utcDate
        """
        if self._db is not None:
            q = QSqlQuery(self._db)
            select = "SELECT shot_name, shot_data FROM automatic_shots WHERE id={}".format(eventId)
            result = q.exec(select)
            if result:
                q.first()
                if q.isValid():
                    shotName = q.value(0)
                    shotBytes = q.value(1)
                    dailyNr, utcDate = self._getDailyNrFromID(eventId)
                    return shotName, shotBytes, dailyNr, utcDate
            e = QSqlError(q.lastError())
            print("DataSource.extractShotData() ", e.text())
        dailyNr, utcDate = self._getDailyNrFromID(eventId)
        return None, None, dailyNr, utcDate
        # return None

    def extractShotsData(self, ids: list):
        """
        returns a list of tuples containing the filename and screenshot of all the events listed in ids
        the tuple contains also its daily number and date when happened
        @param ids: list of event id
        @return: list of tuple(id, shotName, shotBytes, dailyNr, utcDate)
        """
        if self._db is not None:
            q = QSqlQuery(self._db)
            select = "SELECT id, shot_name, shot_data FROM automatic_shots WHERE id IN ("
            for dId in ids:
                qApp.processEvents()
                select += "{}, ".format(dId)
            select = select[0:-2] + ')'
            result = q.exec(select)
            if result:
                tupleList = list()
                q.first()
                while q.isValid():
                    qApp.processEvents()
                    dId = q.value(0)
                    shotName = q.value(1)
                    shotBytes = q.value(2)
                    dailyNr, utcDate = self._getDailyNrFromID(dId)
                    tupleList.append((dId, shotName, shotBytes, dailyNr, utcDate))
                    q.next()
                return tupleList

            e = QSqlError(q.lastError())
            print("DataSource.extractShotsData() ", e.text())
        return None

    def extractDumpData(self, eventId: int):
        """
        returns the filename and  dump qbytearray of the given event ID
        returns also its daily number and date when happened
        @param eventId:
        @return:
        """
        if self._db is not None:
            q = QSqlQuery(self._db)
            select = "SELECT dump_name, dump_data FROM automatic_dumps WHERE id={}".format(eventId)
            result = q.exec(select)
            if result:
                q.first()
                if q.isValid():
                    dumpName = q.value(0)
                    dumpData = qUncompress(q.value(1))
                    '''
                    dumpData = qUncompress(q.value(1)).data().decode()
                    dumpLines = dumpData.splitlines()
                    dumpList = []
                    for line in dumpLines:
                        dumpList.append( line.split() )
                    '''
                    dailyNr, utcDate = self._getDailyNrFromID(eventId)
                    # df = pd.DataFrame(dumpList, columns=['bintime', 'frequency', 'power', 'scantime',
                    # 'S', 'N', 'S-N'])
                    return dumpName, dumpData, dailyNr, utcDate
            e = QSqlError(q.lastError())
            print("DataSource.extractDumpData() ", e.text())
        dailyNr, utcDate = self._getDailyNrFromID(eventId)
        return None, None, dailyNr, utcDate

    def dataChanged(self):
        return self._DBchangedInMemory

    def classifyEvents(self, fromID: int, toID: int, overwrite: bool = False):
        """
        Note: this algorythm has been taken from Echoes PostProc class and pythonized.

        :param fromID:
        :param toID:
        :param overwrite: False=process only unclassified records, True=process all records
        :return:
        """
        df = self.getADpartialFrame(idFrom=fromID, idTo=toID)
        if df is not None:
            if overwrite:
                print("overwriting all current classifications")
                df['classification'] = None

            # the S, N, avgS, diff, avgDiff to be considered for filtering are related to Peak status
            peakRecords = df.loc[df['event_status'] == 'Peak']
            subsetPeak = peakRecords.loc[:, ['S', 'avgS', 'N', 'diff', 'avg_diff', 'diff_start', 'diff_end']]

            # while other fields are considered in Fall status
            fallRecords = df.loc[df['event_status'] == 'Fall']
            subsetFall = fallRecords.loc[:, ['lasting_ms', 'echo_area', 'interval_area', 'peaks_count', 'freq_shift']]
            referenceAvgS = self.DBFS_RANGE_MAX
            nextReferenceAvgS = self.DBFS_RANGE_MAX

            ESDfilter = self._settings.readSettingAsBool('ESDfilter')
            SATfilter = self._settings.readSettingAsBool('SATfilter')
            CAR1filter = self._settings.readSettingAsBool('CAR1filter')
            CAR2filter = self._settings.readSettingAsBool('CAR2filter')
            ESDfilterThreshold = self._settings.readSettingAsFloat('ESDfilterThreshold')
            SATfilterThreshold = self._settings.readSettingAsFloat('SATfilterThreshold')
            CAR1filterThreshold = self._settings.readSettingAsFloat('CAR1filterThreshold')
            CAR2filterThreshold = self._settings.readSettingAsFloat('CAR2filterThreshold')
            underdenseMs = self._settings.readSettingAsInt('underdenseMs')
            overdenseSec = self._settings.readSettingAsInt('overdenseSec')
            LOSfilter = self._settings.readSettingAsBool('LOSfilter')
            LOSfilterThreshold = self._settings.readSettingAsFloat('LOSfilterThreshold')

            cfgOutput = self.loadTableConfig('cfg_output', 0xffff)
            if cfgOutput is None:
                print("classifyEvents(): no output settings table found, doing nothing")
                return False

            detectionRange = int(cfgOutput.iloc[-1:].loc[:, 'shot_freq_range'])

            for idx in fallRecords.index:
                qApp.processEvents()
                referenceAvgS = nextReferenceAvgS
                cla = fallRecords.loc[idx, 'classification']
                myId = fallRecords.loc[idx, 'id']
                if cla == '':
                    print("Classifying eventID#", myId)
                    # idx indexes the fall event - to browse peak events, idx must be decremented by 1
                    idp = idx - 1
                    avgS = subsetPeak.loc[idp, 'avgS']
                    diff = subsetPeak.loc[idp, 'diff']
                    avgDiff = subsetPeak.loc[idp, 'avg_diff']
                    begDiff = subsetPeak.loc[idp, 'diff_start']
                    endDiff = subsetPeak.loc[idp, 'diff_end']

                    result = fpCmp(referenceAvgS, avgS, 1)
                    if result != 0:
                        referenceAvgS = avgS
                    peaksCount = subsetFall.loc[idx, 'peaks_count']
                    if peaksCount > 1:
                        # discards the new reference keeping the previous one
                        nextReferenceAvgS = referenceAvgS

                    echoArea = subsetFall.loc[idx, 'echo_area']
                    intervalArea = subsetFall.loc[idx, 'interval_area']
                    lastingMs = subsetFall.loc[idx, 'lasting_ms']
                    freqShift = subsetFall.loc[idx, 'freq_shift']

                    # filters against rx saturations artifacts
                    if SATfilter > 0:
                        # Strong signals near the receiver site, even on different frequencies
                        # than Echoes tuned frequency, can cause receiver saturations, that
                        # are detected by checking the average S falling down suddendly.
                        # The filt works by storing the average S recorded on any event.
                        # That stored value becomes the reference level. If in a new event,
                        # the average S falls below the reference, exceeding the given tolerance
                        # threshold, the event is classified as saturation

                        fuzzyRatio = fuzzyCompare(referenceAvgS, avgS, SATfilterThreshold)
                        if fuzzyRatio > 0 or diff < 0 :
                            print("eventID#{} is a saturation fake".format(myId))
                            self.setEventClassification(myId, "FAKE SAT")
                            nextReferenceAvgS = referenceAvgS
                            continue


                    # fakes filt suited for lightings and electrostatic discharges ESD
                    if ESDfilter != 0:
                        # ESD appear on waterfall like an horizontal stripe covering the entire bandwidth
                        # with variable duration, depending of its cause: human (i.e. electric motors) or natural
                        # (lightings).
                        # To catch ESD the S-N value at the begin and at the end of the scan
                        # are averaged. The result must not be higher than the diff percentage

                        ref = (begDiff+endDiff)/2
                        perc = abs(diff - ref) / 100.0
                        threshold = (diff * ESDfilterThreshold) / 100.0
                        if ref > threshold:
                            print("eventID#{} is ESD fake".format(myId))
                            self.setEventClassification(myId, "FAKE ESD")
                            nextReferenceAvgS = referenceAvgS
                            continue



                    # fakes filters suited for radio carriers tuned at waterfall's center frequency

                    if CAR1filter > 0:
                        # the filt 1 works on the ratio between the echo area and the interval area covered.
                        # Fixed carriers tend to have very small echo area, being narrow and regular.
                        # In order to compare with the interval area, I must divide it by the detection range
                        # first, in order to let the filt work with any detection range setting.
                        # If the resulting value in below the give threshold, it means it's a carrier
                        coef = echoArea / (lastingMs * int(intervalArea / detectionRange))
                        if 0 < coef < (CAR1filterThreshold * 1e-4):
                            print("eventID#{} is fake,  due to a carrier signal, coef={}".format(myId, coef))
                            self.setEventClassification(myId, "FAKE CAR1")
                            nextReferenceAvgS = referenceAvgS
                            continue

                    if CAR2filter > 0:
                        # The filt 2 finds carriers by checking the istantaneous difference S-N against its average.
                        # If they are too close, into a certain percentage, the event is a carrier
                        fuzzyRatio = fuzzyCompare(diff, avgDiff, CAR2filterThreshold)
                        if fuzzyRatio == 0 and lastingMs > underdenseMs:
                            print(
                                "eventID#{} is fake,  due to a carrier signal, fuzzyRatio={}".format(myId, fuzzyRatio))
                            self.setEventClassification(myId, "FAKE CAR2")
                            nextReferenceAvgS = referenceAvgS
                            continue

                    if LOSfilter != 0:
                        # this filt discriminates events with evident head echoes. The threshold is specified
                        # in Hz and operates on frequency shift field
                        if freqShift > LOSfilterThreshold:
                            print("eventID#{} has important LOS".format(myId))
                            self.setEventClassification(myId, "HI LOS")
                            continue

                    # simple fake filt, lasting based
                    if (lastingMs / 1000) > overdenseSec:
                        print("eventID#{} is fake,  it lasts too long={}ms".format(myId, lastingMs))
                        self.setEventClassification(myId, "FAKE LONG")
                        nextReferenceAvgS = referenceAvgS
                        continue

                    # the event is good
                    if lastingMs <= underdenseMs:
                        print("eventID#{} is underdense, it lasts {}ms".format(myId, lastingMs))
                        self.setEventClassification(myId, "UNDER")
                    elif (lastingMs / 1000) <= overdenseSec:
                        print("eventID#{} is overdense, it lasts {}ms".format(myId, lastingMs))
                        self.setEventClassification(myId, "OVER")
            return True

    def getEventClassifications(self, fromID: int, toID: int):
        """
        @param fromID:
        @param toID:
        @return: dataframe
        """
        if self._adf is not None:
            df = self.getADpartialFrame(idFrom=fromID, idTo=toID)
            fallEdges = df.loc[df['event_status'] == 'Fall']
            classifications = fallEdges.loc[:, ['id', 'classification']]
            classifications = classifications.set_index('id')
            return classifications

    def setEventClassification(self, eventID: int, classif: str):
        """
        @param eventID:
        @param classif:
        @return:
        """
        if self._adf is not None:
            mask = (self._adf['id'] == eventID)
            self._adf.loc[mask, 'classification'] = classif
            try:
                self._parent.classChanges[eventID] = True
                self._DBchangedInMemory = True
                return True
            except IndexError:
                print("BUG! eventId=", eventID)
        return False

    def resetClassifications(self):
        """

        :return:
        """
        self._adf['classification'] = ''
        self._DBchangedInMemory = True

    def getEventData(self, eventID: int):
        """
        Returns a dataframe with event data, having raise, peak and fall data as columns

        @param eventID:
        @return:
        """
        print("getEventData({})".format(eventID))
        df = self.getADpartialFrame(idFrom=eventID, idTo=eventID)
        if df is not None:
            dfr = df[['utc_time', 'up_thr', 'dn_thr', 'S', 'avgS', 'N', 'diff', 'avg_diff', 'top_peak_hz', 'std_dev',
                      'lasting_ms', 'lasting_scans', 'freq_shift', 'echo_area', 'interval_area', 'peaks_count',
                      'LOS_speed', 'scan_ms', 'diff_start', 'diff_end', 'classification', 'shot_name', 'dump_name']]

            dfc = dfr.round(
                {'up_thr': 3, 'dn_thr': 3, 'S': 3, 'avgS': 3, 'N': 3, 'diff': 3, 'avg_diff': 3, 'std_dev': 3})
            dft = dfc.transpose()
            dft.columns = ['RAISE', 'PEAK', 'FALL']
            return dft
        return None

    def getADframe(self):
        return self._adf

    def getASframe(self):
        return self._sdf

    def getADfilteredFrame(self, filters: str = ''):
        """
        :param filters:
        :return:
        """
        if len(filters) > 0:
            filterList = filters.split(',')
            df = self._adf.loc[(self._adf['classification'].isin(filterList))].copy()
        else:
            df = self._adf.copy()
        return df

    def getADpartialCompositeFrame(self, dateFrom: str = None, dateTo: str = None, filters: str = '', idFrom: int = 0,
                                   idTo: int = 0):
        """
        Extracts portions of automatic_data in the given dates interval or ID interval
        packing raise, peak and fall edges in a single row
        @param dateFrom:
        @param dateTo:
        @param idFrom:
        @param idTo:
        @return:
        """
        df = self.getADfilteredFrame(filters)

        # creates a dataframe nf from automatic_data with separate
        # time columns for raise, peak, fall states
        nf = None
        if dateFrom is not None and dateTo is not None:
            nf = df.loc[(df['utc_date'] >= dateFrom) & (df['utc_date'] <= dateTo)]
        elif idFrom > 0 and idTo > 0:
            nf = df.loc[(idFrom <= df['id']) & (idTo >= df['id']),]

        if nf is not None and df.empty is False:
            nf = nf.convert_dtypes(convert_integer=True, convert_floating=True)

        # from nf 3 separate df are created, one for raises,
        # one for peaks and one for falls
        raiseDf = nf.loc[(nf['event_status'] == 'Raise'), :].copy()
        raiseDf.rename(columns={'utc_time': 'utc_raise'}, inplace=True)
        raiseDf.drop(columns=['event_status'], inplace=True)

        peakDf = nf.loc[(nf['event_status'] == 'Peak'), :].copy()
        peakDf.rename(columns={'utc_time': 'utc_peak'}, inplace=True)
        peakDf.drop(columns=['event_status'], inplace=True)

        fallDf = nf.loc[(nf['event_status'] == 'Fall'), :].copy()
        fallDf.rename(columns={'utc_time': 'utc_fall'}, inplace=True)
        fallDf.drop(columns=['event_status'], inplace=True)

        # merge the 3 df in a composite dataframe
        cf = fallDf
        cf = cf.merge(raiseDf[['id', 'utc_raise']], on='id', how='left')
        cf = cf.merge(peakDf[['id', 'utc_peak']], on='id', how='left')

        # the utc_raise and utc_peak columns are moved between utc_date and utc_fall
        cols = cf.columns.to_list()
        colsToMove = ['utc_raise', 'utc_peak']
        inPos = cols.index('utc_fall')
        newCols = cols[0: inPos]
        newCols.extend(colsToMove)
        newCols.extend(cols[inPos:-2])
        cf = cf[newCols]
        if filters == '':
            # everything has been filtered out
            cf = cf.head(0)
        cf.reset_index(drop=True, inplace=True)
        return cf

    def getADpartialFrame(self, dateFrom: str = None, dateTo: str = None, idFrom: int = 0, idTo: int = 0):
        """
        Extracts portions of automatic_data in the given dates interval or ID interval
        @param dateFrom:
        @param dateTo:
        @param idFrom:
        @param idTo:
        @return:
        """
        df = self._adf.copy()
        nf = None
        if dateFrom is not None and dateTo is not None:
            nf = df.loc[(df['utc_date'] >= dateFrom) & (df['utc_date'] <= dateTo)]
        elif idFrom > 0 and idTo > 0:
            nf = df.loc[(idFrom <= df['id']) & (idTo >= df['id']),]

        if nf is not None and df.empty is False:
            nf = nf.convert_dtypes(convert_integer=True, convert_floating=True)
        return nf

    def getASpartialFrame(self, dateFrom: str = None, dateTo: str = None):
        """
        Extracts portions of automatic_sessions in the given dates interval or ID interval
        Rows are filtered by start_dt field
        @param dateFrom:
        @param dateTo:
        @return:
        """
        df = self._sdf.copy()
        subDf = df
        if dateFrom is not None and dateTo is not None:
            dtFrom = pd.to_datetime(dateFrom)
            dtTo = pd.to_datetime(dateTo)
            dtTo = dtTo + timedelta(days=1)
            # selects the rows with start_dt within the given dates range
            subDf = df[(df['start_DT'] >= dtFrom) & (df['end_DT'] < dtTo)]
        return subDf

    def acqWasRunning(self, dtFrom, deltaMins):
        """
        :param dtFrom: datetime as string
        :param deltaMins.
        :return: true if acq was active all along that period

        the minimum resolution is 10 minutes.
        """
        if dtFrom is not None and deltaMins is not None:
            dtTo = dtFrom + np.timedelta64(deltaMins, 'm')
            dateTo = dtTo.strftime("%Y-%m-%d")
            dateFrom = dtFrom.strftime("%Y-%m-%d")
            df = self.getASpartialFrame(dateFrom, dateTo)
            subDf = df[(df['start_DT'] >= dtFrom) & (df['end_DT'] <= dtTo)]
            totalMins = subDf['delta_min'].sum()
            return totalMins >= (deltaMins / 2)

    def tableTimeSeries(self, df: pd.DataFrame, index: list = None, rows: list = None,
                        columns: list = None):
        """
        Gets a dataframe and joins its rows, column by column,  in a Series
        @param df:       source dataframe
        @param index:   dataframe column to be used as index, containing a date or datetime
        @param rows:    dataframe rows list to be converted to series
                        defaults to None meaning all rows
        @param columns:    dataframe columns list to be converted to series
                        defaults to None meaning all columns


        @return:        pandas series

        """

        # TODO: check if [[]] and/or df.explode() could improve this code:

        newDf = df
        # print(df)
        totalColumns = len(df.columns)
        totalRows = len(df.index)
        if rows is None:
            rows = range(0, totalRows)
        if columns is None:
            columns = range(0, totalColumns)
        if index is not None:
            newDf = df.set_index(index)

        seriesList = list()

        for row in rows:
            qApp.processEvents()
            if index is None:
                serie = newDf.iloc[row, columns].reset_index(drop=True).squeeze()
            else:
                serie = newDf.iloc[row, columns].squeeze()
            # print(serie)
            seriesList.append(serie)

        newSerieList = pd.concat(seriesList).tolist()
        index = newDf.index
        indexList = list()
        lenSer = len(newSerieList)
        lenIdx = newDf.shape[0]
        steps = int(lenSer / lenIdx)

        # build index: by joining multiple rows in a single series
        # the original dataframe index won't cover all the series elements.
        # Here a new index is created, in order to cover all the elements.
        # The new labels are formed by a combination of the original index labels
        # plus a progressive (step) number
        for label in index:
            qApp.processEvents()
            st = time.strptime(str(label), "%Y-%m-%d")
            for step in range(0, steps):
                qApp.processEvents()
                if steps <= 24:
                    hours = int(step * (24 / steps))
                    fullSt = (st.tm_year, st.tm_mon, st.tm_mday, hours, 0, 0, 0, 0, 0)
                else:
                    stepByMins = step * ((24 * 60) / steps)
                    hours = int(stepByMins / 60)
                    mins = int(stepByMins % 60)
                    fullSt = (st.tm_year, st.tm_mon, st.tm_mday, hours, mins, 0, 0, 0, 0)

                dt = calendar.timegm(fullSt)
                indexList.append(dt)

        newSerie = pd.Series(data=newSerieList, index=indexList)
        # print(newSerie)
        return newSerie

    def splitAndStackDataframe(self, df: pd.DataFrame, maxColumns=24):
        """

        :param df:
        :param maxColumns:
        :return:
        """
        stacked = pd.DataFrame()
        slices = list()
        step = maxColumns
        last = False
        cols = len(df.columns)
        for index in range(0, cols, step):
            qApp.processEvents()
            if (cols - (index + step)) < step:
                step = cols - index
                last = True
            # print("{}..{}".format(index, index + step))
            ds = df.iloc[:, index:index + step].copy()
            ds.reset_index(inplace=True)
            ds = ds.rename(columns={'index': 'utc_date'})
            h = pd.DataFrame(ds.columns)
            h = h.T
            ds.columns = range(ds.shape[1])
            ds = pd.concat([h, ds])
            # ds.to_csv('c:/temp/slice_{}.csv'.format(len(slices)), sep=';', index=False)
            stacked = pd.concat([stacked, ds])
            slices.append(ds)
            if last:
                break
        return stacked.fillna('-')

    def makeRMOB(self, df: pd.DataFrame, lastOnly: bool = False):
        dfRMOB = None
        if df is not None:
            # RMOB data format is similar to hourly counts table, but covers the latest month in selection
            # and without the rightmost column (row totals) and bottom row (column totals)
            # the date index is split to 3 separate columns year-day-month
            df['date'] = df.index
            df['year'] = df['date'].str.slice(0, 4)
            df['month'] = df['date'].str.slice(5, 7)
            df['day'] = df['date'].str.slice(8, 10)

            coveredYM = df[['year', 'month']].drop_duplicates()
            coveredYM['YM'] = coveredYM['month'] + '_' + coveredYM['year']
            coveredYM.drop(columns=['year', 'month'], inplace=True)
            df = df.set_index('day')
            dfToGenerate = coveredYM['YM'].to_list()
            if lastOnly:
                dfToGenerate = dfToGenerate[-1:]
            dfMonth = None
            for dfMonthName in dfToGenerate:
                qApp.processEvents()
                elements = dfMonthName.split('_')
                month = int(elements[0])
                year = int(elements[1])
                r = range(0, 31)
                dfRMOB = pd.DataFrame(
                    columns=['00h', '01h', '02h', '03h', '04h', '05h', '06h', '07h', '08h', '09h', '10h', '11h', '12h',
                             '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h'],
                    index=[f'{n + 1:02}' for n in r])
                dfRMOB.fillna(value=-1, inplace=True)

                dfMonth = df[df.year == elements[1]]
                dfMonth = dfMonth[df.month == elements[0]]
                dfMonth.drop(columns=['year', 'month', 'date'], inplace=True)

            dfRMOB.loc[dfMonth.index] = dfMonth
            monthNum = int(elements[0])
            year = int(elements[1])
            monthName = calendar.month_abbr[monthNum].lower()
            dfRMOB.index.name = monthName
            return dfRMOB, monthNum, year

    def makeDaily(self, df: pd.DataFrame, dtStart: str, dtEnd: str, dtRes: str, filters: str = '',
                  totalRow: bool = True, totalColumn: bool = True, splitAfterColumns=24):
        """

        @param df:
        @param dtStart:
        @param dtEnd:
        @param dtRes:  'D' daily  'H' hourly  '10T' 10 min.
        @param filters:
        @param totalRow:appends a row with the totals of each column
        @param totalColumn: add a column with the totals of each row
        @param splitAfterColumns maximum number of columns excluding index and rightmost total column if required
        @return:

        """
        df.set_index('id')

        # keeps only "Fall" records
        df = df.loc[(df['event_status'] == 'Fall')].copy()

        # filters fdf by class filters
        filterList = filters.split(',')
        fdf = df.loc[(df['classification'].isin(filterList))].copy()

        # adds a column with timestamp converted to datetime
        fdf['datetime'] = fdf['timestamp_ms'].apply(self.timestamp2datetime)

        dtEndInclusive = datetime.strptime(dtEnd, '%Y-%m-%d') + timedelta(days=1)

        # firstEventDf = fdf.loc[fdf.index[0]]
        # lastEventDf = fdf.loc[fdf.index[-1]]

        # the start it's always at noon of the first considered day, regardless the resolution chosen
        # dtStart = datetime.strptime(firstEventDf['utc_date'], '%Y-%m-%d')
        # same is for the end
        # dtEnd = datetime.strptime(lastEventDf['utc_date'], '%Y-%m-%d')
        oldRow = None
        if dtRes == 'D':
            # daily frequency
            dtRange = pd.date_range(dtStart, dtEnd, freq=dtRes)
            intvlRange = dtRange
            # output dataframe with a single row and days as columns
            outColumns = []
            for dt in intvlRange:
                qApp.processEvents()
                column = '{:02}'.format(dt.date().day)
                outColumns.append(column)
            odf = pd.DataFrame(columns=outColumns, dtype='int32')

            # now scans the reduced dataframe to create a new one
            # containing only records in the required interval
            for i in range(0, len(dtRange) - 1):
                qApp.processEvents()
                dtFrom = dtRange[i]
                dtTo = dtRange[i + 1]
                subdf = fdf[fdf.datetime >= dtFrom]
                ssubdf = subdf[subdf.datetime < dtTo]
                count, nc = ssubdf.shape
                if count == 0 and 'ACQ ACT' in filterList and not self.acqWasRunning(dtFrom, 86400):
                    count = -1
                row = dtFrom.date().strftime('%Y-%m-%d')
                column = '{:02}'.format(dtFrom.date().day)
                if oldRow != row:
                    # avoids turning cells back to floats
                    odf.loc[row] = int(0)
                    oldRow = row
                odf.at[row, column] = count

        elif dtRes == 'H':
            # hourly frequency
            dtRange = pd.date_range(dtStart, dtEndInclusive, freq=dtRes)
            intvlRange = pd.date_range(dtRange[0], periods=24, freq=dtRes)
            # output dataframe with intervals as columns and days on the rows
            outColumns = []
            for dt in intvlRange:
                qApp.processEvents()
                column = '{:02}h'.format(dt.time().hour)
                outColumns.append(column)
            odf = pd.DataFrame(columns=outColumns, dtype='int')
            # now scans the reduced dataframe to create a new one
            # containing only records in the required interval
            for i in range(0, len(dtRange) - 1):
                qApp.processEvents()
                dtFrom = dtRange[i]
                dtTo = dtRange[i + 1]
                subdf = fdf[fdf.datetime >= dtFrom]
                ssubdf = subdf[subdf.datetime < dtTo]
                count, nc = ssubdf.shape
                if count == 0 and 'ACQ ACT' in filterList and not self.acqWasRunning(dtFrom, 60):
                    count = -1
                row = dtFrom.date().strftime('%Y-%m-%d')
                column = '{:02}h'.format(dtFrom.time().hour)
                if oldRow != row:
                    # avoids turning cells back to floats
                    odf.loc[row] = int(0)
                    oldRow = row
                odf.at[row, column] = count

        elif dtRes == '10T':
            # ten minutes frequency
            dtRange = pd.date_range(dtStart, dtEndInclusive, freq=dtRes)
            intvlRange = pd.date_range(dtRange[0], periods=144, freq=dtRes)
            # output dataframe with intervals as columns and days on the rows
            outColumns = []
            for dt in intvlRange:
                qApp.processEvents()
                column = '{:02}h{:02}m'.format(dt.time().hour, dt.time().minute)
                outColumns.append(column)
            odf = pd.DataFrame(columns=outColumns, dtype='int32')

            # now scans the reduced dataframe to create a new one
            # containing only records in the required interval
            for i in range(0, len(dtRange) - 1):
                qApp.processEvents()
                dtFrom = dtRange[i]
                dtTo = dtRange[i + 1]
                subdf = fdf[fdf.datetime >= dtFrom]
                ssubdf = subdf[subdf.datetime < dtTo]
                count, nc = ssubdf.shape
                if count == 0 and 'ACQ ACT' in filterList and not self.acqWasRunning(dtFrom, 10):
                    count = -1
                row = dtFrom.date().strftime('%Y-%m-%d')
                column = '{:02}h{:02}m'.format(dtFrom.time().hour, dtFrom.time().minute)
                if oldRow != row:
                    # avoids turning cells back to floats
                    odf.loc[row] = int(0)
                    oldRow = row
                odf.at[row, column] = count
        else:
            print("format {} not yet implemented".format(dtRes))
            return None

        if totalColumn:
            # adds a column with the totals of all rows
            odf['Total'] = odf.sum(axis=1)

        if totalRow:
            # appends a row with the totals of all columns
            odf.loc['Total'] = odf.sum()

        return odf

    def dbCommit(self):
        if self._db is not None:
            q = QSqlQuery(self._db)
            cmd = "COMMIT"
            result = q.exec(cmd)
            if result > 0:
                return True
            e = QSqlError(q.lastError())
            print("DataSource.dbCommit() ", e.text())
        return False

    def isDateInRange(self, target: str):
        dtFrom = datetime.fromisoformat(self._parent.fromDate)
        dtTo = datetime.fromisoformat(self._parent.toDate)
        dtTarget = datetime.fromisoformat(target)
        return dtFrom <= dtTarget <= dtTo
