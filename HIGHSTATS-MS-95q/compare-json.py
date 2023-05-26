#-rw-rw-r--. 1 legianni legianni  28 Nov  2 19:47 dq-layer_71_11_fitpars.txt
#-rw-rw-r--. 1 legianni legianni  28 Nov  2 19:47 dphi-layer_71_11_fitpars.txt
#-rw-rw-r--. 1 legianni legianni  28 Nov  2 19:47 chi2-layer_71_11_fitpars.txt
import sys
jsonfile=sys.argv[1]
itercode=sys.argv[2]
iterlabel=sys.argv[3]
fromgraph=sys.argv[4]
if fromgraph=="1":
 N=0
 type2d="_GRAPH"
else:
 N=-9
 type2d="_HISTO"

ftxtc=open("chi2FITS_QUALITY_"+iterlabel+type2d+".txt", "w")
ftxtq=open("dqFITS_QUALITY_"+iterlabel+type2d+".txt", "w")
ftxtp=open("dpFITS_QUALITY_"+iterlabel+type2d+".txt", "w")
ftxtp.write("from "+type2d+"\n")
ftxtc.write("from "+type2d+"\n")
ftxtq.write("from "+type2d+"\n")
'''
FROM TH2F
constant
4.467046091769638+-0.668359640577128
chi2/ndof = 1.4632819258351253
plane
1.7967559198090681+-37.39356150955007
invpt slope = 8.428316671513729+-2.7042604995853465
theta slope = -12.175330344548877+-28.59916802439287
chi2/ndof = 0.27578408203887045
from tgraph2D
constant
5.784000000007668+-1.0077270352782204
chi2/ndof = 10.155137777777778
plane
0.17057377979691468+-22.003436949106987
invpt slope = 8.940983606282016+-1.2252255590437626
theta slope = -11.633879788432896+-16.944869220214606
chi2/ndof = 1.3081704918032757
'''
import ROOT
ca=ROOT.TCanvas()
checkvals=ROOT.TH1F("original values", "original values", 10, 0, 10)
checkvals2=ROOT.TH1F("Values", "Values", 10, 0, 10)
checkvals2.SetLineColor(ROOT.kBlue)
checkvals2.SetFillColorAlpha(ROOT.kRed, 0.2)
checkvals.SetLineColor(ROOT.kBlue)
checkvals.SetFillColorAlpha(ROOT.kBlue, 0.2)
checkvals.SetLineWidth(2)
checkvals2.SetLineWidth(2)
checkvals2.SetMarkerSize(3)
checkvals.SetMarkerSize(3)
checkvals2.GetXaxis().SetBinLabel(3,"const");
checkvals2.GetXaxis().SetBinLabel(6,"invpt coeff.");
checkvals2.GetXaxis().SetBinLabel(9,"theta coeff.");

ROOT.gStyle.SetPaintTextFormat("4.3f");
ROOT.gStyle.SetOptStat(0000)

#f=open("../RecoTracker-MkFit/mkfit-phase1-initialStep.json")
f=open(jsonfile)
import json
data=json.load(f)
lcfg=data['m_layer_configs']

