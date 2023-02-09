/*
 * Description:
 * ================================================================
 * Time-stamp: "2023-02-09 18:19:46 trottar"
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
  Ein = stod(split(FindString("Ebeam",InSIMCHistname)[0], '=')[1]);
  kf = num_split(split(FindString("momentum",InSIMCHistname)[0], '=')[1])[0];
  e_th = num_split(split(FindString("angle",InSIMCHistname)[0], '=')[1])[0];
  Pf = num_split(split(FindString("momentum",InSIMCHistname)[0], '=')[1])[1];
  h_th = num_split(split(FindString("angle",InSIMCHistname)[0], '=')[1])[1];

  cout << "Ngen: " << simc_nevents << endl;
  cout << "normfac: " << simc_normfactor << endl;
  cout << "Ein: " << Ein << endl;
  cout << "kf: " << kf << endl;
  cout << "e_th: " << e_th << endl;
  cout << "Pf: " << Pf << endl;
  cout << "h_th: " << h_th << endl;  
  
  ReadTree();
  EventLoop();
  WriteHist();
  
}

void recon_hcana::ReadTree(){
  
  cout << "Calling ReadTree() . . . " << endl;

  f = new TFile(InSIMCRootname,"UPDATE");
  tree = (TTree*)f->Get("h10");
  
  //tree->GetListOfBranches()->Print();

  nentries = tree->GetEntries();

  tree->SetBranchAddress("hsdelta", &hsdelta);
  tree->SetBranchAddress("hsyptar", &hsyptar);
  tree->SetBranchAddress("hsxptar", &hsxptar);
  tree->SetBranchAddress("hsytar", &hsytar);
  tree->SetBranchAddress("hsxfp", &hsxfp);
  tree->SetBranchAddress("hsxpfp", &hsxpfp);
  tree->SetBranchAddress("hsyfp", &hsyfp);
  tree->SetBranchAddress("hsypfp", &hsypfp);
  tree->SetBranchAddress("hsdeltai", &hsdeltai);
  tree->SetBranchAddress("hsyptari", &hsyptari);
  tree->SetBranchAddress("hsxptari", &hsxptari);
  tree->SetBranchAddress("hsytari", &hsytari);
  tree->SetBranchAddress("ssdelta", &ssdelta);
  tree->SetBranchAddress("ssyptar", &ssyptar);
  tree->SetBranchAddress("ssxptar", &ssxptar);
  tree->SetBranchAddress("ssytar", &ssytar);
  tree->SetBranchAddress("ssxfp", &ssxfp);
  tree->SetBranchAddress("ssxpfp", &ssxpfp);
  tree->SetBranchAddress("ssyfp", &ssyfp);
  tree->SetBranchAddress("ssypfp", &ssypfp);
  tree->SetBranchAddress("ssdeltai", &ssdeltai);
  tree->SetBranchAddress("ssyptari", &ssyptari);
  tree->SetBranchAddress("ssxptari", &ssxptari);
  tree->SetBranchAddress("ssytari", &ssytari);
  tree->SetBranchAddress("q", &q);
  tree->SetBranchAddress("nu", &nu);
  tree->SetBranchAddress("Q2", &Q2);
  tree->SetBranchAddress("W", &W);
  tree->SetBranchAddress("epsilon", &epsilon);
  tree->SetBranchAddress("Em", &Em);
  tree->SetBranchAddress("Pm", &Pm);
  tree->SetBranchAddress("thetapq", &thetapq);
  tree->SetBranchAddress("phipq", &phipq);
  tree->SetBranchAddress("corrsing", &corrsing);
  tree->SetBranchAddress("Pmx", &Pmx);
  tree->SetBranchAddress("Pmy", &Pmy);
  tree->SetBranchAddress("Pmz", &Pmz);
  tree->SetBranchAddress("PmPar", &PmPar);
  tree->SetBranchAddress("PmPer", &PmPer);
  tree->SetBranchAddress("PmOop", &PmOop);
  tree->SetBranchAddress("fry", &fry);
  tree->SetBranchAddress("radphot", &radphot);
  tree->SetBranchAddress("sigcc", &sigcc);
  tree->SetBranchAddress("Weight", &Weight);  
  
  newTree = tree->CloneTree(0);

  cout << "Ending ReadTree() . . . " << endl;

}

void recon_hcana::EventLoop(){

  cout << "Calling EventLoop() . . . " << endl;
  
  //Convert MeV to GeV
  Ein = Ein / 1000.;     //incident beam energy
  kf = kf / 1000.;       //final electron momentum
  Pf = Pf / 1000.;       //final proton momentum

  for (Int_t i=0;i<nentries;i++) {
    
    // Progress bar
    if(i%1000==0) {	    
      int barWidth = 25;
      progress = ((float)i/(float)nentries);	    
      // cout<<i<<"/"<<nentries<<endl;
      // cout << progress << endl;
      cout << "[";
      float pos = barWidth * progress;
      for (float i = 0.; i < barWidth; ++i) {
	if (i < pos) cout << "=";
	else if (i == pos) cout << ">";
	else cout << " ";
      }
      cout << "] " << int(progress * 100.0) << " %\r";
      cout.flush();
    }	 

    tree->GetEntry(i);

    //--------Calculated Kinematic Varibales----------------
        
    ki = sqrt(Ein*Ein - me*me);        //initial electron momentum
    
    //redefine
    Ep = sqrt(MP*MP + Pf*Pf);
    En = sqrt(MN*MN + Pm*Pm);

    // cout << "Em: " << Em << endl;
    // cout << "Pm: " << Pm << endl;
    // cout << "Ep: " << Ep << endl;
    // cout << "En: " << En << endl;
    
    Kp = Ep - MP;                                                                    
    Kn = En - MN;

    // cout << "Kp: " << Kp << endl;
    // cout << "Kn: " << Kn << endl;
    
    Em = nu - Kp - Kn;

    // cout << "Em: " << Em << endl;
    
    M_recoil = sqrt( pow(nu+MD-Ep,2) - Pm*Pm );  //recoil mass (neutron missing mass)
    MM2 = M_recoil * M_recoil;

    //-----If H(e,e'p)
    if(reaction=="heep"){
      M_recoil = sqrt(Em*Em - Pm*Pm);
      MM2 = Em*Em - Pm*Pm;
    }
    //----------

    // cout << "MM2: " << MM2 << endl;
    
    W2 = W*W;

    /*
    //Use hcana formula to re-define HMS/SHMS Ztarget
    htar_z = ((h_ytar + h_yMisPoint)-xBPM*(cos(h_th*dtr)-h_yptar*sin(h_th*dtr)))/(-sin(h_th*dtr)-h_yptar*cos(h_th*dtr));
    etar_z = ((e_ytar - e_yMisPoint)-xBPM*(cos(e_th*dtr)-e_yptar*sin(e_th*dtr)))/(-sin(e_th*dtr)-e_yptar*cos(e_th*dtr));
    
    ztar_diff = htar_z - etar_z;
	  
    X = Q2 / (2.*MP*nu);                           
    th_q = acos( (ki - kf*cos(theta_e))/q );       

    //Define Dipole Exit
    xdip_hms = h_xfp - 147.48*h_xpfp;
    ydip_hms = h_yfp - 147.48*h_ypfp;
	  
    xdip_shms = e_xfp - 307.*e_xpfp;
    ydip_shms = e_yfp - 307.*e_ypfp;
    */
    
    //---------------------------------------------------

    //---------Calculate Pmx, Pmy, Pmz in the Lab, and in the q-system----------------

    //Calculate electron final momentum 3-vector
    SetCentralAngles(e_th, e_ph); // ERROR HERE
    TransportToLab(kf, hsxptar, hsyptar, kf_vec); // ERROR HERE

    // cout << "kf_vec.X(): " << kf_vec.X() << endl;
    // cout << "kf_vec.Y(): " << kf_vec.Y() << endl;
    // cout << "kf_vec.Z(): " << kf_vec.Z() << endl;
    
    //Calculate 4-Vectors
    fP0.SetXYZM(0.0, 0.0, ki, me);  //set initial e- 4-momentum
    fP1.SetXYZM(kf_vec.X(), kf_vec.Y(), kf_vec.Z(), me);  //set final e- 4-momentum
    fA.SetXYZM(0.0, 0.0, 0.0, tgt_mass );  //Set initial target at rest
    fQ = fP0 - fP1;
    fA1 = fA + fQ;   //final target (sum of final hadron four momenta)

    //Get Detected Particle 4-momentum
    SetCentralAngles(h_th, h_ph);
    TransportToLab(Pf, ssxptar, ssyptar, Pf_vec);
    
    fX.SetVectM(Pf_vec, MP);       //SET FOUR VECTOR OF detected particle
    fB = fA1 - fX;                 //4-MOMENTUM OF UNDETECTED PARTICLE 

    Pmx_lab = fB.X();
    Pmy_lab = fB.Y(); 
    Pmz_lab = fB.Z(); 
  
    // cout << "Pmx_lab: " << Pmx_lab << endl;
    // cout << "Pmy_lab: " << Pmy_lab << endl;
    // cout << "Pmz_lab: " << Pmz_lab << endl;
    
    //Pm = sqrt(Pmx_lab*Pmx_lab + Pmy_lab*Pmy_lab + Pmz_lab*Pmz_lab);

    //--------Rotate the recoil system from +z to +q-------
    qvec = fQ.Vect();
    kfvec = fP1.Vect();

    rot_to_q.SetZAxis( qvec, kfvec).Invert();

    xq = fX.Vect();
    bq = fB.Vect();

    xq *= rot_to_q;
    bq *= rot_to_q;

    //Calculate Angles of q relative to x(detected proton) and b(recoil neutron)
    th_pq = xq.Theta();   //"theta_pq"                                       
    ph_pq   = xq.Phi();     //"out-of-plane angle", "phi_pq"                                                                    
    th_nq = bq.Theta();   // theta_nq                                                                                                     
    ph_nq   = bq.Phi();     //phi_nq

    p_miss_q = -bq;

    //Missing Momentum Components in the q-frame
    Pmz_q = p_miss_q.Z();   //parallel component to +z
    Pmx_q = p_miss_q.X();   //in-plane perpendicular component to +z
    Pmy_q = p_miss_q.Y();   //out-of-plane component (Oop)

    // Redefine variables
    Pmx = p_miss_q.X();   //in-plane perpendicular component to +z
    Pmy = p_miss_q.Y();   //out-of-plane component (Oop)
    Pmz = p_miss_q.Z();   //parallel component to +z

    Pm = p_miss_q.Mag();

    // cout << "Pmx: " << Pmx << endl;
    // cout << "Pmy: " << Pmy << endl;
    // cout << "Pmz: " << Pmz << endl;
    // cout << "Pm: " << Pm << endl;
    
    newTree->Fill();  
  }
  
  cout << "Ending EventLoop() . . . " << endl;
}

