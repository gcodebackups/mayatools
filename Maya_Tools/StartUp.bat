@echo off

CHOICE /N /C CDEFGHIJKLMNOPQRSTUVWXYZ /M "Enter drive letter of MAYA Installation: "

IF %ERRORLEVEL%==1 set DRIVE=C
IF %ERRORLEVEL%==2 set DRIVE=D
IF %ERRORLEVEL%==3 set DRIVE=E
IF %ERRORLEVEL%==4 set DRIVE=F
IF %ERRORLEVEL%==5 set DRIVE=G
IF %ERRORLEVEL%==6 set DRIVE=H
IF %ERRORLEVEL%==7 set DRIVE=I
IF %ERRORLEVEL%==8 set DRIVE=J
IF %ERRORLEVEL%==9 set DRIVE=K
IF %ERRORLEVEL%==10 set DRIVE=L
IF %ERRORLEVEL%==11 set DRIVE=M
IF %ERRORLEVEL%==12 set DRIVE=N
IF %ERRORLEVEL%==13 set DRIVE=O
IF %ERRORLEVEL%==14 set DRIVE=P
IF %ERRORLEVEL%==15 set DRIVE=Q
IF %ERRORLEVEL%==16 set DRIVE=R
IF %ERRORLEVEL%==17 set DRIVE=S
IF %ERRORLEVEL%==18 set DRIVE=T
IF %ERRORLEVEL%==19 set DRIVE=U
IF %ERRORLEVEL%==20 set DRIVE=V
IF %ERRORLEVEL%==21 set DRIVE=W
IF %ERRORLEVEL%==22 set DRIVE=X
IF %ERRORLEVEL%==23 set DRIVE=Y
IF %ERRORLEVEL%==24 set DRIVE=Z

ECHO 1: press 1 if you would like to run with Maya 2011
ECHO 2: press 2 if you would like to run with Maya 2012
ECHO 3: press 3 if you would like to run with Maya 2013
ECHO 4: press 4 if you would like to run with Maya 2014


CHOICE /N /C 12345 /M "Enter Maya version:"
IF %ERRORLEVEL% == 1 SET MAYAVERSION=2011
IF %ERRORLEVEL% == 2 SET MAYAVERSION=2012
IF %ERRORLEVEL% == 3 SET MAYAVERSION=2013.5
IF %ERRORLEVEL% == 4 SET MAYAVERSION=2014
IF %ERRORLEVEL% == 5 SET MAYAVERSION=2015

REM #### Set up paths for Maya working properly ### 
REM #### Get This script path

SET COMMONPATH=%~dp0

SET PROJECT_DIR=%COMMONPATH%Developer\Project\
 
REM ### Set Python path
SET PYTHONPATH=%COMMONPATH%MAYA_%MAYAVERSION%\;%COMMONPATH%Developer\Main;%COMMONPATH%_Common;%PYTHONPATH%

REM ### Set Plugin path
SET MAYA_PLUG_IN_PATH=%COMMONPATH%Developer\Main\MODULE\CustomNode;%MAYA_PLUG_IN_PATH%

REM ### Set Script path
SET MAYA_SCRIPT_PATH=%COMMONPATH%Developer\Main\MODULE\PolyTools\mel;%COMMONPATH%Developer\Main\MODULE\CrydevTools\mel;%COMMONPATH%Developer\Main\MODULE\CustomNode\AETemplates;%MAYA_SCRIPT_PATH%
SET XBMLANGPATH=%COMMONPATH%Developer\Main\MODULE\ThirdpartyTools\icons;%XBMLANGPATH%

REM ### Start Golaem startup file
CALL "E:\Program Files\Golaem\GolaemCrowd-3.1.0.1-Maya2014\bin\glmCrowdForMaya.bat"

set MAYA_LAUNCHER=%DRIVE%:\PROGRAM FILES\AUTODESK\maya%MAYAVERSION%
"%MAYA_LAUNCHER%\bin\maya.exe"
exit

