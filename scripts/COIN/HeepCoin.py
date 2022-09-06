#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-09-06 00:13:56 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

###################################################################################################################################################

# Import relevant packages
import uproot as up
import numpy as np
import root_numpy as rnp
import pandas as pd
import root_pandas as rpd
import ROOT
import scipy
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import sys, math, os, subprocess
import array
from ROOT import TCanvas, TColor, TGaxis, TH1F, TH2F, TPad, TStyle, gStyle, gPad, TGaxis, TLine, TMath, TPaveText, TArc, TGraphPolar 
from ROOT import kBlack, kBlue, kRed
from functools import reduce

##################################################################################################################################################

# Check the number of arguments provided to the script
if len(sys.argv)-1!=11:
    print("!!!!! ERROR !!!!!\n Expected 11 arguments\n Usage is with - KIN OutDATAFilename.root data_charge data_efficiency OutDUMMYFilename.root dummy_charge dummy_efficiency InSIMCFilename OutFullAnalysisFilename \n!!!!! ERROR !!!!!")
    sys.exit(1)

##################################################################################################################################################

# Input params
heep_kinematics = sys.argv[1]
InDATAFilename = sys.argv[2]
data_charge = int(sys.argv[3])/1000
InData_efficiency = sys.argv[4]
data_runNums = sys.argv[5]
InDUMMYFilename = sys.argv[6]
dummy_charge = int(sys.argv[7])/1000
InDummy_efficiency = sys.argv[8]
dummy_runNums = sys.argv[9]
InSIMCFilename = sys.argv[10]
OutFilename = sys.argv[11]

try:
    data_efficiency = sum([float(i) for i in InData_efficiency.split(" ")])/len([float(i) for i in InData_efficiency.split(" ")])
    print("\n\ndata_efficiency=",data_efficiency)

    dummy_efficiency = sum([float(i) for i in InDummy_efficiency.split(" ")])/len([float(i) for i in InDummy_efficiency.split(" ")])
    print("dummy_efficiency=",dummy_efficiency)
    
except ValueError:
    print("\nError: Invalid efficiency value found...")
    sys.exit(1)

G_data_eff = ROOT.TGraph(len(InData_efficiency.split(' ')), np.array([float(x) for x in data_runNums.split(' ')]),np.array([float(x) for x in InData_efficiency.split(' ')]))
G_dummy_eff = ROOT.TGraph(len(InDummy_efficiency.split(' ')), np.array([float(x) for x in dummy_runNums.split(' ')]),np.array([float(x) for x in InDummy_efficiency.split(' ')]))

###############################################################################################################################################
ROOT.gROOT.SetBatch(ROOT.kTRUE) # Set ROOT to batch mode explicitly, does not splash anything to screen
###############################################################################################################################################

'''
ltsep package import and pathing definitions
'''

# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__),"Plot_SimcCoin")

# Add this to all files for more dynamic pathing
USER=lt.USER # Grab user info for file finding
HOST=lt.HOST
REPLAYPATH=lt.REPLAYPATH
UTILPATH=lt.UTILPATH
SIMCPATH=lt.SIMCPATH
ANATYPE=lt.ANATYPE
OUTPATH=lt.OUTPATH

rootFile = OUTPATH+"/"+InDATAFilename
rootFile_DUMMY = OUTPATH+"/"+InDUMMYFilename
rootFile_SIMC = OUTPATH+"/"+InSIMCFilename

foutname = OUTPATH+"/" + OutFilename + ".root"
fouttxt  = OUTPATH+"/" + OutFilename + ".txt"
outputpdf  = OUTPATH+"/" + OutFilename + ".pdf"

###############################################################################################################################################

# Grabs simc number of events and weight
simc_hist = "%s/OUTPUT/Analysis/HeeP/%s" % (SIMCPATH,InSIMCFilename.replace('.root','.hist'))
f_simc = open(simc_hist)
for line in f_simc:
    print(line)
    if "Ngen" in line:
        val = line.split("=")
        simc_nevents = int(val[1])
    if "normfac" in line:
        val = line.split("=")
        simc_normfactor = float(val[1])
if 'simc_nevents' and 'simc_normfactor' in locals():
    print('\n\nsimc_nevents = ',simc_nevents,'\nsimc_normfactor = ',simc_normfactor,'\n\n')
    print('\n\ndata_charge = ',data_charge,'\ndummy_charge = ',dummy_charge,'\n\n')
else:
    print("ERROR: Invalid simc hist file %s" % simc_hist)
    sys.exit(1)

###############################################################################################################################################

'''
# Grab windows for random subtraction

if "10p6" in heep_kinematics:
    runNum = 4827 # First run number of 10p6 coin heep setting
if "8p2" in heep_kinematics:
    runNum = 7974 # First run number of 8p2 coin heep setting
if "6p2" in heep_kinematics:
    runNum = 7866 # First run number of 6p2 coin heep setting
if "4p9" in heep_kinematics:
    runNum = 6881 # First run number of 4p9 coin heep setting
if "3p8" in heep_kinematics:
    runNum = 6634 # First run number of 3p8 coin heep setting        

try:
    runNum
except:
    print("ERROR: No valid run number for this setting!")
    sys.exit(1)

# Section for grabing Prompt/Random selection parameters from PARAM file
PARAMPATH = "%s/DB/PARAM" % UTILPATH
print("Running as %s on %s, hallc_replay_lt path assumed as %s" % (USER[1], HOST[1], SIMCPATH))
TimingCutFile = "%s/Timing_Parameters.csv" % PARAMPATH # This should match the param file actually being used!
TimingCutf = open(TimingCutFile)
try:
    TimingCutFile
except NameError:
    print("!!!!! ERRROR !!!!!\n One (or more) of the cut files not found!\n!!!!! ERRORR !!!!!")
    sys.exit(2)
print("Reading timing cuts from %s" % TimingCutFile)
PromptWindow = [0, 0]
RandomWindows = [0, 0, 0, 0]
linenum = 0 # Count line number we're on
TempPar = -1 # To check later
for line in TimingCutf: # Read all lines in the cut file
    linenum += 1 # Add one to line number at start of loop
    if(linenum > 1): # Skip first line
        line = line.partition('#')[0] # Treat anything after a # as a comment and ignore it
        line = line.rstrip()
        array = line.split(",") # Convert line into an array, anything after a comma is a new entry 
        if(int(runNum) in range (int(array[0]), int(array[1])+1)): # Check if run number for file is within any of the ranges specified in the cut file
            TempPar += 2 # If run number is in range, set to non -1 value
            BunchSpacing = float(array[2])
            CoinOffset = float(array[3]) # Coin offset value
            nSkip = float(array[4]) # Number of random windows skipped 
            nWindows = float(array[5]) # Total number of random windows
            PromptPeak = float(array[6]) # Pion CT prompt peak positon 
TimingCutf.close() # After scanning all lines in file, close file

if(TempPar == -1): # If value is still -1, run number provided din't match any ranges specified so exit 
    print("!!!!! ERROR !!!!!\n Run number specified does not fall within a set of runs for which cuts are defined in %s\n!!!!! ERROR !!!!!" % TimingCutFile)
    sys.exit(3)
elif(TempPar > 1):
    print("!!! WARNING!!! Run number was found within the range of two (or more) line entries of %s !!! WARNING !!!" % TimingCutFile)
    print("The last matching entry will be treated as the input, you should ensure this is what you want")

# From our values from the file, reconstruct our windows 
PromptWindow[0] = PromptPeak - (BunchSpacing/2) - CoinOffset
PromptWindow[1] = PromptPeak + (BunchSpacing/2) + CoinOffset
RandomWindows[0] = PromptPeak - (BunchSpacing/2) - CoinOffset - (nSkip*BunchSpacing) - ((nWindows/2)*BunchSpacing)
RandomWindows[1] = PromptPeak - (BunchSpacing/2) - CoinOffset - (nSkip*BunchSpacing)
RandomWindows[2] = PromptPeak + (BunchSpacing/2) + CoinOffset + (nSkip*BunchSpacing)
RandomWindows[3] = PromptPeak + (BunchSpacing/2) + CoinOffset + (nSkip*BunchSpacing) + ((nWindows/2)*BunchSpacing)

'''

################################################################################################################################################

InFile_DATA = ROOT.TFile.Open(rootFile, "OPEN")
InFile_DUMMY = ROOT.TFile.Open(rootFile_DUMMY, "OPEN")
InFile_SIMC = ROOT.TFile.Open(rootFile_SIMC, "READ")

#TBRANCH_DATA  = InFile_DATA.Get("Cut_Proton_Events_All")
TBRANCH_DATA  = InFile_DATA.Get("Uncut_Proton_Events")
nEntries_TBRANCH_DATA  = TBRANCH_DATA.GetEntries()
#TBRANCH_DUMMY  = InFile_DUMMY.Get("Cut_Proton_Events_All")
TBRANCH_DUMMY  = InFile_DUMMY.Get("Uncut_Proton_Events")
nEntries_TBRANCH_DUMMY  = TBRANCH_DUMMY.GetEntries()
TBRANCH_SIMC  = InFile_SIMC.Get("h10")
nEntries_TBRANCH_SIMC  = TBRANCH_SIMC.GetEntries()

################################################################################################################################################

H_hsdelta_DATA  = ROOT.TH1D("H_hsdelta_DATA","HMS Delta", 200, -20.0, 20.0)
#H_hsdelta_DATA_rand  = ROOT.TH1D("H_hsdelta_DATA_rand","HMS Delta", 200, -20.0, 20.0)
H_hsdelta_DUMMY  = ROOT.TH1D("H_hsdelta_DUMMY","HMS Delta", 200, -20.0, 20.0)
#H_hsdelta_DUMMY_rand  = ROOT.TH1D("H_hsdelta_DUMMY_rand","HMS Delta", 200, -20.0, 20.0)
H_hsdelta_SIMC  = ROOT.TH1D("H_hsdelta_SIMC","HMS Delta", 200, -20.0, 20.0)

H_hsxptar_DATA  = ROOT.TH1D("H_hsxptar_DATA","HMS xptar", 200, -0.1, 0.1)
#H_hsxptar_DATA_rand  = ROOT.TH1D("H_hsxptar_DATA_rand","HMS xptar", 200, -0.1, 0.1)
H_hsxptar_DUMMY  = ROOT.TH1D("H_hsxptar_DUMMY","HMS xptar", 200, -0.1, 0.1)
#H_hsxptar_DUMMY_rand  = ROOT.TH1D("H_hsxptar_DUMMY_rand","HMS xptar", 200, -0.1, 0.1)
H_hsxptar_SIMC  = ROOT.TH1D("H_hsxptar_SIMC","HMS xptar", 200, -0.1, 0.1)

