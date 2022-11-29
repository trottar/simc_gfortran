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
	echo "        NUMBINS=arg1"
        exit 0
        ;;
        a) t_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

# When any flag is used then the user input changes argument order
if [[ $t_flag = "true" ]]; then
    EPS=$1
    Q2=$2
    W=$3
    NUMBINS=$4
    echo "Epsilon must be - high - low - Case Sensitive!"
    echo "Q2 must be one of - 5.5 - 4.4 - 3.0 - 2.1 - 0.5"
    echo "W must be one of - 3.02 - 2.74 - 3.14 - 2.32 - 2.95 - 2.40"
    if [[ -z "$1" || ! "$EPSILON" =~ high|low ]]; then # Check the 2nd argument was provided and that it's one of the valid options
    echo ""
    echo "I need a valid epsilon..."
    while true; do
	echo ""
	read -p "Epsilon must be - high - low - Case Sensitive! - or press ctrl-c to exit : " EPSILON
	case $EPSILON in
	    '');; # If blank, prompt again
	    'high'|'low') break;; 
	    # If a valid option, break the loop and continue
	esac
    done
    fi
    if [[ -z "$2" || ! "$Q2" =~ 4.4|3.0|2.1|0.5 ]]; then # Check the 2nd argument was provided and that it's one of the valid options
    echo ""
    echo "I need a valid Q2..."
    while true; do
	echo ""
	read -p "Q2 must be one of - 5.5 - 4.4 - 3.0 - 2.1 - 0.5 - or press ctrl-c to exit : " Q2
	case $Q2 in
	    '');; # If blank, prompt again
	    '4.4'|'3.0'|'2.1'|'0.5') break;; 
	    # If a valid option, break the loop and continue
	esac
    done
    fi
    if [[ -z "$3" || ! "$W" =~ 3.02|2.74|3.14|2.32|2.95|2.40 ]]; then # Check the 2nd argument was provided and that it's one of the valid options
    echo ""
    echo "I need a valid W..."
    while true; do
	echo ""
	read -p "W must be one of - 3.02 - 2.74 - 3.14 - 2.32 - 2.95 - 2.40 - or press ctrl-c to exit : " W
	case $W in
	    '');; # If blank, prompt again
	    '3.02'|'2.74'|'3.14'|'2.32'|'2.95'|'2.40') break;; 
	    # If a valid option, break the loop and continue
	esac
    done
    fi
fi

grab_input () {
    if [[ $1 = "" ]]; then
	RunList="Q4p4W2p74center_highe"
    else
	RunList="Q4p4W2p74center_highe"
    fi
    #echo "Reading input file ${RunList}..."
    INPDIR="${REPLAYPATH}/UTIL_BATCH/InputRunLists/KaonLT_2018_2019/${RunList}"
    cd "${SIMCPATH}/scripts"
    RunNumArr=$(python3 getRunNumbers.py $INPDIR)
    echo $RunNumArr
}

grab_input

IFS=', ' read -r -a array <<< "$( grab_input )"

for i in "${array[@]}"
do
    echo
    echo "-----------------------------"
    echo "Analysing data run $i..."
    echo "-----------------------------"
    echo   
done

# Run numbers for left, right, and, center settings
PHI=("RIGHT" "LEFT" "CENTER")
for i in "${PHIVAL[@]}"
do
    if [[ $EPSILON = "high" ]]; then
	if [[ $Q2 = "5.5" && $W = "3.02" ]]; then
	    if [[ $PHI = "RIGHT" ]]; then
		declare -a data_right=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # RIGHT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "LEFT" ]]; then
		declare -a data_left=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # LEFT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "CENTER" ]]; then
		declare -a data_center=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # CENTER, Q2=5.5, W=3.02, x=0.40, high eps	
	    fi
	fi
	if [[ $Q2 = "4.4" && $W = "2.74" ]]; then
	    if [[ $PHI = "RIGHT" ]]; then
		declare -a data_right=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # RIGHT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "LEFT" ]]; then
		declare -a data_left=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # LEFT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "CENTER" ]]; then
		declare -a data_center=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # CENTER, Q2=5.5, W=3.02, x=0.40, high eps	
	    fi
	fi
	if [[ $Q2 = "3.0" && $W = "3.14" ]]; then
	    if [[ $PHI = "RIGHT" ]]; then
		declare -a data_right=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # RIGHT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "LEFT" ]]; then
		declare -a data_left=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # LEFT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "CENTER" ]]; then
		declare -a data_center=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # CENTER, Q2=5.5, W=3.02, x=0.40, high eps	
	    fi
	fi
	if [[ $Q2 = "3.0" && $W = "2.32" ]]; then
	    if [[ $PHI = "RIGHT" ]]; then
		declare -a data_right=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # RIGHT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "LEFT" ]]; then
		declare -a data_left=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # LEFT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "CENTER" ]]; then
		declare -a data_center=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # CENTER, Q2=5.5, W=3.02, x=0.40, high eps	
	    fi
	fi
	if [[ $Q2 = "0.5" && $W = "2.40" ]]; then
	    if [[ $PHI = "RIGHT" ]]; then
		declare -a data_right=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # RIGHT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "LEFT" ]]; then
		declare -a data_left=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # LEFT, Q2=5.5, W=3.02, x=0.40, high eps
	    elif [[ $PHI = "CENTER" ]]; then
		declare -a data_center=(4827 4828 4855 4856 4857 4858 4859 4860 4862 4863) # CENTER, Q2=5.5, W=3.02, x=0.40, high eps	
	    fi
	fi
    fi
done
