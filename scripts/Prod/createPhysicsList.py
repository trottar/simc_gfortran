#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-12-26 13:02:22 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import sys, os

################################################################################################################################################
'''
User Inputs
'''

Q2 = sys.argv[1].replace("p",".")
POL = sys.argv[2]
EPSVAL = sys.argv[3]
TMIN = sys.argv[4]
TMAX = sys.argv[5]
NumtBins = sys.argv[6]
Kset = sys.argv[7]

runNumRight = sys.argv[8].split(" ")
runNumLeft = sys.argv[9].split(" ")
runNumCenter = sys.argv[10].split(" ")

pThetaValRight = sys.argv[11].split(" ")
pThetaValLeft = sys.argv[12].split(" ")
pThetaValCenter = sys.argv[13].split(" ")

EbeamValRight = sys.argv[14].split(" ")
EbeamValLeft = sys.argv[15].split(" ")
EbeamValCenter = sys.argv[16].split(" ")

EffValRight = sys.argv[17].split(" ")
EffValLeft = sys.argv[18].split(" ")
EffValCenter = sys.argv[19].split(" ")
EffErrRight = sys.argv[20].split(" ")
EffErrLeft = sys.argv[21].split(" ")
EffErrCenter = sys.argv[22].split(" ")

ChargeValRight = sys.argv[23].split(" ")
ChargeValLeft = sys.argv[24].split(" ")
ChargeValCenter = sys.argv[25].split(" ")
ChargeErrRight = sys.argv[26].split(" ")
ChargeErrLeft = sys.argv[27].split(" ")
ChargeErrCenter = sys.argv[28].split(" ")

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''
# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
UTILPATH=lt.UTILPATH

################################################################################################################################################

thpq_right = -abs(float(pThetaValCenter[0])-float(pThetaValRight[0]))
thpq_left = abs(float(pThetaValCenter[0])-float(pThetaValLeft[0]))
thpq_center = 0.000

# Open a file in write mode
with open('physics_lists/list.settings', 'w') as f:
    # Write the value of the variable to the file
    f.write("{} {} {} {:.3f} {} {} {} {}\n".format(POL,Q2,EPSVAL,thpq_right,TMIN,TMAX,NumtBins,Kset))
    f.write("{} {} {} {:.3f} {} {} {} {}\n".format(POL,Q2,EPSVAL,thpq_left,TMIN,TMAX,NumtBins,Kset))
    f.write("{} {} {} {:.3f} {} {} {} {}\n".format(POL,Q2,EPSVAL,thpq_center,TMIN,TMAX,NumtBins,Kset))

# Open a file in write mode
with open('physics_lists/lists/list.%s_%s' % (Q2.replace(".",""),EPSVAL.replace("0.","")), 'w') as f:
    # Write the value of the variable to the file
    for i,thpq in enumerate(EbeamValRight):
        f.write("{} {} {} {} {} {:.5f} {} {}\n".format(runNumRight[i],Q2,EbeamValRight[i],ChargeValRight[i],ChargeErrRight[i],EffValRight[i],EffErrRight[i],EPSVAL))
    for i,thpq in enumerate(EbeamValLeft):
        f.write("{} {} {} {} {} {:.5f} {} {}\n".format(runNumLeft[i],Q2,EbeamValLeft[i],ChargeValLeft[i],ChargeErrLeft[i],EffValLeft[i],EffErrLeft[i],EPSVAL))
    for i,thpq in enumerate(EbeamValCenter):
        f.write("{} {} {} {} {} {:.5f} {} {}\n".format(runNumCenter[i],Q2,EbeamValCenter[i],ChargeValCenter[i],ChargeErrCenter[i],EffValCenter[i],EffErrCenter[i],EPSVAL)) 
