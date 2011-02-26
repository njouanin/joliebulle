# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reader.ui'
#
# Created: Sun Feb  6 14:51:56 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!


#JolieBulle 2.0
#Copyright (C) 2010 Pierre Tavares

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 3
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1169, 733)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("Images/bulle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelRecette = QtGui.QLabel(self.centralwidget)
        self.labelRecette.setObjectName(_fromUtf8("labelRecette"))
        self.horizontalLayout.addWidget(self.labelRecette)
        self.lineEditRecette = QtGui.QLineEdit(self.centralwidget)
        self.lineEditRecette.setObjectName(_fromUtf8("lineEditRecette"))
        self.horizontalLayout.addWidget(self.lineEditRecette)
        self.labelRecetteV = QtGui.QLabel(self.centralwidget)
        self.labelRecetteV.setText(_fromUtf8(""))
        self.labelRecetteV.setObjectName(_fromUtf8("labelRecetteV"))
        self.horizontalLayout.addWidget(self.labelRecetteV)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelGenre = QtGui.QLabel(self.centralwidget)
        self.labelGenre.setObjectName(_fromUtf8("labelGenre"))
        self.horizontalLayout_2.addWidget(self.labelGenre)
        self.lineEditGenre = QtGui.QLineEdit(self.centralwidget)
        self.lineEditGenre.setObjectName(_fromUtf8("lineEditGenre"))
        self.horizontalLayout_2.addWidget(self.lineEditGenre)
        self.pushButtonChangerStyle = QtGui.QPushButton(self.centralwidget)
        self.pushButtonChangerStyle.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("Images/document-properties.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonChangerStyle.setIcon(icon1)
        self.pushButtonChangerStyle.setCheckable(True)
        self.pushButtonChangerStyle.setObjectName(_fromUtf8("pushButtonChangerStyle"))
        self.horizontalLayout_2.addWidget(self.pushButtonChangerStyle)
        self.comboBoxStyle = QtGui.QComboBox(self.centralwidget)
        self.comboBoxStyle.setObjectName(_fromUtf8("comboBoxStyle"))
        self.horizontalLayout_2.addWidget(self.comboBoxStyle)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2Volume = QtGui.QLabel(self.centralwidget)
        self.label_2Volume.setObjectName(_fromUtf8("label_2Volume"))
        self.horizontalLayout_4.addWidget(self.label_2Volume)
        self.doubleSpinBox_2Volume = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox_2Volume.setObjectName(_fromUtf8("doubleSpinBox_2Volume"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBox_2Volume)
        self.labelBoil = QtGui.QLabel(self.centralwidget)
        self.labelBoil.setObjectName(_fromUtf8("labelBoil"))
        self.horizontalLayout_4.addWidget(self.labelBoil)
        self.spinBoxBoil = QtGui.QSpinBox(self.centralwidget)
        self.spinBoxBoil.setObjectName(_fromUtf8("spinBoxBoil"))
        self.horizontalLayout_4.addWidget(self.spinBoxBoil)
        self.labelRendement = QtGui.QLabel(self.centralwidget)
        self.labelRendement.setObjectName(_fromUtf8("labelRendement"))
        self.horizontalLayout_4.addWidget(self.labelRendement)
        self.doubleSpinBoxRendemt = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBoxRendemt.setObjectName(_fromUtf8("doubleSpinBoxRendemt"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxRendemt)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBoxIng = QtGui.QCheckBox(self.centralwidget)
        self.checkBoxIng.setObjectName(_fromUtf8("checkBoxIng"))
        self.horizontalLayout_6.addWidget(self.checkBoxIng)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.labelFermentables = QtGui.QLabel(self.centralwidget)
        self.labelFermentables.setObjectName(_fromUtf8("labelFermentables"))
        self.verticalLayout.addWidget(self.labelFermentables)
        self.tableViewF = QtGui.QTableView(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableViewF.sizePolicy().hasHeightForWidth())
        self.tableViewF.setSizePolicy(sizePolicy)
        self.tableViewF.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.tableViewF.setAlternatingRowColors(True)
        self.tableViewF.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableViewF.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableViewF.setShowGrid(False)
        self.tableViewF.setGridStyle(QtCore.Qt.NoPen)
        self.tableViewF.setObjectName(_fromUtf8("tableViewF"))
        self.tableViewF.horizontalHeader().setCascadingSectionResizes(True)
        self.tableViewF.horizontalHeader().setDefaultSectionSize(175)
        self.tableViewF.horizontalHeader().setStretchLastSection(True)
        self.tableViewF.verticalHeader().setVisible(False)
        self.tableViewF.verticalHeader().setDefaultSectionSize(22)
        self.tableViewF.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableViewF)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.pushButtonEnlever = QtGui.QPushButton(self.centralwidget)
        self.pushButtonEnlever.setObjectName(_fromUtf8("pushButtonEnlever"))
        self.horizontalLayout_5.addWidget(self.pushButtonEnlever)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setMinimumSize(QtCore.QSize(170, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(170, 16777215))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout_10.addWidget(self.comboBox)
        self.pushButtonAjouter_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButtonAjouter_2.setObjectName(_fromUtf8("pushButtonAjouter_2"))
        self.horizontalLayout_10.addWidget(self.pushButtonAjouter_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.comboBoxH = QtGui.QComboBox(self.centralwidget)
        self.comboBoxH.setMinimumSize(QtCore.QSize(170, 0))
        self.comboBoxH.setMaximumSize(QtCore.QSize(170, 16777215))
        self.comboBoxH.setObjectName(_fromUtf8("comboBoxH"))
        self.horizontalLayout_11.addWidget(self.comboBoxH)
        self.pushButtonAjouterH = QtGui.QPushButton(self.centralwidget)
        self.pushButtonAjouterH.setObjectName(_fromUtf8("pushButtonAjouterH"))
        self.horizontalLayout_11.addWidget(self.pushButtonAjouterH)
        self.verticalLayout_3.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.comboBoxM = QtGui.QComboBox(self.centralwidget)
        self.comboBoxM.setMinimumSize(QtCore.QSize(170, 0))
        self.comboBoxM.setMaximumSize(QtCore.QSize(170, 16777215))
        self.comboBoxM.setObjectName(_fromUtf8("comboBoxM"))
        self.horizontalLayout_12.addWidget(self.comboBoxM)
        self.pushButtonAjouterM = QtGui.QPushButton(self.centralwidget)
        self.pushButtonAjouterM.setObjectName(_fromUtf8("pushButtonAjouterM"))
        self.horizontalLayout_12.addWidget(self.pushButtonAjouterM)
        self.verticalLayout_3.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.comboBoxY = QtGui.QComboBox(self.centralwidget)
        self.comboBoxY.setMinimumSize(QtCore.QSize(170, 0))
        self.comboBoxY.setMaximumSize(QtCore.QSize(170, 16777215))
        self.comboBoxY.setObjectName(_fromUtf8("comboBoxY"))
        self.horizontalLayout_13.addWidget(self.comboBoxY)
        self.pushButtonAjouterY = QtGui.QPushButton(self.centralwidget)
        self.pushButtonAjouterY.setObjectName(_fromUtf8("pushButtonAjouterY"))
        self.horizontalLayout_13.addWidget(self.pushButtonAjouterY)
        self.verticalLayout_3.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_7.addLayout(self.verticalLayout_3)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem5)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setContentsMargins(-1, 0, -1, 0)
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelOG = QtGui.QLabel(self.centralwidget)
        self.labelOG.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelOG.setObjectName(_fromUtf8("labelOG"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelOG)
        self.labelOGV = QtGui.QLabel(self.centralwidget)
        self.labelOGV.setText(_fromUtf8(""))
        self.labelOGV.setObjectName(_fromUtf8("labelOGV"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.labelOGV)
        self.labelFG = QtGui.QLabel(self.centralwidget)
        self.labelFG.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelFG.setObjectName(_fromUtf8("labelFG"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelFG)
        self.labelFGV = QtGui.QLabel(self.centralwidget)
        self.labelFGV.setText(_fromUtf8(""))
        self.labelFGV.setObjectName(_fromUtf8("labelFGV"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.labelFGV)
        self.labelEBC = QtGui.QLabel(self.centralwidget)
        self.labelEBC.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelEBC.setObjectName(_fromUtf8("labelEBC"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelEBC)
        self.labelEBCV = QtGui.QLabel(self.centralwidget)
        self.labelEBCV.setText(_fromUtf8(""))
        self.labelEBCV.setObjectName(_fromUtf8("labelEBCV"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.labelEBCV)
        self.labelIBU = QtGui.QLabel(self.centralwidget)
        self.labelIBU.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelIBU.setObjectName(_fromUtf8("labelIBU"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelIBU)
        self.labelIBUV = QtGui.QLabel(self.centralwidget)
        self.labelIBUV.setText(_fromUtf8(""))
        self.labelIBUV.setObjectName(_fromUtf8("labelIBUV"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.labelIBUV)
        self.labelAlc = QtGui.QLabel(self.centralwidget)
        self.labelAlc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelAlc.setObjectName(_fromUtf8("labelAlc"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelAlc)
        self.labelAlcv = QtGui.QLabel(self.centralwidget)
        self.labelAlcv.setText(_fromUtf8(""))
        self.labelAlcv.setObjectName(_fromUtf8("labelAlcv"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.labelAlcv)
        self.horizontalLayout_7.addLayout(self.formLayout)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem6)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonFollowStyle)
        self.toolBar.setFloatable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1169, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFichier = QtGui.QMenu(self.menuBar)
        self.menuFichier.setObjectName(_fromUtf8("menuFichier"))
        self.menuEdition = QtGui.QMenu(self.menuBar)
        self.menuEdition.setObjectName(_fromUtf8("menuEdition"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionOuvrir = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8("Images/document-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOuvrir.setIcon(icon2)
        self.actionOuvrir.setObjectName(_fromUtf8("actionOuvrir"))
        self.actionQuitter = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8("Images/application-exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuitter.setIcon(icon3)
        self.actionQuitter.setObjectName(_fromUtf8("actionQuitter"))
        self.actionAbout = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8("Images/help-about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionEnregistrer = QtGui.QAction(MainWindow)
        self.actionEnregistrer.setObjectName(_fromUtf8("actionEnregistrer"))
        self.actionEnregistrer_Sous = QtGui.QAction(MainWindow)
        self.actionEnregistrer_Sous.setObjectName(_fromUtf8("actionEnregistrer_Sous"))
        self.actionQuitter_2 = QtGui.QAction(MainWindow)
        self.actionQuitter_2.setObjectName(_fromUtf8("actionQuitter_2"))
        self.actionOuvrir_2 = QtGui.QAction(MainWindow)
        self.actionOuvrir_2.setObjectName(_fromUtf8("actionOuvrir_2"))
        self.actionEditGrains = QtGui.QAction(MainWindow)
        self.actionEditGrains.setObjectName(_fromUtf8("actionEditGrains"))
        self.actionEditHoublons = QtGui.QAction(MainWindow)
        self.actionEditHoublons.setObjectName(_fromUtf8("actionEditHoublons"))
        self.actionEditDivers = QtGui.QAction(MainWindow)
        self.actionEditDivers.setObjectName(_fromUtf8("actionEditDivers"))
        self.actionEditLevures = QtGui.QAction(MainWindow)
        self.actionEditLevures.setObjectName(_fromUtf8("actionEditLevures"))
        self.toolBar.addAction(self.actionOuvrir)
        self.toolBar.addAction(self.actionAbout)
        self.menuFichier.addAction(self.actionOuvrir_2)
        self.menuFichier.addAction(self.actionEnregistrer)
        self.menuFichier.addAction(self.actionEnregistrer_Sous)
        self.menuFichier.addAction(self.actionQuitter_2)
        self.menuEdition.addAction(self.actionEditGrains)
        self.menuEdition.addAction(self.actionEditHoublons)
        self.menuEdition.addAction(self.actionEditDivers)
        self.menuEdition.addAction(self.actionEditLevures)
        self.menuBar.addAction(self.menuFichier.menuAction())
        self.menuBar.addAction(self.menuEdition.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "JolieBulle", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRecette.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Nom de la recette :</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelGenre.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Genre :</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonChangerStyle.setToolTip(QtGui.QApplication.translate("MainWindow", "Liste de styles BJCP", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2Volume.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Droid Sans\'; font-weight:600;\">Volume (L)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelBoil.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Droid Sans\'; font-weight:600;\">Ebullition (min)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelRendement.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Droid Sans\'; font-weight:600;\">Rendement (%)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBoxIng.setText(QtGui.QApplication.translate("MainWindow", "Ajuster les ingrédients", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFermentables.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Ingredients : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonEnlever.setText(QtGui.QApplication.translate("MainWindow", "Enlever", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAjouter_2.setText(QtGui.QApplication.translate("MainWindow", "Ajouter Grain", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAjouterH.setText(QtGui.QApplication.translate("MainWindow", "Ajouter Houblon", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAjouterM.setText(QtGui.QApplication.translate("MainWindow", "Ajouter Divers", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButtonAjouterY.setText(QtGui.QApplication.translate("MainWindow", "Ajouter Levure", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOG.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Densité Initiale :</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelFG.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Densité Finale :</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEBC.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">EBC :</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelIBU.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">IBU :</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAlc.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Droid Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Alc :</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFichier.setTitle(QtGui.QApplication.translate("MainWindow", "Fichier", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdition.setTitle(QtGui.QApplication.translate("MainWindow", "Edition", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOuvrir.setText(QtGui.QApplication.translate("MainWindow", "Ouvrir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuitter.setText(QtGui.QApplication.translate("MainWindow", "Quitter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "A propos", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnregistrer.setText(QtGui.QApplication.translate("MainWindow", "&Enregistrer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEnregistrer_Sous.setText(QtGui.QApplication.translate("MainWindow", "Enregistrer &sous", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuitter_2.setText(QtGui.QApplication.translate("MainWindow", "Quitter", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOuvrir_2.setText(QtGui.QApplication.translate("MainWindow", "&Ouvrir", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditGrains.setText(QtGui.QApplication.translate("MainWindow", "Editer la base de Grains", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditHoublons.setText(QtGui.QApplication.translate("MainWindow", "Editer la base de Houblons", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditDivers.setText(QtGui.QApplication.translate("MainWindow", "Editer la base de Divers", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditLevures.setText(QtGui.QApplication.translate("MainWindow", "Editer la base de Levures", None, QtGui.QApplication.UnicodeUTF8))
