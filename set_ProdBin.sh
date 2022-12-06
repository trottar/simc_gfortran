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
while getopts 'hdat' flag; do
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
	echo "    -d, debug"	
        echo "    -a, analyze"	
        echo "    -t, set t-bin (!!!required for script!!!)"
	echo "        EPSILON=arg1, Q2=arg2, W=arg3, NumtBins=arg4"	
        exit 0
        ;;
	d) d_flag='true' ;;
	a) a_flag='true' ;;
        t) t_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

# When any flag is used then the user input changes argument order
if [[ $t_flag = "true" ]]; then

    EPSILON=$2
    Q2=$3
    W=$4
    NumtBins=$5
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
	NumtBins=5
    fi
elif [[ $d_flag = "true" ]]; then
    echo
    echo "-----------------------------"
    echo
    echo "!!!!!!! DEBUG TESTING !!!!!!!"
    echo
    echo "-----------------------------"
    echo
    NumtBins=5
fi

##############
# HARD CODED #
##############
# Efficiency csv file
EffData="coin_production_Prod_efficiency_data_2022_12_05.csv"

# Function that calls python script to grab run numbers
grab_runs () {
    RunList=$1
    INPDIR="${REPLAYPATH}/UTIL_BATCH/InputRunLists/KaonLT_2018_2019/${RunList}"
    cd "${SIMCPATH}/scripts"
    RunNumArr=$(python3 getRunNumbers.py $INPDIR)
    echo $RunNumArr
}

echo
echo "---------------------------------------------------------"
echo
echo "Beginning analysis for ${Q2}, ${W}, ${EPSILON} setting..."
echo
echo "---------------------------------------------------------"
echo

