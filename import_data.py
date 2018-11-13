#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np

import qml



def createCompund(num_files)
    """Creates coumpund objects from each xyz-file"""


    compounds = [qml.Compound(xyz="qm/%s.xyz" % str(d).zfill(5)) for d in range(num_files)]
if __name__ == '__main__':
