import serial
import time
import serial.tools.list_ports
import sys
import logger
import S19 as s19
import binView as bw


class TimeOutError(Exception):
    pass
class SerialException(Exception):
    pass
    
    


class MC68HC11:
    def __init__(self,logger,comPort):
        self.logger = logger
        self.binDataFile = 0
        self.serialPort = 0
        self.comPortStr = comPort
        
        #device definition
        self.epromStart = 0
        self.epromEnd = 0
        self.eepromStart = 0
        self.eepromEnd = 0
        self.readPromBootloader = ''
        self.p_prom = 0
        

        
        
        
    def serialOpen(self, speed):
        try:
            self.serialPort = serial.Serial(self.comPortStr, speed)
        except:
            self.serialPort = 0
            raise SerialException

    def serialClose(self):
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
        binaryData = list(binaryData)
        self.serialClose()
        try:
            self.serialOpen(1200)
            
        except:
            self.logger.printCout('Unable to open {}'.format(self.comPortStr))
     
        else:
            self.logger.printCout('Open OK')
            self.serialPort.write(0xFF.to_bytes(1, 'big'))
            #self.serialPort.write(binaryData)
            for data in binaryData:
                self.serialPort.write(data.to_bytes(1, 'big'))
            self.logger.printCout('Bootloader send')
            bw.printBinaryData(binaryData)
            echo = list(self.serialPort.read(len(binaryData)))
            self.logger.printCout('Bootloader echo')
            bw.printBinaryData(echo)
            
            if echo == binaryData:
                self.logger.printCout('Bootloader OK')
            else:
                self.logger.printCout('Error bootloader')
        
        
        #self.__serialClose()
        
    def writeEEPromFromS19(self, s19FileName):
        lineList = s19.makeLineList(s19FileName)
        writeEEProm(s19.makeBinaryList(lineList), s19.getStartAdress(lineList), s19.getDataSize(lineList))    
        
    def writeEEProm(self, data, startAddress, size, configRegister = 0x0F):
        if (startAddress >= self.eepromStart) and (startAddress <= self.eepromEnd) and (startAddress + (size-1) >= self.eepromStart) and (startAddress + (size-1) <= self.eepromEnd):
            bootloaderData = open(self.writeEEPromBootloader,'rb').read()
        else:
            self.logger.printCout('Address {:04X}-{:04X} out of range'.format(startAddress,startAddress + (size-1)))
            return 0
            
        bootloaderData = list(bootloaderData)
        endAddress = (startAddress + size) -1
        bootloaderData[2] = self.p_prom 
        bootloaderData[3] = configRegister#CONFIG register
        bootloaderData[4] = (startAddress & 0xFF00) >> 8
        bootloaderData[5] =  startAddress & 0x00FF
        bootloaderData[6] = (endAddress & 0xFF00) >> 8
        bootloaderData[7] =  endAddress & 0x00FF
        
        self.uploadBootloader(bootloaderData)
        self.serialClose()
        try:
            self.serialOpen(9600)
        except:
            self.logger.printCout('Unable to open {}'.format(self.comPortStr))
            self.serialClose()
            return 0
     
        else:
            self.logger.printCout('Open OK')
            self.serialPort.write('P'.encode('utf-8'))
            self.logger.printCout('EEprom erasing')
            self.serialPort.read(1)
            config = self.serialPort.read(1)[0]
            self.logger.printCout('CONFIG = {:02X}'.format(config))
            
            actualAddress = startAddress
            for intVal in data:
                self.serialPort.write(intVal.to_bytes(1, 'big'))
                resp = self.serialPort.read(1)[0]
                if intVal != resp:
                    self.logger.printCout('Error on {:04X}, write {:02X} != read {:02X}'.format(actualAddress ,intVal , resp))
                    self.serialClose()
                    return 0
                actualAddress +=1
            
            self.logger.printCout('Write succes :)')
            self.serialClose()
            return 1
            
            
        
    def readMemory(self, startAddress, size, configRegister = 0x0F):
        """Read slected memory
        """
        
        if (startAddress >= self.epromStart) and (startAddress <= self.epromEnd) and (startAddress + (size-1) >= self.epromStart) and (startAddress + (size-1) <= self.epromEnd):
            bootloaderData = open(self.readEPromBootloader,'rb').read()
        elif (startAddress >= self.eepromStart) and (startAddress <= self.eepromEnd) and (startAddress + (size-1) >= self.eepromStart) and (startAddress + (size-1) <= self.eepromEnd):
            bootloaderData = open(self.readEEPromBootloader,'rb').read()
        else:
            self.logger.printCout('Address {:04X}-{:04X} out of range'.format(startAddress,startAddress + (size-1) ))
            return 0
        
        bootloaderData = list(bootloaderData)
        endAddress = (startAddress + size) -1
        bootloaderData[2] = self.p_prom 
        bootloaderData[3] = configRegister#CONFIG register
        bootloaderData[4] = (startAddress & 0xFF00) >> 8
        bootloaderData[5] =  startAddress & 0x00FF
        bootloaderData[6] = (endAddress & 0xFF00) >> 8
        bootloaderData[7] =  endAddress & 0x00FF
        
        self.uploadBootloader(bootloaderData)
        self.serialClose()
        try:
            self.serialOpen(9600)
        except:
            self.logger.printCout('Unable to open {}'.format(self.comPortStr))
            return 0
     
        else:
            self.logger.printCout('Open OK')
            self.serialPort.write('L'.encode('utf-8'))
            return self.serialPort.read((endAddress-startAddress) + 2)[1:]
        
       

        

                    
                    
                
                
        
        
        
