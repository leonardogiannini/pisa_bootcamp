# Project: "Hit selection windows code" 

1. prepare environment 

   - start from cmssw clean release
   - add packages
   
   ```
   git cms-addpkg RecoTracker/MkFitCMS
   git cms-addpkg RecoTracker/MkFitCore
   git cms-addpkg FWCore/Utilities

   ```
   - make sure you the commit
   - add the line below to RecoTracker/MkFitCore/interface/Config.h 
    
   ``` 
   #define DUMPHITWINDOW
   ```
   - compile standalone
     

   ``` 
   cd $CMSSW_BASE
   mkdir standalone
   cd standalone
   ../src/RecoTracker/MkFitCore/standalone/configure /full-path-to-CMSSW_BASE/src
   unset INTEL_LICENSE_FILE
   export -n INTEL_LICENSE_FILE
   make -j8
   ```
2. dump hit information
   
   - command example (must be single thread no to mix line printouts) from standalone env
   ```
   ./mkFit --silent --cmssw-n2seeds --num-thr 1 --num-thr-ev 1 --input-file /data2/slava77/samples/2021/10muPt0p2to1000HS/memoryFile.fv7.default.24feee2.230329-1310p2.bin --num-events 100000 --remove-dup --use-dead-modules --try-to-save-sim-info --backward-fit --num-iters-cmssw 10 --build-mimi  | perl -ne 'if (/^HITWINDOWSEL/) { s/^HITWINDOWSEL //og; print; }'
   ```
   - run on all the samples using run-highstat-BF.sh
   
