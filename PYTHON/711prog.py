import M68HC711E9 as hc
import logger as lg

log = lg.logger()
device = hc.M68HC711E9(log,'COM19')



print(device.readProm(device.epromStart,device.epromStart+50))


