#!/usr/bin/python3.10
# -*- coding: utf-8 -*-

# look it for more explains
# https://dev-gang.ru/article/python-i-pyqt-sozdanie-menu-panelei-instrumentov-i-strok-sostojanija-l7ubf6mm7n/
# https://russianblogs.com/article/84551088970/
# https://doc.qt.io/qt-5/qpalette.html

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QDesktopWidget, QAction, QTextEdit, QGridLayout, QMenuBar, QMenu, QDockWidget
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QGroupBox, QLabel, QLineEdit, QHBoxLayout, QDialog, QDialogButtonBox, QFormLayout, QSpinBox, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui

green = "#008800"
red = "#ff0000"
gray = "#8D8D8D"
dark_grey = "#6F6F5F"

class AppGUI(QMainWindow, QDialog):
    
    
    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        
        self._createActions_Menu()
        self._connectActions_Menu()

        self.Set_Shortcuts()
        self.Set_StatusTips()

        self.CreateToolbar()                        # zone with diffenerent instruments

        self.CreateMenuBar()                        # app's menu

        self.CreateWorkspace()

        self.Set_main_window_params()               # set main window params

        self.show()
    
    #-----------------Actions list-------------------
    def _createActions_Menu(self):
        self.newAction = QAction("&New...", self)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("Cut", self)
        self.changeColorAction = QAction("Change color", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)

    def _connectActions_Menu(self):
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        # self.openAction.triggered.connect(self.openAction)
        # self.saveAction.triggered.connect(self.saveAction)
        self.exitAction.triggered.connect(self.close)
        # # Connect Edit actions
        # self.copyAction.triggered.connect(self.copyAction)
        # self.pasteAction.triggered.connect(self.pasteAction)
        # self.cutAction.triggered.connect(self.cutAction)
        self.changeColorAction.triggered.connect(self.changeColor)
        # # Connect Help actions
        # self.helpContentAction.triggered.connect(self.helpAction)
        # self.aboutAction.triggered.connect(self.aboutAction)
        pass
    #------------------------------------------------

    #--------------------Actions---------------------
    def newFile(self):
        # print("lol")
        pass
    
    def changeColor(self):
        self.color = gray

        pal = self.palette()
        
        pal.setColor(QtGui.QPalette.Normal, QtGui.QPalette.Window, QtGui.QColor(self.color))
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor(self.color))
        
        self.setPalette(pal)
    
    def clearTextbox(self):

        pass

    def getText(self):
        textboxValue = self.smallEditor.toPlainText()           # text from smallEditor
        if textboxValue != "":
            if textboxValue[-3:] == ".py":
                # print(textboxValue)
                pass
            else:
                self.Set_Notification("It isn't py file.")

        else:
            self.Set_Notification("Program has not been chosen.")
    #------------------------------------------------

    #---------------------Fitcha---------------------
    def Set_Shortcuts(self):
        self.exitAction.setShortcut('Alt+Q')
    
    def Set_StatusTips(self):
        self.exitAction.setStatusTip('Exit application')
    
    def Set_Notification(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Warning.")
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)

        msg.exec_()
    #------------------------------------------------

    #-----------------Main elements------------------
    def CreateMenuBar(self):
        menuBar = self.menuBar()
        # --------------File menu--------------
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addSeparator()                             # separator
        fileMenu.addAction(self.exitAction)

        # --------------Edit menu--------------
        editMenu = menuBar.addMenu("&Edit")
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)
        editMenu.addAction(self.cutAction)
        editMenu.addSeparator()                             # separator
        editMenu.addAction(self.changeColorAction)                             # separator

        # --------------Help menu--------------
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        helpMenu.addAction(self.aboutAction)
        
        self.menuBar().setNativeMenuBar(False)              # for correct view

    def CreateToolbar(self):
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(self.exitAction)
    
    def CreateWorkspace(self):
        self.create_InputZone()
        self.create_DemoZone()
        

        mainLayout = QVBoxLayout()                          # Вертикальная компоновка
        mainLayout.addWidget(self.gridGroupBox)
        mainLayout.addWidget(self.bigEditor)
        mainLayout.addWidget(self.buttonBox)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def create_InputZone(self):
        self.gridGroupBox = QGroupBox()
        layout = QGridLayout()

        self.smallEditor = QTextEdit()
        self.smallEditor.setToolTip("Input py file name here.")     # prompt

        self.run_btn = QPushButton("&Run")
        self.run_btn.clicked.connect(self.getText)

        self.clear_btn = QPushButton("&Clear")
        self.clear_btn.clicked.connect(self.smallEditor.clear)

        layout.addWidget(self.smallEditor, 0, 1, 2, 1)      # (widget, row, col, count_rows, count cols)
        layout.addWidget(self.run_btn, 0, 0)                # (widget, row, col)
        layout.addWidget(self.clear_btn, 1, 0)

        layout.setColumnStretch(0, 5)      # buttons         (column, stretch)  5 and 20 => 5/25
        layout.setColumnStretch(1, 20)      # smallEditor                       20 and 5 => 20/25
        self.gridGroupBox.setLayout(layout)

    def create_DemoZone(self):
        self.bigEditor = QTextEdit()
        self.bigEditor.setPlainText(
            "Interaction with the program will be here."
        )
        
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    #------------------------------------------------

    def Set_main_window_params(self):
        self.setWindowTitle('Main window')    
        # self.setGeometry(300, 300, 350, 250)

        # self.resize(350, 250)                       # (width, height)
        self.center()
        
        self.setWindowTitle('Example')
        self.statusBar().showMessage('Ready')

        self.color = "#FFFFFF"

        self.setAcceptDrops(True)

    #-------------------Events-----------------------
    def contextMenuEvent(self, event):                      # if call context menu
        
        context_menu = QMenu(self)
        
        context_menu.addAction(self.newAction)
        context_menu.addAction(self.openAction)
        context_menu.addAction(self.saveAction)
        context_menu.addAction(self.exitAction)
        
        context_menu.exec(event.globalPos())                # show context menu

    def closeEvent(self, event):                            # if app will close
        pal = self.palette()
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor(red))
        pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, QtGui.QColor(red))
        self.setPalette(pal)
        
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.No |
            QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            pal = self.palette()
            pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Window, QtGui.QColor(self.color))
            pal.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, QtGui.QColor(self.color))
            self.setPalette(pal)
            event.ignore()
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        # for f in files:
        #     print(f)
        pass
    #------------------------------------------------

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = AppGUI()
    sys.exit(app.exec_())



