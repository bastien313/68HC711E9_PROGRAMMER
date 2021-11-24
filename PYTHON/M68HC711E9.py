import serial
import time
import serial.tools.list_ports
import sys
import logger
import S19 as s19


class TimeOutError(Exception):
    pass
class SerialException(Exception):
    pass

class M68HC711E9:
    def __init__(self,logger,comPort):
        self.logger = logger
        self.binDataFile = 0
        self.serialPort = 0
        self.comPortStr = comPort
        
        #device definition
        self.epromStart = 0xD000
        self.epromEnd = 0xFFFF
        self.eepromStart = 0xB600
        self.eepromEnd = 0xB7FF
        self.readPromBootloader = 'A8NS3P.TSK'
        self.p_prom = 3
        
        
        
    def __serialOpen(self, speed):
        try:
            self.serialPort = serial.Serial(self.comPortStr, speed)
        except:
            self.serialPort = 0
            raise SerialException

    def __serialClose(self):
        if self.serialPort != 0:
            self.serialPort.close()
            self.serialPort = 0
       
        
        
    def uploadBootloaderFromS19(self, bootLoaderS19):  
        lineList = s19.makeLineList(bootLoaderS19)
        binaryDat = s19.makeBinaryList(lineList)
        self.uploadBootloader(binaryDat)
        
    def uploadBootloader(self, binaryData):
        """ Send bootloader to the device.
            binaryData: Binary data of bootLoader
        """
        self.__serialClose()
        try:
            self.__serialOpen(1200)
            
        except:
            self.logger.printCout('Unable to open {}'.format(self.comPortStr))
     
        else:
            self.logger.printCout('Open OK')
            self.serialPort.write(0xFF.to_bytes(1, 'big'))
            #self.serialPort.write(binaryData)
            for data in binaryData:
                self.serialPort.write(data.to_bytes(1, 'big'))
                self.logger.printCout('Send {}'.format(data))
            print('TX')
            print(binaryData)
            echo = list(self.serialPort.read(len(binaryData)))
            print('TX')
            print(echo)
            
            if echo == binaryData:
                self.logger.printCout('Bootloader OK')
            else:
                self.logger.printCout('Error bootloader')
        
        self.__serialClose()
        
    def readProm(self, startAddress, endAddress):
        fileData = open(self.readPromBootloader,'rb').read()
        fileData = list(fileData)
        fileData[2] = self.p_prom 
        fileData[3] = 0x0F #CONFIG register
        fileData[4] = (startAddress & 0xFF00) >> 8
        fileData[5] =  startAddress & 0x00FF
        fileData[6] = (endAddress & 0xFF00) >> 8
        fileData[7] =  endAddress & 0x00FF
        
        self.uploadBootloader(fileData)
        
        try:
            self.__serialOpen(9600)
        except:
            self.logger.printCout('Unable to open {}'.format(self.comPortStr))
            return 0
     
        else:
            self.logger.printCout('Open OK')
            self.serialPort.write('L'.encode('utf-8'))
            return self.serialPort.read( (endAddress-startAddress) + 2)
        