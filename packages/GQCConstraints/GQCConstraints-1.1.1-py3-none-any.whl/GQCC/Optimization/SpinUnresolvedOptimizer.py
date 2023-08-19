"""
Optimizer class for Optimizing a Spin Unresolved Parameter
----------------------------------------------------------

An `UnresolvedOptimizer` contains standard optimization routines used by each of the spin-unresolved quantum chemical methods. 
    
Each of those methods overwrites this empty constructor with its own and is able to call the optimization functionalities of this class.
"""

import numpy as np
import math as m

class SpinUnresolvedOptimizer:
    """
    An `UnresolvedOptimizer` contains standard optimization routines used by each of the spin-unresolved quantum chemical methods. 
    
    Each of those methods overwrites this empty constructor with its own and is able to call the optimization functionalities of this class.
    """
    def __init__(self):
        pass


    def optimizeMultiplier(self, expectation_value, optimize_function, initial_guess=None, **options):
        """
        A method that uses an `optimize_function` to optimize the multiplier value belonging to a specified expectation value.

        Note:                            Optimize function must always take the expectation value and the solver itself as an argument, and returns the optimized mu value.

        Note:                            It is possible to write an optimize function that takes an initial guess.

        :param expectation value:        The expectation value value for which we want to find the multiplier.
        :param optimize_function:        The optimize function used for finding the mu value. 
        :param options:                  The possible options that can be passed to the optimization function.
        
        :returns:                        The optimized mu value.

        To optimize a Lagrange multiplier to yield a certain expectation value (0.5) we can all this method.

        .. code-block:: python

            optimized_mu = Constrained_object.optimizeMultiplier(0.5, GQCC.SpinUnresolvedOptimizationFunctions.GoldenLineSearch)

        This can be done with any spin-unresolved optimization function and the preferred options associated with that function.
        """
        # We can modify the optimize_function at will, as long as it takes the same arguments and returns an optimized mu value
        optimized_mu = optimize_function(expectation_value, self, initial_guess, **options)
       
        return optimized_mu
        
        
    def verifyCombination(self, optimized_mu, expected_value, return_parameters=False, threshold=1e-5, verbose=0):
        """
        A method used to check whether the multiplier found corresponds to the expected value.

        :param optimized_mu:            The optimized mu found with an optimization function.
        :param expected_value:          The expectation value expected at the optimized mu value.
        :param return_parameters:       A boolean flag to indicate whether only the wavefunction parameters should also be returned.
        :param threshold:               The threshold at which the calculated and expected value are compared.
        :param verbose:                 An integer representing the amount of output that will be printed.

        :returns:                       The energy belonging to the multiplier/expectation value combination. If the expected and calculated expectation values don't match, None is returned.
        :returns:                       The ground state parameters belonging to the multiplier/expectation value combination. If the expected and calculated expectation values don't match, None is returned (only if return_parameters is set to True).

        If you ran an optimization calculation, it is imperative to check whether or not your optimization was successful and does indeed result in the wanted expectation value, i.e. 0.5. To do so call this method with your optimized multiplier.

        .. code-block:: python

            energy = Constrained_object.verifyCombination(optimized_mu, 0.5)
        """
        if return_parameters:
            E, W, par = self.calculateEnergyAndExpectationValue(optimized_mu, return_parameters)
        else:
            E, W = self.calculateEnergyAndExpectationValue(optimized_mu, return_parameters)
    
        if m.isclose(W, expected_value, abs_tol=threshold):
            if verbose >= 2:
                print("--------------------------------------------------------")
                print("The found mu value leads to the expected " + self._constrained_observable + " :")
                print("--------------------------------------------------------")
                print("Calculated " + self._constrained_observable + " : " + str(np.around(W, 5))) 
                print("Expected " + self._constrained_observable + " : ", np.around(expected_value, 5))
        else:
            if verbose >= 2:
                print("--------------------------------------------------------")
                print("The found mu value leads to the wrong " + self._constrained_observable + " :")
                print("--------------------------------------------------------")
                print("Calculated " + self._constrained_observable + " : " + str(np.around(W, 5))) 
                print("Expected " + self._constrained_observable + " : ", np.around(expected_value, 5))
            if return_parameters:
                E = np.nan 
                par = np.nan
            else:
                E = np.nan

        # Print the progress of which mu values have been completed if verbose >= 3.
        if verbose >= 3:
            print("--------------------------------------------------------")
            print(self._constrained_observable + " = " + str(np.around(expected_value, 2)) + " done.")

        if return_parameters:    
            return E, par
        else:
            return E
