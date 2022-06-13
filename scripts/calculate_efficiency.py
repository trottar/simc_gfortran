#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-13 09:15:35 trottar"
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
import ltsep as lt 

proc_root = lt.Root(os.path.realpath(__file__),"Plot_SimcCoin").setup_ana()
p = proc_root[2] # Dictionary of pathing variables
OUTPATH = proc_root[3] # Get pathing for OUTPATH

# Add this to all files for more dynamic pathing
UTILPATH = p["UTILPATH"]


################################################################################################################################################
# Define efficiencies

inp_f = UTILPATH+"/scripts/efficiency/OUTPUTS/coin_production_HeePCoin_efficiency_data_2022_06_13.csv"

# Converts csv data to dataframe
try:
    eff_data = pd.read_csv(inp_f)
except IOError:
    print("Error: %s does not appear to exist." % inp_f)
print(eff_data.keys())

eff_data = eff_data[eff_data['Run_Number'] == runNum]

print(eff_data)

data_efficiency = eff_data["Non_Scaler_EDTM_Live_Time"]*eff_data["SHMS_Pion_SING_TRACK_EFF"]*eff_data["SHMS_Aero_SING_Pion_Eff"]*eff_data["SHMS_Hodo_3_of_4_EFF"]*eff_data["HMS_Elec_SING_TRACK_EFF"]*eff_data["HMS_Cer_SING_Elec_Eff"]*eff_data["HMS_Hodo_3_of_4_EFF"]

dummy_efficiency = eff_data["Non_Scaler_EDTM_Live_Time"]*eff_data["SHMS_Pion_SING_TRACK_EFF"]*eff_data["SHMS_Aero_SING_Pion_Eff"]*eff_data["SHMS_Hodo_3_of_4_EFF"]*eff_data["HMS_Elec_SING_TRACK_EFF"]*eff_data["HMS_Cer_SING_Elec_Eff"]*eff_data["HMS_Hodo_3_of_4_EFF"]
