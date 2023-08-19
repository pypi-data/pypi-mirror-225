"""
Multiplier Scan
----------------

A pre-defined method that scans over a given range of multipliers and applies each of them to the constrained object provided.

.. note::

    Examples on how to use our pre-defined methods can be found in the Jupyter notebook examples on our `GitHub page <https://github.com/GQCG-res/GQCConstraints/tree/develop/examples>`_.
"""

# Import dependencies
import pandas as pd


def spinResolved(constrained_object, multiplier_grid, return_parameters=False, verbose=0):
    """
    A multiplier scan for resolved constrained methods.

    :param constrained_object:      The constrained object on which the multipliers will be applied.
    :param multiplier_grid:         The provided grid of multipliers.
    :param return_parameters:       A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param verbose:                 An integer representing the amount of output that will be printed.

    :returns:                       A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Set up a dataframe for the calculated data.
    output_data = pd.DataFrame({'alpha multipliers': multiplier_grid[0].flatten(), 'beta multipliers': multiplier_grid[1].flatten()})

    # Print a starting signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("             Scan over mu values started.               ")
        print("********************************************************")

    # Calculate the energy and population of the Hamiltonian constrained with the current mu value.
    output_array = output_data.apply(lambda row: constrained_object.calculateEnergyAndExpectationValue([row['alpha multipliers'], row['beta multipliers']], return_parameters=return_parameters, verbose=verbose), axis=1)

    # Save the output array elements in their respective locations in the data frame
    for i in range(len(output_array)):
        output_data.loc[i, 'energies'] = output_array[i][0]
        output_data.loc[i, constrained_object._constrained_alpha_observable + 's'] = output_array[i][1][0]
        output_data.loc[i, constrained_object._constrained_beta_observable + 's'] = output_array[i][1][1]
        output_data.loc[i, 'total ' + constrained_object._constrained_observable + 's'] = output_array[i][2]
        if return_parameters:
            output_data.loc[i, 'parameters'] = output_array[i][3]

    # Print a stopping signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("            Scan over mu values completed.              ")
        print("********************************************************")

    # Return the dataframe containing the mus, energies and populations.
    return output_data



def spinUnresolved(constrained_object, multipliers, return_parameters=False, verbose=0):
    """
    A multiplier scan for unresolved constrained methods.

    :param constrained_object:      The constrained object on which the multipliers will be applied.
    :param multipliers:             The provided range of multipliers.
    :param return_parameters:       A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param verbose:                 An integer representing the amount of output that will be printed.

    :returns:                       A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Set up a dataframe for the calculated data.
    output_data = pd.DataFrame({'multipliers': multipliers})

    # Print a starting signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("             Scan over mu values started.               ")
        print("********************************************************")
    
    # Calculate the energy and population of the Hamiltonian constrained with the current mu value.
    output_array = output_data.apply(lambda row: constrained_object.calculateEnergyAndExpectationValue(row['multipliers'], return_parameters=return_parameters, verbose=verbose), axis=1)

    # Save the output array elements in their respective locations in the data frame
    for i in range(len(output_array)):
        output_data.loc[i, 'energies'] = output_array[i][0]
        output_data.loc[i, constrained_object._constrained_observable + 's'] = output_array[i][1]
        if return_parameters:
             output_data.loc[i, 'parameters'] = output_array[i][2]

    # Print a stopping signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("            Scan over mu values completed.              ")
        print("********************************************************")

    # Return the dataframe containing the mus, energies and populations.
    return output_data
