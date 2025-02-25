import inspect, os, re
import maya.mel as mel
import maya.cmds as cmds
from xml.dom.minidom import *

description = 'Checking No Decal.'
name = 'checkNoDecal'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')


def execute():
    print 'EXECUTING: CHECKING NO DECAL----------------------------------'
    import re
    objectOrror = list()
    #meshes = cmds.ls(type = 'mesh')#.split('|')[0]
    all_transform = [f for f in cmds.listRelatives(cmds.ls('mesh')[0], ad = True,f=True) if cmds.nodeType(f) != 'mesh'] 
    allMesh = [tran for tran in all_transform if re.search('mesh_',tran)]#.split('|')[-1]
    mirror = [tran for tran in allMesh if re.search('_mirrors_',tran)]
    spoiler = [spoil for spoil in allMesh if re.search('_spoiler_',spoil)]
    mir_spoil = list(set(mirror + spoiler))
    listNo_mir_spoil = [tran for tran in allMesh if tran not in mir_spoil]
    
    print'################# CORRECT MATERIAL MIRRORS AND SPOILER ################################'
    for mes in mir_spoil:
        #print mes
        object=mes
        shapeNode = cmds.listRelatives(mes, c = True, f = True)[0]
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        shaders = list()
        #print sgs
        if not (sgs is None):
            for sg in sgs:
                if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                    shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                    if shader == 'paint_shader_nodecal_opaque':
                        print(shader,'Shaders corect assign')
                    else:
                        objectOrror.append(object)
                        #print(object,shader,'Error, shaders incorect assign')
        if sgs is None:
            print(shapeNode,', Error connection.')
            
    print'################# INCORRECT MATERIAL ################################'
        
    for mes in listNo_mir_spoil:
        object=mes.split('|')[-1]
        print 'Mes -------------'
        print mes
        shapeNode = cmds.listRelatives(mes, c = True, f = True)[0]
        print 'shape Node'
        print shapeNode
        sgs = cmds.listConnections(shapeNode, t = 'shadingEngine')
        shaders = list()
               
        if not (sgs is None):
            for sg in sgs:
                if cmds.connectionInfo(sg + '.surfaceShader', sfd = True):
                    shader = cmds.connectionInfo(sg + '.surfaceShader', sfd = True).split('.')[0]
                    if shader == 'paint_shader_nodecal_opaque':
                        objectOrror.append(mes)
                    #print(object,'Incorrect material',shader)
        if sgs is None:
            print(shapeNode,', Error connection.')
    #print objectOrror
    objectHide = [obj for obj in allMesh if obj not in objectOrror]
    if len(objectOrror)>0:
        print'####################### OBJECT ERROR ##########'
        for ob in objectOrror:
            #print ob
            cmds.setAttr(ob + '.visibility', 1)
    if len(objectHide)>0:
        print'#######################OBJECT HIDEN ##########'
        for obj in objectHide:
                 
            #print obj
            cmds.setAttr(obj + '.visibility', 0)    