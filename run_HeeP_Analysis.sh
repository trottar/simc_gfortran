#! /bin/bash

while getopts 'ha' flag; do
    case "${flag}" in
        h) 
        echo "---------------------------------------------------"
        echo "./run_HeeP_Analysis.sh -{flags} {kinematic setting}"
        echo "---------------------------------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -a, analyze"
        exit 0
        ;;
        a) a_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

KIN=$2

ANA_DIR="/group/c-kaonlt/USERS/${USER}/simc_gfortran/scripts"

InDATAFilename="Raw_Data_$KIN.root"
InDUMMYFilename="Raw_DummyData_$KIN.root"
InSIMCFilename="Heep_Coin_$KIN.root"
OutDATAFilename="Analysed_Data_$KIN"
OutDUMMYFilename="Analysed_DummyData_$KIN"
OutFullAnalysisFilename="FullAnalysis_$KIN"

cd $ANA_DIR

if [[ $g_flag = "true" ]]; then
    echo
    echo "Analysing data..."
    echo
root -l <<EOF 
.x $ANA_DIR/Analysed_COIN.C("$InDATAFilename","$OutDATAFilename")
EOF
    echo
    echo "Analysing dummy data..."
    echo
root -l <<EOF 
.x $ANA_DIR/Analysed_COIN.C("$InDUMMYFilename","$OutDUMMYFilename")
EOF
fi

python3 HeepCoin.py "${OutDATAFilename}.root" "${OutDUMMYFilename}.root" ${InSIMCFilename} ${OutFullAnalysisFilename}

cd ../
evince "OUTPUTS/${OutFullAnalysisFilename}.pdf"
