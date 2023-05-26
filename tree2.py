import sys
import ROOT
t=ROOT.TTree("t", "t")
t.ReadFile(sys.argv[1])
newFile=ROOT.TFile("/ceph/cms/store/user/legianni/trees-fromdump2/treesfor3dhistos_"+sys.argv[2]+".root", "RECREATE")
newFile.cd()
t.Write()
newFile.Close()


