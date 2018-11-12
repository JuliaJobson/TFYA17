#!/usr/bin/env python3

import random
import os
import sys

import numpy as np

import qml
from parse_poscar import atomInformation

def get_xyz(filename, information):
    """ Returns positions for each xyz-file"""

    #Take out variables that will be constant throughout loops
    natoms=information.num_of_atoms
    print(natoms)
    charge=information.atom_charge
    name=information.type

    counter = 0

    #TODO First timestep, contained in information

    #Loop over all time units in given file
    with open(filename, 'r') as file:
        while True:
            line = next(file)
            if line == '':
                break
            counter += 1
            #Increment filename over time unit
            filepath = str(counter).zfill(4)
            #Create file and insert common information
            xyzfile = open('pos/%s.xyz'% filepath, 'w')
            xyzfile.write("%d \n"%(natoms))
            xyzfile.write("charge = %s \n" % charge)
            #Increment positions over number of atoms for one time unit
            for i in range(natoms):
                xyzfile.write(" %s %s\n" % (name, line))
                line = next(file)
            xyzfile.close()



#compounds = [qml.Compound(xyz=)]
if __name__ == '__main__':
    filepath_poscar = str(sys.argv[1])
    pos_at = atomInformation(filepath_poscar)
    filepath_infile = str(sys.argv[2])
    get_xyz(filepath_infile, pos_at)
