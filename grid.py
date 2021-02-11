# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 16:22:30 2020

Version: 2.1

@author: GLR & PRT
"""
#%%class imporation
import numpy as np

#%% Debut class
class Grid(np.ndarray):
       
    #%%Initialisation:
    def __new__(cls):
        new_array = super(Grid, cls).__new__(cls, (12, 12))
        new_array.pionLeftBlack = 20
        new_array.pionLeftWhite = 20
        new_array.posPostKill = None
        new_array.posKill = None
        new_array.isKill = False
        return new_array
        
    def __init__(self):
        self[:,:]=0 #remove all
        self[:,0]=float('inf')
        self[:,-1]=float('inf')
        self[0,:]=float('inf')
        self[-1,:]=float('inf')

        self[2:5:2,1:-1:2]=-1 #setting black 
        self[1:4:2,2:-1:2]=-1 #setting black 
        
        self[8:11:2,1:-1:2]=1 #setting white
        self[7:11:2,2:-1:2]=1 #setting white

        
    def __array_finalize__(self, obj):
         if obj is None:
             return
         self.pionLeftWhite = getattr(obj, 'pionLeftWhite', None)
         self.pionLeftBlack = getattr(obj, 'pionLeftBlack', None)
         self.isKill = getattr(obj, 'isKill', None)
         self.posPostKill = getattr(obj, 'posPostKill', None)
         self.posKill = getattr(obj, 'posKill', None)
         
    def __str__(self):
        text = super(Grid, self[1:-1,1:-1]).__str__()
        text = text.replace(']]',']').replace('[[',' [')
        temp,c ='', 1
        for e in text:            
            if e == '[':
                if c==10: cr = str(c)
                else:cr=' '+str(c)
                temp += cr+e
                c+=1
            elif e==']':
                temp += e+cr
            else:
                temp+=e
        text = temp
        text = text.replace('[','\u2551').replace(']','\u2551')
        text = text.replace(' 0.','--').replace('-1.','PN').replace(' 1.','PB')
        text = text.replace('-2.','DN').replace(' 2.','DB')
        text = ' x:\u2554'+'\u2550'*29 + '\u2557x:\n'+ text +'\n   \u255A' + '\u2550'*29 +'\u255D'
        text = ' y: 1  2  3  4  5  6  7  8  9  10 \n' + text + '\n y: 1  2  3  4  5  6  7  8  9  10'
        text = '--- Noir {0} pions. ---\n'.format(self.pionLeftBlack)+text
        text += '\n--- Blanc {0} pions. ---'.format(self.pionLeftWhite)
        return text 

      
    #%% Fonctions d'autorisation de mouvement
    def allowMove(self, colorTour, posFrom, posTo):
        """
        Fonction qui autorise le déplacement d'un pion ou d'une dame
        de posFrom à posTo.
        ----------
        Parameters
        ----------
        posFrom : Tuple
            Position de départ.
        posTo : Tuple
            Position d'arrivée.

        Returns
        -------
        Bool
            la valeur booléenne corespondant à l'autorisation
            de déplacement.
        """
        if self[posTo]*self[posFrom]!=0 or self[posFrom]>5 or self[posTo]>5:
            return False
        if self.posPostKill != None and self.posPostKill != posFrom:
            return False
        if colorTour * self[posFrom]<0:
            return False
        dx, dy = posFrom[0]-posTo[0], posFrom[1]-posTo[1]
        if abs(dx)!=abs(dy) or dx==0:
                return False
        if self[posFrom] == 1 or self[posFrom] == -1:
            return self.__allowMovePion(posFrom, posTo)
        elif self[posFrom] == 2 or self[posFrom] == -2:
            return self.__allowMoveDame(posFrom, posTo)
        else: return False
            
    def __allowMovePion(self, posFrom, posTo):
        """
        Fonction qui autorise le déplacement d'un pion de
        posFrom à posTo.
        ----------
        Parameters
        ----------
        posFrom : Tuple
            Position de départ.
        posTo : Tuple
            Position d'arrivée.

        Returns
        -------
        Bool
            la valeur booléenne corespondant à l'autorisation
            de déplacement.
        """
        dx, dy = posFrom[0]-posTo[0], posFrom[1]-posTo[1]
        if dx == self[posFrom]:
            return True, False
        elif abs(dx) == 2:
            posAdv = posFrom[0]-dx//2,posFrom[1]-dy//2
            if self[posFrom] * self[posAdv] <0:
                self.posKill, self.posPostKill = posAdv, posTo
                self.isKill = True
                return True
        else: return False
                
    def __allowMoveDame(self, posFrom, posTo):
        """
        Fonction qui autorise le déplacement d'une dame de
        posFrom à posTo.
        ----------
        Parameters
        ----------
        posFrom : Tuple
            Position de départ.
        posTo : Tuple
            Position d'arrivée.

        Returns
        -------
        Bool
            la valeur booléenne corespondant à l'autorisation
            de déplacement.
        """
        nbPion = 0
        dx, dy = posFrom[0]-posTo[0], posFrom[1]-posTo[1]
        sx = range(posFrom[0],posTo[0],-dx//abs(dx))
        sy = range(posFrom[1],posTo[1],-dy//abs(dy))
        for i in range(1,len(sx)):
             posAdv = (sx[i],sy[i])
             if self[posAdv]:
                 nbPion +=1
                 posKill = posAdv
                 if nbPion >1:
                     return False
        if nbPion == 0: return True
        elif nbPion == 1 and self[posKill] * self[posFrom]<0:
            self.posKill, self.posPostKill = posKill, posTo
            self.isKill = True
            return True
        else: return False
        
        
    #%% Fonctions de mouvement:
    def move(self, posFrom, posTo):
        """
        Fonction qui déplace un pion de posFrom à posTo.
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
        self[posTo] = self[posFrom]
        self[posFrom] = 0
        if self.isKill:
            self.kill()
            self.posPostKill = posTo
        
    #%% Fonction check
    def checkForDames(self):
        """
        Vérifie qu'aucun pion ne doit être transformé en dame.
        Et le transforme le cas échéant.

        Returns
        -------
        None.
        
        """
        for y in range(1,10):
            if self[1,y] == 1:
                self[1,y] = 2
            if self[10,y] == -1:
                self[10,y] = -2
    
    
    #%% Fonctions de kill
    def isKillPossible(self, pos):
        """
        Indique si un pion peut être sauté à partir d'une position.
        ----------
        Parameters
        ----------
        pos : Tuple
            Position du pion a vérifier.

        Returns
        -------
        Bool
            la valeur booléenne corespondant à la possibilité
            de sauter un pion.
        """
        x,y = pos
        posTest = [(1,1),(1,-1),(-1,+1),(-1,-1)]
        if abs(self[pos])==1:     #test Pion          
            for e in posTest:
                if self[x+e[0],y+e[1]] <5 and self[x+e[0],y+e[1]]*self[x,y]<0 and not self[x+e[0]*2,y+e[1]*2]:
                    return True
        elif abs(self[pos])==2:   #test Dame
            for e in posTest:
                i, test = 0, True
                while test:
                    i+=1
                    posAdv = (x+i*e[0],y+i*e[1])
                
                    if not 1<posAdv[0]<11 or not 1<posAdv[1]<11:
                        test = False
                    elif self[posAdv] * self[pos] >0:
                        test = False
                    elif self[posAdv] * self[pos] <0 and not self[x+(i+1)*e[0],y+(i+1)*e[1]]:
                        return True
        return False
    
    def kill(self):
        """
        Fonction qui saute un pion. Met également à jours les attributs
        de la classe.

        Returns
        -------
        None.
        
        """
        if self[self.posKill]<0:
            self.pionLeftBlack -=1
        elif self[self.posKill]>0:
            self.pionLeftWhite -=1
        self[self.posKill] = 0
        self.posKill = None
        

    #%% Fonction de tour
    def calculatePion(self):
        """
        Calcul le nombre de pion restant et met à jours les compteurs.

        Returns
        -------
        None.

        """
        self.pionLeftWhite = sum(sum(self[1:-1,1:-1]>0))
        self.pionLeftBlack = sum(sum(self[1:-1,1:-1]<0))
        
    def continueTour(self, posTo):
        """
        Indique si le tour doit continuer ou non.
        A utilisé après un déplacement.
        ----------
        Parameters
        ----------
        None.
        
        Returns
        -------
        Bool
            la valeur booléenne corespondant à la fin d'un tour.
            True -> le tour continue.
            False -> le tour est fini.
        """
        if self.isKill and self.isKillPossible(posTo):
            res = True
        else: 
            res = False
            self.posPostKill = None
        self.isKill, self.posKill= False, None
        return res

    def endOfGame(self):
        """
        Indique si la partie est finie ou non.
        
        Returns
        -------
        Bool
            la valeur booléenne corespondant à la fin de partie.
            True -> la partie est finie.
            False -> la partie n'est pas finie.
        """
        self.calculatePion()
        return not self.pionLeftWhite or not self.pionLeftBlack

#%% Fonction chargement de partie
    def charger(self):
        """
        Réinitialise les atributs de classe en cas de chargement 
        d'une sauvegarde'

        Returns
        -------
        None.
        """
        self.calculatePion()
        self.posPostKill = None
        self.posKill = None
        self.isKill = False
        
### END OF FILE