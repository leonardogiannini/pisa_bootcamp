import ROOT
import numpy as np

ROOT.gStyle.SetOptStat(0000)

a=ROOT.TCanvas()

filename='histos3d-1000.root'
objname='dq-layer6'
filename='histos3d-MultipleScattering.root'

def fromth3_to_2dfits(f,objname,q9x):
    h = f.Get(objname)
    Nx = h.GetNbinsX()
    Ny = h.GetNbinsY()
    Nz = h.GetNbinsZ()
    print (Nx,Ny,Nz)

    xg=[]
    yg=[]
    zg=[]

    endx=round(h.GetXaxis().GetBinWidth(Nx)/2.+ h.GetXaxis().GetBinCenter(Nx),1)
    endy=round(h.GetYaxis().GetBinWidth(Ny)/2.+ h.GetYaxis().GetBinCenter(Ny),1)

    #print (endx,endy)
    tofill2d=ROOT.TH2F("fill", "fill;invpt;theta", Nx, 0, endx,  Ny, 0, endy)
    occupancy2d=ROOT.TH2F("occupancy", "occupancy;invpt;theta", Nx, 0, endx,  Ny, 0, endy)
    residual2d=ROOT.TH2F("residual", "residual;invpt;theta", Nx, 0, endx,  Ny, 0, endy)    
    residualrel2d=ROOT.TH2F("residualrel", "residual relative;invpt;theta", Nx, 0, endx,  Ny, 0, endy)    

    for i in range(Nx+2):
     for j in range(Ny+2):
       #print(i, j, "projections of bins")
       foo=h.ProjectionZ("ss",i,i+1,j,j+1)
       occupancy2d.SetBinContent(i,j,foo.GetEntries())
       #if(foo.GetEntries()<100):
       #  continue
       if (foo.Integral()>0):
         print ("integral", foo.Integral(), foo.GetEntries(),  i, j)
         if (foo.GetEntries()<100.):
            print("EMERGENCY", objname, "invpt", h.GetXaxis().GetBinCenter(i), "theta", h.GetYaxis().GetBinCenter(j))
         Q99=np.array([0.])
         foo.GetQuantiles(1,Q99,np.array([q9x/100.]))
         print( Q99)
         tofill2d.SetBinContent(i,j,Q99)
         #residual2d.SetBinContent(i,j,Q99) ##subtract later
         zg.append(float(Q99))
         xg.append(h.GetXaxis().GetBinCenter(i))
         yg.append(h.GetYaxis().GetBinCenter(j))
       else:
         tofill2d.SetBinContent(i,j,0)
         #residual2d.SetBinContent(i,j,0)
    print (tofill2d.Integral())
    
    a.cd()
    tofill2d.Draw("colz")
    a.SaveAs("histos/"+objname+"_h_"+str(q9x)+"quantiles.png")
    
    a.cd()
    occupancy2d.Draw("colz")
    a.SaveAs("occ/"+objname+"_OCC_"+str(q9x)+"quantiles.png")

    f2=ROOT.TF2("f2","[0]+[1]*x+[2]*y",0,endx,0,endy)
    f1=ROOT.TF2("f1","[0]",0,endx,0,endy)

    
    tofill2d.Fit(f1)
    print (f1.GetParameter(0),f1.GetParError(0))
    tofill2d.Fit(f2)
    print (f2.GetParameter(0),f2.GetParError(0))
    print (f2.GetParameter(1),f2.GetParError(1))
    print (f2.GetParameter(2),f2.GetParError(2))
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
    g2d=ROOT.TGraph2D(len(xg), np.array(xg), np.array(yg), np.array(zg))
    print(2, np.std(xg), np.std(yg))
    a.cd()
    g2d.GetXaxis().SetTitle("invpt")
    g2d.GetYaxis().SetTitle("theta")
    if(np.std(xg)>0 and np.std(yg)>0):
     g2d.Draw("surf1")
    else:
     print("1")
    a.SaveAs("graphs/"+objname+"_q_"+str(q9x)+"quantiles.png")
    print(len(xg), "LEN Gf")
    g2d.Fit(f1)
    print (f1.GetParameter(0),f1.GetParError(0))
    g2d.Fit(f2)
    print (f2.GetParameter(0),f2.GetParError(0))
    print (f2.GetParameter(1),f2.GetParError(1))
    print (f2.GetParameter(2),f2.GetParError(2))
    ftxt.write("from tgraph2D\n")
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
    
    for i in range(Nx+2):
     for j in range(Ny+2):
       invpt=residual2d.GetXaxis().GetBinCenter(i)
       theta=residual2d.GetYaxis().GetBinCenter(j)

       if (tofill2d.GetBinContent(i,j)>0):
        residual2d.SetBinContent( i, j, tofill2d.GetBinContent(i,j)-(f2.GetParameter(0)+(theta)*f2.GetParameter(2)+(invpt)*f2.GetParameter(1))  ) 
        residualrel2d.SetBinContent(i,j, 1- (f2.GetParameter(0)+(theta)*f2.GetParameter(2)+(invpt)*f2.GetParameter(1))/(tofill2d.GetBinContent(i,j)) )
  
    a.cd()
    residual2d.Draw("colz")
    a.SaveAs("histos-residual/"+objname+"_hr_"+str(q9x)+"quantiles.png")
    residualrel2d.Draw("colz")
    a.SaveAs("histos-residual/"+objname+"_hrrel_"+str(q9x)+"quantiles.png")


f = ROOT.TFile(filename, 'r')

for k in f.GetListOfKeys():
   try:
     print(k.GetName(), "working on this histo")
     fromth3_to_2dfits(f,k.GetName(),95)
   except:
     print ("NOOOOOOOOOOO")
#>>> for i in range(100):
#...  if (fo.GetBinContent(i+1)>0):
#...   print (i, fo.GetBinContent(i+1), fo.GetBinCenter(i+1), fo.GetBinWidth(i+1)/2. +fo.GetBinCenter(i+1) , -fo.GetBinWidth(i+1)/2. +fo.GetBinCenter(i+1))
#... 
#3 4.0 0.7000000000000001 0.8 0.6000000000000001
#5 5.0 1.1 1.2000000000000002 1.0
#7 5.0 1.5000000000000002 1.6000000000000003 1.4000000000000001
#12 4.0 2.5000000000000004 2.6000000000000005 2.4000000000000004
#20 4.0 4.1 4.199999999999999 3.9999999999999996
#21 1.0 4.3 4.3999999999999995 4.2

# Get underlying array and convert it to a numpy array
#arr = h.GetArray()
#binvals = np.ndarray( ((Nx+2)*(Ny+2)*(Nz+2),), dtype=np.float32, buffer=arr)
#binvals = np.transpose(binvals.reshape((Nz+2,Ny+2,Nx+2),order='C'),(2,1,0))
# Strip off underflow and overflow bin
# binvals = binvals[1:-1,1:-1,1:-1]
