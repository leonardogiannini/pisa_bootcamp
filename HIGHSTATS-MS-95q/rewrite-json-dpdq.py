#-rw-rw-r--. 1 legianni legianni  28 Nov  2 19:47 dq-layer_71_11_fitpars.txt
#-rw-rw-r--. 1 legianni legianni  28 Nov  2 19:47 dphi-layer_71_11_fitpars.txt
#-rw-rw-r--. 1 legianni legianni  28 Nov  2 19:47 chi2-layer_71_11_fitpars.txt
import sys
from collections import OrderedDict
jsonfile=sys.argv[1]
itercode=sys.argv[2]
iterlabel=sys.argv[3]

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

for i in range(len(data['m_layer_configs'])):
  cfg=data['m_layer_configs'][i]
  print (data['m_layer_configs'][i])
  print ("layer", i)
  #print ("dphi-pars", c_dp_0,c_dp_1,c_dp_2)
  #print ("dq-pars", c_dq_0,c_dq_1,c_dq_2)
  #print ("chi2-pars", c_dq_0,c_c2_1,c_c2_2)
  print("BONS")
  q=open("txt/dq-layer_"+str(i)+"_"+itercode+"_fitpars.txt")  
  lq=q.readlines()
  p=open("txt/dphi-layer_"+str(i)+"_"+itercode+"_fitpars.txt")
  lp=p.readlines()
  c=open("txt/chi2-layer_"+str(i)+"_"+itercode+"_fitpars.txt")
  lc=c.readlines()
  try:
   a=float(lp[-4:-3][0].split("+")[0])
   b=float(lp[-3:-2][0].split("=")[1].split("+")[0])
   c=float(lp[-2:-1][0].split("=")[1].split("+")[0])
   print (a,b,c)
   data['m_layer_configs'][i]["c_dp_0"]=b
   data['m_layer_configs'][i]["c_dp_1"]=c
   data['m_layer_configs'][i]["c_dp_2"]=a
  except:
   print(1)
  try:
   a=float(lq[-4:-3][0].split("+")[0])
   b=float(lq[-3:-2][0].split("=")[1].split("+")[0])
   c=float(lq[-2:-1][0].split("=")[1].split("+")[0])
   print (a,b,c)
   data['m_layer_configs'][i]["c_dq_0"]=b
   data['m_layer_configs'][i]["c_dq_1"]=c
   data['m_layer_configs'][i]["c_dq_2"]=a
  except:
   print(1)
  try:
   a=float(lc[-4:-3][0].split("+")[0])
   b=float(lc[-3:-2][0].split("=")[1].split("+")[0])
   c=float(lc[-2:-1][0].split("=")[1].split("+")[0])
   print (a,b,c)
   #data['m_layer_configs'][i]["c_c2_0"]=b
   #data['m_layer_configs'][i]["c_c2_1"]=c
   #data['m_layer_configs'][i]["c_c2_2"]=a
  except:
   print(1)
  print (data['m_layer_configs'][i])
 

# Serializing json
json_object = json.dumps(data, indent=1)#4, sort_keys=True)
 
# Writing to sample.json
with open(sys.argv[1].split("/")[-1], "w") as outfile:
    outfile.write(json_object)

