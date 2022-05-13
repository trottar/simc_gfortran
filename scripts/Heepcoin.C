// .... This script has created to the Coin Heep Study....
// .... Created Date: October 22, 2021 ....
// .... Author: VK ....
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
//''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#define EFFICIENCY_cxx
#include <TStyle.h>
#include <TCanvas.h>
#include <TLine.h>
#include <TMath.h>
#include <TPaveText.h>
#include <TGaxis.h>
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <TSystem.h>
#include <TTree.h>
#include <TArc.h>
#include <TCutG.h>
#include <TExec.h>
#include <TColor.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>

// Input should be the input root file name (including suffix) and an output file name string (without any suffix)
void Heepcoin(string InDATAFilename = "", string InDUMMYFilename = "",string InSIMCFilename = "", string OutFilename = "")
{
  TString Hostname = gSystem->HostName();
  TString User = (gSystem->GetUserInfo())->fUser;
  TString Replaypath;
  TString ROOTfilePath;
  TString OutPath;
  TString rootFile;
  TString rootFile_Dummy;
  TString rootFile_SIMC;

  gStyle->SetPalette(55);

  // Set paths depending on system you're running on
  if(Hostname.Contains("farm")){
    Replaypath = "/group/c-kaonlt/USERS/"+User+"/hallc_replay_lt";
    // Output path for root file
    ROOTfilePath = Replaypath+"/UTIL_KAONLT/OUTPUT/Analysis/HeeP";
    OutPath = Replaypath+"/UTIL_KAONLT/OUTPUT/Analysis/HeeP";
  }
  else if(Hostname.Contains("qcd")){
    Replaypath = "/group/c-kaonlt/USERS/"+User+"/hallc_replay_lt";
    // Output path for root file
    ROOTfilePath = Replaypath+"/UTIL_KAONLT/OUTPUT/Analysis/HeeP";
    OutPath = Replaypath+"/UTIL_KAONLT/OUTPUT/Analysis/HeeP";
  }
  else if (Hostname.Contains("phys.uregina.ca")){
    ROOTfilePath = "/home/vijay/work/HeepCoinStudy/";
    OutPath = "/home/vijay/work/HeepCoinStudy/";
  }

  // Add more as needed for your own envrionment
  if(InDATAFilename == "") {
    cout << "Enter a DATA ROOT Filename to analyse: ";
    cin >> InDATAFilename;
  }  

  if(InDUMMYFilename == "") {
    cout << "Enter a DUMMY ROOT Filename to analyse: ";
    cin >> InDUMMYFilename;
  }  

  if(InSIMCFilename == "") {
    cout << "Enter a SIMC ROOT Filename to analyse: ";
    cin >> InSIMCFilename;
  }  

  if(OutFilename == "") {
    cout << "Enter a Filename to output to: ";
    cin >> OutFilename;
  }

  TString TInDATAFilename = InDATAFilename ;
  TString TInDUMMYFilename = InDUMMYFilename ;
  TString TInSIMCFilename = InSIMCFilename ;
  rootFile = ROOTfilePath+"/"+TInDATAFilename;
  rootFile_Dummy = ROOTfilePath+"/"+TInDUMMYFilename;
  rootFile_SIMC = ROOTfilePath+"/"+TInSIMCFilename;

  if (gSystem->AccessPathName(rootFile) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl <<rootFile <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  if (gSystem->AccessPathName(rootFile_Dummy) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl <<rootFile_Dummy <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  if (gSystem->AccessPathName(rootFile_SIMC) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl << rootFile_SIMC <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  TFile *InFile = new TFile(rootFile, "READ");
  TFile *InFile_Dummy = new TFile(rootFile_Dummy, "READ");
  TFile *InFile_SIMC = new TFile(rootFile_SIMC, "READ");
  TString TOutFilename = OutFilename;

  TString foutname = OutPath+"/" + TOutFilename + ".root";
  TString fouttxt  = OutPath+"/" + TOutFilename + ".txt";
  TString outputpdf  = OutPath+"/" + TOutFilename + ".pdf";
   
  //#################################################################### 

  TTree* TBRANCH  = (TTree*)InFile->Get("Uncut_Proton_Events");Long64_t nEntries_TBRANCH  = (Long64_t)TBRANCH->GetEntries();  

  TTree* TBRANCH_Dummy  = (TTree*)InFile->Get("Uncut_Proton_Events");Long64_t nEntries_TBRANCH_Dummy  = (Long64_t)TBRANCH_Dummy->GetEntries();  
 
  TTree* TBRANCH_SIMC  = (TTree*)InFile_SIMC->Get("h10");Long64_t nEntries_TBRANCH_SIMC  = (Long64_t)TBRANCH_SIMC->GetEntries();
  
  //SIMC variables
  //HMS
  Float_t hsdelta;TBRANCH_SIMC->SetBranchAddress("hsdelta", &hsdelta);
  Float_t hsxptar;TBRANCH_SIMC->SetBranchAddress("hsxptar", &hsxptar);
  Float_t hsyptar;TBRANCH_SIMC->SetBranchAddress("hsyptar", &hsyptar);
  Float_t hsxfp;TBRANCH_SIMC->SetBranchAddress("hsxfp", &hsxfp);
  Float_t hsyfp;TBRANCH_SIMC->SetBranchAddress("hsyfp", &hsyfp);
  Float_t hsxpfp;TBRANCH_SIMC->SetBranchAddress("hsxpfp", &hsxpfp);
  Float_t hsypfp;TBRANCH_SIMC->SetBranchAddress("hsypfp", &hsypfp);
  //SHMS
  Float_t ssdelta;TBRANCH_SIMC->SetBranchAddress("ssdelta", &ssdelta);
  Float_t ssxptar;TBRANCH_SIMC->SetBranchAddress("ssxptar", &ssxptar);
  Float_t ssyptar;TBRANCH_SIMC->SetBranchAddress("ssyptar", &ssyptar);
  Float_t ssxfp;TBRANCH_SIMC->SetBranchAddress("ssxfp", &ssxfp);
  Float_t ssyfp;TBRANCH_SIMC->SetBranchAddress("ssyfp", &ssyfp);
  Float_t ssxpfp;TBRANCH_SIMC->SetBranchAddress("ssxpfp", &ssxpfp);
  Float_t ssypfp;TBRANCH_SIMC->SetBranchAddress("ssypfp", &ssypfp);
 
  Float_t q;TBRANCH_SIMC->SetBranchAddress("q", &q);
  Float_t Q2_simc;TBRANCH_SIMC->SetBranchAddress("Q2", &Q2_simc);
  Float_t W_simc;TBRANCH_SIMC->SetBranchAddress("W", &W_simc);
  Float_t epsilon_simc;TBRANCH_SIMC->SetBranchAddress("epsilon", &epsilon_simc);
  Float_t Pmx;TBRANCH_SIMC->SetBranchAddress("Pmx", &Pmx);
  Float_t Pmy;TBRANCH_SIMC->SetBranchAddress("Pmy", &Pmy);
  Float_t Pmz;TBRANCH_SIMC->SetBranchAddress("Pmz", &Pmz);
  Float_t Em;TBRANCH_SIMC->SetBranchAddress("Em", &Em);
  Float_t Pm;TBRANCH_SIMC->SetBranchAddress("Pm", &Pm);
  Float_t Weight;TBRANCH_SIMC->SetBranchAddress("Weight", &Weight);

  //DATA variables
  Double_t  CTime_ePiCoinTime_ROC1;TBRANCH->SetBranchAddress("CTime_ePiCoinTime_ROC1", &CTime_ePiCoinTime_ROC1);
  Double_t  CTime_eKCoinTime_ROC1;TBRANCH->SetBranchAddress("CTime_eKCoinTime_ROC1", &CTime_eKCoinTime_ROC1);
  Double_t  CTime_epCoinTime_ROC1;TBRANCH->SetBranchAddress("CTime_epCoinTime_ROC1", &CTime_epCoinTime_ROC1);
  Double_t  P_RF_tdcTime;TBRANCH->SetBranchAddress("P_RF_tdcTime", &P_RF_tdcTime);
  Double_t  P_hod_fpHitsTime;TBRANCH->SetBranchAddress("P_hod_fpHitsTime", &P_hod_fpHitsTime);
  Double_t  H_RF_Dist;TBRANCH->SetBranchAddress("H_RF_Dist", &H_RF_Dist);
  Double_t  P_RF_Dist;TBRANCH->SetBranchAddress("P_RF_Dist", &P_RF_Dist);
  Double_t  P_dc_InsideDipoleExit;TBRANCH->SetBranchAddress("P_dc_InsideDipoleExit", &P_dc_InsideDipoleExit);
  Double_t  P_hod_betanotrack;TBRANCH->SetBranchAddress("P_hod_betanotrack", &P_hod_betanotrack);
 
  //HMS Info 
  Double_t  H_hod_goodscinhit;TBRANCH->SetBranchAddress("H_hod_goodscinhit", &H_hod_goodscinhit);
  Double_t  H_hod_goodstarttime;TBRANCH->SetBranchAddress("H_hod_goodstarttime", &H_hod_goodstarttime);
  Double_t  H_dc_x_fp;TBRANCH->SetBranchAddress("H_dc_x_fp", &H_dc_x_fp);   
  Double_t  H_dc_y_fp;TBRANCH->SetBranchAddress("H_dc_y_fp", &H_dc_y_fp);   
  Double_t  H_dc_xp_fp;TBRANCH->SetBranchAddress("H_dc_xp_fp", &H_dc_xp_fp);   
  Double_t  H_dc_yp_fp;TBRANCH->SetBranchAddress("H_dc_yp_fp", &H_dc_yp_fp);   
  Double_t  H_gtr_beta;TBRANCH->SetBranchAddress("H_gtr_beta", &H_gtr_beta);
  Double_t  H_gtr_xptar;TBRANCH->SetBranchAddress("H_gtr_xp", &H_gtr_xptar);   
  Double_t  H_gtr_yptar;TBRANCH->SetBranchAddress("H_gtr_yp", &H_gtr_yptar);   
  Double_t  H_gtr_dp;TBRANCH->SetBranchAddress("H_gtr_dp", &H_gtr_dp);   
  Double_t  H_gtr_p;TBRANCH->SetBranchAddress("H_gtr_p", &H_gtr_p);   
  Double_t  H_cal_etotnorm;TBRANCH->SetBranchAddress("H_cal_etotnorm", &H_cal_etotnorm);   
  Double_t  H_cal_etottracknorm;TBRANCH->SetBranchAddress("H_cal_etottracknorm", &H_cal_etottracknorm);   
  Double_t  H_cer_npeSum;TBRANCH->SetBranchAddress("H_cer_npeSum", &H_cer_npeSum);   

  //SHMS Info
  Double_t  P_hod_goodscinhit;TBRANCH->SetBranchAddress("P_hod_goodscinhit", &P_hod_goodscinhit);   
  Double_t  P_hod_goodstarttime;TBRANCH->SetBranchAddress("P_hod_goodstarttime", &P_hod_goodstarttime);   
  Double_t  P_dc_x_fp;TBRANCH->SetBranchAddress("P_dc_x_fp", &P_dc_x_fp);   
  Double_t  P_dc_y_fp;TBRANCH->SetBranchAddress("P_dc_y_fp", &P_dc_y_fp);   
  Double_t  P_dc_xp_fp;TBRANCH->SetBranchAddress("P_dc_xp_fp", &P_dc_xp_fp);   
  Double_t  P_dc_yp_fp;TBRANCH->SetBranchAddress("P_dc_yp_fp", &P_dc_yp_fp);   
  Double_t  P_gtr_beta;TBRANCH->SetBranchAddress("P_gtr_beta", &P_gtr_beta);   
  Double_t  P_gtr_xptar;TBRANCH->SetBranchAddress("P_gtr_xp", &P_gtr_xptar);   
  Double_t  P_gtr_yptar;TBRANCH->SetBranchAddress("P_gtr_yp", &P_gtr_yptar);   
  Double_t  P_gtr_p;TBRANCH->SetBranchAddress("P_gtr_p", &P_gtr_p);   
  Double_t  P_gtr_dp;TBRANCH->SetBranchAddress("P_gtr_dp", &P_gtr_dp);   
  Double_t  P_cal_etotnorm;TBRANCH->SetBranchAddress("P_cal_etotnorm", &P_cal_etotnorm);   
  Double_t  P_cal_etottracknorm;TBRANCH->SetBranchAddress("P_cal_etottracknorm", &P_cal_etottracknorm);   
  Double_t  P_aero_npeSum;TBRANCH->SetBranchAddress("P_aero_npeSum", &P_aero_npeSum);   
  Double_t  P_aero_xAtAero;TBRANCH->SetBranchAddress("P_aero_xAtAero", &P_aero_xAtAero);   
  Double_t  P_aero_yAtAero;TBRANCH->SetBranchAddress("P_aero_yAtAero", &P_aero_yAtAero);   
  Double_t  P_hgcer_npeSum;TBRANCH->SetBranchAddress("P_hgcer_npeSum", &P_hgcer_npeSum);   
  Double_t  P_hgcer_xAtCer;TBRANCH->SetBranchAddress("P_hgcer_xAtCer", &P_hgcer_xAtCer);   
  Double_t  P_hgcer_yAtCer;TBRANCH->SetBranchAddress("P_hgcer_yAtCer", &P_hgcer_yAtCer);   

  // Kinematic quantitites 
  Double_t  Q2;TBRANCH->SetBranchAddress("Q2", &Q2);   
  Double_t  W;TBRANCH->SetBranchAddress("W", &W);   
  Double_t  epsilon;TBRANCH->SetBranchAddress("epsilon", &epsilon);   
  Double_t  ph_q;TBRANCH->SetBranchAddress("ph_q", &ph_q);   
  Double_t  emiss;TBRANCH->SetBranchAddress("emiss", &emiss);   
  Double_t  pmiss;TBRANCH->SetBranchAddress("pmiss", &pmiss);   
  Double_t  MMpi;TBRANCH->SetBranchAddress("MMpi", &MMpi);   
  Double_t  MMK;TBRANCH->SetBranchAddress("MMK", &MMK);   
  Double_t  MMp;TBRANCH->SetBranchAddress("MMp", &MMp);   
  Double_t  MandelT;TBRANCH->SetBranchAddress("MandelT", &MandelT);   
  Double_t  pmiss_x;TBRANCH->SetBranchAddress("pmiss_x", &pmiss_x);   
  Double_t  pmiss_y;TBRANCH->SetBranchAddress("pmiss_y", &pmiss_y);   
  Double_t  pmiss_z;TBRANCH->SetBranchAddress("pmiss_z", &pmiss_z);   

  //DUMMY variables
  Double_t  CTime_ePiCoinTime_ROC1_Dummy;TBRANCH_Dummy->SetBranchAddress("CTime_ePiCoinTime_ROC1", &CTime_ePiCoinTime_ROC1);
  Double_t  CTime_eKCoinTime_ROC1_Dummy;TBRANCH_Dummy->SetBranchAddress("CTime_eKCoinTime_ROC1", &CTime_eKCoinTime_ROC1);
  Double_t  CTime_epCoinTime_ROC1_Dummy;TBRANCH_Dummy->SetBranchAddress("CTime_epCoinTime_ROC1", &CTime_epCoinTime_ROC1);
  Double_t  P_RF_tdcTime_Dummy;TBRANCH_Dummy->SetBranchAddress("P_RF_tdcTime", &P_RF_tdcTime);
  Double_t  P_hod_fpHitsTime_Dummy;TBRANCH_Dummy->SetBranchAddress("P_hod_fpHitsTime", &P_hod_fpHitsTime);
  Double_t  H_RF_Dist_Dummy;TBRANCH_Dummy->SetBranchAddress("H_RF_Dist", &H_RF_Dist);
  Double_t  P_RF_Dist_Dummy;TBRANCH_Dummy->SetBranchAddress("P_RF_Dist", &P_RF_Dist);
  Double_t  P_dc_InsideDipoleExit_Dummy;TBRANCH_Dummy->SetBranchAddress("P_dc_InsideDipoleExit", &P_dc_InsideDipoleExit);
  Double_t  P_hod_betanotrack_Dummy;TBRANCH_Dummy->SetBranchAddress("P_hod_betanotrack", &P_hod_betanotrack);
 
  //HMS Info 
  Double_t  H_hod_goodscinhit_Dummy;TBRANCH_Dummy->SetBranchAddress("H_hod_goodscinhit", &H_hod_goodscinhit);
  Double_t  H_hod_goodstarttime_Dummy;TBRANCH_Dummy->SetBranchAddress("H_hod_goodstarttime", &H_hod_goodstarttime);
  Double_t  H_dc_x_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("H_dc_x_fp", &H_dc_x_fp);   
  Double_t  H_dc_y_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("H_dc_y_fp", &H_dc_y_fp);   
  Double_t  H_dc_xp_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("H_dc_xp_fp", &H_dc_xp_fp);   
  Double_t  H_dc_yp_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("H_dc_yp_fp", &H_dc_yp_fp);   
  Double_t  H_gtr_beta_Dummy;TBRANCH_Dummy->SetBranchAddress("H_gtr_beta", &H_gtr_beta);
  Double_t  H_gtr_xptar_Dummy;TBRANCH_Dummy->SetBranchAddress("H_gtr_xp", &H_gtr_xptar);   
  Double_t  H_gtr_yptar_Dummy;TBRANCH_Dummy->SetBranchAddress("H_gtr_yp", &H_gtr_yptar);   
  Double_t  H_gtr_dp_Dummy;TBRANCH_Dummy->SetBranchAddress("H_gtr_dp", &H_gtr_dp);   
  Double_t  H_gtr_p_Dummy;TBRANCH_Dummy->SetBranchAddress("H_gtr_p", &H_gtr_p);   
  Double_t  H_cal_etotnorm_Dummy;TBRANCH_Dummy->SetBranchAddress("H_cal_etotnorm", &H_cal_etotnorm);   
  Double_t  H_cal_etottracknorm_Dummy;TBRANCH_Dummy->SetBranchAddress("H_cal_etottracknorm", &H_cal_etottracknorm);   
  Double_t  H_cer_npeSum_Dummy;TBRANCH_Dummy->SetBranchAddress("H_cer_npeSum", &H_cer_npeSum);   

  //SHMS Info
  Double_t  P_hod_goodscinhit_Dummy;TBRANCH_Dummy->SetBranchAddress("P_hod_goodscinhit", &P_hod_goodscinhit);   
  Double_t  P_hod_goodstarttime_Dummy;TBRANCH_Dummy->SetBranchAddress("P_hod_goodstarttime", &P_hod_goodstarttime);   
  Double_t  P_dc_x_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("P_dc_x_fp", &P_dc_x_fp);   
  Double_t  P_dc_y_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("P_dc_y_fp", &P_dc_y_fp);   
  Double_t  P_dc_xp_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("P_dc_xp_fp", &P_dc_xp_fp);   
  Double_t  P_dc_yp_fp_Dummy;TBRANCH_Dummy->SetBranchAddress("P_dc_yp_fp", &P_dc_yp_fp);   
  Double_t  P_gtr_beta_Dummy;TBRANCH_Dummy->SetBranchAddress("P_gtr_beta", &P_gtr_beta);   
  Double_t  P_gtr_xptar_Dummy;TBRANCH_Dummy->SetBranchAddress("P_gtr_xp", &P_gtr_xptar);   
  Double_t  P_gtr_yptar_Dummy;TBRANCH_Dummy->SetBranchAddress("P_gtr_yp", &P_gtr_yptar);   
  Double_t  P_gtr_p_Dummy;TBRANCH_Dummy->SetBranchAddress("P_gtr_p", &P_gtr_p);   
  Double_t  P_gtr_dp_Dummy;TBRANCH_Dummy->SetBranchAddress("P_gtr_dp", &P_gtr_dp);   
  Double_t  P_cal_etotnorm_Dummy;TBRANCH_Dummy->SetBranchAddress("P_cal_etotnorm", &P_cal_etotnorm);   
  Double_t  P_cal_etottracknorm_Dummy;TBRANCH_Dummy->SetBranchAddress("P_cal_etottracknorm", &P_cal_etottracknorm);   
  Double_t  P_aero_npeSum_Dummy;TBRANCH_Dummy->SetBranchAddress("P_aero_npeSum", &P_aero_npeSum);   
  Double_t  P_aero_xAtAero_Dummy;TBRANCH_Dummy->SetBranchAddress("P_aero_xAtAero", &P_aero_xAtAero);   
  Double_t  P_aero_yAtAero_Dummy;TBRANCH_Dummy->SetBranchAddress("P_aero_yAtAero", &P_aero_yAtAero);   
  Double_t  P_hgcer_npeSum_Dummy;TBRANCH_Dummy->SetBranchAddress("P_hgcer_npeSum", &P_hgcer_npeSum);   
  Double_t  P_hgcer_xAtCer_Dummy;TBRANCH_Dummy->SetBranchAddress("P_hgcer_xAtCer", &P_hgcer_xAtCer);   
  Double_t  P_hgcer_yAtCer_Dummy;TBRANCH_Dummy->SetBranchAddress("P_hgcer_yAtCer", &P_hgcer_yAtCer);   

  // Kinematic quantitites 
  Double_t  Q2_Dummy;TBRANCH_Dummy->SetBranchAddress("Q2", &Q2);   
  Double_t  W_Dummy;TBRANCH_Dummy->SetBranchAddress("W", &W);   
  Double_t  epsilon_Dummy;TBRANCH_Dummy->SetBranchAddress("epsilon", &epsilon);   
  Double_t  ph_q_Dummy;TBRANCH_Dummy->SetBranchAddress("ph_q", &ph_q);   
  Double_t  emiss_Dummy;TBRANCH_Dummy->SetBranchAddress("emiss", &emiss);   
  Double_t  pmiss_Dummy;TBRANCH_Dummy->SetBranchAddress("pmiss", &pmiss);   
  Double_t  MMpi_Dummy;TBRANCH_Dummy->SetBranchAddress("MMpi", &MMpi);   
  Double_t  MMK_Dummy;TBRANCH_Dummy->SetBranchAddress("MMK", &MMK);   
  Double_t  MMp_Dummy;TBRANCH_Dummy->SetBranchAddress("MMp", &MMp);   
  Double_t  MandelT_Dummy;TBRANCH_Dummy->SetBranchAddress("MandelT", &MandelT);   
  Double_t  pmiss_x_Dummy;TBRANCH_Dummy->SetBranchAddress("pmiss_x", &pmiss_x);   
  Double_t  pmiss_y_Dummy;TBRANCH_Dummy->SetBranchAddress("pmiss_y", &pmiss_y);   
  Double_t  pmiss_z_Dummy;TBRANCH_Dummy->SetBranchAddress("pmiss_z", &pmiss_z);   



  //##############################################################################

  TH1D *H_hsdelta_DATA  = new TH1D("H_hsdelta_DATA","HMS Delta; hsdelta;", 300, -20.0, 20.0);
  TH1D *H_hsdelta_DUMMY  = new TH1D("H_hsdelta_DUMMY","HMS Delta; hsdelta_Dummy;", 300, -20.0, 20.0);
  TH1D *H_hsdelta_SIMC  = new TH1D("H_hsdelta_SIMC","HMS Delta; hsdelta;", 300, -20.0, 20.0);

  TH1D *H_hsxptar_DATA  = new TH1D("H_hsxptar_DATA","HMS xptar; hsxptar;", 300, -0.1, 0.1);
  TH1D *H_hsxptar_DUMMY  = new TH1D("H_hsxptar_DUMMY","HMS xptar; hsxptar_Dummy;", 300, -0.1, 0.1);
  TH1D *H_hsxptar_SIMC  = new TH1D("H_hsxptar_SIMC","HMS xptar; hsxptar;", 300, -0.1, 0.1);

  TH1D *H_hsyptar_DATA  = new TH1D("H_hsyptar_DATA","HMS yptar; hsyptar;", 300, -0.05, 0.05);
  TH1D *H_hsyptar_DUMMY  = new TH1D("H_hsyptar_DUMMY","HMS yptar; hsyptar_Dummy;", 300, -0.05, 0.05);
  TH1D *H_hsyptar_SIMC  = new TH1D("H_hsyptar_SIMC","HMS yptar; hsyptar;", 300, -0.05, 0.05);

  TH1D *H_ssxfp_DATA    = new TH1D("H_ssxfp_DATA","SHMS xfp; ssxfp;", 300, -20.0, 20.0);
  TH1D *H_ssxfp_DUMMY    = new TH1D("H_ssxfp_DUMMY","SHMS xfp; ssxfp_Dummy;", 300, -20.0, 20.0);
  TH1D *H_ssxfp_SIMC    = new TH1D("H_ssxfp_SIMC","SHMS xfp; ssxfp;", 300, -20.0, 20.0);

  TH1D *H_ssyfp_DATA    = new TH1D("H_ssyfp_DATA","SHMS yfp; ssyfp;", 300, -20.0, 20.0);
  TH1D *H_ssyfp_DUMMY    = new TH1D("H_ssyfp_DUMMY","SHMS yfp; ssyfp_Dummy;", 300, -20.0, 20.0);
  TH1D *H_ssyfp_SIMC    = new TH1D("H_ssyfp_SIMC","SHMS yfp; ssyfp;", 300, -20.0, 20.0);

  TH1D *H_ssxpfp_DATA   = new TH1D("H_ssxpfp_DATA","SHMS xpfp; ssxpfp;", 300, -0.09, 0.05);
  TH1D *H_ssxpfp_DUMMY   = new TH1D("H_ssxpfp_DUMMY","SHMS xpfp; ssxpfp_Dummy;", 300, -0.09, 0.05);
  TH1D *H_ssxpfp_SIMC   = new TH1D("H_ssxpfp_SIMC","SHMS xpfp; ssxpfp;", 300, -0.09, 0.05);

  TH1D *H_ssypfp_DATA   = new TH1D("H_ssypfp_DATA","SHMS ypfp; ssypfp;", 300, -0.05, 0.04);
  TH1D *H_ssypfp_DUMMY   = new TH1D("H_ssypfp_DUMMY","SHMS ypfp; ssypfp_Dummy;", 300, -0.05, 0.04);
  TH1D *H_ssypfp_SIMC   = new TH1D("H_ssypfp_SIMC","SHMS ypfp; ssypfp;", 300, -0.05, 0.04);

  TH1D *H_hsxfp_DATA    = new TH1D("H_hsxfp_DATA","HMS xfp; hsxfp;", 300, -40.0, 40.0);
  TH1D *H_hsxfp_DUMMY    = new TH1D("H_hsxfp_DUMMY","HMS xfp; hsxfp_Dummy;", 300, -40.0, 40.0);
  TH1D *H_hsxfp_SIMC    = new TH1D("H_hsxfp_SIMC","HMS xfp; hsxfp;", 300, -40.0, 40.0);

  TH1D *H_hsyfp_DATA    = new TH1D("H_hsyfp_DATA","HMS yfp; hsyfp;", 300, -20.0, 20.0);
  TH1D *H_hsyfp_DUMMY    = new TH1D("H_hsyfp_DUMMY","HMS yfp; hsyfp_Dummy;", 300, -20.0, 20.0);
  TH1D *H_hsyfp_SIMC    = new TH1D("H_hsyfp_SIMC","HMS yfp; hsyfp;", 300, -20.0, 20.0);

  TH1D *H_hsxpfp_DATA   = new TH1D("H_hsxpfp_DATA","HMS xpfp; hsxpfp;", 300, -0.09, 0.05);
  TH1D *H_hsxpfp_DUMMY   = new TH1D("H_hsxpfp_DUMMY","HMS xpfp; hsxpfp_Dummy;", 300, -0.09, 0.05);
  TH1D *H_hsxpfp_SIMC   = new TH1D("H_hsxpfp_SIMC","HMS xpfp; hsxpfp;", 300, -0.09, 0.05);
 
  TH1D *H_hsypfp_DATA   = new TH1D("H_hsypfp_DATA","HMS ypfp; hsypfp;", 300, -0.05, 0.04);
  TH1D *H_hsypfp_DUMMY   = new TH1D("H_hsypfp_DUMMY","HMS ypfp; hsypfp_Dummy;", 300, -0.05, 0.04);
  TH1D *H_hsypfp_SIMC   = new TH1D("H_hsypfp_SIMC","HMS ypfp; hsypfp;", 300, -0.05, 0.04);

  TH1D *H_ssdelta_DATA  = new TH1D("H_ssdelta_DATA","SHMS delta; ssdelta;", 300, -20.0, 20.0);
  TH1D *H_ssdelta_DUMMY  = new TH1D("H_ssdelta_DUMMY","SHMS delta; ssdelta_Dummy;", 300, -20.0, 20.0);
  TH1D *H_ssdelta_SIMC  = new TH1D("H_ssdelta_SIMC","SHMS delta; ssdelta;", 300, -20.0, 20.0);

  TH1D *H_ssxptar_DATA  = new TH1D("H_ssxptar_DATA","SHMS xptar; ssxptar;", 300, -0.05, 0.05);
  TH1D *H_ssxptar_DUMMY  = new TH1D("H_ssxptar_DUMMY","SHMS xptar; ssxptar_Dummy;", 300, -0.05, 0.05);
  TH1D *H_ssxptar_SIMC  = new TH1D("H_ssxptar_SIMC","SHMS xptar; ssxptar;", 300, -0.05, 0.05);

  TH1D *H_ssyptar_DATA  = new TH1D("H_ssyptar_DATA","SHMS yptar; ssyptar;", 300, -0.04, 0.04);
  TH1D *H_ssyptar_DUMMY  = new TH1D("H_ssyptar_DUMMY","SHMS yptar; ssyptar_Dummy;", 300, -0.04, 0.04);
  TH1D *H_ssyptar_SIMC  = new TH1D("H_ssyptar_SIMC","SHMS yptar; ssyptar;", 300, -0.04, 0.04);

  TH1D *H_q_DATA        = new TH1D("H_q_DATA","q; q;", 300, 5.0, 7.0);
  TH1D *H_q_DUMMY        = new TH1D("H_q_DUMMY","q; q_Dummy;", 300, 5.0, 7.0);
  TH1D *H_q_SIMC        = new TH1D("H_q_SIMC","q; q;", 300, 5.0, 7.0);

  TH1D *H_Q2_DATA       = new TH1D("H_Q2_DATA","Q2; Q2;", 300, 2.0, 5.0);  
  TH1D *H_Q2_DUMMY       = new TH1D("H_Q2_DUMMY","Q2; Q2_Dummy;", 300, 2.0, 5.0);  
  TH1D *H_Q2_SIMC       = new TH1D("H_Q2_SIMC","Q2; Q2;", 300, 2.0, 5.0);  

  TH1D *H_epsilon_DATA  = new TH1D("H_epsilon_DATA","epsilon; epsilon;", 300, 0.5, 1.0);
  TH1D *H_epsilon_DUMMY  = new TH1D("H_epsilon_DUMMY","epsilon; epsilon_Dummy;", 300, 0.5, 1.0);
  TH1D *H_epsilon_SIMC  = new TH1D("H_epsilon_SIMC","epsilon; epsilon;", 300, 0.5, 1.0);

  TH1D *H_MMp_DATA  = new TH1D("H_MMp_DATA","MMp ; MMp;", 300, -0.01, 0.01);
  TH1D *H_MMp_DUMMY  = new TH1D("H_MMp_DUMMY","MMp ; MMp_Dummy;", 300, -0.01, 0.01);
  TH1D *H_MMp_SIMC  = new TH1D("H_MMp_SIMC","MMp ; MMp;", 300, -0.01, 0.01);
 
  TH1D *H_th_DATA  = new TH1D("H_th_DATA","X' tar; P_gtr_xp;", 300, -0.1, 0.1);
  TH1D *H_th_DUMMY  = new TH1D("H_th_DUMMY","X' tar; P_gtr_xp_Dummy;", 300, -0.1, 0.1);
  TH1D *H_th_SIMC  = new TH1D("H_th_SIMC","H_th_simc; ssxptar;", 300, -0.1, 0.1);

  TH1D *H_ph_DATA  = new TH1D("H_ph_DATA","Y' tar; P_gtr_yp;", 300, -0.1, 0.1);
  TH1D *H_ph_DUMMY  = new TH1D("H_ph_DUMMY","Y' tar; P_gtr_yp_Dummy;", 300, -0.1, 0.1);
  TH1D *H_ph_SIMC  = new TH1D("H_ph_SIMC","H_ph_simc; ssyptar;", 300, -0.1, 0.1);

  TH1D *H_pmiss_DATA  = new TH1D("H_pmiss_DATA","pmiss; Pm;", 300, -0.1, 0.4);
  TH1D *H_pmiss_DUMMY  = new TH1D("H_pmiss_DUMMY","pmiss; Pm_Dummy;", 300, -0.1, 0.4);
  TH1D *H_pmiss_SIMC  = new TH1D("H_pmiss_SIMC","pmiss; Pm;", 300, -0.1, 0.4);

  TH1D *H_emiss_DATA  = new TH1D("H_emiss_DATA","emiss; emiss;", 300, -0.1, 0.4);
  TH1D *H_emiss_DUMMY  = new TH1D("H_emiss_DUMMY","emiss; emiss_Dummy;", 300, -0.1, 0.4);
  TH1D *H_emiss_SIMC  = new TH1D("H_emiss_SIMC","emiss; emiss;", 300, -0.1, 0.4);
 
  TH1D *H_pmx_DATA  = new TH1D("H_pmx_DATA","Pmx; Pmx;", 300, -0.2, 0.2);
  TH1D *H_pmx_DUMMY  = new TH1D("H_pmx_DUMMY","Pmx; Pmx_Dummy;", 300, -0.2, 0.2);
  TH1D *H_pmx_SIMC  = new TH1D("H_pmx_SIMC","Pmx; Pmx;", 300, -0.2, 0.2);

  TH1D *H_pmy_DATA  = new TH1D("H_pmy_DATA","Pmy ; Pmy;", 300, -0.2, 0.2);
  TH1D *H_pmy_DUMMY  = new TH1D("H_pmy_DUMMY","Pmy ; Pmy_Dummy;", 300, -0.2, 0.2);
  TH1D *H_pmy_SIMC  = new TH1D("H_pmy_SIMC","Pmy; Pmy;", 300, -0.2, 0.2);

  TH1D *H_pmz_DATA  = new TH1D("H_pmz_DATA","Pmz; Pmz;", 300, -0.2, 0.2);
  TH1D *H_pmz_DUMMY  = new TH1D("H_pmz_DUMMY","Pmz; Pmz_Dummy;", 300, -0.2, 0.2);
  TH1D *H_pmz_SIMC  = new TH1D("H_pmz_SIMC","Pmz; Pmz;", 300, -0.2, 0.2);

  TH1D *H_W_DATA  = new TH1D("H_W_DATA","W ; W;", 300, -0.5, 1.5);
  TH1D *H_W_DUMMY  = new TH1D("H_W_DUMMY","W ; W_Dummy;", 300, -0.5, 1.5);
  TH1D *H_W_SIMC  = new TH1D("H_W_SIMC","W; W;", 300, -0.5, 1.5);
 
  // Hist for ROOT file
  TH1D *H_epcoin                = new TH1D("H_epcoin"," e-p events; CTime_epCoinTime_ROC1;", 300, -20.0, 20.0);
  TH1D *H_epcoin_betazero       = new TH1D("H_epcoin_betazero"," e-p events at Beta = 0; CTime_epCoinTime_ROC1;", 300, -20.0, 20.0);
  TH2D *H_epcoin_beta           = new TH2D("H_epcoin_beta", "e-p coin time vs beta; CTime_epCoinTime_ROC1; H_gtr_beta;", 300, -20.0, 20.0, 300, -1.0, 2.0);

  for(Long64_t i = 0; i < nEntries_TBRANCH_SIMC; i++)
    {
      TBRANCH_SIMC->GetEntry(i);
      // Define the acceptance cuts  
      
      Double_t CUT1;           //HMS Delta
      Double_t CUT2;          // HMS xptar
      Double_t CUT3;         //  HMS yptar
      Double_t CUT4;        // SHMS Delta
      Double_t CUT5;       //  SHMS xptar
      Double_t CUT6;      //   SHMS yptar
      // Select the cuts
      //HMS
      CUT1 = hsdelta >=-8.0 && hsdelta <=8.0;
      CUT2 = hsxptar >=-0.08 && hsxpfp <=0.08;
      CUT3 = hsyptar >=-0.045 && hsypfp <=0.045;
  
      //SHMS    
      CUT4 = ssdelta >=-10.0 && hsdelta <=20.0;
      CUT5 = ssxptar >=-0.06 && hsxpfp <=0.06;
      CUT6 = hsyptar >=-0.04 && hsypfp <=0.04;
 
      //........................................
      
      //Fill SIMC events

      if(CUT1 && CUT2 && CUT3 && CUT4 && CUT5 && CUT6)
	{
	  H_ssxfp_SIMC->Fill(ssxfp);
	  H_ssyfp_SIMC->Fill(ssyfp);
	  H_ssxpfp_SIMC->Fill(ssxpfp);
	  H_ssypfp_SIMC->Fill(ssypfp);
	  H_hsxfp_SIMC->Fill(hsxfp);
	  H_hsyfp_SIMC->Fill(hsyfp);
	  H_hsxpfp_SIMC->Fill(hsxpfp);
	  H_hsypfp_SIMC->Fill(hsypfp);
	  H_ssdelta_SIMC->Fill(ssdelta); 
	  H_hsdelta_SIMC->Fill(hsdelta);	
	  H_ssxptar_SIMC->Fill(ssxptar);
	  H_ssyptar_SIMC->Fill(ssyptar);
	  H_hsxptar_SIMC->Fill(hsxptar);	
	  H_hsyptar_SIMC->Fill(hsyptar);	
	  H_pmiss_SIMC->Fill(Pm);	
	  H_emiss_SIMC->Fill(Em);	
	  H_pmx_SIMC->Fill(Pmx);
	  H_pmy_SIMC->Fill(Pmy);
	  H_pmz_SIMC->Fill(Pmz);
	  H_Q2_SIMC->Fill(Q2_simc);
	  H_W_SIMC->Fill(W_simc);
	  H_epsilon_SIMC->Fill(epsilon_simc);
	  H_MMp_SIMC->Fill((pow(Em, 2) - pow(Pm, 2)));  
	}
    }

  // Fill data events 

  for(Long64_t i = 0; i < nEntries_TBRANCH; i++)
    {
      TBRANCH->GetEntry(i);   
      
      H_ssxfp_DATA->Fill(P_dc_x_fp);
      H_ssyfp_DATA->Fill(P_dc_y_fp);
      H_ssxpfp_DATA->Fill(P_dc_xp_fp);
      H_ssypfp_DATA->Fill(P_dc_yp_fp);
      H_hsxfp_DATA->Fill(H_dc_x_fp);
      H_hsyfp_DATA->Fill(H_dc_y_fp);
      H_hsxpfp_DATA->Fill(H_dc_xp_fp);
      H_hsypfp_DATA->Fill(H_dc_yp_fp);
      H_ssxptar_DATA->Fill(P_gtr_xptar);
      H_ssyptar_DATA->Fill(P_gtr_yptar);
      H_hsxptar_DATA->Fill(H_gtr_xptar);	
      H_hsyptar_DATA->Fill(H_gtr_yptar);	
      H_ssdelta_DATA->Fill(P_gtr_dp);
      H_hsdelta_DATA->Fill(H_gtr_dp);	
      H_Q2_DATA->Fill(Q2);
      H_epsilon_DATA->Fill(epsilon);
      H_MMp_DATA->Fill(pow(emiss, 2) - pow(pmiss, 2));  
      H_pmiss_DATA->Fill(pmiss);
      H_emiss_DATA->Fill(emiss);	
      H_pmx_DATA->Fill(pmiss_x); 
      H_pmy_DATA->Fill(pmiss_y); 
      H_pmz_DATA->Fill(pmiss_z); 
      H_W_DATA->Fill(W);
	  
    }


  for(Long64_t i = 0; i < nEntries_TBRANCH_Dummy; i++)
    {
      TBRANCH_Dummy->GetEntry(i);   
      
      H_ssxfp_DUMMY->Fill(P_dc_x_fp);
      H_ssyfp_DUMMY->Fill(P_dc_y_fp);
      H_ssxpfp_DUMMY->Fill(P_dc_xp_fp);
      H_ssypfp_DUMMY->Fill(P_dc_yp_fp);
      H_hsxfp_DUMMY->Fill(H_dc_x_fp);
      H_hsyfp_DUMMY->Fill(H_dc_y_fp);
      H_hsxpfp_DUMMY->Fill(H_dc_xp_fp);
      H_hsypfp_DUMMY->Fill(H_dc_yp_fp);
      H_ssxptar_DUMMY->Fill(P_gtr_xptar);
      H_ssyptar_DUMMY->Fill(P_gtr_yptar);
      H_hsxptar_DUMMY->Fill(H_gtr_xptar);	
      H_hsyptar_DUMMY->Fill(H_gtr_yptar);	
      H_ssdelta_DUMMY->Fill(P_gtr_dp);
      H_hsdelta_DUMMY->Fill(H_gtr_dp);	
      H_Q2_DUMMY->Fill(Q2);
      H_epsilon_DUMMY->Fill(epsilon);
      H_MMp_DUMMY->Fill(pow(emiss, 2) - pow(pmiss, 2));  
      H_pmiss_DUMMY->Fill(pmiss);
      H_emiss_DUMMY->Fill(emiss);	
      H_pmx_DUMMY->Fill(pmiss_x); 
      H_pmy_DUMMY->Fill(pmiss_y); 
      H_pmz_DUMMY->Fill(pmiss_z); 
      H_W_DUMMY->Fill(W);
	  
    }


  // Dummy Subtraction
  H_ssxfp_DATA->Add(H_ssxfp_DUMMY,-1);
  H_ssyfp_DATA->Add(H_ssyfp_DUMMY,-1);
  H_ssxpfp_DATA->Add(H_ssxpfp_DUMMY,-1);
  H_ssypfp_DATA->Add(H_ssypfp_DUMMY,-1);
  H_hsxfp_DATA->Add(H_hsxfp_DUMMY,-1);
  H_hsyfp_DATA->Add(H_hsyfp_DUMMY,-1);
  H_hsxpfp_DATA->Add(H_hsxpfp_DUMMY,-1);
  H_hsypfp_DATA->Add(H_hsypfp_DUMMY,-1);
  H_ssxptar_DATA->Add(H_ssxptar_DUMMY,-1);
  H_ssyptar_DATA->Add(H_ssyptar_DUMMY,-1);
  H_hsxptar_DATA->Add(H_hsxptar_DUMMY,-1);
  H_hsyptar_DATA->Add(H_hsyptar_DUMMY,-1);
  H_ssdelta_DATA->Add(H_ssdelta_DUMMY,-1);
  H_hsdelta_DATA->Add(H_hsdelta_DUMMY,-1);
  H_Q2_DATA->Add(H_Q2_DATA,-1);
  H_epsilon_DATA->Add(H_epsilon_DUMMY,-1);
  H_MMp_DATA->Add(H_MMp_DUMMY,-1);
  H_pmiss_DATA->Add(H_pmiss_DUMMY,-1);
  H_emiss_DATA->Add(H_emiss_DUMMY,-1);
  H_pmx_DATA->Add(H_pmx_DUMMY,-1);
  H_pmy_DATA->Add(H_pmy_DUMMY,-1);
  H_pmz_DATA->Add(H_pmz_DUMMY,-1);
  H_W_DATA->Add(H_W_DUMMY,-1);
  
  //...................................................................

  // PLOT HIST..

  TCanvas *xfp = new TCanvas("xfp", "SHMS xfp");
  H_ssxfp_DATA->SetLineColor(kRed);

  H_ssxfp_SIMC->Draw("");
  H_ssxfp_DATA->Draw("same");

  xfp->Print(outputpdf + '(');

  TCanvas *yfp = new TCanvas("yfp", "SHMS yfp");
  H_ssyfp_DATA->SetLineColor(kRed);

  H_ssyfp_SIMC->Draw("");
  H_ssyfp_DATA->Draw("same");

  yfp->Print(outputpdf);

  TCanvas *xpfp = new TCanvas("xpfp", "SHMS xpfp");
  H_ssxpfp_DATA->SetLineColor(kRed);

  H_ssxpfp_SIMC->Draw("");
  H_ssxpfp_DATA->Draw("same");

  xpfp->Print(outputpdf);

  TCanvas *ypfp = new TCanvas("ypfp", "SHMS ypfp");
  H_ssypfp_DATA->SetLineColor(kRed);

  H_ssypfp_SIMC->Draw("");
  H_ssypfp_DATA->Draw("same");

  ypfp->Print(outputpdf);

  TCanvas *hxfp = new TCanvas("hxfp", "HMS xfp");
  H_hsxfp_DATA->SetLineColor(kRed);

  H_hsxfp_SIMC->Draw("");
  H_hsxfp_DATA->Draw("same");

  hxfp->Print(outputpdf);

  TCanvas *hyfp = new TCanvas("hyfp", "HMS yfp");
  H_hsyfp_DATA->SetLineColor(kRed);

  H_hsyfp_SIMC->Draw("");
  H_hsyfp_DATA->Draw("same");

  hyfp->Print(outputpdf);

  TCanvas *hxpfp = new TCanvas("hxpfp", "HMS xpfp");
  H_hsxpfp_DATA->SetLineColor(kRed);

  H_hsxpfp_SIMC->Draw("");
  H_hsxpfp_DATA->Draw("same");

  hxpfp->Print(outputpdf);

  TCanvas *hypfp = new TCanvas("hypfp", "HMS ypfp");
  H_hsypfp_DATA->SetLineColor(kRed);

  H_hsypfp_SIMC->Draw("");
  H_hsypfp_DATA->Draw("same");

  hypfp->Print(outputpdf);

  TCanvas *xptar = new TCanvas("xptar", "SHMS xptar");
  H_ssxptar_DATA->SetLineColor(kRed);

  H_ssxptar_SIMC->Draw("");
  H_ssxptar_DATA->Draw("same");

  xptar->Print(outputpdf);

  TCanvas *yptar = new TCanvas("yptar", "SHMS yptar");
  H_ssyptar_DATA->SetLineColor(kRed);

  H_ssyptar_SIMC->Draw("");
  H_ssyptar_DATA->Draw("same");

  yptar->Print(outputpdf);

  TCanvas *hxptar = new TCanvas("hxptar", "HMS xptar");
  H_hsxptar_DATA->SetLineColor(kRed);

  H_hsxptar_SIMC->Draw("");
  H_hsxptar_DATA->Draw("same");

  hxptar->Print(outputpdf);

  TCanvas *hyptar = new TCanvas("hyptar", "HMS yptar");
  H_hsyptar_DATA->SetLineColor(kRed);

  H_hsyptar_SIMC->Draw("");
  H_hsyptar_DATA->Draw("same");
 
  hyptar->Print(outputpdf);

  TCanvas *Delta = new TCanvas("Delta", "SHMS Delta");
  H_ssdelta_DATA->SetLineColor(kRed);

  H_ssdelta_SIMC->Draw("");
  H_ssdelta_DATA->Draw("same");

  Delta->Print(outputpdf);

  TCanvas *hDelta = new TCanvas("hDelta", "HMS Delta");
  H_hsdelta_DATA->SetLineColor(kRed);

  H_hsdelta_SIMC->Draw("");
  H_hsdelta_DATA->Draw("same");

  hDelta->Print(outputpdf);

  TCanvas *CQ2 = new TCanvas("CQ2", "SHMS Q2");
  H_Q2_DATA->SetLineColor(kRed);

  H_Q2_SIMC->Draw("");
  H_Q2_DATA->Draw("same");

  CQ2->Print(outputpdf);

  TCanvas *Cepsilon = new TCanvas("Cepsilon", "epsilon");
  H_epsilon_DATA->SetLineColor(kRed);

  H_epsilon_SIMC->Draw("");
  H_epsilon_DATA->Draw("same");

  Cepsilon->Print(outputpdf);

  TCanvas *CMMp = new TCanvas("CMMp", "Proton missing mass");
  H_MMp_DATA->SetLineColor(kRed);

  H_MMp_SIMC->Draw("");
  H_MMp_DATA->Draw("same");

  CMMp->Print(outputpdf);

  TCanvas *Cpmiss = new TCanvas("Cpmiss", "pmiss");
  H_pmiss_DATA->SetLineColor(kRed);

  H_MMp_SIMC->Draw("");
  H_pmiss_DATA->Draw("same");

  Cpmiss->Print(outputpdf);

  TCanvas *Cemiss = new TCanvas("Cemiss", "emiss");
  H_emiss_DATA->SetLineColor(kRed);

  H_emiss_SIMC->Draw("");
  H_emiss_DATA->Draw("same");

  Cemiss->Print(outputpdf);

  TCanvas *Cpmiss_x = new TCanvas("Cpmiss_x", "pmiss_x");
  H_pmx_DATA->SetLineColor(kRed);

  H_pmx_SIMC->Draw("");
  H_pmx_DATA->Draw("same");
  Cpmiss_x->Print(outputpdf);

  TCanvas *Cpmiss_y = new TCanvas("Cpmiss_y", "pmiss_y");
  H_pmy_DATA->SetLineColor(kRed);

  H_pmy_SIMC->Draw("");
  H_pmy_DATA->Draw("same");

  Cpmiss_y->Print(outputpdf);

  TCanvas *Cpmiss_z = new TCanvas("Cpmiss_z", "pmiss_z");
  H_pmz_DATA->SetLineColor(kRed);

  H_pmz_SIMC->Draw("");
  H_pmz_DATA->Draw("same");

  Cpmiss_z->Print(outputpdf);

  TCanvas *CW = new TCanvas("CW", "W");
  H_W_DATA->SetLineColor(kRed);

  H_W_SIMC->Draw("");
  H_W_DATA->Draw("same");

  CW->Print(outputpdf + ')');
       
}
