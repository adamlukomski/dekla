#!/usr/bin/env python3

'''   general sketch 24




'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import time
import datetime
import yaml
import socket
import csv
import random

import io # for StringIO, dummy file

# # this is moved inside CuteManager.runExperiment()
#with open('posner02.yaml','r') as file:
        #db = yaml.load(file,Loader=yaml.Loader)

app = QApplication([])

class defaults:
        appName = "Dekla v0.2 - Posner Experiment"
        screen1 = "Main"
        screen2 = "Left"
        screen3 = "Right"
        savefile = "../data/results_" # and %Y%m%d-%H%M%S

"""
conditions = [
  'close',
  'close',
  'mutual',
  'mutual',
  'mutual',
  'close',
  'close',
  'close',
  'mutual',
  'close',
  'mutual',
  'mutual',
  'mutual',
  'mutual',
  'close',
  'close']


subtrials = [ (lookingside,letterside,letter)
              for lookingside in ['left','right']
              for letterside  in ['left','right']
              for letter in [ 'T','V'] ]

trials = list()

for trial in conditions:
        subtrialsTwice = subtrials.copy()
        subtrialsTwice.extend(subtrials)
        random.shuffle(subtrialsTwice)
        for subtrial in subtrialsTwice:
                place1 = trial + ' ' + subtrial[0]
                place2 = subtrial[1] + ' ' + subtrial[2]
                place3 = 'return ' + subtrial[0]
                place4 = subtrial[1] + ' empty'
                key = subtrial[2]
                
                trials.append(  dict( place1=place1,
                                      place2=place2,
                                      place3=place3,
                                      place4=place4,
                                      key=key ) )
"""














#
#    //
#



class CuteLog:
        def __init__(self):
                self.initTime = time.time_ns()
                try:
                        self.sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.sock1.connect(('127.0.0.1', 50010))
                except OSError as msg:
                        self.sock1 = None
                        print("Please create a logger service if a time log is needed")
                
                
        def log(self,text):
                
                if self.sock1 != None:
                        self.sock1.sendall(text.encode('utf-8'))
                
        
#cuteLog = CuteLog()






#def movielist():
        #'''
        #placeholder for interactive loading of movies later on
        #'''
        #movies = dict()
        ## TODO check files existance before proceeding
        #movies['close left'] = 'movies/close left final0001-0105.mp4'
        #movies['mutual left'] = 'movies/mutual left final0001-0105.mp4'
        #movies['return left'] = 'movies/return left final0001-0065.mp4'

        #movies['close right'] = 'movies/close right final0001-0105.mp4'
        #movies['mutual right'] = 'movies/mutual right final0001-0105.mp4'
        #movies['return right'] = 'movies/return right final0066-0130.mp4'
        #return movies

class CuteVideo(QVideoWidget):
        def __init__(self, moviename):
                super().__init__()
                self.setMinimumSize(640,480)
                
                self.player = QMediaPlayer()
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(QFileInfo(moviename).absoluteFilePath())))
                #self.player.setPlaylist(moviename);
                self.player.setVideoOutput(self)
                #self.player.play()
                self.player.setNotifyInterval(2) # ms
                self.player.positionChanged.connect(self.periodicPause)
                #self.player.mediaStatusChanged.connect(self.statusCheck)
                
        stackedIndex = 0
        
        #def statusCheck(self,status):
                #if status == QMediaPlayer.EndOfMedia:
                        #print("Media ended")
                        #self.player.setPosition(self.player.duration()-10)
        
        def periodicPause(self,position):
                # will spit out errors:
                #  RecursionError: maximum recursion depth exceeded in comparison
                # if you use anything modifying playing position without checking State
                # do any modifications inside if statements only when paused!
                #print(position)
                if self.player.state() == QMediaPlayer.PlayingState:
                        #print(self.player.duration()-position)
                        if self.player.duration()>0:
                                if self.player.duration()-position<10:
                                        # first pause! always first pause!
                                        self.player.pause()
                                        if self.player.isSeekable():
                                                # correct it to be precisely 50ms before the end
                                                self.player.setPosition(self.player.duration()-10)

