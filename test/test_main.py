# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:09:42 2020

Version: 1.0

@author: GLR & PRT
"""

import unittest

from main import Window
import PyQt5


class TestInterface(unittest.TestCase):
    
    def setUp(self):
        self.win = Window()
    
    def testInit(self):
        self.assertIsInstance(self.win, (Window, PyQt5.QtWidgets.QMainWindow))
        self.assertTrue(self.win.partie.play)
        self.assertIsNone(self.win.posFrom)
        self.assertIsNone(self.win.posTo)
        
    def testTourHumain(self):
        self.win.posFrom = (5,5)
        self.win.posTo = (4,4)
        self.win.unTourHuman()
        self.assertIsNone(self.win.posFrom)
        self.assertIsNone(self.win.posTo)
        
    def testTourAi(self):
        self.win.partie.playerVSia(side=0)
        self.win.posFrom = (5,5)
        self.win.posTo = (4,4)
        self.win.unTourAi()
        self.assertIsNone(self.win.posFrom)
        self.assertIsNone(self.win.posTo)
