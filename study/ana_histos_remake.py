import ROOT
import numpy as np
import array

a=ROOT.TCanvas()
ROOT.gStyle.SetOptStat(0000)

import sys
filename=sys.argv[1]

import json
from collections import OrderedDict

dictofIters={

24 : "detachedQuadStep",
7 : "detachedTripletStep",
22 : "highPtTripletStep",
4 : "initialStep",
23 : "lowPtQuadStep",
5 : "lowPtTripletStep",
8 : "mixedTripletStep",
9 : "pixelLessStep",
6 : "pixelPairStep",
10 : "tobTecStep",

}

def fromth3_to_2dfits(f,objname,q9x):
    iterc=int(objname.split("_")[2])
    itername=dictofIters[iterc]
    layer=int(objname.split("_")[1])
    h = f.Get(objname)
    Nx = h.GetNbinsX()
    Ny = h.GetNbinsY()
    Nz = h.GetNbinsZ()
    print (Nx,Ny,Nz)

    #for TGraph
    xg=[]
    yg=[]
    zg=[]
    zerr=[]
    xerr=[]
    yerr=[]

    #should be taken from h but I am doing copy-paste from histo2_fromtreeNewBinning
    binstheta=array.array("d",[0., 0.09375, 0.1875 , 0.28125, 0.375, 0.46875, 0.5625, 0.65625, 0.75, 0.84375, 0.9375, 1.03125, 1.125, 1.21875, 1.3125, 1.40625, 1.5])
    bins1pT=array.array("d",[0., 0.4, 0.8, 1.2, 1.6, 2., 2.4, 2.8, 3.2, 3.6, 4., 4.4, 4.8, 5.2, 5.6, 6., 6.4, 6.8, 7.2, 7.6,  8., 8.4, 8.8, 9.2, 9.6, 10.])

    endx=bins1pT[-1]
    endy=binstheta[-1]
    print ("end bins",endx,endy)

    #prepare quantile histograms + other
    tofill2d=ROOT.TH2F("fill","fill;invpt;theta", Nx, bins1pT,  Ny, binstheta)
    occupancy2d=ROOT.TH2F("occupancy", "occupancy;invpt;theta", Nx, bins1pT,  Ny, binstheta)
    residual2d=ROOT.TH2F("residual", "residual;invpt;theta", Nx, bins1pT,  Ny, binstheta)
    residual2dg=ROOT.TH2F("residualG", "residualG;invpt;theta", Nx, bins1pT,  Ny, binstheta)

    #remove bad bins from quantiles
    avg=[]
    avg2=[]
    avstd=[]
    for i in range(1,Nx):
     for j in range(1,Ny):
       foo=h.ProjectionZ("ss",i,i,j,j)
       ee=foo.GetEntries()
       aa=foo.GetMean()
       bb=foo.GetStdDev()
       if (ee>0):
         avg.append(ee)
         avg2.append(aa)
         avstd.append(bb)

    #compute avg occ /3.
    mval3=np.mean(avg)/3.
    print ("mean occ/3",mval3)
    if (mval3>100): mval3=100
    print ("mean occ/3",mval3)

    # compute average of the mean value (x10) and of the stdDev
    mm2=np.mean(avg2)*2*5 #this is no longe used
    meanstd=np.mean(avstd)

    for i in range(1,Nx):
     for j in range(1,Ny):
       #print(i, j, "projections of bins")
       foo=h.ProjectionZ("ss",i,i,j,j)
       foo.SetTitle(objname+"_BinX_"+str(i)+"_BinY_"+str(j))
       occupancy2d.SetBinContent(i,j,foo.GetEntries())
       # remove bad bins, i.e. large stdDev (error) or low occupancy
       if(foo.GetEntries()<mval3):
         continue
       if(foo.GetStdDev()<(meanstd/10.)):
         continue

       if (foo.Integral()>0):
         #find 95 quantile
         Q99=np.array([0.])
         foo.GetQuantiles(1,Q99,np.array([q9x/100.]))
         if(i%5==0 and j%5==0):
           line2 = ROOT.TLine(Q99,0,Q99,foo.GetMaximum())
           line2.SetLineColor(ROOT.kRed)
           line2.SetLineWidth(3)
           foo.Draw()
           line2.Draw()
           a.SaveAs("examples/"+objname+"_BinX_"+str(i)+"_BinY_"+str(j)+".png")

         #hard coded 91 and 99 quantiles
         Q90=np.array([0.])
         Q100=np.array([0.])
         tofill2d.SetBinContent(i,j,Q99)
         foo.GetQuantiles(1,Q90,np.array([91/100.]))
         foo.GetQuantiles(1,Q100,np.array([99/100.]))

         #error estimate for quantile = interquantile distance / n tracks in the range (proportional to the error ?)
         bino=foo.FindBin(Q99)
         bino2=foo.FindBin(Q90)
         bino3=foo.FindBin(Q100)
         Int1=foo.Integral(bino2,bino)
         Int2=foo.Integral(bino,bino3)
         DN=(Int1/2.+Int2/2.)**0.5
         DE=(-Q90+Q100)/2.

         # complete TH2F
         tofill2d.SetBinError(i,j,DE/DN)

         #prepare equivalent TGraph
         zg.append(float(Q99))
         xg.append(h.GetXaxis().GetBinCenter(i))
         yg.append(h.GetYaxis().GetBinCenter(j))
         zerr.append(DE/DN)
         yerr.append(0.)
         xerr.append(0.)

       else:
         pass

    a.cd()
    tofill2d.Draw("colz")
    a.SaveAs("histos/"+objname+"_h_"+str(q9x)+"quantiles.png")

    a.cd()
    occupancy2d.Draw("colz")
    a.SaveAs("occ/"+objname+"_OCC_"+str(q9x)+"quantiles.png")

    #fit functions
    f2=ROOT.TF2("f2","([0]+[1]*x+[2]*y)",0,endx,0,endy)
    f1=ROOT.TF2("f1","[0]",0,endx,0,endy)
    f2g=ROOT.TF2("f2g","([0] + [1]*x + [2]*y)",0,endx,0,endy)
    f1g=ROOT.TF2("f1g","[0]",0,endx,0,endy)

    #TH2F
    tofill2d.Fit(f1)
    print ("fit 1 par",f1.GetParameter(0),f1.GetParError(0))
    tofill2d.Fit(f2)
    print ("fit 3 par",f2.GetParameter(0),f2.GetParError(0))
    print ("fit 3 par",f2.GetParameter(1),f2.GetParError(1))
    print ("fit 3 par",f2.GetParameter(2),f2.GetParError(2))
    ftxt=open("txt/"+objname+"_fitpars.txt", "w")
    ftxt.write("FROM TH2F\n")
    ftxt.write("constant\n")
    ftxt.write(str(f1.GetParameter(0))+"+-"+str(f1.GetParError(0)))
    ftxt.write("\n")
    ftxt.write("chi2/ndof = "+str(f1.GetChisquare()/f1.GetNDF()))
    ftxt.write("\n")
    ftxt.write("plane\n")
    ftxt.write(str(f2.GetParameter(0))+"+-"+str(f2.GetParError(0)))
    ftxt.write("\n")
    ftxt.write("invpt slope = "+str(f2.GetParameter(1))+"+-"+str(f2.GetParError(1)))
    ftxt.write("\n")
    ftxt.write("theta slope = "+str(f2.GetParameter(2))+"+-"+str(f2.GetParError(2)))
    ftxt.write("\n")
    ftxt.write("chi2/ndof = "+str(f2.GetChisquare()/f2.GetNDF()))
    ftxt.write("\n")

    # fill residual with 1-fit/value
    for i in range(1, Nx):
     for j in range(1, Ny):
       if(tofill2d.GetBinContent(i,j)>0):
         ap=f2.GetParameter(0)
         bp=f2.GetParameter(1)
         cp=f2.GetParameter(2)
         value= (ap+bp*h.GetXaxis().GetBinCenter(i)+cp*h.GetYaxis().GetBinCenter(j))
         residual2d.SetBinContent(i,j,1-value/tofill2d.GetBinContent(i,j))
       else:
         pass

    # draw with range cut
    a.cd()
    residual2d.GetZaxis().SetRangeUser(-1,1)
    residual2d.Draw("colz1")
    a.SaveAs("res/"+objname+"_RES_"+str(q9x)+"quantiles.png")

    # build the TGraph (no errors version should cross check with linalg below, error version should match TH2D)
    g2d=ROOT.TGraph2DErrors(len(xg), np.array(xg), np.array(yg), np.array(zg), np.array(xerr), np.array(yerr), np.array(zerr))
    #g2d=ROOT.TGraph2D(len(xg), np.array(xg), np.array(yg), np.array(zg))

    # draw TGraph
    a.cd()
    g2d.GetXaxis().SetTitle("invpt")
    g2d.GetYaxis().SetTitle("theta")
    if(np.std(xg)>0 and np.std(yg)>0):
     g2d.Draw("surf1")
    else:
     print("1")
    a.SaveAs("graphs/"+objname+"_q_"+str(q9x)+"quantiles.png")

    # fit
    g2d.Fit(f1)
    print ("fit 1 par g",f1.GetParameter(0),f1.GetParError(0))
    g2d.Fit(f2g)
    print ("fit 3 par g",f2g.GetParameter(0),f2g.GetParError(0))
    print ("fit 3 par g",f2g.GetParameter(1),f2g.GetParError(1))
    print ("fit 3 par g",f2g.GetParameter(2),f2g.GetParError(2))
    ftxt.write("from tgraph2D\n")
    ftxt.write("constant\n")
    ftxt.write(str(f1.GetParameter(0))+"+-"+str(f1.GetParError(0)))
    ftxt.write("\n")
    ftxt.write("chi2/ndof = "+str(f1.GetChisquare()/f1.GetNDF()))
    ftxt.write("\n")
    ftxt.write("plane\n")
    ftxt.write(str(f2g.GetParameter(0))+"+-"+str(f2g.GetParError(0)))
    ftxt.write("\n")
    ftxt.write("invpt slope = "+str(f2g.GetParameter(1))+"+-"+str(f2g.GetParError(1)))
    ftxt.write("\n")
    ftxt.write("theta slope = "+str(f2g.GetParameter(2))+"+-"+str(f2g.GetParError(2)))
    ftxt.write("\n")
    ftxt.write("chi2/ndof = "+str(f2g.GetChisquare()/f2g.GetNDF()))
    ftxt.write("\n")

    # no error fit - cross check
    X = np.array(xg)
    Y = np.array(yg)
    C = np.ones(X.shape)
    A = np.array([C, xg, yg]).T
    B = np.array(zg)
    coeff, r, rank, s = np.linalg.lstsq(A, B)
    print("COEFF", coeff, r, rank, s)
    ftxt.write("from linalg\n")
    ftxt.write("const = "+str(coeff[0])+"+-")
    ftxt.write("\n")
    ftxt.write("invpt slope = "+str(coeff[1])+"+-")
    ftxt.write("\n")
    ftxt.write("theta slope = "+str(coeff[2])+"+-")
    ftxt.write("\n")

    # fill residual with 1-fit/value
    for i in range(1,Nx):
     for j in range(1,Ny):
       if(tofill2d.GetBinContent(i,j)>0):
         ap=f2g.GetParameter(0)
         bp=f2g.GetParameter(1)
         cp=f2g.GetParameter(2)
         value= (ap+bp*h.GetXaxis().GetBinCenter(i)+cp*h.GetYaxis().GetBinCenter(j))
         residual2dg.SetBinContent(i,j,1-value/tofill2d.GetBinContent(i,j))
       else:
         pass

    # draw residual  for graph
    a.cd()
    #residual2dg.GetZaxis().SetRangeUser(-1,1)
    print("qui si fa inte")
    residual2dg.Draw("colz1")
    a.SaveAs("res/"+objname+"_RESG_"+str(q9x)+"quantiles.png")

    # ================== #
    # comparison section #
    # ================== #

    fx=ROOT.TF1("fw","([0]+[1]*x)",0,endy)
    fw=ROOT.TF1("fw","([0]+[1]*x+[2])",0,endy)
    fw2=ROOT.TF1("fw2","([0]+[1]*x+[2])",0,endy)
    fw_numpy=ROOT.TF1("fw2","([0]+[1]*x+[2])",0,endy)
    f_old=ROOT.TF1("f_old","([0]+[1]*x+[2])",0,endy)
    f_max=ROOT.TF1("f_max","([0])",0,endy)
    f_min=ROOT.TF1("f_min","([0])",0,endy)
    jsonfile="../../RecoTracker-MkFit/mkfit-phase1-"+itername+".json"
    f=open(jsonfile)
    data=json.loads(f.read(), object_pairs_hook=OrderedDict)
    cfg=data['m_layer_configs'][layer]
    print(cfg['m_winpars_fwd'])
    bkwd="bkwd" in objname
    setofpars="m_winpars_fwd"
    if bkwd: setofpars="m_winpars_bkw"
    print(setofpars)
    print(objname)
    if "chi2" in objname:
      b1=data['m_layer_configs'][layer][setofpars][9]
      c1=data['m_layer_configs'][layer][setofpars][10]
      a1=data['m_layer_configs'][layer][setofpars][11]
      maxi=15/1.1
      mini=15/1.1
    elif "dphi" in objname:
      b1=data['m_layer_configs'][layer][setofpars][1]
      c1=data['m_layer_configs'][layer][setofpars][2]
      a1=data['m_layer_configs'][layer][setofpars][3]
      mini=data['m_layer_configs'][layer]["m_select_min_dphi"]/1.1
      maxi=data['m_layer_configs'][layer]["m_select_max_dphi"]/1.1
    elif "dq" in objname:
      b1=data['m_layer_configs'][layer][setofpars][5]
      c1=data['m_layer_configs'][layer][setofpars][6]
      a1=data['m_layer_configs'][layer][setofpars][7]
      mini=data['m_layer_configs'][layer]["m_select_min_dq"]/1.1
      maxi=data['m_layer_configs'][layer]["m_select_max_dq"]/1.1
    ###add clamp values
    print(objname, jsonfile,layer,b1,c1,a1)
    for i in range(1, Nx):
        rr=tofill2d.ProjectionY("proj "+str(i), i, i)
        if(rr.Integral()<=0):
          continue
        rr.Fit(fx)
        fw.SetParameter(0,f2.GetParameter(0))
        fw.SetParameter(1,f2.GetParameter(2))
        fw.SetParameter(2,f2.GetParameter(1)*h.GetXaxis().GetBinCenter(i))
        fw2.SetParameter(0,f2g.GetParameter(0))
        fw2.SetParameter(1,f2g.GetParameter(2))
        fw2.SetParameter(2,f2g.GetParameter(1)*h.GetXaxis().GetBinCenter(i))
        fw_numpy.SetParameter(0,coeff[0])
        fw_numpy.SetParameter(1,coeff[2])
        fw_numpy.SetParameter(2,coeff[1]*h.GetXaxis().GetBinCenter(i))
        f_old.SetParameter(0,a1)
        f_old.SetParameter(1,c1)
        f_old.SetParameter(2,b1*h.GetXaxis().GetBinCenter(i))
        f_max.SetParameter(0,maxi)
        f_min.SetParameter(0,mini)
        f_old.SetLineColor(ROOT.kPink)
        f_max.SetLineColor(ROOT.kMagenta)
        f_min.SetLineColor(ROOT.kViolet)
        f_old.SetLineWidth(3)
        f_max.SetLineWidth(3)
        f_min.SetLineWidth(3)
        fw2.SetLineColor(ROOT.kGreen+1)
        fx.SetLineColor(ROOT.kOrange)
        fw_numpy.SetLineColor(ROOT.kBlue)
        a.cd()
        rr.Draw("histe")
        fw.Draw("same")
        fw2.Draw("same")
        fx.Draw("same")
        fw_numpy.Draw("same")
        f_old.Draw("same")
        f_min.Draw("same")
        f_max.Draw("same")
        print("BIN "+str(i))
        a.SaveAs("res/"+objname+"_compareFitBin"+str(i)+".png")


f = ROOT.TFile(filename, 'r')
print( "working on this histo")
for k in f.GetListOfKeys():
   try:
     fromth3_to_2dfits(f,k.GetName(),95)
   except:
     print ("NOOOOOOOOOOO")
