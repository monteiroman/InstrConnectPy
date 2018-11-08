#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:35:23 2018

@author: tiago
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import math as mat
import time

# Traemos la libreria VISA
import pyvisa as visa

# Agreamos el path de las librerias
sys.path.insert(0, 'Libreria')
# Traemos la clase base que implmenta las funciones de VISA
from instrument import Instrument


def StartMeasure(instrument, points=256):

    instrument.write("DISP:ANAL:MODE MAGN")
    setPoints = "SENS:WAV:POIN " + str(points)
    instrument.write(setPoints)
    instrument.write("TRIG:GRAP:SOUR IMM")
    instrument.write("INIT:GRAP (@1)")

    aux = "1"
    while int(aux) is not 0:
        instrument.write("STAT:OPER:COND?")
        aux = instrument.read()
        print(aux)
        time.sleep(1)

    instrument.write("FETC:ARR? (@1) ")
    message = instrument.read_raw()

    #print(f"type #: {type(message[0])}")
    if message[0] != 35:
        print("No se pudieron obtener los puntos")
        return 0,0,-1

    # file = open("RAW_Message", "wb")
    # file.write(message)
    # file.close()

    # convert ascii to int. First number of the file
    digits = message[1:2][0] - 48
    print(f"type digits: {type(digits)} = {digits}")

    # extract the number of bytecount
    count = message[2:2+digits]
    #print(f"type count: {type(count)} = {count}")
    # convert bytes to string
    bytecount = count.decode("utf-8")
    print(f"type count: {type(bytecount)} = {bytecount}")

    # string2int
    bytecount = int(bytecount)
    #print(f"type count: {type(aux)} = {aux}")

    # file info data chop
    bytesData = message[2+digits:-1]
    print(f"type count: {type(bytesData)}")

    y = np.frombuffer(bytesData, dtype=np.float32, count=256, offset=0)
    y = y.newbyteorder()
    print (y)
    print (len(y))

    x = np.empty(points)
    filler = np.arange(0,points,1)
    index = np.arange(x.size)
    np.put(x,index,filler)

    return x,y,1

def AnalyzeFile(points=256):

    import struct

    with open("RAW_Message", "rb") as file:
        message = file.read()
    file.close()

    # convert ascii to int. First number of the file
    digits = message[1:2][0] - 48
    print(f"type digits: {type(digits)} = {digits}")

    # extract the number of bytecount
    count = message[2:2+digits]
    #print(f"type count: {type(count)} = {count}")
    # convert bytes to string
    bytecount = count.decode("utf-8")
    print(f"type count: {type(bytecount)} = {bytecount}")

    # string2int
    bytecount = int(bytecount)
    #print(f"type count: {type(aux)} = {aux}")

    # file info data chop
    bytesData = message[2+digits:-1]
    print(f"type count: {type(bytesData)}")

    # converts file bytes in floats
    # y = []
    # for i in range(0, len(bytesData), 4):
    #     packed = bytesData[i:i+4]
    #     y.append(packed)
    #     # unpacked = struct.unpack("f", packed)
    #     # y.append(unpacked[0])
    # print (y)
    # print (len(y))
    #y = str(y)
    y = np.frombuffer(bytesData, dtype=np.float32, count=256, offset=0)
    y = y.newbyteorder()
    print (y)
    # print (len(y))

    x = np.empty(256)
    filler = np.arange(0,256,1)
    index = np.arange(x.size)
    np.put(x,index,filler)

    # plt.plot(x, y)
    # plt.grid(True)
    # plt.xlabel('Frequency [Hz]')
    # plt.ylabel('Magnitude [dB]')
    # plt.title('FFT')
    # plt.show()
    print(points)
    return x,y,1

# This main is left for debugging the measure file
if __name__ == '__main__':

    AnalyzeFile()