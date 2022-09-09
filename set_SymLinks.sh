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

# Check symlinks and create/fix if bad
if [ ! -L "${SIMCPATH}/OUTPUT" ]; then
    ln -s "${VOLATILEPATH}/OUTPUT/" "${SIMCPATH}/OUTPUT"
elif [ -L "${SIMCPATH}/OUTPUT" ]; then
    if [ ! -e "${SIMCPATH}/OUTPUT" ]; then
	echo "${SIMCPATH}/OUTPUT sym link exits but is broken, replacing"
	rm "${SIMCPATH}/OUTPUT"
	ln -s "${VOLATILEPATH}/OUTPUT/" "${SIMCPATH}/OUTPUT"
    else 
	echo "${SIMCPATH}/OUTPUT sym link already exists and not broken"
	echo "             ${SIMCPATH}/OUTPUT-->${VOLATILEPATH}/OUTPUT/"
	echo
	echo
    fi
fi

if [ ! -L "${SIMCPATH}/src/OUTPUTS" ]; then
    ln -s "${SIMCPATH}/OUTPUT/Analysis/HeeP/" "${SIMCPATH}/src/OUTPUTS"
elif [ -L "${SIMCPATH}/src/OUTPUTS" ]; then
    if [ ! -e "${SIMCPATH}/src/OUTPUTS" ]; then
	echo "${SIMCPATH}/src/OUTPUTS sym link exits but is broken, replacing"
	rm "${SIMCPATH}/src/OUTPUTS"
	ln -s "${SIMCPATH}/OUTPUT/Analysis/HeeP/" "${SIMCPATH}/src/OUTPUTS"
    else 
	echo "${SIMCPATH}/src/OUTPUTS sym link already exists and not broken"
	echo "             ${SIMCPATH}/src/OUTPUTS-->${SIMCPATH}/OUTPUT/Analysis/HeeP/"
	echo
	echo
    fi
fi

if [ ! -L "${SIMCPATH}/src/input" ]; then
    ln -s "${SIMCPATH}/input/" "${SIMCPATH}/src/input"
elif [ -L "${SIMCPATH}/src/input" ]; then
    if [ ! -e "${SIMCPATH}/src/input" ]; then
	echo "${SIMCPATH}/src/input sym link exits but is broken, replacing"
	rm "${SIMCPATH}/src/input"
	ln -s "${SIMCPATH}/input/" "${SIMCPATH}/src/input"
    else 
	echo "${SIMCPATH}/src/input sym link already exists and not broken"
	echo "             ${SIMCPATH}/src/input-->${SIMCPATH}/input/"
	echo
	echo
    fi
fi

if [ ! -L "${SIMCPATH}/src/worksim" ]; then
    ln -s "${VOLATILEPATH}/worksim/" "${SIMCPATH}/src/worksim"
elif [ -L "${SIMCPATH}/src/worksim" ]; then
    if [ ! -e "${SIMCPATH}/src/worksim" ]; then
	echo "${SIMCPATH}/src/worksim sym link exits but is broken, replacing"
	rm "${SIMCPATH}/src/worksim"
	ln -s "${VOLATILEPATH}/worksim/" "${SIMCPATH}/src/worksim"
    else 
	echo "${SIMCPATH}/src/worksim sym link already exists and not broken"
	echo "             ${SIMCPATH}/src/worksim-->${VOLATILEPATH}/worksim/"
	echo
	echo
    fi
fi

echo 
echo "Directories and sym links for ${SIMCPATH} now setup"

exit 0
