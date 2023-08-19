#! usr/bin/env python 3
# coding=utf-8
import struct
import numpy as np

__autor__ = 'Ulises García Calderón'

class IOBinFile():
    def __init__(self):
        '''Constructor de la clase'''

    def ReadBinFloatFileIEEE754(self, path: str) -> list:
        handle = open(path, 'rb')
        datastr = handle.read()
        data = list(struct.unpack('<%df' % (len(datastr)/4), datastr))
        return data

    def WriteBinFloatFileIEEE754(self, fileName: str, arreglo: np.array) -> open:
        with open(fileName, 'wb') as handle:
            handle.write(struct.pack('<%df' % len(arreglo), *arreglo))


