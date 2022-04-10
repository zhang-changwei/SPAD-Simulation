import struct
import demjson
import numpy as np
from matplotlib import pyplot as plt

yList = []
data = open('20000101_001126.bin', 'rb')
stack = 0
head = ''

h = data.read(10)

while True:
    h = data.read(1).decode()
    if h=='{': stack += 1
    elif h=='}': stack -= 1
    head = head + h
    if stack==0: break
print(head)
headJ = demjson.decode(head)
# datalen = headJ['SAMPLE']['DATALEN']
datalen = headJ['channel'][0]['Data_Length']
v_rate = headJ['channel'][0]['Voltage_Rate']
print(v_rate)
# datalen = 10000

for i in range(int(datalen)):
    d = data.read(2)
    data_short = struct.unpack('h', d)[0]
    yList.append(data_short)

print('\n', yList)
y = np.array(yList)
plt.plot(y)
plt.show()