#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-01 00:44:53 trottar"
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

##################################################################################################################################################

# Check the number of arguments provided to the script
if len(sys.argv)-1!=4:
    print("!!!!! ERROR !!!!!\n Expected 4 arguments\n Usage is with - InDATAFilename InDUMMYFilename InSIMCFilename OutFilename \n!!!!! ERROR !!!!!")
    sys.exit(1)

##################################################################################################################################################

# Input params - run number and max number of events
InDATAFilename = sys.argv[1]
InDUMMYFilename = sys.argv[2]
InSIMCFilename = sys.argv[3]
OutFilename = sys.argv[4]

###############################################################################################################################################
ROOT.gROOT.SetBatch(ROOT.kTRUE) # Set ROOT to batch mode explicitly, does not splash anything to screen
###############################################################################################################################################

'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 

# Add this to all files for more dynamic pathing
USER =  lt.SetPath(os.path.realpath(__file__)).getPath("USER") # Grab user info for file finding
HOST = lt.SetPath(os.path.realpath(__file__)).getPath("HOST")
UTILPATH = lt.SetPath(os.path.realpath(__file__)).getPath("UTILPATH")
SIMCPATH = lt.SetPath(os.path.realpath(__file__)).getPath("SIMCPATH")
REPLAYPATH = SIMCPATH
ROOTfilePath = "%s/OUTPUTS" % REPLAYPATH
OutPath = "%s/OUTPUTS" % REPLAYPATH

rootFile = ROOTfilePath+"/"+InDATAFilename
rootFile_DUMMY = ROOTfilePath+"/"+InDUMMYFilename
rootFile_SIMC = ROOTfilePath+"/"+InSIMCFilename

foutname = OutPath+"/" + OutFilename + ".root"
fouttxt  = OutPath+"/" + OutFilename + ".txt"
outputpdf  = OutPath+"/" + OutFilename + ".pdf"

simc_hist = "%s/OUTPUTS/Heep_Coin_10p6.hist" % REPLAYPATH
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
else:
    print("ERROR: Invalid simc hist file %s" % simc_hist)
    sys.exit(1)
    
################################################################################################################################################

InFile_DATA = ROOT.TFile.Open(rootFile, "OPEN")
InFile_DUMMY = ROOT.TFile.Open(rootFile_DUMMY, "OPEN")
InFile_SIMC = ROOT.TFile.Open(rootFile_SIMC, "READ")

TBRANCH_DATA  = InFile_DATA.Get("hist")
nEntries_TBRANCH_DATA  = TBRANCH_DATA.GetEntries()
TBRANCH_DUMMY  = InFile_DUMMY.Get("hist")
nEntries_TBRANCH_DUMMY  = TBRANCH_DUMMY.GetEntries()
TBRANCH_SIMC  = InFile_SIMC.Get("h10")
nEntries_TBRANCH_SIMC  = TBRANCH_SIMC.GetEntries()

TSCALER_DATA  = up.open(rootFile)["scaler"]
TSCALER_DUMMY  = up.open(rootFile_DUMMY)["scaler"]

################################################################################################################################################

thres_curr = 2.5

NBCM = 5

# Data charge calculation
bcm1_charge_DATA = TSCALER_DATA.array("bcm1_charge")
bcm2_charge_DATA = TSCALER_DATA.array("bcm2_charge")
bcm4a_charge_DATA = TSCALER_DATA.array("bcm4a_charge")
bcm4b_charge_DATA = TSCALER_DATA.array("bcm4b_charge")
bcm4c_charge_DATA = TSCALER_DATA.array("bcm4c_charge")

bcm1_current_DATA = TSCALER_DATA.array("bcm1_current")
bcm2_current_DATA = TSCALER_DATA.array("bcm2_current")
bcm4a_current_DATA = TSCALER_DATA.array("bcm4a_current")
bcm4b_current_DATA = TSCALER_DATA.array("bcm4b_current")
bcm4c_current_DATA = TSCALER_DATA.array("bcm4c_current")

s_evts_DATA = bcm1_charge_DATA

bcm_value_DATA  = [bcm1_charge_DATA, bcm2_charge_DATA, bcm4a_charge_DATA, bcm4b_charge_DATA, bcm4c_charge_DATA]

