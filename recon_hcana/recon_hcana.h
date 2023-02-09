#ifndef RECON_HCANA_H
#define RECON_HCANA_H

#include<iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include "TVector3.h"

class recon_hcana
{
  
 public:

  //Consructor / Destructor
  recon_hcana();
  ~recon_hcana();
  
  void grabHistData(TString InSIMCHistname);

  //Auxiliary Function Prototypes (obtained from hcana) to calculate Pmx, Pmy, Pmz in the Lab/q-frame correctly
  void GeoToSph( Float_t  th_geo, Float_t  ph_geo, Float_t& th_sph, Float_t& ph_sph);
  void SetCentralAngles(Float_t th_cent, Float_t ph_cent);
  void TransportToLab( Float_t p, Float_t xptar, Float_t yptar, TVector3& pvect ); 
  
  //Utilities Functions for String Parsing
  string getString(char x);
  vector <string> FindString(TString keyword, TString fname);
  vector <string> split(string str, char del=':');
  vector <float> num_split(string str);
  
  void buildFileName(){

    if (reaction == "heep"){
      
      TString kinematics = "10p6";
      InSIMCFilename = "../OUTPUTS/Heep_Coin_" + kinematics;
      
    }else{

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

  }

  void ReadTree();
  void EventLoop();
  void WriteHist();

  TFile *f;
  TTree *tree;
  TTree *newTree;

  Int_t nentries;

  Float_t hsdelta;
  Float_t hsyptar;
  Float_t hsxptar;
  Float_t hsytar;
  Float_t hsxfp;
  Float_t hsxpfp;
  Float_t hsyfp;
  Float_t hsypfp;
  Float_t hsdeltai;
  Float_t hsyptari;
  Float_t hsxptari;
  Float_t hsytari;
  Float_t ssdelta;
  Float_t ssyptar;
  Float_t ssxptar;
  Float_t ssytar;
  Float_t ssxfp;
  Float_t ssxpfp;
  Float_t ssyfp;
  Float_t ssypfp;
  Float_t ssdeltai;
  Float_t ssyptari;
  Float_t ssxptari;
  Float_t ssytari;
  Float_t q;
  Float_t nu;
  Float_t Q2;
  Float_t W;
  Float_t epsilon;
  Float_t Em;
  Float_t Pm;
  Float_t thetapq;
  Float_t phipq;
  Float_t corrsing;
  Float_t Pmx;
  Float_t Pmy;
  Float_t Pmz;
  Float_t PmPar;
  Float_t PmPer;
  Float_t PmOop;
  Float_t fry;
  Float_t radphot;
  Float_t sigcc;
  Float_t Weight;
  
  TString InSIMCFilename;
  TString InSIMCHistname;
  TString InSIMCRootname;

  Int_t simc_nevents;
  Float_t simc_normfactor;

  // Progress bar
  float progress=0.0;

  TString reaction = "heep";

  //Primary Kinematics (electron kinematics) (USED BY DATA AND SIMC)
  Float_t theta_e;              //Central electron arm angle relative to +z (hall coord. system)
  Float_t W2;                    //Invariant mass squared
  Float_t X;                    //B-jorken X  scaling variable
  Float_t th_q;                 //angle between q and +z (hall coord. system)

  //Secondary Kinematics (USED BY DATA AND SIMC)
  Float_t Ein;                  //single beam energy value (SIMC Uses this energy. If not corr. for energy loss, it should be same as in input file)
  Float_t Ep;                     //proton energy
  Float_t Em_nuc;                //Nuclear definition of Missing Energy (Used for D(e,e'p): B.E. of deuteron)
  Float_t Pmx_lab;               //X-Component of Missing Momentum (in Lab(or Hall) frame. +X: beam left, +Y: up, +Z: downstream beam) 
  Float_t Pmy_lab;
  Float_t Pmz_lab;
  Float_t Pmx_q;                 //X-Component of Missing Momentum (in frame where +z_lab is rotated to +z_q. Pmz_q is along +z(parallel to q))
  Float_t Pmy_q;
  Float_t Pmz_q;
  Float_t Kp;                    //Kinetic Energy of detected particle (proton)
  Float_t Kn;                    //Kinetic Energy of recoil system (neutron)
  Float_t M_recoil;              //Missing Mass (neutron Mass)
  Float_t MM2;                   //Missing Mass Squared
  Float_t E_recoil;              //Recoil Energy of the system (neutron total energy)
  Float_t En;                    //Same as above
  Float_t th_pq;                  //Polar angle of detected particle with q   ----> th_pq
  Float_t th_nq;                  //Polar angle of recoil system with q (rad)  ---> th_nq (neutreon-q angle. IMPORTANT in D(e,e'p))
  Float_t ph_pq;                  //Azimuth angle of detected particle with q    ----> phi_pq angle between proton and q-vector
  Float_t ph_nq;                  //Azimuth of recoil system with scattering plane (rad) ----> phi_nq angle between neutron and q-vector
  Float_t xangle;                //Angle of detected particle with scattered electron (Used to determine hadron angle)
  Float_t theta_p;               //to be calculated separately (in data)

  //Electron Arm Focal Plane / Reconstructed Quantities (USED BY DATA AND SIMC)
  Float_t e_xfp;
  Float_t e_xpfp;
  Float_t e_yfp;
  Float_t e_ypfp;
  
  Float_t e_ytar;
  Float_t e_yptar;
  Float_t e_xptar;
  Float_t e_delta;
  Float_t kf;                        //final electron momentum
  Float_t ki;                        //initial electron momentum

  //Hadron Arm Focal Plane / Reconstructed Quantities (USED BY DATA AND SIMC)
  Float_t h_xfp;
  Float_t h_xpfp;
  Float_t h_yfp;
  Float_t h_ypfp;
  
  Float_t h_ytar;
  Float_t h_yptar;
  Float_t h_xptar;
  Float_t h_delta;
  Float_t Pf;                 //final proton momentum
  
  //Target Quantities (tarx, tary, tarz) in Hall Coord. System (USED BY DATA AND SIMC)
  Float_t tar_x; //For SIMC ONLY (It is the same for HMS/SHMS)

  Float_t  htar_x;
  Float_t  htar_y;
  Float_t  htar_z;
  
  Float_t  etar_x;
  Float_t  etar_y;
  Float_t  etar_z;

  Float_t ztar_diff;

  //X,Y Projection to Dipole Exit in HMS/SHMS
  Float_t xdip_hms, ydip_hms;
  Float_t xdip_shms, ydip_shms;  

  //Light-Cone Momentum Variables
  Float_t PmPerp;    //transverse component of recoil momentum relative to q-vector
  Float_t alpha_n;   //light-cone momentum fraction of the recoil neutron
  Float_t alpha;     //momentum fraction of struck nucleon (normalized such that: alpha + alpha_n = 2)

  //----------Variables Used in Auxiliary Functions--------------------------------------

  TRotation       fToLabRot;              //Rotation matrix from TRANSPORT to lab
  Float_t        fThetaGeo;              //In-plane geographic central angle (rad)
  Float_t        fPhiGeo;                //Out-of-plane geographic central angle (rad)
  Float_t        fThetaSph, fPhiSph;     //Central angles in spherical coords. (rad)
  Float_t        fSinThGeo, fCosThGeo;   //Sine and cosine of central angles
  Float_t        fSinPhGeo, fCosPhGeo;   // in geographical coordinates
  Float_t        fSinThSph, fCosThSph;   //Sine and cosine of central angles in 
  Float_t        fSinPhSph, fCosPhSph;   // spherical coordinates  

  //Declare Neccessary Variables to Determine the 4-Momentum of Recoil System
  TLorentzVector fP0;           // Beam 4-momentum
  TLorentzVector fP1;           // Scattered electron 4-momentum
  TLorentzVector fA;            // Target 4-momentum
  TLorentzVector fA1;           // Final system 4-momentum
  TLorentzVector fQ;            // Momentum transfer 4-vector
  TLorentzVector fX;            // Detected secondary particle 4-momentum (GeV)
  TLorentzVector fB;            // Recoil system 4-momentum (GeV)

  TVector3 Pf_vec;
  TVector3 kf_vec;

  //Declare necessary variables for rotaion from +z to +q
  TVector3 qvec;
  TVector3 kfvec;
  TRotation rot_to_q;
  TVector3 bq;   //recoil system in lab frame (Pmx, Pmy, Pmz)
  TVector3 xq;   //detected system in lab frame
  TVector3 p_miss_q;   //recoil system in q-frame

  //Leaf Variables
  Float_t fTheta_xq;
  Float_t fPhi_xq;
  Float_t fTheta_bq;
  Float_t fPhi_bq;  

  //Set Constants
  Float_t pi; 
  Float_t dtr;
  Float_t MP = 0.938272;     //proton mass
  Float_t MD = 1.87561;      //deuteron mass
  Float_t MN = 0.939566;     //neutron mass
  Float_t me = 0.00051099;   //electron mass
  Float_t MAL = 25.131710;   //aluminum mass
  Float_t tgt_mass;

  //Set Varibales to be read from REPORT_FILE
  Float_t e_th=0.;    //electron arm central angle
  Float_t e_ph=0.;    
  Float_t h_th=0.;    //hadron arm central angle
  Float_t h_ph=0.;

  Float_t xBPM;  //in cm
  Float_t yBPM;  //in cm
  
  Float_t e_xMisPoint;
  Float_t e_yMisPoint;
  Float_t h_xMisPoint;
  Float_t h_yMisPoint;

  //Central Spec. Momenta
  Float_t e_Pcen;
  Float_t h_Pcen;
  
};

#endif  //RECON_HCANA_H
