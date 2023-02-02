from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from Plotter import AddPlot


window_size = 1300, 1200*0.5625
_translate = QtCore.QCoreApplication.translate
UI_font = "Segoe UI"


def custom_font(family: str = UI_font, size: int = 9):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font

class GraphWindow(object):
    
    def __init__(self):
        self.pushButton = None
        self.tab_mainWindow = None
        self.centralwidget = None

    def receiveData(self, dict, filepath):
        AddPlot(dict=dict, parent=self.tab_mainWindow, filepath=list(filepath))
        self.tab_mainWindow.setCurrentIndex(self.tab_mainWindow.count()-2)

    def setupUi(self, MainWindow):
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setWindowTitle("Graph Main")
        MainWindow.resize(window_size[0], window_size[1])
        MainWindow.setMinimumSize(QtCore.QSize(window_size[0], window_size[1]))
        MainWindow.setMaximumSize(QtCore.QSize(window_size[0], window_size[1]))
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Tabs on window
        self.tab_mainWindow = self.Tab(self.centralwidget, [10, 10, window_size[0]-20, window_size[1]-60])
        self.tab_mainWindow.insertTab(0, QWidget(), "Main Tab")
        self.NewTab(self.tab_mainWindow)
        # button to remove tabs
        self.pushButton = self.PushButton(self.centralwidget, [window_size[0]-110, window_size[1]-45, 100, 40], name="Delete Tab")
        self.pushButton.setFont(custom_font())
        self.pushButton.clicked.connect(lambda: self.removeTab(self.tab_mainWindow))
        MainWindow.setCentralWidget(self.centralwidget)

    def Tab(self, parent: object, _list: list):
        """Creates a tab holder object"""
        tab = QTabWidget(parent)
        tab.setGeometry(QtCore.QRect(_list[0], _list[1], _list[2], _list[3]))
        tab.setFont(custom_font(size=10))
        tab.setTabPosition(QtWidgets.QTabWidget.South)
        tab.setTabShape(QtWidgets.QTabWidget.Triangular)
        tab.setUpdatesEnabled(True)
        tab.currentChanged.connect(lambda: self.NewTab(parent=tab))
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
    def removeTab(parent):
        if parent.count() != 2 and parent.currentIndex() != 0:
            parent.setCurrentIndex(parent.currentIndex()-1)
            parent.removeTab(parent.currentIndex()+1)

    @staticmethod
    def NewTab(parent):
        tab = QWidget()
        index = parent.count()
        if index - 1 == parent.currentIndex():
            parent.addTab(tab, '')
            parent.setTabText(parent.indexOf(tab), _translate("MainWindow", '  +  '))
            if parent.count() == 2:
                return
            parent.setTabText(parent.indexOf(tab)-1, _translate("MainWindow", "Tab "+f"{parent.count()-1}"))

    @staticmethod
    def PushButton(parent: object, _list: list, name: str = "P.Button"):
        button = QPushButton(parent)
        button.setGeometry(QtCore.QRect(_list[0], _list[1], _list[2], _list[3]))
        button.setText(name)
        button.setUpdatesEnabled(True)
        return button
    

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = GraphWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
