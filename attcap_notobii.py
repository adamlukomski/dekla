#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from PyQt5.QtMultimedia import *

from dekla import *

import csv
import time
import datetime

import random

""" 






"""


class AttCap(Dekla):
        scores = { '30': (1500,-200),
                   '60': (1000,-250),
                   '90': (500,-500),
                   '120': (250,-1000),
                   '150': (200,-1500) }
        
        allbeeps = [ 1,2,3,4,5,10,20,30,60,90,120,150 ] # will be trimmed
        
        waitTime1 = 1000
        waitTime10 = 2000
        
        mode = ''
        participant = None
        #mode = 'cooperative'
        
        player1z = Qt.Key_Z
        player1m = Qt.Key_M
        player2z = Qt.Key_A
        player2m = Qt.Key_K
        
        instructions1 = """
        The basic keybinds:
        
        f for fullscreen
        s for start
        
        Player 1 by default is: z,m
        Player 2 by default is: a,k
        """
        
        labelFont = QFont( "Open Sans", 80, QFont.Bold)
        bigFont = QFont( "Open Sans", 138, QFont.Bold)
        
        petri = dict()
        
        def __init__(self):
                super().__init__()
                
                with open('attcap/trials.csv','r') as csvfile:
                        csvread = csv.DictReader(csvfile)
                        self.trials = [dict(row) for row in csvread]



                # show the config window:
                #
                #  instructions
                #
                #  one number edit field
                #  the focus should be on the field
                #  
                #
                #  buttons for modes
                

                # mode:
                msgBox = QMessageBox()
                msgBox.setText(self.instructions1)
                coopButton = msgBox.addButton("Cooperative", QMessageBox.ActionRole)
                compButton = msgBox.addButton("Competitive", QMessageBox.ActionRole)
                pracButton = msgBox.addButton("Practise", QMessageBox.ActionRole)
                msgBox.setDefaultButton( coopButton )
                msgBox.setEscapeButton( pracButton )
                msgBox.exec()

                if msgBox.clickedButton() == coopButton:
                        print('coop mode')
                        self.mode = 'cooperative'
                if msgBox.clickedButton() == compButton:
                        print('comp mode')
                        self.mode = 'competitive'
                if msgBox.clickedButton() == pracButton:
                        print('practise mode')
                        self.mode = 'practise'
                
                # participant id:
                self.participant, status = QInputDialog.getInt(QWidget(), "Couple id", "Couple id", 0, 0, 300000, 1);
                self.filenameResults = self.savefile+'id_'+str(self.participant)+'_date_'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.csv'
                
                self.addStack('main')
                self.addStack('left')
                self.addStack('right')
                
                self.windows['main'].setMinimumSize(1920,1080)
                self.windows['left'].setMinimumSize(1920,1080)
                self.windows['right'].setMinimumSize(1920,1080)
                
                #self.stacks['main'].addImage('image1','attcap/monday.png') # TODO placeholder for instructions
                
                
                
                #
                #   instructions
                #
                #   show mode
                #
                self.stacks['main'].addImage('image1','attcap/a1.png') # TODO placeholder for instructions
                self.widgets['image1'].setMinimumSize(1920,1080)
                self.widgets['image1'].setBackground('eyetracking/aruco_stage.png')
                self.stacks['left'].addCountDown('timer1')
                self.widgets['timer1'].timeout.connect(self.timerFinished)
                self.widgets['timer1'].setBackground('eyetracking/aruco_timer.png')
                self.widgets['timer1'].labelFont = self.labelFont
                self.stacks['right'].addScore('score1')
                #self.widgets['score1'].setCooperative()
                #self.widgets['score1'].setCompetitive()
                self.widgets['score1'].mode = self.mode
                self.widgets['score1'].setBackground('eyetracking/aruco_score.png')
                
                # TODO this needs to be added to self.widgets
                self.effect = QSoundEffect()
                self.effect.setSource(QUrl.fromLocalFile('attcap/beep_CC_zero.wav'))
                self.effect.setVolume(1.00)
                
                self.petri['current'] = 'place_initial'
                

        def keyPressEvent(self,event):
                super().keyPressEvent(event)
                # TODO refactor this into the new keyboard dict keyDict:
                #if event.key() == Qt.Key_M:
                        #self.checkAnswer(Qt.Key_M)
                #if event.key() == Qt.Key_Z:
                        #self.checkAnswer(Qt.Key_Z)
                        
        def timerFinished(self):
                print("timeout, skipping to self.petri['current'] place_timeout")
                ## do not modify the score
                #self.widgets['score1'].add( self.trial['player'], self.scores[self.trial['maxtime']][1] )
                self.result['answered'] = False
                self.petri['current'] = 'place_timeout'
                
        #def checkAnswer(self,key):
                ##player = 'player1' # TODO fix this to be dynamic
                
                #if self.petri['current'] == 'place_keyboard':
                        #self.result['answered'] = True
                        #correct = (key==QKeySequence.fromString(self.trial['key'])[0])
                        ##print("Correct key should be:",self.trial['key'],'you pressed:',)
                        
                        #self.result['correct'] = correct
                        #if self.result['correct']:
                                #self.widgets['score1'].add( self.trial['player'], self.scores[self.trial['maxtime']][0] )
                        #else:
                                #self.widgets['score1'].add( self.trial['player'], self.scores[self.trial['maxtime']][1] )
                        ##self.results['score1'] = self.widgets['score1'].score()
                        #self.keyboardReceived = True
        
        def sounds(self,timer):
                ##do the beep if crossed on the elements and pop that element
                if self.beeps:
                        if timer.time < max(self.beeps):
                                print("BEEP timer.time:",timer.time,"beep max:", max(self.beeps))
                                self.beeps.remove(max(self.beeps))
                                #play beep
                                self.effect.play()
        
        
        #  ---- main loop ----
        #current = 'place_initial'
        def stepExperiment(self):
                if self.petri['current'] == 'place_initial':
                        self.running = False
                        self.keyTrack( [ self.player1z, self.player1m, self.player2z, self.player2m] )
                        self.petri['current'] = 'place2'
                if self.petri['current'] == 'place2':
                        z1 = self.keyCheck(self.player1z)
                        m1 = self.keyCheck(self.player1m)
                        z2 = self.keyCheck(self.player2z)
                        m2 = self.keyCheck(self.player2m)
                        
                        self.im1 = QPixmap(1200,1000).toImage()
                        self.im1.fill(qRgb(255,255,255))
                        paint1 = QPainter(self.im1)
                        paint1.setPen(Qt.black)
                        paint1.setFont( self.labelFont )
                        paint1.drawText( 200,100,"Trials left: "+str(len(self.trials)+1) )
                        paint1.drawText( 200,300,"Player 1")
                        if z1 or m1:
                                paint1.setPen(Qt.green)
                                paint1.drawText( 700,300,"ready")
                        else:
                                paint1.setPen(Qt.red)
                                paint1.drawText( 700,300,"not ready")
                        paint1.setPen(Qt.black)
                        paint1.setFont( self.labelFont )
                        paint1.drawText( 200,600,"Player 2")
                        if z2 or m2:
                                paint1.setPen(Qt.green)
                                paint1.drawText( 700,600,"ready")
                        else:
                                paint1.setPen(Qt.red)
                                paint1.drawText( 700,600,"not ready")
                                
                        paint1.end
                        self.widgets['image1'].setImage( self.im1 )

                        if ( z1 or m1 ) and ( z2 or m2 ):
                                self.keyRemove( [ self.player1z, self.player1m, self.player2z, self.player2m] )
                                self.petri['current'] = 'place_a2'
                        
                if self.petri['current'] == 'place_a2':
                        self.petriTimer( 2000, 'current', 'place_prepare' )
                        self.petri['current'] = 'pass'
                        # wait for 1 sec
                #
                        # show Player 1 Turn / Player 2 Turn
                # 
                
                
                if self.petri['current'] == 'place_prepare':
                        self.running = True
                        self.widgets['score1'].hideScore()
                        ## this was for randomized time, now it is pseudorandom
                        #self.trial['maxtime'] = random.choice(list(self.scores.keys()))
                        print("maxtime:",self.trial['maxtime'])

                        
                        maxtime = int(self.trial['maxtime'])
                        self.widgets['timer1'].setCountDown( maxtime )
                        self.widgets['timer1'].start()

                        self.beeps = [ b for b in self.allbeeps if b < maxtime ]
                        print("currentBeeps: ",self.beeps)
                        
                        
                        # setImage( imagename, flipped )
                        self.widgets['image1'].setImage( self.trial['imagefile'], self.trial['player']=='player2' )
                        
                        #self.keyboardReceived = False # reset the flag
                        
                        self.keyTrack( [ self.player1z, self.player1m, self.player2z, self.player2m] )
                        self.petri['current'] = 'place_checkkeyboard'
                        
                if self.petri['current'] == 'place_checkkeyboard':
                        z1 = self.keyCheck(self.player1z)
                        m1 = self.keyCheck(self.player1m)
                        z2 = self.keyCheck(self.player2z)
                        m2 = self.keyCheck(self.player2m)
                        # the current player hit one of their two keys:
                        if (self.trial['player']== 'player1' and (z1 or m1)) or (self.trial['player']=='player2' and (z2 or m2)):
                                keys = {'player1z': z1,'player1m': m1, 'player2z': z2, 'player2m': m2}
                                if keys[ self.trial['player']+self.trial['key'] ]:
                                        self.result['correct'] = True
                                        self.widgets['score1'].add( self.trial['player'], self.scores[self.trial['maxtime']][0] )
                                else:
                                        self.result['correct'] = False
                                        self.widgets['score1'].add( self.trial['player'], self.scores[self.trial['maxtime']][1] )
                                self.keyRemove( [ self.player1z, self.player1m, self.player2z, self.player2m] )
                                self.petri['current'] = 'place_keyboard'
                                self.result['answered'] = True
                if self.petri['current'] == 'place_keyboard' or self.petri['current']=='place_timeout':
                        self.widgets['timer1'].stop()
                        self.result['timeLeft'] = self.widgets['timer1'].time
                        self.result['timeUsed'] = int(self.trial['maxtime']) - self.widgets['timer1'].time
                        
                        self.petriTimer( self.waitTime1, 'current', 'place_time1sec' )
                        self.petri['current'] = 'pass'

                if self.petri['current'] == 'place_time1sec':
                        # just show the modified score:
                        self.widgets['score1'].add( self.trial['player'], 0 )
                        self.petriTimer( self.waitTime10-self.waitTime1, 'current', 'place_time10sec' )
                        self.petri['current'] = 'pass'
                
                
                if self.petri['current'] == 'place_time10sec':
                        self.result['participant'] = self.participant
                        self.results.append( self.result )
                        if len(self.trials) > 0:
                                self.sliceTrial()
                                self.petri['current'] = 'place_initial'
                        else:
                                self.petri['current'] = 'pass'
                                self.timer.stop()
                                self.save()
                                qApp.quit()

                if self.running:
                        self.sounds(self.widgets['timer1'])
                
        def closeEvent(self,event):
                super().closeEvent(event)

        def prepareTrials(self):
                with open('attcap/pool.csv','r') as csvfile:
                        csvread = csv.DictReader(csvfile)
                        self.pool = [dict(row) for row in csvread]
                # TODO a full widget to customize those trials

if __name__ == '__main__':
        label = AttCap()
        #label.finishedExperiment.connect(qApp.quit)
        label.show()
        qApp.exec()