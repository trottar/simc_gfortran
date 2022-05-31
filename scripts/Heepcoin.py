#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-05-31 12:12:00 trottar"
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

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''

# Import package for cuts
import ltsep as lt 

# Add this to all files for more dynamic pathing
USER =  lt.SetPath(os.path.realpath(__file__)).getPath("USER") # Grab user info for file finding
HOST = lt.SetPath(os.path.realpath(__file__)).getPath("HOST")
UTILPATH = lt.SetPath(os.path.realpath(__file__)).getPath("UTILPATH")
REPLAYPATH = "/group/c-kaonlt/USERS/%s/simc_gfortran" % USER
ROOTfilePath = "%s/OUTPUTS/" % REPLAYPATH
OutPath = "%s/OUTPUTS/" % REPLAYPATH

rootFile = ROOTfilePath+"/"+InDATAFilename
rootFile_DUMMY = ROOTfilePath+"/"+InDUMMYFilename
rootFile_SIMC = ROOTfilePath+"/"+InSIMCFilename

foutname = OutPath+"/" + OutFilename + ".root"
fouttxt  = OutPath+"/" + OutFilename + ".txt"
outputpdf  = OutPath+"/" + OutFilename + ".pdf"

################################################################################################################################################

InFile_DATA = up.open(rootFile)
InFile_DUMMY = up.open(rootFile_DUMMY)
InFile_SIMC = up.open(rootFile_SIMC)

TBRANCH_DATA  = InFile_DATA["hist"]
nEntries_TBRANCH_DATA  = len(TBRANCH_DATA)
TBRANCH_DUMMY  = InFile_DUMMY["hist"]
nEntries_TBRANCH_DUMMY  = len(TBRANCH_DUMMY)
TBRANCH_SIMC  = InFile_SIMC["h10"]
nEntries_TBRANCH_SIMC  = len(TBRANCH_SIMC)

################################################################################################################################################
  
# SIMC variables
# HMS
hsdelta = TBRANCH_SIMC.array("hsdelta")
hsxptar = TBRANCH_SIMC.array("hsxptar")
hsyptar = TBRANCH_SIMC.array("hsyptar")
hsxfp = TBRANCH_SIMC.array("hsxfp")
hsyfp = TBRANCH_SIMC.array("hsyfp")
hsxpfp = TBRANCH_SIMC.array("hsxpfp")
hsypfp = TBRANCH_SIMC.array("hsypfp")
# SHMS
ssdelta = TBRANCH_SIMC.array("ssdelta")
ssxptar = TBRANCH_SIMC.array("ssxptar")
ssyptar = TBRANCH_SIMC.array("ssyptar")
ssxfp = TBRANCH_SIMC.array("ssxfp")
ssyfp = TBRANCH_SIMC.array("ssyfp")
ssxpfp = TBRANCH_SIMC.array("ssxpfp")
ssypfp = TBRANCH_SIMC.array("ssypfp")

q = TBRANCH_SIMC.array("q")
Q2 = TBRANCH_SIMC.array("Q2")
W = TBRANCH_SIMC.array("W")
epsilon = TBRANCH_SIMC.array("epsilon")
Pmx = TBRANCH_SIMC.array("Pmx")
Pmy = TBRANCH_SIMC.array("Pmy")
Pmz = TBRANCH_SIMC.array("Pmz")
Em = TBRANCH_SIMC.array("Em")
Pm = TBRANCH_SIMC.array("Pm")
Weight = TBRANCH_SIMC.array("Weight")

# DATA variables
# HMS
hsdelta_data = TBRANCH_DATA.array("hsdelta")
hsxptar_data = TBRANCH_DATA.array("hsxptar")
hsyptar_data = TBRANCH_DATA.array("hsyptar")
hsxfp_data = TBRANCH_DATA.array("hsxfp")
hsyfp_data = TBRANCH_DATA.array("hsyfp")
hsxpfp_data = TBRANCH_DATA.array("hsxpfp")
hsypfp_data = TBRANCH_DATA.array("hsypfp")
# SHMS
ssdelta_data = TBRANCH_DATA.array("ssdelta")
ssxptar_data = TBRANCH_DATA.array("ssxptar")
ssyptar_data = TBRANCH_DATA.array("ssyptar")
ssxfp_data = TBRANCH_DATA.array("ssxfp")
ssyfp_data = TBRANCH_DATA.array("ssyfp")
ssxpfp_data = TBRANCH_DATA.array("ssxpfp")
ssypfp_data = TBRANCH_DATA.array("ssypfp")

