import tqdm  # progress bar 표시에 사용되는 package
import os
import zipfile
import py7zr
from datetime import datetime
from multipledispatch import dispatch
import sys
from datetime import datetime
import time

filedir = os.path.dirname(os.path.abspath(__file__))
dllFolder = os.path.join(filedir, r'netcore')

import pythonnet
from clr_loader import get_coreclr
from pythonnet import set_runtime

rt = get_coreclr(runtime_config=os.path.join(dllFolder, "ProcessHost.runtimeconfig.json"))
set_runtime(rt)
sys.path.append(os.path.join(dllFolder, 'downloader'))

import clr
clr.AddReference('MozartDownloader')

# from Mozart.Studio.TaskModel.Utility import FDServiceHelperFactory
import Mozart.Studio.TaskModel.Utility

class Downloader2:
    """
    Baseclass for Mozart zip file download from the server using Mozart OutFileService

    :param url: Mozart server url with port number
    :param subDir: File location to download from the Mozart server
    :example : ml = Downloader('http://192.168.1.2:8000/mozart/OutFileService','VDDF_RTS')

    Methods defined here:
    -- GetFileList() : Return file name list from the server subDir
    -- DownloadFiles(file_list, destination, unzipSwitch=True) : Download Mozart model files for the given file_list to save downloadPath
    -- DownloadFiles(fromDate, toDate, destination, unzipSwitch=True) :Download Mozart model files for the given date period to save downloadPath
    -- DownloadFiles(count, destination, unzipSwitch = True) : Download Mozart model files based on the given number of recently created models

    """
    def __init__(self, url, subDir):
        self.path = 'Auto'
        self.url = url # '{0}/mex?wsdl'.format(url)
        self.subDir = subDir
        self.service = None
        try:
            self.service = Mozart.Studio.TaskModel.Utility.FDServiceHelperFactory.Create(url, wcf=False)
        except ConnectionError as error:
            raise Exception('Connection failed. Wrong or inaccessible hostname:'.format(error=error))

    def GetFileList(self):
        """
        Return file name list from the server subDir

        :return: model file list(list<string>)
        """
        # self.client.service.GetFileList2(self.subDir)
        files = self.service.GetFileList('Auto', self.subDir).ConfigureAwait(False).GetAwaiter().GetResult()
        # with zeep.Client(wsdl=self.url) as client:
        #     files = client.service.GetFileList2(self.subDir)
        return files

    def __checkDir__(self, destination):
        filedir = destination
        if not os.path.exists(filedir):
            print('{0} is not exist path :'.format(filedir))
            pass

    @dispatch(list, str, bool=True)#for function overloading
    def DownloadFiles(self, file_list, destination, unzipSwitch=True):
        """
        Download Mozart model files for the given file_list to save downloadPath

        :param file_list: model file list to download(list<string>)
        :param destination: local file path to save the downloaded files
        :param unzipSwitch: if true, the zip file is unzipped after downloading
        :return:

        """

        filedir = destination
        if not os.path.exists(filedir):
            raise Exception('{0} is not exist path :'.format(filedir))

        downloadedFiles = []
        mainProgress = tqdm.tqdm(file_list, f"Total progress", unit_scale=True, ascii=True, position=0)
        print(f'Total number of files to download = {file_list.__len__()}')
        for fname in file_list:
            filePath = os.path.join(filedir, fname)
            # url에 filedown 함수 호출
            # progress = tqdm.tqdm(0, f"Receiving {fname}", unit="B", unit_scale=True, ascii=True, leave=True,
            #                      unit_divisor=1024)
            # progress.desc('start download')
            try:
                mainProgress.set_description(f'{fname} downlaoding...')
                filesize = self.service.Download('Auto', self.subDir, fname, filePath).ConfigureAwait(False).GetAwaiter().GetResult()
                mainProgress.set_description(f'{fname} downlaoded...')
                # print(f'{fname} downloaded')
                # 각각의 다운로드 파일의 다운로드 상태표시
                downloadedFiles.append(filePath)
            except ConnectionError as error:
                print(filePath)
                raise error

            if unzipSwitch:
                splitFileNames = os.path.splitext(fname)
                if splitFileNames.__len__() < 2:
                    continue

                zipdir = splitFileNames[0]
                try:
                    if zipfile.is_zipfile(filePath):
                        with zipfile.ZipFile(filePath, 'r') as zip_ref:
                            zip_ref.extractall(os.path.join(filedir, zipdir))
                            # mainProgress.set_description(f'{fname} unzip complete')
                        # print(f'{fname} unzip complete')
                    elif splitFileNames[1] == '.7z':
                        # 7z 파일 압축 해제
                        with py7zr.SevenZipFile(filePath, mode='r') as z:
                            z.extractall(path=os.path.join(filedir, zipdir))
                            # mainProgress.set_description(f'{fname} unzip complete')
                    else:
                        continue
                except ConnectionError as error:
                    print(filePath)
                    print(zipdir)
                    raise error

            # progress.update(filesize)
            # progress.close()
            #
            mainProgress.update(1)
            mainProgress.set_description('Done')

        mainProgress.close()

        # delete zipfile
        if unzipSwitch:
            for dfile in downloadedFiles:
                print(dfile)
                os.remove(dfile)

    @dispatch(datetime, datetime, str, bool=True)#for function overloading
    def DownloadFiles(self, fromDate, toDate, destination, unzipSwitch=True):
        """
        Download Mozart model files for the given date period to save downloadPath

        :param fromDate: Start Date(datetime)
        :param toDate: End Date(datetime)
        :param destination: local file path to save the downloaded files
        :param unzipSwitch: if true, the zip file is unzipped after downloading
        :return:
        """
        filedir = destination
        if not os.path.exists(filedir):
            raise Exception('{0} is not exist path :'.format(filedir))

        files = self.GetFileList()
        if files == None:
            print('There is no data')
            pass

        downloadFiles = []
        for fname in files:
            tmp = os.path.splitext(fname)
            if tmp.__len__() < 2:
                continue

            dateStr = tmp[0][-14:]
            try:
                runTime = datetime.strptime(dateStr, '%Y%m%d%H%M%S')
            except:
                print('{0} cannot recognize date :'.format(fname))
                continue

            if fromDate > runTime or runTime > toDate:
                continue

            downloadFiles.append(fname)
        if downloadFiles.__len__() == 0:
            print('There is no data to download : {0} ~ {1}'.format(fromDate, toDate))
            pass

        self.DownloadFiles(downloadFiles, destination, unzipSwitch)

    @dispatch(int, str, bool=True)
    def DownloadFiles(self, count, destination, unzipSwitch = True):
        """
        Download Mozart model files based on the given number of recently created models

        :param count: Number of models to download
        :param destination: local file path to save the downloaded files
        :param unzipSwitch: if true, the zip file is unzipped after downloading
        :return:
        """

        self.__checkDir__(destination)

        files = self.GetFileList()

        downloadFiles = []
        chkCnt = 0
        for fname in files:
            if chkCnt == count:
                break
            downloadFiles.append(fname)
            chkCnt += 1

        self.DownloadFiles(downloadFiles, destination, unzipSwitch)




