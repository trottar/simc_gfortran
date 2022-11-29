#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-11-29 12:14:55 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import sys

inp_f = sys.argv[1]

f_data = ''
with open(inp_f, 'r') as f:
    for line in f:
        f_data += str(line)+' '
print(f_data)