Q2_data = TBRANCH_DATA.array("Q2")
W_data = TBRANCH_DATA.array("W")
epsilon_data = TBRANCH_DATA.array("epsilon")
pmx_data = TBRANCH_DATA.array("pmx")
pmy_data = TBRANCH_DATA.array("pmy")
pmz_data = TBRANCH_DATA.array("pmz")
em_data = TBRANCH_DATA.array("emiss")
pm_data = TBRANCH_DATA.array("pmiss")
MMp_data = TBRANCH_DATA.array("MMp")

P_hod_goodstarttime_data = TBRANCH_DATA.array("P_hod_goodstarttime")  
P_dc_InsideDipoleExit_data = TBRANCH_DATA.array("P_dc_InsideDipoleExit")
P_gtr_xptar_data = TBRANCH_DATA.array("P_gtr_xptar")  
P_gtr_dp_data = TBRANCH_DATA.array("P_gtr_dp")
P_gtr_yptar_data = TBRANCH_DATA.array("P_gtr_yptar")    
P_cal_etottracknorm_data = TBRANCH_DATA.array("P_cal_etottracknorm")  

H_hod_goodscinhit_data = TBRANCH_DATA.array("H_hod_goodscinhit")  
H_hod_goodstarttime_data = TBRANCH_DATA.array("H_hod_goodstarttime")  
H_dc_InsideDipoleExit_data = TBRANCH_DATA.array("H_dc_InsideDipoleExit")
H_gtr_dp_data = TBRANCH_DATA.array("H_gtr_dp")
H_gtr_xptar_data = TBRANCH_DATA.array("H_gtr_xptar")  
H_gtr_yptar_data = TBRANCH_DATA.array("H_gtr_yptar")  
H_cer_npeSum_data = TBRANCH_DATA.array("H_cer_npeSum")
H_cal_etotnorm_data = TBRANCH_DATA.array("H_cal_etotnorm")  

# DUMMY variables
# HMS
hsdelta_dummy = TBRANCH_DUMMY.array("hsdelta")
hsxptar_dummy = TBRANCH_DUMMY.array("hsxptar")
hsyptar_dummy = TBRANCH_DUMMY.array("hsyptar")
hsxfp_dummy = TBRANCH_DUMMY.array("hsxfp")
hsyfp_dummy = TBRANCH_DUMMY.array("hsyfp")
hsxpfp_dummy = TBRANCH_DUMMY.array("hsxpfp")
hsypfp_dummy = TBRANCH_DUMMY.array("hsypfp")
# SHMS
ssdelta_dummy = TBRANCH_DUMMY.array("ssdelta")
ssxptar_dummy = TBRANCH_DUMMY.array("ssxptar")
ssyptar_dummy = TBRANCH_DUMMY.array("ssyptar")
ssxfp_dummy = TBRANCH_DUMMY.array("ssxfp")
ssyfp_dummy = TBRANCH_DUMMY.array("ssyfp")
ssxpfp_dummy = TBRANCH_DUMMY.array("ssxpfp")
ssypfp_dummy = TBRANCH_DUMMY.array("ssypfp")

Q2_dummy = TBRANCH_DUMMY.array("Q2")
W_dummy = TBRANCH_DUMMY.array("W")
epsilon_dummy = TBRANCH_DUMMY.array("epsilon")
pmx_dummy = TBRANCH_DUMMY.array("pmx")
pmy_dummy = TBRANCH_DUMMY.array("pmy")
pmz_dummy = TBRANCH_DUMMY.array("pmz")
em_dummy = TBRANCH_DUMMY.array("emiss")
pm_dummy = TBRANCH_DUMMY.array("pmiss")
MMp_dummy = TBRANCH_DUMMY.array("MMp")

P_hod_goodstarttime_dummy = TBRANCH_DUMMY.array("P_hod_goodstarttime")  
P_dc_InsideDipoleExit_dummy = TBRANCH_DUMMY.array("P_dc_InsideDipoleExit")
P_gtr_xptar_dummy = TBRANCH_DUMMY.array("P_gtr_xptar")  
P_gtr_dp_dummy = TBRANCH_DUMMY.array("P_gtr_dp")
P_gtr_yptar_dummy = TBRANCH_DUMMY.array("P_gtr_yptar")    
P_cal_etottracknorm_dummy = TBRANCH_DUMMY.array("P_cal_etottracknorm")  

