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

# Flag definitions (flags: h, a, o, s)
while getopts 'hat' flag; do
    case "${flag}" in
        h) 
        echo "--------------------------------------------------------------"
        echo "./set_ProdBin.sh -{flags} {variable arguments, see help}"
	echo
        echo "Description: Plots data vs simc"
        echo "--------------------------------------------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -a, analyze"	
        echo "    -t, set t-bin (!!!required for script!!!)"
	echo "        EPSILON=arg1, Q2=arg2, W=arg3, EvtsPerBinRange=arg4"
        exit 0
        ;;
	a) a_flag='true' ;;
        t) t_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

# When any flag is used then the user input changes argument order
if [[ $t_flag = "true" ]]; then
    echo $1 $2 $3 $4 $5
    EPSILON=$2
    Q2=$3
    W=$4
    EvtsPerBinRange=$5
    echo "Epsilon must be - high - low - Case Sensitive!"
    echo "Q2 must be one of - [5p5 - 4p4 - 3p0 - 2p1 - 0p5]"
    echo "W must be one of - [3p02 - 2p74 - 3p14 - 2p32 - 2p95 - 2p40]"
    if [[ -z "$2" || ! "$EPSILON" =~ high|low ]]; then # Check the 1st argument was provided and that it's one of the valid options
	echo ""
	echo "I need a valid epsilon..."
	while true; do
	    echo ""
	    read -p "Epsilon must be - high - low - Case Sensitive! - or press ctrl-c to exit : " EPSILON
	    case $EPSILON in
		'');; # If blank, prompt again
		'high'|'low') break;; # If a valid option, break the loop and continue
	    esac
	done
    fi
    if [[ -z "$3" || ! "$Q2" =~ 5p5|4p4|3p0|2p1|0p5 ]]; then # Check the 2nd argument was provided and that it's one of the valid options
	echo ""
	echo "I need a valid Q2..."
	while true; do
	    echo ""
	    read -p "Q2 must be one of - [5p5 - 4p4 - 3p0 - 2p1 - 0p5] - or press ctrl-c to exit : " Q2
	    case $Q2 in
		'');; # If blank, prompt again
		'5p5'|'4p4'|'3p0'|'2p1'|'0p5') break;; # If a valid option, break the loop and continue
	    esac
	done
    fi
    if [[ -z "$4" || ! "$W" =~ 3p02|2p74|3p14|2p32|2p95|2p40 ]]; then # Check the 3rd argument was provided and that it's one of the valid options
	echo ""
	echo "I need a valid W..."
	while true; do
	    echo ""
	    read -p "W must be one of - [3p02 - 2p74 - 3p14 - 2p32 - 2p95 - 2p40] - or press ctrl-c to exit : " W
	    case $W in
		'');; # If blank, prompt again
		'3p02'|'2p74'|'3p14'|'2p32'|'2p95'|'2p40') break;; # If a valid option, break the loop and continue
	    esac
	done
    fi
    if [[ $5 -eq "" ]]; then
	echo "No number of events per nominal bin range given, assuming 50k..." 
	EvtsPerBinRange=50000	
    fi
fi

grab_runs () {
    RunList=$1
    #echo "Reading input file ${RunList}..."
    INPDIR="${REPLAYPATH}/UTIL_BATCH/InputRunLists/KaonLT_2018_2019/${RunList}"
    cd "${SIMCPATH}/scripts"
    RunNumArr=$(python3 getRunNumbers.py $INPDIR)
    echo $RunNumArr
}

