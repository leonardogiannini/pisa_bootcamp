# Project: "Hit selection windows code" 

1. prepare environment 

   - start from cmssw clean release
   - add packages
   
   ```
   git cms-addpkg RecoTracker/MkFitCMS
   git cms-addpkg RecoTracker/MkFitCore
   git cms-addpkg FWCore/Utilities
   ```
   - make sure you the have the commit https://github.com/trackreco/cmssw/pull/130/commits/e10bc031574cf7e36a5e6007fe6df98ba85816cf
   - add other changes at this point (material/PR127/...)
   - if the Geometry binary file doesn't match you can remake it with RecoTracker/MkFit/test/dumpMkFitGeometry.py and move it to standalone/CMS-phase1.bin
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
3. get to root format
   - the slow step, which can need improvement. use tree2.py - example toruntree2.sh to run full stats.
5. make histograms
   - use histo2_fromtreeNewBinning.C - example running all the stats in ok.sh
   ```
   g++ histo2_fromtreeNewBinning.C -g -o plot-NewBin `root-config --cflags --glibs`
   source ok.sh
   hadd histo-all.root **.root
   ```
6. fit windows
   - everything done by study/ana_histos_remake.py (other useful commands in study/to2)
   - fundamental steps 
     ```
     mkdir occ histos graphs txt res examples
     python3 ana_histos_remake.py ../allhistos-bkfwd2.root
     ```
7. make jsons
   - use study/redojson.sh