H_hsyptar_DATA  = ROOT.TH1D("H_hsyptar_DATA","HMS yptar", 200, -0.1, 0.1)
#H_hsyptar_DATA_rand  = ROOT.TH1D("H_hsyptar_DATA_rand","HMS yptar", 200, -0.1, 0.1)
H_hsyptar_DUMMY  = ROOT.TH1D("H_hsyptar_DUMMY","HMS yptar", 200, -0.1, 0.1)
#H_hsyptar_DUMMY_rand  = ROOT.TH1D("H_hsyptar_DUMMY_rand","HMS yptar", 200, -0.1, 0.1)
H_hsyptar_SIMC  = ROOT.TH1D("H_hsyptar_SIMC","HMS yptar", 200, -0.1, 0.1)

H_ssxfp_DATA    = ROOT.TH1D("H_ssxfp_DATA","SHMS xfp", 200, -25.0, 25.0)
#H_ssxfp_DATA_rand    = ROOT.TH1D("H_ssxfp_DATA_rand","SHMS xfp", 200, -25.0, 25.0)
H_ssxfp_DUMMY    = ROOT.TH1D("H_ssxfp_DUMMY","SHMS xfp", 200, -25.0, 25.0)
#H_ssxfp_DUMMY_rand    = ROOT.TH1D("H_ssxfp_DUMMY_rand","SHMS xfp", 200, -25.0, 25.0)
H_ssxfp_SIMC    = ROOT.TH1D("H_ssxfp_SIMC","SHMS xfp", 200, -25.0, 25.0)

H_ssyfp_DATA    = ROOT.TH1D("H_ssyfp_DATA","SHMS yfp", 200, -25.0, 25.0)
#H_ssyfp_DATA_rand    = ROOT.TH1D("H_ssyfp_DATA_rand","SHMS yfp", 200, -25.0, 25.0)
H_ssyfp_DUMMY    = ROOT.TH1D("H_ssyfp_DUMMY","SHMS yfp", 200, -25.0, 25.0)
#H_ssyfp_DUMMY_rand    = ROOT.TH1D("H_ssyfp_DUMMY_rand","SHMS yfp", 200, -25.0, 25.0)
H_ssyfp_SIMC    = ROOT.TH1D("H_ssyfp_SIMC","SHMS yfp", 200, -25.0, 25.0)

H_ssxpfp_DATA   = ROOT.TH1D("H_ssxpfp_DATA","SHMS xpfp", 200, -0.09, 0.09)
#H_ssxpfp_DATA_rand   = ROOT.TH1D("H_ssxpfp_DATA_rand","SHMS xpfp", 200, -0.09, 0.09)
H_ssxpfp_DUMMY   = ROOT.TH1D("H_ssxpfp_DUMMY","SHMS xpfp", 200, -0.09, 0.09)
#H_ssxpfp_DUMMY_rand   = ROOT.TH1D("H_ssxpfp_DUMMY_rand","SHMS xpfp", 200, -0.09, 0.09)
H_ssxpfp_SIMC   = ROOT.TH1D("H_ssxpfp_SIMC","SHMS xpfp", 200, -0.09, 0.09)

H_ssypfp_DATA   = ROOT.TH1D("H_ssypfp_DATA","SHMS ypfp", 200, -0.05, 0.04)
#H_ssypfp_DATA_rand   = ROOT.TH1D("H_ssypfp_DATA_rand","SHMS ypfp", 200, -0.05, 0.04)
H_ssypfp_DUMMY   = ROOT.TH1D("H_ssypfp_DUMMY","SHMS ypfp", 200, -0.05, 0.04)
#H_ssypfp_DUMMY_rand   = ROOT.TH1D("H_ssypfp_DUMMY_rand","SHMS ypfp", 200, -0.05, 0.04)
H_ssypfp_SIMC   = ROOT.TH1D("H_ssypfp_SIMC","SHMS ypfp", 200, -0.05, 0.04)

H_hsxfp_DATA    = ROOT.TH1D("H_hsxfp_DATA","HMS xfp", 200, -40.0, 40.0)
#H_hsxfp_DATA_rand    = ROOT.TH1D("H_hsxfp_DATA_rand","HMS xfp", 200, -40.0, 40.0)
H_hsxfp_DUMMY    = ROOT.TH1D("H_hsxfp_DUMMY","HMS xfp", 200, -40.0, 40.0)
#H_hsxfp_DUMMY_rand    = ROOT.TH1D("H_hsxfp_DUMMY_rand","HMS xfp", 200, -40.0, 40.0)
H_hsxfp_SIMC    = ROOT.TH1D("H_hsxfp_SIMC","HMS xfp", 200, -40.0, 40.0)

H_hsyfp_DATA    = ROOT.TH1D("H_hsyfp_DATA","HMS yfp", 200, -20.0, 20.0)
#H_hsyfp_DATA_rand    = ROOT.TH1D("H_hsyfp_DATA_rand","HMS yfp", 200, -20.0, 20.0)
H_hsyfp_DUMMY    = ROOT.TH1D("H_hsyfp_DUMMY","HMS yfp", 200, -20.0, 20.0)
#H_hsyfp_DUMMY_rand    = ROOT.TH1D("H_hsyfp_DUMMY_rand","HMS yfp", 200, -20.0, 20.0)
H_hsyfp_SIMC    = ROOT.TH1D("H_hsyfp_SIMC","HMS yfp", 200, -20.0, 20.0)

H_hsxpfp_DATA   = ROOT.TH1D("H_hsxpfp_DATA","HMS xpfp", 200, -0.09, 0.05)
#H_hsxpfp_DATA_rand   = ROOT.TH1D("H_hsxpfp_DATA_rand","HMS xpfp", 200, -0.09, 0.05)
H_hsxpfp_DUMMY   = ROOT.TH1D("H_hsxpfp_DUMMY","HMS xpfp", 200, -0.09, 0.05)
#H_hsxpfp_DUMMY_rand   = ROOT.TH1D("H_hsxpfp_DUMMY_rand","HMS xpfp", 200, -0.09, 0.05)
H_hsxpfp_SIMC   = ROOT.TH1D("H_hsxpfp_SIMC","HMS xpfp", 200, -0.09, 0.05)

H_hsypfp_DATA   = ROOT.TH1D("H_hsypfp_DATA","HMS ypfp", 200, -0.05, 0.04)
#H_hsypfp_DATA_rand   = ROOT.TH1D("H_hsypfp_DATA_rand","HMS ypfp", 200, -0.05, 0.04)
H_hsypfp_DUMMY   = ROOT.TH1D("H_hsypfp_DUMMY","HMS ypfp", 200, -0.05, 0.04)
#H_hsypfp_DUMMY_rand   = ROOT.TH1D("H_hsypfp_DUMMY_rand","HMS ypfp", 200, -0.05, 0.04)
H_hsypfp_SIMC   = ROOT.TH1D("H_hsypfp_SIMC","HMS ypfp", 200, -0.05, 0.04)

H_ssdelta_DATA  = ROOT.TH1D("H_ssdelta_DATA","SHMS delta", 200, -20.0, 20.0)
#H_ssdelta_DATA_rand  = ROOT.TH1D("H_ssdelta_DATA_rand","SHMS delta", 200, -20.0, 20.0)
H_ssdelta_DUMMY  = ROOT.TH1D("H_ssdelta_DUMMY","SHMS delta", 200, -20.0, 20.0)
#H_ssdelta_DUMMY_rand  = ROOT.TH1D("H_ssdelta_DUMMY_rand","SHMS delta", 200, -20.0, 20.0)
H_ssdelta_SIMC  = ROOT.TH1D("H_ssdelta_SIMC","SHMS delta", 200, -20.0, 20.0)

H_ssxptar_DATA  = ROOT.TH1D("H_ssxptar_DATA","SHMS xptar", 200, -0.1, 0.1)
#H_ssxptar_DATA_rand  = ROOT.TH1D("H_ssxptar_DATA_rand","SHMS xptar", 200, -0.1, 0.1)
H_ssxptar_DUMMY  = ROOT.TH1D("H_ssxptar_DUMMY","SHMS xptar", 200, -0.1, 0.1)
#H_ssxptar_DUMMY_rand  = ROOT.TH1D("H_ssxptar_DUMMY_rand","SHMS xptar", 200, -0.1, 0.1)
H_ssxptar_SIMC  = ROOT.TH1D("H_ssxptar_SIMC","SHMS xptar", 200, -0.1, 0.1)

H_ssyptar_DATA  = ROOT.TH1D("H_ssyptar_DATA","SHMS yptar", 200, -0.04, 0.04)
#H_ssyptar_DATA_rand  = ROOT.TH1D("H_ssyptar_DATA_rand","SHMS yptar", 200, -0.04, 0.04)
H_ssyptar_DUMMY  = ROOT.TH1D("H_ssyptar_DUMMY","SHMS yptar", 200, -0.04, 0.04)
#H_ssyptar_DUMMY_rand  = ROOT.TH1D("H_ssyptar_DUMMY_rand","SHMS yptar", 200, -0.04, 0.04)
H_ssyptar_SIMC  = ROOT.TH1D("H_ssyptar_SIMC","SHMS yptar", 200, -0.04, 0.04)

H_q_DATA        = ROOT.TH1D("H_q_DATA","q", 200, 0.0, 10.0)
#H_q_DATA_rand        = ROOT.TH1D("H_q_DATA_rand","q", 200, 0.0, 10.0)
H_q_DUMMY        = ROOT.TH1D("H_q_DUMMY","q", 200, 0.0, 10.0)
#H_q_DUMMY_rand        = ROOT.TH1D("H_q_DUMMY_rand","q", 200, 0.0, 10.0)
H_q_SIMC        = ROOT.TH1D("H_q_SIMC","q", 200, 0.0, 10.0)

H_Q2_DATA       = ROOT.TH1D("H_Q2_DATA","Q2", 200, 0.0, 10.0)  
#H_Q2_DATA_rand       = ROOT.TH1D("H_Q2_DATA_rand","Q2", 200, 0.0, 10.0)  
H_Q2_DUMMY       = ROOT.TH1D("H_Q2_DUMMY","Q2", 200, 0.0, 10.0)  
#H_Q2_DUMMY_rand       = ROOT.TH1D("H_Q2_DUMMY_rand","Q2", 200, 0.0, 10.0)  
H_Q2_SIMC       = ROOT.TH1D("H_Q2_SIMC","Q2", 200, 0.0, 10.0)  

H_epsilon_DATA  = ROOT.TH1D("H_epsilon_DATA","epsilon", 200, 0.5, 1.0)
#H_epsilon_DATA_rand  = ROOT.TH1D("H_epsilon_DATA_rand","epsilon", 200, 0.5, 1.0)
H_epsilon_DUMMY  = ROOT.TH1D("H_epsilon_DUMMY","epsilon", 200, 0.5, 1.0)
#H_epsilon_DUMMY_rand  = ROOT.TH1D("H_epsilon_DUMMY_rand","epsilon", 200, 0.5, 1.0)
H_epsilon_SIMC  = ROOT.TH1D("H_epsilon_SIMC","epsilon", 200, 0.5, 1.0)

