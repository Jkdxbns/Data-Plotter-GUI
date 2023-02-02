import os
import tkinter as tk
from tkinter import filedialog


class ImportData:

    def __init__(self):
        tk.Tk().withdraw()

    def importFiles(self):
        files = filedialog.askopenfilenames()  # filetypes=(("csv files", '*.csv'), ("txt files", "*.txt"))
        return self.checkFiles(files)

    def importDir(self):
        files = os.listdir(filedialog.askdirectory())
        return self.checkFiles(files)

    @staticmethod
    def checkFiles(files):
        allowed_extensions = [".txt", ".csv"]
        dataset = set()
        for filename in files:
            filename = str(filename)
            for extension in allowed_extensions:
                if filename.endswith(extension):
                    dataset.add(filename)
        return dataset


class listPorts:

    @staticmethod
    def getPorts():
        if os.name == 'nt':  # sys.platform == 'win32':
            from serial.tools.list_ports_windows import comports
            hits = 0
            comPortList = []
            iterator = sorted(comports(True))

            for n, (port, desc, hwid) in enumerate(iterator, 1):
                portName = "{}".format(port)
                # sys.stdout.write(portName)
                comPortList.append(portName)
                hits += 1

            if hits == 0:
                # sys.stderr.write("no ports found\n")
                return
            return comPortList

        else:
            raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))