H_hod_goodscinhit_dummy = TBRANCH_DUMMY.array("H_hod_goodscinhit")  
H_hod_goodstarttime_dummy = TBRANCH_DUMMY.array("H_hod_goodstarttime")  
H_dc_InsideDipoleExit_dummy = TBRANCH_DUMMY.array("H_dc_InsideDipoleExit")
H_gtr_dp_dummy = TBRANCH_DUMMY.array("H_gtr_dp")  
H_gtr_xptar_dummy = TBRANCH_DUMMY.array("H_gtr_xptar")  
H_gtr_yptar_dummy = TBRANCH_DUMMY.array("H_gtr_yptar")  
H_cer_npeSum_dummy = TBRANCH_DUMMY.array("H_cer_npeSum")
H_cal_etotnorm_dummy = TBRANCH_DUMMY.array("H_cal_etotnorm")

################################################################################################################################################
  
H_hsdelta_DATA  = ROOT.TH1D("H_hsdelta_DATA","HMS Delta hsdelta", 300, -20.0, 20.0)
H_hsdelta_DUMMY  = ROOT.TH1D("H_hsdelta_DUMMY","HMS Delta hsdelta", 300, -20.0, 20.0)
H_hsdelta_SIMC  = ROOT.TH1D("H_hsdelta_SIMC","HMS Delta hsdelta", 300, -20.0, 20.0)

H_hsxptar_DATA  = ROOT.TH1D("H_hsxptar_DATA","HMS xptar hsxptar", 300, -0.1, 0.1)
H_hsxptar_DUMMY  = ROOT.TH1D("H_hsxptar_DUMMY","HMS xptar hsxptar", 300, -0.1, 0.1)
H_hsxptar_SIMC  = ROOT.TH1D("H_hsxptar_SIMC","HMS xptar hsxptar", 300, -0.1, 0.1)

H_hsyptar_DATA  = ROOT.TH1D("H_hsyptar_DATA","HMS yptar hsyptar", 300, -0.1, 0.1)
H_hsyptar_DUMMY  = ROOT.TH1D("H_hsyptar_DUMMY","HMS yptar hsyptar", 300, -0.1, 0.1)
H_hsyptar_SIMC  = ROOT.TH1D("H_hsyptar_SIMC","HMS yptar hsyptar", 300, -0.1, 0.1)

H_ssxfp_DATA    = ROOT.TH1D("H_ssxfp_DATA","SHMS xfp ssxfp", 300, -20.0, 20.0)
H_ssxfp_DUMMY    = ROOT.TH1D("H_ssxfp_DUMMY","SHMS xfp ssxfp", 300, -20.0, 20.0)
H_ssxfp_SIMC    = ROOT.TH1D("H_ssxfp_SIMC","SHMS xfp ssxfp", 300, -20.0, 20.0)

H_ssyfp_DATA    = ROOT.TH1D("H_ssyfp_DATA","SHMS yfp ssyfp", 300, -20.0, 20.0)
H_ssyfp_DUMMY    = ROOT.TH1D("H_ssyfp_DUMMY","SHMS yfp ssyfp", 300, -20.0, 20.0)
H_ssyfp_SIMC    = ROOT.TH1D("H_ssyfp_SIMC","SHMS yfp ssyfp", 300, -20.0, 20.0)

H_ssxpfp_DATA   = ROOT.TH1D("H_ssxpfp_DATA","SHMS xpfp ssxpfp", 300, -0.09, 0.09)
H_ssxpfp_DUMMY   = ROOT.TH1D("H_ssxpfp_DUMMY","SHMS xpfp ssxpfp", 300, -0.09, 0.09)
H_ssxpfp_SIMC   = ROOT.TH1D("H_ssxpfp_SIMC","SHMS xpfp ssxpfp", 300, -0.09, 0.09)

H_ssypfp_DATA   = ROOT.TH1D("H_ssypfp_DATA","SHMS ypfp ssypfp", 300, -0.05, 0.04)
H_ssypfp_DUMMY   = ROOT.TH1D("H_ssypfp_DUMMY","SHMS ypfp ssypfp", 300, -0.05, 0.04)
H_ssypfp_SIMC   = ROOT.TH1D("H_ssypfp_SIMC","SHMS ypfp ssypfp", 300, -0.05, 0.04)

H_hsxfp_DATA    = ROOT.TH1D("H_hsxfp_DATA","HMS xfp hsxfp", 300, -40.0, 40.0)
H_hsxfp_DUMMY    = ROOT.TH1D("H_hsxfp_DUMMY","HMS xfp hsxfp", 300, -40.0, 40.0)
H_hsxfp_SIMC    = ROOT.TH1D("H_hsxfp_SIMC","HMS xfp hsxfp", 300, -40.0, 40.0)

H_hsyfp_DATA    = ROOT.TH1D("H_hsyfp_DATA","HMS yfp hsyfp", 300, -20.0, 20.0)
H_hsyfp_DUMMY    = ROOT.TH1D("H_hsyfp_DUMMY","HMS yfp hsyfp", 300, -20.0, 20.0)
H_hsyfp_SIMC    = ROOT.TH1D("H_hsyfp_SIMC","HMS yfp hsyfp", 300, -20.0, 20.0)

