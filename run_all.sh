#! /bin/bash

#
# Description:
# ================================================================
# Time-stamp: "2022-12-31 11:20:38 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#

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


#SIMCPATH="/u/group/c-kaonlt/USERS/${USER}/simc_gfortran"

cd "${SIMCPATH}"

#./set_ProdBin.sh -a high 5p5 3p02 5 lh2
#./set_ProdBin.sh -a low 5p5 3p02 5 lh2
#./set_ProdBin.sh -a high 4p4 2p74 5 lh2
#./set_ProdBin.sh -a low 4p4 2p74 5 lh2
#./set_ProdBin.sh -a high 3p0 3p14 5 lh2
#./set_ProdBin.sh -a low 3p0 3p14 5 lh2
#./set_ProdBin.sh -a high 3p0 2p32 5 lh2
#./set_ProdBin.sh -a low 3p0 2p32 5 lh2
#./set_ProdBin.sh -a high 2p1 2p95 5 lh2
#./set_ProdBin.sh -a low 2p1 2p95 5 lh2
#./set_ProdBin.sh -a high 0p5 2p40 5 lh2
#./set_ProdBin.sh -a low 0p5 2p40 5 lh2
#./set_ProdBin.sh -a high 5p5 3p02 5 dummy
#./set_ProdBin.sh -a low 5p5 3p02 5 dummy
#./set_ProdBin.sh -a high 4p4 2p74 5 dummy
#./set_ProdBin.sh -a low 4p4 2p74 5 dummy
#./set_ProdBin.sh -a high 3p0 3p14 5 dummy
#./set_ProdBin.sh -a low 3p0 3p14 5 dummy
#./set_ProdBin.sh -a high 3p0 2p32 5 dummy
#./set_ProdBin.sh -a low 3p0 2p32 5 dummy
#./set_ProdBin.sh -a high 2p1 2p95 5 dummy
#./set_ProdBin.sh -a low 2p1 2p95 5 dummy
#./set_ProdBin.sh -a high 0p5 2p40 5 dummy
#./set_ProdBin.sh -a low 0p5 2p40 5 dummy

./set_ProdBin.sh high 5p5 3p02 5 lh2
echo "test"
