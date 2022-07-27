#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-07-27 11:08:27 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import sys,os

runNum = sys.argv[1]

###############################################################################################################################################

'''
ltsep package import and pathing definitions
'''

# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
UTILPATH=lt.UTILPATH

################################################################################################################################################
# Define efficiencies

inp_f = UTILPATH+"/scripts/efficiency/OUTPUTS/coin_production_HeePCoin_efficiency_data_2022_06_13.csv"
#inp_f = UTILPATH+"/scripts/efficiency/OUTPUTS/coin_production_HeePCoin_efficiency_data_2022_13.csv"

# Converts csv data to dataframe
try:
    eff_data = pd.read_csv(inp_f)
except IOError:
    print("Error: %s does not appear to exist." % inp_f)
    sys.exit(1)
#print(eff_data.keys())

eff_data = eff_data[eff_data['Run_Number'] == int(runNum)]
#print(eff_data)

EDTM = eff_data["Non_Scaler_EDTM_Live_Time"].iloc[0]
pPiTrack = eff_data["SHMS_Pion_SING_TRACK_EFF"].iloc[0]
pPiAero = eff_data["SHMS_Aero_SING_Pion_Eff"].iloc[0]
pHodo3_4 = eff_data["SHMS_Hodo_3_of_4_EFF"].iloc[0]
hElTrack = eff_data["HMS_Elec_SING_TRACK_EFF"].iloc[0]
hElCer = eff_data["HMS_Cer_SING_Elec_Eff"].iloc[0]
hHodo3_4 = eff_data["HMS_Hodo_3_of_4_EFF"].iloc[0]

#print("EDTM",EDTM,"\npPiTrack",pPiTrack,"\npPiAero",pPiAero,"\npHodo3_4",pHodo3_4,"\nhElTrack",hElTrack,"\nhElCer",hElCer,"\nhHodo3_4",hHodo3_4)

data_efficiency = EDTM*pHodo3_4*hHodo3_4
print(data_efficiency)