H_hsxpfp_DATA   = ROOT.TH1D("H_hsxpfp_DATA","HMS xpfp hsxpfp", 300, -0.09, 0.05)
H_hsxpfp_DUMMY   = ROOT.TH1D("H_hsxpfp_DUMMY","HMS xpfp hsxpfp", 300, -0.09, 0.05)
H_hsxpfp_SIMC   = ROOT.TH1D("H_hsxpfp_SIMC","HMS xpfp hsxpfp", 300, -0.09, 0.05)

H_hsypfp_DATA   = ROOT.TH1D("H_hsypfp_DATA","HMS ypfp hsypfp", 300, -0.05, 0.04)
H_hsypfp_DUMMY   = ROOT.TH1D("H_hsypfp_DUMMY","HMS ypfp hsypfp", 300, -0.05, 0.04)
H_hsypfp_SIMC   = ROOT.TH1D("H_hsypfp_SIMC","HMS ypfp hsypfp", 300, -0.05, 0.04)

H_ssdelta_DATA  = ROOT.TH1D("H_ssdelta_DATA","SHMS delta ssdelta", 300, -20.0, 20.0)
H_ssdelta_DUMMY  = ROOT.TH1D("H_ssdelta_DUMMY","SHMS delta ssdelta", 300, -20.0, 20.0)
H_ssdelta_SIMC  = ROOT.TH1D("H_ssdelta_SIMC","SHMS delta ssdelta", 300, -20.0, 20.0)

H_ssxptar_DATA  = ROOT.TH1D("H_ssxptar_DATA","SHMS xptar ssxptar", 300, -0.1, 0.1)
H_ssxptar_DUMMY  = ROOT.TH1D("H_ssxptar_DUMMY","SHMS xptar ssxptar", 300, -0.1, 0.1)
H_ssxptar_SIMC  = ROOT.TH1D("H_ssxptar_SIMC","SHMS xptar ssxptar", 300, -0.1, 0.1)

H_ssyptar_DATA  = ROOT.TH1D("H_ssyptar_DATA","SHMS yptar ssyptar", 300, -0.04, 0.04)
H_ssyptar_DUMMY  = ROOT.TH1D("H_ssyptar_DUMMY","SHMS yptar ssyptar", 300, -0.04, 0.04)
H_ssyptar_SIMC  = ROOT.TH1D("H_ssyptar_SIMC","SHMS yptar ssyptar", 300, -0.04, 0.04)

H_q_DATA        = ROOT.TH1D("H_q_DATA","q q", 300, 5.0, 7.0)
H_q_DUMMY        = ROOT.TH1D("H_q_DUMMY","q q", 300, 5.0, 7.0)
H_q_SIMC        = ROOT.TH1D("H_q_SIMC","q q", 300, 5.0, 7.0)

H_Q2_DATA       = ROOT.TH1D("H_Q2_DATA","Q2 Q2", 300, 1.5, 8.0)  
H_Q2_DUMMY       = ROOT.TH1D("H_Q2_DUMMY","Q2 Q2", 300, 1.5, 8.0)  
H_Q2_SIMC       = ROOT.TH1D("H_Q2_SIMC","Q2 Q2", 300, 1.5, 8.0)  

H_epsilon_DATA  = ROOT.TH1D("H_epsilon_DATA","epsilon epsilon", 300, 0.5, 1.0)
H_epsilon_DUMMY  = ROOT.TH1D("H_epsilon_DUMMY","epsilon epsilon", 300, 0.5, 1.0)
H_epsilon_SIMC  = ROOT.TH1D("H_epsilon_SIMC","epsilon epsilon", 300, 0.5, 1.0)

H_MMp_DATA  = ROOT.TH1D("H_MMp_DATA","MMp  MMp", 300, -0.005, 0.005)
H_MMp_DUMMY  = ROOT.TH1D("H_MMp_DUMMY","MMp  MMp", 300, -0.005, 0.005)
H_MMp_SIMC  = ROOT.TH1D("H_MMp_SIMC","MMp  MMp", 300, -0.005, 0.005)

H_th_DATA  = ROOT.TH1D("H_th_DATA","X' tar P_gtr_xp", 300, -0.1, 0.1)
H_th_DUMMY  = ROOT.TH1D("H_th_DUMMY","X' tar P_gtr_xp", 300, -0.1, 0.1)
H_th_SIMC  = ROOT.TH1D("H_th_SIMC","H_th_simc ssxptar", 300, -0.1, 0.1)

