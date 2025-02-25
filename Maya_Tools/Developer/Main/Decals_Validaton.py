# import maya.cmds as cmds
# import maya.mel as mel
# import maya.OpenMayaUI as OpenMayaUI
# import os, sys, re, inspect , imp, shutil
# import math
# from pymel.core import *
# from PySide import QtGui, QtCore
# import pysideuic
# import xml.etree.ElementTree as xml
# from cStringIO import StringIO
# import shiboken
# import functools

# -- Custom variables. Please alter these vars

dirUI = 'D:/maya_Tools/Maya_Tools/Developer/Main/UI/Decal_Form.ui'
logoPath = 'D:/3D_Works/Dropbox/Shader_Development/logo.tif'
bgPath = 'D:/3D_Works/Dropbox/wireframe.tif'

#-------------------------------------------------------------

def wrapinstance(ptr, base=None):
    if ptr is None:
        return None
    ptr = long(ptr) #Ensure type
    if globals().has_key('shiboken'):
        if base is None:
            qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr(QtGui, cls):
                base = getattr(QtGui, cls)
            elif hasattr(QtGui, superCls):
                base = getattr(QtGui, superCls)
            else:
                base = QtGui.QWidget
        return shiboken.wrapInstance(long(ptr), base)
    elif globals().has_key('sip'):
        base = QtCore.QObject
        return sip.wrapinstance(long(ptr), base)
    else:
        return None

def loadUiType(uiFile):
        parsed = xml.parse(uiFile)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text
    
        with open(uiFile, 'r') as f:
            o = StringIO()
            frame = {}
            
            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec pyc in frame
            
            #Fetch the base_class and form class based on their type in the xml from designer
            form_class = frame['Ui_%s'%form_class]
            base_class = eval('QtGui.%s'%widget_class)
        return form_class, base_class

try:
    form_class, base_class = loadUiType(dirUI)
except IOError:
    print (dirUI + ' not found')
    
def getMayaWindow():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapinstance(long(ptr), QtGui.QWidget)

class Decal(QtGui.QGraphicsPixmapItem):
            
    def __init__(self, path, parent = None):
        super(Decal, self).__init__(parent)
        self.setPixmap(QtGui.QPixmap(path))
        self.size = 1
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, enabled = True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, enabled = True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, enabled = True)
        self.scaleFactor = 1
        
    def setSignalPos(self, dx, dy):
        pos = QtCore.QPointF(dx * 550 / 100.0 - self.boundingRectCustom().width()/2, dy * 550 / 100.0 - self.boundingRectCustom().height()/2)
        self.setPos(pos)

        
    def getCenter(self):
        return self.transformOriginPoint() 
        
    def setCenter(self):
        pos = QtCore.QPointF()
        pos.setX(self.boundingRectCustom().width()/2)
        pos.setY(self.boundingRectCustom().height()/2)
        return pos        
        
    def boundingRectCustom(self):
        rect = QtCore.QRectF()
        rect.setWidth(self.boundingRect().width() * self.scaleFactor)
        rect.setHeight(self.boundingRect().height() * self.scaleFactor)
        return rect
    
    def posCustom(self):
        posF = QtCore.QPointF()
        posF.setX(self.pos().x() + self.boundingRectCustom().width()/2)
        posF.setY(self.pos().y() + self.boundingRectCustom().height()/2)
        return posF

