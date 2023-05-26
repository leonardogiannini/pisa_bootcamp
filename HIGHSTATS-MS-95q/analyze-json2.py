import sys
from collections import OrderedDict
jsonfile=sys.argv[1]
itercode=sys.argv[2]
iterlabel=sys.argv[3]
secondjson=sys.argv[4]
import numpy as np
import ROOT
a=ROOT.TCanvas()
ROOT.gStyle.SetOptStat(0);
a.Divide(2,1,0,0);
#histos3d["3d-layerq_"+str(int(layer))+"_"+str(algo)]=ROOT.TH3F("dq-layer_"+str(int(layer))+"_"+str(algo), "dq-layer_"+str(int(layer))+"_"+str(algo), 50, 0, 10, 50, 0, 1.5, 100, 0, 20)

#abc
#0.01937210155822637+-0.020368984055786524
#invpt slope = 0.009794547877051257+-0.014680193315627837
#theta slope = -0.0016382040045779156+-0.025522160290684864
#0b 1c 2a

#f=open("../RecoTracker-MkFit/mkfit-phase1-initialStep.json")
f=open(jsonfile)
import json
#r = json.load(open('file.json'), object_pairs_hook=OrderedDict)
data=json.loads(f.read(), object_pairs_hook=OrderedDict)

f2=open(secondjson)
#r = json.load(open('file.json'), object_pairs_hook=OrderedDict)
data2=json.loads(f2.read(), object_pairs_hook=OrderedDict)

def draw_dd_c012(c0,c1,c2, cn0, cn1, cn2, label="", mini=0, maxi=100):
  f1=ROOT.TF1("dynamic window","[0]+[1]*x",0,10)
  f2=ROOT.TF1("max","[0]+[1]*x",0,10)
  f3=ROOT.TF1("min","[0]+[1]*x",0,10)
  
  f4=ROOT.TF1("dynamic window","[0]+[1]*x",0,1.5)
  f5=ROOT.TF1("max","[0]+[1]*x",0,1.5)
  f6=ROOT.TF1("min","[0]+[1]*x",0,1.5)
  
  fakeHisto=ROOT.TH1F("w","window size vs theta; theta;", 100, 0,1.5)
  fakeHisto2=ROOT.TH1F("w","window size vs 1/pt; invpt;", 100, 0,10)
    
  fakeHisto.SetLineColor(ROOT.kWhite)
  fakeHisto2.SetLineColor(ROOT.kWhite)
  if(maxi==mini):
   fakeHisto.GetYaxis().SetRangeUser(0,100)
   fakeHisto2.GetYaxis().SetRangeUser(0,100)
  else:
   fakeHisto.GetYaxis().SetRangeUser(0,3*maxi)
   fakeHisto2.GetYaxis().SetRangeUser(0,3*maxi)

  f4.SetParameter(0,c2)
  f4.SetParameter(1,c1)
  f1.SetParameter(0,c2)
  f1.SetParameter(1,c0)
  f5.SetParameter(0,mini)
  f5.SetParameter(1,0)
  f2.SetParameter(0,mini)
  f2.SetParameter(1,0)
  f3.SetParameter(0,maxi)
  f3.SetParameter(1,0)
  f6.SetParameter(0,maxi)
  f6.SetParameter(1,0)
  f3.SetLineColor(ROOT.kRed)
  f6.SetLineColor(ROOT.kRed)
  f2.SetLineColor(ROOT.kBlue)
  f5.SetLineColor(ROOT.kBlue)
  f1.SetLineColor(ROOT.kGreen+1)
  f4.SetLineColor(ROOT.kGreen+1)
  f1.SetLineWidth(3)
  f2.SetLineWidth(3)   
  f3.SetLineWidth(3) 
  f4.SetLineWidth(3)
  f5.SetLineWidth(3)
  f6.SetLineWidth(3)    
  
  f7=ROOT.TF1("dynamic window","[0]+[1]*x",0,10)
  f8=ROOT.TF1("dynamic window","[0]+[1]*x",0,10)  
  f8.SetParameter(0,cn2)
  f8.SetParameter(1,cn1)
  f7.SetParameter(0,cn2)
  f7.SetParameter(1,cn0)
  f8.SetLineColor(ROOT.kOrange+1)
  f7.SetLineColor(ROOT.kOrange+1)
  f8.SetLineWidth(3)
  f7.SetLineWidth(3)

  #a.SetTitle("iterlabel, layer "+str(i)+", max="+str(round(maxi,3))+", mini="+str(round(mini,3)))
  a.cd(1)
  fakeHisto2.Draw()
  f1.Draw("same")
  f2.Draw("same")
  f3.Draw("same")
  f7.Draw("same")
  a.cd(2)
  fakeHisto.Draw()
  f4.Draw("same")
  f5.Draw("same")
  f6.Draw("same")
  f8.Draw("same")
  a.cd()
  legend=ROOT.TLegend(0.1,0.7,0.9,0.9)
  legend.SetHeader( iterlabel+ " layer "+str(i)+", max="+str(round(maxi,3))+", mini="+str(round(mini,3)) )
  legend.AddEntry(f1, str(round(c2,3))+"+("+str(round(c0,3))+")*1/pt+("+str(round(c1,3))+")*theta", "l")
  legend.AddEntry(f7, str(round(cn2,3))+"+("+str(round(cn0,3))+")*1/pt+("+str(round(cn1,3))+")*theta", "l")
  legend.Draw()
  a.SaveAs(label+"_analyzed_"+iterlabel+"_"+str(i)+".png")