H_MMp2_DATA  = ROOT.TH1D("H_MMp2_DATA","(MM)^{2}_{p}", 200, -0.01, 0.01)
#H_MMp2_DATA_rand  = ROOT.TH1D("H_MMp2_DATA_rand","(MM)^{2}_{p}", 200, -0.01, 0.01)
H_MMp2_DUMMY  = ROOT.TH1D("H_MMp2_DUMMY","(MM)^{2}_{p}", 200, -0.01, 0.01)
#H_MMp2_DUMMY_rand  = ROOT.TH1D("H_MMp2_DUMMY_rand","(MM)^{2}_{p}", 200, -0.01, 0.01)
H_MMp2_SIMC  = ROOT.TH1D("H_MMp2_SIMC","(MM)^{2}_{p}", 200, -0.01, 0.01)

H_th_DATA  = ROOT.TH1D("H_th_DATA","X' tar", 200, -0.1, 0.1)
#H_th_DATA_rand  = ROOT.TH1D("H_th_DATA_rand","X' tar", 200, -0.1, 0.1)
H_th_DUMMY  = ROOT.TH1D("H_th_DUMMY","X' tar", 200, -0.1, 0.1)
#H_th_DUMMY_rand  = ROOT.TH1D("H_th_DUMMY_rand","X' tar", 200, -0.1, 0.1)
H_th_SIMC  = ROOT.TH1D("H_th_SIMC","X' tar", 200, -0.1, 0.1)

H_ph_DATA  = ROOT.TH1D("H_ph_DATA","Y' tar", 200, -0.1, 0.1)
#H_ph_DATA_rand  = ROOT.TH1D("H_ph_DATA_rand","Y' tar", 200, -0.1, 0.1)
H_ph_DUMMY  = ROOT.TH1D("H_ph_DUMMY","Y' tar", 200, -0.1, 0.1)
#H_ph_DUMMY_rand  = ROOT.TH1D("H_ph_DUMMY_rand","Y' tar", 200, -0.1, 0.1)
H_ph_SIMC  = ROOT.TH1D("H_ph_SIMC","Y' tar", 200, -0.1, 0.1)

H_pmiss_DATA  = ROOT.TH1D("H_pmiss_DATA","pmiss", 200, -0.1, 0.1)
#H_pmiss_DATA_rand  = ROOT.TH1D("H_pmiss_DATA_rand","pmiss", 200, -0.1, 0.1)
H_pmiss_DUMMY  = ROOT.TH1D("H_pmiss_DUMMY","pmiss", 200, -0.1, 0.1)
#H_pmiss_DUMMY_rand  = ROOT.TH1D("H_pmiss_DUMMY_rand","pmiss", 200, -0.1, 0.1)
H_pmiss_SIMC  = ROOT.TH1D("H_pmiss_SIMC","pmiss", 200, -0.1, 0.1)

H_emiss_DATA  = ROOT.TH1D("H_emiss_DATA","emiss", 200, -0.1, 0.1)
#H_emiss_DATA_rand  = ROOT.TH1D("H_emiss_DATA_rand","emiss", 200, -0.1, 0.1)
H_emiss_DUMMY  = ROOT.TH1D("H_emiss_DUMMY","emiss", 200, -0.1, 0.1)
#H_emiss_DUMMY_rand  = ROOT.TH1D("H_emiss_DUMMY_rand","emiss", 200, -0.1, 0.1)
H_emiss_SIMC  = ROOT.TH1D("H_emiss_SIMC","emiss", 200, -0.1, 0.1)

H_pmx_DATA  = ROOT.TH1D("H_pmx_DATA","pmx", 200, -0.1, 0.1)
#H_pmx_DATA_rand  = ROOT.TH1D("H_pmx_DATA_rand","pmx", 200, -0.1, 0.1)
H_pmx_DUMMY  = ROOT.TH1D("H_pmx_DUMMY","pmx", 200, -0.1, 0.1)
#H_pmx_DUMMY_rand  = ROOT.TH1D("H_pmx_DUMMY_rand","pmx", 200, -0.1, 0.1)
H_pmx_SIMC  = ROOT.TH1D("H_pmx_SIMC","pmx", 200, -0.1, 0.1)

H_pmy_DATA  = ROOT.TH1D("H_pmy_DATA","pmy ", 200, -0.1, 0.1)
#H_pmy_DATA_rand  = ROOT.TH1D("H_pmy_DATA_rand","pmy ", 200, -0.1, 0.1)
H_pmy_DUMMY  = ROOT.TH1D("H_pmy_DUMMY","pmy ", 200, -0.1, 0.1)
#H_pmy_DUMMY_rand  = ROOT.TH1D("H_pmy_DUMMY_rand","pmy ", 200, -0.1, 0.1)
H_pmy_SIMC  = ROOT.TH1D("H_pmy_SIMC","pmy", 200, -0.1, 0.1)

H_pmz_DATA  = ROOT.TH1D("H_pmz_DATA","pmz", 200, -0.1, 0.1)
#H_pmz_DATA_rand  = ROOT.TH1D("H_pmz_DATA_rand","pmz", 200, -0.1, 0.1)
H_pmz_DUMMY  = ROOT.TH1D("H_pmz_DUMMY","pmz", 200, -0.1, 0.1)
#H_pmz_DUMMY_rand  = ROOT.TH1D("H_pmz_DUMMY_rand","pmz", 200, -0.1, 0.1)
H_pmz_SIMC  = ROOT.TH1D("H_pmz_SIMC","pmz", 200, -0.1, 0.1)

H_W_DATA  = ROOT.TH1D("H_W_DATA","W ", 200, 0.7, 1.1)
#H_W_DATA_rand  = ROOT.TH1D("H_W_DATA_rand","W ", 200, 0.7, 1.1)
H_W_DUMMY  = ROOT.TH1D("H_W_DUMMY","W ", 200, 0.7, 1.1)
#H_W_DUMMY_rand  = ROOT.TH1D("H_W_DUMMY_rand","W ", 200, 0.7, 1.1)
H_W_SIMC  = ROOT.TH1D("H_W_SIMC","W", 200, 0.7, 1.1)

H_ct_ep_DATA = ROOT.TH1D("H_ct_ep_DATA", "Electron-Proton CTime", 200, -10, 10)
H_ct_ep_DUMMY = ROOT.TH1D("H_ct_ep_DUMMY", "Electron-Proton CTime", 200, -10, 10)
H_ct_ep_DATA_cut = ROOT.TH1D("H_ct_ep_DATA_cut", "Electron-Proton CTime (cut)", 200, -10, 10)
#H_ct_ep_DATA_cut_rand = ROOT.TH1D("H_ct_ep_DATA_cut_rand", "Electron-Proton CTime (cut)", 200, -10, 10)
H_ct_ep_DUMMY_cut = ROOT.TH1D("H_ct_ep_DUMMY_cut", "Electron-Proton CTime (cut)", 200, -10, 10)
#H_ct_ep_DUMMY_cut_rand = ROOT.TH1D("H_ct_ep_DUMMY_cut_rand", "Electron-Proton CTime (cut)", 200, -10, 10)

H_ct_ep_vs_H_MMp2_DATA = ROOT.TH2D("H_ct_ep_vs_H_MMp2_DATA","Electron-Proton CTime vs (MM)^{2}_{p}; e p Coin_Time; (MM)^{2}_{p}", 200, -10, 10, 200, -0.1, 0.1)
#H_ct_ep_vs_H_MMp2_DATA_rand = ROOT.TH2D("H_ct_ep_vs_H_MMp2_DATA_rand","Electron-Proton CTime vs (MM)^{2}_{p}; e p Coin_Time; (MM)^{2}_{p}", 200, -10, 10, 200, -0.1, 0.1)

H_emiss_vs_H_hsdelta_DATA = ROOT.TH2D("H_emiss_vs_H_hsdelta_DATA","Emiss vs HMS Delta;  Emiss; HMS Delta", 200, -0.1, 0.1, 200, -20.0, 20.0)
H_emiss_vs_H_ssdelta_DATA = ROOT.TH2D("H_emiss_vs_H_ssdelta_DATA","Emiss vs SHMS Delta;  Emiss; SHMS Delta", 200, -0.1, 0.1, 200, -20.0, 20.0)

H_pmiss_vs_H_hsdelta_DATA = ROOT.TH2D("H_pmiss_vs_H_hsdelta_DATA","Pmiss vs HMS Delta;  Pmiss; HMS Delta", 200, -0.1, 0.1, 200, -20.0, 20.0)
H_pmiss_vs_H_ssdelta_DATA = ROOT.TH2D("H_pmiss_vs_H_ssdelta_DATA","Pmiss vs SHMS Delta;  Pmiss; SHMS Delta", 200, -0.1, 0.1, 200, -20.0, 20.0)

################################################################################################################################################

H_cal_etotnorm_DATA = ROOT.TH1D("H_cal_etotnorm_DATA", "HMS Cal etotnorm", 200, 0.2, 1.8)
H_cer_npeSum_DATA = ROOT.TH1D("H_cer_npeSum_DATA", "HMS Cer Npe Sum", 200, 0, 30)

P_cal_etotnorm_DATA = ROOT.TH1D("P_cal_etotnorm_DATA", "SHMS Cal etotnorm", 200, 0, 1)
P_hgcer_npeSum_DATA = ROOT.TH1D("P_hgcer_npeSum_DATA", "SHMS HGCer Npe Sum", 200, 0, 50)
P_aero_npeSum_DATA = ROOT.TH1D("P_aero_npeSum_DATA", "SHMS Aero Npe Sum", 200, 0, 50)

H_cal_etotnorm_vs_H_cer_npeSum_DATA = ROOT.TH2D("H_cal_etotnorm_vs_H_cer_npeSum_DATA","HMS Cal etotnorm vs HMS Cer Npe Sum;  HMS Cal etotnorm; HMS Cer Npe Sum", 200, 0.2, 1.8, 200, 0, 30)
P_cal_etotnorm_vs_P_hgcer_npeSum_DATA = ROOT.TH2D("P_cal_etotnorm_vs_P_hgcer_npeSum_DATA","SHMS Cal etotnorm vs SHMS HGCer Npe Sum;  SHMS Cal etotnorm; SHMS HGCer Npe Sum", 200, 0, 1, 200, 0, 50)
P_cal_etotnorm_vs_P_aero_npeSum_DATA = ROOT.TH2D("P_cal_etotnorm_vs_P_aero_npeSum_DATA","SHMS Cal etotnorm vs SHMS Aero Npe Sum;  SHMS Cal etotnorm; SHMS Aero Npe Sum", 200, 0, 1, 200, 0, 50)
P_hgcer_npeSum_vs_P_aero_npeSum_DATA = ROOT.TH2D("P_hgcer_npeSum_vs_P_aero_npeSum_DATA","SHMS HGCer Npe Sum vs SHMS Aero Npe Sum;  SHMS HGCer Npe Sum; SHMS Aero Npe Sum", 200, 0, 50, 200, 0, 50)

################################################################################################################################################

