#! /bin/bash

RUNNUMBER=$1
MAXEVENTS=$2
SPEC=$3

InDATAFilename=${RUNNUMBER}_${MAXEVENTS}_sw_heep_${SPEC}_Analysis_Distributions
InSIMCFilename=simc_heep_${SPEC}_${RUNNUMBER}_${MAXEVENTS}
OutFilename=analyzed_heep_${SPEC}_${RUNNUMBER}_${MAXEVENTS}

root <<EOF
.Analysis_${SPEC}.C($InDATAFilename,$InSIMCFilename,$OutFilename)
EOF
