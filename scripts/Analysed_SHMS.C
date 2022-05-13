// .... This script has created to analyse HMS Heep data....
// .... Created Date: Dec 5, 2021 ....
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

void Analysed_SHMS(string InDATAFilename = "", string InSIMCFilename = "", string OutFilename = "")
{
  TString Hostname = gSystem->HostName();
  TString User = (gSystem->GetUserInfo())->fUser;
  TString Replaypath;
  TString ROOTfilePath;
  TString OutPath;
  TString rootFile;
  TString rootFile_SIMC;

  gStyle->SetPalette(55);

  // Set paths depending on system you're running on
  if(Hostname.Contains("farm")){
    Replaypath = "/group/c-kaonlt/USERS/"+User+"/hallc_replay_lt";
    // Output path for root file
    ROOTfilePath = Replaypath+"/UTIL_KAONLT/ROOTfiles/Analysis/HeeP";
    OutPath = Replaypath+"/UTIL_KAONLT/OUTPUT/Analysis/HeeP";
  }
  else if(Hostname.Contains("qcd")){
    Replaypath = "/group/c-kaonlt/USERS/"+User+"/hallc_replay_lt";
    // Output path for root file
    ROOTfilePath = Replaypath+"/UTIL_KAONLT/ROOTfiles/Analysis/HeeP";
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

  if(InSIMCFilename == "") {
    cout << "Enter a SIMC ROOT Filename to analyse: ";
    cin >> InSIMCFilename;
  }  

  if(OutFilename == "") {
    cout << "Enter a Filename to output to: ";
    cin >> OutFilename;
  }

  TString TInDATAFilename = InDATAFilename ;
  TString TInSIMCFilename = InSIMCFilename ;
  rootFile = ROOTfilePath+"/"+TInDATAFilename;
  rootFile_SIMC = ROOTfilePath+"/"+TInSIMCFilename;
  if (gSystem->AccessPathName(rootFile) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl <<rootFile <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  if (gSystem->AccessPathName(rootFile_SIMC) == kTRUE){
    cerr << "!!!!! ERROR !!!!! " << endl << rootFile_SIMC <<  " not found" << endl <<  "!!!!! ERRROR !!!!!" << endl;
    exit;
  }

  TFile *InFile = new TFile(rootFile, "READ");
  TFile *InFile_SIMC = new TFile(rootFile_SIMC, "READ");
  TString TOutFilename = OutFilename;

  TString foutname = OutPath+"/" + TOutFilename + ".root";
  TString fouttxt  = OutPath+"/" + TOutFilename + ".txt";
  TString outputpdf  = OutPath+"/" + TOutFilename + ".pdf";
   
  //#################################################################### 

  TTree* TBRANCH  = (TTree*)InFile->Get("Uncut_Proton_Events");Long64_t nEntries_TBRANCH  = (Long64_t)TBRANCH->GetEntries();  
 
  TTree* TBRANCH_SIMC  = (TTree*)InFile_SIMC->Get("h10");Long64_t nEntries_TBRANCH_SIMC  = (Long64_t)TBRANCH_SIMC->GetEntries();

  //SIMC variables

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
  Float_t Weight;TBRANCH_SIMC->SetBranchAddress("Weight", &Weight);

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


  //##############################################################################

  TH1D *H_ssxfp_DATA    = new TH1D("H_ssxfp_DATA","SHMS xfp; ssxfp;", 300, -20.0, 20.0);
  TH1D *H_ssxfp_SIMC    = new TH1D("H_ssxfp_SIMC","SHMS xfp; ssxfp;", 300, -20.0, 20.0);

  TH1D *H_ssyfp_DATA    = new TH1D("H_ssyfp_DATA","SHMS yfp; ssyfp;", 300, -20.0, 20.0);
  TH1D *H_ssyfp_SIMC    = new TH1D("H_ssyfp_SIMC","SHMS yfp; ssyfp;", 300, -20.0, 20.0);

  TH1D *H_ssxpfp_DATA   = new TH1D("H_ssxpfp_DATA","SHMS xpfp; ssxpfp;", 300, -0.09, 0.05);
  TH1D *H_ssxpfp_SIMC   = new TH1D("H_ssxpfp_SIMC","SHMS xpfp; ssxpfp;", 300, -0.09, 0.05);

  TH1D *H_ssypfp_DATA   = new TH1D("H_ssypfp_DATA","SHMS ypfp; ssypfp;", 300, -0.05, 0.04);
  TH1D *H_ssypfp_SIMC   = new TH1D("H_ssypfp_SIMC","SHMS ypfp; ssypfp;", 300, -0.05, 0.04);

  TH1D *H_ssdelta_DATA  = new TH1D("H_ssdelta_DATA","SHMS delta; ssdelta;", 300, -20.0, 20.0);
  TH1D *H_ssdelta_SIMC  = new TH1D("H_ssdelta_SIMC","SHMS delta; ssdelta;", 300, -20.0, 20.0);

  TH1D *H_ssxptar_DATA  = new TH1D("H_ssxptar_DATA","SHMS xptar; ssxptar;", 300, -0.05, 0.05);
  TH1D *H_ssxptar_SIMC  = new TH1D("H_ssxptar_SIMC","SHMS xptar; ssxptar;", 300, -0.05, 0.05);

  TH1D *H_ssyptar_DATA  = new TH1D("H_ssyptar_DATA","SHMS yptar; ssyptar;", 300, -0.04, 0.04);
  TH1D *H_ssyptar_SIMC  = new TH1D("H_ssyptar_SIMC","SHMS yptar; ssyptar;", 300, -0.04, 0.04);

  TH1D *H_q_DATA        = new TH1D("H_q_DATA","q; q;", 300, 5.0, 7.0);
  TH1D *H_q_SIMC        = new TH1D("H_q_SIMC","q; q;", 300, 5.0, 7.0);

  TH1D *H_Q2_DATA       = new TH1D("H_Q2_DATA","Q2; Q2;", 300, 2.0, 5.0);  
  TH1D *H_Q2_SIMC       = new TH1D("H_Q2_SIMC","Q2; Q2;", 300, 2.0, 5.0);  

  TH1D *H_epsilon_DATA  = new TH1D("H_epsilon_DATA","epsilon; epsilon;", 300, 0.5, 1.0);
  TH1D *H_epsilon_SIMC  = new TH1D("H_epsilon_SIMC","epsilon; epsilon;", 300, 0.5, 1.0);

  TH1D *H_th_DATA  = new TH1D("H_th_DATA","X' tar; P_gtr_xp;", 300, -0.1, 0.1);
  TH1D *H_th_SIMC  = new TH1D("H_th_SIMC","H_th_simc; ssxptar;", 300, -0.1, 0.1);

  TH1D *H_ph_DATA  = new TH1D("H_ph_DATA","Y' tar; P_gtr_yp;", 300, -0.1, 0.1);
  TH1D *H_ph_SIMC  = new TH1D("H_ph_SIMC","H_ph_simc; ssyptar;", 300, -0.1, 0.1);

  TH1D *H_W_DATA  = new TH1D("H_W_DATA","W ; W;", 300, -0.5, 1.5);
  TH1D *H_W_SIMC  = new TH1D("H_W_SIMC","W; W;", 300, -0.5, 1.5);
 
  for(Long64_t i = 0; i < nEntries_TBRANCH_SIMC; i++)
    {
      TBRANCH_SIMC->GetEntry(i);
      // Define the acceptance cuts  
      Double_t CUT4;        // SHMS Delta
      Double_t CUT5;       //  SHMS xptar
      Double_t CUT6;      //   SHMS yptar
      // Select the cuts
  
      //SHMS    
      CUT4 = ssdelta >=-10.0 && hsdelta <=20.0;
      CUT5 = ssxptar >=-0.06 && hsxpfp <=0.06;
      CUT6 = hsyptar >=-0.04 && hsypfp <=0.04;
 
      //........................................
      
      //Fill SIMC events

      if(CUT4 && CUT5 && CUT6)
	{
	  H_ssxfp_SIMC->Fill(ssxfp);
	  H_ssyfp_SIMC->Fill(ssyfp);
	  H_ssxpfp_SIMC->Fill(ssxpfp);
	  H_ssypfp_SIMC->Fill(ssypfp);
	  H_ssdelta_SIMC->Fill(ssdelta); 
	  H_ssxptar_SIMC->Fill(ssxptar);
	  H_ssyptar_SIMC->Fill(ssyptar);
	  H_Q2_SIMC->Fill(Q2_simc);
	  H_W_SIMC->Fill(W_simc);
	  H_epsilon_SIMC->Fill(epsilon_simc);
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
      H_ssxptar_DATA->Fill(P_gtr_xptar);
      H_ssyptar_DATA->Fill(P_gtr_yptar);
      H_ssdelta_DATA->Fill(P_gtr_dp);
      H_hsdelta_DATA->Fill(H_gtr_dp);	
      H_Q2_DATA->Fill(Q2);
      H_epsilon_DATA->Fill(epsilon);
      H_W_DATA->Fill(W);
	  
    }
  
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

  TCanvas *Delta = new TCanvas("Delta", "SHMS Delta");
  H_ssdelta_DATA->SetLineColor(kRed);

  H_ssdelta_SIMC->Draw("");
  H_ssdelta_DATA->Draw("same");

  Delta->Print(outputpdf);

  TCanvas *CQ2 = new TCanvas("CQ2", "Q2");
  H_Q2_DATA->SetLineColor(kRed);

  H_Q2_SIMC->Draw("");
  H_Q2_DATA->Draw("same");

  CQ2->Print(outputpdf);

  TCanvas *Cepsilon = new TCanvas("Cepsilon", "epsilon");
  H_epsilon_DATA->SetLineColor(kRed);

  H_epsilon_SIMC->Draw("");
  H_epsilon_DATA->Draw("same");

  Cepsilon->Print(outputpdf);

  TCanvas *CW = new TCanvas("CW", "W");
  H_W_DATA->SetLineColor(kRed);

  H_W_SIMC->Draw("");
  H_W_DATA->Draw("same");

  CW->Print(outputpdf + ')');
       
}