for evt in TBRANCH_SIMC:

  # Define the acceptance cuts  

  # Select the cuts
  #HMS
  CUT1 = (evt.hsdelta >=-8.0) & (evt.hsdelta <=8.0)
  CUT2 = (evt.hsxptar >=-0.08) & (evt.hsxpfp <=0.08)
  CUT3 = (evt.hsyptar >=-0.045) & (evt.hsypfp <=0.045)

  #SHMS    
  CUT4 = (evt.ssdelta >=-10.0) & (evt.ssdelta <=20.0)
  CUT5 = (evt.ssxptar >=-0.06) & (evt.ssxpfp <=0.06)
  CUT6 = (evt.ssyptar >=-0.04) & (evt.ssypfp <=0.04)

  #........................................

  #Fill SIMC events
  if (CUT1 & CUT2 & CUT3 & CUT4 & CUT5 & CUT6):
    
      H_ssxfp_SIMC.Fill(evt.ssxfp, evt.Weight)
      H_ssyfp_SIMC.Fill(evt.ssyfp, evt.Weight)
      H_ssxpfp_SIMC.Fill(evt.ssxpfp, evt.Weight)
      H_ssypfp_SIMC.Fill(evt.ssypfp, evt.Weight)
      H_hsxfp_SIMC.Fill(evt.hsxfp, evt.Weight)
      H_hsyfp_SIMC.Fill(evt.hsyfp, evt.Weight)
      H_hsxpfp_SIMC.Fill(evt.hsxpfp, evt.Weight)
      H_hsypfp_SIMC.Fill(evt.hsypfp, evt.Weight)
      H_ssdelta_SIMC.Fill(evt.ssdelta, evt.Weight) 
      H_hsdelta_SIMC.Fill(evt.hsdelta, evt.Weight)	
      H_ssxptar_SIMC.Fill(evt.ssxptar, evt.Weight)
      H_ssyptar_SIMC.Fill(evt.ssyptar, evt.Weight)
      H_hsxptar_SIMC.Fill(evt.hsxptar, evt.Weight)	
      H_hsyptar_SIMC.Fill(evt.hsyptar, evt.Weight)	
      H_pmiss_SIMC.Fill(evt.Pm, evt.Weight)	
      H_emiss_SIMC.Fill(evt.Em, evt.Weight)	
      H_pmx_SIMC.Fill(evt.Pmx, evt.Weight)
      H_pmy_SIMC.Fill(evt.Pmy, evt.Weight)
      H_pmz_SIMC.Fill(evt.Pmz, evt.Weight)
      H_Q2_SIMC.Fill(evt.Q2, evt.Weight)
      H_W_SIMC.Fill(evt.W, evt.Weight)
      H_epsilon_SIMC.Fill(evt.epsilon, evt.Weight)
      H_MMp2_SIMC.Fill(pow(evt.Em, 2) - pow(evt.Pm, 2), evt.Weight)

for evt in TBRANCH_DATA:

  #CUTs Definations 
  SHMS_FixCut = (evt.P_hod_goodstarttime == 1) & (evt.P_dc_InsideDipoleExit == 1) # & P_hod_betanotrack > 0.5 & P_hod_betanotrack < 1.4
  SHMS_Acceptance = (evt.ssdelta>=-10.0) & (evt.ssdelta<=20.0) & (evt.ssxptar>=-0.06) & (evt.ssxptar<=0.06) & (evt.ssyptar>=-0.04) & (evt.ssyptar<=0.04)

  HMS_FixCut = (evt.H_hod_goodstarttime == 1) & (evt.H_dc_InsideDipoleExit == 1)
  HMS_Acceptance = (evt.hsdelta>=-8.0) & (evt.hsdelta<=8.0) & (evt.hsxptar>=-0.08) & (evt.hsxptar<=0.08) & (evt.hsyptar>=-0.045) & (evt.hsyptar<=0.045)       

  #........................................
  
  H_ct_ep_DATA.Fill(evt.CTime_epCoinTime_ROC1)
  
  if(HMS_FixCut & HMS_Acceptance & SHMS_FixCut & SHMS_Acceptance):

      H_ct_ep_vs_H_MMp2_DATA.Fill(evt.CTime_epCoinTime_ROC1, evt.MMp)
      H_ct_ep_DATA_cut.Fill(evt.CTime_epCoinTime_ROC1)

      H_emiss_vs_H_hsdelta_DATA.Fill(evt.emiss, evt.hsdelta)
      H_emiss_vs_H_ssdelta_DATA.Fill(evt.emiss, evt.ssdelta)
      H_pmiss_vs_H_hsdelta_DATA.Fill(evt.pmiss, evt.hsdelta)
      H_pmiss_vs_H_ssdelta_DATA.Fill(evt.pmiss, evt.ssdelta)
      
      H_ssxfp_DATA.Fill(evt.ssxfp)
      H_ssyfp_DATA.Fill(evt.ssyfp)
      H_ssxpfp_DATA.Fill(evt.ssxpfp)
      H_ssypfp_DATA.Fill(evt.ssypfp)
      H_ssdelta_DATA.Fill(evt.ssdelta)
      H_ssxptar_DATA.Fill(evt.ssxptar)
      H_ssyptar_DATA.Fill(evt.ssyptar)
      
      H_hsxfp_DATA.Fill(evt.hsxfp)
      H_hsyfp_DATA.Fill(evt.hsyfp)
      H_hsxpfp_DATA.Fill(evt.hsxpfp)
      H_hsypfp_DATA.Fill(evt.hsypfp)
      H_hsdelta_DATA.Fill(evt.hsdelta)
      H_hsxptar_DATA.Fill(evt.hsxptar)	
      H_hsyptar_DATA.Fill(evt.hsyptar)
      
      H_pmiss_DATA.Fill(evt.pmiss)	
      H_emiss_DATA.Fill(evt.emiss)	
      #H_emiss_DATA.Fill(evt.emiss_nuc)
      H_pmx_DATA.Fill(evt.pmx)
      H_pmy_DATA.Fill(evt.pmy)
      H_pmz_DATA.Fill(evt.pmz)
      H_Q2_DATA.Fill(evt.Q2)
      H_W_DATA.Fill(evt.W)
      H_epsilon_DATA.Fill(evt.epsilon)
      H_MMp2_DATA.Fill(pow(evt.emiss, 2) - pow(evt.pmiss, 2))  
      #H_MMp2_DATA.Fill(pow(evt.MMp, 2))  
      #H_MMp2_DATA.Fill(evt.Mrecoil)

      '''
      # Random subtraction
      H_ct_ep_vs_H_MMp2_DATA_rand.Fill(evt.CTime_epCoinTime_ROC1, evt.MMp)
      H_ct_ep_DATA_cut_rand.Fill(evt.CTime_epCoinTime_ROC1)
      
      H_ssxfp_DATA_rand.Fill(evt.ssxfp)
      H_ssyfp_DATA_rand.Fill(evt.ssyfp)
      H_ssxpfp_DATA_rand.Fill(evt.ssxpfp)
      H_ssypfp_DATA_rand.Fill(evt.ssypfp)
      H_ssdelta_DATA_rand.Fill(evt.ssdelta)
      H_ssxptar_DATA_rand.Fill(evt.ssxptar)
      H_ssyptar_DATA_rand.Fill(evt.ssyptar)
      
      H_hsxfp_DATA_rand.Fill(evt.hsxfp)
      H_hsyfp_DATA_rand.Fill(evt.hsyfp)
      H_hsxpfp_DATA_rand.Fill(evt.hsxpfp)
      H_hsypfp_DATA_rand.Fill(evt.hsypfp)
      H_hsdelta_DATA_rand.Fill(evt.hsdelta)
      H_hsxptar_DATA_rand.Fill(evt.hsxptar)	
      H_hsyptar_DATA_rand.Fill(evt.hsyptar)
      
      H_pmiss_DATA_rand.Fill(evt.pmiss)	
      H_emiss_DATA_rand.Fill(evt.emiss)	
      #H_emiss_DATA_rand.Fill(evt.emiss_nuc)
      H_pmx_DATA_rand.Fill(evt.pmx)
      H_pmy_DATA_rand.Fill(evt.pmy)
      H_pmz_DATA_rand.Fill(evt.pmz)
      H_Q2_DATA_rand.Fill(evt.Q2)
      H_W_DATA_rand.Fill(evt.W)
      H_epsilon_DATA_rand.Fill(evt.epsilon)
      H_MMp2_DATA_rand.Fill(pow(evt.emiss, 2) - pow(evt.pmiss, 2))  
      #H_MMp2_DATA_rand.Fill(evt.MMp)  
      #H_MMp2_DATA_rand.Fill(evt.Mrecoil)
      '''

      H_cal_etotnorm_DATA.Fill(evt.H_cal_etotnorm)
      H_cer_npeSum_DATA.Fill(evt.H_cer_npeSum)

      P_cal_etotnorm_DATA.Fill(evt.P_cal_etotnorm)
      P_hgcer_npeSum_DATA.Fill(evt.P_hgcer_npeSum)
      P_aero_npeSum_DATA.Fill(evt.P_aero_npeSum)
      
      H_cal_etotnorm_vs_H_cer_npeSum_DATA.Fill(evt.H_cal_etotnorm,evt.H_cer_npeSum)
      P_cal_etotnorm_vs_P_hgcer_npeSum_DATA.Fill(evt.P_cal_etotnorm,evt.P_hgcer_npeSum)
      P_cal_etotnorm_vs_P_aero_npeSum_DATA.Fill(evt.P_cal_etotnorm,evt.P_aero_npeSum)
      P_hgcer_npeSum_vs_P_aero_npeSum_DATA.Fill(evt.P_hgcer_npeSum,evt.P_aero_npeSum)
      
