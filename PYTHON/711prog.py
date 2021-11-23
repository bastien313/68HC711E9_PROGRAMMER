import S19 as s19

#Prompt user for file name. Save file name to var.
file_name= 'BTROM.S19'
#Read file to memory.
f=open(file_name,'r')
#Store file data to var.
f_data=f.read()
#Breakdown S19 records into list.
g='\r\n'
if g in f_data:
    h=f_data.split(g)
else:
    h=f_data.split('\n')

#Print total number of records.
print(file_name + ' has ' + str(len(h)) + ' records.')
#Make list of the count of different type of S records.

print(s19.bytecount_byte(h))

print(s19.makeBinaryList(h))
#print(s19.getDataList(h))