# Run numbers for left, right, and, center settings
PHI=("RIGHT" "LEFT" "CENTER")
for i in "${PHIVAL[@]}"
do
    if [[ $Q2 = "5p5" && $W = "3p02" ]]; then
	if [[ $PHI = "RIGHT" ]]; then
	    file_right="Prod_Test"
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Prod_Test )"             # RIGHT, Q2=5p5, W=3p02, high eps
	elif [[ $PHI = "LEFT" ]]; then
	    file_left="Prod_Test"
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Prod_Test )"		 # LEFT, Q2=5p5, W=3p02, high eps
	elif [[ $PHI = "CENTER" ]]; then
	    file_center="Prod_Test"
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Prod_Test )"		 # CENTER, Q2=5p5, W=3p02, high eps
	fi
	KIN="Prod_Test"	
    fi    
    #    if [[ $Q2 = "5p5" && $W = "3p02" ]]; then
    #	if [[ $PHI = "RIGHT" ]]; then
    #	    file_right="Q5p5W3p02right_${EPSILON}e"
    #	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q5p5W3p02right_${EPSILON}e )"             # RIGHT, Q2=5p5, W=3p02, high eps
    #	elif [[ $PHI = "LEFT" ]]; then
    #	    file_left="Q5p5W3p02left_${EPSILON}e"
    #	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q5p5W3p02left_${EPSILON}e )"		 # LEFT, Q2=5p5, W=3p02, high eps
    #	elif [[ $PHI = "CENTER" ]]; then
    #	    file_center="Q5p5W3p02center_${EPSILON}e"
    #	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q5p5W3p02center_${EPSILON}e )"		 # CENTER, Q2=5p5, W=3p02, high eps
    #	fi
    #	KIN="Q5p5W3p02_${EPSILON}e"	
    #    fi
    if [[ $Q2 = "4p4" && $W = "2p74" ]]; then
	if [[ $PHI = "RIGHT" ]]; then
	    file_right="Q4p4W2p74right_${EPSILON}e"
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q4p4W2p74right_${EPSILON}e )"		 # RIGHT, Q2=4p4, W=2p74, high eps
	elif [[ $PHI = "LEFT" ]]; then
	    file_left="Q4p4W2p74left_${EPSILON}e"
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q4p4W2p74left_${EPSILON}e )"		 # LEFT, Q2=4p4, W=2p74, high eps
	elif [[ $PHI = "CENTER" ]]; then
	    file_center="Q4p4W2p74center_${EPSILON}e"
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q4p4W2p74center_${EPSILON}e )"		 # CENTER, Q2=4p4, W=2p74, high eps
	fi
	KIN="Q4p4W2p74_${EPSILON}e"	
    fi
    if [[ $Q2 = "3p0" && $W = "3p14" ]]; then
	if [[ $PHI = "RIGHT" ]]; then
	    file_right="Q3W3p14right_${EPSILON}e"
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q3W3p14right_${EPSILON}e )"		 # RIGHT, Q2=3p0, W=3p14, high eps
	elif [[ $PHI = "LEFT" ]]; then
	    file_left="Q3W3p14left_${EPSILON}e"
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q3W3p14left_${EPSILON}e )"		 # LEFT, Q2=3p0, W=3p14, high eps
	elif [[ $PHI = "CENTER" ]]; then
	    file_center="Q3W3p14center_${EPSILON}e"
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q3W3p14center_${EPSILON}e )"		 # CENTER, Q2=3p0, W=3p14, high eps
	fi
	KIN="Q3W3p14_${EPSILON}e"	
    fi
    if [[ $Q2 = "3p0" && $W = "2p32" ]]; then
	if [[ $PHI = "RIGHT" ]]; then
	    file_right="Q3W2p32right_${EPSILON}e"
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q3W2p32right_${EPSILON}e )"		 # RIGHT, Q2=3p0, W=2p32, high eps
	elif [[ $PHI = "LEFT" ]]; then
	    file_left="Q3W2p32left_${EPSILON}e"
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q3W2p32left_${EPSILON}e )"		 # LEFT, Q2=3p0, W=2p32, high eps
	elif [[ $PHI = "CENTER" ]]; then
	    file_center="Q3W2p32center_${EPSILON}e"
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q3W2p32center_${EPSILON}e )"		 # CENTER, Q2=3p0, W=2p32, high eps
	fi
	KIN="Q3W2p32_${EPSILON}e"	
    fi
    if [[ $Q2 = "2p1" && $W = "2p95" ]]; then
	if [[ $PHI = "RIGHT" ]]; then
	    file_right="Q2p115W2p95right_${EPSILON}e"
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q2p115W2p95right_${EPSILON}e )"		 # RIGHT, Q2=2p1, W=2p95, high eps
	elif [[ $PHI = "LEFT" ]]; then
	    file_left="Q2p115W2p95left_${EPSILON}e"
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q2p115W2p95left_${EPSILON}e )"		 # LEFT, Q2=2p1, W=2p95, high eps
	elif [[ $PHI = "CENTER" ]]; then
	    file_center="Q2p115W2p95center_${EPSILON}e"
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q2p115W2p95center_${EPSILON}e )"		 # CENTER, Q2=2p1, W=2p95, high eps
	fi
	KIN="Q2p115W2p95_${EPSILON}e"	
    fi        
    if [[ $Q2 = "0p5" && $W = "2p40" ]]; then
	if [[ $PHI = "RIGHT" ]]; then
	    file_right="Q0p5W2p40right_${EPSILON}e"
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q0p5W2p40right_${EPSILON}e )"		 # RIGHT, Q2=0p5, W=2p40, high eps
	elif [[ $PHI = "LEFT" ]]; then
	    file_left="Q0p5W2p40left_${EPSILON}e"
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q0p5W2p40left_${EPSILON}e )"		 # LEFT, Q2=0p5, W=2p40, high eps
	elif [[ $PHI = "CENTER" ]]; then
	    file_center="Q0p5W2p40center_${EPSILON}e"
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q0p5W2p40center_${EPSILON}e )"		 # CENTER, Q2=0p5, W=2p40, high eps
	fi
	KIN="Q0p5W2p40_${EPSILON}e"	
    fi    
