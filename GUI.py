# Form implementation generated from reading ui file 'Excel_SQL_GUI.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(613, 579)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setSizeIncrement(QtCore.QSize(1, 1))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        MainWindow.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setSizeIncrement(QtCore.QSize(1, 1))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.inputButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputButton.sizePolicy().hasHeightForWidth())
        self.inputButton.setSizePolicy(sizePolicy)
        self.inputButton.setObjectName("inputButton")
        self.horizontalLayout.addWidget(self.inputButton)
        self.inputInput = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.inputInput.setObjectName("inputInput")
        self.horizontalLayout.addWidget(self.inputInput)
        self.sheetNumLabel = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sheetNumLabel.sizePolicy().hasHeightForWidth())
        self.sheetNumLabel.setSizePolicy(sizePolicy)
        self.sheetNumLabel.setMinimumSize(QtCore.QSize(60, 0))
        self.sheetNumLabel.setObjectName("sheetNumLabel")
        self.horizontalLayout.addWidget(self.sheetNumLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.sheetList = QtWidgets.QListWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sheetList.sizePolicy().hasHeightForWidth())
        self.sheetList.setSizePolicy(sizePolicy)
        self.sheetList.setObjectName("sheetList")
        self.horizontalLayout_3.addWidget(self.sheetList)
        self.columnList = QtWidgets.QListWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.columnList.sizePolicy().hasHeightForWidth())
        self.columnList.setSizePolicy(sizePolicy)
        self.columnList.setObjectName("columnList")
        self.horizontalLayout_3.addWidget(self.columnList)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.outputButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputButton.sizePolicy().hasHeightForWidth())
        self.outputButton.setSizePolicy(sizePolicy)
        self.outputButton.setObjectName("outputButton")
        self.horizontalLayout_2.addWidget(self.outputButton)
        self.outputIInput = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.outputIInput.setObjectName("outputIInput")
        self.horizontalLayout_2.addWidget(self.outputIInput)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.loadQueryButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadQueryButton.sizePolicy().hasHeightForWidth())
        self.loadQueryButton.setSizePolicy(sizePolicy)
        self.loadQueryButton.setObjectName("loadQueryButton")
        self.horizontalLayout_5.addWidget(self.loadQueryButton)
        self.saveQueryButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveQueryButton.sizePolicy().hasHeightForWidth())
        self.saveQueryButton.setSizePolicy(sizePolicy)
        self.saveQueryButton.setObjectName("saveQueryButton")
        self.horizontalLayout_5.addWidget(self.saveQueryButton)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.queryInput = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.queryInput.setObjectName("queryInput")
        self.horizontalLayout_7.addWidget(self.queryInput)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.executeButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.executeButton.sizePolicy().hasHeightForWidth())
        self.executeButton.setSizePolicy(sizePolicy)
        self.executeButton.setObjectName("executeButton")
        self.horizontalLayout_6.addWidget(self.executeButton)
        self.cancelButton = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_6.addWidget(self.cancelButton)
        spacerItem1 = QtWidgets.QSpacerItem(340, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.showTableButton = QtWidgets.QToolButton(parent=self.centralwidget)
        self.showTableButton.setObjectName("showTableButton")
        self.horizontalLayout_4.addWidget(self.showTableButton)
        self.fullscreenTableButton = QtWidgets.QToolButton(parent=self.centralwidget)
        self.fullscreenTableButton.setObjectName("fullscreenTableButton")
        self.horizontalLayout_4.addWidget(self.fullscreenTableButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.outputTable = QtWidgets.QTableView(parent=self.centralwidget)
        self.outputTable.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.outputTable.sizePolicy().hasHeightForWidth())
        self.outputTable.setSizePolicy(sizePolicy)
        self.outputTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.outputTable.setSortingEnabled(True)
        self.outputTable.setObjectName("outputTable")
        self.verticalLayout.addWidget(self.outputTable)
        self.verticalLayout.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 613, 21))
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionToggleTheme = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon.fromTheme("QIcon::ThemeIcon::WeatherClear")
        self.actionToggleTheme.setIcon(icon)
        self.actionToggleTheme.setObjectName("actionToggleTheme")
        self.actionSettings = QtGui.QAction(parent=MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionExit = QtGui.QAction(parent=MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.actionExit.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Excel SQL Query Tool"))
        self.inputButton.setText(_translate("MainWindow", " Select Input File "))
        self.sheetNumLabel.setText(_translate("MainWindow", "Sheets: 0"))
        self.outputButton.setText(_translate("MainWindow", " Select Output File "))
        self.loadQueryButton.setText(_translate("MainWindow", " Load SQL Query "))
        self.saveQueryButton.setText(_translate("MainWindow", " Save SQL Query "))
        self.executeButton.setText(_translate("MainWindow", " Execute Query "))
        self.cancelButton.setText(_translate("MainWindow", " Cancel Query "))
        self.showTableButton.setText(_translate("MainWindow", " v "))
        self.fullscreenTableButton.setText(_translate("MainWindow", " Fullscreen "))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionToggleTheme.setText(_translate("MainWindow", "Toggle Dark/Light Mode"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
