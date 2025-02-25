import inspect, os
import maya.mel as mel
import maya.cmds as cmds

description = 'Select Exterior Tag node only'
name = 'selectTagNode'
fileDirCommmon = os.path.split(inspect.getfile(inspect.currentframe()))[0].replace('\\','/')

def execute():
    print '--------------- FCC-------------------------'
    tagNode = cmds.ls('BOOST_L1','BOOST_L2','BOOST_R1','BOOST_R2','BOOT','CHASSIS','HUB_BL','HUB_BR','HUB_FL'
                      ,'HUB_FR','HUB_BL','HUB_BR','HUB_FL','HUB_FR','LIGHT_BL','LIGHT_BR','LIGHT_FL','LIGHT_FR',
                      'LIGHT_LENS_FL','LIGHT_LENS_FR','SPOILER','WHEEL_BL'
                      ,'WHEEL_BR','WHEEL_FL','WHEEL_FR','WINDOW_BL','WINDOW_BR','BOOT')
    cmds.select(tagNode)