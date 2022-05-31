#! /bin/bash

KIN=$1

InDATAFilename="${KIN}_Raw_Data.root"
InDUMMYFilename="${KIN}_Raw_DummyData.root"
InSIMCFilename="Heep_Coin_${KIN}.root"
OutDATAFilename="${KIN}_Analysed_Data"
OutDUMMYFilename="${KIN}_Analysed_DummyData"
OutFullAnalysisFilename="${KIN}_FullAnalysis"

cd scripts
root <<EOF
.Analysis_COIN.C($InDATAFilename,$OutDATAFilename)
EOF
root <<EOF
.Analysis_COIN.C($InDUMMYFilename,$OutDUMMYFilename)
EOF

python3 HeepCoin.py OutDATAFilename OutDUMMYFilename InSIMCFilename OutFullAnalysisFilename
