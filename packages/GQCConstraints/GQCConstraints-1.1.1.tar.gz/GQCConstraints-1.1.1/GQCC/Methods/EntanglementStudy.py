"""
Entanglement Study
------------------

.. warning::

    The entanglement study method is only implemented for constrained calculations applied to the **Hubbard Model**. 

A pre-defined methods that can be used to study the entanglement between subsystems and the environment.

.. note::

    Examples on how to use our pre-defined methods can be found in the Jupyter notebook examples on our `GitHub page <https://github.com/GQCG-res/GQCConstraints/tree/develop/examples>`_.

"""

# Import dependencies
import pandas as pd
import GQCC.Methods.MultiplierScan as scan
import GQCC.Methods.ExpectationValueSearch as search


def ofSpinResolvedExpectationValueSearch(constrained_object, optimization_function, expectation_value_grid, domain_partition_p, domain_partition_q, domain_partition_pq, initial_alpha_guesses=None, initial_beta_guesses=None, return_parameters=False, threshold=1e-5, verbose=0, **options):
    """
    An optimization that optimizes the multiplier at each one of the provided expectation values, for the given constrained object.

    :param constrained_object:          The GQCC constrained object that will be used for the calculations.
    :param optimization_function:       The optimization function that will be used to optimize the multipliers. Can be a pre-defined function by GQCC or a self-implemented function that adheres to the same form.
    :param expectation_value_grid:      The series of expectation values at which the multiplier will be optimized.
    :param domain_partition_p:          The domain partition for the first domain.
    :param domain_partition_q:          The domain partition for the second domains.
    :param domain_partition_pq:         The domain partition of the first and second domain combined.
    :param initial_alpha_guesses:       The series of initial guesses for the optimization, if required.
    :param initial_beta_guesses:        The series of initial guesses for the optimization, if required.
    :param return_parameters:           A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param threshold:                   The threshold at which the calculated and expected value are compared.
    :param verbose:                     An integer representing the amount of output that will be printed.
    :param options:                     The possible options that can be passed to the optimization function.

    :returns:                           A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Start with an unresolved expectation value search, which returns the parameters.
    if initial_alpha_guesses is not None and initial_beta_guesses is not None:
        resolved_search_output = search.spinResolved(constrained_object, optimization_function, expectation_value_grid, initial_alpha_guesses=initial_alpha_guesses, initial_beta_guesses=initial_beta_guesses, return_parameters=True, threshold=threshold, verbose=verbose, **options)
    elif initial_alpha_guesses is None and initial_beta_guesses is None:
        resolved_search_output = search.spinResolved(constrained_object, optimization_function, expectation_value_grid, return_parameters=True, threshold=threshold, verbose=verbose, **options)
    else:
        raise Exception("If a Guess is provided, it needs to be provided for both the alpha and beta parameters. Otherwise, no guess should be supplied for either.")

    if verbose >= 1: 
        print("*****************************************************")
        print("             Start entanglement study.               ")
        print("*****************************************************")

    # Subsequently use those parameters in combination with the domain partitions to calculate the entropic measures.
    resolved_search_output['Sp'] = resolved_search_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_p, row['parameters']), axis=1)
    resolved_search_output['Sq'] = resolved_search_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_q, row['parameters']), axis=1)
    resolved_search_output['Spq'] = resolved_search_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_pq, row['parameters']), axis=1)
    resolved_search_output['mutual information'] = resolved_search_output.apply(lambda row: constrained_object.mutualInformation(domain_partition_p, domain_partition_q, domain_partition_pq, row['parameters']), axis=1)

    if verbose >= 1:
        print("*******************************************************")
        print("            Entanglement study completed.              ")
        print("*******************************************************")

    # If return parameters is set to `True` the column is kept. Otherwise it is dropped before returning the dataframe.
    if return_parameters:
        return resolved_search_output
    else:
        resolved_search_output = resolved_search_output.drop(columns='parameters')
        return resolved_search_output


def ofSpinResolvedMultiplierScan(constrained_object, multiplier_grid, domain_partition_p, domain_partition_q, domain_partition_pq, return_parameters=False, verbose=0):
    """
    An entanglement study of a multiplier scan for unresolved constrained Hubbard methods.

    :param constrained_object:      The constrained object on which the multipliers will be applied.
    :param multiplier_grid:         The provided grid of multipliers.
    :param domain_partition_p:      The domain partition for the first domain.
    :param domain_partition_q:      The domain partition for the second domains.
    :param domain_partition_pq:     The domain partition of the first and second domain combined.
    :param return_parameters:       A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param verbose:                 An integer representing the amount of output that will be printed.

    :returns:                       A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Start with an unresolved mu scan, which returns the parameters.
    resolved_scan_output = scan.spinResolved(constrained_object, multiplier_grid, return_parameters=True, verbose=verbose)

    if verbose >= 1:
        print("*****************************************************")
        print("             Start entanglement study.               ")
        print("*****************************************************")

    # Subsequently use those parameters in combination with the domain partitions to calculate the entropic measures.
    resolved_scan_output['Sp'] = resolved_scan_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_p, row['parameters']), axis=1)
    resolved_scan_output['Sq'] = resolved_scan_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_q, row['parameters']), axis=1)
    resolved_scan_output['Spq'] = resolved_scan_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_pq, row['parameters']), axis=1)
    resolved_scan_output['mutual information'] = resolved_scan_output.apply(lambda row: constrained_object.mutualInformation(domain_partition_p, domain_partition_q, domain_partition_pq, row['parameters']), axis=1)

    if verbose >= 1:
        print("*******************************************************")
        print("            Entanglement study completed.              ")
        print("*******************************************************")

    # If return parameters is set to `True` the column is kept. Otherwise it is dropped before returning the dataframe.
    if return_parameters:
        return resolved_scan_output
    else:
        resolved_scan_output = resolved_scan_output.drop(columns='parameters')
        return resolved_scan_output


