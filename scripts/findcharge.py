#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-13 04:40:53 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import re
import sys, os

################################################################################################################################################
'''
User Inputs
'''
ROOTPrefix = sys.argv[1]
runNum = sys.argv[2]
MaxEvent=sys.argv[3]

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 

proc_root = lt.Root(os.path.realpath(__file__)).setup_ana()
p = proc_root[2] # Dictionary of pathing variables

# Add this to all files for more dynamic pathing
UTILPATH = p["UTILPATH"]

################################################################################################################################################

# Open report file to grab prescale values and tracking efficiency
report = UTILPATH+"/REPORT_OUTPUT/Analysis/General/%s_%s_%s.report" % (ROOTPrefix,runNum,MaxEvent)
#report = UTILPATH+"/REPORT_OUTPUT/Analysis/HeeP/%s_%s_%s.report" % (ROOTPrefix,runNum,MaxEvent)

with open(report) as f:
    # Search for keywords, then save as value in dictionary
    for line in f:
        data = line.split(':')
        if 'BCM1_Beam_Cut_Charge' in data[0]:
            charge = int(re.sub("\D","","%s" % data[1]))
print(charge)