def lol():
    # #!/usr/bin/python3.10
    # # -*- coding: utf-8 -*-

    # # look it for more explains
    # # https://dev-gang.ru/article/python-i-pyqt-sozdanie-menu-panelei-instrumentov-i-strok-sostojanija-l7ubf6mm7n/

    # import sys
    # from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QDesktopWidget, QAction, QTextEdit, QGridLayout, QMenuBar, QMenu, QDockWidget
    # from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QGroupBox, QLabel, QLineEdit, QHBoxLayout, QDialog)
    # from PyQt5.QtGui import QIcon

    # class AppGUI(QMainWindow, QDialog):

    #     def __init__(self):
    #         super().__init__()

    #         self.initUI()


    #     def initUI(self):
            
    #         run_btn = QPushButton("Run")
    #         stop_btn = QPushButton("Stop")
            
    #         self._createActions_Menu()
    #         self._connectActions_Menu()

    #         self.Set_Shortcuts()
    #         self.Set_StatusTips()

    #         self.CreateToolbar()                        # zone with diffenerent instruments

    #         self.CreateMenuBar()                        # app's menu

    #         self.CreateWorkspace()

    #         self.Set_main_window_params()               # set main window params
    #         mainLayout = QVBoxLayout()
    #         mainLayout.addWidget(self.horizontalGroupBox)
    #         self.show()

    #     def _createActions_Menu(self):
    #         self.newAction = QAction("&New...", self)
    #         self.openAction = QAction("&Open...", self)
    #         self.saveAction = QAction("&Save", self)
    #         self.exitAction = QAction("&Exit", self)
    #         self.copyAction = QAction("&Copy", self)
    #         self.pasteAction = QAction("&Paste", self)
    #         self.cutAction = QAction("Cut", self)
    #         self.helpContentAction = QAction("&Help Content", self)
    #         self.aboutAction = QAction("&About", self)

    #     def _connectActions_Menu(self):
    #         # Connect File actions
    #         self.newAction.triggered.connect(self.newFile)
    #         # self.openAction.triggered.connect(self.openAction)
    #         # self.saveAction.triggered.connect(self.saveAction)
    #         self.exitAction.triggered.connect(self.close)
    #         # # Connect Edit actions
    #         # self.copyAction.triggered.connect(self.copyAction)
    #         # self.pasteAction.triggered.connect(self.pasteAction)
    #         # self.cutAction.triggered.connect(self.cutAction)
    #         # # Connect Help actions
    #         # self.helpContentAction.triggered.connect(self.helpAction)
    #         # self.aboutAction.triggered.connect(self.aboutAction)
    #         pass

    #     def newFile(self):
    #         print("lol")

    #     def Set_Shortcuts(self):
    #         self.exitAction.setShortcut('Alt+Q')
        
    #     def Set_StatusTips(self):
    #         self.exitAction.setStatusTip('Exit application')

    #     def CreateMenuBar(self):
    #         menuBar = self.menuBar()
    #         # --------------File menu--------------
    #         fileMenu = menuBar.addMenu("&File")
    #         fileMenu.addAction(self.newAction)
    #         fileMenu.addAction(self.openAction)
    #         fileMenu.addAction(self.saveAction)
    #         fileMenu.addSeparator()                             # separator
    #         fileMenu.addAction(self.exitAction)

    #         # --------------Edit menu--------------
    #         editMenu = menuBar.addMenu("&Edit")
    #         editMenu.addAction(self.copyAction)
    #         editMenu.addAction(self.pasteAction)
    #         editMenu.addAction(self.cutAction)

    #         # --------------Help menu--------------
    #         helpMenu = menuBar.addMenu("&Help")
    #         helpMenu.addAction(self.helpContentAction)
    #         helpMenu.addAction(self.aboutAction)
            
    #         self.menuBar().setNativeMenuBar(False)              # for correct view

    #     def CreateToolbar(self):
    #         toolbar = self.addToolBar('Exit')
    #         toolbar.addAction(self.exitAction)
        
    #     def CreateWorkspace(self):
    #         # textEdit = QTextEdit()
    #         # self.setCentralWidget(textEdit)

    #         self.horizontalGroupBox = QGroupBox("Horizontal layout")
    #         layout = QHBoxLayout()

    #         for i in range(4):
    #             button = QPushButton("Button %d" % (i + 1))
    #             layout.addWidget(button)

    #         self.horizontalGroupBox.setLayout(layout)

    #         pass

    #     def Set_main_window_params(self):
    #         self.setWindowTitle('Main window')    
    #         # self.setGeometry(300, 300, 350, 250)

    #         self.resize(350, 250)                       # (width, height)
    #         self.center()
            
    #         self.setWindowTitle('Example')
    #         self.statusBar().showMessage('Ready')

    #     def contextMenuEvent(self, event):                      # if call context menu
            
    #         context_menu = QMenu(self)
            
    #         context_menu.addAction(self.newAction)
    #         context_menu.addAction(self.openAction)
    #         context_menu.addAction(self.saveAction)
    #         context_menu.addAction(self.exitAction)
            
    #         context_menu.exec(event.globalPos())                # show context menu

    #     def closeEvent(self, event):                            # if app will close

    #         reply = QMessageBox.question(self, 'Message',
    #             "Are you sure to quit?", QMessageBox.No |
    #             QMessageBox.Yes)

    #         if reply == QMessageBox.Yes:
    #             event.accept()
    #         else:
    #             event.ignore()
        
    #     def center(self):
    #         qr = self.frameGeometry()
    #         cp = QDesktopWidget().availableGeometry().center()
    #         qr.moveCenter(cp)
    #         self.move(qr.topLeft())


    # if __name__ == '__main__':
        
    #     app = QApplication(sys.argv)
    #     ex = AppGUI()
    #     sys.exit(app.exec_())
    pass