#!/usr/bin/python3
#­*­coding: utf­8 -­*­



#JolieBulle 2.7
#Copyright (C) 2010-2012 Pierre Tavares

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


import shutil
import os
import os.path
import glob
import logging
import logging.config
from sys import platform
import PyQt4
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from reader import *
from settings import *
from export import *
from exportHTML import *
from exportBBCode import *
from base import *
from importMashXml import *
from editgrain import *
from edithoublon import *
from editdivers import * 
from editlevures import *
from outilDens import *
from outilAlc import *
from outilDilution import *
from outilEvaporation import *
from outilPaliers import * 
from stepEditWindow import *
from mashEditWindow import *
from mashDetail import * 
from exportMash import *
from preferences import *
from brewCalc import *
from stepAdjustWindow import *
from home import *
from globals import *
#from ui.MainWindow import *
from reader import *

import xml.etree.ElementTree as ET
from model.recipe import *
from model.hop import *
import model.constants
import view.constants
from view.fermentableview import *
from view.recipeview import *
from view.hopview import *
from view.yeastview import *

# class BiblioFileSystem (QtGui.QFileSystemModel) :
#     def __init__(self, parent=None):
#         QtGui.QFileSystemModel.__init__(self, parent)
#     def data(self,index, role=QtCore.Qt.DisplayRole):
#         if role == QtCore.Qt.DisplayRole:
#             name = self.fileName(index)    
#             return name
          


# class RecipesDelegate(QtGui.QStyledItemDelegate) : 
#     def __init__(self, parent):
#         QtGui.QStyledItemDelegate.__init__(self, parent)
#         self.palette = parent.palette()
#     def paint(self, painter, option, index):
#         item_var = index.data(QtCore.Qt.DisplayRole)
#         # item_str = item_var.toPyObject()
#         item_info = QtCore.QFileInfo(item_var)
#         item_name = item_info.baseName()
       
#         painter.save()
#         if option.state & QtGui.QStyle.State_Selected: 
#             #painter.fillRect(option.rect, painter.brush())
#             painter.fillRect(option.rect, self.palette.highlight())
#             painter.setPen(self.palette.highlightedText().color() )
#         painter.drawText(option.rect, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter, item_name)
#         target = QtCore.QRectF(0, 0, 12, 12)
#         source = QtCore.QRectF(0, 0, 24, 24)
#         image = QtGui.QPixmap("folder.png")
#         painter.drawPixmap(option.rect.topLeft(), image)
#         painter.restore()

def initLogging():
    config = {
        'version': 1,              
        'root': {
            'handlers': ['console','file'],
            'level': 'DEBUG'
        },
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s]: %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s %(module)-17s line:%(lineno)-4d %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'stream':'ext://sys.stdout',
                'formatter':'standard'
            },
            'file': {
                'class':'logging.FileHandler',
                'level':'DEBUG',
                'formatter':'detailed',
                'mode':'a',
                'filename':os.path.join(config_dir,'joliebulle.log')
            }  
        }
    }
    logging.config.dictConfig(config)


class IngDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
    def createEditor(self, parent, option, index) :  
        #return editor
        pass
    def setEditorData(self, spinBox, index):
        pass
    def setModelData(self, spinBox, model, index):
        pass
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class AmountDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
            QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index) :
        editor = None
        modele = index.model()
        data = modele.data(index, view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Fermentable) or isinstance(data, Hop) or isinstance(data, Misc):
            editor = QtGui.QLineEdit(parent)
            editor.installEventFilter(self)
        else:
            logger.debug("Selection is not a Fermentable or Hop or Misc:%s", type(data))
        return editor

    def setEditorData(self, lineEdit, index):
        value= index.model().data(index, QtCore.Qt.DisplayRole)
        lineEdit.setText(value)
        #spinBox.setSuffix(" g")

    def setModelData(self, lineEdit, model, index):
        data = index.data(view.constants.MODEL_DATA_ROLE)
        value = lineEdit.text()
        model.setData(index, value)
        self.emit( QtCore.SIGNAL( "pySig"))
        
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
        
class TimeDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index) :
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Hop) or isinstance(data, Misc):        
            editor = QtGui.QSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(20000)
            editor.installEventFilter(self)
        return editor

    def setEditorData(self, spinBox, index):
        data = index.data(view.constants.MODEL_DATA_ROLE)
        value = index.data(QtCore.Qt.DisplayRole)
        if isinstance(data, Hop):
            spinBox.setValue(HopView.display_to_time(value))
        elif isinstance(data, Misc):
            spinBox.setValue(MiscView.display_to_time(value))
        spinBox.setSuffix(" min")

    def setModelData(self, spinBox, model, index):
        data = index.data(view.constants.MODEL_DATA_ROLE)
        spinBox.interpretText()
        value = spinBox.value()
        if isinstance(data, Hop):
            model.setData(index, HopView.time_to_display(value))
        elif isinstance(data, Misc):
            model.setData(index, MiscView.time_to_display(value))
        self.emit( QtCore.SIGNAL( "pySig"))
                            
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
    

class AlphaDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.hopLabels = HopViewLabels()
        self.hopView = HopView(None)

    def createEditor(self, parent, option, index) :
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Hop):
            editor = QtGui.QDoubleSpinBox(parent)
            editor.setMinimum(0)
            editor.setMaximum(20000)
            editor.installEventFilter(self)
        return editor

    def setEditorData(self, spinBox, index):
        value = index.data(QtCore.Qt.DisplayRole)
        spinBox.setValue(HopView.display_to_alpha(value))
        spinBox.setSuffix(" %")

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()
        model.setData(index, HopView.alpha_to_display(value))
        self.emit( QtCore.SIGNAL( "pySig"))
                            
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class HopFormComboBoxDelegate(QtGui.QItemDelegate):
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.hopLabels = HopViewLabels()

    def createEditor(self, parent, option, index):
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Hop):
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.hopLabels.formLabels.items():
                editor.addItem(v, k)
        return editor

    def setEditorData( self, comboBox, index ):
        display = index.data(QtCore.Qt.DisplayRole)
        value = 0
        for (k,v) in self.hopLabels.formLabels.items():
            if display == v:
                break
            value += 1
        comboBox.setCurrentIndex(value)
        
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData( index, value )
        self.emit( QtCore.SIGNAL( "pySig"))    

    def updateEditorGeometry( self, editor, option, index ):

        editor.setGeometry(option.rect)
        
class UseDelegate(QtGui.QItemDelegate):
    def __init__(self, parent = None):
        QtGui.QItemDelegate.__init__(self, parent)
        self.hopLabels = HopViewLabels()
        self.fermentableLabels = FermentableViewLabels()
        self.miscLabels = MiscViewLabels()

    def createEditor(self, parent, option, index):
        editor = None
        data = index.data(view.constants.MODEL_DATA_ROLE)
        if isinstance(data, Fermentable):
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.fermentableLabels.useLabels.items():
                editor.addItem(v, k)
        elif isinstance(data, Hop):
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.hopLabels.useLabels.items():
                editor.addItem(v, k)
        elif isinstance(data, Misc):        
            editor = QtGui.QComboBox( parent )
            for (k,v) in self.miscLabels.useLabels.items():
                editor.addItem(v, k)
        return editor

    def setEditorData( self, comboBoxUse, index ):
        display = index.data(QtCore.Qt.DisplayRole)
        data = index.data(view.constants.MODEL_DATA_ROLE)
        value = 0
        if isinstance(data, Fermentable):
            for (k,v) in self.fermentableLabels.useLabels.items():
                if display == v:
                    break
                value += 1
        elif isinstance(data, Hop):
            for (k,v) in self.hopLabels.useLabels.items():
                if display == v:
                    break
                value += 1
        elif isinstance(data, Misc):
            for (k,v) in self.miscLabels.useLabels.items():
                if display == v:
                    break
                value += 1
        comboBoxUse.setCurrentIndex(value)
        
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData( index, value )
        self.emit( QtCore.SIGNAL( "pySig"))

    def updateEditorGeometry( self, editor, option, index ):
        editor.setGeometry(option.rect)
        


class AppWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

#####################################################################################################
#####################################################################################################

        # self.buttonLibrary=QtGui.QPushButton("Bibliothèque")
        # self.buttonLibrary.setCheckable(True)
        # self.buttonEditor=QtGui.QPushButton("Editeur")
        # self.buttonEditor.setCheckable(True)
        # self.buttonBrewday=QtGui.QPushButton("Brassage")
        # self.buttonBrewday.setCheckable(True)

        self.buttonMenu=QtGui.QPushButton("")
        self.buttonMenu.setIcon(QtGui.QIcon("Images/config.png"))
        self.buttonMenu.setIconSize(QtCore.QSize(24,24))
        self.buttonMenu.setFlat(True)

        self.buttonSave=QtGui.QPushButton("")
        self.buttonSave.setIcon(QtGui.QIcon("Images/save.png"))
        self.buttonSave.setIconSize(QtCore.QSize(24,24))
        self.buttonSave.setFlat(True)
        self.buttonSave.setToolTip(self.trUtf8("Enregistrer"))
        self.buttonSave.setText(self.trUtf8("Enregistrer"))

        self.buttonNewRecipe=QtGui.QPushButton("")
        self.buttonNewRecipe.setIcon(QtGui.QIcon("Images/more.png"))
        self.buttonNewRecipe.setIconSize(QtCore.QSize(24,24))
        self.buttonNewRecipe.setFlat(True)
        self.buttonNewRecipe.setToolTip(self.trUtf8("Nouvelle recette"))
        self.buttonNewRecipe.setText(self.trUtf8("Nouvelle recette"))
        
        

        # left_spacer = QtGui.QWidget()
        # left_spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        right_spacer = QtGui.QWidget()
        right_spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        layoutToolBar=QtGui.QHBoxLayout()
        layoutToolBar.setContentsMargins(9,0,9,0)

        # self.toolBar.addAction(self.actionVueBibliothequeToolBar)
        # self.toolBar.addAction(self.actionVueEditeurToolBar)
        # self.toolBar.addAction(self.actionBrewdayMode)
        # self.toolBar.addWidget(left_spacer)
        
        
        layoutToolBar.addWidget(self.buttonMenu)
        # monLayout.addWidget(self.buttonEditor)
        # monLayout.addWidget(self.buttonBrewday)

        self.widgetToolBar=QtGui.QWidget()

        self.widgetToolBar.setLayout(layoutToolBar)

        # self.toolBar.addWidget(self.widgetToolBar)
        self.toolBar.addWidget(self.buttonNewRecipe)
        self.toolBar.addWidget(right_spacer)
        self.toolBar.addWidget(self.widgetToolBar)

        # self.toolBar.addWidget(self.buttonMenu)

       
        generalMenu = QtGui.QMenu()
        # le menu fichier
        menuFile=generalMenu.addMenu(self.trUtf8('''Fichier'''))
        menuFile.addAction(self.actionImporter)
        menuFile.addAction(self.actionOuvrir_2)
        menuFile.addAction(self.actionNouvelle_recette)
        menuFile.addAction(self.actionRecharger)
        menuFile.addAction(self.actionImprimer)
        menuFile.addAction(self.actionEnregistrer)
        menuFile.addAction(self.actionEnregistrer_Sous)
        menuFile.addAction(self.actionExporterHtml)
        menuFile.addAction(self.actionCopierBbcode)
        menuFile.addAction(self.actionQuitter_2)


        # le menu ingredients
        menuIngredients=generalMenu.addMenu(self.trUtf8('''Ingrédients'''))
        menuIngredients.addAction(self.actionEditGrains)
        menuIngredients.addAction(self.actionEditHoublons)
        menuIngredients.addAction(self.actionEditDivers)
        menuIngredients.addAction(self.actionEditLevures)
        menuIngredients.addAction(self.actionRestaurerIngredients)

        # le menu profils
        menuProfiles = generalMenu.addMenu(self.trUtf8('''Profils de brassage'''))
        menuProfiles.addAction(self.actionManageProfiles)

        # le menu outils
        menuTools=generalMenu.addMenu(self.trUtf8('''Outils'''))
        menuTools.addAction(self.actionCorrectionDens)
        menuTools.addAction(self.actionCalculAlc)
        menuTools.addAction(self.actionDilution)
        menuTools.addAction(self.actionEvaporation)
        menuTools.addAction(self.actionPaliers)


        generalMenu.addAction(self.actionPreferences)
        generalMenu.addAction(self.actionAbout)
        self.buttonMenu.setMenu(generalMenu)

        self.buttonSave.clicked.connect(self.enregistrer)
        self.buttonSave.hide()
        self.buttonNewRecipe.hide()
        self.buttonNewRecipe.clicked.connect(self.newRecipeFromLibrary)


