# -*- coding: utf-8 -*-
"""
Created on Sun May 31 14:45:29 2020

Version: 1.0

@author: GLR & PRT
"""

import unittest
import os

loader = unittest.TestLoader()

start_dir = os.getcwd()+'/test'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)