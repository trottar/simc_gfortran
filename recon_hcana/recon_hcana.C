/*
 * Description:
 * ================================================================
 * Time-stamp: "2023-02-08 16:29:14 trottar"
 * ================================================================
 *
 * Author:  Richard L. Trotta III <trotta@cua.edu>, Carlos Yero <cyero002@fiu.edu, cyero@jlab.org>
 *
 * Copyright (c) trottar
 */

#include<iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "recon_hcana.h"

using namespace std;

recon_hcana::recon_hcana() {
  string kinematics = "Q5p5W3p02_lowe";
  string phi_setting = "Right";
  vector<string> kinematics_split;
  stringstream kinematics_stream(kinematics);
  string kinematics_part;

  while (getline(kinematics_stream, kinematics_part, '_')) {
    kinematics_split.push_back(kinematics_part);
  }

  transform(phi_setting.begin(), phi_setting.end(), phi_setting.begin(), [](unsigned char c) { return std::tolower(c); });
  
  string InSIMCFilename = "../OUTPUTS/Prod_Coin_" + kinematics_split[0] + phi_setting + "_" + kinematics_split[1];

  string InSIMCHistname = InSIMCFilename + ".hist";
  string InSIMCRootname = InSIMCFilename + ".root";
  cout << "InSIMCFilename: " << InSIMCFilename << endl;
  cout << "InSIMCHistname: " << InSIMCHistname << endl;
  cout << "InSIMCRootname: " << InSIMCRootname << endl;


  grabHistData(InSIMCHistname);
  
  /*
  TFile *f = new TFile(InSIMCRootname,"UPDATE");
  TTree *tree = (TTree*)f->Get("h10");
  Int_t x;
  
  tree->SetBranchAddress("x",&x);
  
  for (Int_t i=0;i<tree->GetEntries();i++) {
    tree->GetEntry(i);
    x=x*2;
    tree->Fill();
  }

  tree->Write("",TObject::kOverwrite);
  f->Close();
  */
}

void recon_hcana::grabHistData(string InSIMCHistname) {

  ifstream f_simc(InSIMCHistname);
  int simc_nevents = 0;
  float simc_normfactor = 0.0;

  if (f_simc.is_open()) {
    string line;
    while (getline(f_simc, line)) {
      if (line.find("Ngen") != string::npos) {
        stringstream line_stream(line);
        string keyword;
        int value;
        line_stream >> keyword >> value;
        simc_nevents = value;
      }
      if (line.find("normfac") != string::npos) {
        stringstream line_stream(line);
        string keyword;
        float value;
        line_stream >> keyword >> value;
        simc_normfactor = value;
      }
    }
    f_simc.close();
  } else {
    cerr << "Error: unable to open file " << InSIMCHistname << endl;
  }

  cout << "Ngen: " << simc_nevents << endl;
  cout << "normfac: " << simc_normfactor << endl;
  
}