for evt in TBRANCH_DUMMY:

  #......... Define Cuts.................

  #CUTs Definations 
  SHMS_FixCut = (evt.P_hod_goodstarttime == 1) & (evt.P_dc_InsideDipoleExit == 1) # & P_hod_betanotrack > 0.5 & P_hod_betanotrack < 1.4
  SHMS_Acceptance = (evt.ssdelta>=-10.0) & (evt.ssdelta<=20.0) & (evt.ssxptar>=-0.06) & (evt.ssxptar<=0.06) & (evt.ssyptar>=-0.04) & (evt.ssyptar<=0.04)

  HMS_FixCut = (evt.H_hod_goodstarttime == 1) & (evt.H_dc_InsideDipoleExit == 1)
  HMS_Acceptance = (evt.hsdelta>=-8.0) & (evt.hsdelta<=8.0) & (evt.hsxptar>=-0.08) & (evt.hsxptar<=0.08) & (evt.hsyptar>=-0.045) & (evt.hsyptar<=0.045)       
  
  #........................................

  H_ct_ep_DUMMY.Fill(evt.CTime_epCoinTime_ROC1)
  
  if(HMS_FixCut & HMS_Acceptance & SHMS_FixCut & SHMS_Acceptance):

      H_ct_ep_DUMMY_cut.Fill(evt.CTime_epCoinTime_ROC1)
      
      H_ssxfp_DUMMY.Fill(evt.ssxfp)
      H_ssyfp_DUMMY.Fill(evt.ssyfp)
      H_ssxpfp_DUMMY.Fill(evt.ssxpfp)
      H_ssypfp_DUMMY.Fill(evt.ssypfp)
      H_ssdelta_DUMMY.Fill(evt.ssdelta)
      H_ssxptar_DUMMY.Fill(evt.ssxptar)
      H_ssyptar_DUMMY.Fill(evt.ssyptar)
      
      H_hsxfp_DUMMY.Fill(evt.hsxfp)
      H_hsyfp_DUMMY.Fill(evt.hsyfp)
      H_hsxpfp_DUMMY.Fill(evt.hsxpfp)
      H_hsypfp_DUMMY.Fill(evt.hsypfp)
      H_hsdelta_DUMMY.Fill(evt.hsdelta)
      H_hsxptar_DUMMY.Fill(evt.hsxptar)	
      H_hsyptar_DUMMY.Fill(evt.hsyptar)
      
      H_pmiss_DUMMY.Fill(evt.pmiss)	
      H_emiss_DUMMY.Fill(evt.emiss)	
      #H_emiss_DUMMY.Fill(evt.emiss_nuc)
      H_pmx_DUMMY.Fill(evt.pmx)
      H_pmy_DUMMY.Fill(evt.pmy)
      H_pmz_DUMMY.Fill(evt.pmz)
      H_Q2_DUMMY.Fill(evt.Q2)
      H_W_DUMMY.Fill(evt.W)
      H_epsilon_DUMMY.Fill(evt.epsilon)
      H_MMp2_DUMMY.Fill(pow(evt.emiss, 2) - pow(evt.pmiss, 2))  
      #H_MMp2_DUMMY.Fill(evt.MMp)  
      #H_MMp2_DUMMY.Fill(evt.Mrecoil)

      '''
      # Random subtraction
      H_ct_ep_DUMMY_cut_rand.Fill(evt.CTime_epCoinTime_ROC1)
      
      H_ssxfp_DUMMY_rand.Fill(evt.ssxfp)
      H_ssyfp_DUMMY_rand.Fill(evt.ssyfp)
      H_ssxpfp_DUMMY_rand.Fill(evt.ssxpfp)
      H_ssypfp_DUMMY_rand.Fill(evt.ssypfp)
      H_ssdelta_DUMMY_rand.Fill(evt.ssdelta)
      H_ssxptar_DUMMY_rand.Fill(evt.ssxptar)
      H_ssyptar_DUMMY_rand.Fill(evt.ssyptar)
      
      H_hsxfp_DUMMY_rand.Fill(evt.hsxfp)
      H_hsyfp_DUMMY_rand.Fill(evt.hsyfp)
      H_hsxpfp_DUMMY_rand.Fill(evt.hsxpfp)
      H_hsypfp_DUMMY_rand.Fill(evt.hsypfp)
      H_hsdelta_DUMMY_rand.Fill(evt.hsdelta)
      H_hsxptar_DUMMY_rand.Fill(evt.hsxptar)	
      H_hsyptar_DUMMY_rand.Fill(evt.hsyptar)
      
      H_pmiss_DUMMY_rand.Fill(evt.pmiss)	
      H_emiss_DUMMY_rand.Fill(evt.emiss)	
      #H_emiss_DUMMY_rand.Fill(evt.emiss_nuc)
      H_pmx_DUMMY_rand.Fill(evt.pmx)
      H_pmy_DUMMY_rand.Fill(evt.pmy)
      H_pmz_DUMMY_rand.Fill(evt.pmz)
      H_Q2_DUMMY_rand.Fill(evt.Q2)
      H_W_DUMMY_rand.Fill(evt.W)
      H_epsilon_DUMMY_rand.Fill(evt.epsilon)
      H_MMp2_DUMMY_rand.Fill(pow(evt.emiss, 2) - pow(evt.pmiss, 2))  
      #H_MMp2_DUMMY_rand.Fill(evt.MMp)  
      #H_MMp2_DUMMY_rand.Fill(evt.Mrecoil)
      '''

normfac_simc = (simc_normfactor)/(simc_nevents)
H_ssxfp_SIMC.Scale(normfac_simc)                                                                                                                                   
H_ssyfp_SIMC.Scale(normfac_simc)                                                                                                                                  
H_ssxpfp_SIMC.Scale(normfac_simc)                                                                                                                              
H_ssypfp_SIMC.Scale(normfac_simc)                                                                                                                                      
H_hsxfp_SIMC.Scale(normfac_simc)                                                                                                                                              
H_hsyfp_SIMC.Scale(normfac_simc)                                                                                                                                               
H_hsxpfp_SIMC.Scale(normfac_simc)                                                                                                                                                                    
H_hsypfp_SIMC.Scale(normfac_simc)                                                                                                                                                                    
H_ssdelta_SIMC.Scale(normfac_simc)                                                                                                                                                                  
H_hsdelta_SIMC.Scale(normfac_simc)                                                                                                                                                                  
H_ssxptar_SIMC.Scale(normfac_simc)                                                                                                                                                                  
H_ssyptar_SIMC.Scale(normfac_simc)                                                                                                                                                                  
H_hsxptar_SIMC.Scale(normfac_simc)                                                                                                                                                                  
H_hsyptar_SIMC.Scale(normfac_simc)                                                                                                                                                                  
H_pmiss_SIMC.Scale(normfac_simc)                                                                                                                                        
H_emiss_SIMC.Scale(normfac_simc)                                                                                                                                            
H_pmx_SIMC.Scale(normfac_simc)                                                                                                                                                
H_pmy_SIMC.Scale(normfac_simc)                                                                                                                                                
H_pmz_SIMC.Scale(normfac_simc)                                                                                                                                                
H_Q2_SIMC.Scale(normfac_simc)
H_W_SIMC.Scale(normfac_simc)                                                                                                                                                         
H_epsilon_SIMC.Scale(normfac_simc)                                                                                                                                                    
H_MMp2_SIMC.Scale(normfac_simc)

dummy_target_corr = 4.8579
normfac_dummy = 1/(dummy_charge*dummy_target_corr*dummy_efficiency)
H_ssxfp_DUMMY.Scale(normfac_dummy)
H_ssyfp_DUMMY.Scale(normfac_dummy)
H_ssxpfp_DUMMY.Scale(normfac_dummy)
H_ssypfp_DUMMY.Scale(normfac_dummy)
H_hsxfp_DUMMY.Scale(normfac_dummy)
H_hsyfp_DUMMY.Scale(normfac_dummy)
H_hsxpfp_DUMMY.Scale(normfac_dummy)
H_hsypfp_DUMMY.Scale(normfac_dummy)
H_ssxptar_DUMMY.Scale(normfac_dummy)
H_ssyptar_DUMMY.Scale(normfac_dummy)
H_hsxptar_DUMMY.Scale(normfac_dummy)
H_hsyptar_DUMMY.Scale(normfac_dummy)
H_ssdelta_DUMMY.Scale(normfac_dummy)
H_hsdelta_DUMMY.Scale(normfac_dummy)
H_Q2_DUMMY.Scale(normfac_dummy)
H_epsilon_DUMMY.Scale(normfac_dummy)
H_MMp2_DUMMY.Scale(normfac_dummy)
H_pmiss_DUMMY.Scale(normfac_dummy)
H_emiss_DUMMY.Scale(normfac_dummy)
H_pmx_DUMMY.Scale(normfac_dummy)
H_pmy_DUMMY.Scale(normfac_dummy)
H_pmz_DUMMY.Scale(normfac_dummy)
H_W_DUMMY.Scale(normfac_dummy)
H_ct_ep_DUMMY.Scale(normfac_dummy)
H_ct_ep_DUMMY_cut.Scale(normfac_dummy)

normfac_data = 1/(data_charge*data_efficiency)
H_ssxfp_DATA.Scale(normfac_data)
H_ssyfp_DATA.Scale(normfac_data)
H_ssxpfp_DATA.Scale(normfac_data)
H_ssypfp_DATA.Scale(normfac_data)
H_hsxfp_DATA.Scale(normfac_data)
H_hsyfp_DATA.Scale(normfac_data)
H_hsxpfp_DATA.Scale(normfac_data)
H_hsypfp_DATA.Scale(normfac_data)
H_ssxptar_DATA.Scale(normfac_data)
H_ssyptar_DATA.Scale(normfac_data)
H_hsxptar_DATA.Scale(normfac_data)
H_hsyptar_DATA.Scale(normfac_data)
H_ssdelta_DATA.Scale(normfac_data)
H_hsdelta_DATA.Scale(normfac_data)
H_Q2_DATA.Scale(normfac_data)
H_epsilon_DATA.Scale(normfac_data)
H_MMp2_DATA.Scale(normfac_data)
H_pmiss_DATA.Scale(normfac_data)
H_emiss_DATA.Scale(normfac_data)
H_pmx_DATA.Scale(normfac_data)
H_pmy_DATA.Scale(normfac_data)
H_pmz_DATA.Scale(normfac_data)
H_W_DATA.Scale(normfac_data)
H_ct_ep_DATA.Scale(normfac_data)
H_ct_ep_DATA_cut.Scale(normfac_data)

