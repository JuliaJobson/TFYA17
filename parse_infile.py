#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np

import qml
from parse_poscar import atomInformation

def get_xyz(filename, information):
    """ Returns xyz-files from data file"""

    #Take out variables that will be constant throughout loops
    natoms=information.num_of_atoms
    charge=information.atom_charge
    name=information.type

    atom_counter = 1
    time_step_counter = 0
    T = time.time()


    #Loop over all time units in given file
    with open(filename, 'r') as file:


        for line in file:
            #Format string to desired format
            line = line.split("  ")
            line = "{0} {1} {2}".format(*line)

            if atom_counter==1:
                #Increment filename over time unit
                filepath = str(time_step_counter).zfill(5)
                #Create file and insert common information, observe, this needs a folder called 'qm'
                xyzfile = open('qm/%s.xyz'% filepath, 'w')
                xyzfile.write("%d \n"%(natoms))
                xyzfile.write("charge = %s \n" % charge)
                time_step_counter += 1

            xyzfile.write(" %s %s\n" % (name, line))
            atom_counter += 1

            if atom_counter == natoms + 1:
                atom_counter = 1
                xyzfile.close()

        print("End of file, counter: %d \n time: %f, %f "%(time_step_counter, time.time() - T, time.clock()))


if __name__ == '__main__':
    filepath_poscar = str(sys.argv[1])
    pos_at = atomInformation(filepath_poscar)
    filepath_infile = str(sys.argv[2])
    get_xyz(filepath_infile, pos_at)