charge_sum_DATA = [0]*NBCM
previous_charge_DATA = [0]*NBCM

current_DATA  = [bcm1_current_DATA, bcm2_current_DATA, bcm4a_current_DATA, bcm4b_current_DATA, bcm4c_current_DATA]

for ibcm in range(0, 5):
    previous_charge_DATA[ibcm] = bcm_value_DATA[ibcm][0]
    # Iterate over all scaler events to get various scaler values
    for i, evt in enumerate(s_evts_DATA):
        if (current_DATA[ibcm][i] > thres_curr ):
            # Iterate over current value then subtracting previous so that there is no double counting. Subtracted values are uncut.
            charge_sum_DATA[ibcm] += (bcm_value_DATA[ibcm][i] - previous_charge_DATA[ibcm])
        previous_charge_DATA[ibcm] = bcm_value_DATA[ibcm][i]
        
data_charge = charge_sum_DATA[0]/100
        
# Dummy charge calculation
bcm1_charge_DUMMY = TSCALER_DUMMY.array("bcm1_charge")
bcm2_charge_DUMMY = TSCALER_DUMMY.array("bcm2_charge")
bcm4a_charge_DUMMY = TSCALER_DUMMY.array("bcm4a_charge")
bcm4b_charge_DUMMY = TSCALER_DUMMY.array("bcm4b_charge")
bcm4c_charge_DUMMY = TSCALER_DUMMY.array("bcm4c_charge")

bcm1_current_DUMMY = TSCALER_DUMMY.array("bcm1_current")
bcm2_current_DUMMY = TSCALER_DUMMY.array("bcm2_current")
bcm4a_current_DUMMY = TSCALER_DUMMY.array("bcm4a_current")
bcm4b_current_DUMMY = TSCALER_DUMMY.array("bcm4b_current")
bcm4c_current_DUMMY = TSCALER_DUMMY.array("bcm4c_current")

s_evts_DUMMY = bcm1_charge_DUMMY

bcm_value_DUMMY  = [bcm1_charge_DUMMY, bcm2_charge_DUMMY, bcm4a_charge_DUMMY, bcm4b_charge_DUMMY, bcm4c_charge_DUMMY]

charge_sum_DUMMY = [0]*NBCM
previous_charge_DUMMY = [0]*NBCM

current_DUMMY  = [bcm1_current_DUMMY, bcm2_current_DUMMY, bcm4a_current_DUMMY, bcm4b_current_DUMMY, bcm4c_current_DUMMY]

for ibcm in range(0, 5):
    previous_charge_DUMMY[ibcm] = bcm_value_DUMMY[ibcm][0]
    # Iterate over all scaler events to get various scaler values
    for i, evt in enumerate(s_evts_DUMMY):
        if (current_DUMMY[ibcm][i] > thres_curr ):
            # Iterate over current value then subtracting previous so that there is no double counting. Subtracted values are uncut.
            charge_sum_DUMMY[ibcm] += (bcm_value_DUMMY[ibcm][i] - previous_charge_DUMMY[ibcm])
        previous_charge_DUMMY[ibcm] = bcm_value_DUMMY[ibcm][i]
        
dummy_charge = charge_sum_DUMMY[0]/100

print("\ndata_charge = ",data_charge,"\ndummy_charge = ",dummy_charge,"\n\n")

################################################################################################################################################
  
H_hsdelta_DATA  = ROOT.TH1D("H_hsdelta_DATA","HMS Delta", 300, -20.0, 20.0)
H_hsdelta_DUMMY  = ROOT.TH1D("H_hsdelta_DUMMY","HMS Delta", 300, -20.0, 20.0)
H_hsdelta_SIMC  = ROOT.TH1D("H_hsdelta_SIMC","HMS Delta", 300, -20.0, 20.0)

H_hsxptar_DATA  = ROOT.TH1D("H_hsxptar_DATA","HMS xptar", 300, -0.1, 0.1)
H_hsxptar_DUMMY  = ROOT.TH1D("H_hsxptar_DUMMY","HMS xptar", 300, -0.1, 0.1)
H_hsxptar_SIMC  = ROOT.TH1D("H_hsxptar_SIMC","HMS xptar", 300, -0.1, 0.1)

