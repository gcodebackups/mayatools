'''
Created on Jul 10, 2014
@author: trungtran
@email: trungswat@gmail.com
@description: ''
'''

import inspect, os, pkgutil
from PyQt4 import QtGui, QtCore
try:
    reload(cf)
except:
    from developer.main.common import commonFunctions as cf
    
try:
    reload(dW)
except:
    from developer.main.common.dockWidget import *

class QtSubWidget(DockWidget):
    def __init__(self, modName, modDir, modList):
        super(DockWidget, self).__init__(modName)
        self.titleBar = DockWidgetTitleBar(self)
        self.setTitleBarWidget(self.titleBar)
        # create some item to store widget
        self.vLayout = QtGui.QVBoxLayout()
        self.vLayout.setContentsMargins(0, 0, 0, 0)
        self.vLayout.setSpacing(0)
        self.widget = QtGui.QWidget()
        self.widget.setLayout(self.vLayout)
        self.setWidget(self.widget)
        # add widget
        for pkg_loader, pkg_name, is_pkg in pkgutil.walk_packages(os.path.split(modDir)):
            if is_pkg and pkg_name == 'widget':
                pkg = pkg_loader.find_module(pkg_name).load_module(pkg_name)
                for mod_loader, mod_name, is_mod in pkgutil.iter_modules(pkg.__path__):
                    if len(modList) == 0: # load all submodule in package
                        if not is_mod and mod_name != '__init__':
                            mod = mod_loader.find_module(mod_name).load_module(mod_name)
                            self.vLayout.addWidget(mod.QtWidget())
                    if not is_mod and mod_name in modList:
                        mod = mod_loader.find_module(mod_name).load_module(mod_name)
                        self.vLayout.addWidget(mod.QtWidget())
        #self.vLayout.addItem(self.vSpacer)
        #--