# Get run numbers for left, right, and, center settings
declare -a PHI=("RIGHT" "LEFT" "CENTER")
for i in "${PHI[@]}"
do
    if [[ $d_flag = "true" ]]; then
	if [[ $i = "RIGHT" ]]; then
	    file_right="Prod_Test"
	    echo "Reading in run numbers for right file ${file_right}..."
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Prod_Test )"             # RIGHT, Q2=5p5, W=3p02
	    echo "Run Numbers: [${data_right[@]}]"
	    echo
	elif [[ $i = "LEFT" ]]; then
	    file_left="Prod_Test"
	    echo "Reading in run numbers for left file ${file_left}..."
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Prod_Test )"		 # LEFT, Q2=5p5, W=3p02
	    echo "Run Numbers: [${data_left[@]}]"
	    echo	    
	elif [[ $i = "CENTER" ]]; then
	    file_center="Prod_Test"
	    echo "Reading in run numbers for center file ${file_center}..."
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Prod_Test )"		 # CENTER, Q2=5p5, W=3p02
	    echo "Run Numbers: [${data_center[@]}]"
	    echo
	fi
	KIN="Prod_Test"	
    fi    
    if [[ $Q2 = "5p5" && $W = "3p02" ]]; then
	if [[ $i = "RIGHT" ]]; then
	    # Define run list based off kinematics selected
	    file_right="Q5p5W3p02right_${EPSILON}e"
	    echo "Reading in run numbers for right file ${file_right}..."
	    # Converts python output to bash array
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q5p5W3p02right_${EPSILON}e )"             # RIGHT, Q2=5p5, W=3p02
	    echo "Run Numbers: [${data_right[@]}]"
	    echo	    
	elif [[ $i = "LEFT" ]]; then
	    file_left="Q5p5W3p02left_${EPSILON}e"
	    echo "Reading in run numbers for left file ${file_left}..."
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q5p5W3p02left_${EPSILON}e )"		 # LEFT, Q2=5p5, W=3p02
	    echo "Run Numbers: [${data_left[@]}]"
	    echo	    
	elif [[ $i = "CENTER" ]]; then
	    file_center="Q5p5W3p02center_${EPSILON}e"
	    echo "Reading in run numbers for center file ${file_center}..."
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q5p5W3p02center_${EPSILON}e )"		 # CENTER, Q2=5p5, W=3p02
	    echo "Run Numbers: [${data_center[@]}]"
	    echo	    
	fi
	KIN="Q5p5W3p02_${EPSILON}e"
    fi
    if [[ $Q2 = "4p4" && $W = "2p74" ]]; then
	if [[ $i = "RIGHT" ]]; then
	    file_right="Q4p4W2p74right_${EPSILON}e"
	    echo "Reading in run numbers for right file ${file_right}..."
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q4p4W2p74right_${EPSILON}e )"		 # RIGHT, Q2=4p4, W=2p74
	    echo "Run Numbers: [${data_right[@]}]"
	    echo	    
	elif [[ $i = "LEFT" ]]; then
	    file_left="Q4p4W2p74left_${EPSILON}e"
	    echo "Reading in run numbers for left file ${file_left}..."
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q4p4W2p74left_${EPSILON}e )"		 # LEFT, Q2=4p4, W=2p74
	    echo "Run Numbers: [${data_left[@]}]"
	    echo	    	    
	elif [[ $i = "CENTER" ]]; then
	    file_center="Q4p4W2p74center_${EPSILON}e"
	    echo "Reading in run numbers for center file ${file_center}..."
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q4p4W2p74center_${EPSILON}e )"		 # CENTER, Q2=4p4, W=2p74
	    echo "Run Numbers: [${data_center[@]}]"
	    echo	    	    	    
	fi
	KIN="Q4p4W2p74_${EPSILON}e"	
    fi
    if [[ $Q2 = "3p0" && $W = "3p14" ]]; then
	if [[ $i = "RIGHT" ]]; then
	    file_right="Q3W3p14right_${EPSILON}e"
	    echo "Reading in run numbers for right file ${file_right}..."
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q3W3p14right_${EPSILON}e )"		 # RIGHT, Q2=3p0, W=3p14
	    echo "Run Numbers: [${data_right[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "LEFT" ]]; then
	    file_left="Q3W3p14left_${EPSILON}e"
	    echo "Reading in run numbers for left file ${file_left}..."
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q3W3p14left_${EPSILON}e )"		 # LEFT, Q2=3p0, W=3p14
	    echo "Run Numbers: [${data_left[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "CENTER" ]]; then
	    file_center="Q3W3p14center_${EPSILON}e"
	    echo "Reading in run numbers for center file ${file_center}..."
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q3W3p14center_${EPSILON}e )"		 # CENTER, Q2=3p0, W=3p14
	    echo "Run Numbers: [${data_center[@]}]"
	    echo	    	    	    	    
	fi
	KIN="Q3W3p14_${EPSILON}e"	
    fi
    if [[ $Q2 = "3p0" && $W = "2p32" ]]; then
	if [[ $i = "RIGHT" ]]; then
	    file_right="Q3W2p32right_${EPSILON}e"
	    echo "Reading in run numbers for right file ${file_right}..."
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q3W2p32right_${EPSILON}e )"		 # RIGHT, Q2=3p0, W=2p32
	    echo "Run Numbers: [${data_right[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "LEFT" ]]; then
	    file_left="Q3W2p32left_${EPSILON}e"
	    echo "Reading in run numbers for left file ${file_left}..."
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q3W2p32left_${EPSILON}e )"		 # LEFT, Q2=3p0, W=2p32
	    echo "Run Numbers: [${data_left[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "CENTER" ]]; then
	    file_center="Q3W2p32center_${EPSILON}e"
	    echo "Reading in run numbers for center file ${file_center}..."
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q3W2p32center_${EPSILON}e )"		 # CENTER, Q2=3p0, W=2p32
	    echo "Run Numbers: [${data_center[@]}]"
	    echo	    	    	    	    
	fi
	KIN="Q3W2p32_${EPSILON}e"	
    fi
    if [[ $Q2 = "2p1" && $W = "2p95" ]]; then
	if [[ $i = "RIGHT" ]]; then
	    file_right="Q2p115W2p95right_${EPSILON}e"
	    echo "Reading in run numbers for right file ${file_right}..."
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q2p115W2p95right_${EPSILON}e )"		 # RIGHT, Q2=2p1, W=2p95
	    echo "Run Numbers: [${data_right[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "LEFT" ]]; then
	    file_left="Q2p115W2p95left_${EPSILON}e"
	    echo "Reading in run numbers for left file ${file_left}..."
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q2p115W2p95left_${EPSILON}e )"		 # LEFT, Q2=2p1, W=2p95
	    echo "Run Numbers: [${data_left[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "CENTER" ]]; then
	    file_center="Q2p115W2p95center_${EPSILON}e"
	    echo "Reading in run numbers for center file ${file_center}..."
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q2p115W2p95center_${EPSILON}e )"		 # CENTER, Q2=2p1, W=2p95
	    echo "Run Numbers: [${data_center[@]}]"
	    echo	    	    	    	    
	fi
	KIN="Q2p115W2p95_${EPSILON}e"	
    fi        
    if [[ $Q2 = "0p5" && $W = "2p40" ]]; then
	if [[ $i = "RIGHT" ]]; then
	    file_right="Q0p5W2p40right_${EPSILON}e"
	    echo "Reading in run numbers for right file ${file_right}..."
	    IFS=', ' read -r -a data_right <<< "$( grab_runs Q0p5W2p40right_${EPSILON}e )"		 # RIGHT, Q2=0p5, W=2p40
	    echo "Run Numbers: [${data_right[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "LEFT" ]]; then
	    file_left="Q0p5W2p40left_${EPSILON}e"
	    echo "Reading in run numbers for left file ${file_left}..."
	    IFS=', ' read -r -a data_left <<< "$( grab_runs Q0p5W2p40left_${EPSILON}e )"		 # LEFT, Q2=0p5, W=2p40
	    echo "Run Numbers: [${data_left[@]}]"
	    echo	    	    	    	    
	elif [[ $i = "CENTER" ]]; then
	    file_center="Q0p5W2p40center_${EPSILON}e"
	    echo "Reading in run numbers for center file ${file_center}..."
	    IFS=', ' read -r -a data_center <<< "$( grab_runs Q0p5W2p40center_${EPSILON}e )"		 # CENTER, Q2=0p5, W=2p40
	    echo "Run Numbers: [${data_center[@]}]"
	    echo	    	    	    	    
	fi
	KIN="Q0p5W2p40_${EPSILON}e"	
    fi    