for i in range(len(lcfg)):
  cfg=lcfg[i]
  c_dp_0=cfg["c_dp_0"] 
  c_dp_1=cfg["c_dp_1"] 
  c_dp_2=cfg["c_dp_2"]  
  c_dq_0=cfg["c_dq_0"]  
  c_dq_1=cfg["c_dq_1"]
  c_dq_2=cfg["c_dq_2"]
  c_c2_0=cfg["c_c2_0"]  
  c_c2_1=cfg["c_c2_1"]
  c_c2_2=cfg["c_c2_2"]
  print ("layer", i)
  #print ("dphi-pars", c_dp_0,c_dp_1,c_dp_2)
  #print ("dq-pars", c_dq_0,c_dq_1,c_dq_2)
  #print ("chi2-pars", c_dq_0,c_c2_1,c_c2_2)

  q=open("txt/dq-layer_"+str(i)+"_"+itercode+"_fitpars.txt")  
  lq=q.readlines()
  p=open("txt/dphi-layer_"+str(i)+"_"+itercode+"_fitpars.txt")
  lp=p.readlines()
  c=open("txt/chi2-layer_"+str(i)+"_"+itercode+"_fitpars.txt")
  lc=c.readlines()
  maxx=max(abs(c_dp_0),abs(c_dp_1),abs(c_dp_2))
  print ("dphi-pars", c_dp_0,c_dp_1,c_dp_2)
  checkvals.SetBinContent(2,c_dp_2)
  checkvals.SetBinContent(5,c_dp_0)
  checkvals.SetBinContent(8,c_dp_1)
  try:
   chifit=lp[-1+N]
   a=float(lp[-4+N:-3+N][0].split("+")[0])
   b=float(lp[-3+N:-2+N][0].split("=")[1].split("+")[0])
   c=float(lp[-2+N:-1+N][0].split("=")[1].split("+")[0])
   print("ABC1", a,b,c)
   ae=float(lp[-4+N:-3+N][0].split("+-")[1])
   be=float(lp[-3+N:-2+N][0].split("+-")[1])
   ce=float(lp[-2+N:-1+N][0].split("+-")[1])
   print ("ABC", a,b,c)
   maxi=max(maxx,abs(a),abs(b),abs(c))
   checkvals2.SetBinContent(3,a)
   checkvals2.SetBinContent(6,b)
   checkvals2.SetBinContent(9,c)
   checkvals2.SetBinError(3,ae)
   checkvals2.SetBinError(6,be)
   checkvals2.SetBinError(9,ce)
   checkvals2.GetYaxis().SetRangeUser(-1.2*maxi,1.2*maxi)
  except:
   print(1)
   chifit="N\n"
   checkvals2.SetBinContent(3,0)
   checkvals2.SetBinContent(6,0)
   checkvals2.SetBinContent(9,0)
   checkvals2.SetBinError(3,0)
   checkvals2.SetBinError(6,0)
   checkvals2.SetBinError(9,0)
   checkvals2.GetYaxis().SetRangeUser(-1.2*maxx,1.2*maxx)
  ca.cd()
  checkvals2.Draw("histtext")
  checkvals2.Draw("e1same")
  checkvals.Draw("histtextsame")
  ca.SaveAs("dphi_checklayer"+str(i)+"_"+iterlabel+type2d+".png")
  ftxtp.write("dphi_checklayer"+str(i)+"_"+iterlabel+"\n")
  ftxtp.write(chifit)
  maxx=max(abs(c_dq_0),abs(c_dq_1),abs(c_dq_2))
  print ("dq-pars", c_dq_0,c_dq_1,c_dq_2)
  checkvals.SetBinContent(2,c_dq_2)
  checkvals.SetBinContent(5,c_dq_0)
  checkvals.SetBinContent(8,c_dq_1)
  try:
   chifit=lq[-1+N]
   a=float(lq[-4+N:-3+N][0].split("+")[0])
   b=float(lq[-3+N:-2+N][0].split("=")[1].split("+")[0])
   c=float(lq[-2+N:-1+N][0].split("=")[1].split("+")[0])
   print("ABC1", a,b,c)
   ae=float(lq[-4+N:-3+N][0].split("+-")[1])
   be=float(lq[-3+N:-2+N][0].split("+-")[1])
   ce=float(lq[-2+N:-1+N][0].split("+-")[1])
   maxi=max(maxx,abs(a),abs(b),abs(c))
   checkvals2.SetBinContent(3,a)
   checkvals2.SetBinContent(6,b)
   checkvals2.SetBinContent(9,c)
   checkvals2.SetBinError(3,ae)
   checkvals2.SetBinError(6,be)
   checkvals2.SetBinError(9,ce)
   checkvals2.GetYaxis().SetRangeUser(-1.2*maxi,1.2*maxi)
   print ("ABC",a,b,c)
  except:
   print(1)
   chifit="N\n"
   checkvals2.SetBinContent(3,0)
   checkvals2.SetBinContent(6,0)
   checkvals2.SetBinContent(9,0)
   checkvals2.SetBinError(3,0)
   checkvals2.SetBinError(6,0)
   checkvals2.SetBinError(9,0)
   checkvals2.GetYaxis().SetRangeUser(-1.2*maxx,1.2*maxx)  
  ca.cd()
  checkvals2.Draw("histtext")
  checkvals2.Draw("e1same")
  checkvals.Draw("histtextsame")
  ca.SaveAs("dq_checklayer"+str(i)+"_"+iterlabel+type2d+".png")
  ftxtq.write("dq_checklayer"+str(i)+"_"+iterlabel+"\n")
  ftxtq.write(chifit)
  maxx=max(abs(c_c2_0),abs(c_c2_1),abs(c_c2_2))
  print ("chi2-pars", c_c2_0,c_c2_1,c_c2_2)
  checkvals.SetBinContent(2,c_c2_2)
  checkvals.SetBinContent(5,c_c2_0)
  checkvals.SetBinContent(8,c_c2_1)
  try:
   chifit=lc[-1+N]
   a=float(lc[-4+N:-3+N][0].split("+")[0])
   b=float(lc[-3+N:-2+N][0].split("=")[1].split("+")[0])
   c=float(lc[-2+N:-1+N][0].split("=")[1].split("+")[0])
   print("ABC1", a,b,c)
   ae=float(lq[-4+N:-3+N][0].split("+-")[1])
   be=float(lq[-3+N:-2+N][0].split("+-")[1])
   ce=float(lq[-2+N:-1+N][0].split("+-")[1])
   maxi=max(maxx,abs(a),abs(b),abs(c))
   checkvals2.SetBinContent(3,a)
   checkvals2.SetBinContent(6,b)
   checkvals2.SetBinContent(9,c)
   checkvals2.SetBinError(3,ae)
   checkvals2.SetBinError(6,be)
   checkvals2.SetBinError(9,ce)
   checkvals2.GetYaxis().SetRangeUser(-1.2*maxi,1.2*maxi)
   print ("ABC",a,b,c)
  except:
   print(1)
   chifit="N\n"
   checkvals2.SetBinContent(3,0)
   checkvals2.SetBinContent(6,0)
   checkvals2.SetBinContent(9,0) 
   checkvals2.SetBinError(3,0)
   checkvals2.SetBinError(6,0)
   checkvals2.SetBinError(9,0)
   checkvals2.GetYaxis().SetRangeUser(-1.2*maxx,1.2*maxx)
  ca.cd()
  checkvals2.Draw("histtext")
  checkvals2.Draw("e1same")
  checkvals.Draw("histtextsame")
  ca.SaveAs("chi2_checklayer"+str(i)+"_"+iterlabel+type2d+".png")
  ftxtc.write("chi2_checklayer"+str(i)+"_"+iterlabel+"\n")
  ftxtc.write(chifit)