H_hsyptar_DATA  = ROOT.TH1D("H_hsyptar_DATA","HMS yptar", 300, -0.1, 0.1)
H_hsyptar_DUMMY  = ROOT.TH1D("H_hsyptar_DUMMY","HMS yptar", 300, -0.1, 0.1)
H_hsyptar_SIMC  = ROOT.TH1D("H_hsyptar_SIMC","HMS yptar", 300, -0.1, 0.1)

H_ssxfp_DATA    = ROOT.TH1D("H_ssxfp_DATA","SHMS xfp", 300, -20.0, 20.0)
H_ssxfp_DUMMY    = ROOT.TH1D("H_ssxfp_DUMMY","SHMS xfp", 300, -20.0, 20.0)
H_ssxfp_SIMC    = ROOT.TH1D("H_ssxfp_SIMC","SHMS xfp", 300, -20.0, 20.0)

H_ssyfp_DATA    = ROOT.TH1D("H_ssyfp_DATA","SHMS yfp", 300, -20.0, 20.0)
H_ssyfp_DUMMY    = ROOT.TH1D("H_ssyfp_DUMMY","SHMS yfp", 300, -20.0, 20.0)
H_ssyfp_SIMC    = ROOT.TH1D("H_ssyfp_SIMC","SHMS yfp", 300, -20.0, 20.0)

H_ssxpfp_DATA   = ROOT.TH1D("H_ssxpfp_DATA","SHMS xpfp", 300, -0.09, 0.09)
H_ssxpfp_DUMMY   = ROOT.TH1D("H_ssxpfp_DUMMY","SHMS xpfp", 300, -0.09, 0.09)
H_ssxpfp_SIMC   = ROOT.TH1D("H_ssxpfp_SIMC","SHMS xpfp", 300, -0.09, 0.09)

H_ssypfp_DATA   = ROOT.TH1D("H_ssypfp_DATA","SHMS ypfp", 300, -0.05, 0.04)
H_ssypfp_DUMMY   = ROOT.TH1D("H_ssypfp_DUMMY","SHMS ypfp", 300, -0.05, 0.04)
H_ssypfp_SIMC   = ROOT.TH1D("H_ssypfp_SIMC","SHMS ypfp", 300, -0.05, 0.04)

H_hsxfp_DATA    = ROOT.TH1D("H_hsxfp_DATA","HMS xfp", 300, -40.0, 40.0)
H_hsxfp_DUMMY    = ROOT.TH1D("H_hsxfp_DUMMY","HMS xfp", 300, -40.0, 40.0)
H_hsxfp_SIMC    = ROOT.TH1D("H_hsxfp_SIMC","HMS xfp", 300, -40.0, 40.0)

H_hsyfp_DATA    = ROOT.TH1D("H_hsyfp_DATA","HMS yfp", 300, -20.0, 20.0)
H_hsyfp_DUMMY    = ROOT.TH1D("H_hsyfp_DUMMY","HMS yfp", 300, -20.0, 20.0)
H_hsyfp_SIMC    = ROOT.TH1D("H_hsyfp_SIMC","HMS yfp", 300, -20.0, 20.0)

H_hsxpfp_DATA   = ROOT.TH1D("H_hsxpfp_DATA","HMS xpfp", 300, -0.09, 0.05)
H_hsxpfp_DUMMY   = ROOT.TH1D("H_hsxpfp_DUMMY","HMS xpfp", 300, -0.09, 0.05)
H_hsxpfp_SIMC   = ROOT.TH1D("H_hsxpfp_SIMC","HMS xpfp", 300, -0.09, 0.05)

H_hsypfp_DATA   = ROOT.TH1D("H_hsypfp_DATA","HMS ypfp", 300, -0.05, 0.04)
H_hsypfp_DUMMY   = ROOT.TH1D("H_hsypfp_DUMMY","HMS ypfp", 300, -0.05, 0.04)
H_hsypfp_SIMC   = ROOT.TH1D("H_hsypfp_SIMC","HMS ypfp", 300, -0.05, 0.04)

