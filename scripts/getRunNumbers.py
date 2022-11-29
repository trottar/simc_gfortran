#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2022-11-29 11:48:27 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import sys

inp_f = sys.argv[1]

with open(inp_f, 'r') as f:
    f_data = f.read()

BashPathEntry=("{0},{1},{2},{3},{4}".format(inpDict["ebeam"],inpDict["eTh"],inpDict["eP"],inpDict["pTh"],inpDict["pP"]))
print(BashPathEntry)
