# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:57:26 2020

Version: 1.0

@author: GLR & PRT
"""
#%%class imporation
from random import randint
import grid
import player

#%% Debut class
class Partie():
    def __init__(self):
        self.playerVSplayer()
        self.ialvl = 2
        self.side = randint(0,1)
        self.generer()
     
    def generer(self):
        self.grid= grid.Grid()
        self.colorTour = 1
        self.nbrTour = 1
        self.play = True
        self.winer = None
        
        if self.currentPlayerType() == 'ai':
            self.unTourAi()
        
        
    #%% gestion joueurs
    def playerVSia(self):
        if self.side is None:
            side = randint(0,1)
        else:
            side = self.side
        if side:
            self.player = {-1:player.AiPlayer("noir", self.ialvl), 1:player.HumanPlayer("blanc") }
        else:
            self.player = {-1:player.HumanPlayer("noir"), 1:player.AiPlayer("blanc", self.ialvl) }
    
    def playerVSplayer(self):
        self.player = {-1:player.HumanPlayer("noir"), 1:player.HumanPlayer("blanc") }     
    
    #fonction de débug uniquement
    def __iaVSia(self):
        self.player = {-1:player.AiPlayer("noir",2), 1:player.AiPlayer("blanc", 0) }
    
    def currentPlayer(self):
        """
        Joueur à qui c'est le tour.

        Returns
        -------
        player.Player()
            Joueur qui doit jouer.

        """
        return self.player[self.colorTour]
    
    def nextPlayer(self):
        """
        Joueur à qui ce n'est pas le tour.

        Returns
        -------
        player.Player()
            Joueur qui doit jouer au prochain tour.

        """
        return self.player[self.colorTour*-1]
    
    def currentPlayerType(self):
        """
        Type du joueur à qui c'est le tour.

        Returns
        -------
        str
            type du joueur qui doit jouer.

        """
        return self.currentPlayer().type

    #%% Fonctions de tour:  
    def unTourPlayer(self, posFrom, posTo):
        """
        Fonction qui effectue la totalité d'un tour de jeu d'un joueur.
        ----------
        Parameters
        ----------
        posFrom : Tuple
            Position de départ.
        posTo : Tuple
            Position d'arrivée.

        Returns
        -------
        None.
        
        """
        if self.grid.allowMove(self.colorTour, posFrom, posTo):
            self.grid.move(posFrom, posTo)
            if not self.continueTour(posTo):
                self.endOfTour()
        
    def unTourAi(self):
        """
        Fonction qui effectue la totalité d'un tour de jeu d'une IA.
        ----------
        None.
        """
        self.currentPlayer().updateGrid(self.grid)
        moves = self.currentPlayer().askMove()
        if moves == None:
            self.winer = self.nextPlayer()
            self.endOfGame()
        else:
            for i in range(len(moves)//2):
                posFrom, posTo = moves[i*2], moves[i*2+1]
                if self.grid.allowMove(self.colorTour, posFrom, posTo):
                    self.grid.move(posFrom, posTo)
            self.endOfTourAi()
        
    def endOfTourAi(self):
        """
        Fonction de fin de tour d'une Ai.
        ----------
        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        self.endOfTour()
        self.grid.isKill, self.grid.posKill, self.grid.posPostKill = False, None, None
        
    def endOfTour(self):
        """
        Fonction de fin de tour.
        ----------
        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        if self.colorTour == -1: self.nbrTour +=1
        self.colorTour *=-1
        self.grid.checkForDames()
        self.continueGame()
        

        
    def continueTour(self, posTo):
        """
        Indique si le tour doit continuer ou non.
        A utilisé après un déplacement.
        ----------
        Parameters
        ----------
        posTo : Tuple
                Position d'arrivée.
        
        Returns
        -------
        Bool
            la valeur booléenne corespondant à la fin d'un tour.
            True -> le tour continue.
            False -> le tour est fini.
        """
        return self.grid.continueTour(posTo)
    
    
    #%% Fonction de fin de partie          
    def continueGame(self):
        """
        Indique si la partie est finie.
        
        Returns
        -------
        None.
        """
        if self.play:
            self.play = self.grid.pionLeftBlack and self.grid.pionLeftWhite
    
    def whoWin(self):
        """
        Indique qui gagne la partie, actualise self.winer.

        Returns
        -------
        None.
        """
        if self.winer is None:
            if self.grid.pionLeftBlack == 0:
                self.winer = 'Blanc'
            elif self.grid.pionLeftWhite == 0:
                self.winer = 'Noir'
    
    def endOfGame(self):
        """
        Met fin a la partie et renvoie le gagnant.

        Returns
        -------
        Str
            Couleur du joueur gagnant.

        """
        self.play = False
        return self.winer
    
    def charger(self):
        """
        Charge une partie existante.

        Returns
        -------
        None.

        """
        temp = self.grid[:,:]
        self.grid = grid.Grid()
        self.grid[:,:] = temp
        self.grid.charger()

### END OF FILE