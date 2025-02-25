import maya.cmds as cmds
import maya.mel as mel
import pymel.core as py
import re

from PyQt4 import QtGui, QtCore, uic
import os, sys, inspect
import functools 

LODsChain = ['_LOD0_','_LOD1_','_LOD2_','_LOD3_','_LOD4_','_LOD5_','_LOD6_']
# SONY Lods:
Sony_mapping_LODs = ['_LOD0_','_LOD1_','_LOD2_','_LOD3_','_LOD4_','_LOD5_','_LOD6_']
Sony_nohide = []
# IronMonkey Lods:
IronMonkey_mapping_LODs = ['lod_00_layer', 'lod_01_layer', 'lod_02_layer', 'lod_03_layer', 'lod_04_layer', 'lod_05_layer', 'lod_06_layer']
IronMonkey_nohide = ['base_car_layer','spoilers','exhausts', 'hoods']

lods = ['lod_00','lod_01','lod_02','lod_03','lod_04','lod_05','lod_06']
parts = ['type_a','type_b','type_c','type_d','kit_y','kit_z', 'kit_x', 'pulled_type_a','pulled_type_b', 'pulled_type_c', 'pulled_type_d',
         'large_type_a', 'large_type_b', 'large_type_c', 'large_type_d',
         'small_type_a','small_type_b', 'small_type_c', 'small_type_d']#,'pull_wheelarch','large_overfender','small_overfender']

fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0]
dirUI= fileDirCommmon +'/UI/IronMonkeyLODTools.ui'

form_class, base_class = uic.loadUiType(dirUI)        

def mappingLODs(projectName, lod):
    try:
        return globals()[projectName + '_mapping_LODs'][LODsChain.index(lod)]
    except:
        return False # cannot find matched imte with lod
    