H_ssdelta_DATA  = ROOT.TH1D("H_ssdelta_DATA","SHMS delta", 300, -20.0, 20.0)
H_ssdelta_DUMMY  = ROOT.TH1D("H_ssdelta_DUMMY","SHMS delta", 300, -20.0, 20.0)
H_ssdelta_SIMC  = ROOT.TH1D("H_ssdelta_SIMC","SHMS delta", 300, -20.0, 20.0)

H_ssxptar_DATA  = ROOT.TH1D("H_ssxptar_DATA","SHMS xptar", 300, -0.1, 0.1)
H_ssxptar_DUMMY  = ROOT.TH1D("H_ssxptar_DUMMY","SHMS xptar", 300, -0.1, 0.1)
H_ssxptar_SIMC  = ROOT.TH1D("H_ssxptar_SIMC","SHMS xptar", 300, -0.1, 0.1)

H_ssyptar_DATA  = ROOT.TH1D("H_ssyptar_DATA","SHMS yptar", 300, -0.04, 0.04)
H_ssyptar_DUMMY  = ROOT.TH1D("H_ssyptar_DUMMY","SHMS yptar", 300, -0.04, 0.04)
H_ssyptar_SIMC  = ROOT.TH1D("H_ssyptar_SIMC","SHMS yptar", 300, -0.04, 0.04)

H_q_DATA        = ROOT.TH1D("H_q_DATA","q", 300, 5.0, 7.0)
H_q_DUMMY        = ROOT.TH1D("H_q_DUMMY","q", 300, 5.0, 7.0)
H_q_SIMC        = ROOT.TH1D("H_q_SIMC","q", 300, 5.0, 7.0)

H_Q2_DATA       = ROOT.TH1D("H_Q2_DATA","Q2", 300, 1.5, 8.0)  
H_Q2_DUMMY       = ROOT.TH1D("H_Q2_DUMMY","Q2", 300, 1.5, 8.0)  
H_Q2_SIMC       = ROOT.TH1D("H_Q2_SIMC","Q2", 300, 1.5, 8.0)  

H_epsilon_DATA  = ROOT.TH1D("H_epsilon_DATA","epsilon", 300, 0.5, 1.0)
H_epsilon_DUMMY  = ROOT.TH1D("H_epsilon_DUMMY","epsilon", 300, 0.5, 1.0)
H_epsilon_SIMC  = ROOT.TH1D("H_epsilon_SIMC","epsilon", 300, 0.5, 1.0)

H_MMp_DATA  = ROOT.TH1D("H_MMp_DATA","MMp ", 300, -0.055, 0.055)
H_MMp_DUMMY  = ROOT.TH1D("H_MMp_DUMMY","MMp ", 300, -0.055, 0.055)
H_MMp_SIMC  = ROOT.TH1D("H_MMp_SIMC","MMp ", 300, -0.055, 0.055)

H_th_DATA  = ROOT.TH1D("H_th_DATA","X' tar", 300, -0.1, 0.1)
H_th_DUMMY  = ROOT.TH1D("H_th_DUMMY","X' tar", 300, -0.1, 0.1)
H_th_SIMC  = ROOT.TH1D("H_th_SIMC","X' tar", 300, -0.1, 0.1)

H_ph_DATA  = ROOT.TH1D("H_ph_DATA","Y' tar", 300, -0.1, 0.1)
H_ph_DUMMY  = ROOT.TH1D("H_ph_DUMMY","Y' tar", 300, -0.1, 0.1)
H_ph_SIMC  = ROOT.TH1D("H_ph_SIMC","Y' tar", 300, -0.1, 0.1)

H_pmiss_DATA  = ROOT.TH1D("H_pmiss_DATA","pmiss", 300, -0.1, 0.4)
H_pmiss_DUMMY  = ROOT.TH1D("H_pmiss_DUMMY","pmiss", 300, -0.1, 0.4)
H_pmiss_SIMC  = ROOT.TH1D("H_pmiss_SIMC","pmiss", 300, -0.1, 0.4)

H_emiss_DATA  = ROOT.TH1D("H_emiss_DATA","emiss", 300, -0.1, 0.4)
H_emiss_DUMMY  = ROOT.TH1D("H_emiss_DUMMY","emiss", 300, -0.1, 0.4)
H_emiss_SIMC  = ROOT.TH1D("H_emiss_SIMC","emiss", 300, -0.1, 0.4)

