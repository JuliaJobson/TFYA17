#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np
from qml.representations import get_slatm_mbtypes
from qml.kernels import gaussian_kernel
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
    compounds = generateRep(200, 'infile.forces')

    # Make a big 2D array with all the
    X = np.array([atoms.representation for atoms in compounds])
    Y = np.array([atoms.properties for atoms in compounds])

    #print(X)
    #print(Y)

    # Assign 1000 first atoms to the training set
    X_training = X[:100]
    Y_training = Y[:100]
    #print(X_training)
    #print(Y_training)
    # Y_training = energy_delta[:1000]

    # Assign 1000 last atoms to the training set
    X_test = X[-100:]
    Y_test = Y[-100:]
    # Y_test = energy_delta[-1000:]

    # Calculate the Gaussian kernel
    sigma = 1000.0
    K = gaussian_kernel(X_training, X_training, sigma)
    #print(K)
    #print(K.shape)
    # Add a small lambda to the diagonal of the kernel matrix
    #K[np.diag_indices_from(K)] += 1e-8

    # Use the built-in Cholesky-decomposition to solve
    #print(K.shape)
    #print(Y_training.shape)
    #alpha = cho_solve(K, Y_training)


    #print(alpha)

    # Assign 1000 last molecules to the test set
    X_test = X[-100:]
    Y_test = Y[-100:]

    # calculate a kernel matrix between test and training data, using the same sigma
    Ks = gaussian_kernel(X_test, X_training, sigma)

    # Make the predictions
    Y_predicted = np.dot(Ks, alpha)

    # Calculate mean-absolute-error (MAE):
    print(np.mean(np.abs(Y_predicted - Y_test)))
