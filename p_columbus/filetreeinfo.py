import os
from datetime import datetime
import time

class FileInfo:
    filetype = ''
    authority = ''
    nohardlink = 0
    user = ''
    group = ''
    size = 0
    ctime = 0
    path = ''

    # 这里的file是一整条属性信息
    def __init__(self, file):
        self.filetype = self.getFileType(file)
        self.authority = self.getAuthority(file)
        self.nohardlink = self.getNohardlink(file)
        self.user = self.getUser(file)
        self.group = self.getGroup(file)
        self.size = self.getSize(file)
        self.ctime = self.getCtime(file)
        self.path = self.getPath(file)

    def getFileType(self, file):
        return file[0]

    def getAuthority(self, file):
        return file[1:10]

    def getNohardlink(self, file):
        return int(file.split(' ')[1])

    def getUser(self, file):
        return file.split(' ')[2]

    def getGroup(self, file):
        return file.split(' ')[3]

    def getSize(self, file):
        return int(file.split(' ')[4].replace(',', ''))

    def getCtime(self, file):
        ads = file.index('/')
        ctime_str = file[ads - 36:ads - 13].strip()
        datetime_obj = datetime.strptime(ctime_str, "%Y-%m-%d %H:%M:%S.%f")
        ctime_int = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)  # ctime_int
        return ctime_int

    def getPath(self, file):
        ads = file.find('/')
        ade = file.find('>') - 2 if file.find('>') != -1 else None
        path = file[ads:ade]
        return path

    def getFiletree(self):
        filetree=os.popen('find  / | xargs ls -lcd --full-time ').readlines()