class M68HC711E9(MC68HC11):
    def __init__(self,logger,comPort):
        MC68HC11.__init__(self, logger, comPort)
        #device definition
        self.epromStart = 0xD000
        self.epromEnd = 0xFFFF
        self.eepromStart = 0xB600
        self.eepromEnd = 0xB7FF
        self.readEPromBootloader = 'A8NS3P.TSK'
        self.writeEPromBootloader = 'BTROM.S19'
        self.readEEPromBootloader = 'A8NS3E.TSK'
        self.writeEEPromBootloader = 'A8NS3E.TSK'
        self.p_prom = 3
    
    def writeMemoryFromS19(self, s19FileName, configRegister = 0x0F):
        lineList = s19.makeLineList(s19FileName)
        self.writeMemory(s19.makeBinaryList(lineList), s19.getStartAdress(lineList), s19.getDataSize(lineList), configRegister)  
    
    def writeMemory(self, data, startAddress, size, configRegister = 0x0F):
        if (startAddress >= self.epromStart) and (startAddress <= self.epromEnd) and (startAddress + (size-1) >= self.epromStart) and (startAddress + (size-1) <= self.epromEnd):
            self.writeEProm(data, startAddress, size)
        elif (startAddress >= self.eepromStart) and (startAddress <= self.eepromEnd) and (startAddress + (size-1) >= self.eepromStart) and (startAddress + (size-1) <= self.eepromEnd):
            self.writeEEProm(data, startAddress, size, configRegister)
        else:
            self.logger.printCout('Address {:04X}-{:04X} out of range'.format(startAddress,startAddress + (size-1) ))
            return 0
    
    def writeEPromFromS19(self, s19FileName):
        lineList = s19.makeLineList(s19FileName)
        writeEProm(s19.makeBinaryList(lineList), s19.getStartAdress(lineList), s19.getDataSize(lineList))    
        
    def writeEProm(self, data, startAddress, size):
        """Write data in eprom.
           size of data must be a multiple of 2. 
        """
        lineList = s19.makeLineList(self.writeEPromBootloader)
        bootloaderData = s19.makeBinaryList(lineList)
        
        bootloaderData[2] = (startAddress & 0xFF00) >> 8 
        bootloaderData[3] = startAddress & 0x00FF
        
        self.uploadBootloader(bootloaderData)
        
        #self.logger.printCout('Wait ready flag')  
        rdyFlag = self.serialPort.read(1)
        #self.logger.printCout('Rdy? {:02X}'.format(rdyFlag[0]))
        if rdyFlag[0] == 0xFF:
            idData = 0
            self.logger.printCout('Device ready')
            
            while idData < size:
                #Write and verify twice data
                nbDataToSend = 2 if ((size - idData) != 1) else 1
                dataVerify = []
                for nb in range(0,nbDataToSend):
                    dataVerify.append(data[idData])
                    self.serialPort.write(data[idData].to_bytes(1, 'big'))
                    #self.logger.printCout('Write {:02X} at {:04X}'.format(data[idData] , startAddress + idData))
                    idData +=1
                
                echo = list(self.serialPort.read(nbDataToSend))
                if echo != dataVerify:
                    for nb in range(0,nbDataToSend):
                        #print(idData - ( 1-nb) - 1)
                        self.logger.printCout('Error on {:04X}, write {:02X} != read {:02X}'.format(startAddress + (idData - ( 1-nb)) - 1 ,dataVerify[1-nb] , echo[1-nb]))
                    self.serialClose()
                    self.logger.printCout('Write abort')
                    return 0
        else:
            self.serialClose()
            self.logger.printCout('Device busy?')
            return 0
        self.serialClose()
        self.logger.printCout('Write succes :)')
                