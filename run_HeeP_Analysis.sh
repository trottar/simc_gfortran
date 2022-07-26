#! /bin/bash

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

while getopts 'haos' flag; do
    case "${flag}" in
        h) 
        echo "--------------------------------------------------------------"
        echo "./run_HeeP_Analysis.sh -{flags} {variable arguments, see help}"
        echo "--------------------------------------------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -a, analyze"
	echo "        coin -> KIN=arg1"
	echo "        sing -> SPEC=arg1 KIN=arg2 (requires -s flag)"
	echo "    -s, single arm"
	echo "    -o, offset to replay applied"
        exit 0
        ;;
        a) a_flag='true' ;;
        o) o_flag='true' ;;
	s) s_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

if [[ $a_flag = "true" || $o_flag = "true" ]]; then
    KIN=$2
elif [[ $s_flag = "true" ]]; then
    spec=$2
    SPEC=$(echo "$spec" | tr '[:lower:]' '[:upper:]')
    KIN=$3
else
    KIN=$1
fi

if [[ $s_flag = "true" ]]; then
    InDATAFilename="Raw_Data_${SPEC}_${KIN}.root"
    InDUMMYFilename="Raw_DummyData_${SPEC}_${KIN}.root"
    InSIMCFilename="Heep_Coin_${SPEC}_${KIN}.root"
    OutDATAFilename="Analysed_Data_${SPEC}_${KIN}"
    OutDUMMYFilename="Analysed_DummyData_${SPEC}_${KIN}"
    if [[ $o_flag = "true" ]]; then
	OutFullAnalysisFilename="FullAnalysis_Offset_${SPEC}_${KIN}"
    else
	OutFullAnalysisFilename="FullAnalysis_${SPEC}_${KIN}"
    fi
else
    InDATAFilename="Raw_Data_${KIN}.root"
    InDUMMYFilename="Raw_DummyData_${KIN}.root"
    InSIMCFilename="Heep_Coin_${KIN}.root"
    OutDATAFilename="Analysed_Data_${KIN}"
    OutDUMMYFilename="Analysed_DummyData_${KIN}"
    if [[ $o_flag = "true" ]]; then
	OutFullAnalysisFilename="FullAnalysis_Offset_${KIN}"
    else
	OutFullAnalysisFilename="FullAnalysis_${KIN}"
    fi
fi

if [[ $KIN = "10p6" && $s_flag != "true" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # All heep coin 10p6 runs
    #declare -a data=(4827) # Just one test run
    declare -a dummydata=(4864)
elif [[ $KIN = "8p2" && $s_flag != "true" ]]; then
    declare -a data=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863)
    declare -a dummydata=(4864)
elif [[ $KIN = "10p6" && $s_flag = "true" ]]; then
    declare -a data=(4784 4785) # All heep singles 10p6 runs
    declare -a dummydata=(4786)
elif [[ $KIN = "8p2" && $s_flag = "true" ]]; then
    declare -a data=(111)
    declare -a dummydata=(111)    
else
    echo "Invalid kinematic setting, ${KIN}"
    exit 128
fi
