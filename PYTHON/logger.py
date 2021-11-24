import sys
from time import strftime
from datetime import datetime


class logger:
    def __init__(self):
        self.ihmDirect = 0
        self.logFile = open("log.txt", "w")



    def printCerr(self,str):
        sys.stderr.write(self._getStrTime()+ str+'\n')

    def printCout(self,str):
        sys.stdout.write(self._getStrTime()+ str+'\n')
        self.printLogFile(str)

    def printLogFile(self,str):
        self.logFile.write(self._getStrTime()+ str+'\n')
        self.logFile.flush()

    def _getStrTime(self):
        myDatetime = datetime.now()
        myStr = '<'
        myStr += myDatetime.strftime('%Y-%m-%d %H:%M:%S')
        myStr += '> '
        return myStr