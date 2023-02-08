#ifndef RECON_HCANA_H
#define RECON_HCANA_H

class recon_hcana
{
  
 public:

  //Consructor / Destructor
  recon_hcana();
  ~recon_hcana();

  void buildFileName(TString InSIMCFilename);
  void grabHistData(TString InSIMCHistname);

  TString InSIMCFilename;
  TString InSIMCHistname;
  TString InSIMCRootname;
  
};

#endif  //RECON_HCANA_H
