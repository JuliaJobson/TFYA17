#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np
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
    #    print("Representation:")
    #    print(compound.representation)


if __name__ == "__main__":

    num_xyz = 10000

    # For every compound generate a coulomb matrix
    compounds = generateRep(num_xyz, 'infile.forces')

    # Make a big 2D array with all the
    X = np.concatenate([atoms.representation for atoms in compounds])
    N = np.array([atoms.natoms for atoms in compounds])
    Y = np.array([atoms.properties for atoms in compounds])


    # variables
    num_atoms = N[0]
    num_comp = floor(num_xyz/2)


    # Assign 1000 first atoms to the training set
    X_training = X[:num_comp*num_atoms, :]
    Y_training = Y[:num_comp, :, :]
    print('X_training')
    print(X_training.shape)
    #print(Y_training)



    # Calculate the Gaussian kernel
    sigmas =  [1000.0]
    K = get_local_kernels_gaussian(X_training, X_training, N[:num_comp], N[:num_comp], sigmas)
    print('K')
    print(K.shape)

    # Add a small lambda to the diagonal of the kernel matrix
    K[0, :, :][np.diag_indices_from(K[0, :, :])] += 1e-8


    # Use the built-in Cholesky-decomposition to solve
    alphas=np.zeros([num_comp, num_atoms, 3])
    for i in range(num_atoms):
        for j in range(3):
            alphas[:,i,j] = cho_solve(K[0,:,:], Y_training[:,i,j])
    print('alphas')
    print(alphas.shape)

    # Assign last atoms to the test set
    X_test = X[-num_comp*num_atoms:, :]
    Y_test = Y[-num_comp:, : , :]
    print('X-test')
    print(X_test.shape)

    # calculate a kernel matrix between test and training data, using the same sigma
    Ks = get_local_kernels_gaussian(X_training, X_test, N[:num_comp], N[-num_comp:], sigmas)
    print('Ks')
    print(Ks.shape)

    # Make the predictions
    Y_predicted = np.zeros([num_comp, num_atoms, 3])
    for i in range(num_atoms):
        for j in range(3):
            Y_predicted[:,i,j] = np.dot(Ks[0,:,:], alphas[:,i,j])
    print('Y_predicted')
    print(Y_predicted.shape)
    # Calculate mean-absolute-error (MAE):
    print(np.mean(np.abs(Y_predicted - Y_test)))
