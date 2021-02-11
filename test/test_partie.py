# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:09:01 2020

Version: 1.0

@author: GLR & PRT
"""

import unittest

from partie import Partie

class TestPartie(unittest.TestCase):
    
    def setUp(self):
        self.partie = Partie()
    
    def testinit(self):
        self.assertIsInstance(self.partie, Partie)
        self.assertEqual(self.partie.ialvl, 2)
        self.assertEqual(self.partie.colorTour, 1)
        self.assertEqual(self.partie.nbrTour, 1)
        self.assertTrue(self.partie.play)
        self.assertIsNone(self.partie.winer)
        
    def testTour(self):
        self.assertEqual(self.partie.colorTour, 1)
        self.partie.endOfTour()
        self.assertEqual(self.partie.colorTour, -1)
    
    def testCurentPlayer(self):
        self.assertEqual(self.partie.currentPlayer(), self.partie.player[self.partie.colorTour])
        self.assertEqual(self.partie.currentPlayerType(), self.partie.player[self.partie.colorTour].type)
        self.assertEqual(self.partie.nextPlayer(), self.partie.player[self.partie.colorTour*-1])
    
    def testEndOfGame(self):
        self.partie.grid.pionLeftWhite = 0
        self.partie.continueGame()
        self.assertFalse(self.partie.play)
        self.partie.whoWin()
        self.partie.endOfGame()
        self.assertFalse(self.partie.play)
        self.assertEqual(self.partie.winer, 'Noir')
        self.partie.grid.pionLeftBlack = 0
        self.partie.grid.pionLeftWhite = 20
        self.partie.continueGame()
        self.assertFalse(self.partie.play)
        self.partie.whoWin()
        self.partie.endOfGame()
        self.assertFalse(self.partie.play)
        self.assertEqual(self.partie.winer, 'Blanc')
    
    def testSetPlayer(self):
        self.partie.playerVSplayer()
        self.assertEqual(self.partie.player[1].type, 'player')
        self.assertEqual(self.partie.player[-1].type, 'player')
        self.partie.playerVSia(side=1)
        self.assertEqual(self.partie.player[1].type, 'player')
        self.assertEqual(self.partie.player[-1].type, 'ai')