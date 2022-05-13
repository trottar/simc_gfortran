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

void Analysed_HMS(string InDATAFilename = "", string InSIMCFilename = "", string OutFilename = "")
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
  //HMS
  Float_t hsdelta;TBRANCH_SIMC->SetBranchAddress("hsdelta", &hsdelta);
  Float_t hsxptar;TBRANCH_SIMC->SetBranchAddress("hsxptar", &hsxptar);
  Float_t hsyptar;TBRANCH_SIMC->SetBranchAddress("hsyptar", &hsyptar);
  Float_t hsxfp;TBRANCH_SIMC->SetBranchAddress("hsxfp", &hsxfp);
  Float_t hsyfp;TBRANCH_SIMC->SetBranchAddress("hsyfp", &hsyfp);
  Float_t hsxpfp;TBRANCH_SIMC->SetBranchAddress("hsxpfp", &hsxpfp);
  Float_t hsypfp;TBRANCH_SIMC->SetBranchAddress("hsypfp", &hsypfp);
 
  Float_t q;TBRANCH_SIMC->SetBranchAddress("q", &q);
  Float_t Q2_simc;TBRANCH_SIMC->SetBranchAddress("Q2", &Q2_simc);
  Float_t W_simc;TBRANCH_SIMC->SetBranchAddress("W", &W_simc);
  Float_t epsilon_simc;TBRANCH_SIMC->SetBranchAddress("epsilon", &epsilon_simc);
  Float_t Weight;TBRANCH_SIMC->SetBranchAddress("Weight", &Weight);
 
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

  // Kinematic quantitites 
  Double_t  Q2;TBRANCH->SetBranchAddress("Q2", &Q2);   
  Double_t  W;TBRANCH->SetBranchAddress("W", &W);   
  Double_t  epsilon;TBRANCH->SetBranchAddress("epsilon", &epsilon);   
  Double_t  ph_q;TBRANCH->SetBranchAddress("ph_q", &ph_q);   


  //##############################################################################

  TH1D *H_hsdelta_DATA  = new TH1D("H_hsdelta_DATA","HMS Delta; hsdelta;", 300, -20.0, 20.0);
  TH1D *H_hsdelta_SIMC  = new TH1D("H_hsdelta_SIMC","HMS Delta; hsdelta;", 300, -20.0, 20.0);

  TH1D *H_hsxptar_DATA  = new TH1D("H_hsxptar_DATA","HMS xptar; hsxptar;", 300, -0.1, 0.1);
  TH1D *H_hsxptar_SIMC  = new TH1D("H_hsxptar_SIMC","HMS xptar; hsxptar;", 300, -0.1, 0.1);

  TH1D *H_hsyptar_DATA  = new TH1D("H_hsyptar_DATA","HMS yptar; hsyptar;", 300, -0.05, 0.05);
  TH1D *H_hsyptar_SIMC  = new TH1D("H_hsyptar_SIMC","HMS yptar; hsyptar;", 300, -0.05, 0.05);

  TH1D *H_hsxfp_DATA    = new TH1D("H_hsxfp_DATA","HMS xfp; hsxfp;", 300, -40.0, 40.0);
  TH1D *H_hsxfp_SIMC    = new TH1D("H_hsxfp_SIMC","HMS xfp; hsxfp;", 300, -40.0, 40.0);

  TH1D *H_hsyfp_DATA    = new TH1D("H_hsyfp_DATA","HMS yfp; hsyfp;", 300, -20.0, 20.0);
  TH1D *H_hsyfp_SIMC    = new TH1D("H_hsyfp_SIMC","HMS yfp; hsyfp;", 300, -20.0, 20.0);

  TH1D *H_hsxpfp_DATA   = new TH1D("H_hsxpfp_DATA","HMS xpfp; hsxpfp;", 300, -0.09, 0.05);
  TH1D *H_hsxpfp_SIMC   = new TH1D("H_hsxpfp_SIMC","HMS xpfp; hsxpfp;", 300, -0.09, 0.05);
 
  TH1D *H_hsypfp_DATA   = new TH1D("H_hsypfp_DATA","HMS ypfp; hsypfp;", 300, -0.05, 0.04);
  TH1D *H_hsypfp_SIMC   = new TH1D("H_hsypfp_SIMC","HMS ypfp; hsypfp;", 300, -0.05, 0.04);

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
      
      Double_t CUT1;           //HMS Delta
      Double_t CUT2;          // HMS xptar
      Double_t CUT3;         //  HMS yptar
      // Select the cuts
      //HMS
      CUT1 = hsdelta >=-8.0 && hsdelta <=8.0;
      CUT2 = hsxptar >=-0.08 && hsxpfp <=0.08;
      CUT3 = hsyptar >=-0.045 && hsypfp <=0.045;
 
      //........................................
      
      //Fill SIMC events

      if(CUT1 && CUT2 && CUT3)
	{
	  H_hsxfp_SIMC->Fill(hsxfp);
	  H_hsyfp_SIMC->Fill(hsyfp);
	  H_hsxpfp_SIMC->Fill(hsxpfp);
	  H_hsypfp_SIMC->Fill(hsypfp);
	  H_hsdelta_SIMC->Fill(hsdelta);	
	  H_hsxptar_SIMC->Fill(hsxptar);	
	  H_hsyptar_SIMC->Fill(hsyptar);	
	  H_Q2_SIMC->Fill(Q2_simc);
	  H_W_SIMC->Fill(W_simc);
	  H_epsilon_SIMC->Fill(epsilon_simc);
	}
    }

  // Fill data events 

  for(Long64_t i = 0; i < nEntries_TBRANCH; i++)
    {
      TBRANCH->GetEntry(i);   
      
      H_hsxfp_DATA->Fill(H_dc_x_fp);
      H_hsyfp_DATA->Fill(H_dc_y_fp);
      H_hsxpfp_DATA->Fill(H_dc_xp_fp);
      H_hsypfp_DATA->Fill(H_dc_yp_fp);
      H_hsxptar_DATA->Fill(H_gtr_xptar);	
      H_hsyptar_DATA->Fill(H_gtr_yptar);	
      H_hsdelta_DATA->Fill(H_gtr_dp);	
      H_Q2_DATA->Fill(Q2);
      H_epsilon_DATA->Fill(epsilon);
      H_W_DATA->Fill(W);
	  
    }
  
  //...................................................................

  // PLOT HIST..


  TCanvas *hxfp = new TCanvas("hxfp", "HMS xfp");
  H_hsxfp_DATA->SetLineColor(kRed);

  H_hsxfp_SIMC->Draw("");
  H_hsxfp_DATA->Draw("same");

  hxfp->Print(outputpdf+'(');

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

  TCanvas *hDelta = new TCanvas("hDelta", "HMS Delta");
  H_hsdelta_DATA->SetLineColor(kRed);

  H_hsdelta_SIMC->Draw("");
  H_hsdelta_DATA->Draw("same");

  hDelta->Print(outputpdf);

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