# do not add too much here, this is essentially a keypress forward class!
#  it makes it possible to have focus on any window and still activate functions from the main one
class CuteSideWindow(QWidget):
        def __init__(self,cuteMain):
                super().__init__()
                self.cuteMain = cuteMain
                self.setMinimumSize(640,480)
        stackedIndex = 0
        def keyPressEvent(self,event):
                # TODO add an if statement here and a manual tick option for overriding in setup
                self.cuteMain.keyPressEvent(event)

class CuteLabel(QLabel):
        stackedIndex = 0
        stack = '' # left, right, main

class CuteMain(QWidget):
        helpMessageBoxText = """
                        The windows will go fullscreen
                        on the screen where they are currently on
                        F5 - fullscreen and start
                        F9 - only start the experiment
                        F11 - fullscreen toggle
                        p - pause (semi working)
                        q or Escape - quit
                        """
        def __init__(self,db):
                super().__init__()
                self.db = db
                self.setMinimumSize(640,480)
                self.setWindowTitle(defaults.screen1)

                #movies = self.db['info']['movies']  # kyveli
 
                self.layoutStack = dict()
                self.layoutStack['main'] = QStackedLayout()
                self.players = dict()
                index = 0

                self.labels = dict()
               
                
                
                self.labels["instructions"] = CuteLabel(self.helpMessageBoxText)
                self.labels["instructions"].setFont( QFont( "Arial", 14, QFont.Bold) )
                self.labels["instructions"].setAlignment(Qt.AlignCenter)
                #self.labels["left T"].setStyleSheet("border: solid 10px grey;  background-color: rgba(255, 0, 0,127); color:rgb(0,255,0)");
                self.labels["instructions"].setStyleSheet("background-color: rgba(120, 120, 120,30)");
                
                self.layoutStack['main'].addWidget(self.labels['instructions'])
                index += 1
                
                #for movie in movies:
                        #print(index,movie)
                        #self.players[movie] = CuteVideo(movies[movie])
                        #self.players[movie].player.setPosition(0)
                        #self.layoutStack['main'].addWidget(self.players[movie])
                        ## do this automatically next time: (not reliable)
                        #self.players[movie].stackedIndex = index
                        ## maybe one more dictionary that stores indices?
                        #index = index + 1
                        
                self.layoutStack['main'].setContentsMargins(0,0,0,0)
                self.layoutStack['main'].setCurrentIndex(0)
                
                self.setLayout(self.layoutStack['main'])
                
                # main done
                
                #print("LEFT")
                #self.left = CuteSideWindow(self)
                #self.left.setWindowTitle(defaults.screen2)
                #self.left.setWindowTitle('Left')
                #self.layoutStack['left'] = QStackedLayout()
                #self.labels["left V"] = CuteLabel("V")
                ##self.labels["left V"].setFont( QFont( "Arial", 100, QFont.Bold) )
                #self.labels["left V"].setStyleSheet( 'font: bold 100px'  )
                #self.labels["left V"].setAlignment(Qt.AlignCenter)
                #self.labels["left T"] = CuteLabel("T")
                #self.labels["left T"].setFont( QFont( "Arial", 100, QFont.Bold) )
                #self.labels["left T"].setAlignment(Qt.AlignCenter)
                ##self.labels["left T"].setStyleSheet("border: solid 10px grey;  background-color: rgba(255, 0, 0,127); color:rgb(0,255,0)");
                #self.labels["left empty"] = CuteLabel() # QWidget? 
                #self.layoutStack['left'].addWidget(self.labels["left empty"])  # 0
                #self.layoutStack['left'].addWidget(self.labels["left V"]) # 1
                #self.layoutStack['left'].addWidget(self.labels["left T"]) # 2
                ##this should be automatic:
                #self.labels["left empty"].stackedIndex = 0
                #self.labels["left V"].stackedIndex = 1
                #self.labels["left T"].stackedIndex = 2
                #self.left.setLayout(self.layoutStack['left'])
                #self.left.show()

                #self.labels["left empty"].stack = 'left'
                #self.labels["left V"].stack = 'left'
                #self.labels["left T"].stack = 'left'

                
                #print("RIGHT")
                #self.right = CuteSideWindow(self)
                #self.right.setWindowTitle('Right')
                #self.right.setWindowTitle(defaults.screen3)
                #self.layoutStack['right'] = QStackedLayout()
                #self.labels["right V"] = CuteLabel("V")
                #self.labels["right V"].setFont( QFont( "Arial", 100, QFont.Bold) )
                #self.labels["right V"].setAlignment(Qt.AlignCenter)
                #self.labels["right T"] = CuteLabel("T")
                #self.labels["right T"].setFont( QFont( "Arial", 100, QFont.Bold) )
                #self.labels["right T"].setAlignment(Qt.AlignCenter)
                #self.labels["right empty"] = CuteLabel() # QWidget? 
                #self.layoutStack['right'].addWidget(self.labels["right empty"])  # 0
                #self.layoutStack['right'].addWidget(self.labels["right V"]) # 1
                #self.layoutStack['right'].addWidget(self.labels["right T"]) # 2
                ##this should be automatic:
                #self.labels["right empty"].stackedIndex = 0
                #self.labels["right V"].stackedIndex = 1
                #self.labels["right T"].stackedIndex = 2
                
                #self.labels["right empty"].stack = 'right'
                #self.labels["right V"].stack = 'right'
                #self.labels["right T"].stack = 'right'
                
                #print("layout")
                #self.right.setLayout(self.layoutStack['right'])
                #self.right.show()
                
                
                print("save")
                self.filenameResults, extension = QFileDialog.getSaveFileName( self, "Save results as...", defaults.savefile+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.csv')

                #msgBox = QMessageBox()
                #msgBox.setText(self.helpMessageBoxText)
                #msgBox.exec()

        def full(self):
                if not self.windowState() == Qt.WindowFullScreen:
                        self.setWindowState(Qt.WindowFullScreen)
                        self.left.setWindowState(Qt.WindowFullScreen)
                        self.right.setWindowState(Qt.WindowFullScreen)
                else:
                        self.setWindowState(Qt.WindowNoState)
                        self.left.setWindowState(Qt.WindowNoState)
                        self.right.setWindowState(Qt.WindowNoState)
                        

        def keyPressEvent(self,event):
                #if event.key() in list_all_keys:
                        # list_all_keys is a dict, {Qt.Key_T: 'event_name'}
                        # 'event_name' allows a transition
                        # or directly change the transition state here?
                        #  and pop it from the list_all_keys right away?

                # see: snippet_090_key_stack.py !


                print( event.key() )
                if event.key() == Qt.Key_F11:
                        self.full()
                if event.key() == Qt.Key_Q or event.key() == Qt.Key_Escape:
                        if self.layoutStack['main'].currentIndex() != 0:
                                self.pauseExperiment()
                                self.labels['instructions'].setText('trials left: '+str(self.trialsLeft())+'\n press q to quit' )
                                self.layoutStack['main'].setCurrentIndex(0)
                        else:
                                self.finishedExperiment.emit()
                
                if event.key() == Qt.Key_F9:
                        self.startExperiment()
                        #self.players['close left'].player.play()
                        #self.player1.player.play()
                        print("Sent play")
                if event.key() == Qt.Key_F5:
                        if not self.windowState() == Qt.WindowFullScreen:
                                self.full()
                        self.startExperiment()
                if event.key() == Qt.Key_R:
                        #self.player.player.setPosition(0)
                        #self.player1.player.setPosition(0)
                        print("Sent reset")
                if event.key() == Qt.Key_P:
                        self.pauseExperiment()
                        #self.player.player.pause()
                        print("Sent pause")
                        #print(self.playlist.errorString())
                if event.key() == Qt.Key_T:
                        self.correctInput = 'T'
                if event.key() == Qt.Key_V:
                        self.correctInput = 'V'
                if event.key() == Qt.Key_F1:
                        msgBox = QMessageBox()
                        msgBox.setText(self.helpMessageBoxText)
                        msgBox.exec()
                if event.key() == Qt.Key_0:
                        self.layoutStack['left'].setCurrentIndex(0)
                if event.key() == Qt.Key_1:
                        self.layoutStack['left'].setCurrentIndex(1)
                if event.key() == Qt.Key_2:
                        self.layoutStack['left'].setCurrentIndex(2)
                        
                        
        timer = None
        time_us = 0 # microseconds!
        time_max = 0
        def startExperiment(self):
                #self.setWindowState( Qt.WindowFullScreen )
                #self.right.setWindowState( Qt.WindowFullScreen )
                #self.left.setWindowState( Qt.WindowFullScreen )

                self.sliceTrial()

                # TODO reverse naming convention to self.resultsFile self.resultsCSV
                
                
                #datetime.datetime.now().strftime('%Y%m%d-%H%M%S')                
                
                if len(self.filenameResults):
                        self.fileResults = open(self.filenameResults,'w+') # or a+ if appending
                else:
                        # if you choose not to save, a dummy file:
                        self.fileResults = io.StringIO()
                
                
                self.csvResults = csv.DictWriter(self.fileResults,list(self.trial.keys()))
                if self.fileResults.tell()==0:
                        self.csvResults.writeheader()
                



                #self.players['close left'].player.play()

                #self.currentVideo = 'close left'
                #self.currentVideo = self.trial['place1']

                #self.layoutStack['main'].setCurrentIndex( self.players[self.currentVideo].stackedIndex )
                #self.players[self.currentVideo].player.play()
                
                #The robot has its eyes closed
                
                self.currentVideo = 'close left' # default, TODO set it to index 0
                
                # prepare
                #self.time_us = time.time_ns()/1000
                self.time_us = time.time()*1e6
                self.nextEvent = 0
#                self.timeEvent = time.time_ns()/1000
                self.timeEvent = time.time()*1e6
                
                # start
                self.timer = QTimer()
                self.timer.timeout.connect(self.stepExperiment)
                self.timer.start()
                
                #It opens its eyes
                #It either looks straight towards participants' eyes or down.
                #It looks towards the left or right screen
                #After a specific time of the initiation of the robot's lateral movement towards the left/right screen (this time is called SOA, here it should be 1s), the target letter (T or V) appears. We have prepared the videos which embed steps 1-4 with the specific SOA. That means that when the video finishes the letter should appear directly.
                #The letter should appear for 200 ms. The central robot video should be stuck to the last frame (when the letters are presented) but we also want to continue listening to the sound of the video. Participants can respond from the appearance of the letter and on. Only when they respond the video stops being presented and we go to step 7
                #The robot returns to its initial position with eyes closed and the next trial starts. We have prepared a video for this.

        finishedExperiment = pyqtSignal()
        def stepExperiment(self):
                #
                #  this is from sketch11, incompatible with mods in sketch12 (dynamic .yaml interpreter)
                #    DO NOT MIX THEIR CODE !
                #
                #  requires self.currentVideo to be already set
                
                #timeNew = time.time_ns()/1000 # microseconds
                timeNew = time.time()*1e6 # microseconds
                
                # time passed since the last event:
                timePassed = (timeNew - self.timeEvent)/1000 # milliseconds
                
                #print(timeNew - self.time_us)
                if timeNew - self.time_us > self.time_max:
                        self.time_max = timeNew - self.time_us
                        print("new max",self.time_max)
                self.time_us=timeNew
                #print("time passed",timePassed)

                if self.nextEvent==0: # wait for the head to go left
                        print("DEBUG: event 0")
                        self.players[ self.currentVideo].player.setPosition(0) # grab a pencil and rewind tape
                        self.currentVideo = self.trial['place1']

                        self.layoutStack['main'].setCurrentIndex( self.players[self.currentVideo].stackedIndex )
                        self.players[self.currentVideo].player.play()
                        self.nextEvent += 1
                        self.timeEvent = timeNew # reset time

                        print(f"DEBUG: {self.nextEvent},{self.timeEvent}")
                if self.nextEvent==1: # wait for the head to go left
                        if self.players[self.currentVideo].player.state() == QMediaPlayer.PausedState:
                                print("DEBUG: paused")
                                self.nextEvent += 1
                                self.timeEvent = timeNew # reset time
                                self.correctInput = '' # clear input
                                place2 = self.trial['place2']
                                stack = self.labels[place2].stack
                                self.layoutStack[stack].setCurrentIndex(self.labels[place2].stackedIndex) # show letter
                elif self.nextEvent==2: # show letter
                        if timePassed>200:
                                place4 = self.trial['place4']
                                stack = self.labels[place4].stack
                                self.layoutStack[stack].setCurrentIndex(self.labels[place4].stackedIndex) # hide letter
                        if len(self.correctInput)>0: # check for input flag
                                if self.trial['key']==self.correctInput:
                                        print("User took:",timePassed,"ms to hit the right key")
                                        self.results['key'] = timePassed
                                place4 = self.trial['place4']
                                stack = self.labels[place4].stack
                                self.layoutStack[stack].setCurrentIndex(self.labels[place4].stackedIndex) # be sure about hiding the letter!
                                self.nextEvent += 1
                                self.timeEvent = timeNew # reset time
                        if timePassed>1500: # timeout
                                self.nextEvent += 1
                                self.timeEvent = timeNew # reset time
                                print("user input timed out")
                elif self.nextEvent==3: 
                        self.players[ self.currentVideo].player.setPosition(0) # grab a pencil and rewind tape
                        self.currentVideo = self.trial['place3']
                        self.layoutStack['main'].setCurrentIndex( self.players[self.currentVideo].stackedIndex )
                        self.players[self.currentVideo].player.play()
                        self.timeEvent = timeNew # reset time
                        self.nextEvent += 1
                elif self.nextEvent==4:
                        if timePassed>2000:
                                if self.players[self.currentVideo].player.state() == QMediaPlayer.PausedState:
                                        self.nextEvent += 1
                                        self.timeEvent = timeNew # reset time
                elif self.nextEvent==5: # reset
                        #self.players[ self.currentVideo].player.setPosition(0) # grab a pencil and rewind tape
                        #self.currentVideo = 'mutual left
                        #self.layoutStack.setCurrentIndex(1)
                        #self.players[ self.currentVideo ].player.play()
                        
                        self.timeEvent = timeNew # reset time
                        self.nextEvent += 1
                elif self.nextEvent==6:
                        self.nextEvent = 0
                        self.saveResults()
                        #if  > 0: # yaml-based
                        if self.trialsLeft()>0:
                                self.sliceTrial()
                        else:
                                self.fileResults.close()
                                self.pauseExperiment()
                                self.labels['instructions'].setText('press q to return to main menu' )
                                self.layoutStack['main'].setCurrentIndex(0)
                                
        def trialsLeft(self):
                return len(trials) # list of dictionaries
                #return len(self.db['trial']) # yaml-based dict of a dict

        def sliceTrial(self):
                # # yaml-based:
                #trialTuple = self.db['trial'].popitem() # will return a tuple (name,dict)
                #self.trial = trialTuple[1] # extract only the dictionary
                
                self.trial = trials.pop(0)
                self.results = self.trial # prepare results
                
        def pauseExperiment(self):
                self.timer.stop()
                #self.players['close left'].player.stop()
                print("Max recorded delay in stepExperiment:",self.time_max,"us")

        def saveResults(self):
                # DELETED, pasted into snippet_089_csv.py
                self.csvResults.writerow(self.results)
                pass

        def closeEvent(self,event):
                super().closeEvent(event)
                self.left.close()
                self.right.close()


class CuteManager( QMainWindow ):
        def __init__(self):
                super().__init__()
                self.setWindowTitle(defaults.appName)
                self.initMenus()
                self.statusBar().showMessage("Ready")
                
                self.cuteTextEditor = CuteTextEditor()
                self.cuteTextEditor.setDisabled( True )
                
                self.cuteGraph = QWidget()
                self.cuteTrials = QWidget()
                self.cuteResults = QWidget()
                
                #self.cuteDocument = QTextDocument()
                
                layout = QHBoxLayout()
                
                self.properties = CuteProperties()
                
                self.dock1 = QDockWidget("Properties")
                self.dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
                self.dock1.setWidget(self.properties)
                self.addDockWidget(Qt.LeftDockWidgetArea, self.dock1)
                
                
                self.tabs = QTabWidget()
                self.tabs.addTab(self.cuteTextEditor,"Text")
                self.tabs.addTab(self.cuteGraph,"Graph")
                self.tabs.addTab(self.cuteTrials,"Trials")
                self.tabs.addTab(self.cuteResults,"Results")
                
                self.tabs.setTabEnabled(self.tabs.indexOf(self.cuteGraph),False)
                self.tabs.setTabEnabled(self.tabs.indexOf(self.cuteTrials),False)
                
                self.setCentralWidget(self.tabs)
                self.resize(QSize(700,600))
                
                self.openFile(fileName="posner03.yaml")
                
        def initMenus(self):
                
                # TODO change to self.actionExit - naming convention
                exitAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_TrashIcon')), '&Exit', self)        
                exitAct.setShortcut('Ctrl+Q')
                exitAct.setStatusTip('Exit application')
                exitAct.triggered.connect(app.quit)

                openAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_DirOpenIcon')), '&Open', self)        
                openAct.setShortcut('Ctrl+O')
                openAct.setStatusTip('Open File')
                openAct.triggered.connect(self.openFile)

                self.playAct = QAction(self.style().standardIcon(getattr(QStyle, 'SP_MediaPlay')), '&Run', self)        
                self.playAct.setShortcut('F5')
                self.playAct.setStatusTip('Run')
                self.playAct.triggered.connect(self.runExperiment)
                self.playAct.setDisabled( True )
                
                self.toolbar = self.addToolBar('Toolbar')
                self.toolbar.addAction(openAct)
                self.toolbar.addAction(self.playAct)

                #self.statusBar() # show something on a statusbar?

                menubar = self.menuBar()
                fileMenu = menubar.addMenu('&File')
                #fileMenu.addAction(newAct)
                fileMenu.addAction(openAct)
                #fileMenu.addMenu(localAct) # check current dir and make a quick list
                #fileMenu.addAction(saveAct)
                #fileMenu.addAction(saveasAct)
                fileMenu.addAction(exitAct)
                editMenu = menubar.addMenu('&Edit')
                #fileMenu.addAction(openAct)
                runMenu = menubar.addMenu('&Run')
                runMenu.addAction(self.playAct)

        def openFile(self,logic=False,fileName=""):
                if len(fileName)==0:
                        fileName, fileType = QFileDialog.getOpenFileName(self, "Open File", "", "YAML files (*.yml *.yaml)")
                if len(fileName)!=0:
                        file = QFile(fileName)
                        if file.open(QFile.ReadOnly | QFile.Text):
                                self.cuteTextEditor.setPlainText(str(file.readAll(),'utf-8'))
                        self.fileName = fileName
                        self.playAct.setDisabled( False )
                        
        def runExperiment(self):
                # first save the experiment, sync all the files:
                pass # TODO
                # final setup window, hit enter to continue with defaults
                pass # TODO
                
                # start
                self.setWindowState(Qt.WindowMinimized)
                with open(self.fileName,'r') as file:
                        self.db = yaml.load(file,Loader=yaml.Loader)
                self.cuteMain = CuteMain(self.db)
                self.cuteMain.finishedExperiment.connect(self.closeExperiment)
                self.cuteMain.show()
                
                
        def closeExperiment(self):
                self.cuteMain.close()
                #self.setWindowState(Qt.WindowNoState) # NOT working on Ubuntu w/ Docker
                self.hide()
                self.show()
                self.windowHandle().setVisibility(QWindow.Windowed)
        
        
class CuteTextEditor( QTextEdit ):
        def __init__(self):
                super().__init__()
                pass


class CuteProperties( QTreeWidget ):
        def __init__(self):
                super().__init__()
                pass




if __name__ == '__main__':
        label = CuteManager()
        label.show()
        app.exec()