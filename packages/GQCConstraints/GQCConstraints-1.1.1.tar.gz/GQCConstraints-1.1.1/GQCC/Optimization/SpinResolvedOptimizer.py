"""
Optimizer class for Optimizing a Spin Resolved Parameter
---------------------------------------------------------

A `ResolvedOptimizer` contains standard optimization routines used by each of the spin-resolved quantum chemical methods. 
    
Each of those methods overwrites this empty constructor with its own and is able to call the optimization functionalities of this class.
"""

import numpy as np
import math as m

class SpinResolvedOptimizer:

    def __init__(self):
        pass


    def optimizeMultiplier(self, value_array, optimize_function, initial_guess=None, **options):
        """
        A method that uses an `optimize_function` to optimize the multiplier value belonging to a specified expectation value.

        Note:                            Optimize function must always take the expectation value and the solver itself as an argument, and returns the ground state energy and the optimized mu value.
        
        Note:                            It is possible to write an optimize function that takes an initial guess.

        :param value_array:              The expectation value for which we want to find the multiplier.
        :param optimize_function:        The optimize function used for finding the mu value.
        :param initial_guess:            The initial guess for the optimization. If `None` a guess is chosen for you (default). 
        :param options:                  The possible options that can be passed to the optimization function.
        
        :returns:                        The optimized mu values for alpha and beta.

        To optimize a set of Lagrange multipliers to yield a certain expectation value for alpha and beta (0.5 and 0.0) we can all this method.

        .. code-block:: python

            optimized_mu = Constrained_object.optimizeMultiplier([0.5, 0.0], GQCC.SpinResolvedOptimizationFunctions.GlobalBrute, ranges=((-1, 1), (-1, 1)), Ns=100)

        .. note::

            `optimized_mu` is an array that looks like this: `[optimized_alpha_mu, optimized_beta_mu]`.

        This can be done with any spin-resolved optimization function and the preferred options associated with that function.
        """
        # Raise an exception if the multiplier is not conform with the requirements.
        if type(value_array) is float or len(value_array) != 2:
             raise ValueError("Value_array must be of dimension 2 as it must contain both an alpha and beta value.")

        if initial_guess is not None and (type(initial_guess) is float or len(value_array) != 2):
             raise ValueError("Initial guess must be None or must be of dimension 2 as it must contain both an alpha and beta value.")

        # We can modify the optimize_function at will, as long as it takes the same arguments and returns an optimized mu value
        optimized_mu = optimize_function([value_array[0], value_array[1]], self, initial_guess, **options)
       
        return optimized_mu
        
        
    def verifyCombination(self, optimized_mu, expected_value_array, return_parameters=False, threshold=1e-5, verbose=0):
        """
        A method used to check whether the multiplier found corresponds to the expected expectation values.

        :param optimized_mu:                       The optimized mu found with an optimization function.
        :param expected_value_array:               The expectation values values expected at the optimized mu values for both alpha and beta.
        :return_parameters:                        A boolean flag that specifies whether the wavefunction parameters are also returned.
        :param threshold:                          The threshold at which the calculated and expected values are compared.
        :param verbose:                            An integer representing the amount of output that will be printed.

        :returns:                                  The energy belonging to the multiplier/expectation value combination. If the expected and calculated values don't match, None is returned.

        If you ran an optimization calculation, it is imperative to check whether or not your optimization was successful and does indeed result in the wanted expectation values, i.e. 0.5 and 0.0. To do so call this method with your optimized multiplier.

        .. code-block:: python

            energy = Constrained_object.verifyCombination([optimized_alpha_mu, optimized_beta_mu], [0.5, 0.0])
        """
        # Raise an exception if the multiplier is not conform with the requirements.
        if type(expected_value_array) is float or len(expected_value_array) != 2:
             raise ValueError("Expected_value_array must be of dimension 2 as it must contain both an alpha and beta value.")

        if return_parameters:
            E, spinResolved_W, _, par = self.calculateEnergyAndExpectationValue(optimized_mu, return_parameters)
        else:
            E, spinResolved_W, _ = self.calculateEnergyAndExpectationValue(optimized_mu, return_parameters)
    
        if m.isclose(spinResolved_W[0], expected_value_array[0], abs_tol=threshold) and m.isclose(spinResolved_W[1], expected_value_array[1], abs_tol=threshold):
            if verbose >= 2:
                print("-----------------------------------------------------------------------------------------------")
                print("The found mu value leads to the expected " + self._constrained_alpha_observable + " and " + self._constrained_beta_observable + " :")
                print("-----------------------------------------------------------------------------------------------")
                print("Calculated " + self._constrained_alpha_observable + ": " + str(np.around(spinResolved_W[0], 5)) + "; Calculated " + self._constrained_beta_observable + ": "+ str(np.around(spinResolved_W[1], 5))) 
                print("Expected " + self._constrained_alpha_observable + ": ", np.around(expected_value_array[0], 5), "; Expected " + self._constrained_beta_observable + ": ", np.around(expected_value_array[1], 5))
        else:
            if verbose >= 2:
                print("-----------------------------------------------------------------------------------------------")
                print("The found mu value leads to the wrong " + self._constrained_alpha_observable + " and/or " + self._constrained_beta_observable + " :")
                print("-----------------------------------------------------------------------------------------------")
                print("Calculated " + self._constrained_alpha_observable + ": " + str(np.around(spinResolved_W[0], 5)) + "; Calculated " + self._constrained_beta_observable + ": "+ str(np.around(spinResolved_W[1], 5))) 
                print("Expected " + self._constrained_alpha_observable + ": ", np.around(expected_value_array[0], 5), "; Expected " + self._constrained_beta_observable + ": ", np.around(expected_value_array[1], 5))
            if return_parameters:
                E = np.nan 
                par = np.nan
            else:
                E = np.nan

        # Print the progress of which mu values have been completed if verbose >= 3.
        if verbose >= 3:
            print("-----------------------------------------------------------------------------------------------")
            print(self._constrained_observable + " combo: alpha = " + str(np.around(expected_value_array[0], 2)) + " , beta = " + str(np.around(expected_value_array[1], 2)) + " done.")

        if return_parameters:    
            return E, par
        else:
            return E