'''
# Data Random subtraction
H_ssxfp_DATA_rand.Scale(normfac_data/nWindows)
H_ssyfp_DATA_rand.Scale(normfac_data/nWindows)
H_ssxpfp_DATA_rand.Scale(normfac_data/nWindows)
H_ssypfp_DATA_rand.Scale(normfac_data/nWindows)
H_hsxfp_DATA_rand.Scale(normfac_data/nWindows)
H_hsyfp_DATA_rand.Scale(normfac_data/nWindows)
H_hsxpfp_DATA_rand.Scale(normfac_data/nWindows)
H_hsypfp_DATA_rand.Scale(normfac_data/nWindows)
H_ssxptar_DATA_rand.Scale(normfac_data/nWindows)
H_ssyptar_DATA_rand.Scale(normfac_data/nWindows)
H_hsxptar_DATA_rand.Scale(normfac_data/nWindows)
H_hsyptar_DATA_rand.Scale(normfac_data/nWindows)
H_ssdelta_DATA_rand.Scale(normfac_data/nWindows)
H_hsdelta_DATA_rand.Scale(normfac_data/nWindows)
H_Q2_DATA_rand.Scale(normfac_data/nWindows)
H_epsilon_DATA_rand.Scale(normfac_data/nWindows)
H_MMp2_DATA_rand.Scale(normfac_data/nWindows)
H_pmiss_DATA_rand.Scale(normfac_data/nWindows)
H_emiss_DATA_rand.Scale(normfac_data/nWindows)
H_pmx_DATA_rand.Scale(normfac_data/nWindows)
H_pmy_DATA_rand.Scale(normfac_data/nWindows)
H_pmz_DATA_rand.Scale(normfac_data/nWindows)
H_W_DATA_rand.Scale(normfac_data/nWindows)
#H_ct_ep_DATA_rand.Scale(normfac_data/nWindows)
H_ct_ep_DATA_cut_rand.Scale(normfac_data/nWindows)

# Dummy Random subtraction
H_ssxfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_ssyfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_ssxpfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_ssypfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_hsxfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_hsyfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_hsxpfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_hsypfp_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_ssxptar_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_ssyptar_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_hsxptar_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_hsyptar_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_ssdelta_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_hsdelta_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_Q2_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_epsilon_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_MMp2_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_pmiss_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_emiss_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_pmx_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_pmy_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_pmz_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_W_DUMMY_rand.Scale(normfac_dummy/nWindows)
#H_ct_ep_DUMMY_rand.Scale(normfac_dummy/nWindows)
H_ct_ep_DUMMY_cut_rand.Scale(normfac_dummy/nWindows)

###

# Data Random subtraction
H_ssxfp_DATA.Add(H_ssxfp_DATA_rand,-1)
H_ssyfp_DATA.Add(H_ssyfp_DATA_rand,-1)
H_ssxpfp_DATA.Add(H_ssxpfp_DATA_rand,-1)
H_ssypfp_DATA.Add(H_ssypfp_DATA_rand,-1)
H_hsxfp_DATA.Add(H_hsxfp_DATA_rand,-1)
H_hsyfp_DATA.Add(H_hsyfp_DATA_rand,-1)
H_hsxpfp_DATA.Add(H_hsxpfp_DATA_rand,-1)
H_hsypfp_DATA.Add(H_hsypfp_DATA_rand,-1)
H_ssxptar_DATA.Add(H_ssxptar_DATA_rand,-1)
H_ssyptar_DATA.Add(H_ssyptar_DATA_rand,-1)
H_hsxptar_DATA.Add(H_hsxptar_DATA_rand,-1)
H_hsyptar_DATA.Add(H_hsyptar_DATA_rand,-1)
H_ssdelta_DATA.Add(H_ssdelta_DATA_rand,-1)
H_hsdelta_DATA.Add(H_hsdelta_DATA_rand,-1)
H_Q2_DATA.Add(H_Q2_DATA_rand,-1)
H_epsilon_DATA.Add(H_epsilon_DATA_rand,-1)
H_MMp2_DATA.Add(H_MMp2_DATA_rand,-1)
H_pmiss_DATA.Add(H_pmiss_DATA_rand,-1)
H_emiss_DATA.Add(H_emiss_DATA_rand,-1)
H_pmx_DATA.Add(H_pmx_DATA_rand,-1)
H_pmy_DATA.Add(H_pmy_DATA_rand,-1)
H_pmz_DATA.Add(H_pmz_DATA_rand,-1)
H_W_DATA.Add(H_W_DATA_rand,-1)
#H_ct_ep_DATA.Add(H_ct_ep_DATA_rand,-1)
H_ct_ep_DATA_cut.Add(H_ct_ep_DATA_cut_rand,-1)

# Dummy Random subtraction
H_ssxfp_DUMMY.Add(H_ssxfp_DUMMY_rand,-1)
H_ssyfp_DUMMY.Add(H_ssyfp_DUMMY_rand,-1)
H_ssxpfp_DUMMY.Add(H_ssxpfp_DUMMY_rand,-1)
H_ssypfp_DUMMY.Add(H_ssypfp_DUMMY_rand,-1)
H_hsxfp_DUMMY.Add(H_hsxfp_DUMMY_rand,-1)
H_hsyfp_DUMMY.Add(H_hsyfp_DUMMY_rand,-1)
H_hsxpfp_DUMMY.Add(H_hsxpfp_DUMMY_rand,-1)
H_hsypfp_DUMMY.Add(H_hsypfp_DUMMY_rand,-1)
H_ssxptar_DUMMY.Add(H_ssxptar_DUMMY_rand,-1)
H_ssyptar_DUMMY.Add(H_ssyptar_DUMMY_rand,-1)
H_hsxptar_DUMMY.Add(H_hsxptar_DUMMY_rand,-1)
H_hsyptar_DUMMY.Add(H_hsyptar_DUMMY_rand,-1)
H_ssdelta_DUMMY.Add(H_ssdelta_DUMMY_rand,-1)
H_hsdelta_DUMMY.Add(H_hsdelta_DUMMY_rand,-1)
H_Q2_DUMMY.Add(H_Q2_DUMMY_rand,-1)
H_epsilon_DUMMY.Add(H_epsilon_DUMMY_rand,-1)
H_MMp2_DUMMY.Add(H_MMp2_DUMMY_rand,-1)
H_pmiss_DUMMY.Add(H_pmiss_DUMMY_rand,-1)
H_emiss_DUMMY.Add(H_emiss_DUMMY_rand,-1)
H_pmx_DUMMY.Add(H_pmx_DUMMY_rand,-1)
H_pmy_DUMMY.Add(H_pmy_DUMMY_rand,-1)
H_pmz_DUMMY.Add(H_pmz_DUMMY_rand,-1)
H_W_DUMMY.Add(H_W_DUMMY_rand,-1)
#H_ct_ep_DUMMY.Add(H_ct_ep_DUMMY_rand,-1)
H_ct_ep_DUMMY_cut.Add(H_ct_ep_DUMMY_cut_rand,-1)
'''

# Dummy Subtraction
H_ssxfp_DATA.Add(H_ssxfp_DUMMY,-1)
H_ssyfp_DATA.Add(H_ssyfp_DUMMY,-1)
H_ssxpfp_DATA.Add(H_ssxpfp_DUMMY,-1)
H_ssypfp_DATA.Add(H_ssypfp_DUMMY,-1)
H_hsxfp_DATA.Add(H_hsxfp_DUMMY,-1)
H_hsyfp_DATA.Add(H_hsyfp_DUMMY,-1)
H_hsxpfp_DATA.Add(H_hsxpfp_DUMMY,-1)
H_hsypfp_DATA.Add(H_hsypfp_DUMMY,-1)
H_ssxptar_DATA.Add(H_ssxptar_DUMMY,-1)
H_ssyptar_DATA.Add(H_ssyptar_DUMMY,-1)
H_hsxptar_DATA.Add(H_hsxptar_DUMMY,-1)
H_hsyptar_DATA.Add(H_hsyptar_DUMMY,-1)
H_ssdelta_DATA.Add(H_ssdelta_DUMMY,-1)
H_hsdelta_DATA.Add(H_hsdelta_DUMMY,-1)
H_Q2_DATA.Add(H_Q2_DUMMY,-1)
H_epsilon_DATA.Add(H_epsilon_DUMMY,-1)
H_MMp2_DATA.Add(H_MMp2_DUMMY,-1)
H_pmiss_DATA.Add(H_pmiss_DUMMY,-1)
H_emiss_DATA.Add(H_emiss_DUMMY,-1)
H_pmx_DATA.Add(H_pmx_DUMMY,-1)
H_pmy_DATA.Add(H_pmy_DUMMY,-1)
H_pmz_DATA.Add(H_pmz_DUMMY,-1)
H_W_DATA.Add(H_W_DUMMY,-1)
H_ct_ep_DATA.Add(H_ct_ep_DUMMY,-1)
H_ct_ep_DATA_cut.Add(H_ct_ep_DUMMY_cut,-1)

################################################################################################################################################
ROOT.gStyle.SetOptStat(0)
################################################################################################################################################

# PLOT HIST..

eff_plt = TCanvas()
G_eff_plt = ROOT.TMultiGraph()
l_eff_plt = ROOT.TLegend(0.115,0.735,0.33,0.9)

eff_plt.SetGrid()

G_data_eff.SetMarkerStyle(21)
G_dummy_eff.SetMarkerStyle(21)

G_data_eff.SetMarkerSize(1)
G_dummy_eff.SetMarkerSize(1)

G_dummy_eff.SetMarkerColor(kRed)

G_eff_plt.Add(G_data_eff)
G_eff_plt.Add(G_dummy_eff)

G_eff_plt.Draw("AP")

G_eff_plt.SetTitle(" ;Run Numbers; Total Efficiency")

i=0
while i <= G_eff_plt.GetXaxis().GetXmax():
    bin_ix = G_eff_plt.GetXaxis().FindBin(i)
    if str(i) in data_runNums.split(" ") or str(i) in dummy_runNums.split(" "): 
        G_eff_plt.GetXaxis().SetBinLabel(bin_ix,"%d" % i)
    i+=1

G_eff_plt.GetYaxis().SetTitleOffset(1.5)
G_eff_plt.GetXaxis().SetTitleOffset(1.5)
G_eff_plt.GetXaxis().SetLabelSize(0.04)

l_eff_plt.AddEntry(G_data_eff,"Data")
l_eff_plt.AddEntry(G_dummy_eff,"Dummy")

l_eff_plt.Draw()

eff_plt.Print(outputpdf + '(')

c_pid = TCanvas()

c_pid.Divide(2,3)

c_pid.cd(1)
gPad.SetLogy()
H_cal_etotnorm_DATA.Draw()

c_pid.cd(2)
gPad.SetLogy()
H_cer_npeSum_DATA.Draw()

c_pid.cd(3)
gPad.SetLogy()
P_cal_etotnorm_DATA.Draw()

c_pid.cd(4)
gPad.SetLogy()
P_hgcer_npeSum_DATA.Draw()

c_pid.cd(5)
gPad.SetLogy()
P_aero_npeSum_DATA.Draw()

c_pid.Draw()

c_pid.Print(outputpdf)

c_pid_2d = TCanvas()

c_pid_2d.Divide(2,2)

c_pid_2d.cd(1)
H_cal_etotnorm_vs_H_cer_npeSum_DATA.Draw("colz")

c_pid_2d.cd(2)
P_cal_etotnorm_vs_P_hgcer_npeSum_DATA.Draw("colz")

c_pid_2d.cd(3)
P_cal_etotnorm_vs_P_aero_npeSum_DATA.Draw("colz")

c_pid_2d.cd(4)
P_hgcer_npeSum_vs_P_aero_npeSum_DATA.Draw("colz")

c_pid_2d.Draw()

c_pid_2d.Print(outputpdf)

ct_ep = TCanvas()
l_ct_ep = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ct_ep_DATA.SetLineColor(kRed)

H_ct_ep_DATA.Draw("")
H_ct_ep_DATA_cut.Draw("same")

l_ct_ep.AddEntry(H_ct_ep_DATA,"No cut")
l_ct_ep.AddEntry(H_ct_ep_DATA_cut,"Cut")

l_ct_ep.Draw()

ct_ep.Print(outputpdf)

ct_ep_mmp = TCanvas()

H_ct_ep_vs_H_MMp2_DATA.Draw("colz")

ct_ep_mmp.Print(outputpdf)

emiss_vs_delta = TCanvas()

emiss_vs_delta.Divide(1,2)

emiss_vs_delta.cd(1)
H_emiss_vs_H_hsdelta_DATA.Draw("colz")

emiss_vs_delta.cd(2)
H_emiss_vs_H_ssdelta_DATA.Draw("colz")

