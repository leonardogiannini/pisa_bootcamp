import ROOT
import numpy as np

ROOT.gStyle.SetOptStat(0000)

canv=ROOT.TCanvas()

filename='histos3d-1000.root'
objname='dq-layer6'
filename='histos3d-MultipleScattering.root'

N=0

def fromth3_to_checkq(f,objname,q9x):
    h = f.Get(objname)
    Nx = h.GetNbinsX()
    Ny = h.GetNbinsY()
    Nz = h.GetNbinsZ()
    print (Nx,Ny,Nz)
    
    layer=objname.split("_")[1]
    iterc=objname.split("_")[2]
    print(layer,iterc, objname)

    xg=[]
    yg=[]
    zg=[]

    endx=round(h.GetXaxis().GetBinWidth(Nx)/2.+ h.GetXaxis().GetBinCenter(Nx),1)
    endy=round(h.GetYaxis().GetBinWidth(Ny)/2.+ h.GetYaxis().GetBinCenter(Ny),1)

    #print (endx,endy)
    tofill2d=ROOT.TH2F("fill", "fill;invpt;theta", Nx, 0, endx,  Ny, 0, endy)
    print(1)
    for i in range(Nx+2):
     for j in range(Ny+2):
       
       if (abs(h.GetXaxis().GetBinCenter(i)-1)>0.1): 
          continue
       if (abs(h.GetYaxis().GetBinCenter(j)-0.7)>0.015 and abs(h.GetYaxis().GetBinCenter(j)-0.3)>0.015):
          continue
       #print(i, j, "projections of bins")
       foo=h.ProjectionZ("ss",i,i+1,j,j+1)
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
         print(12) 
         ftxt=open("txt/"+objname+"_fitpars.txt")
         lp=ftxt.readlines()
         chifit=lp[-1+N]
         a=float(lp[-4+N:-3+N][0].split("+")[0])
         b=float(lp[-3+N:-2+N][0].split("=")[1].split("+")[0])
         c=float(lp[-2+N:-1+N][0].split("=")[1].split("+")[0])
         print("ABC1", a,b,c)
         ae=float(lp[-4+N:-3+N][0].split("+-")[1])
         be=float(lp[-3+N:-2+N][0].split("+-")[1])
         ce=float(lp[-2+N:-1+N][0].split("+-")[1]) 
         value= a+b*h.GetXaxis().GetBinCenter(i)+c*h.GetYaxis().GetBinCenter(j)
         line = ROOT.TLine(value,0,value,foo.GetMaximum())
         line.SetLineColor(ROOT.kRed)
         line2 = ROOT.TLine(Q99,0,Q99,foo.GetMaximum())
         line2.SetLineColor(ROOT.kBlue)
         canv.cd() 
         ll=ROOT.TLegend(0.7,0.7,0.88,0.88)
         ll.AddEntry(foo, "histo")
         ll.AddEntry(line2, "quantile 0.95", "l")
         ll.AddEntry(line, "quantile 0.95 from fit", "l")
         foo.Draw("hist")
         line.Draw()
         line2.Draw()
         ll.Draw()
         canv.SaveAs(objname+"__bin"+str(i)+"__"+str(j)+".png")
         print(Q99, value)
       else:
         tofill2d.SetBinContent(i,j,0)


f = ROOT.TFile(filename, 'r')

for k in f.GetListOfKeys():
   try:
     print(k.GetName(), "working on this histo")
     objname=k.GetName()
     layer=objname.split("_")[1]
     iterc=objname.split("_")[2]
     print(layer,iterc, objname)
     if((layer=='4' or layer=='21' or layer=='48')and (iterc=='4'or iterc=='22' or iterc=='7'or iterc=='24')):
      fromth3_to_checkq(f,k.GetName(),95)
     else:
      print(1)
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
