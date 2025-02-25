import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect

import functools 

import CommonFunctions as cf
reload(cf)

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/ThirdpartyTools.ui'

# set icon path

form_class, base_class = uic.loadUiType(dirUI)

class ThirdpartyTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'Third Party tools'
        self.load()
        
    def load(self):
        melScripts = [f for f in os.listdir(fileDirCommmon + '/mel/') if f.endswith('mel')]
        pythonScripts = [f for f in os.listdir(fileDirCommmon + '/python/') if f.endswith('py')]
        for script in melScripts + pythonScripts:
            icon = QtGui.QIcon()
            size = QtCore.QSize(200, 30)
            size.scale(200, 30, QtCore.Qt.KeepAspectRatio)
            icon.addFile(fileDirCommmon + '/icons/' + script.split('.')[0] + '.png', size)
            button = QtGui.QPushButton('')
            button.setIcon(icon)
            button.setIconSize(size)
            self.verticalLayout.addWidget(button)
            if script in melScripts:
                attachFileSource = (fileDirCommmon + '/mel/' +  script).replace('\\' ,'/')
                button.clicked.connect(functools.partial(self.sourceMelScript, attachFileSource))
            if script in pythonScripts:
                dir = fileDirCommmon + '/python/' + script
                module = cf.loadModule_v2(dir)
                button.clicked.connect(module.main)
                
    def sourceMelScript(self, melScript):
        mel.eval('source \"{file}\";'.format(file = melScript))

def main(xmlFile):
    form = ThirdpartyTools(xmlFile)
    return form             