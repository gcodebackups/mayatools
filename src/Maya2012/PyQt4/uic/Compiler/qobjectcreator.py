#############################################################################
##
## Copyright (C) 2011 Riverbank Computing Limited.
## Copyright (C) 2006 Thorsten Marek.
## All right reserved.
##
## This file is part of PyQt.
##
## You may use this file under the terms of the GPL v2 or the revised BSD
## license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of the Riverbank Computing Limited nor the names
##     of its contributors may be used to endorse or promote products
##     derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
#############################################################################


import logging

from PyQt4.uic.Compiler.indenter import write_code
from PyQt4.uic.Compiler.qtproxies import QtGui, Literal, strict_getattr


try:
    set()
except NameError:
    from sets import Set as set



logger = logging.getLogger(__name__)
DEBUG = logger.debug


class _QtGuiWrapper(object):
    def search(clsname):
        try:
            return strict_getattr(QtGui, clsname)
        except AttributeError:
            return None

    search = staticmethod(search)


class _ModuleWrapper(object):
    def __init__(self, name, classes):
        if "." in name:
            idx = name.rfind(".")
            self._package = name[:idx]
            self._module = name[idx + 1:]
        else:
            self._package = None
            self._module = name
            
        self._classes = set(classes)
        self._used = False
    
    def search(self, cls):
        if cls in self._classes:
            self._used = True
            return type(cls, (QtGui.QWidget,), {"module": self._module})
        else:
            return None

    def _writeImportCode(self):
        if self._used:
            if self._package is None:
                write_code("import %s" % self._module)
            else:
                write_code("from %s import %s" % (self._package, self._module))


class _CustomWidgetLoader(object):
    def __init__(self):
        self._widgets = {}
        self._usedWidgets = set()
        
    def addCustomWidget(self, widgetClass, baseClass, module):
        assert widgetClass not in self._widgets 
        self._widgets[widgetClass] = (baseClass, module)


    def _resolveBaseclass(self, baseClass):
        try:
            for x in range(0, 10):
                try: return strict_getattr(QtGui, baseClass)
                except AttributeError: pass
                
                baseClass = self._widgets[baseClass][0]
            else:
                raise ValueError("baseclass resolve took too long, check custom widgets")

        except KeyError:
            raise ValueError("unknown baseclass %s" % baseClass)
        

    def search(self, cls):
        try:
            self._usedWidgets.add(cls)
            baseClass = self._resolveBaseclass(self._widgets[cls][0])
            DEBUG("resolved baseclass of %s: %s" % (cls, baseClass))
            
            return type(cls, (baseClass,),
                        {"module" : ""})
        
        except KeyError:
            return None

    def _writeImportCode(self):
        imports = {}
        for widget in self._usedWidgets:
            _, module = self._widgets[widget]
            imports.setdefault(module, []).append(widget)

        for module, classes in imports.items():
            write_code("from %s import %s" % (module, ", ".join(classes)))


class CompilerCreatorPolicy(object):
    def __init__(self):
        self._modules = []
        
    def createQtGuiWrapper(self):
        return _QtGuiWrapper

    def createModuleWrapper(self, name, classes):
        mw = _ModuleWrapper(name, classes)
        self._modules.append(mw)
        return mw

    def createCustomWidgetLoader(self):
        cw = _CustomWidgetLoader()
        self._modules.append(cw)
        return cw

    def instantiate(self, clsObject, objectname, ctor_args, is_attribute=True, no_instantiation=False):
        return clsObject(objectname, is_attribute, ctor_args, no_instantiation)

    def invoke(self, rname, method, args):
        return method(rname, *args)

    def getSlot(self, object, slotname):
        return Literal("%s.%s" % (object, slotname))

    def _writeOutImports(self):
        for module in self._modules:
            module._writeImportCode()