emiss_vs_delta.Print(outputpdf)

pmiss_vs_delta = TCanvas()

pmiss_vs_delta.Divide(1,2)

pmiss_vs_delta.cd(1)
H_pmiss_vs_H_hsdelta_DATA.Draw("colz")

pmiss_vs_delta.cd(2)
H_pmiss_vs_H_ssdelta_DATA.Draw("colz")

pmiss_vs_delta.Print(outputpdf)

xfp = TCanvas()
l_xfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ssxfp_DATA.SetLineColor(kRed)
H_ssxfp_SIMC.Draw("")
H_ssxfp_DATA.Draw("same")

b_int_xfp_simc = int(H_ssxfp_SIMC.Integral())
b_int_xfp_data = int(H_ssxfp_DATA.Integral())

l_xfp.AddEntry(H_ssxfp_SIMC,"SIMC, INT = %s" % b_int_xfp_simc)
l_xfp.AddEntry(H_ssxfp_DATA,"DATA, INT = %s" % b_int_xfp_data)

l_xfp.Draw()

xfp.Print(outputpdf)

yfp = TCanvas()
l_yfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ssyfp_DATA.SetLineColor(kRed)
H_ssyfp_SIMC.Draw("")
H_ssyfp_DATA.Draw("same")

b_int_yfp_simc = int(H_ssyfp_SIMC.Integral())
b_int_yfp_data = int(H_ssyfp_DATA.Integral())

l_yfp.AddEntry(H_ssyfp_SIMC,"SIMC, INT = %s" % b_int_yfp_simc)
l_yfp.AddEntry(H_ssyfp_DATA,"DATA, INT = %s" % b_int_yfp_data)

l_yfp.Draw()

yfp.Print(outputpdf)

xpfp = TCanvas()
l_xpfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ssxpfp_DATA.SetLineColor(kRed)
H_ssxpfp_SIMC.Draw("")
H_ssxpfp_DATA.Draw("same")

b_int_xpfp_simc = int(H_ssxpfp_SIMC.Integral())
b_int_xpfp_data = int(H_ssxpfp_DATA.Integral())

l_xpfp.AddEntry(H_ssxpfp_SIMC,"SIMC, INT = %s" % b_int_xpfp_simc)
l_xpfp.AddEntry(H_ssxpfp_DATA,"DATA, INT = %s" % b_int_xpfp_data)

l_xpfp.Draw()

xpfp.Print(outputpdf)

ypfp = TCanvas()
l_ypfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ssypfp_DATA.SetLineColor(kRed)
H_ssypfp_SIMC.Draw("")
H_ssypfp_DATA.Draw("same")

b_int_ypfp_simc = int(H_ssypfp_SIMC.Integral())
b_int_ypfp_data = int(H_ssypfp_DATA.Integral())

l_ypfp.AddEntry(H_ssypfp_SIMC,"SIMC, INT = %s" % b_int_ypfp_simc)
l_ypfp.AddEntry(H_ssypfp_DATA,"DATA, INT = %s" % b_int_ypfp_data)

l_ypfp.Draw()

ypfp.Print(outputpdf)

hxfp = TCanvas()
l_hxfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_hsxfp_DATA.SetLineColor(kRed)
H_hsxfp_SIMC.Draw("")
H_hsxfp_DATA.Draw("same")

b_int_hxfp_simc = int(H_hsxfp_SIMC.Integral())
b_int_hxfp_data = int(H_hsxfp_DATA.Integral())

l_hxfp.AddEntry(H_hsxfp_SIMC,"SIMC, INT = %s" % b_int_hxfp_simc)
l_hxfp.AddEntry(H_hsxfp_DATA,"DATA, INT = %s" % b_int_hxfp_data)

l_hxfp.Draw()

hxfp.Print(outputpdf)

hyfp = TCanvas()
l_hyfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_hsyfp_DATA.SetLineColor(kRed)
H_hsyfp_SIMC.Draw("")
H_hsyfp_DATA.Draw("same")

b_int_hyfp_simc = int(H_hsyfp_SIMC.Integral())
b_int_hyfp_data = int(H_hsyfp_DATA.Integral())

l_hyfp.AddEntry(H_hsyfp_SIMC,"SIMC, INT = %s" % b_int_hyfp_simc)
l_hyfp.AddEntry(H_hsyfp_DATA,"DATA, INT = %s" % b_int_hyfp_data)

l_hyfp.Draw()

hyfp.Print(outputpdf)

hxpfp = TCanvas()
l_hxpfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_hsxpfp_DATA.SetLineColor(kRed)
H_hsxpfp_SIMC.Draw("")
H_hsxpfp_DATA.Draw("same")

b_int_hxpfp_simc = int(H_hsxpfp_SIMC.Integral())
b_int_hxpfp_data = int(H_hsxpfp_DATA.Integral())

l_hxpfp.AddEntry(H_hsxpfp_SIMC,"SIMC, INT = %s" % b_int_hxpfp_simc)
l_hxpfp.AddEntry(H_hsxpfp_DATA,"DATA, INT = %s" % b_int_hxpfp_data)

l_hxpfp.Draw()

hxpfp.Print(outputpdf)

hypfp = TCanvas()
l_hypfp = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_hsypfp_DATA.SetLineColor(kRed)
H_hsypfp_SIMC.Draw("")
H_hsypfp_DATA.Draw("same")

b_int_hypfp_simc = int(H_hsypfp_SIMC.Integral())
b_int_hypfp_data = int(H_hsypfp_DATA.Integral())

l_hypfp.AddEntry(H_hsypfp_SIMC,"SIMC, INT = %s" % b_int_hypfp_simc)
l_hypfp.AddEntry(H_hsypfp_DATA,"DATA, INT = %s" % b_int_hypfp_data)

l_hypfp.Draw()

hypfp.Print(outputpdf)

xptar = TCanvas()
l_xptar = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ssxptar_DATA.SetLineColor(kRed)
H_ssxptar_SIMC.Draw("")
H_ssxptar_DATA.Draw("same")

b_int_xptar_simc = int(H_ssxptar_SIMC.Integral())
b_int_xptar_data = int(H_ssxptar_DATA.Integral())

l_xptar.AddEntry(H_ssxptar_SIMC,"SIMC, INT = %s" % b_int_xptar_simc)
l_xptar.AddEntry(H_ssxptar_DATA,"DATA, INT = %s" % b_int_xptar_data)

l_xptar.Draw()

xptar.Print(outputpdf)

yptar = TCanvas()
l_yptar = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ssyptar_DATA.SetLineColor(kRed)
H_ssyptar_SIMC.Draw("")
H_ssyptar_DATA.Draw("same")

b_int_yptar_simc = int(H_ssyptar_SIMC.Integral())
b_int_yptar_data = int(H_ssyptar_DATA.Integral())

l_yptar.AddEntry(H_ssyptar_SIMC,"SIMC, INT = %s" % b_int_yptar_simc)
l_yptar.AddEntry(H_ssyptar_DATA,"DATA, INT = %s" % b_int_yptar_data)

l_yptar.Draw()

yptar.Print(outputpdf)

hxptar = TCanvas()
l_hxptar = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_hsxptar_DATA.SetLineColor(kRed)
H_hsxptar_SIMC.Draw("")
H_hsxptar_DATA.Draw("same")

b_int_hxptar_simc = int(H_hsxptar_SIMC.Integral())
b_int_hxptar_data = int(H_hsxptar_DATA.Integral())

l_hxptar.AddEntry(H_hsxptar_SIMC,"SIMC, INT = %s" % b_int_hxptar_simc)
l_hxptar.AddEntry(H_hsxptar_DATA,"DATA, INT = %s" % b_int_hxptar_data)

l_hxptar.Draw()

hxptar.Print(outputpdf)

hyptar = TCanvas()
l_hyptar = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_hsyptar_DATA.SetLineColor(kRed)
H_hsyptar_SIMC.Draw("")
H_hsyptar_DATA.Draw("same")

b_int_hyptar_simc = int(H_hsyptar_SIMC.Integral())
b_int_hyptar_data = int(H_hsyptar_DATA.Integral())

l_hyptar.AddEntry(H_hsyptar_SIMC,"SIMC, INT = %s" % b_int_hyptar_simc)
l_hyptar.AddEntry(H_hsyptar_DATA,"DATA, INT = %s" % b_int_hyptar_data)

l_hyptar.Draw()

hyptar.Print(outputpdf)

Delta = TCanvas()
l_Delta = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_ssdelta_DATA.SetLineColor(kRed)
H_ssdelta_SIMC.Draw("")
H_ssdelta_DATA.Draw("same")

b_int_Delta_simc = int(H_ssdelta_SIMC.Integral())
b_int_Delta_data = int(H_ssdelta_DATA.Integral())

l_Delta.AddEntry(H_ssdelta_SIMC,"SIMC, INT = %s" % b_int_Delta_simc)
l_Delta.AddEntry(H_ssdelta_DATA,"DATA, INT = %s" % b_int_Delta_data)

l_Delta.Draw()

Delta.Print(outputpdf)

hDelta = TCanvas()
l_hDelta = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_hsdelta_DATA.SetLineColor(kRed)

H_hsdelta_SIMC.Draw("")
H_hsdelta_DATA.Draw("same")

b_int_hDelta_simc = int(H_hsdelta_SIMC.Integral())
b_int_hDelta_data = int(H_hsdelta_DATA.Integral())

l_hDelta.AddEntry(H_hsdelta_SIMC,"SIMC, INT = %s" % b_int_hDelta_simc)
l_hDelta.AddEntry(H_hsdelta_DATA,"DATA, INT = %s" % b_int_hDelta_data)

l_hDelta.Draw()

hDelta.Print(outputpdf)

CQ2 = TCanvas()
l_Q2 = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_Q2_DATA.SetLineColor(kRed)
H_Q2_SIMC.Draw("")
H_Q2_DATA.Draw("same")

b_int_Q2_simc = int(H_Q2_SIMC.Integral())
b_int_Q2_data = int(H_Q2_DATA.Integral())

l_Q2.AddEntry(H_Q2_SIMC,"SIMC, INT = %s" % b_int_Q2_simc)
l_Q2.AddEntry(H_Q2_DATA,"DATA, INT = %s" % b_int_Q2_data)

l_Q2.Draw()

CQ2.Print(outputpdf)

Cepsilon = TCanvas()
l_epsilon = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_epsilon_DATA.SetLineColor(kRed)
H_epsilon_SIMC.Draw("")
H_epsilon_DATA.Draw("same")

b_int_epsilon_simc = int(H_epsilon_SIMC.Integral())
b_int_epsilon_data = int(H_epsilon_DATA.Integral())

l_epsilon.AddEntry(H_epsilon_SIMC,"SIMC, INT = %s" % b_int_epsilon_simc)
l_epsilon.AddEntry(H_epsilon_DATA,"DATA, INT = %s" % b_int_epsilon_data)

l_epsilon.Draw()

Cepsilon.Print(outputpdf)

