#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np
from qml.representation import get_slatm_mbtypes

import qml



def createCompound(num_files)
    """Creates coumpund objects from each xyz-file"""


    compound_list = [qml.Compound(xyz="qm/%s.xyz" % str(d).zfill(5)) for d in range(num_files)]
    return compound_list


if __name__ == '__main__':
    compounds = createCompound(5)
    mbtypes = get_slatm_mbtypes([atoms.nuclear_charges for atoms in compounds])

    for atoms in compounds:
        atoms.generate_slatm(atoms, mbtypes)
    
