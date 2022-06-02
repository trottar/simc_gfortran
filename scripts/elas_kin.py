#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-01 20:23:43 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import numpy as np
from numpy import f2py
import pandas as pd
import os,sys

inp_f = 'elas_kin'

with open("%s.f" % inp_f) as srcf:
    srcc = srcf.read()
f2py.compile(srcc,modulename='pyadd', verbose=False)
#f2py.compile(srcc,modulename='pyadd', verbose=True)

try:
    import pyadd
except ModuleNotFoundError:
    print("ERROR: Module for %s not found..." % inp_f)
    sys.exit(0)

print("\n\nDoc for %s..." % inp_f)    
print(pyadd.__doc__)

N = 1000
beam_energy = 10.600
Th_e = np.zeros(N)
Q2 = np.zeros(N)
E_e = np.zeros(N)
Th_p = np.zeros(N)
P_p = np.zeros(N)
Mott = np.zeros(N)
Sig_p = np.zeros(N)

# Th_e,Q2,E_e,Th_p,P_p,Mott,Sig_p are will get redefined with the proper values from calculations
pyadd.kin_table(beam_energy,Th_e,Q2,E_e,Th_p,P_p,Mott,Sig_p,N)

kinDict = {

    'Theta_e' : Th_e,
    'Q2' : Q2,
    'E_e' : E_e,
    'Th_p' : Th_p,
    'P_p' : P_p,
    'Mott' : Mott,
    'Sig_p (fm^2/sr)' : Sig_p,
}

kin_data = {i : kinDict[i] for i in sorted(kinDict.keys())}

# Convert merged dictionary to a pandas dataframe then sort it
table  = pd.DataFrame([kin_data], columns=kin_data.keys())
table = table.reindex(sorted(table.columns), axis=1)

print(table['P_p'])