done

# Define input and output file names
InDATAFilename="Raw_Data_${KIN}.root"
OutDATAFilename="Analysed_Data_${KIN}"
OutFullAnalysisFilename="FullAnalysis_${KIN}"

# When analysis flag is used then the analysis script (Analysed_Prod.py)
# will create a new root file per run number which are combined using hadd
if [[ $a_flag = "true" ]]; then

    # Checks that array isn't empty
    if [ ${#data_right[@]} -ne 0 ]; then
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
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/${ANATYPE}LT"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}_Right.root *_-1_Raw_Data.root
	for i in *_-1_Raw_Data.root; do mv -- "$i" "${i%_-1_Raw_Data.root}_-1_Raw_Right_Target.root"; done
    fi

    # Checks that array isn't empty
    if [ ${#data_left[@]} -ne 0 ]; then
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
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/${ANATYPE}LT"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}_Left.root *_-1_Raw_Data.root
	for i in *_-1_Raw_Data.root; do mv -- "$i" "${i%_-1_Raw_Data.root}_-1_Raw_Left_Target.root"; done
    fi
    
    # Checks that array isn't empty
    if [ ${#data_center[@]} -ne 0 ]; then
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
	done
	cd "${SIMCPATH}/OUTPUT/Analysis/${ANATYPE}LT"
	echo
	echo "Combining root files..."  
	hadd -f ${OutDATAFilename}_Center.root *_-1_Raw_Data.root
	for i in *_-1_Raw_Data.root; do mv -- "$i" "${i%_-1_Raw_Data.root}_-1_Raw_Center_Target.root"; done
    fi
    
fi

cd "${SIMCPATH}/scripts"

# Checks that array isn't empty
if [ ${#data_right[@]} -ne 0 ]; then
    DataChargeValRight=()
    DataEffValRight=()
    echo
    echo "Calculating data total effective charge right..."
    for i in "${data_right[@]}"
    do
	# Calculates total efficiency then applies to the charge for each run number
	# to get the effective charge per run and saves as an array
	DataChargeValRight+=($(python3 findEffectiveCharge.py ${EffData} "replay_coin_production" "$i" -1))
	# Grabs the total effiency value per run and saves as an array
	DataEffValRight+=($(python3 getEfficiency.py "$i" ${EffData}))
	#echo "${DataChargeVal[@]} mC"
    done
    #echo ${DataChargeVal[*]}
    # Sums the array to get the total effective charge
    # Note: this must be done as an array! This is why uC is used at this step
    #       and later converted to C
    DataChargeSumRight=$(IFS=+; echo "$((${DataChargeValRight[*]}))") # Only works for integers
    echo "Total Charge Right: ${DataChargeSumRight} uC"
fi

# Checks that array isn't empty
if [ ${#data_left[@]} -ne 0 ]; then
    DataChargeValLeft=()
    DataEffValLeft=()
    echo
    echo "Calculating data total effective charge left..."
    for i in "${data_left[@]}"
    do
	# Calculates total efficiency then applies to the charge for each run number
	# to get the effective charge per run and saves as an array
	DataChargeValLeft+=($(python3 findEffectiveCharge.py ${EffData} "replay_coin_production" "$i" -1))
	# Grabs the total effiency value per run and saves as an array
	DataEffValLeft+=($(python3 getEfficiency.py "$i" ${EffData}))
	#echo "${DataChargeVal[@]} mC"
    done
    #echo ${DataChargeVal[*]}
    # Sums the array to get the total effective charge
    # Note: this must be done as an array! This is why uC is used at this step
    #       and later converted to C
    DataChargeSumLeft=$(IFS=+; echo "$((${DataChargeValLeft[*]}))") # Only works for integers
    echo "Total Charge Left: ${DataChargeSumLeft} uC"
fi

# Checks that array isn't empty
if [ ${#data_center[@]} -ne 0 ]; then
    DataChargeValCenter=()
    DataEffValCenter=()
    echo
    echo "Calculating data total effective charge center..."
    for i in "${data_center[@]}"
    do
	# Calculates total efficiency then applies to the charge for each run number
	# to get the effective charge per run and saves as an array
	echo $i
	DataChargeValCenter+=($(python3 findEffectiveCharge.py ${EffData} "replay_coin_production" "$i" -1))
	# Grabs the total effiency value per run and saves as an array
	DataEffValCenter+=($(python3 getEfficiency.py "$i" ${EffData}))
	#echo "${DataChargeVal[@]} mC"
    done
    #echo ${DataChargeVal[*]}
    # Sums the array to get the total effective charge
    # Note: this must be done as an array! This is why uC is used at this step
    #       and later converted to C
    DataChargeSumCenter=$(IFS=+; echo "$((${DataChargeValCenter[*]}))") # Only works for integers
    echo "Total Charge Center: ${DataChargeSumCenter} uC"
fi

cd "${SIMCPATH}/scripts/Prod/binning"

# Finally, run the plotting script
# Checks that array isn't empty
if [ ${#data_right[@]} -ne 0 && ${#data_left[@]} -ne 0 && ${#data_center[@]} -ne 0 ]; then
    if [[ $t_flag = "true" || $d_flag = "true" ]]; then
    python3 find_tBinRange.py ${KIN} ${OutDATAFilename} ${OutFullAnalysisFilename} ${NumtBins} "${data_right[*]}" "${data_left[*]}" "${data_center[*]}" ${DataChargeSumRight} ${DataChargeSumLeft} ${DataChargeSumCenter} "${DataEffValRight[*]}" "${DataEffValLeft[*]}" "${DataEffValCenter[*]}" ${EffData}
    fi
else
    python3 find_tBinRange.py ${KIN} ${OutDATAFilename} ${OutFullAnalysisFilename} ${NumtBins} "0" "${data_left[*]}" "${data_center[*]}" "0" ${DataChargeSumLeft} ${DataChargeSumCenter} "0" "${DataEffValLeft[*]}" "${DataEffValCenter[*]}" ${EffData}
fi

cd "${SIMCPATH}"
evince "OUTPUT/Analysis/${ANATYPE}LT/${OutFullAnalysisFilename}.pdf"
