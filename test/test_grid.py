# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:23:29 2020

Version: 1.0

@author: GLR & PRT
"""

import unittest

from grid import Grid
import numpy as np

class TestGrid(unittest.TestCase):
    
    def setUp(self):
        self.grid = Grid()
            
    def testInitGrid(self):
        self.assertIsInstance(self.grid, (Grid, np.ndarray))   
        self.assertEqual(self.grid.pionLeftBlack, 20)
        self.assertEqual(self.grid.pionLeftWhite, 20)
        self.assertIsNone(self.grid.posPostKill)
        self.assertIsNone(self.grid.posKill)
        self.assertFalse(self.grid.isKill)
    
    def testAllowMove(self):
        self.assertTrue(self.grid.allowMove(1,(7,4),(6,5)))
        self.assertTrue(self.grid.allowMove(-1,(4,7),(5,6)))
        self.assertFalse(self.grid.allowMove(-1,(7,4),(6,5)))
        self.assertFalse(self.grid.allowMove(-1,(7,5),(6,5)))
    
    def testCheckForDame(self):
        self.grid[1,5]=1
        self.grid[10,5]=-1
        self.grid.checkForDames ()
        self.assertEqual(self.grid[1,5], 2)
        self.assertEqual(self.grid[10,5], -2)
    
    def testTour(self):
        self.grid.move((7,4),(6,5))
        self.assertEqual(self.grid[7,4],0)
        self.assertEqual(self.grid[6,5],1)
        self.grid.move((4,7),(5,6))
        self.assertEqual(self.grid[4,7],0)
        self.assertEqual(self.grid[5,6],-1)
        
        #testkill
        self.grid.allowMove(1,(6,5),(4,7))
        self.grid.move((6,5),(4,7))
        self.assertEqual(self.grid[6,5],0)
        self.assertEqual(self.grid[5,6],0)
        self.assertEqual(self.grid[4,7],1)
        self.assertEqual(self.grid.pionLeftBlack, 19)
        self.assertTrue(self.grid.isKill)
        
        #test continue 
        self.assertFalse(self.grid.continueTour((4,7)))
        self.grid[2,9]=0
        self.grid.isKill = True
        self.assertTrue(self.grid.continueTour((4,7)))
               
    def testEndOfGame(self):
        self.assertFalse(self.grid.endOfGame())
        self.grid[1:-1,1:-1]=0
        self.assertTrue(self.grid.endOfGame())
        self.grid[5,5] = 1
        self.assertTrue(self.grid.endOfGame())
        self.grid[5,5] = -1
        self.assertTrue(self.grid.endOfGame())
        

