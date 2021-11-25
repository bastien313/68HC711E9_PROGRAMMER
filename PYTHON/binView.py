import S19 as s19

def printBinaryS19(s19File):
    lineList = s19.makeLineList(s19File)
    binList = s19.makeBinaryList(lineList)
    startAdr = s19.getStartAdress(lineList)
    printBinaryData(binList, startAdr)

def printBinaryData(binaryData, startAdrress = 0):
    print(binaryFormatText(binaryData, startAdrress))

def binaryFormatText(binaryData, startAdrress = 0):
    binaryID = 0
    adress = startAdrress
    textOut = ''
    sizeData = len(binaryData)
    
    
    #Print top information
    textOut = '     ' 
    for lowerAdress in range(0,16):
        textOut += '{:02X} '.format(lowerAdress)
    textOut += '\n'
        
    while binaryID < sizeData:
        textOut += '{:04X} '.format(adress)
        for lowerAdress in range(0,16):
            if binaryID < sizeData:
                textOut += '{:02X} '.format(binaryData[binaryID])
            binaryID += 1
        textOut += '\n'
        adress += 16
    return textOut