H_pmx_DATA  = ROOT.TH1D("H_pmx_DATA","pmx", 300, -0.2, 0.2)
H_pmx_DUMMY  = ROOT.TH1D("H_pmx_DUMMY","pmx", 300, -0.2, 0.2)
H_pmx_SIMC  = ROOT.TH1D("H_pmx_SIMC","pmx", 300, -0.2, 0.2)

H_pmy_DATA  = ROOT.TH1D("H_pmy_DATA","pmy ", 300, -0.2, 0.2)
H_pmy_DUMMY  = ROOT.TH1D("H_pmy_DUMMY","pmy ", 300, -0.2, 0.2)
H_pmy_SIMC  = ROOT.TH1D("H_pmy_SIMC","pmy", 300, -0.2, 0.2)

H_pmz_DATA  = ROOT.TH1D("H_pmz_DATA","pmz", 300, -0.2, 0.2)
H_pmz_DUMMY  = ROOT.TH1D("H_pmz_DUMMY","pmz", 300, -0.2, 0.2)
H_pmz_SIMC  = ROOT.TH1D("H_pmz_SIMC","pmz", 300, -0.2, 0.2)

H_W_DATA  = ROOT.TH1D("H_W_DATA","W ", 300, 0.5, 1.5)
H_W_DUMMY  = ROOT.TH1D("H_W_DUMMY","W ", 300, 0.5, 1.5)
H_W_SIMC  = ROOT.TH1D("H_W_SIMC","W", 300, 0.5, 1.5)

################################################################################################################################################

for evt in TBRANCH_SIMC:

  # Define the acceptance cuts  

  # Select the cuts
  #HMS
  CUT1 = (evt.hsdelta >=-8.0) & (evt.hsdelta <=8.0)
  CUT2 = (evt.hsxptar >=-0.08) & (evt.hsxpfp <=0.08)
  CUT3 = (evt.hsyptar >=-0.045) & (evt.hsypfp <=0.045)

  #SHMS    
  CUT4 = (evt.ssdelta >=-10.0) & (evt.hsdelta <=20.0)
  CUT5 = (evt.ssxptar >=-0.06) & (evt.hsxpfp <=0.06)
  CUT6 = (evt.hsyptar >=-0.04) & (evt.hsypfp <=0.04)

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
      H_MMp_SIMC.Fill(np.sqrt(pow(evt.Em, 2) - pow(evt.Pm, 2)), evt.Weight)
    
