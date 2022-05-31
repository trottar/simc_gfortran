#! /bin/bash

KIN=$1

ANA_DIR="/group/c-kaonlt/USERS/${USER}/simc_gfortran/scripts/"

InDATAFilename="${KIN}_Raw_Data.root"
InDUMMYFilename="${KIN}_Raw_DummyData.root"
InSIMCFilename="Heep_Coin_${KIN}.root"
OutDATAFilename="${KIN}_Analysed_Data"
OutDUMMYFilename="${KIN}_Analysed_DummyData"
OutFullAnalysisFilename="${KIN}_FullAnalysis"

cd $ANA_DIR

root -l <<EOF
.x ${ANA_DIR}Analysis_COIN.C($InDATAFilename,$OutDATAFilename)
EOF
root -l <<EOF
.x ${ANA_DIR}Analysis_COIN.C($InDUMMYFilename,$OutDUMMYFilename)
EOF

python3 HeepCoin.py OutDATAFilename OutDUMMYFilename InSIMCFilename OutFullAnalysisFilename
