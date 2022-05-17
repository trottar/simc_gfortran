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
  TString rootFile_DUMMY;
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
  rootFile_DUMMY = ROOTfilePath+"/"+TInDUMMYFilename;
  rootFile_SIMC = ROOTfilePath+"/"+TInSIMCFilename;

  if (gSystem->AccessPathName(rootFile) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl <<rootFile <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  if (gSystem->AccessPathName(rootFile_DUMMY) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl <<rootFile_DUMMY <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  if (gSystem->AccessPathName(rootFile_SIMC) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl << rootFile_SIMC <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  TFile *InFile = new TFile(rootFile, "OPEN");
  InFile->GetListOfKeys()->Print();
  TFile *InFile_DUMMY = new TFile(rootFile_DUMMY, "OPEN");
  TFile *InFile_SIMC = new TFile(rootFile_SIMC, "READ");
  TString TOutFilename = OutFilename;

  TString foutname = OutPath+"/" + TOutFilename + ".root";
  TString fouttxt  = OutPath+"/" + TOutFilename + ".txt";
  TString outputpdf  = OutPath+"/" + TOutFilename + ".pdf";
   
  //#################################################################### 
  
  //TTree* TBRANCH  = (TTree*)InFile->Get("hist");Long64_t nEntries_TBRANCH  = (Long64_t)TBRANCH->GetEntries();  
  
  //TTree* TBRANCH_DUMMY  = (TTree*)InFile_DUMMY->Get("hist");Long64_t nEntries_TBRANCH_DUMMY  = (Long64_t)TBRANCH_DUMMY->GetEntries();  
  
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
  
  //##############################################################################
  
  TH1F *H_hsdelta_DATA  = new TH1F("H_hsdelta_DATA","HMS Delta; hsdelta;", 300, -20.0, 20.0);
  TH1F *H_hsdelta_DUMMY  = new TH1F("H_hsdelta_DUMMY","HMS Delta; hsdelta;", 300, -20.0, 20.0);
  TH1F *H_hsdelta_SIMC  = new TH1F("H_hsdelta_SIMC","HMS Delta; hsdelta;", 300, -20.0, 20.0);

  TH1F *H_hsxptar_DATA  = new TH1F("H_hsxptar_DATA","HMS xptar; hsxptar;", 300, -0.1, 0.1);
  TH1F *H_hsxptar_DUMMY  = new TH1F("H_hsxptar_DUMMY","HMS xptar; hsxptar;", 300, -0.1, 0.1);
  TH1F *H_hsxptar_SIMC  = new TH1F("H_hsxptar_SIMC","HMS xptar; hsxptar;", 300, -0.1, 0.1);

  TH1F *H_hsyptar_DATA  = new TH1F("H_hsyptar_DATA","HMS yptar; hsyptar;", 300, -0.05, 0.05);
  TH1F *H_hsyptar_DUMMY  = new TH1F("H_hsyptar_DUMMY","HMS yptar; hsyptar;", 300, -0.05, 0.05);
  TH1F *H_hsyptar_SIMC  = new TH1F("H_hsyptar_SIMC","HMS yptar; hsyptar;", 300, -0.05, 0.05);

  TH1F *H_ssxfp_DATA    = new TH1F("H_ssxfp_DATA","SHMS xfp; ssxfp;", 300, -20.0, 20.0);
  TH1F *H_ssxfp_DUMMY    = new TH1F("H_ssxfp_DUMMY","SHMS xfp; ssxfp;", 300, -20.0, 20.0);
  TH1F *H_ssxfp_SIMC    = new TH1F("H_ssxfp_SIMC","SHMS xfp; ssxfp;", 300, -20.0, 20.0);

  TH1F *H_ssyfp_DATA    = new TH1F("H_ssyfp_DATA","SHMS yfp; ssyfp;", 300, -20.0, 20.0);
  TH1F *H_ssyfp_DUMMY    = new TH1F("H_ssyfp_DUMMY","SHMS yfp; ssyfp;", 300, -20.0, 20.0);
  TH1F *H_ssyfp_SIMC    = new TH1F("H_ssyfp_SIMC","SHMS yfp; ssyfp;", 300, -20.0, 20.0);

  TH1F *H_ssxpfp_DATA   = new TH1F("H_ssxpfp_DATA","SHMS xpfp; ssxpfp;", 300, -0.09, 0.05);
  TH1F *H_ssxpfp_DUMMY   = new TH1F("H_ssxpfp_DUMMY","SHMS xpfp; ssxpfp;", 300, -0.09, 0.05);
  TH1F *H_ssxpfp_SIMC   = new TH1F("H_ssxpfp_SIMC","SHMS xpfp; ssxpfp;", 300, -0.09, 0.05);

  TH1F *H_ssypfp_DATA   = new TH1F("H_ssypfp_DATA","SHMS ypfp; ssypfp;", 300, -0.05, 0.04);
  TH1F *H_ssypfp_DUMMY   = new TH1F("H_ssypfp_DUMMY","SHMS ypfp; ssypfp;", 300, -0.05, 0.04);
  TH1F *H_ssypfp_SIMC   = new TH1F("H_ssypfp_SIMC","SHMS ypfp; ssypfp;", 300, -0.05, 0.04);

  TH1F *H_hsxfp_DATA    = new TH1F("H_hsxfp_DATA","HMS xfp; hsxfp;", 300, -40.0, 40.0);
  TH1F *H_hsxfp_DUMMY    = new TH1F("H_hsxfp_DUMMY","HMS xfp; hsxfp;", 300, -40.0, 40.0);
  TH1F *H_hsxfp_SIMC    = new TH1F("H_hsxfp_SIMC","HMS xfp; hsxfp;", 300, -40.0, 40.0);

  TH1F *H_hsyfp_DATA    = new TH1F("H_hsyfp_DATA","HMS yfp; hsyfp;", 300, -20.0, 20.0);
  TH1F *H_hsyfp_DUMMY    = new TH1F("H_hsyfp_DUMMY","HMS yfp; hsyfp;", 300, -20.0, 20.0);
  TH1F *H_hsyfp_SIMC    = new TH1F("H_hsyfp_SIMC","HMS yfp; hsyfp;", 300, -20.0, 20.0);

  TH1F *H_hsxpfp_DATA   = new TH1F("H_hsxpfp_DATA","HMS xpfp; hsxpfp;", 300, -0.09, 0.05);
  TH1F *H_hsxpfp_DUMMY   = new TH1F("H_hsxpfp_DUMMY","HMS xpfp; hsxpfp;", 300, -0.09, 0.05);
  TH1F *H_hsxpfp_SIMC   = new TH1F("H_hsxpfp_SIMC","HMS xpfp; hsxpfp;", 300, -0.09, 0.05);
 
  TH1F *H_hsypfp_DATA   = new TH1F("H_hsypfp_DATA","HMS ypfp; hsypfp;", 300, -0.05, 0.04);
  TH1F *H_hsypfp_DUMMY   = new TH1F("H_hsypfp_DUMMY","HMS ypfp; hsypfp;", 300, -0.05, 0.04);
  TH1F *H_hsypfp_SIMC   = new TH1F("H_hsypfp_SIMC","HMS ypfp; hsypfp;", 300, -0.05, 0.04);

  TH1F *H_ssdelta_DATA  = new TH1F("H_ssdelta_DATA","SHMS delta; ssdelta;", 300, -20.0, 20.0);
  TH1F *H_ssdelta_DUMMY  = new TH1F("H_ssdelta_DUMMY","SHMS delta; ssdelta;", 300, -20.0, 20.0);
  TH1F *H_ssdelta_SIMC  = new TH1F("H_ssdelta_SIMC","SHMS delta; ssdelta;", 300, -20.0, 20.0);

  TH1F *H_ssxptar_DATA  = new TH1F("H_ssxptar_DATA","SHMS xptar; ssxptar;", 300, -0.05, 0.05);
  TH1F *H_ssxptar_DUMMY  = new TH1F("H_ssxptar_DUMMY","SHMS xptar; ssxptar;", 300, -0.05, 0.05);
  TH1F *H_ssxptar_SIMC  = new TH1F("H_ssxptar_SIMC","SHMS xptar; ssxptar;", 300, -0.05, 0.05);

  TH1F *H_ssyptar_DATA  = new TH1F("H_ssyptar_DATA","SHMS yptar; ssyptar;", 300, -0.04, 0.04);
  TH1F *H_ssyptar_DUMMY  = new TH1F("H_ssyptar_DUMMY","SHMS yptar; ssyptar;", 300, -0.04, 0.04);
  TH1F *H_ssyptar_SIMC  = new TH1F("H_ssyptar_SIMC","SHMS yptar; ssyptar;", 300, -0.04, 0.04);

  TH1F *H_q_DATA        = new TH1F("H_q_DATA","q; q;", 300, 5.0, 7.0);
  TH1F *H_q_DUMMY        = new TH1F("H_q_DUMMY","q; q;", 300, 5.0, 7.0);
  TH1F *H_q_SIMC        = new TH1F("H_q_SIMC","q; q;", 300, 5.0, 7.0);

  TH1F *H_Q2_DATA       = new TH1F("H_Q2_DATA","Q2; Q2;", 300, 2.0, 5.0);  
  TH1F *H_Q2_DUMMY       = new TH1F("H_Q2_DUMMY","Q2; Q2;", 300, 2.0, 5.0);  
  TH1F *H_Q2_SIMC       = new TH1F("H_Q2_SIMC","Q2; Q2;", 300, 2.0, 5.0);  

  TH1F *H_epsilon_DATA  = new TH1F("H_epsilon_DATA","epsilon; epsilon;", 300, 0.5, 1.0);
  TH1F *H_epsilon_DUMMY  = new TH1F("H_epsilon_DUMMY","epsilon; epsilon;", 300, 0.5, 1.0);
  TH1F *H_epsilon_SIMC  = new TH1F("H_epsilon_SIMC","epsilon; epsilon;", 300, 0.5, 1.0);

  TH1F *H_MMp_DATA  = new TH1F("H_MMp_DATA","MMp ; MMp;", 300, -0.01, 0.01);
  TH1F *H_MMp_DUMMY  = new TH1F("H_MMp_DUMMY","MMp ; MMp;", 300, -0.01, 0.01);
  TH1F *H_MMp_SIMC  = new TH1F("H_MMp_SIMC","MMp ; MMp;", 300, -0.01, 0.01);
 
  TH1F *H_th_DATA  = new TH1F("H_th_DATA","X' tar; P_gtr_xp;", 300, -0.1, 0.1);
  TH1F *H_th_DUMMY  = new TH1F("H_th_DUMMY","X' tar; P_gtr_xp;", 300, -0.1, 0.1);
  TH1F *H_th_SIMC  = new TH1F("H_th_SIMC","H_th_simc; ssxptar;", 300, -0.1, 0.1);

  TH1F *H_ph_DATA  = new TH1F("H_ph_DATA","Y' tar; P_gtr_yp;", 300, -0.1, 0.1);
  TH1F *H_ph_DUMMY  = new TH1F("H_ph_DUMMY","Y' tar; P_gtr_yp;", 300, -0.1, 0.1);
  TH1F *H_ph_SIMC  = new TH1F("H_ph_SIMC","H_ph_simc; ssyptar;", 300, -0.1, 0.1);

  TH1F *H_pmiss_DATA  = new TH1F("H_pmiss_DATA","pmiss; Pm;", 300, -0.1, 0.4);
  TH1F *H_pmiss_DUMMY  = new TH1F("H_pmiss_DUMMY","pmiss; Pm;", 300, -0.1, 0.4);
  TH1F *H_pmiss_SIMC  = new TH1F("H_pmiss_SIMC","pmiss; Pm;", 300, -0.1, 0.4);

  TH1F *H_emiss_DATA  = new TH1F("H_emiss_DATA","emiss; emiss;", 300, -0.1, 0.4);
  TH1F *H_emiss_DUMMY  = new TH1F("H_emiss_DUMMY","emiss; emiss;", 300, -0.1, 0.4);
  TH1F *H_emiss_SIMC  = new TH1F("H_emiss_SIMC","emiss; emiss;", 300, -0.1, 0.4);
 
  TH1F *H_pmx_DATA  = new TH1F("H_pmx_DATA","Pmx; Pmx;", 300, -0.2, 0.2);
  TH1F *H_pmx_DUMMY  = new TH1F("H_pmx_DUMMY","Pmx; Pmx;", 300, -0.2, 0.2);
  TH1F *H_pmx_SIMC  = new TH1F("H_pmx_SIMC","Pmx; Pmx;", 300, -0.2, 0.2);

  TH1F *H_pmy_DATA  = new TH1F("H_pmy_DATA","Pmy ; Pmy;", 300, -0.2, 0.2);
  TH1F *H_pmy_DUMMY  = new TH1F("H_pmy_DUMMY","Pmy ; Pmy;", 300, -0.2, 0.2);
  TH1F *H_pmy_SIMC  = new TH1F("H_pmy_SIMC","Pmy; Pmy;", 300, -0.2, 0.2);

  TH1F *H_pmz_DATA  = new TH1F("H_pmz_DATA","Pmz; Pmz;", 300, -0.2, 0.2);
  TH1F *H_pmz_DUMMY  = new TH1F("H_pmz_DUMMY","Pmz; Pmz;", 300, -0.2, 0.2);
  TH1F *H_pmz_SIMC  = new TH1F("H_pmz_SIMC","Pmz; Pmz;", 300, -0.2, 0.2);

  TH1F *H_W_DATA  = new TH1F("H_W_DATA","W ; W;", 300, -0.5, 1.5);
  TH1F *H_W_DUMMY  = new TH1F("H_W_DUMMY","W ; W;", 300, -0.5, 1.5);
  TH1F *H_W_SIMC  = new TH1F("H_W_SIMC","W; W;", 300, -0.5, 1.5);

  //DATA variables
  //HMS
  //InFile->Get("hist/H_hsdelta",H_hsdelta_DATA);
  H_hsdelta_DATA = (TH1F*)InFile->Get("hist/H_hsdelta");
  // Checks if histogram is empty
  if (!H_hsdelta_DATA){
    cout << "ERROR!!!\n\n\n" << endl;
    return;
  }
  H_hsxptar_DATA = (TH1F*)InFile->Get("hist/H_hsxptar");
  H_hsyptar_DATA = (TH1F*)InFile->Get("hist/H_hsyptar");
  H_hsxfp_DATA = (TH1F*)InFile->Get("hist/H_hsxfp");
  H_hsyfp_DATA = (TH1F*)InFile->Get("hist/H_hsyfp");
  H_hsxpfp_DATA = (TH1F*)InFile->Get("hist/H_hsxpfp");
  H_hsypfp_DATA = (TH1F*)InFile->Get("hist/H_hsypfp");
  //SHMS
  H_ssdelta_DATA = (TH1F*)InFile->Get("hist/H_ssdelta");
  H_ssxptar_DATA = (TH1F*)InFile->Get("hist/H_ssxptar");
  H_ssyptar_DATA = (TH1F*)InFile->Get("hist/H_ssyptar");
  H_ssxfp_DATA = (TH1F*)InFile->Get("hist/H_ssxfp");
  H_ssyfp_DATA = (TH1F*)InFile->Get("hist/H_ssyfp");
  H_ssxpfp_DATA = (TH1F*)InFile->Get("hist/H_ssxpfp");
  H_ssypfp_DATA = (TH1F*)InFile->Get("hist/H_ssypfp");
 
  H_q_DATA = (TH1F*)InFile->Get("hist/H_q");
  H_Q2_DATA = (TH1F*)InFile->Get("hist/H_Q2");
  H_W_DATA = (TH1F*)InFile->Get("hist/H_W");
  H_epsilon_DATA = (TH1F*)InFile->Get("hist/H_epsilon");
  H_pmx_DATA = (TH1F*)InFile->Get("hist/H_pmx");
  H_pmy_DATA = (TH1F*)InFile->Get("hist/H_pmy");
  H_pmz_DATA = (TH1F*)InFile->Get("hist/H_pmz");
  H_emiss_DATA = (TH1F*)InFile->Get("hist/H_emiss");
  H_pmiss_DATA = (TH1F*)InFile->Get("hist/H_pmiss");

  // H_MMp_DATA = (Em_data*Em_data - Pm_data*Pm_data);

  //DUMMY variables
  //HMS
  H_hsdelta_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_hsdelta");
  H_hsxptar_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_hsxptar");
  H_hsyptar_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_hsyptar");
  H_hsxfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_hsxfp");
  H_hsyfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_hsyfp");
  H_hsxpfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_hsxpfp");
  H_hsypfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_hsypfp");
  //SHMS
  H_ssdelta_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_ssdelta");
  H_ssxptar_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_ssxptar");
  H_ssyptar_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_ssyptar");
  H_ssxfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_ssxfp");
  H_ssyfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_ssyfp");
  H_ssxpfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_ssxpfp");
  H_ssypfp_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_ssypfp");
 
  H_q_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_q");
  H_Q2_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_Q2");
  H_W_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_W");
  H_epsilon_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_epsilon");
  H_pmx_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_pmx");
  H_pmy_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_pmy");
  H_pmz_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_pmz");
  H_emiss_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_emiss");
  H_pmiss_DUMMY = (TH1F*)InFile_DUMMY->Get("hist/H_pmiss");

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
  H_Q2_DATA->Add(H_Q2_DUMMY,-1);
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