for evt in TBRANCH_DATA:

  #CUTs Definations 
  SHMS_FixCut = (evt.P_hod_goodstarttime == 1) & (evt.P_dc_InsideDipoleExit == 1) # & P_hod_betanotrack > 0.5 & P_hod_betanotrack < 1.4
  SHMS_Acceptance = (evt.P_gtr_dp>=-10.0) & (evt.P_gtr_dp<=20.0) & (evt.P_gtr_xptar>=-0.06) & (evt.P_gtr_xptar<=0.06) & (evt.P_gtr_yptar>=-0.04) & (evt.P_gtr_yptar<=0.04)
  SHMS_ELECTRON_PID = (evt.P_cal_etottracknorm >= 0.85) & (evt.P_cal_etottracknorm <= 1.2) # evt.P_hgcer_npeSum >=0.5 & evt.P_aero_npeSum >=0.5

  HMS_FixCut = (evt.H_hod_goodscinhit == 1) & (evt.H_hod_goodstarttime == 1) & (evt.H_dc_InsideDipoleExit == 1)
  HMS_Acceptance = (evt.H_gtr_dp>=-8.0) & (evt.H_gtr_dp<=8.0) & (evt.H_gtr_xptar>=-0.08) & (evt.H_gtr_xptar<=0.08) & (evt.H_gtr_yptar>=-0.045) & (evt.H_gtr_yptar<=0.045)       
  HMS_ELECTRON_PID = (evt.H_cer_npeSum >=0.5) & (evt.H_cal_etotnorm >=0.8) & (evt.H_cal_etotnorm <=1.2)

  #........................................

  #if(SHMS_FixCut & SHMS_Acceptance & SHMS_ELECTRON_PID) 
  if(SHMS_FixCut & SHMS_Acceptance):
    
      H_ssxfp_DATA.Fill(evt.ssxfp)
      H_ssyfp_DATA.Fill(evt.ssyfp)
      H_ssxpfp_DATA.Fill(evt.ssxpfp)
      H_ssypfp_DATA.Fill(evt.ssypfp)
      H_ssdelta_DATA.Fill(evt.ssdelta)
      H_ssxptar_DATA.Fill(evt.ssxptar)
      H_ssyptar_DATA.Fill(evt.ssyptar)

    

  #if(HMS_FixCut & HMS_Acceptance & HMS_ELECTRON_PID)
  if(HMS_FixCut & HMS_Acceptance):
    
      H_pmiss_DATA.Fill(evt.pmiss)	
      H_emiss_DATA.Fill(evt.emiss)	
      H_pmx_DATA.Fill(evt.pmx)
      H_pmy_DATA.Fill(evt.pmy)
      H_pmz_DATA.Fill(evt.pmz)
      H_Q2_DATA.Fill(evt.Q2)
      H_W_DATA.Fill(evt.W)
      H_epsilon_DATA.Fill(evt.epsilon)
      H_MMp_DATA.Fill((pow(evt.emiss, 2) - pow(evt.pmiss, 2)))  
      #H_MMp_DATA.Fill(evt.MMp)  

      H_hsxfp_DATA.Fill(evt.hsxfp)
      H_hsyfp_DATA.Fill(evt.hsyfp)
      H_hsxpfp_DATA.Fill(evt.hsxpfp)
      H_hsypfp_DATA.Fill(evt.hsypfp)
      H_hsdelta_DATA.Fill(evt.hsdelta)
      H_hsxptar_DATA.Fill(evt.hsxptar)	
      H_hsyptar_DATA.Fill(evt.hsyptar)

for evt in TBRANCH_DUMMY:

  #......... Define Cuts.................

  #CUTs Definations 
  SHMS_FixCut = (evt.P_hod_goodstarttime == 1) & (evt.P_dc_InsideDipoleExit == 1) # & evt.P_hod_betanotrack > 0.5 & evt.P_hod_betanotrack < 1.4
  SHMS_Acceptance = (evt.P_gtr_dp>=-10.0) & (evt.P_gtr_dp<=20.0) & (evt.P_gtr_xptar>=-0.06) & (evt.P_gtr_xptar<=0.06) & (evt.P_gtr_yptar>=-0.04) & (evt.P_gtr_yptar<=0.04)
  SHMS_ELECTRON_PID = (evt.P_cal_etottracknorm >= 0.85) & (evt.P_cal_etottracknorm <= 1.2) # evt.P_hgcer_npeSum >=0.5 & evt.P_aero_npeSum >=0.5

  HMS_FixCut = (evt.H_hod_goodscinhit == 1) & (evt.H_hod_goodstarttime == 1) & (evt.H_dc_InsideDipoleExit == 1)
  HMS_Acceptance = (evt.H_gtr_dp>=-8.0) & (evt.H_gtr_dp<=8.0) & (evt.H_gtr_xptar>=-0.08) & (evt.H_gtr_xptar<=0.08) & (evt.H_gtr_yptar>=-0.045) & (evt.H_gtr_yptar<=0.045)       
  HMS_ELECTRON_PID = (evt.H_cer_npeSum >=0.5) & (evt.H_cal_etotnorm >=0.8) & (evt.H_cal_etotnorm <=1.2)
  
  #........................................

  #if(SHMS_FixCut & SHMS_Acceptance & SHMS_ELECTRON_PID) 
  if(SHMS_FixCut & SHMS_Acceptance):
    
      H_ssxfp_DUMMY.Fill(evt.ssxfp)
      H_ssyfp_DUMMY.Fill(evt.ssyfp)
      H_ssxpfp_DUMMY.Fill(evt.ssxpfp)
      H_ssypfp_DUMMY.Fill(evt.ssypfp)
      H_ssdelta_DUMMY.Fill(evt.ssdelta)
      H_ssxptar_DUMMY.Fill(evt.ssxptar)
      H_ssyptar_DUMMY.Fill(evt.ssyptar)

    

  #if(HMS_FixCut & HMS_Acceptance & HMS_ELECTRON_PID)
  if(HMS_FixCut & HMS_Acceptance):
    
      H_pmiss_DUMMY.Fill(evt.pmiss)	
      H_emiss_DUMMY.Fill(evt.emiss)	
      H_pmx_DUMMY.Fill(evt.pmx)
      H_pmy_DUMMY.Fill(evt.pmy)
      H_pmz_DUMMY.Fill(evt.pmz)
      H_Q2_DUMMY.Fill(evt.Q2)
      H_W_DUMMY.Fill(evt.W)
      H_epsilon_DUMMY.Fill(evt.epsilon)
      H_MMp_DUMMY.Fill((pow(evt.emiss, 2) - pow(evt.pmiss, 2)))  
      #H_MMp_DUMMY.Fill(evt.MMp)  

      H_hsxfp_DUMMY.Fill(evt.hsxfp)
      H_hsyfp_DUMMY.Fill(evt.hsyfp)
      H_hsxpfp_DUMMY.Fill(evt.hsxpfp)
      H_hsypfp_DUMMY.Fill(evt.hsypfp)
      H_hsdelta_DUMMY.Fill(evt.hsdelta)
      H_hsxptar_DUMMY.Fill(evt.hsxptar)	
      H_hsyptar_DUMMY.Fill(evt.hsyptar)
    
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
H_MMp_SIMC.Scale(normfac_simc)

