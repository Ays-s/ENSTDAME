# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 17:02:29 2020

Version: 2.0

@author: GLR & PRT
"""
#%%class imporation
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from functools import partial
import sys
import time
import pickle

import partie

#%% Debut class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        #Load UI
        self.ui = uic.loadUi('Interface.ui', self)
        self.ui.bouton_new_2.clicked.connect(self.generer)
        
        #Menu
        self.ui.ialvl0.triggered.connect(partial(self.setialvl,0))
        self.ui.ialvl1.triggered.connect(partial(self.setialvl,1))
        self.ui.ialvl2.triggered.connect(partial(self.setialvl,2))
        self.ui.ialvl3.triggered.connect(partial(self.setialvl,3))
        self.ui.ialvl4.triggered.connect(partial(self.setialvl,4))
        self.ui.ialvl5.triggered.connect(partial(self.setialvl,5)) 
        self.ui.sideBlanc.triggered.connect(partial(self.setside,1))
        self.ui.sideNoir.triggered.connect(partial(self.setside,0))
        self.ui.sideAlea.triggered.connect(partial(self.setside,None))
        self.ui.playerVplayer.triggered.connect(self.setplayer)
        self.ui.actionCharger.triggered.connect(self.charger)
        self.ui.actionSauvegarder.triggered.connect(self.sauvegarder)
        
        self.pawnWhite = QPixmap("img/pawnWhite.png")
        self.kingWhite = QPixmap("img/kingWhite.png")
        self.pawnBlack = QPixmap("img/pawnBlack.png")
        self.kingBlack = QPixmap("img/kingBlack.png")   
        pixmap = QtGui.QPixmap()
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.Conteneur.lower()
        self.ui.Conteneur.stackUnder(self)
        self.ui.Conteneur.setAutoFillBackground(True)
        self.ui.Conteneur.setPalette(pal)
    
        size = min(self.size().width(), self.size().height())
        self.marge = size//5
        self.win = size-2*size//5
        self.case = self.win//10
        
        self.movie = QMovie('img/firework.gif', QByteArray(), self)
        self.movie_screen = QLabel(self)
        self.movie_screen.setGeometry((self.size().width()-500)/2,(self.size().width()-522)/2,500, 522)
        self.movie_screen.setMovie(self.movie)
        
        #generation de la partie
        self.partie = partie.Partie()
        self.posTo = None
        self.posFrom = None
        
    #%%Nouvelle partie    
    def generer(self):
        """
        Genere une nouvelle partie.

        Returns
        -------
        None.

        """
        self.partie.generer()
        self.movie.stop()
        self.movie_screen.hide()
        self.repaint()
    
    def setialvl(self, level):
        """
        Change le niveau de l'IA. Et lance une partie joueur contre IA.

        Parameters
        ----------
        level : int
            Niveau de recursion de l'IA.

        Returns
        -------
        None.

        """
        self.partie.ialvl = level
        self.partie.playerVSia()
        self.generer()
        
    def setside(self,side):
        """
        Change la couleur du joueur. Et lance une partie joueur contre IA.

        Parameters
        ----------
        side : int
            Correspond au side du joueur.

        Returns
        -------
        None.

        """
        self.partie.side = side
        self.partie.playerVSia()
        self.generer()     
        
        
    def setplayer(self):
        """
        lance une partie de joueur contre joueur.

        Returns
        -------
        None.

        """
        self.partie.playerVSplayer()
        self.generer()
        
    #%% Gestion de l'affichage
    def resizeEvent(self, event):
        """
        Redimensionne la fenetre.

        Parameters
        ----------
        event : event.

        Returns
        -------
        None.

        """
        self.win = min(self.size().width(), self.size().height())
        self.case = self.win/12
        self.movie_screen.move((self.size().width()-500)/2,(self.size().width()-522)/2,)
        QMainWindow.resizeEvent(self, event)
        
    def paintEvent(self, event):
        """
        Affiche le plateau de jeu, ou la fenetre de fin de jeu.

        Parameters
        ----------
        event : event.

        Returns
        -------
        None.

        """
        painter = QPainter(self)        

        if self.partie.play:
            #move bouton
            self.ui.horizontalLayoutWidget_2.setGeometry(self.case, self.case*10.5, self.case*10, self.case)
            #Draw background
            painter.setPen(QPen(Qt.black,  1, Qt.SolidLine))
            painter.setBrush(QBrush(QColor(47,47,47), Qt.SolidPattern))
            painter.drawRect(self.case, self.case, self.win-2*self.case, self.win-2*self.case)
            
            #Draw Tour
            painter.setPen(QColor("royalblue"))
            painter.setFont(QFont('Helvetica', self.case/3))
            painter.drawText(self.case*4.3,self.case*0.9,"Tour {0} : {1}".format(self.partie.nbrTour, self.partie.currentPlayer()))
        
            #Draw checkboard
            painter.setBrush(QBrush(QColor(255,250,240), Qt.SolidPattern))
            for i in range(1, 11):
                for j in range(1, 11):
                    if (i+j)%2:
                        painter.drawRect(self.case*i, self.case*j, self.case, self.case)
                    if self.partie.grid[j,i] == 1 :
                        painter.drawPixmap(QRect(self.case*i, self.case*j, self.case, self.case), self.pawnWhite)
                    elif self.partie.grid[j,i] == -1:
                        painter.drawPixmap(QRect(self.case*i, self.case*j, self.case, self.case), self.pawnBlack)
                    elif self.partie.grid[j,i] == 2:
                        painter.drawPixmap(QRect(self.case*i, self.case*j, self.case, self.case), self.kingWhite)
                    elif self.partie.grid[j,i] == -2:
                        painter.drawPixmap(QRect(self.case*i, self.case*j, self.case, self.case), self.kingBlack)
        else:
            #Draw winer
            self.movie_screen.show()
            painter.setPen(QColor("royalblue"))
            painter.setFont(QFont('Helvetica', self.case))
            painter.drawText(QRectF(0,0,self.size().width(),self.case*3),Qt.AlignCenter|Qt.AlignTop,"{0} gagne !!!".format(self.partie.winer).capitalize())
            self.movie.start()
            
    #%% gestion de la souris
    def mousePressEvent(self, event):
        """
        Séléctionne un pion.

        Parameters
        ----------
        event : Mousse press.

        Returns
        -------
        None.

        """
        self.posFrom = (int(event.y()/self.case), int(event.x()/self.case))
        
    def mouseReleaseEvent(self, event):
        """
        Séléctionne une case si un pion a déja été séléctionné.

        Parameters
        ----------
        event : Mousse realese.

        Returns
        -------
        None.

        """
        self.posTo = (int(event.y()/self.case), int(event.x()/self.case))
        if (0<self.posFrom[0]<11 and      #prevent click out of bound
            0<self.posFrom[1]<11 and 
            0<self.posTo[0]<11 and 
            0<self.posTo[1]<11):
            self.unTourHuman()
            
    #%% Sauvegarde et chargement de partie
    def sauvegarder(self):
        """
        Sauvegarde l'état de la partie courante dans un fichier

        Returns
        -------
        None.

        """
        fichier = QFileDialog.getSaveFileName(self, 
                     "Nom de sauvegarde", 
                     "save/save_"+time.strftime("%d-%m-%Y_%Hh%Mm%Ss",time.localtime()), 
                     "Fichier save (*.sav);;Tous (*.*)")
        try: pickle.dump(self.partie ,open(fichier[0],'wb'))
        except: pass
        
    def charger(self):
        """
        Charge une partie précédemment sauvegardée.

        Returns
        -------
        None.

        """
        fichier = QFileDialog.getOpenFileName(self, 
                     "Sélectionnez le fichier à charger", 
                     "save/", 
                     "Fichier save (*.sav);;Tous (*.*)")
        try: 
            self.partie = pickle.load(open(fichier[0],'rb'))
            self.partie.charger()
            self.repaint()
        except: pass

    #%% Gestion des tours de jeu 
    def unTourHuman(self):
        """
        Effectue le tour d'un joueur humain.

        Returns
        -------
        None.

        """
        self.partie.unTourPlayer(self.posFrom, self.posTo) 
        self.endOfTour()
        
    def unTourAi(self):
        """
        Joue le tour d'une IA.

        Returns
        -------
        None.

        """
        self.partie.unTourAi()
        self.endOfTour() 
        
    def endOfTour(self):
        """
        Fin d'un tour, et joue le tour d'une IA si c'est nécéssaire.

        Returns
        -------
        None.

        """
        self.posFrom, self.posTo = None, None
        self.repaint()
        if not self.partie.play :
            self.endOfGame()
        elif  self.partie.currentPlayerType() == 'ai':
            self.unTourAi()
        
    def endOfGame(self):
        """
        Fin de la partie.

        Returns
        -------
        None.

        """
        self.partie.continueGame()
        self.partie.whoWin()
        self.repaint()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()


### END OF FILE