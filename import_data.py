#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np
from qml.representations import get_slatm_mbtypes

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
                prop_lst.append([float(k) for k in line])
            atoms.properties = np.array(prop_lst)
            atoms.properties = atoms.properties.reshape(atoms.natoms,3)
            print(atoms.properties)

    return compound_list


if __name__ == '__main__':

    compounds = createCompound(5, "infile.forces")
    mbtypes = get_slatm_mbtypes([atoms.nuclear_charges for atoms in compounds])

    for atoms in compounds:
        atoms.generate_slatm(atoms, mbtypes)
        print("Representation:")
        print(atoms.representation)
        print(atoms.properties)
