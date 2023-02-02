import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PlotterWindow import GraphWindow
from LoadData import ImportData, listPorts
from ReadData import getColumnName, plotSerial

window_size = 900, 480
_translate = QtCore.QCoreApplication.translate
UI_font = "Segoe UI"
dataset = set([])
deviceset = set([])


def custom_font(family: str = UI_font, size: int = 10):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font


def getDevices():
    global deviceset
    devices = listPorts().getPorts()
    if devices is None:
        return
    for i in devices:
        deviceset.add(i)


def getFiles(tipe):
    global dataset
    data = ImportData()
    files = []
    if tipe == 'all':
        files = data.importDir()
    elif tipe == 'single':
        files = data.importFiles()
    for _ in files:
        dataset.add(_)


class Ui_Graph(QMainWindow):

    def openGrapher(self):
        if not (self.radio_modeData.isChecked() or self.radio_modeLive.isChecked()):
            QMessageBox.warning(self, "Plot Warning!", "Nothing selected")
            return
        if self.radio_modeData.isChecked():
            if len(dataset) == 0:
                QMessageBox.warning(self, "Plot Warning!", "No data to plot.")
                return
        elif self.radio_modeLive.isChecked():
            if len(deviceset) == 0:
                QMessageBox.warning(self, "Plot Warning!", "No devices to plot.")
                return
        self.win = QMainWindow()
        self.ux = GraphWindow()
        self.ux.setupUi(self.win)
        self.ux.receiveData(dict=self.sendData(), filepath=dataset)
        self.win.show()

    def __init__(self):
        super(Ui_Graph, self).__init__()
        # QtCore.QMetaObject.connectSlotsByName(self)
        self.win = None
        self.ux = None
        self.resize(window_size[0], window_size[1])
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        self.setMinimumSize(window_size[0], window_size[1])
        self.setMaximumSize(window_size[0], window_size[1])
        self.setWindowTitle("Grapher Configure")
        self.setStyleSheet("""
        QMainWindow{
            background: rgb(220, 220, 220);
            color: rgb(0,0,0);
        }
        
        QMenuBar{
            background: rgb(190,190,190);
        }
        
        QMenuBar::item::Selected{
            background: rgb(230, 230, 230);
        }
        
        QMenu{
            background: rgb(230,230,230);
            color: rgb(0,0,0);
        }
        
        QMenu::item::Selected{
            background: rgb(190,190,190)
        }
        
        """)
        # Central Widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        # Main Frame
        self.frame = self.Frame(self.centralwidget, [10, 10, 880, 420])
        self.frame.setFont(custom_font())
        self.frame.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        # Button to call GRAPH WINDOW and push contents onto it
        self.button_plot = self.PushButton(self.frame, [595, 350, 80, 40], name="Plot")
        font = QtGui.QFont()
        font.setFamily(UI_font)
        font.setPointSize(12)
        self.button_plot.setFont(font)
        self.button_plot.setShortcut('Ctrl+space')
        self.button_plot.clicked.connect(lambda: self.openGrapher())
        # self.button_plot.clicked.connect(self.selectedMedia)
        # All boxes and their radiobutton
        self.box_mode = self.Box(parent=self.frame, _list=[10, 10, 200, 100], name="Mode")

        self.radio_modeLive = self.RadioButton(parent=self.box_mode, _list=[10, 25, 180, 30], name="Live mode")
        self.radio_modeLive.clicked.connect(lambda: self.box_deviceList.setEnabled(True))
        self.radio_modeLive.clicked.connect(lambda: self.box_dataList.setEnabled(False))
        self.radio_modeLive.clicked.connect(lambda: self.menu_importData.setEnabled(False))

        self.radio_modeData = self.RadioButton(parent=self.box_mode, _list=[10, 60, 180, 30], name="Existing Datasets")
        self.radio_modeData.clicked.connect(lambda: self.box_dataList.setEnabled(True))
        self.radio_modeData.clicked.connect(lambda: self.box_deviceList.setEnabled(False))
        self.radio_modeData.clicked.connect(lambda: self.menu_importData.setEnabled(True))

        self.box_plotSelector = self.Box(parent=self.frame, _list=[220, 10, 200, 100], name="Plot Control")
        self.radio_plotPlotAll = self.RadioButton(parent=self.box_plotSelector, _list=[10, 25, 180, 30], name="Plot all")
        self.radio_plotPlotAll.clicked.connect(lambda: self.box_axesPlotter.setEnabled(False))
        self.button_plotSelect = self.PushButton(parent=self.box_plotSelector, _list=[20, 60, 140, 30], name="Refresh plot selector")
        self.button_plotSelect.setShortcut('Ctrl+P')
        self.button_plotSelect.clicked.connect(lambda: self.box_axesPlotter.setEnabled(True))
        self.button_plotSelect.clicked.connect(lambda: self.radio_plotPlotAll.setChecked(False))
        self.button_plotSelect.clicked.connect(self.updatePlotSelector)
        self.box_axesPlotter = self.Box(parent=self.frame, _list=[10, 120, 410, 300], name="Plot selector")
        self.box_axesPlotter.setEnabled(False)

        # Data List Box
        self.box_dataList = self.Box(self.frame, [430, 10, 200, 300], name="Data List")
        self.selectAll = self.PushButton(parent=self.box_dataList, _list=[10, 260, 180, 30], name="Select All")
        self.selectAll.setShortcut('Ctrl+A')
        self.selectAll.clicked.connect(self.select_all)
        self.box_dataList.setEnabled(False)
        self.dataVertLayout = QtWidgets.QWidget(self.box_dataList)
        self.dataVertLayout.setGeometry(QtCore.QRect(10, 30, 190, 230))
        self.layout_dataList = QVBoxLayout(self.dataVertLayout)
        self.layout_dataList.setAlignment(QtCore.Qt.AlignTop)

        # Device List Box
        self.box_deviceList = self.Box(self.frame, [640, 10, 200, 300], name="Device List")
        self.refreshDevList = self.PushButton(parent=self.box_deviceList, _list=[10, 260, 180, 30], name="Refresh List")
        self.refreshDevList.setShortcut('Ctrl+R')
        self.refreshDevList.clicked.connect(getDevices)
        self.refreshDevList.clicked.connect(self.updateDeviceList)
        self.box_deviceList.setEnabled(False)
        self.deviceVertLayout = QWidget(self.box_deviceList)
        self.deviceVertLayout.setGeometry(QtCore.QRect(10, 30, 190, 230))
        self.layout_deviceList = QVBoxLayout(self.deviceVertLayout)
        self.layout_deviceList.setAlignment(QtCore.Qt.AlignTop)
        self.setCentralWidget(self.centralwidget)

        self.tab_axesSelector = self.Tab(self.box_axesPlotter, [0, 20, 410, 280])

        self.Xaxis = QScrollArea()
        self.x_contentWidget = QWidget()
        self.Xaxis.setWidget(self.x_contentWidget)
        self.Xaxis.setWidgetResizable(True)
        self.layout_xaxis = QVBoxLayout(self.x_contentWidget)
        self.tab_axesSelector.addTab(self.Xaxis, "")
        self.tab_axesSelector.setTabText(self.tab_axesSelector.indexOf(self.Xaxis), _translate("self", "X-axis"))

        self.Yaxis = QScrollArea()
        self.y_contentWidget = QWidget()
        self.Yaxis.setWidget(self.y_contentWidget)
        self.Yaxis.setWidgetResizable(True)
        self.layout_yaxis = QVBoxLayout(self.y_contentWidget)
        self.tab_axesSelector.addTab(self.Yaxis, "")
        self.tab_axesSelector.setTabText(self.tab_axesSelector.indexOf(self.Yaxis), _translate("self", "Y-axis"))

        # self.plot_type = QScrollArea()
        # self.tab_axesSelector.addTab(self.plot_type, "")
        # self.tab_axesSelector.setTabText(self.tab_axesSelector.indexOf(self.plot_type), _translate("self", "Plot Type"))

        # End of central Widget now Menu Bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 26))

        # MenuBar File and its children
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.menu_file.setTitle(_translate("self", "File"))  # File
        self.menubar.addAction(self.menu_file.menuAction())

        self.file_saveData = QtWidgets.QAction(self)
        # self.file_saveData.setShortcut(_translate("self", "Ctrl+S"))
        self.file_saveData.setText(_translate("self", "Save Data"))
        self.menu_file.addAction(self.file_saveData)

        self.menu_importData = QtWidgets.QMenu(self.menu_file)
        self.menu_file.addAction(self.menu_importData.menuAction())
        self.menu_importData.setTitle(_translate("self", "Import Data"))
        self.menu_importData.setEnabled(False)

        self.file_import_file = QtWidgets.QAction(self)
        # self.file_import_file.setShortcut(_translate("self", "Ctrl+O"))
        self.file_import_file.setText(_translate("self", "From File"))
        self.file_import_file.setShortcut('Ctrl+O')
        self.menu_importData.addAction(self.file_import_file)
        self.file_import_file.triggered.connect(lambda: getFiles('single'))
        self.file_import_file.triggered.connect(self.updateDataList)

        self.file_import_dir = QtWidgets.QAction(self)
        # self.file_import_dir.setShortcut(_translate("self", "Ctrl+P"))
        # self.file_import_dir.setText(_translate("self", "From Directory"))
        # self.file_import_dir.setShortcut('Ctrl+P')
        # self.menu_importData.addAction(self.file_import_dir)
        self.file_import_dir.triggered.connect(lambda: getFiles('all'))
        self.file_import_dir.triggered.connect(self.updateDataList)

        # MenuBar Help and its children
        self.menuContact = QtWidgets.QMenu(self.menubar)  # Help
        self.menuContact.setTitle(_translate("self", "Contact Us"))
        self.menubar.addMenu(self.menuContact)
        # self.menuContact.triggered.connect(self.openContactUs)
        self.setMenuBar(self.menubar)

        # EOF
        self.show()

    def updateDataList(self):
        global dataset
        if not self.box_dataList.isEnabled():
            return
        myChildren = []
        for i in range(self.layout_dataList.count()):
            myChildren.append(self.layout_dataList.itemAt(i).widget().objectName())

        for file in dataset:
            file = os.path.basename(file)
            if file not in myChildren:
                self.layout_dataList.addWidget(QCheckBox(file, objectName=file))

    def select_all(self):
        for i in range(self.layout_dataList.count()):
            item = self.layout_dataList.itemAt(i).widget()
            item.setChecked(True)

    def updateDeviceList(self):
        global deviceset
        if not self.box_deviceList.isEnabled():
            return
        myChildren = []
        for i in range(self.layout_deviceList.count()):
            myChildren.append(self.layout_deviceList.itemAt(i).widget().objectName())

        if len(deviceset) == 0:
            QMessageBox.information(self, "Device List", "no ports found")
            return

        for file in deviceset:
            if file not in myChildren:
                self.layout_deviceList.addWidget(QCheckBox(file, objectName=file))

    def updatePlotSelector(self):
        for i in reversed(range(self.layout_xaxis.count())):
            self.layout_xaxis.removeWidget(self.layout_xaxis.itemAt(i).widget())
            self.layout_yaxis.removeWidget(self.layout_yaxis.itemAt(i).widget())
            
        global dataset
        if self.box_dataList.isEnabled():
            for i in range(self.layout_dataList.count()):
                item = self.layout_dataList.itemAt(i).widget()
                if item.isChecked():
                    for file in dataset:
                        if item.objectName() == os.path.basename(file):
                            columns = getColumnName(file)
                            box_x = QGroupBox(f"{item.objectName()}", objectName=f"{item.objectName()}")
                            box_y = QGroupBox(f"{item.objectName()}", objectName=f"{item.objectName()}")
                            gridLayout_x = QGridLayout()
                            gridLayout_y = QGridLayout()
                            x = 1
                            cols = 2
                            for j in range(int(len(columns)/cols)+1):
                                for k in range(cols):
                                    gridLayout_x.addWidget(QRadioButton(f"Col {x}", objectName=f"{columns[x-1]}"), j, k)
                                    gridLayout_y.addWidget(QCheckBox(f"Col {x}", objectName=f"{columns[x-1]}"), j, k)
                                    x += 1
                                if x == len(columns):
                                    break
                            box_x.setLayout(gridLayout_x)
                            box_y.setLayout(gridLayout_y)
                            self.layout_xaxis.addWidget(box_x)
                            self.layout_yaxis.addWidget(box_y)

        global deviceset
        if self.box_deviceList.isEnabled():
            for i in range(self.layout_deviceList.count()):
                item = self.layout_deviceList.itemAt(i).widget()
                if item.isChecked():
                    for file in deviceset:
                        columns = plotSerial(str(item.objectName()))
                        box_x = QGroupBox(f"{item.objectName()}", objectName=f"{item.objectName()}")
                        box_y = QGroupBox(f"{item.objectName()}", objectName=f"{item.objectName()}")
                        gridLayout_x = QGridLayout()
                        gridLayout_y = QGridLayout()
                        x = 0
                        cols = 2
                        iteration = len(columns)/cols
                        if isinstance(iteration, float):
                            iteration = int(iteration)+1
                        for j in range(iteration):
                            for k in range(cols):
                                gridLayout_x.addWidget(QRadioButton(f"Col {x}", objectName=f"{columns[x-1]}"), j, k)
                                gridLayout_y.addWidget(QCheckBox(f"Col {x}", objectName=f"{columns[x-1]}"), j, k)
                                x += 1
                                if x == len(columns):
                                    break        
                        box_x.setLayout(gridLayout_x)
                        box_y.setLayout(gridLayout_y)
                        self.layout_xaxis.addWidget(box_x)
                        self.layout_yaxis.addWidget(box_y)

    @staticmethod
    def Tab(parent: object, _list: list):
        tab = QTabWidget(parent)
        tab.setGeometry(QtCore.QRect(_list[0], _list[1], _list[2], _list[3]))
        tab.setTabPosition(QtWidgets.QTabWidget.South)
        tab.setTabShape(QtWidgets.QTabWidget.Triangular)
        tab.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        tab.setFont(custom_font())
        return tab

    @staticmethod
    def Frame(parent, _list):
        frame = QFrame(parent)
        frame.setGeometry(QtCore.QRect(_list[0], _list[1], _list[2], _list[3]))
        frame.setMaximumSize(_list[2], _list[3])
        frame.setMinimumSize(QtCore.QSize(_list[2], _list[3]))
        frame.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        return frame

    @staticmethod
    def Box(parent: object = None, _list: list = None, name: str = 'box'):
        if parent is not None:
            box = QGroupBox(parent)
        else:
            box = QGroupBox(f"{name}")
        if _list is not None:
            box.setGeometry(QtCore.QRect(_list[0], _list[1], _list[2], _list[3]))
            box.setMinimumSize(QtCore.QSize(_list[2], _list[3]))
            box.setMaximumSize(QtCore.QSize(_list[2], _list[3]))
        box.setTitle(_translate("self", name))
        box.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        box.setFont(custom_font())
        box.setStyleSheet("background: rgb(230, 230, 230)")
        return box

    @staticmethod
    def RadioButton(parent: object, _list: list, name: str = "Radio"):
        radio = QRadioButton(parent)
        radio.setGeometry(QtCore.QRect(_list[0], _list[1], _list[2], _list[3]))
        radio.setText(name)
        radio.setFont(custom_font(size=9))
        radio.setUpdatesEnabled(True)
        return radio

    @staticmethod
    def PushButton(parent: object, _list: list, name: str = "P.Button"):
        button = QPushButton(parent)
        button.setGeometry(QtCore.QRect(_list[0], _list[1], _list[2], _list[3]))
        button.setText(name)
        button.setStyleSheet("background-color: rgb(200,200,200)")
        button.setUpdatesEnabled(True)
        return button

    def sendData(self):
        data = {'dataList': {}, 'deviceList': {}}

        if self.box_dataList.isEnabled():
            for i in range(self.layout_dataList.count()):
                file_name = self.layout_dataList.itemAt(i).widget()
                if file_name.isChecked():
                    data['dataList'][file_name.objectName()] = {'X-axis': [], 'Y-axis': []}

                    for j in range(self.layout_xaxis.count()):
                        item_x = self.layout_xaxis.itemAt(j).widget()
                        item_y = self.layout_yaxis.itemAt(j).widget()
                        if item_x.objectName() == file_name.objectName():
                            row_count = item_x.layout().rowCount()
                            col_count = item_x.layout().columnCount()

                            for row in range(row_count):
                                for col in range(col_count):
                                    try:             
                                        xaxis = item_x.layout().itemAtPosition(row, col).widget()
                                        yaxis = item_y.layout().itemAtPosition(row, col).widget()
                                    except AttributeWrror:
                                        pass
                                    if xaxis.isChecked():
                                        data['dataList'][file_name.objectName()]['X-axis'].append(xaxis.objectName())
                                    if yaxis.isChecked():
                                        data['dataList'][file_name.objectName()]['Y-axis'].append(yaxis.objectName())

        if self.box_deviceList.isEnabled():
            for i in range(self.layout_deviceList.count()):
                com_port = self.layout_deviceList.itemAt(i).widget()
                if com_port.isChecked():
                    data['deviceList'][com_port.objectName()] = {'X-axis': [], 'Y-axis': []}

                    for j in range(self.layout_xaxis.count()):
                        item_x = self.layout_xaxis.itemAt(j).widget()
                        item_y = self.layout_yaxis.itemAt(j).widget()
                        if item_x.objectName() == com_port.objectName():
                            row_count = item_x.layout().rowCount()
                            col_count = item_x.layout().columnCount()

                            x = 0
                            for row in range(row_count):
                                for col in range(col_count):             
                                    xaxis = item_x.layout().itemAtPosition(row, col).widget()
                                    yaxis = item_y.layout().itemAtPosition(row, col).widget()
                                    if xaxis.isChecked():
                                        data['deviceList'][com_port.objectName()]['X-axis'].append(xaxis.text())
                                    if yaxis.isChecked():
                                        data['deviceList'][com_port.objectName()]['Y-axis'].append(yaxis.text())
                                    x += 1
                                    if x == item_x.layout().count():
                                        break
        return data


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Graph()
    sys.exit(app.exec_())