H_ph_DATA  = ROOT.TH1D("H_ph_DATA","Y' tar P_gtr_yp", 300, -0.1, 0.1)
H_ph_DUMMY  = ROOT.TH1D("H_ph_DUMMY","Y' tar P_gtr_yp", 300, -0.1, 0.1)
H_ph_SIMC  = ROOT.TH1D("H_ph_SIMC","H_ph_simc ssyptar", 300, -0.1, 0.1)

H_pmiss_DATA  = ROOT.TH1D("H_pmiss_DATA","pmiss pm", 300, -0.1, 0.4)
H_pmiss_DUMMY  = ROOT.TH1D("H_pmiss_DUMMY","pmiss pm", 300, -0.1, 0.4)
H_pmiss_SIMC  = ROOT.TH1D("H_pmiss_SIMC","pmiss pm", 300, -0.1, 0.4)

H_emiss_DATA  = ROOT.TH1D("H_emiss_DATA","emiss emiss", 300, -0.1, 0.4)
H_emiss_DUMMY  = ROOT.TH1D("H_emiss_DUMMY","emiss emiss", 300, -0.1, 0.4)
H_emiss_SIMC  = ROOT.TH1D("H_emiss_SIMC","emiss emiss", 300, -0.1, 0.4)

H_pmx_DATA  = ROOT.TH1D("H_pmx_DATA","pmx pmx", 300, -0.2, 0.2)
H_pmx_DUMMY  = ROOT.TH1D("H_pmx_DUMMY","pmx pmx", 300, -0.2, 0.2)
H_pmx_SIMC  = ROOT.TH1D("H_pmx_SIMC","pmx pmx", 300, -0.2, 0.2)

H_pmy_DATA  = ROOT.TH1D("H_pmy_DATA","pmy  pmy", 300, -0.2, 0.2)
H_pmy_DUMMY  = ROOT.TH1D("H_pmy_DUMMY","pmy  pmy", 300, -0.2, 0.2)
H_pmy_SIMC  = ROOT.TH1D("H_pmy_SIMC","pmy pmy", 300, -0.2, 0.2)

H_pmz_DATA  = ROOT.TH1D("H_pmz_DATA","pmz pmz", 300, -0.2, 0.2)
H_pmz_DUMMY  = ROOT.TH1D("H_pmz_DUMMY","pmz pmz", 300, -0.2, 0.2)
H_pmz_SIMC  = ROOT.TH1D("H_pmz_SIMC","pmz pmz", 300, -0.2, 0.2)

H_W_DATA  = ROOT.TH1D("H_W_DATA","W  W", 300, 0.5, 1.5)
H_W_DUMMY  = ROOT.TH1D("H_W_DUMMY","W  W", 300, 0.5, 1.5)
H_W_SIMC  = ROOT.TH1D("H_W_SIMC","W W", 300, 0.5, 1.5)

################################################################################################################################################

for i in range(nEntries_TBRANCH_SIMC):

  TBRANCH_SIMC.GetEntry(i)
  # Define the acceptance cuts  

  # Select the cuts
  #HMS
  CUT1 = hsdelta >=-8.0 and hsdelta <=8.0
  CUT2 = hsxptar >=-0.08 and hsxpfp <=0.08
  CUT3 = hsyptar >=-0.045 and hsypfp <=0.045

  #SHMS    
  CUT4 = ssdelta >=-10.0 and hsdelta <=20.0
  CUT5 = ssxptar >=-0.06 and hsxpfp <=0.06
  CUT6 = hsyptar >=-0.04 and hsypfp <=0.04

  #........................................

  #Fill SIMC events

  if(CUT1 and CUT2 and CUT3 and CUT4 and CUT5 and CUT6):
    
      H_ssxfp_SIMC.Fill(ssxfp, Weight)
      H_ssyfp_SIMC.Fill(ssyfp, Weight)
      H_ssxpfp_SIMC.Fill(ssxpfp, Weight)
      H_ssypfp_SIMC.Fill(ssypfp, Weight)
      H_hsxfp_SIMC.Fill(hsxfp, Weight)
      H_hsyfp_SIMC.Fill(hsyfp, Weight)
      H_hsxpfp_SIMC.Fill(hsxpfp, Weight)
      H_hsypfp_SIMC.Fill(hsypfp, Weight)
      H_ssdelta_SIMC.Fill(ssdelta, Weight) 
      H_hsdelta_SIMC.Fill(hsdelta, Weight)	
      H_ssxptar_SIMC.Fill(ssxptar, Weight)
      H_ssyptar_SIMC.Fill(ssyptar, Weight)
      H_hsxptar_SIMC.Fill(hsxptar, Weight)	
      H_hsyptar_SIMC.Fill(hsyptar, Weight)	
      H_pmiss_SIMC.Fill(Pm, Weight)	
      H_emiss_SIMC.Fill(Em, Weight)	
      H_pmx_SIMC.Fill(Pmx, Weight)
      H_pmy_SIMC.Fill(Pmy, Weight)
      H_pmz_SIMC.Fill(Pmz, Weight)
      H_Q2_SIMC.Fill(Q2_simc, Weight)
      H_W_SIMC.Fill(W_simc, Weight)
      H_epsilon_SIMC.Fill(epsilon_simc, Weight)
      H_MMp_SIMC.Fill((pow(Em, 2) - pow(Pm, 2)), Weight)  
    
