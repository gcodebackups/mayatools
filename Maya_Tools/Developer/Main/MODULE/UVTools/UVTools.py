import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
from pymel.core import *
import functools 
import boltUvRatio
import math

import Source.IconResource_rc
reload(Source.IconResource_rc)


try:
    reload(uv)
except:
    from MODULE.CheckList_QA import UVFlipped as uv

import CommonFunctions as cf
reload(cf)

from MODULE.PolyTools import PolyTools as pt
reload(pt)

from MODULE.ShaderTools import ShaderTools as st
reload(st)

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/UVTools.ui'

form_class, base_class = uic.loadUiType(dirUI)

class UVTools(form_class,base_class):
    def __init__(self, inputFile):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'UV tools'
        
        self.btnUp.clicked.connect(functools.partial(self.moveUVShell,'up'))
        self.btnDown.clicked.connect(functools.partial(self.moveUVShell,'down'))
        self.btnLeft.clicked.connect(functools.partial(self.moveUVShell,'left'))
        self.btnRight.clicked.connect(functools.partial(self.moveUVShell,'right'))
        
        self.btnSetUVScale.clicked.connect(self.setUVScale)
        self.btnGetUVScale.clicked.connect(self.getUVScale)
        
        self.btnSetTexel.clicked.connect(functools.partial(self.setUVScale))

        self.btnMirrorU.clicked.connect(functools.partial(self.mirrorUV,'H'))
        self.btnMirrorV.clicked.connect(functools.partial(self.mirrorUV,'V'))
        
        self.cbbSourceMat.addItems(['Materials from source'])
        self.cbbTargetMat.addItems(['Materials from target'])
        
        self.ldtSource.addActions([self.actionAddSource, self.actionClearSource, self.actionCopySource, self.actionPasteSource])
        self.ldtTarget.addActions([self.actionAddTarget,self.actionClearTarget, self.actionCopyTarget, self.actionPasteTarget])
        
        self.actionAddSource.triggered.connect(functools.partial(self.getNameFromSelected, 'Source'))
        self.actionAddTarget.triggered.connect(functools.partial(self.getNameFromSelected, 'Target'))
        
        self.actionClearSource.triggered.connect(functools.partial(self.clear, 'Source'))
        self.actionClearTarget.triggered.connect(functools.partial(self.clear, 'Target'))
        
        self.actionCopySource.triggered.connect(functools.partial(self.copy, 'Source'))
        self.actionCopyTarget.triggered.connect(functools.partial(self.copy, 'Target'))
        
        self.actionPasteSource.triggered.connect(functools.partial(self.paste, 'Source'))
        self.actionPasteTarget.triggered.connect(functools.partial(self.paste, 'Target'))
        
        self.ldtSource.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ldtTarget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.cbbSourceMat.currentIndexChanged.connect(self.autoSync)
        self.btnTransferUV.clicked.connect(self.transferUV)
        
        self.ldtTarget.returnPressed.connect(functools.partial(self.updateShader, 'Source'))
        self.ldtSource.returnPressed.connect(functools.partial(self.updateShader, 'Target'))
        
        self.btnSelectFlippedUVs.pressed.connect(self.selectFlippedUVs)
        #self.btnSelectUnmappedVertexes.pressed.connect()
        
    def filterTheFirstFaceInCluster(self, inList):
        out = list()
        exit = False
        while not exit:
            cmds.select(mesh[0])
            mel.eval('ConvertSelectionToUVShell')
            selFaces = set(cmds.ls(sl = True, fl = True )) 
            a = selFaces.intersection(inList)

    def moveUVShell(self, direction):
        if direction == 'down':
            cmds.polyEditUVShell( u = 0, v = -float(self.lineEdit.text()))
        if direction == 'up':
            cmds.polyEditUVShell( u = 0, v = float(self.lineEdit.text()))
        if direction == 'left':
            cmds.polyEditUVShell( u = -float(self.lineEdit.text()), v = 0)
        if direction == 'right':
            cmds.polyEditUVShell( u = float(self.lineEdit.text()), v = 0)
    
    def validateInfo(self):
        try:
            texel = float(self.ldtTexel.text())
            res = float(self.ldtRes.text())
            ratio = float(self.ldtRatio.text())
        except:
            QtGui.QMessageBox.information(self, 'Wrong data', 'Vui long xem lai cac thong so can thiet da dung chua?', buttons=QMessageBox_Ok, defaultButton=QMessageBox_NoButton)
    
    def setUVScale(self):
        boltUvRatio.collect_shells_and_set_shells_UV_ratio(float(self.ldtRatio.text()))
    
    def getUVScale(self):
        ratio = boltUvRatio.get_sel_faces_UV_ratio(1)
        self.ldtRatio.setText(str(1/ratio))
        
    def on_ldtRes_returnPressed(self):
        #self.validateInfo()
        self.ldtTexel.setText( str(float(self.ldtRes.text())/math.sqrt(float(self.ldtRatio.text()))))
    
    def on_ldtRatio_returnPressed(self):
        #self.validateInfo()
        self.ldtTexel.setText( str ( float(self.ldtRes.text())/math.sqrt(float(self.ldtRatio.text()))))
        
    def on_ldtTexel_returnPressed(self):
        #self.validateInfo()
        self.ldtRatio.setText( str(math.pow(float(self.ldtRes.text())/float(self.ldtTexel.text()),2)) )
        
    def openUVRatioToolBox(self):
        reload(UvRatio)
        self.uvRatio = UvRatio.UVRatio()
        self.uvRatio.show()
        
    def mirrorUV(self,direction):#, pivotPoint = setPivotMirror()):
        meshes = cmds.ls(hl = True)
        UVs = cmds.ls(sl = True)
        filterMesh = []
        for i in meshes:
            temp = []
            for j in UVs:
                if j.split('.')[0] == i:
                    temp.append(j)
            filterMesh.append(temp)
        cmds.select(cl = True)
        for l in filterMesh:
            try:
                cmds.select(l)
                if direction == 'V':
                    cmds.polyMoveUV(pivot = [0,0], scaleV = -1)
                if direction == 'H':
                    cmds.polyMoveUV(pivot = [0,0], scaleU = -1)
            except:
                pass
            
    def createRightClickonMenu_on_selectedItems(self,pos):
            RightClickMenu = QtGui.QMenu(self)
            RightClickMenu.addAction(self.actionAdd)
            RightClickMenu.exec_(QtGui.QCursor.pos())
            
    def getNameFromSelected(self, widget):
        objName = cmds.ls(sl = True)[0]
        shaders = st.getShadersFromMesh(objName)
        #print shaders
        # ---------------------------
        if widget =='Source':
            self.ldtSource.setText(objName)
            self.cbbSourceMat.clear()
            self.cbbSourceMat.addItems(list(set(shaders)))
            # test whether material in source and target matched together
            
        if widget =='Target':
            self.ldtTarget.setText(objName)
            self.cbbTargetMat.clear()
            self.cbbTargetMat.addItems(list(set(shaders)))
            
    def clear(self, widget):
        if widget =='Source':
            self.ldtSource.setText('')
            self.cbbSourceMat.clear()
            self.cbbSourceMat.addItems(['Materials from source'])
        
        if widget =='Target':
            self.ldtTarget.setText('')
            self.cbbTargetMat.clear()
            self.cbbTargetMat.addItems(['Materials from target'])
            
    def copy(self, widget):
        if widget =='Source':
            cf.setDataToClipboard(self.ldtSource.text())
        if widget =='Target':
            cf.setDataToClipboard(self.ldtTarget.text())
            
    def paste(self, widget):
        if widget =='Source':
            self.ldtSource.setText(cf.getDataFromClipboard())
            shaders = st.getShadersFromMesh(str(self.ldtSource.text()))
            self.cbbSourceMat.clear()
            self.cbbSourceMat.addItems(list(set(shaders)))
        if widget =='Target':
            self.ldtTarget.setText(cf.getDataFromClipboard())
            shaders = st.getShadersFromMesh(str(self.ldtTarget.text()))
            self.cbbTargetMat.clear()
            self.cbbTargetMat.addItems(list(set(shaders)))
            
    def updateShader(self, widget):
        if widget =='Source':
            self.ldtSource.update()
            shaders = st.getShadersFromMesh(str(self.ldtSource.text()))
            self.cbbSourceMat.clear()
            self.cbbSourceMat.addItems(list(set(shaders)))
        if widget =='Target':
            self.ldtTarget.update()
            shaders = st.getShadersFromMesh(str(self.ldtTarget.text()))
            self.cbbTargetMat.clear()
            self.cbbTargetMat.addItems(list(set(shaders)))
        
    def autoSync(self):
        mat = self.cbbSourceMat.currentText()
        id = self.cbbTargetMat.findText(mat, QtCore.Qt.MatchExactly|QtCore.Qt.MatchCaseSensitive)
        if id != -1:
            self.cbbTargetMat.setCurrentIndex(id)
            
    def transferUV(self):
        isAttached = False
        isDeleted = False
        # testing if node just have one shader
        shaders = st.getShadersFromMesh(str(self.ldtSource.text()))
        if len(shaders) > 1:
            st.selectFaceByShaderPerMesh(str(self.ldtSource.text()), str(self.cbbSourceMat.currentText()))
            pt.extractMesh()
            sourceMesh = py.ls(sl = True)[0]
            isDeleted = True
        elif len(shaders) == 1: 
            sourceMesh = str(self.ldtSource.text())
        elif len(shaders) == 0:
            QtGui.QMessageBox.critical(None, 'No shader found', 'Exit!', QtGui.QMessageBox.Ok)
            return
        #------------------------------------
        shaders = st.getShadersFromMesh(str(self.ldtTarget.text()))
        if len(shaders) > 1:
            st.selectFaceByShaderPerMesh(str(self.ldtTarget.text()), str(self.cbbTargetMat.currentText()))
            pt.detachMesh()
            targetMesh = py.ls(sl = True)[0]
        elif len(shaders) == 1:
            isAttached = False 
            targetMesh = str(self.ldtTarget.text())
        elif len(shaders) == 0:
            QtGui.QMessageBox.critical(None, 'No shader found', 'Exit!', QtGui.QMessageBox.Ok)
            return
        # transfer source mesh to target
        cmds.transferAttributes(sourceMesh, targetMesh, uvs = 2)
        # post-processing 
        cmds.select(targetMesh)
        mel.eval('DeleteHistory;')
        
        cmds.select(str(self.ldtTarget.text()))
        cmds.select(targetMesh, add = True)
        if isAttached:
            pt.attachMesh()
        if isDeleted:
            cmds.delete(sourceMesh)
            
    def selectFlippedUVs(self):
        mesh = cmds.ls(sl = True)[0]
        result = uv.run(mesh)
        cmds.select(result(2))
    
        
def main(xmlFile):
    form = UVTools(xmlFile)
    return form  