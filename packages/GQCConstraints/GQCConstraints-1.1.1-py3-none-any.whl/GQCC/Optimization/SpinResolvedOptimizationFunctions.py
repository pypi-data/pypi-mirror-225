"""
Optimization Functions - Spin Resolved
--------------------------------------

The pre-defined optimization functions for a expectation value search calculation in a spin resolved constrained quantum chemical method framework.

If the user does not want to use these predefined functions, the possibility to add a self-defined optimization function is also provided within the library.

"""

# Import statements.
from scipy import optimize
import numpy as np

# Default optimization functions that can be used.
def NelderMead(expected_expectation_value_array, constrained_method_setup, initial_guess=None, **options):
    """
    A line search optimization function in two parameters.

    Note: An initial guess is optional for Nelder Mead optimization.

    :param expected_expectation_value:     The expectation value for which you wish to optimize.
    :param constrained_method_setup:       The setup required to calculate the expectation value.
    :param initial_guess:                  An optional initial guess for the optimization algorithm.
    :param options:                        The options that you want to pass to `optimize.minimize(method="Nelder-Mead)` (https://docs.scipy.org/doc/scipy/reference/optimize.minimize-neldermead.html)

    :returns:                       An array containing an optimized alpha and beta multiplier.
    """
    def objective_function(mu):
        # Unpack the parameter to be optimized.     
        mua, mub = mu
        
        # Calculate the expectation values.
        _, spinResolved_W, _ = constrained_method_setup.calculateEnergyAndExpectationValue([mua, mub])

        # Create a delta N array. Squares are used to make the function more well behaved.  
        delta_N = np.array([(spinResolved_W[0] - expected_expectation_value_array[0]) ** 2, (spinResolved_W[1] - expected_expectation_value_array[1]) ** 2])
                    
        return (delta_N.T @ delta_N) ** 2
    
    # Nelder Mead always requires a guess. If no guess is specified, we use 0.5, multiplied by a value depending on the expectation value region.
    if initial_guess is None:
        guess = [0.5, 0.5]

        if (expected_expectation_value_array[0] + expected_expectation_value_array[1]) <= 1:
            optimized = optimize.minimize(objective_function, [guess[0]*-1, guess[1]*-1], method='Nelder-Mead', **options)
        elif (expected_expectation_value_array[0] + expected_expectation_value_array[1]) <= 2:
            optimized = optimize.minimize(objective_function, guess, method='Nelder-Mead', **options)
        elif (expected_expectation_value_array[0] + expected_expectation_value_array[1]) <= 3:
            optimized = optimize.minimize(objective_function, [guess[0]*2, guess[1]*2], method='Nelder-Mead', **options)
        else:
            optimized = optimize.minimize(objective_function, [guess[0]*3, guess[1]*3], method='Nelder-Mead', **options)

    # If a guess is specified, we just use that guess.
    else:
        guess = initial_guess
        optimized = optimize.minimize(objective_function, guess, method='Nelder-Mead', **options)

    return optimized.x


def Root(expected_expectation_value_array, constrained_method_setup, initial_guess=None, **options):
    """
    A root finding optimization function in two parameters.

    Note: An initial guess is optional for root finding.

    :param expected_expectation_value:     The expectation value for which you wish to optimize.
    :param constrained_method_setup:       The setup required to calculate the expectation value.
    :param initial_guess:                  An optional initial guess for the root finder.
    :param options:                        The options that you want to pass to `optimize.minimize.root` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html)

    :returns:                              An array containing the roots of the objective function, representing an optimized alpha and beta multiplier.
    """
    def objective_function(mu):
        # Unpack the parameter to be optimized.     
        mua, mub = mu
        
        # Calculate the expectation values.
        _, spinResolved_W, _ = constrained_method_setup.calculateEnergyAndExpectationValue([mua, mub])

        # Create a delta N array. Squares are used to make the function more well behaved.  
        delta_N = np.array([(spinResolved_W[0] - expected_expectation_value_array[0]) ** 2, (spinResolved_W[1] - expected_expectation_value_array[1]) ** 2])   
                    
        return delta_N

    # Root finding always requires a guess. If no guess is specified, we use 0.0.
    if initial_guess is None:
        guess = [0.0, 0.0]
    else:
        guess = initial_guess           

    # Use Root finding to optimize the function       
    optimized = optimize.root(objective_function, x0=guess, **options)
    
    return optimized.x


