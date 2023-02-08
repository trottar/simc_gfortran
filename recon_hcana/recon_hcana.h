#ifndef RECON_HCANA_H
#define RECON_HCANA_H

#include<iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

class recon_hcana
{
  
 public:

  //Consructor / Destructor
  recon_hcana();
  ~recon_hcana();

  void grabHistData(TString InSIMCHistname);
  void buildFileName(TString InSIMCFilename){

    string kinematics = "Q5p5W3p02_highe";
    string phi_setting = "Right";
    vector<string> kinematics_split;
    stringstream kinematics_stream(kinematics);
    string kinematics_part;

    while (getline(kinematics_stream, kinematics_part, '_')) {
      kinematics_split.push_back(kinematics_part);
    }

    transform(phi_setting.begin(), phi_setting.end(), phi_setting.begin(), [](unsigned char c) { return std::tolower(c); });

    InSIMCFilename = "../OUTPUTS/Prod_Coin_" + kinematics_split[0] + phi_setting + "_" + kinematics_split[1];

  }
  
  TString InSIMCFilename;
  TString InSIMCHistname;
  TString InSIMCRootname;
  
};

#endif  //RECON_HCANA_H
