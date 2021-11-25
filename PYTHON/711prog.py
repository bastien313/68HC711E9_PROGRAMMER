import M68HC711E9 as hc
import logger as lg
import binView as bw
import S19 as s19

log = lg.logger()
device = hc.M68HC711E9(log,'COM1')

#bw.printBinaryS19('BTROM.S19')
#device.writeEProm([0xAB, 0xC8],0xFEF6, 2)

#epromData = device.readEProm(0xFEF0,256)


#bw.printBinaryData(epromData[1:], 0xFEF0)



#addressToRead = device.epromStart
#bw.printBinaryData(device.readMemory(addressToRead,512)[1:], addressToRead)

#device.writeEEProm([0,0xAB,0X15,0xFF], device.eepromStart, 4)




print('    ********************************************')
print('    *        Modern 68HC711E9 programmer       *')
print('    *                  V1.0                    *')
print('    *             BY B.S 11/2021               *')
print('    *                  OXILEC                  *')
print('    ********************************************')

print('Enter a command, type help for more information')

while 1:
    command = input(">")

    if command == 'help':
        print('read - read memory (EPROM or EEPROM) from 68HC711E9')
        print('write - write memory (EPROM or EEPROM) from 68HC711E9')

    elif command == 'readS19':
        fileName = input("Enter file name:  ")
        bw.printBinaryS19(fileName)
    elif command == 'read':
        address = int(input("Enter start address in hexadecimal:  "),16)
        size = int(input("Enter lengt of read in decimal:"))
        config = int(input("New config register in hexadecimal, default = 0x0F:  "),16)
        input("Make reset and press ENTER")
        bw.printBinaryData(device.readMemory(address, size, config), address)
        
    elif command == 'write':
        fileName = input("Enter file name:  ")
        if 'S19' in fileName:
            bw.printBinaryS19(fileName)
            startAddress = s19.getStartAdress(s19.makeLineList(fileName))
            endAdress = s19.getDataSize(s19.makeLineList(fileName)) + startAddress
            print('{:04X}'.format(endAdress))
            if (startAddress >= device.epromStart) and (startAddress <= device.epromEnd) and (endAdress >= device.epromStart) and (endAdress <= device.epromEnd):
               input("Plance VPP 12V and press ENTER") 
            input("Make reset and press ENTER")
            device.writeMemoryFromS19(fileName)
