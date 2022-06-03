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

if [[ $a_flag = "true" ]]; then
    KIN=$2
else
    KIN=$1
fi

ANA_DIR="/group/c-kaonlt/USERS/${USER}/simc_gfortran"

InDATAFilename="Raw_Data_$KIN.root"
InDUMMYFilename="Raw_DummyData_$KIN.root"
InSIMCFilename="Heep_Coin_$KIN.root"
OutDATAFilename="Analysed_Data_$KIN"
OutDUMMYFilename="Analysed_DummyData_$KIN"
OutFullAnalysisFilename="FullAnalysis_$KIN"

declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863)
declare -a dummydata=(4864)

cd "${ANA_DIR}/scripts"

if [[ $a_flag = "true" ]]; then
    echo
    echo "Analysing data..."
    echo
    
    for i in "${data[@]}"
    do
	echo "Analysing data run $i"
	python3 Analysed_COIN.py "$i"
	#root -l <<EOF 
	#.x $ANA_DIR/Analysed_COIN.C("$InDATAFilename","$OutDATAFilename")
	#EOF
    done
    cd "${ANA_DIR}/OUTPUTS"
    hadd -f Analysed_Data_10p6.root *_-1_Raw_Data.root
    rm -rf *_-1_Raw_Data.root
    
    cd "${ANA_DIR}/scripts"    
    echo
    echo "Analysing dummy data..."
    echo
    
    for i in "${dummydata[@]}"
    do
	echo "Analysing dummy data run $i"
	python3 Analysed_COIN.py "$i"
	#root -l <<EOF 
	#.x $ANA_DIR/Analysed_COIN.C("$InDUMMYFilename","$OutDUMMYFilename")
	#EOF
    done
    cd "${ANA_DIR}/OUTPUTS"
    hadd -f Analysed_Data_10p6.root *_-1_Raw_Data.root
    rm -rf *_-1_Raw_Data.root
fi

python3 HeepCoin.py ${KIN} "${OutDATAFilename}.root" "${OutDUMMYFilename}.root" ${InSIMCFilename} ${OutFullAnalysisFilename}

cd ../
evince "OUTPUTS/${OutFullAnalysisFilename}.pdf"