for i in range(nEntries_TBRANCH_DATA):

  TBRANCH_DATA.GetEntry(i)

  #CUTs Definations 
  SHMS_FixCut = P_hod_goodstarttime_data = 1 and P_dc_InsideDipoleExit_data = 1 # and P_hod_betanotrack_data > 0.5 and P_hod_betanotrack_data < 1.4
  SHMS_Acceptance = P_gtr_dp_data>=-10.0 and P_gtr_dp_data<=20.0andP_gtr_xptar_data>=-0.06andP_gtr_xptar_data<=0.06andP_gtr_yptar_data>=-0.04andP_gtr_yptar_data<=0.04
  SHMS_ELECTRON_PID = P_cal_etottracknorm_data >= 0.85 and P_cal_etottracknorm_data <= 1.2 # P_hgcer_npeSum_data >=0.5 and P_aero_npeSum_data >=0.5

  HMS_FixCut = H_hod_goodscinhit_data = 1 and H_hod_goodstarttime_data = 1andH_dc_InsideDipoleExit_data = 1
  HMS_Acceptance = H_gtr_dp_data>=-8.0 and H_gtr_dp_data<=8.0andH_gtr_xptar_data>=-0.08andH_gtr_xptar_data<=0.08andH_gtr_yptar_data>=-0.045andH_gtr_yptar_data<=0.045       
  HMS_ELECTRON_PID = H_cer_npeSum_data >=0.5 and H_cal_etotnorm_data >=0.8 and H_cal_etotnorm_data <=1.2

  #........................................

  #if(SHMS_FixCut and SHMS_Acceptance and SHMS_ELECTRON_PID) 
  if(SHMS_FixCut and SHMS_Acceptance):
    
      H_ssxfp_DATA.Fill(ssxfp_data)
      H_ssyfp_DATA.Fill(ssyfp_data)
      H_ssxpfp_DATA.Fill(ssxpfp_data)
      H_ssypfp_DATA.Fill(ssypfp_data)
      H_ssdelta_DATA.Fill(ssdelta_data)
      H_ssxptar_DATA.Fill(ssxptar_data)
      H_ssyptar_DATA.Fill(ssyptar_data)

    

  #if(HMS_FixCut and HMS_Acceptance and HMS_ELECTRON_PID)
  if(HMS_FixCut and HMS_Acceptance):
    
      H_pmiss_DATA.Fill(pm_data)	
      H_emiss_DATA.Fill(em_data)	
      H_pmx_DATA.Fill(pmx_data)
      H_pmy_DATA.Fill(pmy_data)
      H_pmz_DATA.Fill(pmz_data)
      H_Q2_DATA.Fill(Q2_data)
      H_W_DATA.Fill(W_data)
      H_epsilon_DATA.Fill(epsilon_data)
      H_MMp_DATA.Fill((pow(em_data, 2) - pow(pm_data, 2)))  
      #H_MMp_DATA.Fill(MMp_data)  

      H_hsxfp_DATA.Fill(hsxfp_data)
      H_hsyfp_DATA.Fill(hsyfp_data)
      H_hsxpfp_DATA.Fill(hsxpfp_data)
      H_hsypfp_DATA.Fill(hsypfp_data)
      H_hsdelta_DATA.Fill(hsdelta_data)
      H_hsxptar_DATA.Fill(hsxptar_data)	
      H_hsyptar_DATA.Fill(hsyptar_data)