void recon_hcana::WriteHist(){

  cout << "Calling WriteHist() . . . " << endl;
  
  //tree->Write("",TObject::kOverwrite);
  f->Delete("h10;*");
  newTree->Write();
  f->Close();

  cout << "Ending WriteHist() . . . " << endl;
}
//---------------AUXILIARY FUNCTIONS TO CALCULATE Pmx, Pmy, Pmz in SIMC (same as HCANA) -------------------

//_____________________________________________________
void recon_hcana::GeoToSph( Double_t  th_geo, Double_t  ph_geo, Double_t& th_sph, Double_t& ph_sph){
  
  // Convert geographical to spherical angles. Units are rad.
  
  static const Double_t twopi = 2.0*TMath::Pi();
  Double_t ct = cos(th_geo), cp = cos(ph_geo);
  Double_t tmp = ct*cp;
  th_sph = acos( tmp );
  tmp = sqrt(1.0 - tmp*tmp);
  ph_sph = (fabs(tmp) < 1e-6 ) ? 0.0 : acos( sqrt(1.0-ct*ct)*cp/tmp );
  if( th_geo/twopi-floor(th_geo/twopi) > 0.5 ) ph_sph = TMath::Pi() - ph_sph;
  if( ph_geo/twopi-floor(ph_geo/twopi) > 0.5 ) ph_sph = -ph_sph;
  
  // cout << "th_geo: " << th_geo << endl;
  // cout << "ph_geo: " << ph_geo << endl;
  // cout << "th_sph: " << th_sph << endl;
  // cout << "ph_sph: " << ph_sph << endl;
}