for i in range(len(data['m_layer_configs'])):
  cfg=data['m_layer_configs'][i]
  print (data['m_layer_configs'][i])
  print ("layer", i)
  c_dp_0=data['m_layer_configs'][i]["c_dp_0"]
  c_dp_1=data['m_layer_configs'][i]["c_dp_1"]
  c_dp_2=data['m_layer_configs'][i]["c_dp_2"]
  c_dq_0=data['m_layer_configs'][i]["c_dq_0"]
  c_dq_1=data['m_layer_configs'][i]["c_dq_1"]
  c_dq_2=data['m_layer_configs'][i]["c_dq_2"]
  c_c2_0=data['m_layer_configs'][i]["c_c2_0"]
  c_c2_1=data['m_layer_configs'][i]["c_c2_1"]
  c_c2_2=data['m_layer_configs'][i]["c_c2_2"]
  m_select_min_dphi=data['m_layer_configs'][i]["m_select_min_dphi"]
  m_select_max_dphi=data['m_layer_configs'][i]["m_select_max_dphi"]
  m_select_min_dq=data['m_layer_configs'][i]["m_select_min_dq"]
  m_select_max_dq=data['m_layer_configs'][i]["m_select_max_dq"]
  cfg2=data2['m_layer_configs'][i]
  print (data2['m_layer_configs'][i])
  print ("layer", i)
  c_dpn_0=data2['m_layer_configs'][i]["c_dp_0"]
  c_dpn_1=data2['m_layer_configs'][i]["c_dp_1"]
  c_dpn_2=data2['m_layer_configs'][i]["c_dp_2"]
  c_dqn_0=data2['m_layer_configs'][i]["c_dq_0"]
  c_dqn_1=data2['m_layer_configs'][i]["c_dq_1"]
  c_dqn_2=data2['m_layer_configs'][i]["c_dq_2"]
  c_c2n_0=data2['m_layer_configs'][i]["c_c2_0"]
  c_c2n_1=data2['m_layer_configs'][i]["c_c2_1"]
  c_c2n_2=data2['m_layer_configs'][i]["c_c2_2"]
  draw_dd_c012(c_dp_0,c_dp_1,c_dp_2,c_dpn_0,c_dpn_1,c_dpn_2, "dp", m_select_min_dphi,m_select_max_dphi)
  draw_dd_c012(c_dq_0,c_dq_1,c_dq_2,c_dqn_0,c_dqn_1,c_dqn_2, "dq", m_select_min_dq,m_select_max_dq)
  draw_dd_c012(c_c2_0,c_c2_1,c_c2_2,c_c2n_0,c_c2n_1,c_c2n_2, "chi2", 15.,15.)