for i in range(nEntries_TBRANCH_DUMMY):

  TBRANCH_DUMMY.GetEntry(i)

  #......... Define Cuts.................

  #CUTs Definations 
  SHMS_FixCut = P_hod_goodstarttime_dummy = 1 and P_dc_InsideDipoleExit_dummy = 1 # and P_hod_betanotrack_dummy > 0.5 and P_hod_betanotrack_dummy < 1.4
  SHMS_Acceptance = P_gtr_dp_dummy>=-10.0 and P_gtr_dp_dummy<=20.0andP_gtr_xptar_dummy>=-0.06andP_gtr_xptar_dummy<=0.06andP_gtr_yptar_dummy>=-0.04andP_gtr_yptar_dummy<=0.04
  SHMS_ELECTRON_PID = P_cal_etottracknorm_dummy >= 0.85 and P_cal_etottracknorm_dummy <= 1.2 # P_hgcer_npeSum_dummy >=0.5 and P_aero_npeSum_dummy >=0.5

  HMS_FixCut = H_hod_goodscinhit_dummy = 1 and H_hod_goodstarttime_dummy = 1andH_dc_InsideDipoleExit_dummy = 1
  HMS_Acceptance = H_gtr_dp_dummy>=-8.0 and H_gtr_dp_dummy<=8.0andH_gtr_xptar_dummy>=-0.08andH_gtr_xptar_dummy<=0.08andH_gtr_yptar_dummy>=-0.045andH_gtr_yptar_dummy<=0.045       
  HMS_ELECTRON_PID = H_cer_npeSum_dummy >=0.5 and H_cal_etotnorm_dummy >=0.8 and H_cal_etotnorm_dummy <=1.2

  #........................................

  #if(SHMS_FixCut and SHMS_Acceptance and SHMS_ELECTRON_PID) 
  if(SHMS_FixCut and SHMS_Acceptance):
    
      H_ssxfp_DUMMY.Fill(ssxfp_dummy)
      H_ssyfp_DUMMY.Fill(ssyfp_dummy)
      H_ssxpfp_DUMMY.Fill(ssxpfp_dummy)
      H_ssypfp_DUMMY.Fill(ssypfp_dummy)
      H_ssdelta_DUMMY.Fill(ssdelta_dummy)
      H_ssxptar_DUMMY.Fill(ssxptar_dummy)
      H_ssyptar_DUMMY.Fill(ssyptar_dummy)

    

  #if(HMS_FixCut and HMS_Acceptance and HMS_ELECTRON_PID)
  if(HMS_FixCut and HMS_Acceptance):
    
      H_pmiss_DUMMY.Fill(pm_dummy)	
      H_emiss_DUMMY.Fill(em_dummy)	
      H_pmx_DUMMY.Fill(pmx_dummy)
      H_pmy_DUMMY.Fill(pmy_dummy)
      H_pmz_DUMMY.Fill(pmz_dummy)
      H_Q2_DUMMY.Fill(Q2_dummy)
      H_W_DUMMY.Fill(W_dummy)
      H_epsilon_DUMMY.Fill(epsilon_dummy)
      H_MMp_DUMMY.Fill((pow(em_dummy, 2) - pow(pm_dummy, 2)))  
      #H_MMp_DUMMY.Fill(MMp_dummy)  

      H_hsxfp_DUMMY.Fill(hsxfp_dummy)
      H_hsyfp_DUMMY.Fill(hsyfp_dummy)
      H_hsxpfp_DUMMY.Fill(hsxpfp_dummy)
      H_hsypfp_DUMMY.Fill(hsypfp_dummy)
      H_hsdelta_DUMMY.Fill(hsdelta_dummy)
      H_hsxptar_DUMMY.Fill(hsxptar_dummy)	
      H_hsyptar_DUMMY.Fill(hsyptar_dummy)
    

#simc_wgt = 0.131105E-04
simc_normfactor = 0.830037E+07
simc_nevents = 200000
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

dummy_charge = 42.096
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

data_charge = 542.499
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

# PLOT HIST..

xfp = TCanvas("xfp", "SHMS xfp")
H_ssxfp_DATA.SetLineColor(kRed)

H_ssxfp_SIMC.Draw("")
H_ssxfp_DATA.Draw("same")

xfp.Print(outputpdf + '(')

yfp = TCanvas("yfp", "SHMS yfp")
H_ssyfp_DATA.SetLineColor(kRed)

H_ssyfp_SIMC.Draw("")
H_ssyfp_DATA.Draw("same")

yfp.Print(outputpdf)

xpfp = TCanvas("xpfp", "SHMS xpfp")
H_ssxpfp_DATA.SetLineColor(kRed)

H_ssxpfp_SIMC.Draw("")
H_ssxpfp_DATA.Draw("same")

xpfp.Print(outputpdf)

ypfp = TCanvas("ypfp", "SHMS ypfp")
H_ssypfp_DATA.SetLineColor(kRed)

H_ssypfp_SIMC.Draw("")
H_ssypfp_DATA.Draw("same")

ypfp.Print(outputpdf)

hxfp = TCanvas("hxfp", "HMS xfp")
H_hsxfp_DATA.SetLineColor(kRed)

H_hsxfp_SIMC.Draw("")
H_hsxfp_DATA.Draw("same")

