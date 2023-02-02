import sys
import pandas as pd
import serial
from PyQt5.QtWidgets import QMessageBox


def plotSerial(port):
    ser = None
    try:
        ser = serial.Serial(port)
    except:
        print(f"Couldnt connect to {port}")

    text = ser.readline().decode('utf-8')
    ser.close()
    text = text.split(',')
    text[-1] = text[-1][0:-2]
    return text


def getColumnName(file):
    column_name = []
    try:
        data = pd.read_csv(file)
    except:
        sys.stderr.write(f"Pandas couldn't read {file}")
        return column_name
    for i in data.columns:
        column_name.append(str(i))
    return column_name

def getContent(filepath):
    data = pd.read_csv(filepath)
