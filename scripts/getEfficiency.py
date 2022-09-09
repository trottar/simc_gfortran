#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-09-09 00:53:45 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import sys,os

runNum = sys.argv[1]
efficiency_table = sys.argv[2]

###############################################################################################################################################

'''
ltsep package import and pathing definitions
'''

# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
UTILPATH=lt.UTILPATH

################################################################################################################################################
# Grab and calculate efficiency 

from getDataTable import calculate_efficiency

tot_efficiency = calculate_efficiency(runNum,efficiency_table)

################################################################################################################################################

print(tot_efficiency)