def setupLOD():
        #----- remove current layers. An setup correct structures
        layers = cmds.ls(type = 'displayLayer')
        cmds.delete(layers)
        
        #----- create structure layers. --------------------------------------------------
        cmds.createDisplayLayer(n = 'decal_placement_layer')
        cmds.createDisplayLayer(n = 'locator_layer')
        cmds.createDisplayLayer(n = 'collision_layer')
        cmds.createDisplayLayer(n = 'wheel_placeholder_layer')
        cmds.createDisplayLayer(n = 'base_car_layer')
        cmds.createDisplayLayer(n = 'pulled_wheel_arch_layer')
        cmds.createDisplayLayer(n = 'small_overfenders_layer')
        cmds.createDisplayLayer(n = 'large_overfenders_layer')
        cmds.createDisplayLayer(n = 'base_unwrap_layer')
        cmds.createDisplayLayer(n = 'spoilers')
        cmds.createDisplayLayer(n = 'exhausts')
        cmds.createDisplayLayer(n = 'hoods')
        for part in parts:
            try:
                py.select('*' + part + '*')
                cmds.createDisplayLayer(e = False, n = part + '_layer')
            except:
                pass
        for lod in lods:
            try: 
                py.select('*' + lod + '*')
                cmds.createDisplayLayer(e = False, n = lod + '_layer')
            except:
                pass

        # adding wheelarch standard to type a
        #cmds.editDisplayLayerMembers('type_a_layer', cmds.ls('wheel_arch|standard'), noRecurse = True)
        # select all locator and put them in 
        try:
            cmds.editDisplayLayerMembers('locator_layer', cmds.ls(type = 'locator'), noRecurse = True)
        except:
            pass
        # select wheel place holder and put them in
        try:
            cmds.editDisplayLayerMembers('wheel_placeholder_layer', cmds.ls('*placeholder*'), noRecurse = True)
        except:
            pass
        # select decal placeholder and put them in
        # cmds.editDisplayLayerMembers('decal_placement_layer', [x for x in cmds.ls('*decal_*') if x not in cmds.ls(materials = True)], noRecurse = True)
        # select decal placeholder and put them in
        try:
            cmds.editDisplayLayerMembers('base_unwrap_layer', cmds.ls('*base_unwrap*'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.editDisplayLayerMembers('decal_placement_layer', cmds.ls('mesh_decal_placement_shell'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.editDisplayLayerMembers('collision_layer', cmds.ls('mesh_collider_roof','mesh_collider_rain','mesh_collider_chassis'), noRecurse = True)
        except:
            pass
        # select lod00 and add them to layer
        try:
            cmds.editDisplayLayerMembers('lod_00_layer', cmds.ls('lod_00'), noRecurse = True)
        except:
            pass
        # select lod01 and add them to layer
        try:
            cmds.editDisplayLayerMembers('lod_01_layer', cmds.ls('lod_01'), noRecurse = True)
        except:
            pass
        # select lod02 and add them to layer
        try:
            cmds.editDisplayLayerMembers('lod_02_layer', cmds.ls('lod_02'), noRecurse = True)
        except:
            pass   
        # select lod03 and add them to layer
        try:
            cmds.editDisplayLayerMembers('lod_03_layer', cmds.ls('lod_03'), noRecurse = True)
        except:
            pass
        # select lod04 and add them to layer
        try:
            cmds.editDisplayLayerMembers('lod_04_layer', cmds.ls('lod_04'), noRecurse = True)
        except:
            pass
        # select lod05 and add them to layer
        try:
            cmds.editDisplayLayerMembers('lod_05_layer', cmds.ls('lod_05'), noRecurse = True)
        except:
            pass
        # select lod06 and add them to layer
        try:
            cmds.editDisplayLayerMembers('lod_06_layer', cmds.ls('lod_06'), noRecurse = True)
        except:
            pass
        # select base car and add them to layer
        try:
            cmds.editDisplayLayerMembers('base_car_layer', cmds.ls('rotor|type_a','caliper|type_a','chassis|type_a','body|type_a','interior|type_a','windows|type_a','headlights|type_a','taillights|type_a','wheel_arch|standard'), noRecurse = True)
        except:
            pass
        # select pull wheel arch
        try:
            cmds.editDisplayLayerMembers('pulled_wheel_arch_layer', cmds.ls('pulled'), noRecurse = True)
        except:
            pass
        # select small over fender
        try:
            cmds.editDisplayLayerMembers('small_overfenders_layer', cmds.ls('small'), noRecurse = True)
        except:
            pass
        # select large over fender
        try:
            cmds.editDisplayLayerMembers('large_overfenders_layer', cmds.ls('large'), noRecurse = True)
        except:
            pass
        # select misc meshes
        try:
            cmds.editDisplayLayerMembers('base_unwrap', cmds.ls('base_unwrap'), noRecurse = True)
        except:
            pass
        # add spoilers to layers
        try:
            cmds.editDisplayLayerMembers('spoilers', cmds.ls('spoiler|*'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.editDisplayLayerMembers('exhausts', cmds.ls('exhaust|*'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.editDisplayLayerMembers('hoods', cmds.ls('hood|*'), noRecurse = True)
        except:
            pass


class CustomLODTools(form_class,base_class):
    def __init__(self):
        super(base_class,self).__init__()
        self.setupUi(self)
        self.__name__ = 'LOD Tools'
        self._projectName = 'IronMonkey'
        self._nohide = list()
        self._currentPart = ''
        self.btnSetupLOD.clicked.connect(self.check)
        self.btnSwitchLOD.clicked.connect(self.SwapLOD)
        self.btnCleanUp.clicked.connect(self.CleanUp)
        self.btnSpreadHonrizonal.clicked.connect(self.setPosition)
        self.btnSpreadVertical.clicked.connect(self.setPosition)
        self.btnPreviousLOD.clicked.connect(functools.partial(self.moveToNeighborLOD,'previous'))
        self.btnNextLOD.clicked.connect(functools.partial(self.moveToNeighborLOD,'next'))
        self.spnValue.valueChanged.connect(self.setPosition)
        self.btnLOD0.clicked.connect(functools.partial(self.selectLOD,'0'))
        self.btnLOD1.clicked.connect(functools.partial(self.selectLOD,'1'))
        self.btnLOD2.clicked.connect(functools.partial(self.selectLOD,'2'))
        self.btnLOD3.clicked.connect(functools.partial(self.selectLOD,'3'))
        self.btnTypeX.clicked.connect(functools.partial(self.selectLOD,'x'))
        self.btnTypeY.clicked.connect(functools.partial(self.selectLOD,'y'))
        self.btnTypeZ.clicked.connect(functools.partial(self.selectLOD,'z'))
        self.btnPulled.clicked.connect(functools.partial(self.selectLOD,'pulled'))
        self.btnSmall.clicked.connect(functools.partial(self.selectLOD,'small'))
        self.btnLarge.clicked.connect(functools.partial(self.selectLOD,'large'))
        self.chkSpoiler.clicked.connect(self.loadSpoilerTypeA)
        #self.btnLOD6.clicked.connect(functools.partial(self.selectLOD,'6'))
        #self.btnLOD7.clicked.connect(functools.partial(self.selectLOD,'7'))
        #self.btnLOD8.clicked.connect(functools.partial(self.selectLOD,'8'))
        self.btnStandard.clicked.connect(functools.partial(self.selectLOD,'6'))
  
        self.cbbSpoilers.currentIndexChanged.connect(self.showSpoilers)
        self.cbbExhausted.currentIndexChanged.connect(self.showExhausted)
        self.cbbHood.currentIndexChanged.connect(self.showHood)
        
        self.btnLOD0.setChecked(True)
        self.btnStandard.setChecked(True)


    def UnParent(self):
        transformEvo = [x for x in cmds.ls(dag = True) if cmds.nodeType(cmds.pickWalk(x,d = 'down')) == 'evoAttributeNode']
        try:
            cmds.delete(transformEvo)
        except:
            pass
        transformMayaNode = cmds.ls(transforms = True)
        for node in transformMayaNode: 
            try:
                cmds.parent(node, world = True)
            except:
                pass
        
    def CleanUp(self):
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in ['defaultLayer']]
        try:
            cmds.delete(displayLayerNotWork)
            cmds.delete('LayerSetup')
        except:
            pass
        self.btnCleanUp.setEnabled(False)
        self.btnSpreadHonrizonal.setEnabled(False)
        self.btnSpreadVertical.setEnabled(False)
        self.btnPreviousLOD.setEnabled(False)
        self.btnNextLOD.setEnabled(False)
        
        try:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', 0)
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', 0)  
                #cmds.delete(LODsChain[index].lstrip('_').rstrip('_'))
        except:
            pass
        self.UnParent()
        
    def check(self):
        self.cbbSpoilers.clear()
        self.cbbExhausted.clear()
        self.cbbHood.clear()
        if self._projectName == 'IronMonkey':
            setupLOD()
            childrenOfSpoilers = cmds.listRelatives('spoiler', c = True)
            childrenOfSpoilers.append('---Nothing---')
            childrenOfExhaust = cmds.listRelatives('exhaust', c = True)
            childrenOfExhaust.append('---Nothing---')
            childrenOfHood = cmds.listRelatives('hood', c = True)
            childrenOfHood.append('---Nothing---')
            
            self.cbbSpoilers.addItems(childrenOfSpoilers)
            self.cbbExhausted.addItems(childrenOfExhaust)
            self.cbbHood.addItems(childrenOfHood)
        else:
            if not cmds.objExists('LayerSetup'):
                self.createLOD()
                
    def showSpoilers(self):
        spoiler = self.cbbSpoilers.currentText()
        for s in cmds.listRelatives('spoiler', c = True, f= True):
            print s
            if spoiler == '---Nothing---':
                cmds.setAttr(s + '.visibility', 0)
            else:
                if str(spoiler) in s:
                    cmds.setAttr(s + '.visibility', 1)
                    if self.chkSpoiler.isChecked():
                        cmds.setAttr('spoiler|type_a.visibility', 1)
                else:
                    cmds.setAttr(s + '.visibility', 0)
                
    def showExhausted(self):
        exhaust = self.cbbExhausted.currentText()
        for s in cmds.listRelatives('exhaust', c = True, f= True):
            if exhaust == '---Nothing---':
                cmds.setAttr(s + '.visibility', 0)
            else:
                if str(exhaust) in s:
                    cmds.setAttr(s + '.visibility', 1)
                else:
                    cmds.setAttr(s + '.visibility', 0)
                    
    def showHood(self):
        hood = self.cbbHood.currentText()
        for s in cmds.listRelatives('hood', c = True, f= True):
            if hood == '---Nothing---':
                cmds.setAttr(s + '.visibility', 0)
            else:
                if str(hood) in s:
                    cmds.setAttr(s + '.visibility', 1)
                else:
                    cmds.setAttr(s + '.visibility', 0)
        
    def createLOD(self):
        # --
        cmds.createNode('test')
        cmds.rename('unknown1', 'LayerSetup')
        self.btnCleanUp.setEnabled(True)
        self.btnSpreadHonrizonal.setEnabled(True)
        self.btnSpreadVertical.setEnabled(True)
        self.btnNextLOD.setEnabled(True)
        self.btnPreviousLOD.setEnabled(True)
        
        #-- create LOD1 Layer
        try:
            cmds.select('*LOD1*')
            cmds.group(n = 'LOD1')
            cmds.createDisplayLayer(n = '_LOD1_')
            cmds.editDisplayLayerMembers('_LOD1_', cmds.ls(type = 'LOD1'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD2*')
            cmds.group(n = 'LOD2')
            cmds.createDisplayLayer(n = '_LOD2_')
            cmds.editDisplayLayerMembers('_LOD2_', cmds.ls(type = 'LOD2'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD3*')
            cmds.group(n = 'LOD3')
            cmds.createDisplayLayer(n = '_LOD3_')
            cmds.editDisplayLayerMembers('_LOD3_', cmds.ls(type = 'LOD3'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD4*')
            cmds.group(n = 'LOD4')
            cmds.createDisplayLayer(n = '_LOD4_')
            cmds.editDisplayLayerMembers('_LOD4_', cmds.ls(type = 'LOD4'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*LOD5')
            cmds.group(n = 'LOD5')
            cmds.createDisplayLayer(n = '_LOD5_')
            cmds.editDisplayLayerMembers('_LOD5_', cmds.ls(type = 'LOD5'), noRecurse = True)
        except: 
            pass
        
        try:
            cmds.select('*LOD6')
            cmds.group(n = 'LOD6')
            cmds.createDisplayLayer(n = '_LOD6_')
            cmds.editDisplayLayerMembers('_LOD6_', cmds.ls(type = 'LOD6'), noRecurse = True)
        except:
            pass
        
        try:
            cmds.select('*SHADOW')
            cmds.group(n = 'SHADOW')
            cmds.createDisplayLayer(n = '_SHADOW_')
            cmds.editDisplayLayerMembers('_SHADOW_', cmds.ls(type = 'SHADOW'), noRecurse = True)
        except:
            pass
        
        try:
            patternLOD = re.compile(r'(.*)LOD(\.*)',re.I)
            patternSHADOW = re.compile(r'(.*)SHADOW(\.*)',re.I)
            LOD0s = [x for x in cmds.ls(transforms = True) if not re.search(patternLOD,x) and not re.search(patternSHADOW,x) ]
            cmds.select(LOD0s)
            cmds.group(n = 'LOD0')
            cmds.createDisplayLayer(n = '_LOD0_', nr = False)
            cmds.editDisplayLayerMembers('_LOD0_', cmds.ls(type = 'LOD0'), noRecurse = True)
        except:
            pass
        
        cmds.showHidden(all = True)
        
    def SwapLOD(self):
        cmds.undoInfo(openChunk = True)
        if self._projectName == 'IronMonkey':
            self.SwapLODIronMonkey()
        if self._projectName == 'Sony':
            self.SwapLODSony()
        cmds.undoInfo(closeChunk = True)
        
    def SwapLODIronMonkey(self):
 
            #if layer not in self._nohide]
        if self._projectName == 'IronMonkey':
            mel.eval('showHidden -all;')        
        self._nohide = ['base_car_layer', 'spoilers','exhausts', 'hoods']
        
        if self.rdbSourceLOD0.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD0_')
        elif self.rdbSourceLOD1.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD1_')
        elif self.rdbSourceLOD2.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD2_')
        elif self.rdbSourceLOD3.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD3_')
        elif self.rdbSourceLOD4.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD4_')
        elif self.rdbSourceLOD5.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD5_')
        elif self.rdbSourceLOD6.isChecked():
            LODa = mappingLODs(self._projectName,'_LOD6_')
        elif self.rdbSourceSHADOW.isChecked():
            LODa = mappingLODs(self._projectName,'_SHADOW_')
            
        if self.rdbTargetLOD0.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD0_')
        elif self.rdbTargetLOD1.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD1_')
        elif self.rdbTargetLOD2.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD2_')
        elif self.rdbTargetLOD3.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD3_')
        elif self.rdbTargetLOD4.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD4_')
        elif self.rdbTargetLOD5.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD5_')
        elif self.rdbTargetLOD6.isChecked():
            LODb = mappingLODs(self._projectName,'_LOD6_')
        elif self.rdbTargetSHADOW.isChecked():
            LODb = mappingLODs(self._projectName,'_SHADOW_')
        # ------------------------------------------------
        type_a = list()
        if not self.btnLOD0.isChecked():
            cmds.setAttr('type_a_layer.visibility', 1)
            if self.chkBumper_front.isChecked():
                if 'type_a_layer' not in self._nohide:
                    self._nohide.append('type_a_layer')
                if self.btnStandard.isChecked():
                    type_a.append('bumper_front|standard_type_a')
                if self.btnPulled.isChecked():
                    if cmds.objExists('bumper_front|pulled_type_a'):
                        type_a.append('bumper_front|pulled_type_a')
                    else:
                        type_a.append('bumper_front|standard_type_a')
                if self.btnLarge.isChecked():
                    if cmds.objExists('bumper_front|large_type_a'):
                        type_a.append('bumper_front|large_type_a')
                    else:
                        type_a.append('bumper_front|large_type_a')
                        
                if self.btnSmall.isChecked():

            if self.chkBumper_rear.isChecked():
                if 'type_a_layer' not in self._nohide:
                    self._nohide.append('type_a_layer')
                if self.btnStandard.isChecked():
                    type_a.append('bumper_rear|standard_type_a')
                if self.btnPulled.isChecked():
                    if cmds.objExists('bumper_rear|pulled_type_a'):
                        type_a.append('bumper_rear|pulled_type_a')
                    else:
                        type_a.append('bumper_rear|standard_type_a')
                if self.btnLarge.isChecked():
                    if cmds.objExists('bumper_rear|large_type_a'):
                        type_a.append('bumper_rear|large_type_a')
                    else:
                        type_a.append('bumper_rear|large_type_a')

            if self.chkSide_skirt.isChecked():
                if 'type_a_layer' not in self._nohide:
                    self._nohide.append('type_a_layer')
                if self.btnStandard.isChecked():
                    type_a.append('side_skirts|standard_type_a')
                if self.btnPulled.isChecked():
                    if cmds.objExists('side_skirts|pulled_type_a'):
                        type_a.append('side_skirts|pulled_type_a')
                    else:
                        type_a.append('side_skirts|standard_type_a')
                if self.btnLarge.isChecked():
                    if cmds.objExists('side_skirts|large_type_a'):
                        type_a.append('side_skirts|large_type_a')
                    else:
                        type_a.append('side_skirts|large_type_a')

            groups = [group.split('.')[0] for group in cmds.connectionInfo('type_a_layer.drawInfo', dfs = True)]
            for g in groups:
                if g not in type_a:
                    try:
                        cmds.setAttr(g + '.visibility', 0)
                    except:
                        pass 
        else:
            type_a = cmds.ls('standard_type_a')
            for g in type_a:
                cmds.setAttr(g + '.visibility', 1)
                    
        if self.btnTypeX.isChecked() or self.btnTypeY.isChecked() or self.btnTypeZ.isChecked(): # kit Y and kit Z
            cmds.setAttr('wheel_arch.visibility', 1)
            try:
                cmds.setAttr('wheel_arch|standard.visibility', 0)
            except:
                pass
            try:
                cmds.setAttr('wheel_arch|pulled.visibility', 0)
            except:
                pass
            try:
                cmds.setAttr('wheel_arch|small.visibility', 0)
            except:
                pass
            try:
                cmds.setAttr('wheel_arch|large.visibility', 0)
            except:
                pass
        
        # ------------------------------------------------
        self._nohide.append(LODa)
        self._nohide.append(LODb)
        self._nohide.append('defaultLayer')
        self._nohide.append(self._currentPart)
        if self.btnPulled.isChecked():
            print 'pulled'
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            self._nohide.append('pulled_wheel_arch_layer') 
            if self.btnLOD0.isChecked(): # if type A is selected
                if cmds.objExists('pulled_type_a_layer'):
                    self._nohide.append('pulled_type_a_layer')
                    try:
                        cmds.setAttr('bumper_front|standard_type_a.visibility', 0)
                        cmds.setAttr('bumper_rear|standard_type_a.visibility', 0)
                        cmds.setAttr('side_skirts|standard_type_a.visibility', 0)
                    except:
                        pass
            if self.btnLOD1.isChecked(): # if type B is selected
                if cmds.objExists('pulled_type_b_layer'):
                    self._nohide.append('pulled_type_b_layer')
                    try:
                        cmds.setAttr('bumper_front|standard_type_b.visibility', 0)
                        cmds.setAttr('bumper_rear|standard_type_b.visibility', 0)
                        cmds.setAttr('side_skirts|standard_type_b.visibility', 0)
                    except:
                        pass
            if self.btnLOD2.isChecked(): # if type C is selected
                if cmds.objExists('pulled_type_c_layer'):
                    self._nohide.append('pulled_type_c_layer')
                    try:
                        cmds.setAttr('bumper_front|standard_type_c.visibility', 0)
                        cmds.setAttr('bumper_rear|standard_type_c.visibility', 0)
                        cmds.setAttr('side_skirts|standard_type_c.visibility', 0)
                    except:
                        pass
            if self.btnLOD3.isChecked(): # if type D is selected
                self._nohide.append('pulled_type_d_layer')
                try:
                    cmds.setAttr('bumper_front|standard_type_d.visibility', 0)
                    cmds.setAttr('bumper_rear|standard_type_d.visibility', 0)
                    cmds.setAttr('side_skirts|standard_type_d.visibility', 0)
                except:
                    pass
                
        if self.btnSmall.isChecked():
            print 'pulled'
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            self._nohide.append('small_overfenders_layer') 
                 
        if self.btnLarge.isChecked():
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            print 'large'
            self._nohide.append('large_overfenders_layer')
            if self.btnLOD0.isChecked():
                self._nohide.append('large_type_a_layer')
            if self.btnLOD1.isChecked():
                self._nohide.append('large_type_b_layer')
            if self.btnLOD2.isChecked():
                self._nohide.append('large_type_c_layer')
            if self.btnLOD3.isChecked():
                self._nohide.append('large_type_d_layer')
                
    
        print self._nohide      
        displayLayerNotWork = [layer for layer in cmds.ls(type = 'displayLayer') if layer not in self._nohide]

        for l in displayLayerNotWork:
            cmds.setAttr(l + '.visibility', 0)
            
        flag = cmds.getAttr(LODa + '.visibility')
        cmds.setAttr(LODa + '.visibility', not flag)
        cmds.setAttr(LODb + '.visibility', flag)
        
        self.showSpoilers()
        self.showExhausted()
        self.showHood()
        
       
    def setPosition(self):
        if not self.btnSpreadHonrizonal.isChecked():
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', 0)
        else:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateX', int(self.spnValue.value()) * index)
        if not self.btnSpreadVertical.isChecked():
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', 0)
        else:
            for index in range(len(LODsChain)):
                cmds.setAttr(LODsChain[index].lstrip('_').rstrip('_') + '.translateY', int(self.spnValue.value()) * index)
    
    def moveToNeighborLOD(self, direction):
        indexofCurrentLOD, indexofNeighborLOD = 0,0
        currentLODs = [lod for lod in cmds.ls(type = 'displayLayer') if cmds.getAttr(lod + '.visibility') == True and lod != 'defaultLayer']
        if len(currentLODs) > 1:
            for i in range(1, len(currentLODs)):
                cmds.setAttr(currentLODs[i] + '.visibility', False)
        elif len(currentLODs) == 0:
            currentLODs = ['LOD0']
        indexofCurrentLOD = LODsChain.index(currentLODs[0])
        
        if direction == 'next':
            if indexofCurrentLOD == len(LODsChain) - 1:
                indexofNeighborLOD = 0
            else:
                indexofNeighborLOD = indexofCurrentLOD + 1
            
        if direction == 'previous':
            if indexofCurrentLOD == 0:
                indexofNeighborLOD = len(LODsChain) - 1
            else:
                indexofNeighborLOD = indexofCurrentLOD - 1
                
        cmds.setAttr(LODsChain[indexofNeighborLOD] + '.visibility', True)
        cmds.setAttr(LODsChain[indexofCurrentLOD] + '.visibility', False)
        
    def selectLOD(self, lod):
        type_layer = cmds.ls('type_*_layer')
        if lod == '0':
            patternLOD = re.compile(r'(.*)LOD(\.*)',re.I)
            patternSHADOW = re.compile(r'(.*)SHADOW(\.*)',re.I)
            LOD0s = [x for x in cmds.ls(transforms = True) if not re.search(patternLOD,x) and not re.search(patternSHADOW,x) ]
            cmds.select(LOD0s)
            self._currentPart = 'type_a_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '1':
            try:
                cmds.select('*LOD1')
            except:
                pass
            self._currentPart = 'type_b_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            
        if lod == '2':
            try:
                cmds.select('*LOD2')
            except:
                pass
            self._currentPart = 'type_c_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == '3':
            try:
                cmds.select('*LOD3')
            except:
                pass
            self._currentPart = 'type_d_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
        if lod == 'x':
            try:
                cmds.select('*LOD4')
            except:
                pass
            self._currentPart = 'kit_x_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
        if lod == 'y':
            try:
                cmds.select('*LOD5')
            except:
                pass
            self._currentPart = 'kit_y_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
        if lod == 'z':
            try:
                cmds.select('*LOD6')
            except:
                pass
            self._currentPart = 'kit_z_layer'
            cmds.setAttr(self._currentPart + '.visibility', 1)
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            
        if lod == 'pulled':
            cmds.setAttr('wheel_arch|standard.visibility', 0)
            cmds.setAttr('pulled_wheel_arch_layer.visibility', 1)
            cmds.setAttr('large_overfenders_layer.visibility', 0)
            cmds.setAttr('small_overfenders_layer.visibility', 0)
            if self.btnLOD0.isChecked():
                cmds.setAttr('pulled_type_a_layer.visibility',1)
            if self.btnLOD1.isChecked():
                if cmds.objExists('pulled_type_b_layer'):
                    cmds.setAttr('pulled_type_b_layer.visibility',1)
                else:
                    cmds.setAttr('pulled_type_a_layer.visibility',1)
            if self.btnLOD2.isChecked():
                if cmds.objExists('pulled_type_c_layer'):
                    cmds.setAttr('pulled_type_c_layer.visibility',1)
                else:
                    cmds.setAttr('pulled_type_a_layer.visibility',1)
            if self.btnLOD3.isChecked():
                if cmds.objExists('pulled_type_d_layer'):
                    cmds.setAttr('pulled_type_d_layer.visibility',1)
                else:
                    cmds.setAttr('pulled_type_a_layer.visibility',1)
        
        if lod == 'small':
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            cmds.setAttr('pulled_wheel_arch_layer.visibility', 0)
            cmds.setAttr('large_overfenders_layer.visibility', 0)
            cmds.setAttr('small_overfenders_layer.visibility', 1)
            
        
        if lod == 'large':
            cmds.setAttr('wheel_arch|standard.visibility', 1)
            cmds.setAttr('pulled_wheel_arch_layer.visibility', 0)
            cmds.setAttr('large_overfenders_layer.visibility', 1)
            cmds.setAttr('small_overfenders_layer.visibility', 0)
            if self.btnLOD0.isChecked():
                cmds.setAttr('large_type_a_layer.visibility',1)
            if self.btnLOD1.isChecked():
                if cmds.objExists('large_type_b_layer'):
                    cmds.setAttr('large_type_b_layer.visibility',1)
                else:
                    cmds.setAttr('large_type_a_layer.visibility',1)
            if self.btnLOD2.isChecked():
                if cmds.objExists('large_type_c_layer'):
                    cmds.setAttr('large_type_c_layer.visibility',1)
                else:
                    cmds.setAttr('large_type_a_layer.visibility',1)
            if self.btnLOD3.isChecked():
                if cmds.objExists('large_type_d_layer'):
                    cmds.setAttr('large_type_d_layer.visibility',1)
                else:
                    cmds.setAttr('large_type_a_layer.visibility',1)
            
    def loadSpoilerTypeA(self):
        if self.chkSpoiler.isChecked():
            cmds.setAttr('spoiler|type_a.visibility', 1)
        else:
            cmds.setAttr('spoiler|type_a.visibility', 0)
            
def main():
    form = CustomLODTools()
    return form 
    
