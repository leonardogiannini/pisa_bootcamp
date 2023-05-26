#include <string>
#include <vector>
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <fstream>
#include <iostream>

#include "TBranch.h"
#include "TCanvas.h"
#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TH3D.h"
#include "TMath.h"
#include "TH2D.h"
#include "TH1F.h"
#include "TH3F.h"
#include <TLorentzVector.h>

//compile root g++ plotter_vbfzll.C -g -o plot `root-config --cflags --glibs`//
using namespace std;

void findDuplTracksEtc(char* filename= (char*)"file", char* folder= (char*)"boh", char* cut= (char*)"not")
{

  std::cout << "in" <<std::endl;
  TString thefile = TString(filename);
  TString path = TString(folder);
  TString postfix = TString(cut);//"post";
  
  TChain* ch = new TChain("t");
  ch->AddFile(path+thefile);
  

  float invpt,theta,dq,dphi,chi2;
  int lyr_id,seed_algo,seed_mcid,hit_mcid,trk_label;
  int bkwd; 
  float dq_cut, dphi_cut;
 
  ch->SetBranchAddress("trk_label", &trk_label);
  ch->SetBranchAddress("hit_mcid", &hit_mcid);
  ch->SetBranchAddress("seed_mcid", &seed_mcid);
  ch->SetBranchAddress("seed_algo", &seed_algo);
  ch->SetBranchAddress("lyr_id", &lyr_id);

  ch->SetBranchAddress("trk_invpt",  &invpt);
  ch->SetBranchAddress("trk_theta", &theta);
  ch->SetBranchAddress("dq_trkhit", &dq);
  ch->SetBranchAddress("dphi_trkhit",&dphi);
  ch->SetBranchAddress("h_chi2",&chi2);
  
  ch->SetBranchAddress("dphi_cut",&dphi_cut);
  ch->SetBranchAddress("dq_cut",&dq_cut);  

  ch->SetBranchAddress("bkwd",&bkwd);

  std::cout << "branches" << std::endl;

  TFile* out  = TFile::Open(postfix+""+".root","RECREATE");
  out->cd();


  vector<float> layers = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0};
  vector<float> algos = {4.0,22.0,23.0,5.0,24.0,7.0,6.0,8.0,9.0,10.0,11.0};
 
  vector<TString> algoss = {"4","22","23","5","24","7","6","8","9","10","11"};
  vector<TString> layerss = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71"};
 
  map<TString, TH3F*> histos3d;
  
  float bsize=0.0;
  Double_t binschi2[4001];
  bsize=200/4000.;
  for (unsigned int i=0; i<4001;i++){std::cout << binschi2[i] ; binschi2[i]=i*bsize; std::cout <<"  after " << i <<" bsize "<< binschi2[i] << std::endl;}
  Double_t binsdq[4001];
  bsize=100/4000.;
  for (unsigned int i=0; i<4001;i++){binsdq[i]=i*bsize; }
  Double_t binsdphi[4001];
  bsize=1.64/4000.;
  for (unsigned int i=0; i<4001;i++){binsdphi[i]=i*bsize; }

  Double_t binstheta[17]={0.     , 0.09375, 0.1875 , 0.28125, 0.375  , 0.46875, 0.5625 ,
       0.65625, 0.75   , 0.84375, 0.9375 , 1.03125, 1.125  , 1.21875,
       1.3125 , 1.40625, 1.5 
  };

  Double_t bins1pT[26]={0. ,  0.4,  0.8,  1.2,  1.6,  2. ,  2.4,  2.8,  3.2,  3.6,  4. ,
        4.4,  4.8,  5.2,  5.6,  6. ,  6.4,  6.8,  7.2,  7.6,  8. ,  8.4,
        8.8,  9.2,  9.6, 10.
  };
   
  Double_t Sbins1pT[25]={0.018, 0.024, 0.031, 0.04 , 0.052, 0.068, 0.088, 0.115, 0.15 ,
       0.194, 0.253, 0.329, 0.427, 0.556, 0.723, 0.939, 1.221, 1.588,
       2.065, 2.685, 3.49 , 4.538, 5.9  , 7.671, 9.974};
 
  for( int l =0 ; l < layers.size() ; ++l){
     std::cout << "layer " << layerss[l] << std::endl;
     for( int g =0 ; g < algos.size() ; ++g){
      
       histos3d["3d-layerq_"+layerss[l]+"_"+algoss[g]]= new TH3F("dq-fwd-layer_"+layerss[l]+"_"+algoss[g], "dq-layer_"+layerss[l]+"_"+algoss[g], 25, bins1pT, 16, binstheta, 4000, binsdq);
       histos3d["3d-layerp_"+layerss[l]+"_"+algoss[g]]= new TH3F("dphi-fwd-layer_"+layerss[l]+"_"+algoss[g], "dphi-layer_"+layerss[l]+"_"+algoss[g], 25, bins1pT, 16, binstheta, 4000, binsdphi);   
       histos3d["3d-layerc_"+layerss[l]+"_"+algoss[g]]= new TH3F("chi2-fwd-layer_"+layerss[l]+"_"+algoss[g], "chi2-layer_"+layerss[l]+"_"+algoss[g], 25, bins1pT, 16, binstheta, 4000, binschi2);
       histos3d["3dB-layerq_"+layerss[l]+"_"+algoss[g]]= new TH3F("dq-bkwd-layer_"+layerss[l]+"_"+algoss[g], "dq-layer_"+layerss[l]+"_"+algoss[g], 25, bins1pT, 16, binstheta, 4000, binsdq);
       histos3d["3dB-layerp_"+layerss[l]+"_"+algoss[g]]= new TH3F("dphi-bkwd-layer_"+layerss[l]+"_"+algoss[g], "dphi-layer_"+layerss[l]+"_"+algoss[g], 25, bins1pT, 16, binstheta, 4000, binsdphi); 
       histos3d["3dB-layerc_"+layerss[l]+"_"+algoss[g]]= new TH3F("chi2-bkwd-layer_"+layerss[l]+"_"+algoss[g], "chi2-layer_"+layerss[l]+"_"+algoss[g], 25, bins1pT, 16, binstheta, 4000, binschi2);
           
       //histos3d["3d-layerq_"+layerss[l]+"_"+algoss[g]]= new TH3F("dq-layer_"+layerss[l]+"_"+algoss[g], "dq-layer_"+layerss[l]+"_"+algoss[g], 50, 0, 10, 50, 0, 1.5, 1000, 0, 100);
       //histos3d["3d-layerp_"+layerss[l]+"_"+algoss[g]]= new TH3F("dphi-layer_"+layerss[l]+"_"+algoss[g], "dphi-layer_"+layerss[l]+"_"+algoss[g], 50, 0, 10, 50, 0, 1.5, 1000, 0, 1.64);
       //histos3d["3d-layerc_"+layerss[l]+"_"+algoss[g]]= new TH3F("chi2-layer_"+layerss[l]+"_"+algoss[g], "chi2-layer_"+layerss[l]+"_"+algoss[g], 50, 0, 10, 50, 0, 1.5, 1000, 0, 200);
      
   }
  }
 
  int nentries=ch->GetEntries();
  std::cout << "nentries " << nentries << std::endl;
  for (Long64_t ie = 0; ie < nentries; ++ie){

    if(ie%5000==0) cout << ie << "/" << nentries << " [ " << float(ie)/nentries*100 << "% ]" << endl;

    ch->GetEntry(ie);

    for( int l =0 ; l < layers.size() ; ++l){ 
      for( int g =0 ; g < algos.size() ; ++g){
       float cond=(invpt-5)*(invpt-5)/16+theta*theta/0.09; 
       if( cond>1 && lyr_id==layers[l] && seed_algo==algos[g] && seed_mcid==hit_mcid && hit_mcid==trk_label) {
        //if( dq<(dq_cut/5.) && dphi<(dphi_cut/5.) && chi2<200 && lyr_id==layers[l] && seed_algo==algos[g] && seed_mcid==hit_mcid && hit_mcid==trk_label) {
        //histo2_fromtreeRebin.C
        //about the windows analysis, I was thinking to suggest to use the closest hit if there are multiple hits in the same layer. Your example file points that these tails are predominantly from multiple hits.
          if(!bkwd) {
                       histos3d["3d-layerq_"+layerss[l]+"_"+algoss[g]]->Fill(invpt,theta,dq);
                       histos3d["3d-layerp_"+layerss[l]+"_"+algoss[g]]->Fill(invpt,theta,dphi);
                       histos3d["3d-layerc_"+layerss[l]+"_"+algoss[g]]->Fill(invpt,theta,chi2);
                    }
          else {
                  histos3d["3dB-layerq_"+layerss[l]+"_"+algoss[g]]->Fill(invpt,theta,dq);
                  histos3d["3dB-layerp_"+layerss[l]+"_"+algoss[g]]->Fill(invpt,theta,dphi);
                  histos3d["3dB-layerc_"+layerss[l]+"_"+algoss[g]]->Fill(invpt,theta,chi2);
               }
      
       }
      
     }
    }
  } 
  
  out->cd();
  for( int l =0 ; l < layers.size() ; ++l){
     for( int g =0 ; g < algos.size() ; ++g){
       histos3d["3d-layerq_"+layerss[l]+"_"+algoss[g]]->Write();
       histos3d["3d-layerp_"+layerss[l]+"_"+algoss[g]]->Write();
       histos3d["3d-layerc_"+layerss[l]+"_"+algoss[g]]->Write();
       histos3d["3dB-layerq_"+layerss[l]+"_"+algoss[g]]->Write();
       histos3d["3dB-layerp_"+layerss[l]+"_"+algoss[g]]->Write();
       histos3d["3dB-layerc_"+layerss[l]+"_"+algoss[g]]->Write();
      
    }
  }

  out->Close();

}


int main(int argc, char *argv[]){

    const char* file1 = argv[1];
    const char* folder = argv[2];
    const char* cut =argv[3];

    std::cout<<argv[1]<<" "<<argv[2]<<" "<<argv[3]<<std::endl;

    std::cout << "launch" << std::endl;
    findDuplTracksEtc(argv[1], argv[2], argv[3]);

}

