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

while getopts 'hcas' flag; do
    case "${flag}" in
        h) 
        echo "----------------------------------------------------------"
        echo "./set_HeepInput.sh -{flags} {variable arguments, see help}"
        echo "----------------------------------------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -c, compile fortran code (singles only)"
	echo "    -a, run SIMC with new settings"
	echo "        coin -> KIN=arg1"
	echo "        sing -> SPEC=arg1 KIN=arg2 (requires -s flag)"
	echo "    -s, single arm"
        exit 0
        ;;
        c) c_flag='true' ;;
	a) a_flag='true' ;;
	s) s_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

if [[ $s_flag = "true" ]]; then
    ELASFOR="elas_kin"

    cd ${SIMCPATH}/scripts/SING
    if [[ $c_flag = "true" ]]; then
	echo "Compiling ${ELASFOR}.f..."
	eval "gfortran -o  ${ELASFOR} ${ELASFOR}.f"
	spec=$2
	SPEC=$(echo "$spec" | tr '[:lower:]' '[:upper:]')
	KIN=$3
    elif [[ $a_flag = "true" ]]; then
	spec=$2
	SPEC=$(echo "$spec" | tr '[:lower:]' '[:upper:]')
	KIN=$3
    else
	spec=$1
	SPEC=$(echo "$spec" | tr '[:lower:]' '[:upper:]')
	KIN=$2
    fi

    InputSIMC="Heep_${SPEC}_${KIN}"

    cd ${SIMCPATH}/scripts
    SIMCINP=`python3 getSetting.py ${InputSIMC}`

    BEAMINP=`echo ${SIMCINP} | cut -d ',' -f1`
    THETAINP=`echo ${SIMCINP} | cut -d ',' -f2`

    cd ${SIMCPATH}/scripts/SING
    OUTPUTELAS=$(echo "$(./${ELASFOR}.expect ${BEAMINP})")

    python3 setElasArm.py ${KIN} ${SPEC} ${BEAMINP} ${THETAINP} ${InputSIMC} "$OUTPUTELAS"
else
    cd ${SIMCPATH}/scripts/COIN
    KIN=$1

    InputSIMC="Heep_Coin_${KIN}"
fi

cd ${SIMCPATH}/scripts
if [[ $a_flag = "true" ]]; then
    echo
    echo 
    echo "Running simc analysis for ${InputSIMC}..."
    echo
    cd "${SIMCPATH}"
    ./run_simc_tree "${InputSIMC}"
fi
