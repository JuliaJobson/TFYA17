#!/usr/bin/env python3

import sys
import re
import numpy as np

class atomInformation(object):
    """The atomInformation module is used to store information about the OUTCAR data"""
    def __init__(self, filepath):


        # Information about the atom
        self.type = None
        self.param_type = None
        self.supercell = np.empty((3,3), float)
        self.num_of_atoms = None
        self.coordinate_type = None
        self.atom_pos = np.empty
        self.atom_charge = 0 #TODO need to find out how to extract atom charge from atom type

        # Parse the POSCAR file
        if filepath:
            self.parse(filepath)

        # print
    def Print_Atom(self):
        print('Atom: %s \n' %self.type)
        print('Parameter type: %s \n' %self.param_type)
        print('Number of atoms in POSCAR: %s \n' %self.num_of_atoms)
        print(self.supercell)
        print('Coordinate typ of postion: %s \n' %self.coordinate_type)
        print(self.atom_pos)

    def parse(self, filepath):
        """
        Parse text at given filepath

        Parameters
        ----------
        filepath : str
            Filepath for file to be parsed

        Returns
        -------
        data : Atom module
            Parsed data

        """
        with open(filepath, 'r') as file:
            next(file)

            # Second row defines if latice parameter is used
            line = next(file)
            if "-" in line:
                self.param_type = "Å"
            else:
                self.param_type = "latice"

            # Supercell
            cell = []
            for i in range(3):
                line = next(file).split()
                cell.append([float(k) for k in line])
            self.supercell = np.array(cell)
            self.supercell = self.supercell.reshape(3,3)

            # Atom type
            self.type = next(file).rstrip()

            # Numer of atoms in OUTCAR
            self.num_of_atoms = int(next(file))

            # Coordinate type
            self.coordinate_type = next(file)

            # Positons of atoms
            pos = []
            for i in range(self.num_of_atoms):
                line = next(file).split()
                pos.append([float(k) for k in line])
            self.atom_pos = np.array(pos)
            self.atom_pos = self.atom_pos.reshape(self.num_of_atoms,3)




#if __name__ == '__main__':
#    if len(sys.argv) > 1:
#        filepath = str(sys.argv[1])
#        pos_at = atomInformation(filepath)

        #Testing
        #pos_at.Print_atomInformation()

#    else :
#        print("error: no arguments given")
