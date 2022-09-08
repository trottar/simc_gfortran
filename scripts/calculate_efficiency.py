#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-09-08 04:39:14 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
from functools import reduce
import sys,os

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

def calculate_efficiency(runNum,efficiency_table):

    inp_f = UTILPATH+"/scripts/efficiency/OUTPUTS/%s" % efficiency_table

    # Converts csv data to dataframe
    try:
        eff_data = pd.read_csv(inp_f)
    except IOError:
        print("Error: %s does not appear to exist." % inp_f)
        sys.exit(1)
    #print(eff_data.keys())

    # Redefine table to be only the run number of interest
    eff_data = eff_data[eff_data['Run_Number'] == int(runNum)]
    #print(eff_data)

    # Define dictionary of efficiency values
    effDict ={
        "EDTM" : eff_data["Non_Scaler_EDTM_Live_Time"].iloc[0],
        #"pPiTrack" : eff_data["SHMS_Pion_SING_TRACK_EFF"].iloc[0],
        #"pPiAero" : eff_data["SHMS_Aero_SING_Pion_Eff"].iloc[0],
        "pHodo3_4" : eff_data["SHMS_Hodo_3_of_4_EFF"].iloc[0],
        #"hElTrack" : eff_data["HMS_Elec_SING_TRACK_EFF"].iloc[0],
        #"hElCer" : eff_data["HMS_Cer_SING_Elec_Eff"].iloc[0],
        "hHodo3_4" : eff_data["HMS_Hodo_3_of_4_EFF"].iloc[0],
    }
    

    # Calculate total efficiency. The reduce function pretty much iterates on
    # its arguments which in this case is a lambda function. This lambda function
    # takes x,y from the list (ie the list of efficiencies) and multiplies them.
    # This is all pythonic language for doing the product of everything in the
    # list. Enjoy!
    tot_efficiency = reduce(lambda x, y: x*y, list(effDict.values()))
    return tot_efficiency
