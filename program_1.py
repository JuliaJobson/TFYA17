#!/usr/bin/env python3

import random
import os
import sys
import time

import numpy as np
<<<<<<< HEAD
import pickle

=======
>>>>>>> 05c5cf7657d15c38704fc7d148412ffb3c6ab12d
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


        compound.generate_slatm(mbtypes, local=True, pbc = '000')


    return compounds
    #    print("Representation:")
    #    print(compound.representation)


if __name__ == "__main__":


    num_xyz = 4000


    # For every compound generate a coulomb matrix
    compounds = generateRep(num_xyz, 'infile.forces')

    # Make a big 2D array with all the
    with open('XData.pickle', 'rb') as f:
        X = pickle.load(f)

    with open('NData.pickle', 'rb') as f:
        N = pickle.load(f)

    with open('YData.pickle', 'rb') as f:
        Y = pickle.load(f)


    # variables
    num_atoms = N[0]
    num_comp = floor(num_xyz/2)


    X_training = X[:num_comp*num_atoms, :]
    Y_training = Y[:num_comp, :, :]
    print('X_training')
    print(X_training)
    print('Y_training')
    print(Y_training)




    # Calculate the Gaussian kernel
    sigmas =  [3200.0]
    #K = get_local_kernels_gaussian(X, X, N, N, sigmas)
    K = get_local_kernels_gaussian(X_training, X_training, N[:num_comp], N[:num_comp], sigmas)

    print('K')
    print(K)

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
    print(Y_predicted)
    # Calculate mean-absolute-error (MAE):
    print(np.mean(np.abs(Y_predicted - Y_test)))

    # Pickle dump
    with open('kernelsData.pickle', 'wb') as f:
        pickle.dump(Ks, f, pickle.HIGHEST_PROTOCOL)

    with open('alphaData.pickle', 'wb') as f:
        pickle.dump(alphas, f, pickle.HIGHEST_PROTOCOL)

    with open('kernelData.pickle', 'wb') as f:
        pickle.dump(K, f, pickle.HIGHEST_PROTOCOL)


    #with open('kernelData.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        #data = pickle.load(f)

