/*
 * Description:
 * ================================================================
 * Time-stamp: "2023-02-08 17:31:25 trottar"
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


  simc_nevents = split(FindString("Ngen",InSIMCHistname)[0], '=')[1];
  simc_normfactor = split(FindString("normfac",InSIMCHistname)[0], '=')[1];
  
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
vector <string> recon_hcana::FindString(TString keyword, TString fname)
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
      //if(cmt==";" || cmt=="#" || cmt=="!") {found=-1;}  //Found commented line. So Skip

      if(found!=-1){
	
	line_found.push_back(line);
	

      } //end if statement
    
      line_cnt++;
    } //end readlines

  return line_found;

}

vector <string> recon_hcana::split(string str, char del=':')
{

  //method to split a string into a vetor of strings separated by a delimiter del
  //Returns a vector of strings, whose elements are separated by the delimiter del.

  string temp1, temp2;

  vector <string> parse_word;
  int del_pos;  //delimiter position
    
    for (int i=0; i < str.size(); i++){

      //Get position of delimiter
      if(str[i]==del){
	del_pos = i;
      }

    }

    for (int i=0; i < str.size(); i++){

      //append char to a string for char left of the delimiter
      if(i<del_pos){
	temp1.append(getString(str[i]));
      }      

      //append char to a string for char right of the delimiter
      else if(i>del_pos){
	temp2.append(getString(str[i]));
      }

    }
    parse_word.push_back(temp1);
    parse_word.push_back(temp2);
    
    return parse_word;
}

string recon_hcana::getString(char x)
{
  //method to convert a character to a string
  string s(1,x);
  return s;
}

recon_hcana::~recon_hcana()
{
  //Destructor

  //delete File; File = NULL;
}  
