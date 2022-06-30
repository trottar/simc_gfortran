#! /bin/bash

while getopts 'hao' flag; do
    case "${flag}" in
        h) 
        echo "---------------------------------------------------"
        echo "./run_HeeP_Analysis.sh -{flags} {kinematic setting}"
        echo "---------------------------------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -a, analyze"
        echo "    -o, offset"
        exit 0
        ;;
        a) a_flag='true' ;;
        o) o_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

if [[ $a_flag = "true" || $o_flag = "true" ]]; then
    KIN=$2
else
    KIN=$1
fi

# Runs script in the ltsep python package that grabs current path enviroment
if [[ ${HOSTNAME} = *"cdaq"* ]]; then
    PATHFILE_INFO=`python3 /home/cdaq/pionLT-2021/hallc_replay_lt/UTIL_PION/bin/python/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
elif [[ ${HOSTNAME} = *"farm"* ]]; then
    PATHFILE_INFO=`python3 /u/home/${USER}/.local/lib/python3.4/site-packages/ltsep/scripts/getPathDict.py $PWD` # The output of this python script is just a comma separated string
fi

# Split the string we get to individual variables, easier for printing and use later
VOLATILEPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f1` # Cut the string on , delimitter, select field (f) 1, set variable to output of command
ANALYSISPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f2`
HCANAPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f3`
REPLAYPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f4`
UTILPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f5`
PACKAGEPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f6`
OUTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f7`
ROOTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f8`
REPORTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f9`
CUTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f10`
PARAMPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f11`
SCRIPTPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f12`
ANATYPE=`echo ${PATHFILE_INFO} | cut -d ','  -f13`
USER=`echo ${PATHFILE_INFO} | cut -d ','  -f14`
HOST=`echo ${PATHFILE_INFO} | cut -d ','  -f15`
SIMCPATH=`echo ${PATHFILE_INFO} | cut -d ','  -f16`

InDATAFilename="Raw_Data_${KIN}.root"
InDUMMYFilename="Raw_DummyData_${KIN}.root"
if [[ $o_flag = "true" ]]; then
    InSIMCFilename="Heep_Coin_${KIN}_Offset.root"
    OutFullAnalysisFilename="FullAnalysis_${KIN}_Offset"
else
    InSIMCFilename="Heep_Coin_${KIN}.root"
    OutFullAnalysisFilename="FullAnalysis_${KIN}"
fi
OutDATAFilename="Analysed_Data_${KIN}"
OutDUMMYFilename="Analysed_DummyData_${KIN}"

if [[ $KIN = "10p6" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # All heep coin 10p6 runs
    #declare -a data=(4827) # Just one test run
    declare -a dummydata=(4864)
elif [[ $KIN = "8p2" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863)
    declare -a dummydata=(4864)
else
    echo "Invalid kinematic setting, ${KIN}"
    exit 1
fi

if [[ $a_flag = "true" ]]; then
    
    cd "${SIMCPATH}/scripts/COIN"
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
	#.x $SIMCPATH/Analysed_COIN.C("$InDATAFilename","$OutDATAFilename")
	#EOF
    done
    cd "${SIMCPATH}/OUTPUT/Analysis/HeeP"
    echo
    echo "Combining root files..."  
    hadd -f Analysed_Data_${KIN}.root *_-1_Raw_Data.root
    rm -f *_-1_Raw_Data.root
    
    cd "${SIMCPATH}/scripts/COIN"    
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
	#.x $SIMCPATH/Analysed_COIN.C("$InDUMMYFilename","$OutDUMMYFilename")
	#EOF
    done
    cd "${SIMCPATH}/OUTPUT/Analysis/HeeP"
    echo
    echo "Combining root files..."
    hadd -f Analysed_DummyData_${KIN}.root *_-1_Raw_Data.root
    rm -f *_-1_Raw_Data.root
fi

cd "${SIMCPATH}/scripts"

DataChargeVal=()
DataEffVal=()
echo
echo "Calculating data total charge..."
for i in "${data[@]}"
do
    DataChargeVal+=($(python3 findcharge.py replay_coin_heep "$i" -1))
    DataEffVal+=($(python3 calculate_efficiency.py "$i"))
    #echo "${DataChargeVal[@]} mC"
done
DataChargeSum=$(IFS=+; echo "$((${DataChargeVal[*]}))") # Only works for integers
echo "${DataChargeSum} uC"

DummyChargeVal=()
DummyEffVal=()
echo
echo "Calculating dummy total charge..."
for i in "${dummydata[@]}"
do
    DummyChargeVal+=($(python3 findcharge.py replay_coin_heep "$i" -1))
    DummyEffVal+=($(python3 calculate_efficiency.py "$i"))
    #echo "${DummyChargeVal[@]} mC"
done
DummyChargeSum=$(IFS=+; echo "$((${DummyChargeVal[*]}))") # Only works for integers
echo "${DummyChargeSum} uC"

cd "${SIMCPATH}/scripts/COIN"
python3 HeepCoin.py ${KIN} "${OutDATAFilename}.root" $DataChargeSum "${DataEffVal[*]}" "${OutDUMMYFilename}.root" $DummyChargeSum "${DummyEffVal[*]}" ${InSIMCFilename} ${OutFullAnalysisFilename}

cd "${SIMCPATH}"
evince "OUTPUT/Analysis/HeeP/${OutFullAnalysisFilename}.pdf"
