#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np

import qml

def createCompound(num_files, filename):
    """Creates coumpund objects from each xyz-file"""


    compound_list = [qml.Compound(xyz="qm/%s.xyz" % str(d).zfill(5)) for d in range(num_files)]

    with open(filename, 'r') as file:

        for atoms in compound_list:
            prop_lst = []

            for n in range(atoms.natoms):
                line = file.readline().strip("\n")
                line = line.split(" ")
                prop_lst.append([float(k) for k in line if (k != '')])

            atoms.properties = np.array(prop_lst)
            #atoms.properties = atoms.properties.reshape(atoms.natoms,3)
            #print(atoms.properties)
            #print(atoms.nuclear_charges)
    return compound_list
