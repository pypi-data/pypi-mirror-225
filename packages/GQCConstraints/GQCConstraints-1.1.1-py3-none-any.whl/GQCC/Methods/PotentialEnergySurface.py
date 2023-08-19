"""
Potential Energy Surface
-------------------------

A pre-defined method that takes a series of constrained objects, each from a different internuclear distance & calculates the energies and parameters for each one of them.

Each calculation happens at the same constraint.

.. note::

    Examples on how to use our pre-defined methods can be found in the Jupyter notebook examples on our `GitHub page <https://github.com/GQCG-res/GQCConstraints/tree/develop/examples>`_.
"""

# Import dependencies
import pandas as pd
import numpy as np


def spinResolved(constrained_object_array, distances, alpha_constraint, beta_constraint, optimization_function, initial_guesses=None, threshold=1e-5, verbose=0, **options):
    """
    A multiplier scan for unresolved constrained methods.

    note: For a Hubbard PES, the "distances" parameter should be a list of U/t values.

    :param constrained_object_array:        The constrained objects belonging to different internuclear distances.
    :param distances:                       The provided range internuclear distances for the potential energy surface.
    :param alpha_constraint:                The alpha value at which each calculation shall be constrained.
    :param beta_constraint:                 The beta value at which each calculation shall be constrained.
    :param initial_guesses:                 The series of initial guesses for the optimization, if required.
    :param optimization_function:           The optimization function that will be used to optimize the multipliers. Can be a pre-defined function by GQCC or a self-implemented function that adheres to the same form.
    :param threshold:                       The threshold at which the calculated and expected value are compared.
    :param verbose:                         An integer representing the amount of output that will be printed.
    :param options:                         The possible options that can be passed to the optimization function.

    :returns:                               A pandas dataframe in which the calculated data is cleanly stored.
    """
    return spinUnresolved(constrained_object_array, distances, [alpha_constraint, beta_constraint], optimization_function, initial_guesses=initial_guesses, threshold=threshold, verbose=verbose, **options)


def spinUnresolved(constrained_object_array, distances, constraint, optimization_function, initial_guesses=None, threshold=1e-5, verbose=0, **options):
    """
    A multiplier scan for unresolved constrained methods.

    note: For a Hubbard PES, the "distances" parameter should be a list of U/t values.

    :param constrained_object_array:        The constrained objects belonging to different internuclear distances.
    :param distances:                       The provided range internuclear distances for the potential energy surface.
    :param constraint:                      The value at which each calculation shall be constrained.
    :param optimization_function:           The optimization function that will be used to optimize the multipliers. Can be a pre-defined function by GQCC or a self-implemented function that adheres to the same form.
    :param initial_guesses:                 The series of initial guesses for the optimization, if required.
    :param threshold:                       The threshold at which the calculated and expected value are compared.
    :param verbose:                         An integer representing the amount of output that will be printed.
    :param options:                         The possible options that can be passed to the optimization function.

    :returns:                               A pandas dataframe in which the calculated data is cleanly stored.
    """
    # In case of initial guesses, we need to make sure enough guesses are provided.
    if initial_guesses is not None:
        if len(initial_guesses) != len(distances):
            raise Exception("The list of initial guesses must be as long as the total number of calculations: i.e. len(distances).")

    # In case of initial guesses, we need to make sure enough guesses are provided.
    if len(constrained_object_array) != len(distances):
        raise Exception("The list of constrained objects has to have the same dimension as the list of distances: i.e. (len(constrained_object_array) == len(distances)).")

    # Set up a dataframe for the calculated data.
    output_data = pd.DataFrame({'distances': distances})

    # Print a starting signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("      Potential energy surface generation started.      ")
        print("********************************************************")
    
    # Calculate the energy and population of the Hamiltonian constrained with the current mu value.
    for i, constrained_object in enumerate(constrained_object_array):
        if initial_guesses is not None:
            initial_guess = initial_guesses[i]
        else:
            initial_guess = None 

        multiplier = constrained_object.optimizeMultiplier(constraint, optimization_function, initial_guess=initial_guess, **options)
        if isinstance(multiplier, np.ndarray):
            output_data.loc[i, 'alpha multipliers'] = multiplier[0]
            output_data.loc[i, 'beta multipliers'] = multiplier[1]
        else:
            output_data.loc[i, 'multipliers'] = multiplier

        if isinstance(constraint, list):
            output_data.loc[i, constrained_object._constrained_alpha_observable + 's'] = constraint[0]
            output_data.loc[i, constrained_object._constrained_beta_observable + 's'] = constraint[1]
        else:
            output_data.loc[i, constrained_object._constrained_observable + 's'] = constraint

        energy, parameters = constrained_object.verifyCombination(multiplier, constraint, return_parameters=True, threshold=threshold, verbose=verbose)
        output_data.loc[i, 'energies'] = energy
        output_data.loc[i, 'parameters'] = parameters

    # Print a stopping signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("      Potential energy surface generation ended.        ")
        print("********************************************************")

    # Return the dataframe containing the mus, energies and populations.
    return output_data
