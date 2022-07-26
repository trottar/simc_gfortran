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

while getopts 'hca' flag; do
    case "${flag}" in
        h) 
        echo "---------------------------"
        echo "./check_Offsets.sh -{flags}"
        echo "---------------------------"
        echo
        echo "The following flags can be called for the heep analysis..."
        echo "    -h, help"
        echo "    -c, compile fortran code"
	echo "    -a, run SIMC with new singles settings"
        exit 0
        ;;
        c) c_flag='true' ;;
	a) a_flag='true' ;;
        *) print_usage
        exit 1 ;;
    esac
done

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
    KIN=$1
fi


InputSIMC="Heep_${SPEC}_${KIN}"

SIMCINP=`python3 getSetting.py ${KIN} ${SPEC} ${InputSIMC}`

BEAMINP=`echo ${SIMCINP} | cut -d ',' -f1`
THETAINP=`echo ${SIMCINP} | cut -d ',' -f2`

OUTPUTELAS=$(echo "$(./${ELASFOR}.expect ${BEAMINP})")

cd "${SIMCPATH}/scripts/SING"
python3 setElasArm.py  ${KIN} ${SPEC} ${BEAMINP} ${THETAINP} "$OUTPUTELAS" ${InputSIM}

if [[ $a_flag = "true" ]]; then
    echo
    echo 
    echo "Running simc analysis for ${InputSIMC}..."
    echo
    cd "${SIMCPATH}"
    ./run_simc_tree "${InputSIMC}"
fi
