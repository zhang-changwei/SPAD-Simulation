import struct
import demjson
import pickle

# 4+3040+4+3040=6088, 2 channel, 1520个点

def BinRead(f='data/wave_record_0.bin'):
    '''-> 2d List'''
    yAllList = []

    data = open(f, 'rb')

    prehead = data.read(8)
    data.seek(0)
    while data.read(8)==prehead:
        yList = []
        stack = 0
        head = ''
        # head
        while True:
            h = data.read(1).decode()
            if h=='{': stack += 1
            elif h=='}': stack -= 1
            head = head + h
            if stack==0: break
        # print(head)
        headJ = demjson.decode(head)
        datalen = int(headJ['SAMPLE']['DATALEN']) # 1520

        for c in range(2):
            if headJ['CHANNEL'][c]['DISPLAY']=='ON' and c==0: #先丢掉ch2数据
                data.read(4)
                for i in range(datalen):
                    d = data.read(2)
                    data_short = struct.unpack('h', d)[0]
                    yList.append(data_short)
            else:
                data.read(4+2*datalen)
        yAllList.append(yList)

    data.close()
    with open(f+'.pickle', 'wb') as pf:
        pickle.dump(yAllList, pf)
    return yAllList
