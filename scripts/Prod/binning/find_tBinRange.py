#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-11-30 00:54:27 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

##################################################################################################################################################

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
from ROOT import kBlack, kCyan, kRed, kGreen, kMagenta
from functools import reduce

##################################################################################################################################################

# Check the number of arguments provided to the script
if len(sys.argv)-1!=4:
    print("!!!!! ERROR !!!!!\n Expected 4 arguments\n Usage is with - KIN OutDATAFilename.root OutFullAnalysisFilename EvtsPerBinRange\n!!!!! ERROR !!!!!")
    sys.exit(1)

##################################################################################################################################################    

DEBUG = False # Flag for no cut plots

# Input params
kinematics = sys.argv[1]
InDATAFilename = sys.argv[2]
OutFilename = sys.argv[3]
EvtsPerBinRange = int(sys.argv[4])

###############################################################################################################################################
ROOT.gROOT.SetBatch(ROOT.kTRUE) # Set ROOT to batch mode explicitly, does not splash anything to screen
###############################################################################################################################################

'''
ltsep package import and pathing definitions
'''

# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__),"Plot_Prod")

# Add this to all files for more dynamic pathing
USER=lt.USER # Grab user info for file finding
HOST=lt.HOST
REPLAYPATH=lt.REPLAYPATH
UTILPATH=lt.UTILPATH
SIMCPATH=lt.SIMCPATH
ANATYPE=lt.ANATYPE
OUTPATH=lt.OUTPATH

foutname = OUTPATH+"/" + OutFilename + ".root"
fouttxt  = OUTPATH+"/" + OutFilename + ".txt"
outputpdf  = OUTPATH+"/" + OutFilename + ".pdf"

################################################################################################################################################

