# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:23:29 2020

Version: 1.0

@author: GLR & PRT
"""

import unittest

from player import Player, AiPlayer, HumanPlayer
from grid import Grid


lvl = 2
class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.playerAiN = AiPlayer('noir',lvl)
        self.playerAiB = AiPlayer('blanc', lvl)
        self.playerHuN = HumanPlayer('noir')
        self.playerhuN = HumanPlayer('blanc')
        
    def testInitPlayer(self):
        playerN = Player('noir')
        playerB = Player('blanc')
        self.assertIsInstance(playerN, Player)
        self.assertEqual(playerN.color, -1)
        self.assertEqual(playerB.color, 1)
    
    def testInitHuman(self):
        player1 = HumanPlayer('noir')
        self.assertIsInstance(player1, (Player, HumanPlayer))
        self.assertEqual(player1.type,'player')
        self.assertEqual(player1.color, -1)
    
    def testInitAi(self):
        self.assertIsInstance(self.playerAiB, (Player, AiPlayer))
        self.assertEqual(self.playerAiB.type,'ai')
        self.assertEqual(self.playerAiB.color, 1)
        self.assertEqual(self.playerAiB.level, lvl)
        self.assertIsNone(self.playerAiB.grid)
               
    def testMoveAi(self):
        grid = Grid()
        self.playerAiN.updateGrid(grid)
        self.assertIn(self.playerAiN.askMove(),self.playerAiN.actionPossible(grid,-1))