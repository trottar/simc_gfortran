#! /bin/bash

ANA_DIR="/group/c-kaonlt/USERS/${USER}/simc_gfortran"
HEEPFOR="heepcheck"


cd ${ANA_DIR}/scripts/
echo "Compiling ${HEEPFOR}.f..."
eval "gfortran -o  ${HEEPFOR} ${HEEPFOR}.f"
./${HEEPFOR}
