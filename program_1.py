#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np
from qml.representations import get_slatm_mbtypes
from qml.kernels import get_local_kernels_gaussian
from qml.math import cho_solve

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

    # For every compound generate a coulomb matrix
    compounds = generateRep(400, 'infile.forces')

    # Make a big 2D array with all the
    X = np.concatenate([atoms.representation for atoms in compounds])
    N = np.array([atoms.natoms for atoms in compounds])
    Y = np.array([atoms.properties for atoms in compounds])

    print(X.shape)
    print(Y.shape)

    # Assign 1000 first atoms to the training set
    X_training = X[:200*N[0], :]
    Y_training = Y[:200, :, :]
    print('X_training')
    print(X_training.shape)
    #print(Y_training)


    # Assign 1000 last atoms to the training set
    #X_test = X[-1000:]
    #Y_test = Y[-1000:]


    # Calculate the Gaussian kernel
    sigmas =  [1000.0]
    K = get_local_kernels_gaussian(X_training, X_training, N[:200], N[:200], sigmas)
    print('K')
    print(K.shape)

    # Add a small lambda to the diagonal of the kernel matrix
    K[0, :, :][np.diag_indices_from(K[0, :, :])] += 1e-8


    # Use the built-in Cholesky-decomposition to solve
    alphas=np.zeros([200, N[0], 3])
    for i in range(N[0]):
        for j in range(3):
            alphas[:,i,j] = cho_solve(K[0,:,:], Y_training[:,i,j])
    print('alphas')
    print(alphas.shape)

    # Assign 1000 last molecules to the test set
    X_test = X[-200*32:, :]
    Y_test = Y[-200:, : , :]
    print('X-test')
    print(X_test.shape)

    # calculate a kernel matrix between test and training data, using the same sigma
    Ks = get_local_kernels_gaussian(X_training, X_test, N[:200], N[-200:], sigmas)
    print('Ks')
    print(Ks.shape)

    # Make the predictions
    Y_predicted = np.zeros([200, 32, 3])
    for i in range(N[0]):
        for j in range(3):
            Y_predicted[:,i,j] = np.dot(Ks[0,:,:], alphas[:,i,j])
    print(Y_predicted.shape)
    # Calculate mean-absolute-error (MAE):
    print(np.mean(np.abs(Y_predicted - Y_test)))