def FSolve(expected_expectation_value_array, constrained_method_setup, initial_guess=None, **options):
    """
    A root finding optimization function in two parameters.

    Note: An initial guess is optional for root finding.

    :param expected_expectation_value:     The expectation value for which you wish to optimize.
    :param constrained_method_setup:       The setup required to calculate the expectation value.
    :param initial_guess:                  An optional initial guess for the root finder.
    :param options:                        The options that you want to pass to `optimize.fsolve` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html)

    :returns:                              An array containing the roots of the objective function, representing an optimized alpha and beta multiplier.
    """
    def objective_function(mu):
        # Unpack the parameter to be optimized.     
        mua, mub = mu
        
        # Calculate the expectation values.
        _, spinResolved_W, _ = constrained_method_setup.calculateEnergyAndExpectationValue([mua, mub])

        # Create a delta N array. 
        delta_N = np.array([(spinResolved_W[0] - expected_expectation_value_array[0]), (spinResolved_W[1] - expected_expectation_value_array[1])])   
                    
        return delta_N

    # Root finding always requires a guess. If no guess is specified, we use 0.0.
    if initial_guess is None:
        guess = [0.0, 0.0]
    else:
        guess = initial_guess           

    # Use fsolve finding to optimize the function       
    optimized = optimize.fsolve(objective_function, x0=guess, **options)
    
    return optimized


def GlobalBrute(expected_expectation_value_array, constrained_method_setup, initial_guess=None, **options):
    """
    A global optimization function in two parameters.

    Note: Brute optimization never requires an initial guess. The parameter is only provided to not cause an error.

    :param expected_expectation_value:     The expectation value for which you wish to optimize.
    :param constrained_method_setup:       The setup required to calculate the expectation value.
    :param options:                        The options that you want to pass to `optimize.optimize.brute` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.brute.html)

    :returns:                              An array containing an optimized alpha and beta multiplier.
    """
    def objective_function(mu):
        # Unpack the parameter to be optimized.     
        mua, mub = mu
        
        # Calculate the expectation values.
        _, spinResolved_W, _ = constrained_method_setup.calculateEnergyAndExpectationValue([mua, mub])

        # Create a delta N array. Squares are used to make the function more well behaved.  
        delta_N = np.array([(spinResolved_W[0] - expected_expectation_value_array[0]) ** 2, (spinResolved_W[1] - expected_expectation_value_array[1]) ** 2])
                    
        return delta_N.T @ delta_N
                
    # Use the global optimization algorithm `brute` in order to find the minimum.
    optimized = optimize.brute(objective_function, **options)
    
    return optimized


def Basinhopping(expected_expectation_value_array, constrained_method_setup, initial_guess, **options):
    """
    A global optimization function that runs subsequent local optimizations at each step.

    Note: An initial guess is obligatory for basinhopping.

    :param expected_expectation_value:     The expectation value for which you wish to optimize.
    :param constrained_method_setup:       The setup required to calculate the expectation value.
    :param initial_guess:                  The initial guess for the basinhopping algorithm.
    :param options:                        The options that you want to pass to `optimize.minimize.basinhopping` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html#scipy.optimize.basinhopping)

    :returns:                              An array containing the roots of the objective function, representing an optimized alpha and beta multiplier.
    """
    def objective_function(mu):
        # Unpack the parameter to be optimized.     
        mua, mub = mu
        
        # Calculate the expectation values.
        _, spinResolved_W, _ = constrained_method_setup.calculateEnergyAndExpectationValue([mua, mub])

        # Create a delta N array. Squares are used to make the function more well behaved.  
        delta_N = np.array([(spinResolved_W[0] - expected_expectation_value_array[0]) ** 2, (spinResolved_W[1] - expected_expectation_value_array[1]) ** 2])
                    
        return delta_N.T @ delta_N
                
    # Use the global optimization algorithm `brute` in order to find the minimum.
    optimized = optimize.basinhopping(objective_function, x0=initial_guess, **options)
    
    return optimized.x