class DecalScene(QtGui.QGraphicsScene):
    insertDecal, moveDecal = range(2)
    
    decalMoved = QtCore.Signal(QtCore.QPointF)
    
    decalScaled = QtCore.Signal(float)
    
    def __init__(self, bg, dc, parent = None):
        super(DecalScene, self).__init__(0, 0, 550, 550, parent)
        self._backgroundImage = QtGui.QPixmap(bg).scaled(self.sceneRect().width(), self.sceneRect().height(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self._decalImage = QtGui.QPixmap(dc)
        self.myMode = self.insertDecal
        self.cursorPos = QtCore.QPointF()
        self.decal = Decal(self._decalImage)
        self.originRatio = 550.0/self.decal.boundingRect().height()
        
    def addGraphicsItem(self):
        self.decal = Decal(self._decalImage)
        
    def setMode(self, mode):
        self.myMode = mode
        
    def drawBackground(self, QPainter, QRect):
         QRect = self.sceneRect()
         QPoint = QtCore.QPointF(QRect.top(), QRect.left())
         QPainter.drawPixmap(QPoint, self._backgroundImage, QRect)
        
    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() != QtCore.Qt.LeftButton:
            return
        if self.myMode == self.insertDecal:
            #self.addGraphicsItem()
            self.addItem(self.decal)
            insertedPos = QtCore.QPointF(mouseEvent.scenePos().x() - self.decal.boundingRect().width()/2, mouseEvent.scenePos().y() - self.decal.boundingRect().height()/2)
            self.setMode(self.moveDecal)
        super(DecalScene, self).mousePressEvent(mouseEvent)
        
    def mouseMoveEvent(self, mouseEvent):
        if self.myMode == self.moveDecal:
            if self.decal.isSelected() and mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.decalMoved.emit(self.cursorPos)    
            super(DecalScene, self).mouseMoveEvent(mouseEvent)
            self.cursorPos = QtCore.QPointF(self.decal.posCustom())
            
    def mouseReleaseEvent(self, mouseEvent):
        super(DecalScene, self).mouseReleaseEvent(mouseEvent)
        
    def wheelEvent(self, event):
        self.decal.scaleFactor += event.delta() / 1800.00
        if self.decal.scaleFactor < 0.1: 
            self.decal.scaleFactor = 0.1
        if self.decal.scaleFactor > 2:
            self.decal.scaleFactor = 2
        self.decal.setScale(self.decal.scaleFactor)
        self.decalScaled.emit(self.decal.boundingRectCustom().height()/550)
    
class DecalsForm(form_class,base_class):
    def __init__(self, backgroundImage, decalImage, parent = getMayaWindow()):
        super(DecalsForm,self).__init__(parent)
        self.setObjectName('ProjectUIWindow')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        self.scene = DecalScene(backgroundImage, decalImage)
        self.graphicsView.setScene(self.scene)
        
        self.scene.decalMoved.connect(self.setValueSlider)
        self.scene.decalScaled.connect(self.setScaleDecal)
        
        self.hSlider.valueChanged.connect(self.updateDecalPos)
        self.vSlider.valueChanged.connect(self.updateDecalPos)
        
        self.spbScale.valueChanged.connect(self.updateDecalScale)
        
        self.rdbHStrip.clicked.connect(self.changeTexture)
        self.rdbVStrip.clicked.connect(self.changeTexture)
        self.rdbDecal.clicked.connect(self.changeTexture)
        
        self.graphicsView.show()
        self.startup()
        
    def startup(self):
        if cmds.objExists('body_paint'):
            cmds.setAttr('body_paint.Scale', 1/(self.scene.originRatio))
    
    def setValueSlider(self, QPointF):
        self.vSlider.setValue(QPointF.y()/550.0 * 100)
        self.hSlider.setValue(QPointF.x()/550.0 * 100)
        w = self.scene.decal.boundingRectCustom().width()
        h = self.scene.decal.boundingRectCustom().height()
        #------ work with my shader
        uValue = (self.hSlider.value() - w / 11.0)/(100 - 2 * w / 11.0) *100
        vValue = (self.vSlider.value() - h / 11.0)/(100 - 2 * h / 11.0) *100
        #--------------------------------------------------------------------
        #uValue = self.hSlider.value()
        #uValue = self.hSlider.value()
        
        cmds.setAttr('body_paint.Move_U', uValue/100.0)
        cmds.setAttr('body_paint.Move_V', 1 - vValue/100.0)

    def setScaleDecal(self, factor):
        cmds.setAttr('body_paint.Scale', factor)
        self.spbScale.setValue(factor)
        
    def updateDecalPos(self):
        self.scene.decal.setSignalPos(self.hSlider.value(), self.vSlider.value())
        w = self.scene.decal.boundingRectCustom().width()
        h = self.scene.decal.boundingRectCustom().height()
        #------ work with my shader
        uValue = (self.hSlider.value() - w / 11.0)/(100 - 2 * w / 11.0) *100
        vValue = (self.vSlider.value() - h / 11.0)/(100 - 2 * h / 11.0) *100
        #--------------------------------------------------------------------
        #uValue = self.hSlider.value()
        #uValue = self.hSlider.value()
        
        if self.rdbDecal.isChecked():
            cmds.setAttr('body_paint.Move_U', uValue/100.0) # change shader's name and shader properties's name
            cmds.setAttr('body_paint.Move_V', 1 - vValue/100.0) # change shader's name and shader properties's name
            
        if self.rdbHStrip.isChecked():
            
           # -----------------------------do something
           # ---------------------------------------------------------------------------
           pass # please remove pass after write your code
           
        if self.rdbVStrip.isChecked():
            
           # -----------------------------do something
           # ---------------------------------------------------------------------------
           pass # please remove pass after write your code
        
    def updateDecalScale(self):
        sValue = self.spbScale.value()
        cmds.setAttr('body_paint.Scale', sValue)
        sFactor = sValue * 550.00/self.scene.decal.boundingRect().width()
        self.scene.decal.setScale(sFactor)
        
    def changeTexture(self):
        if self.rdbDecal.isChecked():
           self.scene.setMode(self.scene.insertDecal)
           
           # -----------------------------do something
           # --------------------------------------------------------------------------
           
        if self.rdbHStrip.isChecked():
            self.scene.removeItem(self.scene.decal)
          
           # -----------------------------do something
           # ---------------------------------------------------------------------------

        if self.rdbVStrip.isChecked():
            self.scene.removeItem(self.scene.decal)
           
           # -----------------------------do something
           # ---------------------------------------------------------------------------

           

form = DecalsForm(bgPath, logoPath)
form.show()
        