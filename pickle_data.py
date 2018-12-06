#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np
import pickle

from qml.representations import get_slatm_mbtypes
from qml.kernels import get_local_kernels_gaussian
from qml.math import cho_solve
from math import floor

import qml

from import_data import createCompound


def generateRep(num_of_xyz, property_filename):

    compounds = createCompound(num_of_xyz, property_filename)
    mbtypes = get_slatm_mbtypes([atoms.nuclear_charges for atoms in compounds])

    for compound in compounds:

        compound.generate_slatm(mbtypes, local=True, pbc = '111')

    return compounds


if __name__ == "__main__":

    num_xyz = 4000

    # For every compound generate a coulomb matrix
    compounds = generateRep(num_xyz, 'infile.forces')


    # Make a big 2D array with all the
    X = np.concatenate([atoms.representation for atoms in compounds])
    N = np.array([atoms.natoms for atoms in compounds])
    Y = np.array([atoms.properties for atoms in compounds])

    with open('XData.pickle', 'wb') as f:
        pickle.dump(X, f, pickle.HIGHEST_PROTOCOL)

    with open('YData.pickle', 'wb') as f:
        pickle.dump(Y, f, pickle.HIGHEST_PROTOCOL)

    with open('NData.pickle', 'wb') as f:
        pickle.dump(N, f, pickle.HIGHEST_PROTOCOL)
