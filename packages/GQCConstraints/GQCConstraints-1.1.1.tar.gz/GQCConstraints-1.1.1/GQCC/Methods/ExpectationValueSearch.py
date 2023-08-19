"""
Expectation Value Search
------------------------

A pre-defined methods that take a series of expectation values and optimize the multiplier for the constrained method at each one of them.

.. note::

    Examples on how to use our pre-defined methods can be found in the Jupyter notebook examples on our `GitHub page <https://github.com/GQCG-res/GQCConstraints/tree/develop/examples>`_.
"""

# Import dependencies
import pandas as pd


def spinResolved(constrained_object, optimization_function, expectation_value_grid, initial_alpha_guesses=None, initial_beta_guesses=None, return_parameters=False, threshold=1e-5, verbose=0, **options):
    """
    An optimization that optimizes the multiplier at each one of the provided expectation values, for the given constrained object.

    :param constrained_object:            The GQCC constrained object that will be used for the calculations.
    :param optimization_function:         The optimization function that will be used to optimize the multipliers. Can be a pre-defined function by GQCC or a self-implemented function that adheres to the same form.
    :param expectation_value_grid:        The series of expectation values at which the multiplier will be optimized.
    :param initial_alpha_guesses:         The series of initial guesses for the optimization, if required.
    :param initial_beta_guesses:          The series of initial guesses for the optimization, if required.
    :param return_parameters:             A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param threshold:                     The threshold at which the calculated and expected value are compared.
    :param verbose:                       An integer representing the amount of output that will be printed.
    :param options:                       The possible options that can be passed to the optimization function.

    :returns:                             A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Set up a dataframe for the calculated data.
    alpha_name = constrained_object._constrained_alpha_observable + 's'
    beta_name = constrained_object._constrained_beta_observable + 's'

    output_data = pd.DataFrame({alpha_name: expectation_value_grid[0].flatten(), beta_name: expectation_value_grid[1].flatten()})

    # Add the total expectation value to the dataframe.
    output_data['total ' + constrained_object._constrained_observable + 's'] = output_data[alpha_name].values + output_data[beta_name].values 

    # Print a starting signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("             Search for mu values started.              ")
        print("********************************************************")

    # In case of initial guesses, we need to make sure enough guesses are provided.
    if initial_alpha_guesses is not None:
        if len(initial_alpha_guesses) != len(expectation_value_grid[0].flatten()):
            raise Exception("The list of initial alpha guesses must be as long as the total number of calculations: i.e. (len(alpha_expectation_value_list) * len(beta_expectation_value_list)).")

    if initial_beta_guesses is not None:
        if len(initial_beta_guesses) != len(expectation_value_grid[1].flatten()):
            raise Exception("The list of initial beta guesses must be as long as the total number of calculations: i.e. (len(beta_expectation_value_list) * len(alpha_expectation_value_list)).")

    # Calculate the optimized mu value for the desired expectation value.
    if initial_alpha_guesses is not None and initial_beta_guesses is not None:
        # Add the guess lists (which are of equal dimensions due to lines 130-137) to the DataFrame.
        output_data['alpha_guesses'] = initial_alpha_guesses
        output_data['beta_guesses'] = initial_beta_guesses

        # Run the calculation with the initial guesses.
        output_array = output_data.apply(lambda row: constrained_object.optimizeMultiplier([row[alpha_name], row[beta_name]], optimization_function, [row['alpha_guesses'], row['beta_guesses']], **options), axis=1)

        # Delete the guess columns from the output data.
        output_data = output_data.drop(columns='alpha_guesses')
        output_data = output_data.drop(columns='beta_guesses')
    else:
        output_array = output_data.apply(lambda row: constrained_object.optimizeMultiplier([row[alpha_name], row[beta_name]], optimization_function, **options), axis=1)
        
    # Save the output array elements in their respective locations in the data frame
    for i in range(len(output_array)):
        output_data.loc[i, 'alpha multipliers'] = output_array[i][0]
        output_data.loc[i, 'beta multipliers'] = output_array[i][1]

    # Use the optimized mu to calculate the energy value.
    # We use the `verifyCombination` to check whether the multiplier belongs to the correct expectation value.
    # If verbose >= 2 the check will be printed.
    if return_parameters:
        output_array = output_data.apply(lambda row: constrained_object.verifyCombination([row['alpha multipliers'], row['beta multipliers']], [row[alpha_name], row[beta_name]], return_parameters=return_parameters, verbose=verbose, threshold=threshold), axis=1)
        for i in range(len(output_array)):
            output_data.loc[i, 'energies'] = output_array[i][0]
            output_data.loc[i, 'parameters'] = output_array[i][1]
    else:
        output_data['energies'] = output_data.apply(lambda row: constrained_object.verifyCombination([row['alpha multipliers'], row['beta multipliers']], [row[alpha_name], row[beta_name]], return_parameters=return_parameters, verbose=verbose, threshold=threshold), axis=1)

    # Print a stopping signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("            Search for mu values completed.             ")
        print("********************************************************")

    # Return the dataframe containing the mus, energies and expectation values.
    return output_data



def spinUnresolved(constrained_object, optimization_function, expectation_values, initial_guesses=None, return_parameters=False, threshold=1e-5, verbose=0, **options):
    """
    An optimization that optimizes the multiplier at each one of the provided expectation values, for the given constrained object.

    :param constrained_object:          The GQCC constrained object that will be used for the calculations.
    :param optimization_function:       The optimization function that will be used to optimize the multipliers. Can be a pre-defined function by GQCC or a self-implemented function that adheres to the same form.
    :param expectation_values:          The series of expectation values at which the multiplier will be optimized.
    :param initial_guesses:             The series of initial guesses for the optimization, if required.
    :param return_parameters:           A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param threshold:                   The threshold at which the calculated and expected value are compared.
    :param verbose:                     An integer representing the amount of output that will be printed.
    :param options:                     The possible options that can be passed to the optimization function.

    :returns:                           A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Set up a dataframe for the calculated data.
    output_data = pd.DataFrame({constrained_object._constrained_observable + 's': expectation_values})

    # Print a starting signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("             Search for mu values started.              ")
        print("********************************************************")

    # In case of initial guesses, we need to make sure enough guesses are provided.
    if initial_guesses is not None:
        if len(initial_guesses) != len(expectation_values):
            raise Exception("The list of initial guesses must be as long as the total number of calculations: i.e. len(expectation_values).")

    if initial_guesses is not None:
        # Add the guess list (which is of equal dimensions due to the previous clause) to the DataFrame.
        output_data['guesses'] = initial_guesses
            
        # Run the calculation with the initial guesses.
        output_data['multipliers'] = output_data.apply(lambda row: constrained_object.optimizeMultiplier(row[constrained_object._constrained_observable + 's'], optimization_function, row['guesses'], **options), axis=1)
            
        # Delete the guess column from the output data.
        output_data = output_data.drop(columns='guesses')

    else:
        # Calculate the optimized mu value for the desired expectation value.
        output_data['multipliers'] = output_data.apply(lambda row: constrained_object.optimizeMultiplier(row[constrained_object._constrained_observable + 's'], optimization_function, **options), axis=1)

    # Use the optimized mu to calculate the energy value.
    # We use the `verifyCombination` to check whether the multiplier belongs to the correct expectation value.
    # If verbose >= 2 the check will be printed.
    if return_parameters:
        output_array = output_data.apply(lambda row: constrained_object.verifyCombination(row['multipliers'], row[constrained_object._constrained_observable + 's'], return_parameters=return_parameters, threshold=threshold, verbose=verbose), axis=1)
        for i in range(len(output_array)):
            output_data.loc[i, 'energies'] = output_array[i][0]
            output_data.loc[i, 'parameters'] = output_array[i][1]
    else:
        output_data['energies'] = output_data.apply(lambda row: constrained_object.verifyCombination(row['multipliers'], row[constrained_object._constrained_observable + 's'], return_parameters=return_parameters, threshold=threshold, verbose=verbose), axis=1)

    # Print a stopping signal if verbose >= 1.
    if verbose >= 1:
        print("********************************************************")
        print("            Search for mu values completed.             ")
        print("********************************************************")

    # Return the dataframe containing the mus, energies and expectation values.
    return output_data
    