done

InDATAFilename="Raw_Data_${KIN}.root"
OutDATAFilename="Analysed_Data_${KIN}"
OutFullAnalysisFilename="FullAnalysis_${KIN}"

# When analysis flag is used then the analysis script (Analysed_Prod.py)
# will create a new root file per run number which are combined using hadd
if [[ $a_flag = "true" ]]; then

    if [ ${#data_right[@]} -eq 0 ]; then
	cd "${SIMCPATH}/scripts/Prod"
	echo
	echo "Analysing right data..."
	echo
	for i in "${data_right[@]}"
	do
	    echo
	    echo "-----------------------------"
	    echo "Analysing right data run $i..."
	    echo "-----------------------------"
	    echo
	    python3 Analysed_Prod.py "$i" | tee ../../log/Analysed_Prod_$i.log
	    #root -l <<EOF 
	    #.x $SIMCPATH/Analysed_Prod.C("$InDATAFilename","$OutDATAFilename")
	    #EOF
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/${ANATYPE}"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}.root *_-1_Raw_Data.root
	for i in *_-1_Raw_Data.root; do mv -- "$i" "${i%_-1_Raw_Data.root}_-1_Raw_Right_Target.root"; done
    fi

    if [ ${#data_left[@]} -eq 0 ]; then
	cd "${SIMCPATH}/scripts/Prod"
	echo
	echo "Analysing left data..."
	echo
	for i in "${data_left[@]}"
	do
	    echo
	    echo "-----------------------------"
	    echo "Analysing left data run $i..."
	    echo "-----------------------------"
	    echo
	    python3 Analysed_Prod.py "$i" | tee ../../log/Analysed_Prod_$i.log
	    #root -l <<EOF 
	    #.x $SIMCPATH/Analysed_Prod.C("$InDATAFilename","$OutDATAFilename")
	    #EOF
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/${ANATYPE}"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}.root *_-1_Raw_Data.root
	for i in *_-1_Raw_Data.root; do mv -- "$i" "${i%_-1_Raw_Data.root}_-1_Raw_Left_Target.root"; done
    fi

    if [ ${#data_center[@]} -eq 0 ]; then
	cd "${SIMCPATH}/scripts/Prod"
	echo
	echo "Analysing center data..."
	echo
	for i in "${data_center[@]}"
	do
	    echo
	    echo "-----------------------------"
	    echo "Analysing center data run $i..."
	    echo "-----------------------------"
	    echo
	    python3 Analysed_Prod.py "$i" | tee ../../log/Analysed_Prod_$i.log
	    #root -l <<EOF 
	    #.x $SIMCPATH/Analysed_Prod.C("$InDATAFilename","$OutDATAFilename")
	    #EOF
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/${ANATYPE}"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}.root *_-1_Raw_Data.root
	for i in *_-1_Raw_Data.root; do mv -- "$i" "${i%_-1_Raw_Data.root}_-1_Raw_Center_Target.root"; done
    fi    
    
fi

cd "${SIMCPATH}/scripts"

# Finally, run the plotting script
cd "${SIMCPATH}/scripts/Prod"
#python3 HeepCoin.py ${KIN} "${OutDATAFilename}.root" $DataChargeSum "${DataEffVal[*]}" "${DataRunNum[*]}" "${OutDUMMYFilename}.root" $DummyChargeSum "${DummyEffVal[*]}" "${DummyRunNum[*]}" ${InSIMCFilename} ${OutFullAnalysisFilename} ${EffData}

cd "${SIMCPATH}"
#evince "OUTPUT/Analysis/${ANATYPE}/${OutFullAnalysisFilename}.pdf"