//_______________________________________________________________
void recon_hcana::SetCentralAngles(Double_t th_cent=0, Double_t ph_cent=0){
  
  fThetaGeo = TMath::DegToRad()*th_cent; fPhiGeo = TMath::DegToRad()*ph_cent;
  
  // cout << "th_cent: " << th_cent << endl;
  // cout << "ph_cent: " << ph_cent << endl;
    
  GeoToSph( fThetaGeo, fPhiGeo, fThetaSph, fPhiSph );
  fSinThGeo = TMath::Sin( fThetaGeo ); fCosThGeo = TMath::Cos( fThetaGeo );
  fSinPhGeo = TMath::Sin( fPhiGeo );   fCosPhGeo = TMath::Cos( fPhiGeo );
  Double_t st, ct, sp, cp;
  st = fSinThSph = TMath::Sin( fThetaSph ); ct = fCosThSph = TMath::Cos( fThetaSph );
  sp = fSinPhSph = TMath::Sin( fPhiSph );   cp = fCosPhSph = TMath::Cos( fPhiSph );
  
  Double_t norm = TMath::Sqrt(ct*ct + st*st*cp*cp);
  
  // cout << "norm: " << norm << endl;
  
  TVector3 nx( st*st*sp*cp/norm, -norm, st*ct*sp/norm );
  TVector3 ny( ct/norm,          0.0,   -st*cp/norm   );
  TVector3 nz( st*cp,            st*sp, ct            );

  // cout << "nx.X(): " << nx.X() << endl;
  // cout << "nx.Y(): " << nx.Y() << endl;
  // cout << "nx.Z(): " << nx.Z() << endl;
  
  fToLabRot.SetToIdentity().RotateAxes( nx, ny, nz );
}

