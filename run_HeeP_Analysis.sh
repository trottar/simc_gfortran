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

if [[ $KIN = "10p6" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863)
    declare -a dummydata=(4864)
elif [[ $KIN = "8p2" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863)
    declare -a dummydata=(4864)
else
    echo "Invalid kinematic setting, ${KIN}"
    exit 1
fi

if [[ $a_flag = "true" ]]; then
    
    cd "${ANA_DIR}/scripts"
    echo
    echo "Analysing data..."
    echo
    
    for i in "${data[@]}"
    do
	echo
	echo "-----------------------------"
	echo "Analysing data run $i..."
	echo "-----------------------------"
	echo
	python3 Analysed_COIN.py "$i"
	#root -l <<EOF 
	#.x $ANA_DIR/Analysed_COIN.C("$InDATAFilename","$OutDATAFilename")
	#EOF
    done
    cd "${ANA_DIR}/OUTPUTS"
    echo
    echo "Combining root files..."  
    hadd -f Analysed_Data_${KIN}.root *_-1_Raw_Data.root
    rm -f *_-1_Raw_Data.root
    
    cd "${ANA_DIR}/scripts"    
    echo
    echo "Analysing dummy data..."
    echo
    
    for i in "${dummydata[@]}"
    do
	echo
	echo "-----------------------------------"
	echo "Analysing dummy data run $i..."
	echo "-----------------------------------"
	echo
	python3 Analysed_COIN.py "$i"
	#root -l <<EOF 
	#.x $ANA_DIR/Analysed_COIN.C("$InDUMMYFilename","$OutDUMMYFilename")
	#EOF
    done
    cd "${ANA_DIR}/OUTPUTS"
    echo
    echo "Combining root files..."
    hadd -f Analysed_DummyData_${KIN}.root *_-1_Raw_Data.root
    rm -f *_-1_Raw_Data.root
fi

cd "${ANA_DIR}/scripts"

DataChargeVal=()
echo
echo "Calculating data total charge..."
for i in "${data[@]}"
do
    DataChargeVal+=($(python3 findcharge.py replay_coin_heep "$i" -1))
    echo "Run:$i ${DataChargeVal} mC"
done
DataChargeSum=$(IFS=+; echo "$((${DataChargeVal[*]}))") # Only works for integers
echo $DataChargeSum

DummyChargeVal=()
echo
echo "Calculating dummy total charge..."
for i in "${dummydata[@]}"
do
    DummyChargeVal+=($(python3 findcharge.py replay_coin_heep "$i" -1))
    echo "Run:$i ${DummyChargeVal} mC"
done
DummyChargeSum=$(IFS=+; echo "$((${DummyChargeVal[*]}))") # Only works for integers
echo $DummyChargeSum

python3 HeepCoin.py ${KIN} "${OutDATAFilename}.root" $DataChargeSum "${OutDUMMYFilename}.root" $DummyChargeSum ${InSIMCFilename} ${OutFullAnalysisFilename}

cd ../
evince "OUTPUTS/${OutFullAnalysisFilename}.pdf"
