# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:00:04 2020

Version: 1.0

@author: GLR & PRT
"""

from random import randint as rd
from copy import deepcopy as cp


class Player():
    def __init__(self, color):
        if color == 'noir':
            self.__color__ = -1
        else:
            self.__color__ = 1
            
    
    def colorName(self):
        colorCode = {-1:'noir', 1:'blanc'}
        return colorCode[self.color]
    
    def __str__(self):
        return self.colorName()
    
    @property
    def color(self):
        return self.__color__
    

class HumanPlayer(Player):
    """
    Classe joueur humain.
    """
    def __init__(self, color):
        Player.__init__(self, color)
        self.type = 'player'


class AiPlayer(Player):
    """
    Classe joueur Interlligence artificielle.
    """
    def __init__(self, color, level):
        Player.__init__(self, color)
        self.type = 'ai'
        self.grid = None
        self.level = level
    
    #%% Position jouable
    def playablePos(self, grid, color):
        """
        Donne la liste des pions jouables selon les règles du jeu de Dame.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
        color : int
            -1 ou 1 suivant le type du joueur.

        Returns
        -------
        playable : list
            liste des tuple de position jouable.

        """
        playable = []
        for i in range(1,11):
            for j in range(1,11):              
                if grid[i,j]*color>0 and self.__playablePion(grid, (i,j),color) :
                    playable.append((i,j))
        return playable
           
    def __playablePion(self, grid, pos, color):        
        """
        Retourne le booléen corespondant à la jouabilité d'une position.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
        pos : tuple
            position à tester
        color : int
            -1 ou 1 suivant le type du joueur.

        Returns
        -------
        bool
            jouabilité du pion

        """
        posTestKill = [(1,1),(1,-1),(-1,1),(-1,-1)]
        if abs(grid[pos]) == 1:
            posTest = [(-color,1),(-color,-1)]
        else:
            posTest = posTestKill
        i,j = pos
        for e in posTest:
            if not grid[i+e[0],j+e[1]]:
                return True
        for e in posTestKill:
            pos1 = grid[i+e[0],j+e[1]]
            if pos1 < 5 and pos1*color<0 and not grid[i+e[0]*2,j+e[1]*2]:
                return True
        return False
    
    #%% Mouvement avec kill
    def killPossibles(self, grid, pos, color):
        """
        Retourne les mouvements en cas de kill.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
        pos : tuple
            position à tester
        color : int
            -1 ou 1 suivant le type du joueur.        

        Returns
        -------
        list
            list des mouvement tuant possible.

        """
        test = abs(grid[pos])
        if test == 1:
            return self.__killPossiblesPion(grid, pos, color, [])
        elif test == 2:
            return self.__killPossiblesDame(grid, pos, color, [])
          
    def __killPossiblesPion(self, grid, pos, color, posKill):
        """comme killPossibles mais uniquement pour un pion"""
        res = []
        x,y = pos
        posTest = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for e in posTest:
            posAdv = x+e[0],y+e[1]
            posTo = x+e[0]*2,y+e[1]*2
            if posAdv in posKill:
                pionPosAdv = 0
            else:
                pionPosAdv = grid[posAdv]
            if posTo in posKill:
                pionPosTo = 0
            elif 0<posTo[0]<11 and 0<posTo[1]<11 :
                pionPosTo = grid[posTo]
            else:
                pionPosTo = float('inf')
            if (pionPosAdv <5
                and pionPosAdv*color<0 
                and not pionPosTo):
                temp = [pos, posTo]
                res.append(temp)
                for elm in self.__killPossiblesPion(grid, posTo, color, posKill+[posAdv, pos]):
                    res.append(temp+elm)
        return res
      
    def __killPossiblesDame(self, grid, pos, color, posKill):
        """comme killPossibles mais uniquement pour une dame"""
        x,y = pos
        posTest = [(1,1), (1,-1), (-1,1), (-1,-1)]
        res = []
        for e in posTest:
            i = 0
            test = True
            kill = 0
            while test:
                i+=1
                posAdv = (x+i*e[0],y+i*e[1])
                if 0<posAdv[0]<11 and 0<posAdv[1]<11:
                    if posAdv in posKill:
                        pionPosAdv = 0
                    else:
                        pionPosAdv = grid[posAdv]
                    if pionPosAdv * color >0:
                        test = False
                    elif pionPosAdv * color <0 and not kill:
                        kill = 1
                        posKillPion = posAdv
                    elif pionPosAdv * color <0 and kill:
                        test = False
                    elif kill and not pionPosAdv:
                        temp = [pos, posAdv]
                        res.append(temp)
                        for elm in self.__killPossiblesDame(grid, posAdv, color, posKill+[posKillPion, pos]):
                            res.append(temp+elm)
                        
                else:
                    test = False
        return res

    #%% Mouvement sans kill
    def movePossibles(self, grid, pos, color):
        """
        Donne la liste des mouvements possibles selon les règles
        du jeu de Dame.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
        pos : tuple
            position à tester
        color : int
            -1 ou 1 suivant le type du joueur.   

        Returns
        -------
        list
            mouvements possibles.

        """
        if color *grid[pos]<0:
            return []
        test = abs(grid[pos])
        if test == 1:
            return self.__movePossiblesPion(grid, pos, color)
        elif test == 2:
            return self.__movePossiblesDame(grid, pos, color)
        
    def __movePossiblesPion(self, grid, pos, color):
        """comme movesPossibles mais uniquement pour un pion"""
        posTest = [(-color,1),(-color,-1)]
        res = []
        for e in posTest:
            posTo = (pos[0]+e[0],pos[1]+e[1])
            if not grid[posTo]:
                res.append((pos,posTo))
        return res
    
    def __movePossiblesDame(self, grid, pos, color):
        """comme movePossibles mais uniquement pour une dame"""
        posTest = [(1,1),(1,-1),(-1,1),(-1,-1)]
        res = []
        for e in posTest:
            i=1
            test = True
            posTo = (pos[0]+i*e[0],pos[1]+i*e[1])
            while test and 0<posTo[0]<11 and 0<posTo[1]<11:
                i+=1
                if not grid[posTo]:
                    res.append((pos,posTo))
                    posTo = (pos[0]+i*e[0],pos[1]+i*e[1])
                else :
                    test = False
                    
        return res
    
    #%% Toutes les actions possibles          
    def actionPossible(self, grid, color):
        """
        Donne la liste des mouvements possibles selon les règles
        du jeu de Dame, en tanant compte du principe de kill prioritaire.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
        color : int
            -1 ou 1 suivant le type du joueur.

        Returns
        -------
        res : list
            Mouvements possibles.

        """
        res = []
        pionPlayable = self.playablePos(grid, color)
        for pos in pionPlayable:
            res += self.killPossibles(grid, pos, color)
        if not res:
            for pos in pionPlayable:
                res += self.movePossibles(grid, pos, color)   
        else:
            len_max = -1
            for move in res:
                len_move = len(move)
                if len_move > len_max:
                    len_max = len_move
                    resKill = [move]
                elif len_move == len_max:
                   resKill.append(move)
            res = resKill
        return res
    
    def finDePartie(self, grid, color):
        """
        Retorune si la partie est finie ou non.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
        color : int
            -1 ou 1 suivant le type du joueur.

        Returns
        -------
        Bool
            booleen représentant l'état de la partie.

        """
        return (not grid.pionLeftBlack 
            or not grid.pionLeftWhite 
            or not len(self.playablePos(grid, color)))

    #%% Fonction de choix de mouvement    
    def countPoint(self, node, color):
        """
        Fonction d'évaluation d'une grille.

        Parameters
        ----------
        node : grid.Grid()
            plateau de jeu.
        color : int
            -1 ou 1 suivant le type du joueur.

        Returns
        -------
        int
            Point correspondant à l'évaluation de l'état d'un plateau.

        """
        if not node.pionLeftBlack :
            point = float('inf')
        elif not node.pionLeftWhite: 
            point = -float('inf')
        else:
            point = 0
            for i in range(1,11):
                for j in range(1,11):
                    if abs(node[i,j])==2:
                        point+= node[i,j]*5
                    elif j==1 or j==10:
                        point+= node[i,j]*2
                    else:
                        point+= node[i,j]
        return point*color
    
    def __moveChoice(self):  
        """
        Choisis le mouvement optimal.

        Returns
        -------
        list
            mouvement choisi.

        """
        moves = self.actionPossible(self.grid, self.color)
        if len(moves) == 0:    #pas de mouvement possible
            return None        #fin de le partie
        if len(moves) == 1:    #gain de temps lorsqu'un seul
            return moves[0]    #mouvement est possible
        bestPoint = -float('inf')
        bestMove = [moves[0]]
        for move in moves:
            node = cp(self.grid)
            self.moveAi(node, move, self.color)
            point = self.negamax(node, self.level-1, self.color*-1)
            if point > bestPoint:
                bestPoint, bestMove = point, [move]
            elif point == bestPoint:
                bestMove.append(move)
        return bestMove[rd(0,len(bestMove)-1)]
            

    def moveAi(self, grid, moves, color):
        """
        Fonction qui réalise le mouvement.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
        moves : list
            list des mouvements à réaliser.
        color : int
            -1 ou 1 suivant le type du joueur.

        Returns
        -------
        None.

        """
        for i in range(len(moves)//2):
            posFrom, posTo = moves[i*2], moves[i*2+1]
            if grid.allowMove(color, posFrom, posTo):
                grid.move(posFrom, posTo)
        grid.checkForDames() #une dame n'est formée que si on s'arrete sur la
                             #case pas si on y passe en tuant
        grid.isKill, grid.posKill, grid.posPostKill = False, None, None

       
    def askMove(self):
        """
        Fonction de choix de mouvement à appeler.

        Returns
        -------
        move : list
            Mouvement choisi.

        """
        move = self.__moveChoice()
        return move
    
    def updateGrid(self, grid):
        """
        Met a jours le plateau de jeu.

        Parameters
        ----------
        grid : grid.Grid()
            plateau de jeu.
            
        Returns
        -------
        None.

        """
        self.grid = grid
        
    def negamax(self, node, depth, color):
        """
        Evalue un arbre de possibilité de mouvement.

        Parameters
        ----------
        node : grid.Grid()
            plateau de jeu.
        depth : int
            Profondeur restant a calculer.
        color : int
            -1 ou 1 suivant le type du joueur.

        Returns
        -------
        int
            Meilleur score possible.

        """
        if depth <= 0 or node.endOfGame():
            return self.countPoint(node, color*-1)
        value = -float('inf')
        for moves in self.actionPossible(node, color):
            child = cp(node)
            self.moveAi(child, moves, color)
            value = max(value, -self.negamax(child, depth-1, color*-1 ))
        return value
        

### END OF FILE