def defineHists(phi_setting):
    ################################################################################################################################################
    # Define root file trees of interest

    rootFile = OUTPATH+"/"+InDATAFilename+"_%s.root" % (phi_setting)
    if not os.path.isfile(rootFile):
        return {}

    InFile_DATA = ROOT.TFile.Open(rootFile, "OPEN")

    TBRANCH_DATA  = InFile_DATA.Get("Uncut_Kaon_Events")
    #TBRANCH_DATA  = InFile_DATA.Get("Cut_Kaon_Events_all_noRF")
    #TBRANCH_DATA  = InFile_DATA.Get("Cut_Kaon_Events_prompt_noRF")
    #TBRANCH_DATA  = InFile_DATA.Get("Cut_Kaon_Events_rand_noRF")
    #TBRANCH_DATA  = InFile_DATA.Get("Cut_Kaon_Events_all_RF")
    #TBRANCH_DATA  = InFile_DATA.Get("Cut_Kaon_Events_prompt_RF")
    #TBRANCH_DATA  = InFile_DATA.Get("Cut_Kaon_Events_rand_RF")

    ################################################################################################################################################
    # Plot definitions

    H_hsdelta_DATA  = ROOT.TH1D("H_hsdelta_DATA","HMS Delta", 200, -20.0, 20.0)
    H_hsxptar_DATA  = ROOT.TH1D("H_hsxptar_DATA","HMS xptar", 200, -0.1, 0.1)
    H_hsyptar_DATA  = ROOT.TH1D("H_hsyptar_DATA","HMS yptar", 200, -0.1, 0.1)
    H_ssxfp_DATA    = ROOT.TH1D("H_ssxfp_DATA","SHMS xfp", 200, -25.0, 25.0)
    H_ssyfp_DATA    = ROOT.TH1D("H_ssyfp_DATA","SHMS yfp", 200, -25.0, 25.0)
    H_ssxpfp_DATA   = ROOT.TH1D("H_ssxpfp_DATA","SHMS xpfp", 200, -0.09, 0.09)
    H_ssypfp_DATA   = ROOT.TH1D("H_ssypfp_DATA","SHMS ypfp", 200, -0.05, 0.04)
    H_hsxfp_DATA    = ROOT.TH1D("H_hsxfp_DATA","HMS xfp", 200, -40.0, 40.0)
    H_hsyfp_DATA    = ROOT.TH1D("H_hsyfp_DATA","HMS yfp", 200, -20.0, 20.0)
    H_hsxpfp_DATA   = ROOT.TH1D("H_hsxpfp_DATA","HMS xpfp", 200, -0.09, 0.05)
    H_hsypfp_DATA   = ROOT.TH1D("H_hsypfp_DATA","HMS ypfp", 200, -0.05, 0.04)
    H_ssdelta_DATA  = ROOT.TH1D("H_ssdelta_DATA","SHMS delta", 200, -20.0, 20.0)
    H_ssxptar_DATA  = ROOT.TH1D("H_ssxptar_DATA","SHMS xptar", 200, -0.1, 0.1)
    H_ssyptar_DATA  = ROOT.TH1D("H_ssyptar_DATA","SHMS yptar", 200, -0.04, 0.04)
    H_q_DATA        = ROOT.TH1D("H_q_DATA","q", 200, 0.0, 10.0)
    H_Q2_DATA       = ROOT.TH1D("H_Q2_DATA","Q2", 200, 0.0, 10.0)
    H_W_DATA  = ROOT.TH1D("H_W_DATA","W ", 200, 0.0, 10.0)
    H_t_DATA       = ROOT.TH1D("H_t_DATA","-t", 200, 0.0, 1.0)  
    H_epsilon_DATA  = ROOT.TH1D("H_epsilon_DATA","epsilon", 200, 0.5, 1.0)
    H_MMp2_DATA  = ROOT.TH1D("H_MMp2_DATA","(MM)^{2}_{p}", 200, 0.0, 2.0)
    H_th_DATA  = ROOT.TH1D("H_th_DATA","X' tar", 200, -0.1, 0.1)
    H_ph_DATA  = ROOT.TH1D("H_ph_DATA","Y' tar", 200, -0.1, 0.1)
    H_ph_q_DATA  = ROOT.TH1D("H_ph_q_DATA","Phi Detected (ph_xq)", 200, -10.0, 10.0)
    H_th_q_DATA  = ROOT.TH1D("H_th_q_DATA","Theta Detected (th_xq)", 200, -0.2, 0.2)
    H_ph_recoil_DATA  = ROOT.TH1D("H_ph_recoil_DATA","Phi Recoil (ph_bq)", 200, -10.0, 10.0)
    H_th_recoil_DATA  = ROOT.TH1D("H_th_recoil_DATA","Theta Recoil (th_bq)", 200, -10.0, 10.0)
    H_pmiss_DATA  = ROOT.TH1D("H_pmiss_DATA","pmiss", 200, 0.0, 10.0)
    H_emiss_DATA  = ROOT.TH1D("H_emiss_DATA","emiss", 200, 0.0, 10.0)
    H_pmx_DATA  = ROOT.TH1D("H_pmx_DATA","pmx", 200, 0.0, 10.0)
    H_pmy_DATA  = ROOT.TH1D("H_pmy_DATA","pmy ", 200, 0.0, 10.0)
    H_pmz_DATA  = ROOT.TH1D("H_pmz_DATA","pmz", 200, 0.0, 10.0)
    H_ct_ep_DATA = ROOT.TH1D("H_ct_ep_DATA", "Electron-Proton CTime", 200, -10, 10)
    H_cal_etottracknorm_DATA = ROOT.TH1D("H_cal_etottracknorm_DATA", "HMS Cal etottracknorm", 200, 0.2, 1.8)
    H_cer_npeSum_DATA = ROOT.TH1D("H_cer_npeSum_DATA", "HMS Cer Npe Sum", 200, 0, 30)
    P_cal_etottracknorm_DATA = ROOT.TH1D("P_cal_etottracknorm_DATA", "SHMS Cal etottracknorm", 200, 0, 1)
    P_hgcer_npeSum_DATA = ROOT.TH1D("P_hgcer_npeSum_DATA", "SHMS HGCer Npe Sum", 200, 0, 50)
    P_aero_npeSum_DATA = ROOT.TH1D("P_aero_npeSum_DATA", "SHMS Aero Npe Sum", 200, 0, 50)

    H_hsdelta_DATA_rand  = ROOT.TH1D("H_hsdelta_DATA_rand","HMS Delta", 200, -20.0, 20.0)
    H_hsxptar_DATA_rand  = ROOT.TH1D("H_hsxptar_DATA_rand","HMS xptar", 200, -0.1, 0.1)
    H_hsyptar_DATA_rand  = ROOT.TH1D("H_hsyptar_DATA_rand","HMS yptar", 200, -0.1, 0.1)
    H_ssxfp_DATA_rand    = ROOT.TH1D("H_ssxfp_DATA_rand","SHMS xfp", 200, -25.0, 25.0)
    H_ssyfp_DATA_rand    = ROOT.TH1D("H_ssyfp_DATA_rand","SHMS yfp", 200, -25.0, 25.0)
    H_ssxpfp_DATA_rand   = ROOT.TH1D("H_ssxpfp_DATA_rand","SHMS xpfp", 200, -0.09, 0.09)
    H_ssypfp_DATA_rand   = ROOT.TH1D("H_ssypfp_DATA_rand","SHMS ypfp", 200, -0.05, 0.04)
    H_hsxfp_DATA_rand    = ROOT.TH1D("H_hsxfp_DATA_rand","HMS xfp", 200, -40.0, 40.0)
    H_hsyfp_DATA_rand    = ROOT.TH1D("H_hsyfp_DATA_rand","HMS yfp", 200, -20.0, 20.0)
    H_hsxpfp_DATA_rand   = ROOT.TH1D("H_hsxpfp_DATA_rand","HMS xpfp", 200, -0.09, 0.05)
    H_hsypfp_DATA_rand   = ROOT.TH1D("H_hsypfp_DATA_rand","HMS ypfp", 200, -0.05, 0.04)
    H_ssdelta_DATA_rand  = ROOT.TH1D("H_ssdelta_DATA_rand","SHMS delta", 200, -20.0, 20.0)
    H_ssxptar_DATA_rand  = ROOT.TH1D("H_ssxptar_DATA_rand","SHMS xptar", 200, -0.1, 0.1)
    H_ssyptar_DATA_rand  = ROOT.TH1D("H_ssyptar_DATA_rand","SHMS yptar", 200, -0.04, 0.04)
    H_q_DATA_rand        = ROOT.TH1D("H_q_DATA_rand","q", 200, 0.0, 10.0)
    H_Q2_DATA_rand       = ROOT.TH1D("H_Q2_DATA_rand","Q2", 200, 0.0, 10.0)
    H_W_DATA_rand  = ROOT.TH1D("H_W_DATA_rand","W ", 200, 0.0, 10.0)
    H_t_DATA_rand       = ROOT.TH1D("H_t_DATA_rand","-t", 200, 0.0, 1.0)  
    H_epsilon_DATA_rand  = ROOT.TH1D("H_epsilon_DATA_rand","epsilon", 200, 0.5, 1.0)
    H_MMp2_DATA_rand  = ROOT.TH1D("H_MMp2_DATA_rand","(MM)^{2}_{p}", 200, 0.0, 2.0)
    H_th_DATA_rand  = ROOT.TH1D("H_th_DATA_rand","X' tar", 200, -0.1, 0.1)
    H_ph_DATA_rand  = ROOT.TH1D("H_ph_DATA_rand","Y' tar", 200, -0.1, 0.1)
    H_ph_q_DATA_rand  = ROOT.TH1D("H_ph_q_DATA_rand","Phi Detected (ph_xq)", 200, -10.0, 10.0)
    H_th_q_DATA_rand  = ROOT.TH1D("H_th_q_DATA_rand","Theta Detected (th_xq)", 200, -0.2, 0.2)
    H_ph_recoil_DATA_rand  = ROOT.TH1D("H_ph_recoil_DATA_rand","Phi Recoil (ph_bq)", 200, -10.0, 10.0)
    H_th_recoil_DATA_rand  = ROOT.TH1D("H_th_recoil_DATA_rand","Theta Recoil (th_bq)", 200, -10.0, 10.0)
    H_pmiss_DATA_rand  = ROOT.TH1D("H_pmiss_DATA_rand","pmiss", 200, 0.0, 10.0)
    H_emiss_DATA_rand  = ROOT.TH1D("H_emiss_DATA_rand","emiss", 200, 0.0, 10.0)
    H_pmx_DATA_rand  = ROOT.TH1D("H_pmx_DATA_rand","pmx", 200, 0.0, 10.0)
    H_pmy_DATA_rand  = ROOT.TH1D("H_pmy_DATA_rand","pmy ", 200, 0.0, 10.0)
    H_pmz_DATA_rand  = ROOT.TH1D("H_pmz_DATA_rand","pmz", 200, 0.0, 10.0)
    H_ct_ep_DATA_rand = ROOT.TH1D("H_ct_ep_DATA_rand", "Electron-Proton CTime", 200, -10, 10)

    H_t_BinTest       = ROOT.TH1D("H_t_BinTest","-t", 200, 0.0, 1.0)  
    
    ################################################################################################################################################

    # Check if number of events is less than events per bin range
    if TBRANCH_DATA.GetEntries() <= EvtsPerBinRange:
        sys.exit(1)

    # Grab t bin range for EvtsPerBinRange evts
    for i,evt in enumerate(TBRANCH_DATA):
        lt.progressBar(i, TBRANCH_DATA.GetEntries(), bar_length=50)
        H_t_BinTest.Fill(-evt.MandelT)
        tbinval = np.array(H_t_BinTest).sum()
        for val,binval in zip(np.linspace(0,0.5,201),range(1,len(np.array(H_t_BinTest)))):
            if (EvtsPerBinRange-1000 <= (val<=H_t_BinTest.GetBinCenter(binval)) & ((1-val)<=H_t_BinTest.GetBinCenter(binval))).sum() <= EvtsPerBinRange+1000:
                tbin_min = val
                tbin_max = 1-val
                tbin_size = tbin_max-tbin_max
    print("\n\nHERE",tbin_size)
    print("HERE",tbin_min)
    print("HERE",tbin_max)
    
    ################################################################################################################################################
    # Fill histograms for various trees called above

    
    ibin = 1
    for evt in TBRANCH_DATA:

        #CUTs Definations 
        SHMS_FixCut = (evt.P_hod_goodstarttime == 1) & (evt.P_dc_InsideDipoleExit == 1) # & P_hod_betanotrack > 0.5 & P_hod_betanotrack < 1.4
        SHMS_Acceptance = (evt.ssdelta>=-10.0) & (evt.ssdelta<=20.0) & (evt.ssxptar>=-0.06) & (evt.ssxptar<=0.06) & (evt.ssyptar>=-0.04) & (evt.ssyptar<=0.04)

        HMS_FixCut = (evt.H_hod_goodstarttime == 1) & (evt.H_dc_InsideDipoleExit == 1)
        HMS_Acceptance = (evt.hsdelta>=-8.0) & (evt.hsdelta<=8.0) & (evt.hsxptar>=-0.08) & (evt.hsxptar<=0.08) & (evt.hsyptar>=-0.045) & (evt.hsyptar<=0.045)

        tBin_Cut = (-evt.MandelT>=tbin_min) & (-evt.MandelT<=tbin_max)

        #........................................
                
        if(HMS_FixCut & HMS_Acceptance & SHMS_FixCut & SHMS_Acceptance & tBin_Cut):
            
          H_ct_ep_DATA.Fill(evt.CTime_epCoinTime_ROC1)

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

          H_ph_q_DATA.Fill(evt.ph_q)
          H_th_q_DATA.Fill(evt.th_q)
          H_ph_recoil_DATA.Fill(evt.ph_recoil)
          H_th_recoil_DATA.Fill(evt.th_recoil)

          H_pmiss_DATA.Fill(evt.pmiss)	
          H_emiss_DATA.Fill(evt.emiss)	
          #H_emiss_DATA.Fill(evt.emiss_nuc)
          H_pmx_DATA.Fill(evt.pmx)
          H_pmy_DATA.Fill(evt.pmy)
          H_pmz_DATA.Fill(evt.pmz)
          H_Q2_DATA.Fill(evt.Q2)
          H_t_DATA.Fill(-evt.MandelT)
          H_W_DATA.Fill(evt.W)
          H_epsilon_DATA.Fill(evt.epsilon)
          H_MMp2_DATA.Fill(pow(evt.emiss, 2) - pow(evt.pmiss, 2))  
          #H_MMp2_DATA.Fill(pow(evt.MMp, 2))  
          #H_MMp2_DATA.Fill(evt.Mrecoil)

          ###################################################################################################################################################

          # Random subtraction

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
          H_t_DATA_rand.Fill(-evt.MandelT)
          H_W_DATA_rand.Fill(evt.W)
          H_epsilon_DATA_rand.Fill(evt.epsilon)
          H_MMp2_DATA_rand.Fill(pow(evt.emiss, 2) - pow(evt.pmiss, 2))  

          H_cal_etottracknorm_DATA.Fill(evt.H_cal_etottracknorm)
          H_cer_npeSum_DATA.Fill(evt.H_cer_npeSum)

          P_cal_etottracknorm_DATA.Fill(evt.P_cal_etottracknorm)
          P_hgcer_npeSum_DATA.Fill(evt.P_hgcer_npeSum)
          P_aero_npeSum_DATA.Fill(evt.P_aero_npeSum)

          ibin+=1

    '''
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
    H_t_DATA.Scale(normfac_data)
    H_epsilon_DATA.Scale(normfac_data)
    H_MMp2_DATA.Scale(normfac_data)
    H_ph_q_DATA.Scale(normfac_data)
    H_th_q_DATA.Scale(normfac_data)
    H_ph_recoil_DATA.Scale(normfac_data)
    H_th_recoil_DATA.Scale(normfac_data)
    H_pmiss_DATA.Scale(normfac_data)
    H_emiss_DATA.Scale(normfac_data)
    H_pmx_DATA.Scale(normfac_data)
    H_pmy_DATA.Scale(normfac_data)
    H_pmz_DATA.Scale(normfac_data)
    H_W_DATA.Scale(normfac_data)
    H_ct_ep_DATA.Scale(normfac_data)
    '''


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
    H_t_DATA_rand.Scale(normfac_data/nWindows)
    H_epsilon_DATA_rand.Scale(normfac_data/nWindows)
    H_MMp2_DATA_rand.Scale(normfac_data/nWindows)
    H_pmiss_DATA_rand.Scale(normfac_data/nWindows)
    H_emiss_DATA_rand.Scale(normfac_data/nWindows)
    H_pmx_DATA_rand.Scale(normfac_data/nWindows)
    H_pmy_DATA_rand.Scale(normfac_data/nWindows)
    H_pmz_DATA_rand.Scale(normfac_data/nWindows)
    H_W_DATA_rand.Scale(normfac_data/nWindows)
    #H_ct_ep_DATA_rand.Scale(normfac_data/nWindows)
    '''

    ###

    '''
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
    H_t_DATA.Add(H_t_DATA_rand,-1)
    H_epsilon_DATA.Add(H_epsilon_DATA_rand,-1)
    H_MMp2_DATA.Add(H_MMp2_DATA_rand,-1)
    H_pmiss_DATA.Add(H_pmiss_DATA_rand,-1)
    H_emiss_DATA.Add(H_emiss_DATA_rand,-1)
    H_pmx_DATA.Add(H_pmx_DATA_rand,-1)
    H_pmy_DATA.Add(H_pmy_DATA_rand,-1)
    H_pmz_DATA.Add(H_pmz_DATA_rand,-1)
    H_W_DATA.Add(H_W_DATA_rand,-1)
    H_ct_ep_DATA.Add(H_ct_ep_DATA_rand,-1)
    '''
    
    histDict = {
        "phi_setting" : phi_setting,
        "H_hsdelta_DATA" :     H_hsdelta_DATA,
        "H_hsxptar_DATA" :     H_hsxptar_DATA,
        "H_hsyptar_DATA" :     H_hsyptar_DATA,
        "H_ssxfp_DATA" :     H_ssxfp_DATA  ,
        "H_ssyfp_DATA" :     H_ssyfp_DATA  ,
        "H_ssxpfp_DATA" :     H_ssxpfp_DATA ,
        "H_ssypfp_DATA" :     H_ssypfp_DATA ,
        "H_hsxfp_DATA" :     H_hsxfp_DATA  ,
        "H_hsyfp_DATA" :     H_hsyfp_DATA  ,
        "H_hsxpfp_DATA" :     H_hsxpfp_DATA ,
        "H_hsypfp_DATA" :     H_hsypfp_DATA ,
        "H_ssdelta_DATA" :     H_ssdelta_DATA,
        "H_ssxptar_DATA" :     H_ssxptar_DATA,
        "H_ssyptar_DATA" :     H_ssyptar_DATA,
        "H_q_DATA" :     H_q_DATA      ,
        "H_Q2_DATA" :     H_Q2_DATA     ,
        "H_t_DATA" :     H_t_DATA     ,
        "H_epsilon_DATA" :     H_epsilon_DATA,
        "H_MMp2_DATA" :     H_MMp2_DATA,
        "H_th_DATA" :     H_th_DATA,
        "H_ph_DATA" :     H_ph_DATA,
        "H_ph_q_DATA" :     H_ph_q_DATA,
        "H_th_q_DATA" :     H_th_q_DATA,
        "H_ph_recoil_DATA" :     H_ph_recoil_DATA,
        "H_th_recoil_DATA" :     H_th_recoil_DATA,
        "H_pmiss_DATA" :     H_pmiss_DATA,
        "H_emiss_DATA" :     H_emiss_DATA,
        "H_pmx_DATA" :     H_pmx_DATA,
        "H_pmy_DATA" :     H_pmy_DATA,
        "H_pmz_DATA" :     H_pmz_DATA,
        "H_W_DATA" :     H_W_DATA,
        "H_ct_ep_DATA" :     H_ct_ep_DATA,
        "H_cal_etottracknorm_DATA" :     H_cal_etottracknorm_DATA,
        "H_cer_npeSum_DATA" :     H_cer_npeSum_DATA,
        "P_cal_etottracknorm_DATA" :     P_cal_etottracknorm_DATA,
        "P_hgcer_npeSum_DATA" :     P_hgcer_npeSum_DATA,
        "P_aero_npeSum_DATA" :     P_aero_npeSum_DATA,
        "InFile_DATA" : InFile_DATA,
    }

    return histDict

################################################################################################################################################
# Removes stat box
ROOT.gStyle.SetOptStat(0)
################################################################################################################################################

# Call histogram function above to define dictonaries for right, left, center settings
# Put these all into an array so that if we are missing a setting it is easier to remove
# Plus it makes the code below less repetitive
histlist = [defineHists("Right"),defineHists("Left"),defineHists("Center")]

for i,hist in enumerate(histlist):
    if not bool(hist): # If hist is empty
        histlist.remove(hist)
        
# Plot histograms

c_pid = TCanvas()

c_pid.Divide(2,3)

c_pid.cd(1)
gPad.SetLogy()

for i,hist in enumerate(histlist):
    hist["H_cal_etottracknorm_DATA"].SetLineColor(i+1)
    hist["H_cal_etottracknorm_DATA"].Draw("same, E1")

c_pid.cd(2)
gPad.SetLogy()

for i,hist in enumerate(histlist):
    hist["H_cer_npeSum_DATA"].SetLineColor(i+1)
    hist["H_cer_npeSum_DATA"].Draw("same, E1")

c_pid.cd(3)
gPad.SetLogy()
for i,hist in enumerate(histlist):
    hist["P_cal_etottracknorm_DATA"].SetLineColor(i+1)
    hist["P_cal_etottracknorm_DATA"].Draw("same, E1")

c_pid.cd(4)
gPad.SetLogy()
for i,hist in enumerate(histlist):
    hist["P_hgcer_npeSum_DATA"].SetLineColor(i+1)
    hist["P_hgcer_npeSum_DATA"].Draw("same, E1")

c_pid.cd(5)
gPad.SetLogy()
for i,hist in enumerate(histlist):
    hist["P_aero_npeSum_DATA"].SetLineColor(i+1)
    hist["P_aero_npeSum_DATA"].Draw("same, E1")
        
c_pid.Draw()

c_pid.Print(outputpdf + '(')

ct_ep = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ct_ep_DATA"].SetLineColor(i+1)
    hist["H_ct_ep_DATA"].Draw("same, E1")

ct_ep.Print(outputpdf)


CQ2 = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_Q2_DATA"].SetLineColor(i+1)
    hist["H_Q2_DATA"].Draw("same, E1")

CQ2.Print(outputpdf)

CW = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_W_DATA"].SetLineColor(i+1)
    hist["H_W_DATA"].Draw("same, E1")
    
CW.Print(outputpdf)

Ct = TCanvas()
l_t = ROOT.TLegend(0.115,0.55,0.33,0.9)
l_t.SetTextSize(0.0335)

for i,hist in enumerate(histlist):
    hist["H_t_DATA"].SetLineColor(i+1)
    l_t.AddEntry(hist["H_t_DATA"],hist["phi_setting"])
    hist["H_t_DATA"].Draw("same, E1")            
    
    #l_t.AddEntry(hist["H_t_DATA"],tbinval)

l_t.Draw()    

Ct.Print(outputpdf)

Cepsilon = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_epsilon_DATA"].SetLineColor(i+1)
    hist["H_epsilon_DATA"].Draw("same, E1")

Cepsilon.Print(outputpdf)

CMMp2 = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_MMp2_DATA"].SetLineColor(i+1)
    hist["H_MMp2_DATA"].Draw("same, E1")

CMMp2.Print(outputpdf)

xfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ssxfp_DATA"].SetLineColor(i+1)
    hist["H_ssxfp_DATA"].Draw("same, E1")

xfp.Print(outputpdf)

yfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ssyfp_DATA"].SetLineColor(i+1)
    hist["H_ssyfp_DATA"].Draw("same, E1")

yfp.Print(outputpdf)

xpfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ssxpfp_DATA"].SetLineColor(i+1)
    hist["H_ssxpfp_DATA"].Draw("same, E1")
    
xpfp.Print(outputpdf)

ypfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ssxpfp_DATA"].SetLineColor(i+1)
    hist["H_ssxpfp_DATA"].Draw("same, E1")

ypfp.Print(outputpdf)

hxfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_hsxfp_DATA"].SetLineColor(i+1)
    hist["H_hsxfp_DATA"].Draw("same, E1")

hxfp.Print(outputpdf)

hyfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_hsyfp_DATA"].SetLineColor(i+1)
    hist["H_hsyfp_DATA"].Draw("same, E1")

hyfp.Print(outputpdf)

hxpfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_hsxpfp_DATA"].SetLineColor(i+1)
    hist["H_hsxpfp_DATA"].Draw("same, E1")

hxpfp.Print(outputpdf)

hypfp = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_hsypfp_DATA"].SetLineColor(i+1)
    hist["H_hsypfp_DATA"].Draw("same, E1")

hypfp.Print(outputpdf)

xptar = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ssxptar_DATA"].SetLineColor(i+1)
    hist["H_ssxptar_DATA"].Draw("same, E1")

xptar.Print(outputpdf)

yptar = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ssyptar_DATA"].SetLineColor(i+1)
    hist["H_ssyptar_DATA"].Draw("same, E1")

yptar.Print(outputpdf)

hxptar = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_hsxptar_DATA"].SetLineColor(i+1)
    hist["H_hsxptar_DATA"].Draw("same, E1")

hxptar.Print(outputpdf)

hyptar = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_hsyptar_DATA"].SetLineColor(i+1)
    hist["H_hsyptar_DATA"].Draw("same, E1")

hyptar.Print(outputpdf)

Delta = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ssdelta_DATA"].SetLineColor(i+1)
    hist["H_ssdelta_DATA"].Draw("same, E1")

Delta.Print(outputpdf)

hDelta = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_hsdelta_DATA"].SetLineColor(i+1)
    hist["H_hsdelta_DATA"].Draw("same, E1")

hDelta.Print(outputpdf)

Cph_q = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ph_q_DATA"].SetLineColor(i+1)
    hist["H_ph_q_DATA"].Draw("same, E1")

Cph_q.Print(outputpdf)

Cth_q = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_th_q_DATA"].SetLineColor(i+1)
    hist["H_th_q_DATA"].Draw("same, E1")

Cth_q.Print(outputpdf)

Cph_recoil = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_ph_recoil_DATA"].SetLineColor(i+1)
    hist["H_ph_recoil_DATA"].Draw("same, E1")

Cph_recoil.Print(outputpdf)

Cth_recoil = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_th_recoil_DATA"].SetLineColor(i+1)
    hist["H_th_recoil_DATA"].Draw("same, E1")

Cth_recoil.Print(outputpdf)

Cpmiss = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_pmiss_DATA"].SetLineColor(i+1)
    hist["H_pmiss_DATA"].Draw("same, E1")

Cpmiss.Print(outputpdf)

Cemiss = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_emiss_DATA"].SetLineColor(i+1)
    hist["H_emiss_DATA"].Draw("same, E1")

Cemiss.Print(outputpdf)

Cpmiss_x = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_pmx_DATA"].SetLineColor(i+1)
    hist["H_pmx_DATA"].Draw("same, E1")

Cpmiss_x.Print(outputpdf)

Cpmiss_y = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_pmy_DATA"].SetLineColor(i+1)
    hist["H_pmy_DATA"].Draw("same, E1")

Cpmiss_y.Print(outputpdf)

Cpmiss_z = TCanvas()

for i,hist in enumerate(histlist):
    hist["H_pmz_DATA"].SetLineColor(i+1)
    hist["H_pmz_DATA"].Draw("same, E1")

Cpmiss_z.Print(outputpdf+')')

#############################################################################################################################################
# Create new root file with trees representing cut simc and data used above. Good for those who see python as...problematic

outHistFile = ROOT.TFile.Open(foutname, "RECREATE")
d_Right_Data = outHistFile.mkdir("Right")
d_Left_Data = outHistFile.mkdir("Left")
d_Center_Data = outHistFile.mkdir("Center")

d_Right_Data.cd()
for i,hist in enumerate(histlist):
    if bool(hist):
        continue
    if hist["phi_setting"] == "Right":
        d_Right_Data.cd()
    if hist["phi_setting"] == "Left":
        d_Left_Data.cd()
    if hist["phi_setting"] == "Center":
        d_Center_Data.cd()
    hist["H_hsdelta_DATA"].Write()
    hist["H_hsxptar_DATA"].Write()
    hist["H_hsyptar_DATA"].Write()
    hist["H_ssxfp_DATA"].Write()
    hist["H_ssyfp_DATA"].Write()
    hist["H_ssxpfp_DATA"].Write()
    hist["H_ssypfp_DATA"].Write()
    hist["H_hsxfp_DATA"].Write()
    hist["H_hsyfp_DATA"].Write()
    hist["H_hsxpfp_DATA"].Write()
    hist["H_hsypfp_DATA"].Write()
    hist["H_ssdelta_DATA"].Write()
    hist["H_ssxptar_DATA"].Write()
    hist["H_ssyptar_DATA"].Write()
    hist["H_q_DATA"].Write()
    hist["H_Q2_DATA"].Write()
    hist["H_W_DATA"].Write()
    hist["H_t_DATA"].Write()
    hist["H_epsilon_DATA"].Write()
    hist["H_MMp2_DATA"].Write()
    hist["H_th_DATA"].Write()
    hist["H_ph_DATA"].Write()
    hist["H_ph_q_DATA"].Write()
    hist["H_th_q_DATA"].Write()
    hist["H_ph_recoil_DATA"].Write()
    hist["H_th_recoil_DATA"].Write()
    hist["H_pmiss_DATA"].Write()
    hist["H_emiss_DATA"].Write()
    hist["H_pmx_DATA"].Write()
    hist["H_pmy_DATA"].Write()
    hist["H_pmz_DATA"].Write()
    hist["H_ct_ep_DATA"].Write()

outHistFile.Close()

for i,hist in enumerate(histlist):
    hist["InFile_DATA"].Close()
    
print ("Processing Complete")