dummy_target_corr = 4.8579
normfac_dummy = 1/(dummy_charge*dummy_target_corr)
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
H_MMp_DUMMY.Scale(normfac_dummy)
H_pmiss_DUMMY.Scale(normfac_dummy)
H_emiss_DUMMY.Scale(normfac_dummy)
H_pmx_DUMMY.Scale(normfac_dummy)
H_pmy_DUMMY.Scale(normfac_dummy)
H_pmz_DUMMY.Scale(normfac_dummy)
H_W_DUMMY.Scale(normfac_dummy)

normfac_data = 1/(data_charge)
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
H_MMp_DATA.Scale(normfac_data)
H_pmiss_DATA.Scale(normfac_data)
H_emiss_DATA.Scale(normfac_data)
H_pmx_DATA.Scale(normfac_data)
H_pmy_DATA.Scale(normfac_data)
H_pmz_DATA.Scale(normfac_data)
H_W_DATA.Scale(normfac_data)

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
H_MMp_DATA.Add(H_MMp_DUMMY,-1)
H_pmiss_DATA.Add(H_pmiss_DUMMY,-1)
H_emiss_DATA.Add(H_emiss_DUMMY,-1)
H_pmx_DATA.Add(H_pmx_DUMMY,-1)
H_pmy_DATA.Add(H_pmy_DUMMY,-1)
H_pmz_DATA.Add(H_pmz_DUMMY,-1)
H_W_DATA.Add(H_W_DUMMY,-1)

################################################################################################################################################

ROOT.gStyle.SetOptStat(0)

# PLOT HIST..

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

xfp.Print(outputpdf + '(')

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

CMMp = TCanvas()
l_MMp = ROOT.TLegend(0.115,0.735,0.33,0.9)


H_MMp_DATA.SetLineColor(kRed)
H_MMp_SIMC.Draw("")
H_MMp_DATA.Draw("same")

b_int_MMp_simc = int(H_MMp_SIMC.Integral())
b_int_MMp_data = int(H_MMp_DATA.Integral())

l_MMp.AddEntry(H_MMp_SIMC,"SIMC, INT = %s" % b_int_MMp_simc)
l_MMp.AddEntry(H_MMp_DATA,"DATA, INT = %s" % b_int_MMp_data)

l_MMp.Draw()

CMMp.Print(outputpdf)

Cpmiss = TCanvas()
l_pmiss = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmiss_DATA.SetLineColor(kRed)
H_pmiss_SIMC.Draw("")
H_pmiss_DATA.Draw("same")

b_int_pmiss_simc = int(H_pmiss_SIMC.Integral())
b_int_pmiss_data = int(H_pmiss_DATA.Integral())