hxfp.Print(outputpdf)

hyfp = TCanvas("hyfp", "HMS yfp")
H_hsyfp_DATA.SetLineColor(kRed)

H_hsyfp_SIMC.Draw("")
H_hsyfp_DATA.Draw("same")

hyfp.Print(outputpdf)

hxpfp = TCanvas("hxpfp", "HMS xpfp")
H_hsxpfp_DATA.SetLineColor(kRed)

H_hsxpfp_SIMC.Draw("")
H_hsxpfp_DATA.Draw("same")

hxpfp.Print(outputpdf)

hypfp = TCanvas("hypfp", "HMS ypfp")
H_hsypfp_DATA.SetLineColor(kRed)

H_hsypfp_SIMC.Draw("")
H_hsypfp_DATA.Draw("same")

hypfp.Print(outputpdf)

xptar = TCanvas("xptar", "SHMS xptar")
H_ssxptar_DATA.SetLineColor(kRed)

H_ssxptar_SIMC.Draw("")
H_ssxptar_DATA.Draw("same")

xptar.Print(outputpdf)

yptar = TCanvas("yptar", "SHMS yptar")
H_ssyptar_DATA.SetLineColor(kRed)

H_ssyptar_SIMC.Draw("")
H_ssyptar_DATA.Draw("same")

yptar.Print(outputpdf)

hxptar = TCanvas("hxptar", "HMS xptar")
H_hsxptar_DATA.SetLineColor(kRed)

H_hsxptar_SIMC.Draw("")
H_hsxptar_DATA.Draw("same")

hxptar.Print(outputpdf)

hyptar = TCanvas("hyptar", "HMS yptar")
H_hsyptar_DATA.SetLineColor(kRed)

H_hsyptar_SIMC.Draw("")
H_hsyptar_DATA.Draw("same")

hyptar.Print(outputpdf)

Delta = TCanvas("Delta", "SHMS Delta")
H_ssdelta_DATA.SetLineColor(kRed)

H_ssdelta_SIMC.Draw("")
H_ssdelta_DATA.Draw("same")

Delta.Print(outputpdf)

hDelta = TCanvas("hDelta", "HMS Delta")
H_hsdelta_DATA.SetLineColor(kRed)

H_hsdelta_SIMC.Draw("")
H_hsdelta_DATA.Draw("same")

hDelta.Print(outputpdf)

CQ2 = TCanvas("CQ2", "SHMS Q2")
H_Q2_DATA.SetLineColor(kRed)

H_Q2_SIMC.Draw("")
H_Q2_DATA.Draw("same")

CQ2.Print(outputpdf)

Cepsilon = TCanvas("Cepsilon", "epsilon")
H_epsilon_DATA.SetLineColor(kRed)

H_epsilon_SIMC.Draw("")
H_epsilon_DATA.Draw("same")

Cepsilon.Print(outputpdf)

CMMp = TCanvas("CMMp", "Proton missing mass")
H_MMp_DATA.SetLineColor(kRed)

H_MMp_SIMC.Draw("")
H_MMp_DATA.Draw("same")

CMMp.Print(outputpdf)

Cpmiss = TCanvas("Cpmiss", "pmiss")
H_pmiss_DATA.SetLineColor(kRed)

H_pmiss_SIMC.Draw("")
H_pmiss_DATA.Draw("same")

Cpmiss.Print(outputpdf)

Cemiss = TCanvas("Cemiss", "emiss")
H_emiss_DATA.SetLineColor(kRed)

H_emiss_SIMC.Draw("")
H_emiss_DATA.Draw("same")

Cemiss.Print(outputpdf)

Cpmiss_x = TCanvas("Cpmiss_x", "pmiss_x")
H_pmx_DATA.SetLineColor(kRed)

H_pmx_SIMC.Draw("")
H_pmx_DATA.Draw("same")
Cpmiss_x.Print(outputpdf)

Cpmiss_y = TCanvas("Cpmiss_y", "pmiss_y")
H_pmy_DATA.SetLineColor(kRed)

H_pmy_SIMC.Draw("")
H_pmy_DATA.Draw("same")

Cpmiss_y.Print(outputpdf)

Cpmiss_z = TCanvas("Cpmiss_z", "pmiss_z")
H_pmz_DATA.SetLineColor(kRed)

H_pmz_SIMC.Draw("")
H_pmz_DATA.Draw("same")

Cpmiss_z.Print(outputpdf)

CW = TCanvas("CW", "W")
H_W_DATA.SetLineColor(kRed)

H_W_SIMC.Draw("")
H_W_DATA.Draw("same")

CW.Print(outputpdf + ')')