def ofSpinUnresolvedExpectationValueSearch(constrained_object, optimization_function, expectation_values, domain_partition_p, domain_partition_q, domain_partition_pq, initial_guesses=None, return_parameters=False, threshold=1e-5, verbose=0, **options):
    """
    An optimization that optimizes the multiplier at each one of the provided expectation values, for the given constrained object.

    :param constrained_object:          The GQCC constrained object that will be used for the calculations.
    :param optimization_function:       The optimization function that will be used to optimize the multipliers. Can be a pre-defined function by GQCC or a self-implemented function that adheres to the same form.
    :param expectation_values:          The series of expectation values at which the multiplier will be optimized.
    :param domain_partition_p:          The domain partition for the first domain.
    :param domain_partition_q:          The domain partition for the second domains.
    :param domain_partition_pq:         The domain partition of the first and second domain combined.
    :param initial_guesses:             The series of initial guesses for the optimization, if required.
    :param return_parameters:           A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param threshold:                   The threshold at which the calculated and expected value are compared.
    :param verbose:                     An integer representing the amount of output that will be printed.
    :param options:                     The possible options that can be passed to the optimization function.

    :returns:                           A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Start with an unresolved expectation value search, which returns the parameters.
    if initial_guesses is not None:
        unresolved_search_output = search.spinUnresolved(constrained_object, optimization_function, expectation_values, initial_guesses=initial_guesses, return_parameters=True, threshold=threshold, verbose=verbose, **options)
    else:
        unresolved_search_output = search.spinUnresolved(constrained_object, optimization_function, expectation_values, return_parameters=True, threshold=threshold, verbose=verbose, **options)

    if verbose >= 1: 
        print("*****************************************************")
        print("             Start entanglement study.               ")
        print("*****************************************************")

    # Subsequently use those parameters in combination with the domain partitions to calculate the entropic measures.
    unresolved_search_output['Sp'] = unresolved_search_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_p, row['parameters']), axis=1)
    unresolved_search_output['Sq'] = unresolved_search_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_q, row['parameters']), axis=1)
    unresolved_search_output['Spq'] = unresolved_search_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_pq, row['parameters']), axis=1)
    unresolved_search_output['mutual information'] = unresolved_search_output.apply(lambda row: constrained_object.mutualInformation(domain_partition_p, domain_partition_q, domain_partition_pq, row['parameters']), axis=1)

    if verbose >= 1:
        print("*******************************************************")
        print("            Entanglement study completed.              ")
        print("*******************************************************")

    # If return parameters is set to `True` the column is kept. Otherwise it is dropped before returning the dataframe.
    if return_parameters:
        return unresolved_search_output
    else:
        unresolved_search_output = unresolved_search_output.drop(columns='parameters')
        return unresolved_search_output


def ofSpinUnresolvedMultiplierScan(constrained_object, multipliers, domain_partition_p, domain_partition_q, domain_partition_pq, return_parameters=False, verbose=0):
    """
    An entanglement study of a multiplier scan for unresolved constrained Hubbard methods.

    :param constrained_object:      The constrained object on which the multipliers will be applied.
    :param multipliers:             The provided range of multipliers.
    :param domain_partition_p:      The domain partition for the first domain.
    :param domain_partition_q:      The domain partition for the second domains.
    :param domain_partition_pq:     The domain partition of the first and second domain combined.
    :param return_parameters:       A boolean flag to indicate whether only the wavefunction parameters should also be returned.
    :param verbose:                 An integer representing the amount of output that will be printed.

    :returns:                       A pandas dataframe in which the calculated data is cleanly stored.
    """
    # Start with an unresolved mu scan, which returns the parameters.
    unresolved_scan_output = scan.spinUnresolved(constrained_object, multipliers, return_parameters=True, verbose=verbose)

    if verbose >= 1:
        print("*****************************************************")
        print("             Start entanglement study.               ")
        print("*****************************************************")

    # Subsequently use those parameters in combination with the domain partitions to calculate the entropic measures.
    unresolved_scan_output['Sp'] = unresolved_scan_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_p, row['parameters']), axis=1)
    unresolved_scan_output['Sq'] = unresolved_scan_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_q, row['parameters']), axis=1)
    unresolved_scan_output['Spq'] = unresolved_scan_output.apply(lambda row: constrained_object.vonNeumannEntropy(domain_partition_pq, row['parameters']), axis=1)
    unresolved_scan_output['mutual information'] = unresolved_scan_output.apply(lambda row: constrained_object.mutualInformation(domain_partition_p, domain_partition_q, domain_partition_pq, row['parameters']), axis=1)

    if verbose >= 1:
        print("*******************************************************")
        print("            Entanglement study completed.              ")
        print("*******************************************************")

    # If return parameters is set to `True` the column is kept. Otherwise it is dropped before returning the dataframe.
    if return_parameters:
        return unresolved_scan_output
    else:
        unresolved_scan_output = unresolved_scan_output.drop(columns='parameters')
        return unresolved_scan_output