######################################################################################
######################################################################################
        self.settings = Settings()
        self.initRep()
        self.dlgEditG = Dialog(self)
        self.dlgEditH = DialogH(self)
        self.dlgEditD = DialogD(self)
        self.dlgEditY = DialogL(self)
        self.dlgOutilDens = DialogOutilDens(self)
        self.dlgOutilAlc = DialogAlc(self)
        self.dlgOutilDilution = DialogDilution(self)
        self.dlgOutilEvaporation = DialogEvaporation(self)
        self.dlgOutilPaliers = DialogPaliers(self)
        self.dlgPref = DialogPref(self)
        self.dlgStep = DialogStep(self)
        self.dlgMash = DialogMash(self)
        self.dlgStepBrewday = DialogStepAdjust(self)

        self.base = ImportBase()
        self.mashProfilesBase = ImportMash()
        self.mashProfileExport = ExportMash()
        self.brewCalc = CalcBrewday()
        
#        self.base.importBeerXML()
        self.s=0
        self.nbreLevures = 0
        
        self.baseStyleListe = [self.trUtf8('Générique'), '1A. Lite American Lager', '1B. Standard American Lager', '1C. Premium American Lager', '1D. Munich Helles', '1E. Dortmunder Export', '2A. German Pilsner (Pils)', '2B. Bohemian Pilsener', '2C. Classic American Pilsner', '3A. Vienna Lager', '3B. Oktoberfest/Märzen', '4A. Dark American Lager', '4B. Munich Dunkel', '4C. Schwarzbier (Black Beer)', '5A. Maibock/Helles Bock', '5B. Traditional Bock', '5C. Doppelbock', '5D. Eisbock', '6A. Cream Ale', '6B. Blonde Ale', '6C. Kölsch', '6D. American Wheat or Rye Beer', '7A. Northern German Altbier', '7B. California Common Beer', '7C. Düsseldorf Altbier', '8A. Standard/Ordinary Bitter', '8B. Special/Best/Premium Bitter', '8C. Extra Special/Strong Bitter (English Pale Ale)', '9A. Scottish Light 60/-', '9B. Scottish Heavy 70/-', '9C. Scottish Export 80/- ', '9D. Irish Red Ale', '9E. Strong Scotch Ale', '10A. American Pale Ale', '10B. American Amber Ale', '10C. American Brown Ale', '11A. Mild','11B. Southern English Brown', '11C. Northern English Brown Ale', '12A. Brown Porter', '12B. Robust Porter', '12C. Baltic Porter', '13A. Dry Stout', '13B. Sweet Stout', '13C. Oatmeal Stout', '13D. Foreign Extra Stout', '13E. American Stout', '13F. Russian Imperial Stout', '14A. English IPA', '14B. American IPA', '14C. Imperial IPA','15A. Weizen/Weissbier', '15B. Dunkelweizen', '15C. Weizenbock', '15D. Roggenbier (German Rye Beer)','16A. Witbier', '16B. Belgian Pale Ale', '16C. Saison', '16D. Bière de Garde', '16E. Belgian Specialty Ale', '17A. Berliner Weisse', '17B. Flanders Red Ale', '17C. Flanders Brown Ale/Oud Bruin', '17D. Straight (Unblended) Lambic', '17E. Gueuze', '17F. Fruit Lambic', '18A. Belgian Blond Ale', '18B. Belgian Dubbel', '18C. Belgian Tripel', '18D. Belgian Golden Strong Ale', '18E. Belgian Dark Strong Ale', '19A. Old Ale', '19B. English Barleywine', '19C. American Barleywine', '20. Fruit Beer', '21A. Spice, Herb, or Vegetable Beer', '21B. Christmas/Winter Specialty Spiced Beer', '22A. Classic Rauchbier', '22B. Other Smoked Beer', '22C. Wood-Aged Beer', '23. Specialty Beer', '24A. Dry Mead', '24B. Semi-sweet Mead', '24C. Sweet Mead', '25A. Cyser', '25B. Pyment', '25C. Other Fruit Melomel', '26A. Metheglin', '26B. Braggot', '26C. Open Category Mead', '27A. Common Cider', '27B. English Cider', '27C. French Cider', '27D. Common Perry', '27E. Traditional Perry', '28A. New England Cider', '28B. Fruit Cider', '28C. Applewine', '28D. Other Specialty Cider/Perry']
       
        self.typesList = [self.trUtf8("Tout grain"), self.trUtf8("Extrait"), self.trUtf8("Partial mash")]


        #Les connexions
        self.connect(self.actionOuvrir, QtCore.SIGNAL("triggered()"), self.ouvrir_clicked)
        self.connect(self.actionOuvrir_2, QtCore.SIGNAL("triggered()"), self.ouvrir_clicked)
        self.connect(self.actionNouvelle_recette, QtCore.SIGNAL("triggered()"), self.purge)
        self.connect(self.actionEnregistrer, QtCore.SIGNAL("triggered()"), self.enregistrer)
        self.connect(self.actionEnregistrerToolBar, QtCore.SIGNAL("triggered()"), self.enregistrer)
        self.connect(self.actionEnregistrer_Sous, QtCore.SIGNAL("triggered()"), self.enregistrerSous)
        self.connect(self.actionExporterHtml, QtCore.SIGNAL("triggered()"), self.exporterHtml)
        self.connect(self.actionCopierBbcode, QtCore.SIGNAL("triggered()"), self.copierBbcode)
        self.connect(self.actionRecharger, QtCore.SIGNAL("triggered()"), self.recharger)
        #self.connect(self.actionSwitch, QtCore.SIGNAL("triggered()"), self.switch)
        self.actionImporter.triggered.connect(self.importInLib)
        self.connect(self.actionQuitter, QtCore.SIGNAL("triggered()"), app, QtCore.SLOT("quit()"))
        
        self.connect(self.actionEditGrains, QtCore.SIGNAL("triggered()"), self.editGrains)
        self.connect(self.actionEditHoublons, QtCore.SIGNAL("triggered()"), self.editHoublons)
        self.connect(self.actionEditDivers, QtCore.SIGNAL("triggered()"), self.editDivers)
        self.connect(self.actionEditLevures, QtCore.SIGNAL("triggered()"), self.editLevures)
        self.connect(self.actionRestaurerIngredients, QtCore.SIGNAL("triggered()"), self.restoreDataBase)
        self.actionManageProfiles.triggered.connect(self.seeMash)
        
        self.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.about)
        self.connect(self.actionCorrectionDens, QtCore.SIGNAL("triggered()"), self.outilDens)
        self.connect(self.actionCalculAlc, QtCore.SIGNAL("triggered()"), self.outilAlc)
        self.connect(self.actionDilution, QtCore.SIGNAL("triggered()"), self.outilDilution)
        self.connect(self.actionEvaporation, QtCore.SIGNAL("triggered()"), self.outilEvaporation)
        self.connect(self.actionPaliers, QtCore.SIGNAL("triggered()"), self.outilPaliers)
        self.connect(self.actionPreferences, QtCore.SIGNAL("triggered()"), self.dialogPreferences)
        
        self.spinBoxBoil.valueChanged.connect(self.unlockBrewdayMode)

        self.pushButtonSave.clicked.connect(self.enregistrer)
        self.pushButtonCancel.clicked.connect(self.cancelRecipe)
        self.pushButtonOk.clicked.connect(self.okRecipe)
        self.pushButtonBrewdayModeClose.clicked.connect(self.closeBrewday)
        



        
        #Les vues
        #####################################################################################
        #####################################################################################
        self.connect(self.actionVueEditeur, QtCore.SIGNAL("triggered()"), self.switchToEditor)
        self.connect(self.actionVueBibliotheque, QtCore.SIGNAL("triggered()"), self.switchToLibrary)
        
        self.connect(self.actionVueEditeurToolBar, QtCore.SIGNAL("triggered()"), self.switchToEditor)
        self.connect(self.actionVueBibliothequeToolBar, QtCore.SIGNAL("triggered()"), self.switchToLibrary)

        self.connect(self.actionBrewdayMode,QtCore.SIGNAL("triggered()"),self.switchToBrewday)

        # self.connect(self.buttonEditor, QtCore.SIGNAL("clicked()"),self.switchToEditor)
        # self.connect(self.buttonLibrary, QtCore.SIGNAL("clicked()"), self.switchToLibrary)
        # self.connect(self.buttonBrewday, QtCore.SIGNAL("clicked()"), self.switchToBrewday)

        
        #############################################################################################
        #############################################################################################
        
        
        ##########################
        #Boutons notes
        ##########################
        self.pushButtonRecipeNotes.clicked.connect(self.recipeNotesClicked)
        self.buttonBoxRecipeNotes.accepted.connect(self.recipeNotesAccepted)
        self.buttonBoxRecipeNotes.rejected.connect(self.recipeNotesRejected)
        
        
        #############################################################################################
        self.connect(self.actionImprimer, QtCore.SIGNAL("triggered()"), self.printRecipe)
        
        self.connect(self.doubleSpinBoxRendemt, QtCore.SIGNAL("valueChanged(QString)"), self.rendemt_changed)
        self.connect(self.doubleSpinBox_2Volume, QtCore.SIGNAL("valueChanged(QString)"), self.volume_changed)
        self.connect(self.pushButtonAjouter_2, QtCore.SIGNAL("clicked()"), self.ajouterF)
        self.connect(self.pushButtonAjouterH, QtCore.SIGNAL("clicked()"), self.ajouterH)
        self.connect(self.pushButtonAjouterY, QtCore.SIGNAL("clicked()"), self.ajouterY)
        self.connect(self.pushButtonAjouterM, QtCore.SIGNAL("clicked()"), self.ajouterM)
        self.connect(self.pushButtonEnlever, QtCore.SIGNAL("clicked()"), self.enlever)
        self.connect(self.pushButtonChangerStyle, QtCore.SIGNAL("clicked()"), self.modifierStyle)
        self.connect(self.pushButtonVolMore, QtCore.SIGNAL("clicked()"), self.volMore)
        self.connect(self.doubleSpinBoxVolPre, QtCore.SIGNAL("valueChanged(QString)"), self.volPreCalc)
        
        
        self.connect(self.comboBoxStyle, QtCore.SIGNAL("currentIndexChanged(QString)"), self.addStyle)
        #self.connect(self.pushButtonEssai, QtCore.SIGNAL("clicked()"), self.essai)
        self.connect(self.comboBoxType, QtCore.SIGNAL("currentIndexChanged(QString)"), self.typeChanged)
        
        #######################################################################################################
        # Profil de brassage       #########################################################################################################
        self.pushButtonMashDetails.clicked.connect(self.mashDetails)
        self.listWidgetSteps.itemSelectionChanged.connect (self.stepDetails)
        self.listWidgetMashProfiles.itemSelectionChanged.connect (self.mashClicked)
        self.buttonBoxMashDetails.rejected.connect(self.mashRejected)
        self.buttonBoxMashDetails.accepted.connect(self.mashAccepted)