CMMp2 = TCanvas()
l_MMp2 = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_MMp2_DATA.SetLineColor(kRed)
H_MMp2_DATA.Draw("")
H_MMp2_SIMC.Draw("same")

#H_MMp2_SIMC.Draw("")
#H_MMp2_DATA.Draw("same")

b_int_MMp2_simc = int(H_MMp2_SIMC.Integral())
b_int_MMp2_data = int(H_MMp2_DATA.Integral())

b_mean_MMp2_simc = H_MMp2_SIMC.GetMean()
b_mean_MMp2_data = H_MMp2_DATA.GetMean()

l_MMp2.AddEntry(H_MMp2_SIMC,"SIMC, INT = %s" % b_int_MMp2_simc)
l_MMp2.AddEntry(H_MMp2_DATA,"DATA, INT = %s" % b_int_MMp2_data)
l_MMp2.AddEntry(H_MMp2_SIMC,"SIMC, MEAN = {0:.3f}".format(b_mean_MMp2_simc))
l_MMp2.AddEntry(H_MMp2_DATA,"DATA, MEAN = {0:.3f}".format(b_mean_MMp2_data))

l_MMp2.Draw()

CMMp2.Print(outputpdf)

Cpmiss = TCanvas()
l_pmiss = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmiss_DATA.SetLineColor(kRed)
H_pmiss_SIMC.Draw("")
H_pmiss_DATA.Draw("same")

b_int_pmiss_simc = int(H_pmiss_SIMC.Integral())
b_int_pmiss_data = int(H_pmiss_DATA.Integral())

b_mean_pmiss_simc = H_pmiss_SIMC.GetMean()
b_mean_pmiss_data = H_pmiss_DATA.GetMean(H_pmiss_DATA.GetMaximumBin())

l_pmiss.AddEntry(H_pmiss_SIMC,"SIMC, INT = %s" % b_int_pmiss_simc)
l_pmiss.AddEntry(H_pmiss_DATA,"DATA, INT = %s" % b_int_pmiss_data)
l_pmiss.AddEntry(H_pmiss_SIMC,"SIMC, MEAN = {0:.3f}".format(b_mean_pmiss_simc))
l_pmiss.AddEntry(H_pmiss_DATA,"DATA, MEAN = {0:.3f}".format(b_mean_pmiss_data))

l_pmiss.Draw()

Cpmiss.Print(outputpdf)

Cemiss = TCanvas()
l_emiss = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_emiss_DATA.SetLineColor(kRed)
H_emiss_SIMC.Draw("same")
H_emiss_DATA.Draw("same")

b_int_emiss_simc = int(H_emiss_SIMC.Integral())
b_int_emiss_data = int(H_emiss_DATA.Integral())

b_mean_emiss_simc = H_emiss_SIMC.GetMean()
b_mean_emiss_data = H_emiss_DATA.GetMean()

l_emiss.AddEntry(H_emiss_SIMC,"SIMC, INT = %s" % b_int_emiss_simc)
l_emiss.AddEntry(H_emiss_DATA,"DATA, INT = %s" % b_int_emiss_data)
l_emiss.AddEntry(H_emiss_SIMC,"SIMC, MEAN = {0:.3f}".format(b_mean_emiss_simc))
l_emiss.AddEntry(H_emiss_DATA,"DATA, MEAN = {0:.3f}".format(b_mean_emiss_data))

l_emiss.Draw()

Cemiss.Print(outputpdf)

Cpmiss_x = TCanvas()
l_pmx = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmx_DATA.SetLineColor(kRed)
H_pmx_SIMC.Draw("")
H_pmx_DATA.Draw("same")

b_int_pmx_simc = int(H_pmx_SIMC.Integral())
b_int_pmx_data = int(H_pmx_DATA.Integral())

b_mean_pmx_simc = H_pmx_SIMC.GetMean()
b_mean_pmx_data = H_pmx_DATA.GetMean()

l_pmx.AddEntry(H_pmx_SIMC,"SIMC, INT = %s" % b_int_pmx_simc)
l_pmx.AddEntry(H_pmx_DATA,"DATA, INT = %s" % b_int_pmx_data)
l_pmx.AddEntry(H_pmx_SIMC,"SIMC, MEAN = {0:.3f}".format(b_mean_pmx_simc))
l_pmx.AddEntry(H_pmx_DATA,"DATA, MEAN = {0:.3f}".format(b_mean_pmx_data))

l_pmx.Draw()

Cpmiss_x.Print(outputpdf)

Cpmiss_y = TCanvas()
l_pmy = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmy_DATA.SetLineColor(kRed)
H_pmy_SIMC.Draw("")
H_pmy_DATA.Draw("same")

b_int_pmy_simc = int(H_pmy_SIMC.Integral())
b_int_pmy_data = int(H_pmy_DATA.Integral())

b_mean_pmy_simc = H_pmy_SIMC.GetMean()
b_mean_pmy_data = H_pmy_DATA.GetMean()

l_pmy.AddEntry(H_pmy_SIMC,"SIMC, INT = %s" % b_int_pmy_simc)
l_pmy.AddEntry(H_pmy_DATA,"DATA, INT = %s" % b_int_pmy_data)
l_pmy.AddEntry(H_pmy_SIMC,"SIMC, MEAN = {0:.3f}".format(b_mean_pmy_simc))
l_pmy.AddEntry(H_pmy_DATA,"DATA, MEAN = {0:.3f}".format(b_mean_pmy_data))

l_pmy.Draw()

Cpmiss_y.Print(outputpdf)

Cpmiss_z = TCanvas()
l_pmz = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmz_DATA.SetLineColor(kRed)
H_pmz_SIMC.Draw("")
H_pmz_DATA.Draw("same")

b_int_pmz_simc = int(H_pmz_SIMC.Integral())
b_int_pmz_data = int(H_pmz_DATA.Integral())

b_mean_pmz_simc = H_pmz_SIMC.GetMean()
b_mean_pmz_data = H_pmz_DATA.GetMean()

l_pmz.AddEntry(H_pmz_SIMC,"SIMC, INT = %s" % b_int_pmz_simc)
l_pmz.AddEntry(H_pmz_DATA,"DATA, INT = %s" % b_int_pmz_data)
l_pmz.AddEntry(H_pmz_SIMC,"SIMC, MEAN = {0:.3f}".format(b_mean_pmz_simc))
l_pmz.AddEntry(H_pmz_DATA,"DATA, MEAN = {0:.3f}".format(b_mean_pmz_data))

l_pmz.Draw()

Cpmiss_z.Print(outputpdf)

CW = TCanvas()
l_W = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_W_DATA.SetLineColor(kRed)
H_W_SIMC.Draw("")
H_W_DATA.Draw("same")

b_int_W_simc = int(H_W_SIMC.Integral())
b_int_W_data = int(H_W_DATA.Integral())

b_mean_W_simc = H_W_SIMC.GetMean()
b_mean_W_data = H_W_DATA.GetMean()

l_W.AddEntry(H_W_SIMC,"SIMC, INT = %s" % b_int_W_simc)
l_W.AddEntry(H_W_DATA,"DATA, INT = %s" % b_int_W_data)
l_W.AddEntry(H_W_SIMC,"SIMC, MEAN = {0:.3f}".format(b_mean_W_simc))
l_W.AddEntry(H_W_DATA,"DATA, MEAN = {0:.3f}".format(b_mean_W_data))

l_W.Draw()

CW.Print(outputpdf + ')')

#############################################################################################################################################

outHistFile = ROOT.TFile.Open(foutname, "RECREATE")
d_Data = outHistFile.mkdir("Data")
d_Dummy = outHistFile.mkdir("Dummy")
d_Simc = outHistFile.mkdir("SIMC")

d_Data.cd()
H_hsdelta_DATA.Write()
H_hsxptar_DATA.Write()
H_hsyptar_DATA.Write()
H_ssxfp_DATA.Write()
H_ssyfp_DATA.Write()
H_ssxpfp_DATA.Write()
H_ssypfp_DATA.Write()
H_hsxfp_DATA.Write()
H_hsyfp_DATA.Write()
H_hsxpfp_DATA.Write()
H_hsypfp_DATA.Write()
H_ssdelta_DATA.Write()
H_ssxptar_DATA.Write()
H_ssyptar_DATA.Write()
H_q_DATA.Write()
H_Q2_DATA.Write()
H_epsilon_DATA.Write()
H_MMp2_DATA.Write()
H_th_DATA.Write()
H_ph_DATA.Write()
H_pmiss_DATA.Write()
H_emiss_DATA.Write()
H_pmx_DATA.Write()
H_pmy_DATA.Write()
H_pmz_DATA.Write()
H_W_DATA.Write()
H_ct_ep_DATA.Write()

d_Dummy.cd()
H_hsdelta_DUMMY.Write()
H_hsxptar_DUMMY.Write()
H_hsyptar_DUMMY.Write()
H_ssxfp_DUMMY.Write()
H_ssyfp_DUMMY.Write()
H_ssxpfp_DUMMY.Write()
H_ssypfp_DUMMY.Write()
H_hsxfp_DUMMY.Write()
H_hsyfp_DUMMY.Write()
H_hsxpfp_DUMMY.Write()
H_hsypfp_DUMMY.Write()
H_ssdelta_DUMMY.Write()
H_ssxptar_DUMMY.Write()
H_ssyptar_DUMMY.Write()
H_q_DUMMY.Write()
H_Q2_DUMMY.Write()
H_epsilon_DUMMY.Write()
H_MMp2_DUMMY.Write()
H_th_DUMMY.Write()
H_ph_DUMMY.Write()
H_pmiss_DUMMY.Write()
H_emiss_DUMMY.Write()
H_pmx_DUMMY.Write()
H_pmy_DUMMY.Write()
H_pmz_DUMMY.Write()
H_W_DUMMY.Write()
H_ct_ep_DUMMY.Write()

d_Simc.cd()
H_hsdelta_SIMC.Write()
H_hsxptar_SIMC.Write()
H_hsyptar_SIMC.Write()
H_ssxfp_SIMC.Write()
H_ssyfp_SIMC.Write()
H_ssxpfp_SIMC.Write()
H_ssypfp_SIMC.Write()
H_hsxfp_SIMC.Write()
H_hsyfp_SIMC.Write()
H_hsxpfp_SIMC.Write()
H_hsypfp_SIMC.Write()
H_ssdelta_SIMC.Write()
H_ssxptar_SIMC.Write()
H_ssyptar_SIMC.Write()
H_q_SIMC.Write()
H_Q2_SIMC.Write()
H_epsilon_SIMC.Write()
H_MMp2_SIMC.Write()
H_th_SIMC.Write()
H_ph_SIMC.Write()
H_pmiss_SIMC.Write()
H_emiss_SIMC.Write()
H_pmx_SIMC.Write()
H_pmy_SIMC.Write()
H_pmz_SIMC.Write()
H_W_SIMC.Write()

outHistFile.Close()
InFile_DATA.Close()
InFile_DUMMY.Close()
InFile_SIMC.Close()
print ("Processing Complete")
