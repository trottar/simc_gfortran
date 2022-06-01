#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-06-01 17:35:06 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
from numpy import f2py
import os,sys

inp_f = 'heepcheck'

with open("%s.f" % inp_f) as srcf:
    srcc = srcf.read()
f2py.compile(srcc,modulename='pyadd', verbose=False)

try:
    import pyadd
except ModuleNotFoundError:
    print("ERROR: Module for %s not found..." % inp_f)
    sys.exit(0)

print("\n\nDoc for %s..." % inp_f)    
print(pyadd.__doc__)


e0 = 10500

the0 = 15.00