//____________________________________________________________________________________
void recon_hcana::TransportToLab( Double_t p, Double_t xptar, Double_t yptar, TVector3& pvect) {
  
  TVector3 v( xptar, yptar, 1.0 );
  v *= p/TMath::Sqrt( 1.0+xptar*xptar+yptar*yptar );

  // cout << "v.X(): " << v.X() << endl;
  // cout << "v.Y(): " << v.Y() << endl;
  // cout << "v.Z(): " << v.Z() << endl;
  
  pvect = fToLabRot * v;

  // cout << "pvect.X(): " << pvect.X() << endl;
  // cout << "pvect.Y(): " << pvect.Y() << endl;
  // cout << "pvect.Z(): " << pvect.Z() << endl;  
}

//------------------------------------------------------------------------------------------


//----------------------------------UTILITIES FUNCTIONS--------------------------------------

vector <string> recon_hcana::FindString(TString keyword, TString fname){

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

vector <string> recon_hcana::split(string str, char del=':'){

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

vector <float> recon_hcana::num_split(string str){

  istringstream stream(str);
  vector<float> values;
  float value;
  while (stream >> value) {
    values.push_back(value);
    if (stream.fail()) break;
  }

  return values;
}

string recon_hcana::getString(char x){
  //method to convert a character to a string
  string s(1,x);
  return s;
}

recon_hcana::~recon_hcana(){
  //Destructor

  //delete File; File = NULL;
}  
