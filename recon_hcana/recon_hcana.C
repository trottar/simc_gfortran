/*
 * Description:
 * ================================================================
 * Time-stamp: "2023-02-08 17:16:40 trottar"
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

  buildFileName();

  InSIMCHistname = InSIMCFilename + ".hist";
  InSIMCRootname = InSIMCFilename + ".root";
  cout << "InSIMCFilename: " << InSIMCFilename << endl;
  cout << "InSIMCHistname: " << InSIMCHistname << endl;
  cout << "InSIMCRootname: " << InSIMCRootname << endl;


  simc_nevents = stod(split(FindString("Ngen",InSIMCHistname)[0], '=')[1]);
  simc_normfactor = stod(split(FindString("normfac",InSIMCHistname)[0], '=')[1]);
  
  cout << "Ngen: " << simc_nevents << endl;
  cout << "normfac: " << simc_normfactor << endl;
  
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

//_______________________________________________________________________________________
vector <string> recon_hcana::FindString(string keyword, string fname)
{

  //Method: Finds string keyword in a given txt file. 
  //Returns the lines (stored in a vector) in which the keyword was found. Lines are counted from 0. 
  
  ifstream ifile(fname);

  vector <string> line_found; //vector to store in which lines was the keyword found
  
  int line_cnt = 0;
  string line;                  //line string to read
  
  int found = -1; //position of found keyword

  while(getline(ifile, line))
    {
      //Check 1st character of found string
      TString cmt = line[0];
      
      found = line.find(keyword);
      
      if(found<0||found>1000){found=-1;} //not found
      if(cmt==";" || cmt=="#" || cmt=="!") {found=-1;}  //Found commented line. So Skip

      if(found!=-1){
	
	line_found.push_back(line);
	

      } //end if statement
    
      line_cnt++;
    } //end readlines

  return line_found;

}

recon_hcana::~recon_hcana()
{
  //Destructor

  //delete File; File = NULL;
}  