#        self.comboBoxStepType.addItems(["Infusion", "Température", "Décoction"])
        self.pushButtonStepEdit.clicked.connect(self.stepEdit)
        self.dlgStep.stepChanged.connect(self.stepReload)
        self.pushButtonStepRemove.clicked.connect(self.removeStep)
        self.pushButtonNewStep.clicked.connect(self.addStep)
        self.pushButtonMashEdit.clicked.connect(self.mashEdit)
        self.dlgMash.mashChanged.connect(self.mashReload)
        self.pushButtonNewProfile.clicked.connect(self.addMash)
        self.pushButtonRemoveProfile.clicked.connect(self.removeMash)
        
        
        self.popMashCombo()
        self.comboBoxMashProfiles.setCurrentIndex(-1)
        self.comboBoxMashProfiles.currentIndexChanged.connect(self.mashComboChanged)

        
        self.pushButtonSaveProfile.clicked.connect(self.saveProfile)


        
        #On connecte ici les signaux émits à la fermeture des fenêtres d'édition de la base
        #########################################################################################
        ##########################################################################################
        #self.connect(self.dlgEditG, QtCore.SIGNAL( "baseChanged"), self.baseReload)
        self.dlgEditG.baseChanged.connect(self.baseReload)
        self.dlgEditH.baseChanged.connect(self.baseReload)
        self.dlgEditD.baseChanged.connect(self.baseReload)
        self.dlgEditY.baseChanged.connect(self.baseReload)
        
        #Signal pour l'affichage du widget de modif des ingrédients
        self.pushButtonChangeIngredients.clicked.connect(self.displayIngredients) 
        
        
        #Les modeles et vues du widget central
        self.modele = QtGui.QStandardItemModel(0, 7)
        self.connect(self.modele, QtCore.SIGNAL("itemChanged(QStandardItem *)"), self.reverseMVC)
        
        liste_headers = [self.trUtf8("Ingrédients"),self.trUtf8("Quantité (g)"),self.trUtf8("Temps (min)"),self.trUtf8("Acide Alpha (%)"),self.trUtf8("Type"),self.trUtf8("Proportion"), self.trUtf8("Étape")]
        self.modele.setHorizontalHeaderLabels(liste_headers)
        
        
        
        self.deleg = AmountDelegate(self)
        self.tableViewF.setItemDelegateForColumn(1,self.deleg)
        self.connect(self.deleg, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        
        
        
        self.delegT = TimeDelegate(self)
        self.tableViewF.setItemDelegateForColumn(2,self.delegT)
        self.connect(self.delegT, QtCore.SIGNAL( "pySig"), self.modeleProportion)

        self.delegA = AlphaDelegate(self)
        self.tableViewF.setItemDelegateForColumn(3,self.delegA)
        self.connect(self.delegA, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        
        self.delegC = HopFormComboBoxDelegate(self)
        self.tableViewF.setItemDelegateForColumn(4,self.delegC)  
        self.connect(self.delegC, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        
        self.delegI = IngDelegate(self)
        self.tableViewF.setItemDelegateForColumn(0,self.delegI)
        self.tableViewF.setItemDelegateForColumn(5,self.delegI)
        
        self.delegUse = UseDelegate(self)
        self.tableViewF.setItemDelegateForColumn(6,self.delegUse)
        self.connect(self.delegUse, QtCore.SIGNAL( "pySig"), self.modeleProportion)
        

        self.tableViewF.setModel(self.modele)
        
        self.tableViewF.resizeColumnsToContents()
        self.tableViewF.setColumnWidth(0,250)
        self.tableViewF.setColumnWidth(1,125)
        self.tableViewF.setColumnWidth(3,125)
        self.tableViewF.setColumnWidth(4,150)
        self.tableViewF.setColumnWidth(6,150)
        
        #La bibliotheque
        ###################################################################################################################
        ###################################################################################################################
        self.modeleBiblio = QtGui.QFileSystemModel()
        self.modeleBiblio.setReadOnly(False)
        self.modeleBiblio.setRootPath(recettes_dir)
        self.setHomePage()
        
        # self.listViewBiblio.setModel(self.modeleBiblio)
        # self.listViewBiblio.setRootIndex(self.modeleBiblio.index(recettes_dir))
        # self.connect(self.listViewBiblio, QtCore.SIGNAL("doubleClicked(const QModelIndex &)"), self.selectionRecette)
        
        self.treeViewBiblio.setContextMenuPolicy(QtCore.Qt.CustomContextMenu) 
        self.connect(self.treeViewBiblio, QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"), self.menuBiblio)
        #self.listViewBiblio.setEditTriggers(QtGui.QAbstractItemView.SelectedClicked | QtGui.QAbstractItemView.AnyKeyPressed) 


        self.treeViewBiblio.setModel(self.modeleBiblio)
        self.treeViewBiblio.setRootIndex(self.modeleBiblio.index(recettes_dir))
        self.treeViewBiblio.setColumnHidden(1,True)
        self.treeViewBiblio.setColumnHidden(2,True)
        self.treeViewBiblio.setColumnHidden(3,True)

        # self.webViewBiblio.setHtml('''<html><p>hello world</p></html>''')
        self.connect(self.treeViewBiblio, QtCore.SIGNAL("doubleClicked(const QModelIndex &)"), self.selectionRecette2)
        self.connect(self.treeViewBiblio, QtCore.SIGNAL("clicked(const QModelIndex &)"), self.viewRecipeBiblio)

        self.pushButtonEditCurrentRecipe.clicked.connect(self.editCurrentRecipe)

        # self.pushButtonRemoveRecipeBiblio.clicked.connect(self.supprimerBiblio)
        # self.pushButtonNewFolderBiblio.clicked.connect(self.createFolder)
        # self.pushButtonEditRecipeBiblio.clicked.connect(self.renommerBiblio)
        self.pushButtonBrewRecipeBiblio.clicked.connect(self.switchToBrewday)

        self.listdir(recettes_dir)
        # self.delegRecipes=RecipesDelegate(self)
        # self.treeViewBiblio.setItemDelegate(self.delegRecipes)    


        # le menu "nouveau"
        newLibMenu = QtGui.QMenu()
        newLibMenu.addAction(self.actionNouveau_Dossier)
        newLibMenu.addAction(self.actionNouvelle_recette_2)
        # self.pushButtonNewFolderBiblio.setMenu(newLibMenu)

        self.actionNouveau_Dossier.triggered.connect(self.createFolder)
        self.actionNouvelle_recette_2.triggered.connect(self.newRecipeFromLibrary)



        ############################################################################################################################
        ############################################################################################################################
        
        #Brewday Mode
        ###############################
        ###############################
              
        self.pushButtonAdjustStep.clicked.connect(self.stepAdjustBrewday)
        self.tableWidgetStepsBrewday.itemSelectionChanged.connect(self.tableWidgetStepsBrewday_currentRowChanged)
        self.dlgStepBrewday.stepAdjustBrewdayClosed.connect(self.stepAdjustBrewday_closed)
        self.radioButtonClassicBrew.toggled.connect(self.brewdayModeCalc)



        
        ##on cree un modele pour les ingredients dispo dans la base
        #self.modeleIngBase = QtGui.QStandardItemModel()
        ##la vue correspondante
        #self.treeViewIng.setModel(self.modeleIngBase)
        ##on va remplir tout ça... avec une autre fonction
        #self.listeIng()
        self.comboBox.setModel(view.base.getFermentablesQtModel() )
        
        self.comboBoxH.setModel(view.base.getHopsQtModel() )
        
        self.comboBoxY.setModel(view.base.getYeastsQtModel() )
        
        self.comboBoxM.setModel(view.base.getMiscsQtModel() )
       
        self.comboBoxStyle.hide()
        self.comboBoxStyle.addItems(self.baseStyleListe)
        
        self.comboBoxType.addItems(self.typesList)
        self.comboBoxType.setCurrentIndex(0)

        self.widgetVol.hide()
        
        self.nouvelle()
 
        self.widgetIngredients.hide()

        self.actionVueEditeurToolBar.setChecked(False)


        # print("argv:",sys.argv)

###################################################################################################
######## gestion des arguments au lancement du programme  #########################################


        argumentsList=QtGui.QApplication.arguments()
        if len(argumentsList) > 1 :
            logger.debug("la liste d'arguments: %s",argumentsList)
            logger.debug("le chemin: %s",argumentsList[1])
            # for part in argumentsList :
            #     recipePath=recipePath + " " + part
            try:
                recipePath= argumentsList[1]
                for part in argumentsList[2:] :
                    recipePath= recipePath +" " + part
                
                self.openRecipeFile(recipePath)
            except :
                pass
        else:
            pass
            
########################################################################################################################
####################################################################################################################
# le signal émit à la fermeture de la fenêtre de préférences
        self.dlgPref.prefAccepted.connect(self.prefReload)

#####################################################################
        ###on configure la vue par défaut à l'ouverture
#####################################################################
        self.stackedWidget.setCurrentIndex(1)
        self.actionVueEditeurToolBar.setChecked(False)
        self.actionVueBibliothequeToolBar.setChecked(True)
        self.actionBrewdayMode.setChecked(False)
        self.buttonSave.hide()
        self.buttonNewRecipe.show()

        


        
    #Une fonction qui gère l'aperçu des couleurs. 
    #Contient un tupple avec plusieurs références de couleurs, classées par rang selon la valeur SRM.
    #################################################################################################
    def colorPreview (self) :
        self.colorTuppleSrm = ('FFE699', 'FFD878', 'FFCA5A', 'FFBF42', 'FBB123', 'F8A600', 'F39C00', 'EA8F00', 'E58500', 'DE7C00', 'D77200', 'CF6900', 'CB6200', 'C35900','BB5100', 'B54C00', 'B04500', 'A63E00', 'A13700', '9B3200', '952D00', '8E2900', '882300', '821E00', '7B1A00', '771900', '701400', '6A0E00', '660D00','5E0B00','5A0A02','600903', '520907', '4C0505', '470606', '440607', '3F0708', '3B0607', '3A070B', '36080A')
        
        colorRef= round(self.recipe.compute_EBC()/1.97)
        
        if colorRef >= 30 :
            color = "#" + self.colorTuppleSrm[30]
        elif colorRef <= 1 :
            color = "#" + self.colorTuppleSrm[0]
        else :
            color = "#" + self.colorTuppleSrm[colorRef-1]
        self.widgetColor.setStyleSheet("background-color :" + color)
        
        
    def displayIngredients(self) :
        if self.pushButtonChangeIngredients.isChecked() :
            self.widgetIngredients.show()
        else :
            self.widgetIngredients.hide()
        
        
    #Une fonction qui recharge les combobox qd la base d'ingrédients a été modifiée. Pratique.
    #############################################################################################   
    def baseReload (self): 
        self.base.importBeerXML()
        
        self.comboBox.clear()
        self.comboBox.setModel(self.base.getFermentablesQtModel() )
        
        self.comboBoxH.clear()
        self.comboBoxH.setModel(self.base.getHopsQtModel() )
        
        self.comboBoxY.clear()
        self.comboBoxY.setModel(self.base.getYeastsQtModel() )
        
        self.comboBoxM.clear()
        self.comboBoxM.setModel(self.base.getMiscsQtModel() )
        
    def selectionRecette2(self):
        selection = self.treeViewBiblio.selectionModel()
        self.indexRecette = selection.currentIndex()

        self.chemin =self.modeleBiblio.filePath (self.indexRecette)
        if os.path.isdir(self.chemin) == False :
            self.purge()
            self.s = self.chemin
        
            self.importBeerXML()
            logger.debug("selectionRecette2 -> initModele")
            self.initModele()
            self.stackedWidget.setCurrentIndex(0)
            self.actionVueEditeurToolBar.setChecked(True)
            self.actionVueBibliothequeToolBar.setChecked(False)
        else :
            logger.debug("Répertoire sélectionné")


    def viewRecipeBiblio(self) :
        selection = self.treeViewBiblio.selectionModel()
        self.indexRecette = selection.currentIndex()

        self.chemin =self.modeleBiblio.filePath(self.indexRecette)
        if os.path.isdir(self.chemin) == False :
            
            self.purge()
            
            self.s = self.chemin
            
            self.importBeerXML()
            exp = ExportHTML()
            exp.exportRecipeHtml(self.recipe)
            exp.generateHtml()
            self.webViewBiblio.setHtml(exp.generatedHtml, )
            # self.modele.blockSignals(True)
            #logger.debug("viewRecipeBiblio -> MVC")
            #self.MVC()
            # self.modele.blockSignals(False)
            self.HtmlRecipe = exp.generatedHtml
        else :
            logger.debug("Répertoire sélectionné")

    def setHomePage(self) :
        home = HomePage()
        home.generateHomePage()
        self.webViewBiblio.setHtml(home.homePage, )


    def listdir(self, rootdir) :
        fileList=[]
        rootList=[]
        filenameList=[]
        for root, subFolders, files in os.walk(rootdir):
            for file2 in files:
                fileList.append(os.path.join(root,file2))
                rootList.append(root)
                filenameList.append(file2)
        # print ('liste',fileList)
        # print('liste dossiers',rootList)
        # print('liste nom',filenameList)

        #on parse
        newFileNameList = []
        j=0
        while j < len(filenameList) :
            j=j+1
            recipe = fileList[j-1]
            arbre = ET.parse(recipe)
            presentation=arbre.find('.//RECIPE')
            for nom in presentation :
                try :
                    if nom.tag == "NAME" : 
                       nomRecette = nom.text
                       newFileNameList.append(nomRecette)
                except :
                    pass
        # print('newFileNameList', newFileNameList)

        #on reconstitue
        newFileList=[]
        i=0
        while i < len(filenameList) :
            i=i+1
            folder = rootList[i-1]
            recipe = newFileNameList[i-1]
            newName = os.path.join(folder,recipe)
            
         
            if newName in newFileList :
                logger.debug('doublon !')
                sameCount= 0 
                while sameCount < len(newFileNameList) :
                    sameCount = sameCount+1
                    newNameModif = newName + '(' + str(sameCount) + ')'
                    if newNameModif in newFileList :
                        continue
                    else :
                        newFileList.append(newNameModif)
                        break
            else :
                newFileList.append(newName) 
        logger.debug(newFileList)

        #on renomme
        # k=0
        # while k < len(newFileNameList) :
        #     k=k+1
        #     old=fileList[k-1]
        #     new=newFileList[k-1] 
        #     if old == new :
        #         pass
        #     else: 
        #         try :
        #             os.rename(old,new)
        #         except :
        #             print("raté")

        #on renomme
        dir = QtCore.QDir(recettes_dir)
        k=0
        while k < len(newFileNameList) :
            k=k+1
            old=fileList[k-1]
            new=newFileList[k-1]  + '.xml'
            if old == new :
                pass
            else :
                try :
                    dir.rename(old,new)
                except:
                    pass
      

    def editCurrentRecipe(self):
        self.switchToEditor()
        self.s = self.chemin
        
        self.importBeerXML()
        # self.modele.blockSignals(True)
        logger.debug("editCurrentRecipe -> initModele")
        self.initModele()
        # self.modele.blockSignals(False)
        self.stackedWidget.setCurrentIndex(0)
        self.actionVueEditeurToolBar.setChecked(True)
        self.actionVueBibliothequeToolBar.setChecked(False) 

        
    def menuBiblio(self,position) :
        selection = self.treeViewBiblio.selectionModel()
        self.indexRecette = selection.currentIndex()
        menu = QtGui.QMenu()
        #EditeurAction = menu.addAction("Editeur de recette")
        RenommerAction  = menu.addAction(self.trUtf8("Renommer"))
        SupprimerAction = menu.addAction(self.trUtf8("Supprimer"))        
        # CopyAction = menu.addAction(self.trUtf8("Copier"))
        # PasteAction = menu.addAction(self.trUtf8("Coller"))
        FolderAction = menu.addAction(self.trUtf8("Nouveau dossier"))
        # UpAction = menu.addAction(self.trUtf8("Remonter"))
        menu.addAction(self.actionNouvelle_recette_2)
        
        # PasteAction.setEnabled(False)
        # clipboard = app.clipboard()
        # data = clipboard.mimeData
        # if clipboard.mimeData().hasUrls() :
        #     PasteAction.setEnabled(True)

        RenommerAction.setEnabled(False)
        if self.modeleBiblio.isDir(self.indexRecette) :
            RenommerAction.setEnabled(True)
               
        action = menu.exec_(self.listViewBiblio.mapToGlobal(position))
        #if action == EditeurAction:
          #  self.switchToEditor()
        if action == SupprimerAction:
            self.supprimerBiblio()  
        if action == RenommerAction:
            self.renommerBiblio() 
        if action == FolderAction:
            self.createFolder()   
        # if action == UpAction :
        #     self.upFolder()
        # if action == CopyAction :
        #     self.copy()
        # if action == PasteAction :
        #     self.paste()

        
        
                    
    def supprimerBiblio (self) :
        selection = self.treeViewBiblio.selectionModel()
        self.indexRecette = selection.currentIndex()
        confirmation = QtGui.QMessageBox.question(self,
                            self.trUtf8("Supprimer"),
                            self.trUtf8("La recette sera définitivement supprimée <br/> Continuer ?"),
                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if (confirmation == QtGui.QMessageBox.Yes):
            self.modeleBiblio.remove(self.indexRecette)
        else :      
            pass
    
    def renommerBiblio (self) :
        selection = self.treeViewBiblio.selectionModel()
        self.indexRecette = selection.currentIndex()
        if self.modeleBiblio.isDir(self.indexRecette) :
            self.treeViewBiblio.edit(self.indexRecette)
        else :
            pass

    def importInLib (self) :
        self.s = QtGui.QFileDialog.getOpenFileName(self,
            self.trUtf8("Ouvrir un fichier"),
            home_dir,
            )

        shutil.copy(self.s, recettes_dir)

        
    def createFolder(self) :
        selection = self.treeViewBiblio.selectionModel()
        self.indexRecette = selection.currentIndex()
        text = self.trUtf8("nouveau dossier")
       # recettes = QtCore.QFile(recettes_dir)
        path = self.modeleBiblio.filePath(self.treeViewBiblio.rootIndex()) + "/" + text
        os.mkdir(path)
        
        
    # def navFolder(self) :
    #     selection = self.treeViewBiblio.selectionModel()
    #     self.indexRecette = selection.currentIndex()        
    #     self.listViewBiblio.setRootIndex(self.indexRecette)
        #self.modeleBiblio.setRootPath("/home/pierre/.config/joliebulle/recettes/nouveau dossier")
        
    # def upFolder(self) :
    #     self.listViewBiblio.setRootIndex(self.treeViewBiblio.rootIndex().parent())
        
    # def copy (self) :
    #     data = QtCore.QMimeData()
    #     selection = self.treeViewBiblio.selectionModel()
    #     self.indexRecette = selection.currentIndex()  
    #     path = self.modeleBiblio.filePath(self.indexRecette)
    #     url = QtCore.QUrl.fromLocalFile(path)
    #     self.lurl = [url]
    #     data.setUrls(self.lurl)
    #     clipboard = app.clipboard()
    #     clipboard.setMimeData(data)
              
    # def paste (self) :
    #     clipboard = app.clipboard()
    #     data = clipboard.mimeData()
    #     file = QtCore.QFile()
    #     file.setFileName(self.lurl[0].toLocalFile())
    #     info = QtCore.QFileInfo(file.fileName())
    #     name= info.fileName()
    #     path = self.modeleBiblio.filePath(self.treeViewBiblio.rootIndex()) + "/" + name
    #     file.copy(path)
    #     clipboard.clear()
       
    def cancelRecipe(self):
        self.switchToLibrary() 

    def okRecipe(self):
        self.enregistrer()
        self.switchToLibrary()

    def closeBrewday(self) :
        self.stackedWidget.setCurrentIndex(1)        
        self.actionVueEditeurToolBar.setChecked(False)
        self.actionVueBibliothequeToolBar.setChecked(True)
        self.actionBrewdayMode.setChecked(False)
        self.buttonSave.hide()
        self.buttonNewRecipe.show()
              
    def initRep(self) :   
        home = QtCore.QDir(home_dir)
        config = QtCore.QDir(config_dir)
        logger.debug (config)
        if not config.exists() :
            home.mkpath (config_dir)
        else :
            pass
        database = QtCore.QFile(database_file)
        if not database.exists() :
            database.copy(database_root, database_file)
        else :
            pass
        recettes = QtCore.QFile(recettes_dir)
        if not recettes.exists() :
            try :
                shutil.copytree(samples_dir, samples_target)
            except :
                home.mkpath(recettes_dir)
        mash  = QtCore.QFile(mash_file)
        if not mash.exists() :
            mash.copy(mash_root, mash_file)
        else :
            pass
        
        # on configure des valeurs par défaut
        if not settings.conf.contains("BoilOffRate") :
            settings.conf.setValue("BoilOffRate", 10)
        if not settings.conf.contains("CoolingLoss") :
            settings.conf.setValue("CoolingLoss", 5)
        if not settings.conf.contains("GrainTemp") :
            settings.conf.setValue("GrainTemp", 20)
        if not settings.conf.contains("FudgeFactor") :
            settings.conf.setValue("FudgeFactor", 1.7)
        if not settings.conf.contains("GrainRetention") :
            settings.conf.setValue("GrainRetention", 1)
        if not settings.conf.contains("Menus") :
            settings.conf.setValue("Menus", "button")

        # on configure la barre de Menus
        if settings.conf.value("Menus") == "button":
            self.menuBar.hide()
            self.buttonMenu.show()
        if settings.conf.value("Menus") == "menubar":
            self.menuBar.show()
            self.buttonMenu.hide()

    def prefReload(self) :
        self.initRep()
  
        
    def switchToEditor(self) :
        self.stackedWidget.setCurrentIndex(0)
        self.buttonNewRecipe.show()

        
    def switchToLibrary(self) :
        self.stackedWidget.setCurrentIndex(1)        
        self.viewRecipeBiblio()

        
    def switchToNotes(self) :
        self.stackedWidget.setCurrentIndex(2)        

        
    def switchToMash(self) :
        self.stackedWidget.setCurrentIndex(3)        

        
    def switchToBrewday(self) :
        logger.debug ("lock %s",self.brewdayLock)
        self.stackedWidget.setCurrentIndex(4)        

        if self.brewdayLock == 1 :
            pass
        else :
            self.brewdayModeCalc()
        self.tableWidgetStepsBrewday.setCurrentCell(0,0) 
        
    def restoreDataBase(self) :
        home = QtCore.QDir(home_dir)
        config = QtCore.QDir(config_dir)
        database = QtCore.QFile(database_file)
        confirmation = QtGui.QMessageBox.question(self,
                                    self.trUtf8("Remplacer la base ?"),
                                    self.trUtf8("La base des ingrédients actuelle va être effacée et remplacée par la base originale. Toutes vos modifications vont être effacées. Un redémarrage de l'application sera nécessaire.<br> Continuer ?"),
                                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if (confirmation == QtGui.QMessageBox.Yes):
            database.remove(database_file)
            database.copy(database_root, database_file)
        else :
            
            pass

    def modeleProportion (self) :
        #Cette fonction est appelée chaque fois que la quantité, les AA ou les temps sont modifiés, via un signal émit par les classes Delegate.
        #Cette fonction met à jour les données du modèle Qt
        recipeView = RecipeView(self.recipe)
        for i in range(self.modele.rowCount()):
            data = self.modele.item(i, 5).data(view.constants.MODEL_DATA_ROLE)
            if isinstance(data, Fermentable):
                self.modele.setItem(i, 5, recipeView.QStandardItem_for_fermentable_proportion(data))
            elif isinstance(data, Hop):
                self.modele.setItem(i, 5, recipeView.QStandardItem_for_hop_ibu(data))
        self.displayProfile()

    # cette fonction est appelee chaque fois que les donnees du modele changent
    def reverseMVC(self, item) :
        #logger.debug("item:%s %s %s", item, item.data(view.constants.MODEL_DATA_ROLE), item.data(QtCore.Qt.EditRole))
        row = item.row()
        column = item.column()
        modelInstance = item.data(view.constants.MODEL_DATA_ROLE)
        newValue = item.text()

        #Update Hop item
        if isinstance(modelInstance, Hop):
            #logger.debug("Model update at [row=%d,column=%d] for Hop:%s; newValue=%s", row, column, modelInstance, newValue)
            hopLabels = HopViewLabels()
            if column == 1:
                #Update Hop amount value
                try:
                    modelInstance.amount = HopView.display_to_amount(newValue)
                except ValueError as e:
                    logger.warn("Can't set Hop amount value to:'%s' %s", newValue, e)
                    item.setData(HopView.amount_to_display(modelInstance.amount), QtCore.Qt.DisplayRole)
            if column == 2:
                #Update Hop time value
                try:
                    modelInstance.time = HopView.display_to_time(newValue)
                except ValueError:
                    logger.warn("Can't set Hop time value to:'%s'", newValue)
                    item.setData(HopView.time_to_display(modelInstance.time), QtCore.Qt.DisplayRole)
            if column == 3:
                #Update Hop alpha value
                try:
                    modelInstance.alpha = HopView.display_to_alpha(newValue)
                except ValueError:
                    logger.warn("Can't set Hop alpha value to:'%s'", newValue)
                    item.setData(HopView.alpha_to_display(modelInstance.alpha), QtCore.Qt.DisplayRole)
            elif column == 4:
                #Update Hop form
                for (k,v) in hopLabels.formLabels.items():
                    if newValue == v:
                        modelInstance.form = k
                        break
            elif column == 6:
                #Update form use
                for (k,v) in hopLabels.useLabels.items():
                    if newValue == v:
                        modelInstance.use = k
                        break

        #Update Fermentable item
        if isinstance(modelInstance, Fermentable):
            logger.debug("Model update at [row=%d,column=%d]for Fermentable:%s; newValue=%s", row, column, modelInstance, newValue)
            fermentableLabels = FermentableViewLabels()
            if column == 1:
                #Update amount value
                try:
                    modelInstance.amount = FermentableView.display_to_amount(newValue)
                except ValueError as e:
                    logger.warn("Can't set Fermentable amount value to:'%s' %s", newValue, e)
                    item.setData(FermentableView.amount_to_display(modelInstance.amount), QtCore.Qt.DisplayRole)
            if column == 6:
                #Update form use
                if newValue == fermentableLabels.useLabels[model.constants.FERMENTABLE_USE_BOIL]:
                    modelInstance.useAfterBoil = False
                elif newValue == fermentableLabels.useLabels[model.constants.FERMENTABLE_USE_AFTER_BOIL]:
                    modelInstance.useAfterBoil = True

        #Update Misc item
        if isinstance(modelInstance, Misc):
            logger.debug("Model update at [row=%d,column=%d] for Misc:%s; newValue=%s", row, column, modelInstance, newValue)
            miscLabels = MiscViewLabels()
            if column == 1:
                #Update Misc amount value
                try:
                    modelInstance.amount = MiscView.display_to_amount(newValue)
                except ValueError as e:
                    logger.warn("Can't set Misc amount value to:'%s' %s", newValue, e)
                    item.setData(MiscView.amount_to_display(modelInstance.amount), QtCore.Qt.DisplayRole)
            if column == 2:
                #Update Misc time value
                try:
                    modelInstance.time = MiscView.display_to_time(newValue)
                except ValueError:
                    logger.warn("Can't set Misc time value to:'%s'", newValue)
                    item.setData(MiscView.time_to_display(modelInstance.time), QtCore.Qt.DisplayRole)
            if column == 6:
                #Update form use
                for (k,v) in miscLabels.useLabels.items():
                    if newValue == v:
                        modelInstance.use = k
                        break
        #Dump updates for debugging
        #for h in self.recipe.listeHops:
        #    logger.debug(h)
        #for h in self.recipe.listeFermentables:
        #    logger.debug(h)
        #for h in self.recipe.listeMiscs:
        #    logger.debug(h)

    def clearModele(self):
        count = self.modele.rowCount()
        logger.debug("%s items in modele", count)
        ret = self.modele.removeRows(0, count)
        logger.debug("removeRows returns %s", ret)
           
    def initModele(self) :

        logger.debug("initModele")
        if self.recipe is not None:
            self.clearModele()
            recipeView = RecipeView(self.recipe)
            
            for f in self.recipe.listeFermentables:
                fView = FermentableView(f)
                items = list()
                items.append( fView.QStandardItem_for_name() )
                items.append( fView.QStandardItem_for_amount() )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( fView.QStandardItem_for_type() )
                items.append( recipeView.QStandardItem_for_fermentable_proportion(f) )
                items.append( fView.QStandardItem_for_use() )
                self.modele.appendRow(items)

            for h in self.recipe.listeHops:
                hView = HopView(h)
                items = list()
                items.append( hView.QStandardItem_for_name() )
                items.append( hView.QStandardItem_for_amount() )
                items.append( hView.QStandardItem_for_time() )
                items.append( hView.QStandardItem_for_alpha() )
                items.append( hView.QStandardItem_for_form() )
                items.append (recipeView.QStandardItem_for_hop_ibu(h) )
                items.append( hView.QStandardItem_for_use() )
                self.modele.appendRow(items)

            for m in self.recipe.listeMiscs:
                mView = MiscView(m)
                items = list()
                items.append( mView.QStandardItem_for_name_type() )
                items.append( mView.QStandardItem_for_amount() )
                items.append( mView.QStandardItem_for_time() )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( mView.QStandardItem_for_use() )
                items.append( QtGui.QStandardItem('') )
                self.modele.appendRow(items)

            for y in self.recipe.listeYeasts:
                yView = YeastView(y)
                items = list()
                items.append( yView.QStandardItem_for_detail() )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                items.append( QtGui.QStandardItem('') )
                self.modele.appendRow(items)
                
    def editGrains(self) :
        self.dlgEditG.setModal(True)
        self.dlgEditG.show()
        
    def editHoublons(self) :
        self.dlgEditH.setModal(True)
        self.dlgEditH.show()
        
    def editDivers(self) :
        self.dlgEditD.setModal(True)
        self.dlgEditD.show()   
    
    def editLevures(self) :
        self.dlgEditY.setModal(True)
        self.dlgEditY.show()     
        
    def outilDens(self) : 
        self.dlgOutilDens.setModal(True)
        self.dlgOutilDens.show()
        
    def outilAlc(self) :
        self.dlgOutilAlc.setModal(True)
        self.dlgOutilAlc.show()
        
    def outilDilution(self) :
        self.dlgOutilDilution.setModal(True)
        self.dlgOutilDilution.show()
    
    def outilEvaporation (self) :
        self.dlgOutilEvaporation.setModal(True)
        self.dlgOutilEvaporation.show()
        
    def outilPaliers (self) :
        self.dlgOutilPaliers.setModal(True)
        self.dlgOutilPaliers.show()
        
    def dialogPreferences (self) :
        self.dlgPref.setModal(True)
        self.dlgPref.show()
        
    def stepAdjustBrewday(self) :
        self.tableWidgetStepsBrewday_currentRowChanged()
        self.dlgStepBrewday.setModal(True)
        self.dlgStepBrewday.show()
        self.dlgStepBrewday.setFields(self.brewdayCurrentStepTargetTemp, self.brewdayCurrentStepRatio, self.brewdayCurrentStepInfuseAmount, self.brewdayCurrentStepWaterTemp, self.grainWeight, self.stepsListVol, self.brewdayCurrentRow, self.brewdayListTemp, self.strikeTargetTemp)
        
        
    def purge (self) :
        self.clearModele()
        self.s = 0
        self.nouvelle()
        
    def newRecipeFromLibrary (self) :
        self.switchToEditor()
        self.purge()
            
    def ajouterF(self) :
        comboText = self.comboBox.currentText()
        #Find selected Fermentable in database and copy it in recipe as new Fermentable
        try:
            fBase = [f for f in ImportBase().listeFermentables if f.name == comboText][0]
            newFermentable = fBase.copy()
            newFermentable.amount = 1000
            newFermentable.useAfterBoil = False
            self.recipe.listeFermentables.append(newFermentable)
            #Refill listView model
            self.initModele()
        except IndexError as e:
            logger.error("Problème dans la base de données des Fermentables :%s", e)
        
    def ajouterH(self) : 
        comboText = self.comboBoxH.currentText()
        #Find selected Hop in database and copy it in recipe as new Hop
        try:
            hBase = [h for h in ImportBase().listeHops if h.name == comboText][0]
            newHop = hBase.copy()
            newHop.amount = 0
            newHop.time = 0.0
            self.recipe.listeHops.append(newHop)
            self.initModele()
        except IndexError as e:
            logger.error("Problème dans la base de données des Houblons :%s", e)
    
    def ajouterM(self) :
        comboText = self.comboBoxM.currentText()
        #Find selected Misc in database and copy it in recipe as new Misc object
        try:
            mBase = [m for m in ImportBase().listeMiscs if m.name == comboText][0]
            newMisc = mBase.copy()
            self.recipe.listeMiscs.append(newMisc)
            self.initModele()
        except IndexError as e:
            logger.error("Problème dans la base de données des Divers :%s", e)

    def ajouterY(self) :
        comboText = self.comboBoxY.currentText()
        #Find selected Misc in database and copy it in recipe as new Misc object
        yBase = None
        for y in ImportBase().listeYeasts :
            yView = YeastView(y)
            if yView.yeastDetailDisplay() == comboText:
                yBase = y
        if yBase == None:
            logger.error("Problème dans la base de données des Levures ...")
        else:
            newYeast = yBase.copy()
            self.recipe.listeYeasts.append(newYeast)
            self.initModele()
        
    def enlever(self) :
        selection = self.tableViewF.selectionModel()
        data = None
        logger.debug("Nb de lignes sélectionnées :%d", len(selection.selectedRows()))
        logger.debug("Nb de colonnes sélectionnées :%d", len(selection.selectedColumns()))
        for index in selection.selectedRows():
            logger.debug("data=%s", index.data(view.constants.MODEL_DATA_ROLE))
            data = index.data(view.constants.MODEL_DATA_ROLE)
            if data is not None:
                break

        logger.debug("selection=%s data=%s",selection, data)
        if data is not None:
            if isinstance(data, Hop):
                tailleAvant = len(self.recipe.listeHops)
                self.recipe.listeHops.remove(data)
                tailleApres = len(self.recipe.listeHops)
                logger.debug("%d houblon supprimé", (tailleAvant-tailleApres))
            elif isinstance(data, Fermentable):
                tailleAvant = len(self.recipe.listeFermentables)
                self.recipe.listeFermentables.remove(data)
                tailleApres = len(self.recipe.listeFermentables)
                logger.debug("%d fermentable supprimé", (tailleAvant-tailleApres))
            elif isinstance(data, Yeast):
                tailleAvant = len(self.recipe.listeYeasts)
                self.recipe.listeYeasts.remove(data)
                tailleApres = len(self.recipe.listeYeasts)
                logger.debug("%d levure supprimé", (tailleAvant-tailleApres))
            elif isinstance(data, Misc):
                tailleAvant = len(self.recipe.listeMiscs)
                self.recipe.listeMiscs.remove(data)
                tailleApres = len(self.recipe.listeMiscs)
                logger.debug("%d divers supprimé", (tailleAvant-tailleApres))
            else :
                logger.warn("Impossible de supprimer un ingrédient de type: %s", type(data))
            self.initModele()

    def importBeerXML(self) :
        fichierBeerXML = self.s

        arbre = ET.parse(fichierBeerXML)

        self.recipe = Recipe.parse(arbre)

        self.lineEditRecette.setText(self.recipe.name)
        self.lineEditGenre.setText(self.recipe.style)
        self.doubleSpinBox_2Volume.setValue(self.recipe.volume)
        self.doubleSpinBoxRendemt.setValue(self.recipe.efficiency)
        self.spinBoxBoil.setValue(self.recipe.boil)
        self.doubleSpinBoxVolPre.setValue(self.recipe.volume)
        
        if self.recipe.type == model.constants.RECIPE_TYPE_ALL_GRAIN :
            self.comboBoxType.setCurrentIndex(0)
        elif self.recipe.type == model.constants.RECIPE_TYPE_PARTIAL_MASH :
            self.comboBoxType.setCurrentIndex(2)
        elif self.recipe.type == model.constants.RECIPE_TYPE_EXTRACT :
            self.comboBoxType.setCurrentIndex(1)
        else :
            self.comboBoxType.setCurrentIndex(0)
        self.lineEditBrewer.setText(self.recipe.brewer)
        self.displayProfile()
        self.colorPreview()
        
        self.currentRecipeMash = self.recipe.mash
        try :
            self.popMashCombo()
            logger.debug("mash name: %s", self.recipe.mash.name)
            logger.debug("len(self.listMash): %s", len(self.listMash))
            logger.debug("len(self.mashProfilesBase.listeMashes): %s", len(self.mashProfilesBase.listeMashes))
            if self.recipe.mash.name is not None :
                # self.comboBoxMashProfiles.setCurrentIndex(len(self.listMash)-1)
                self.comboBoxMashProfiles.addItem(self.recipe.mash.name + "*")
                self.comboBoxMashProfiles.setCurrentIndex(len(self.mashProfilesBase.listeMashes))
            else :
                self.comboBoxMashProfiles.setCurrentIndex(-1)
        except :
            self.comboBoxMashProfiles.setCurrentIndex(-1)
                    
    def displayProfile(self) :     
        self.labelOGV.setText("%.3f" %(self.recipe.compute_OG()))
        self.labelFGV.setText("%.3f" %(self.recipe.compute_FG() ))
        self.labelEBCV.setText("%.0f" %(self.recipe.compute_EBC() ))
        self.labelIBUV.setText("%.0f" %(self.recipe.compute_IBU() ))
        self.labelAlcv.setText("%.1f%%" %(self.recipe.compute_ABV() ))
        self.labelRatioBuGu.setText("%.1f" %(self.recipe.compute_ratioBUGU()))
        
        
                        
    def volPreCalc(self) :
        indice = float(self.recipe.volume) / self.doubleSpinBoxVolPre.value()       
        self.GUS = self.recipe.compute_GU() * indice
        self.SG = 1+ (self.GUS/1000) 
        self.labelSG.setText("%.3f" %self.SG)
        
        
    def ouvrir_clicked (self) :    
        self.s = QtGui.QFileDialog.getOpenFileName(self,
            self.trUtf8("Ouvrir un fichier"),
            home_dir,
            )
        if not self.s :
            pass
        else :
            i = (AppWindow.nbreFer + AppWindow.nbreDivers + AppWindow.nbreHops + self.nbreLevures)
            self.modele.removeRows(0,i)
            AppWindow.nbreFer = 0
            AppWindow.nbreHops = 0
            AppWindow.nbreDivers = 0
            self.nouvelle()
            self.importBeerXML()
            self.calculs_recette()
            logger.debug("ouvrir_clicked -> MVC")
            self.MVC()
            self.switchToEditor()
       
    def openRecipeFile(self,filePath):
        self.s = filePath
        AppWindow.nbreFer = 0
        AppWindow.nbreHops = 0
        AppWindow.nbreDivers = 0
        self.nouvelle()
        self.importBeerXML()
        logger.debug("ouvrirRecipeFile -> MVC")
        self.initModele()
        self.switchToEditor()

    
    def about(self) : 
        QtGui.QMessageBox.about(self,
                self.trUtf8("A propos"),
                self.trUtf8("<h1>JolieBulle</h1> <b>version 2.7</b><br/>copyright (c) 2010-2012 Pierre Tavares<p> JolieBulle est un logiciel de lecture et de formulation de recettes de brassage.</p><p><a href =http://www.gnu.org/licenses/gpl-3.0.html>Licence : Version 3 de la Licence Générale Publique GNU</a></p><p>Certaines icônes proviennent du pack Faenza par Tiheum (Matthieu James), également distribué sous licence GPL.</p>"))
        
            
    def rendemt_changed(self) :
        if self.checkBoxIng.isChecked() :
            ratio = self.rendement/self.doubleSpinBoxRendemt.value()
            
            i = 0
            while i < AppWindow.nbreFer :
                i = i +1 
                if self.liste_fType[i-1] == 'Extract' :
                    pass
                else :
                    self.liste_fAmount[i-1] = self.liste_fAmount[i-1] * ratio
                    amount = QtGui.QStandardItem("%.0f" %(self.liste_fAmount[i-1]))
                    self.modele.setItem(i-1,1,amount)
            self.rendement = self.doubleSpinBoxRendemt.value()
            try :
                self.calculs_recette() 
            except :
                pass     
                    
        else :
            self.rendement = self.doubleSpinBoxRendemt.value()
            try :
                self.calculs_recette()
            except :
                pass
            
    def volume_changed(self) :
        if self.checkBoxIng.isChecked() :
            ratio = self.doubleSpinBox_2Volume.value()/float(self.volume)
            
            i = 0
            while i < AppWindow.nbreFer :
                i=i+1
                self.liste_fAmount[i-1] = self.liste_fAmount[i-1] * ratio
                self.volume = self.doubleSpinBox_2Volume.value()
                amount = QtGui.QStandardItem("%.0f" %(self.liste_fAmount[i-1]))
                self.modele.setItem(i-1,1,amount)
            
            h = 0
            while h < AppWindow.nbreHops :
                h = h + 1
                self.liste_hAmount[h-1] = self.liste_hAmount[h-1] * ratio
                self.volume = self.doubleSpinBox_2Volume.value()
                amount = QtGui.QStandardItem("%.3f" %(self.liste_hAmount[h-1]) )
                self.modele.setItem(i+h-1,1,amount)
            
            
            m = 0
            while m < AppWindow.nbreDivers :
                m = m + 1
                self.liste_dAmount[m-1] = self.liste_dAmount[m-1] * ratio
                self.volume = self.doubleSpinBox_2Volume.value()
                amount = QtGui.QStandardItem("%.0f" %(self.liste_dAmount[m-1]) )
                self.modele.setItem(i+h+m-1, 1, amount)
            try :
                self.calculs_recette()
            except:
                pass

        else :
            self.volume = self.doubleSpinBox_2Volume.value()
            try :
                self.calculs_recette()
            except :
                pass
            
    def typeChanged (self) :
        if self.comboBoxType.currentIndex() == 0 :
            self.typeRecette = "All Grain"
        if self.comboBoxType.currentIndex() == 1 :   
            self.typeRecette = "Extract"
        if self.comboBoxType.currentIndex() == 2 :
            self.typeRecette = "Partial Mash"

    def enregistrer (self) :
        exp=Export()
        self.nomRecette = self.lineEditRecette.text()
        self.styleRecette = self.lineEditGenre.text()   
        self.brewer = self.lineEditBrewer.text()        
        self.boil = self.spinBoxBoil.value()
        if not self.s : 
            #self.enregistrerSous()
            recettes = QtCore.QFile(recettes_dir)
            self.s =  recettes_dir +"/" + self.nomRecette + ".xml"
            if os.path.exists(self.s) :
                warning = QtGui.QMessageBox.warning(self,
                            self.trUtf8("Recette déjà existante"),
                            self.trUtf8("Ce nom de recette existe déjà. L'enregistrement a été annulé. Vous pouvez choisir un nouveau nom.")
                            )
                self.s=''
            else :
                exp.exportXML(self.nomRecette, self.styleRecette, self.typeRecette, self.brewer, self.volume, self.boil, self.rendement,self.OG, self.FG, AppWindow.nbreHops, self.liste_houblons, self.liste_hAmount, self.liste_hForm, self.liste_hTime, self.liste_hAlpha,self.liste_hUse, AppWindow.nbreFer, self.fNom, self.fAmount ,self.fType, self.fYield, self.fMashed, self.color, self.liste_ingr, self.liste_fAmount, self.liste_fType, self.liste_fYield, self.liste_fMashed, self.liste_fUse, self.liste_color, self.dNom, self.dAmount, self.dType, AppWindow.nbreDivers, self.liste_divers, self.liste_dAmount, self.liste_dType, self.liste_dTime,self.liste_dUse, self.nbreLevures, self.lNom, self.lForm, self.lLabo, self.lProd, self.lAtten, self.liste_levures, self.liste_lForm, self.liste_lLabo, self.liste_lProdid, self.liste_levureAtten, self.recipeNotes,self.currentMash)
                exp.enregistrer(self.s)
        else :

            
            exp.exportXML(self.nomRecette, self.styleRecette, self.typeRecette, self.brewer, self.volume, self.boil, self.rendement, self.OG, self.FG,AppWindow.nbreHops, self.liste_houblons, self.liste_hAmount, self.liste_hForm, self.liste_hTime, self.liste_hAlpha,self.liste_hUse, AppWindow.nbreFer, self.fNom, self.fAmount ,self.fType, self.fYield, self.fMashed, self.color, self.liste_ingr, self.liste_fAmount, self.liste_fType, self.liste_fYield, self.liste_fMashed, self.liste_fUse, self.liste_color, self.dNom, self.dAmount, self.dType, AppWindow.nbreDivers, self.liste_divers, self.liste_dAmount, self.liste_dType, self.liste_dTime,self.liste_dUse, self.nbreLevures, self.lNom, self.lForm, self.lLabo, self.lProd, self.lAtten, self.liste_levures, self.liste_lForm, self.liste_lLabo, self.liste_lProdid, self.liste_levureAtten, self.recipeNotes,self.currentMash)
            exp.enregistrer(self.s)
    
        
    def enregistrerSous (self) :
        exp=Export()
        self.nomRecette = self.lineEditRecette.text()  
        self.styleRecette = self.lineEditGenre.text()
        self.brewer = self.lineEditBrewer.text()  
        self.boil = self.spinBoxBoil.value()
        self.s = QtGui.QFileDialog.getSaveFileName (self,
                                                    self.trUtf8("Enregistrer dans un fichier"),
                                                    recettes_dir + "/" + self.nomRecette,
                                                    "BeerXML (*.xml)")
        exp.exportXML(self.nomRecette, self.styleRecette, self.typeRecette, self.brewer, self.volume, self.boil, self.rendement,self.OG, self.FG, AppWindow.nbreHops, self.liste_houblons, self.liste_hAmount, self.liste_hForm, self.liste_hTime, self.liste_hAlpha, self.liste_hUse, AppWindow.nbreFer, self.fNom, self.fAmount ,self.fType, self.fYield, self.fMashed, self.color, self.liste_ingr, self.liste_fAmount, self.liste_fType, self.liste_fYield, self.liste_fMashed, self.liste_fUse, self.liste_color, self.dNom, self.dAmount, self.dType, AppWindow.nbreDivers, self.liste_divers, self.liste_dAmount, self.liste_dType, self.liste_dTime, self.liste_dUse, self.nbreLevures, self.lNom, self.lForm, self.lLabo, self.lProd, self.lAtten, self.liste_levures, self.liste_lForm, self.liste_lLabo, self.liste_lProdid, self.liste_levureAtten, self.recipeNotes,self.currentMash)
        exp.enregistrer(self.s)  
    def exporterHtml (self) :
        self.nomRecette = self.lineEditRecette.text()
        self.styleRecette = self.lineEditGenre.text()
        
        exp = ExportHTML()
        self.h = QtGui.QFileDialog.getSaveFileName (self,
                                                    self.trUtf8("Enregistrer dans un fichier"),
                                                    self.nomRecette,
                                                    "HTML (*.html)")    
        
        self.fileHtml = QtCore.QFile(self.h)
        #exp.exportHtml(self.nomRecette,self.styleRecette, self.volume, self.boil, AppWindow.nbreFer, self.liste_ingr, self.liste_fAmount, self.liste_fUse, AppWindow.nbreHops, self.liste_houblons, self.liste_hAlpha, self.liste_hForm, self.liste_hAmount, self.liste_hTime,self.liste_hUse, AppWindow.nbreDivers, self.liste_divers, self.liste_dType, self.liste_dAmount, self.liste_dTime, self.liste_dUse, self.nbreLevures, self.liste_levuresDetail,self.rendement, self.OG, self.FG, self.ratioBuGu, self.EBC, self.ibuTot ,self.ABV, self.recipeNotes)
        exp.exportRecipeHtml(self.recipe)
        
        exp.enregistrerHtml(self.fileHtml)
    
    def copierBbcode (self):
        self.nomRecette = self.lineEditRecette.text()
        self.styleRecette = self.lineEditGenre.text()
        
        exp = ExportBBCode()
        exp.exportBbcode(self.nomRecette,self.styleRecette, self.volume, self.boil, AppWindow.nbreFer, self.liste_ingr, self.liste_fAmount, AppWindow.nbreHops, self.liste_houblons, self.liste_hAlpha, self.liste_hForm, self.liste_hAmount, self.liste_hTime,self.liste_hUse, AppWindow.nbreDivers, self.liste_divers, self.liste_dType, self.liste_dAmount, self.liste_dTime, self.liste_dUse, self.nbreLevures, self.liste_levuresDetail,self.rendement, self.OG, self.FG, self.EBC, self.ibuTot ,self.ABV, self.recipeNotes)
        
        app.clipboard().setText(exp.generatedBbcode)

    def modifierStyle (self) :
        if self.pushButtonChangerStyle.isChecked () :
            self.comboBoxStyle.show()
        else :
            self.comboBoxStyle.hide()   

    def volMore (self) :
        if self.pushButtonVolMore.isChecked() :
            self.widgetVol.show()
        else :
            self.widgetVol.hide()

            
    def nouvelle(self) :
        self.recipe = Recipe()
        self.recipe.name = self.trUtf8('Nouvelle Recette')
        self.recipe.efficiency = 0.75
        self.recipe.volume = 10
        self.recipe.boil = 60
        self.recipe.style = self.trUtf8('''Générique''')
        self.recipe.recipeNotes =''

        self.lineEditBrewer.setText('')
        self.comboBoxType.setCurrentIndex(0)
        self.lineEditRecette.setText(self.recipe.name)
        self.lineEditGenre.setText(self.recipe.style)
        self.doubleSpinBox_2Volume.setValue(self.recipe.volume)
        self.doubleSpinBoxRendemt.setValue(self.recipe.efficiency)
        self.spinBoxBoil.setValue(self.recipe.boil)
            
        self.currentMash = None
        self.listStepsAll = list()
        self.dicMashDetail = {}
        self.mashName=None
        self.popMashCombo()
        self.comboBoxMashProfiles.setCurrentIndex(-1)
        self.brewdayLock = 0
        
    def recharger(self) :
        if not self.s :
            pass
        else :
            self.clearModele()
            self.initModele()

                        
    def addStyle(self) :
        self.lineEditGenre.setText(self.comboBoxStyle.currentText())
        
    def recipeNotesClicked (self) :
        self.switchToNotes()
        self.textEditRecipeNotes.setText(self.recipe.recipeNotes)
    
    def recipeNotesAccepted (self) :
        self.switchToEditor()
        self.recipe.recipeNotes = self.textEditRecipeNotes.toPlainText()
        
    def recipeNotesRejected (self) :
        self.switchToEditor()
        
    def popMashCombo (self):
        self.listMash = self.mashProfilesBase.listeMashes
        self.comboBoxMashProfiles.clear() 
        for mash in self.mashProfilesBase.listeMashes :
           self.comboBoxMashProfiles.addItem(mash.name)
           
    def mashComboChanged (self) :
        #on remet le verrou à 0, il va falloir recalculer en repassant en brewday mode
        self.brewdayLock = 0
        self.enableBrewdayMode()
        try :
            i =self.comboBoxMashProfiles.currentIndex()
            self.currentMash = self.mashProfilesBase.listeMashes[i]
        except :
            self.currentMash = self.currentRecipeMash
        self.tableWidgetStepsBrewday_currentRowChanged()

        
    def seeMash(self) :
        self.switchToMash()
        self.listWidgetMashProfiles.clear() 
#        print(self.mashProfilesBase.listMash)
        self.numMash = self.mashProfilesBase.numMash
        self.numSteps = self.mashProfilesBase.numSteps
        self.listMash = self.mashProfilesBase.listMash
        self.listStepsAll = list()
        self.popMashList()
        self.pushButtonMashEdit.setEnabled(False)
        self.pushButtonRemoveProfile.setEnabled(False)
        self.pushButtonStepRemove.setEnabled(False)
        self.pushButtonStepEdit.setEnabled(False)
        
    def popMashList(self) :
        self.listWidgetMashProfiles.clear() 
        for name in self.listMash :
           self.listWidgetMashProfiles.addItem(name['name'])    
        for steps in self.listMash :
            dicStep = steps['mashSteps']
            self.listStepsAll.append(dicStep)
            
            
    def mashClicked(self) :
        self.listWidgetSteps.clear()         
        index = self.listWidgetMashProfiles.currentRow()
        self.listSteps = self.listStepsAll[index]
        self.dicMashDetail = self.listMash[index]
        for stepName in self.listSteps :
            self.listWidgetSteps.addItem(stepName['name'])
            
        self.labelStepName.setTextFormat(QtCore.Qt.RichText)   
        self.labelMashName.setText("<b>" + self.dicMashDetail['name'] + "</b>")
        self.labelMashPh.setText("%.1f" %float(self.dicMashDetail['ph']))
#        self.labelMashGrainTemp.setText("%.1f" %float(self.dicMashDetail['grainTemp']))
#        self.labelMashTunTemp.setText("%.1f" %float(self.dicMashDetail['tunTemp']))
        try :
            self.labelMashSpargeTemp.setText("%.1f" %float(self.dicMashDetail['spargeTemp']))
        except :
            pass
        try :
            self.listWidgetSteps.setCurrentRow(0)
        except :
            pass
#        print(self.dicMashDetail)
        self.pushButtonMashEdit.setEnabled(True)
        self.pushButtonRemoveProfile.setEnabled(True)
            
                
    def mashDetails(self) :

        # self.seeMash()
        # i = self.comboBoxMashProfiles.currentIndex()
        # self.listWidgetMashProfiles.setCurrentRow(i)
        self.dlgMashDetail = DialogMashDetail(self)
        self.dlgMashDetail.setModal(True)
        self.dlgMashDetail.show()
        self.dlgMashDetail.setFields(self.currentMash)
        print(self.currentMash)
        print(self.comboBoxMashProfiles.currentIndex())
        self.dlgMashDetail.setAttribute( QtCore.Qt.WA_DeleteOnClose, True ) 

        
    def stepDetails(self) :
        i = self.listWidgetSteps.currentRow()
        self.listStepName = list()
        self.listStepType = list()
        self.listStepTemp = list()
        self.listStepTime = list()
        self.listStepVol = list()  
        for stepName in self.listSteps :
            self.listStepName.append(stepName['name'])
        for stepType in self.listSteps :
            self.listStepType.append(stepType['type'])
        for stepTime in self.listSteps :
            self.listStepTime.append(float(stepTime['stepTime']))
        for stepTemp in self.listSteps :
            self.listStepTemp.append(float(stepTemp['stepTemp']))
        for stepVol in self.listSteps :
            self.listStepVol.append(float(stepVol['stepVol']))
            
        self.labelStepName.setTextFormat(QtCore.Qt.RichText)
        self.labelStepName.setText("<b>" + self.listStepName[i] +"</b>")            
        self.labelStepType.setText(self.listStepType[i])
        self.labelStepTemp.setText("%.1f" %(self.listStepTemp[i]))
        self.labelStepTime.setText("%.0f" %(self.listStepTime[i]))  
#        self.labelStepVol.setText("%.1f" %(self.listStepVol[i]))   
        self.pushButtonStepRemove.setEnabled(True)
        self.pushButtonStepEdit.setEnabled(True)
            
        
        
    def stepEdit(self) :
        i = self.listWidgetSteps.currentRow()
        self.dlgStep.show()
        self.dlgStep.fields (self.listStepName[i], self.listStepType[i], self.listStepTime[i], self.listStepTemp[i], self.listStepVol[i])
    
    def stepReload(self, stepName, stepType, stepTime, stepTemp ,stepVol) :
        f = self.listWidgetMashProfiles.currentRow()
        i = self.listWidgetSteps.currentRow()
        self.listStepName[i] = stepName
        self.listStepType[i] = stepType
        self.listStepTemp[i] = stepTemp
        self.listStepTime[i] = stepTime
        self.listStepVol[i] = stepVol
        dicCurrentStep = {}
        dicCurrentStep = {'name' : stepName, 'type' : stepType, 'stepTime' : stepTime, 'stepTemp' : stepTemp, 'stepVol' : stepVol}
        del self.listSteps[i]
        self.listSteps.insert(i, dicCurrentStep) 
        self.listWidgetSteps.clear() 
        self.seeMash()
        self.stepDetails()
        self.listWidgetMashProfiles.setCurrentRow(f)
        self.listWidgetSteps.setCurrentRow(i)
        
        
    def removeStep(self) :
        i = self.listWidgetSteps.currentRow()
        del self.listSteps[i]
        self.seeMash()
        
    def addStep(self) :
        f = self.listWidgetMashProfiles.currentRow()
        dicNewStep = {'name' : 'Nouveau Palier', 'type' : 'Infusion', 'stepTime' : '0', 'stepTemp' : '0', 'stepVol' : '0'}
        self.listSteps.append(dicNewStep)
        i = len(self.listSteps)
        self.listWidgetMashProfiles.setCurrentRow(f)
        self.seeMash()
        self.stepDetails()      
        self.listWidgetMashProfiles.setCurrentRow(f)
        self.listWidgetSteps.setCurrentRow(i-1)
        self.stepEdit()
        
        
    def mashEdit(self) :
        i = self.listWidgetMashProfiles.currentRow()
        self.dlgMash.show()
        self.dlgMash.fields(self.dicMashDetail['name'],self.dicMashDetail['ph'],self.dicMashDetail['grainTemp'],self.dicMashDetail['tunTemp'],self.dicMashDetail['spargeTemp'])
        
    def mashReload(self,name,ph,grainT,tunT,spargeT) :
        #on remet le verrou à 0, il va falloir recalculer en repassant en brewday mode
        self.brewdayLock = 0
        
        f = self.listWidgetMashProfiles.currentRow()
        self.dicMashDetail['name'] = name
        self.dicMashDetail['ph'] = ph
        self.dicMashDetail['grainTemp'] = 20
        self.dicMashDetail['tunTemp'] = 20
        self.dicMashDetail['spargeTemp'] = spargeT
        del self.listMash[f]
        self.listMash.insert(f, self.dicMashDetail)
        self.popMashList()
        self.listWidgetMashProfiles.setCurrentRow(f)
        
#        print(self.dicMashDetail)

    def addMash(self) :
        dicNewMash = {'name' : 'Nouveau profil', 'grainTemp' : '0', 'tunTemp' : '0', 'spargeTemp' : '78', 'ph' : '5.4', 'mashSteps' : [{'name' : 'Nouveau Palier', 'type' : 'Infusion', 'stepTime' : '0', 'stepTemp' : '0', 'stepVol' : '0'}]}
        self.listMash.append(dicNewMash)
        self.seeMash()
        self.listWidgetMashProfiles.setCurrentRow(len(self.listMash)-1)
        
    def removeMash(self) :
        i = self.listWidgetMashProfiles.currentRow()
        del self.listMash[i]
        self.seeMash()
        self.listWidgetSteps.clear() 
        
    def mashRejected (self) :
        self.mashProfilesBase.importBeerXML()
        self.switchToEditor()
        
    def mashAccepted (self) :
        i = self.listWidgetMashProfiles.currentRow()
        self.currentMash = self.listMash[i]
        self.popMashCombo()
        self.switchToEditor()
        self.comboBoxMashProfiles.setCurrentIndex(i)
        logger.debug(self.currentMash)
        
    def saveProfile(self) : 
        self.mashProfileExport.export(self.listMash)
        self.mashProfileExport.enregistrer(mash_file)
        
        
    def brewdayModeCalc(self) :
        self.labelWarningBiab.hide() 
        self.brewdayLock = 1
    
        if self.radioButtonClassicBrew.isChecked() :
            self.labelNoSparge.hide()
            self.labelSparge1.show()
            self.labelSparge2.show()
            self.labelSpargeTemp.show()
            self.labelSpargeVol.show()            
        else :
            self.labelNoSparge.show()
            self.labelSparge1.hide()
            self.labelSparge2.hide()
            self.labelSpargeTemp.hide()
            self.labelSpargeVol.hide()
            
        self.labelNoDecoction.hide()
                
        self.brewCalc.calcPreBoilVolume(self.volume, self.spinBoxBoil.value())
        
        self.brewCalc.calcPreBoilSg(self.GU, self.volume)
       
        
        self.labelPreBoilVol.setText("%.1f" %(self.brewCalc.volPreBoil) + " " + "L")
        self.labelPreBoilGravity.setText("%.3f" %(self.brewCalc.preBoilSg))
        
        
        listSteps = self.currentMash['mashSteps']
        spargeTemp = float(self.currentMash['spargeTemp'])
#        print("la liste en breday mode", listSteps)
        
        strikeStep = listSteps[0]
        strikeTargetTemp = strikeStep['stepTemp']
        strikeName = strikeStep['name']
        strikeTime = strikeStep['stepTime']
        
        self.tableWidgetStepsBrewday.setRowCount(len(listSteps))
        
#       si on n'est pas dans le cas d'un BIAB
        if self.radioButtonClassicBrew.isChecked() :
            self.brewCalc.calcStrikeTemp(strikeTargetTemp, 3)
            self.brewCalc.calcStrikeVol(self.grainWeight, 3)
            self.brewCalc.calcMashVolume(self.grainWeight)
            self.brewCalc.calcGrainRetention(self.grainWeight)
            self.pushButtonAdjustStep.setEnabled(True)
        
            listVol = []
            listVol.append(self.brewCalc.strikeVol)
            self.brewdayListTemp = []
            listName = []
            #on traite les paliers autres que l'empâtage,
            i = 0
            while i < len(listSteps)-1 :
                i = i+1 
                step = listSteps[i]
                stepName = step['name']
    #            stepVol =  float(step['stepVol'])
                stepTemp = float(step['stepTemp'])
                stepType= step['type']  
                stepTime = step['stepTime']          
                
                listName.append(stepName)
                self.brewdayListTemp.append(stepTemp)
                if i == 1 :
                    mashTemp = strikeTargetTemp
                elif i != 1 :
                    mashTemp = self.brewdayListTemp[i-2]
                
                self.brewCalc.calcInfusionStep(i, self.grainWeight, listVol, stepTemp, mashTemp, 90, stepType )

                listVol.append(self.brewCalc.infuseVol)
                
                self.tableWidgetStepsBrewday.setItem(i,0,QtGui.QTableWidgetItem(stepName))
                self.tableWidgetStepsBrewday.setItem(i,1,QtGui.QTableWidgetItem("%.1f" %(self.brewCalc.infuseVol)))
                if stepType == 'Infusion' :
                    self.tableWidgetStepsBrewday.setItem(i,2,QtGui.QTableWidgetItem(str(90)))
                elif stepType == 'Temperature' :
                    self.tableWidgetStepsBrewday.setItem(i,2,QtGui.QTableWidgetItem(str(0)))
                else : 
                    self.labelNoDecoction.show()
                    
                self.tableWidgetStepsBrewday.setItem(i,3,QtGui.QTableWidgetItem("%.1f" %(self.brewCalc.newRatio))) 
                self.tableWidgetStepsBrewday.setItem(i,4,QtGui.QTableWidgetItem("%.1f" %(stepTemp) + "°C, " + stepTime +" min"))         

            
              
            self.tableWidgetStepsBrewday.setItem(0,0,QtGui.QTableWidgetItem(strikeName))
            self.tableWidgetStepsBrewday.setItem(0,1,QtGui.QTableWidgetItem(str(self.brewCalc.strikeVol)))
            self.tableWidgetStepsBrewday.setItem(0,2,QtGui.QTableWidgetItem("%.1f" %(self.brewCalc.strikeTemp)))
            self.tableWidgetStepsBrewday.setItem(0,3,QtGui.QTableWidgetItem("%.1f" %(self.brewCalc.strikeVol/(self.grainWeight/1000))))
            self.tableWidgetStepsBrewday.setItem(0,4,QtGui.QTableWidgetItem(str(strikeTargetTemp) + "°C, " + str(strikeTime) +" min"))
            
            self.stepsListVol = listVol
            
            self.brewCalc.calcSpargeVol(self.stepsListVol, self.brewCalc.volPreBoil, self.brewCalc.grainRetention)
    #        print('volume de rinçage :', self.brewCalc.spargeVol)
    
            self.labelSpargeVol.setText("%.1f" %(self.brewCalc.spargeVol))
            self.labelSpargeTemp.setText("%.1f" %(spargeTemp))

            #on calcule les volumes
            self.brewCalc.calcMashVolume(self.grainWeight)
            self.mashVolumeLastStep = self.brewCalc.grainVolume + sum(self.stepsListVol)
            self.labelGrainVolume.setText("%.1f" %(self.brewCalc.grainVolume))       
            self.labelTotalVolumeStrike.setText("%.1f" %(self.brewCalc.mashVolumeStrike)) 
            self.labelTotalVolumeLast.setText("%.1f" %(self.mashVolumeLastStep))
    
        else :
            self.brewCalc.calcGrainRetention(self.grainWeight)
            self.strikeVol = self.brewCalc.volPreBoil + self.brewCalc.grainRetention
            ratio = self.strikeVol / (self.grainWeight / 1000)
            self.brewCalc.calcStrikeTemp(strikeTargetTemp,ratio)
                
            self.tableWidgetStepsBrewday.setItem(0,0,QtGui.QTableWidgetItem(strikeName))
            self.tableWidgetStepsBrewday.setItem(0,1,QtGui.QTableWidgetItem("%.1f" %(self.strikeVol)))
            self.tableWidgetStepsBrewday.setItem(0,2,QtGui.QTableWidgetItem("%.1f" %(self.brewCalc.strikeTemp)))
            self.tableWidgetStepsBrewday.setItem(0,3,QtGui.QTableWidgetItem("%.1f" %(ratio)))
            self.pushButtonAdjustStep.setEnabled(False)

            #on calcule les volumes
            self.brewCalc.calcMashVolume(self.grainWeight)
            self.mashVolumeLastStep = self.brewCalc.grainVolume + sum(self.stepsListVol)
            self.labelGrainVolume.setText("%.1f" %(self.brewCalc.grainVolume))       
            self.labelTotalVolumeStrike.setText("%.1f" %(self.strikeVol + self.brewCalc.grainVolume)) 
            self.labelTotalVolumeLast.setText("idem")
            
            #on vérifie que le profil est bien compatible avec un BIAB :
            i = 0
            while i < len(listSteps)-1 :
                i = i+1 
                step = listSteps[i]
                stepType= step['type']
                if stepType != "Temperature" :
                    self.labelWarningBiab.show()
                else :
                    pass
                    
        


            
        
    def tableWidgetStepsBrewday_currentRowChanged (self) :
        listSteps = self.currentMash.listeSteps
        strikeStep = listSteps[0]
        self.strikeTargetTemp = strikeStep.temp
        self.brewdayCurrentRow = self.tableWidgetStepsBrewday.currentRow()
        i = self.tableWidgetStepsBrewday.currentRow()
        if i == -1 :
            return  #No selection in tableWidgetStepsBrewday

        step = listSteps[i]
        stepType= step.type
        
        self.brewdayCurrentStepName = self.tableWidgetStepsBrewday.item(i,0).text()
        self.brewdayCurrentStepInfuseAmount = self.tableWidgetStepsBrewday.item(i,1).text()
        self.brewdayCurrentStepWaterTemp = self.tableWidgetStepsBrewday.item(i,2).text()
        self.brewdayCurrentStepRatio = self.tableWidgetStepsBrewday.item(i,3).text()
        if i == 0 :
            self.brewdayCurrentStepTargetTemp = strikeTargetTemp
        else :
            self.brewdayCurrentStepTargetTemp = self.brewdayListTemp[i-1]
            
        if stepType == 'Infusion' and self.radioButtonClassicBrew.isChecked ():
            self.pushButtonAdjustStep.setEnabled(True)
        else :
            self.pushButtonAdjustStep.setEnabled(False)
            
            
    def stepAdjustBrewday_closed (self, targetRatio, infuseAmount, waterTemp,listVol, currentRow, listTemp) :
        #on insère les nouvelles données dans la table
        self.tableWidgetStepsBrewday.setItem(currentRow,1,QtGui.QTableWidgetItem(str(infuseAmount)))
        self.tableWidgetStepsBrewday.setItem(currentRow,2,QtGui.QTableWidgetItem("%.1f" %(waterTemp)))
        self.tableWidgetStepsBrewday.setItem(currentRow,3,QtGui.QTableWidgetItem("%.1f" %(targetRatio)))
        #il faut tout recalculer après la ligne modifiée
        listSteps = self.currentMash.listeSteps
        
        i = currentRow
        

        while i < len(listSteps) - 1 :
            i = i+1
            step = listSteps[i]
            stepType= step['type'] 
            stepTemp = float(step['stepTemp'])
            if i == 1 :
                strikeStep = listSteps[0]
                strikeTargetTemp = strikeStep['stepTemp']
                mashTemp = strikeTargetTemp
            else :
                mashTemp = self.brewdayListTemp[i-2]
            self.brewCalc.calcInfusionStep(i-1, self.grainWeight, listVol, stepTemp, mashTemp, 90, stepType )
#            listVol.append(self.brewCalc.infuseVol)
            listVol[i] = self.brewCalc.infuseVol
            self.tableWidgetStepsBrewday.setItem(i,1,QtGui.QTableWidgetItem("%.1f" %(self.brewCalc.infuseVol)))
            self.tableWidgetStepsBrewday.setItem(i,3,QtGui.QTableWidgetItem("%.1f" %(self.brewCalc.newRatio)))
            if stepType == 'Infusion' :
                self.tableWidgetStepsBrewday.setItem(i,2,QtGui.QTableWidgetItem("%.1f" %(90)))
            else :
                self.tableWidgetStepsBrewday.setItem(i,2,QtGui.QTableWidgetItem("%.1f" %(0)))
            
            
        #on calcule les volumes
        # self.brewCalc.calcMashVolume(self.grainWeight)
        self.mashVolumeLastStep = self.brewCalc.grainVolume + sum(self.stepsListVol)
        self.labelGrainVolume.setText("%.1f" %(self.brewCalc.grainVolume))       
        self.labelTotalVolumeStrike.setText("%.1f" %(self.brewCalc.grainVolume+listVol[0])) 
        self.labelTotalVolumeLast.setText("%.1f" %(self.mashVolumeLastStep))
            
#            print('température du moût', mashTemp)
            
        self.brewCalc.calcSpargeVol(self.stepsListVol, self.brewCalc.volPreBoil, self.brewCalc.grainRetention)
#        print('volume de rinçage :', self.brewCalc.spargeVol)

        self.tableWidgetStepsBrewday_currentRowChanged()
        
    def unlockBrewdayMode (self) :  
        self.brewdayLock = 0 

    def enableBrewdayMode(self) :
        if self.comboBoxMashProfiles.currentIndex() == -1 :
            # self.pushButtonBrewdayMode.setEnabled(False)
            pass
        else :
            # self.pushButtonBrewdayMode.setEnabled(True)
            pass
        

    def printRecipe (self) :
        printer=QtGui.QPrinter()
        dialog = QtGui.QPrintDialog(printer)
        dialog.setModal(True)
        dialog.setWindowTitle("Print Document" )
        # dialog.addEnabledOption(QAbstractPrintDialog.PrintSelection)
        if dialog.exec_() == True:
            self.webViewBiblio.print(printer)
                

from plugins import PluginManager
from plugins.ExtensionPoints import AppLifecycleExtensionPoint

if __name__ == "__main__":

    initLogging()

    logger = logging.getLogger(__name__)

    for p in AppLifecycleExtensionPoint.plugins:
        p().startup()

    logger.debug("Initializing UI");
    QtCore.QTextCodec.setCodecForCStrings(QtCore.QTextCodec.codecForName("utf-8"))
    app = QtGui.QApplication(sys.argv)
    
    locale = QtCore.QLocale.system().name()
    translator=QtCore.QTranslator ()
    #~ translator.load(("qt_") +locale, QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    translator.load('joliebulle_' + locale)
    app.installTranslator(translator)

    translatorQt = QtCore.QTranslator ()
    translatorQt.load('qt_' + locale)
    app.installTranslator(translatorQt)

    main_window = AppWindow()
    #main_window = MainWindow()
    main_window.show()

    logger.debug("UI initialized");

    app.exec_()

    for p in AppLifecycleExtensionPoint.plugins:
        p().shutdown()

