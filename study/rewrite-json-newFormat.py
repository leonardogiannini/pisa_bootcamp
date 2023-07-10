import sys
from collections import OrderedDict
jsonfile=sys.argv[1]
itercode=sys.argv[2]
iterlabel=sys.argv[3]
N=-4

f=open(jsonfile)
import json
data=json.loads(f.read(), object_pairs_hook=OrderedDict)

for i in range(len(data['m_layer_configs'])):
  #example names
  #chi2-bkwd-layer_8_5_fitpars.txt
  #chi2-fwd-layer_8_6_fitpars.txt
  for direction in ["bkwd", "fwd"]:
    setofpars="m_winpars_fwd"
    if direction=="bkwd": setofpars="m_winpars_bkw"
    cfg=data['m_layer_configs'][i]
    print (data['m_layer_configs'][i])
    print ("layer", i)
    print("BONS")
    q=open("txt/dq-"+direction+"-layer_"+str(i)+"_"+itercode+"_fitpars.txt")
    lq=q.readlines()
    p=open("txt/dphi-"+direction+"-layer_"+str(i)+"_"+itercode+"_fitpars.txt")
    lp=p.readlines()
    c=open("txt/chi2-"+direction+"-layer_"+str(i)+"_"+itercode+"_fitpars.txt")
    lc=c.readlines()
    try:
     a=float(lp[-4+N:-3+N][0].split("+")[0])
     b=float(lp[-3+N:-2+N][0].split("=")[1].split("+")[0])
     c=float(lp[-2+N:-1+N][0].split("=")[1].split("+")[0])
     print (a,b,c)
     data['m_layer_configs'][i][setofpars][1]=b
     data['m_layer_configs'][i][setofpars][2]=c
     data['m_layer_configs'][i][setofpars][3]=a
     print("replaced")
    except:
     print(1)
    try:
     a=float(lq[-4+N:-3+N][0].split("+")[0])
     b=float(lq[-3+N:-2+N][0].split("=")[1].split("+")[0])
     c=float(lq[-2+N:-1+N][0].split("=")[1].split("+")[0])
     print (a,b,c)
     data['m_layer_configs'][i][setofpars][5]=b
     data['m_layer_configs'][i][setofpars][6]=c
     data['m_layer_configs'][i][setofpars][7]=a
     print("replaced")
    except:
     print(1)
    try:
     a=float(lc[-4+N:-3+N][0].split("+")[0])
     b=float(lc[-3+N:-2+N][0].split("=")[1].split("+")[0])
     c=float(lc[-2+N:-1+N][0].split("=")[1].split("+")[0])
     print (a,b,c)
     data['m_layer_configs'][i][setofpars][9]=b
     data['m_layer_configs'][i][setofpars][10]=c
     data['m_layer_configs'][i][setofpars][11]=a
     print("replaced")
    except:
     print(1)
    print (data['m_layer_configs'][i])


# Serializing json
json_object = json.dumps(data, indent=1)#4, sort_keys=True)

# Writing to sample.json
with open(sys.argv[1].split("/")[-1], "w") as outfile:
    outfile.write(json_object)