l_pmiss.AddEntry(H_pmiss_SIMC,"SIMC, INT = %s" % b_int_pmiss_simc)
l_pmiss.AddEntry(H_pmiss_DATA,"DATA, INT = %s" % b_int_pmiss_data)

l_pmiss.Draw()

Cpmiss.Print(outputpdf)

Cemiss = TCanvas()
l_emiss = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_emiss_DATA.SetLineColor(kRed)
H_emiss_SIMC.Draw("")
H_emiss_DATA.Draw("same")

b_int_emiss_simc = int(H_emiss_SIMC.Integral())
b_int_emiss_data = int(H_emiss_DATA.Integral())

l_emiss.AddEntry(H_emiss_SIMC,"SIMC, INT = %s" % b_int_emiss_simc)
l_emiss.AddEntry(H_emiss_DATA,"DATA, INT = %s" % b_int_emiss_data)

l_emiss.Draw()

Cemiss.Print(outputpdf)

Cpmiss_x = TCanvas()
l_pmx = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmx_DATA.SetLineColor(kRed)
H_pmx_SIMC.Draw("")
H_pmx_DATA.Draw("same")

b_int_pmx_simc = int(H_pmx_SIMC.Integral())
b_int_pmx_data = int(H_pmx_DATA.Integral())

l_pmx.AddEntry(H_pmx_SIMC,"SIMC, INT = %s" % b_int_pmx_simc)
l_pmx.AddEntry(H_pmx_DATA,"DATA, INT = %s" % b_int_pmx_data)

l_pmx.Draw()

Cpmiss_x.Print(outputpdf)

Cpmiss_y = TCanvas()
l_pmy = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmy_DATA.SetLineColor(kRed)
H_pmy_SIMC.Draw("")
H_pmy_DATA.Draw("same")

b_int_pmy_simc = int(H_pmy_SIMC.Integral())
b_int_pmy_data = int(H_pmy_DATA.Integral())

l_pmy.AddEntry(H_pmy_SIMC,"SIMC, INT = %s" % b_int_pmy_simc)
l_pmy.AddEntry(H_pmy_DATA,"DATA, INT = %s" % b_int_pmy_data)

l_pmy.Draw()

Cpmiss_y.Print(outputpdf)

Cpmiss_z = TCanvas()
l_pmz = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_pmz_DATA.SetLineColor(kRed)
H_pmz_SIMC.Draw("")
H_pmz_DATA.Draw("same")

b_int_pmz_simc = int(H_pmz_SIMC.Integral())
b_int_pmz_data = int(H_pmz_DATA.Integral())

l_pmz.AddEntry(H_pmz_SIMC,"SIMC, INT = %s" % b_int_pmz_simc)
l_pmz.AddEntry(H_pmz_DATA,"DATA, INT = %s" % b_int_pmz_data)

l_pmz.Draw()

Cpmiss_z.Print(outputpdf)

CW = TCanvas()
l_W = ROOT.TLegend(0.115,0.735,0.33,0.9)

H_W_DATA.SetLineColor(kRed)
H_W_SIMC.Draw("")
H_W_DATA.Draw("same")

b_int_W_simc = int(H_W_SIMC.Integral())
b_int_W_data = int(H_W_DATA.Integral())

l_W.AddEntry(H_W_SIMC,"SIMC, INT = %s" % b_int_W_simc)
l_W.AddEntry(H_W_DATA,"DATA, INT = %s" % b_int_W_data)

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
H_MMp_DATA.Write()
H_th_DATA.Write()
H_ph_DATA.Write()
H_pmiss_DATA.Write()
H_emiss_DATA.Write()
H_pmx_DATA.Write()
H_pmy_DATA.Write()
H_pmz_DATA.Write()
H_W_DATA.Write()

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
H_MMp_DUMMY.Write()
H_th_DUMMY.Write()
H_ph_DUMMY.Write()
H_pmiss_DUMMY.Write()
H_emiss_DUMMY.Write()
H_pmx_DUMMY.Write()
H_pmy_DUMMY.Write()
H_pmz_DUMMY.Write()
H_W_DUMMY.Write()

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
H_MMp_SIMC.Write()
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
