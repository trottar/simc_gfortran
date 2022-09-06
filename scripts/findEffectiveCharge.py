#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-09-06 04:13:38 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import re, sys, os

################################################################################################################################################
'''
User Inputs
'''
efficiency_table = sys.argv[1]
ROOTPrefix = sys.argv[2]
runNum = sys.argv[3]
MaxEvent=sys.argv[4]

################################################################################################################################################
'''
ltsep package import and pathing definitions
'''
# Import package for cuts
from ltsep import Root

lt=Root(os.path.realpath(__file__))

# Add this to all files for more dynamic pathing
UTILPATH=lt.UTILPATH

################################################################################################################################################
################################################################################################################################################
# Define efficiencies

inp_f = UTILPATH+"/scripts/efficiency/OUTPUTS/%s" % efficiency_table

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

tot_eff = EDTM*pHodo3_4*hHodo3_4

################################################################################################################################################

# Open report file to grab prescale values and tracking efficiency
report = UTILPATH+"/REPORT_OUTPUT/Analysis/General/%s_%s_%s.report" % (ROOTPrefix,runNum,MaxEvent)
#report = UTILPATH+"/REPORT_OUTPUT/Analysis/HeeP/%s_%s_%s.report" % (ROOTPrefix,runNum,MaxEvent)

with open(report) as f:
    # Search for keywords, then save as value in dictionary
    for line in f:
        data = line.split(':')
        if 'BCM1_Beam_Cut_Charge' in data[0]:
            charge = int(re.sub("\D","","%s" % data[1]))
        if 'Total_Events' in data[0]:
            numevts = int(re.sub("\D","","%s" % data[1]))

effective_charge = float(charge/1000)*float(tot_eff)

print(int(1000*effective_charge))
