"""
Optimization Functions - Spin Unresolved
----------------------------------------

The pre-defined optimization functions for a expectation value search calculation in a spin unresolved constrained quantum chemical method framework.

If the user does not want to use these predefined functions, the possibility to add a self-defined optimization function is also provided within the library.

"""

# Import statements.
from scipy import optimize
import time


# Default optimization functions that can be used.
def Brent(estimated_expectation_value, constrained_method_setup, initial_guess=None, **options):
    """
    A line search optimization function.

    Note: Brent Line Search does not require an initial guess.

    :param estimated_expectation_value:         The expectation value for which you wish to optimize.
    :param constrainedMethodSetup:              The setup required to calculate the expectation value.
    :param options:                             The options that you want to pass to `optimize.golden` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize_scalar.html#scipy.optimize.minimize_scalar)

    :returns:                                   An optimized multiplier belonging to the estimated expectation value.
    """
    def objective_function(mu):
                
        # The constrained solver contains the necessary method to calculate the average expectation value.
        _, W = constrained_method_setup.calculateEnergyAndExpectationValue(mu)
        
        # We want to optimize the difference between the calculated and the expected expectation value. 
        # The square is used to make the function more well-behaved.
        return (W - estimated_expectation_value)**2
                
    optimized_mu = optimize.minimize_scalar(objective_function, **options)
    
    return optimized_mu.x


def GoldenLineSearch(estimated_expectation_value, constrained_method_setup, initial_guess=None, **options):
    """
    A line search optimization function.

    Note: Golden Line Search does not require an initial guess.

    :param estimated_expectation_value:         The expectation value for which you wish to optimize.
    :param constrainedMethodSetup:              The setup required to calculate the expectation value.
    :param options:                             The options that you want to pass to `optimize.golden` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.golden.html)

    :returns:                                   An optimized multiplier belonging to the estimated expectation value.
    """
    def objective_function(mu):
                
        # The constrained solver contains the necessary method to calculate the average expectation value.
        _, W = constrained_method_setup.calculateEnergyAndExpectationValue(mu)
        
        # We want to optimize the difference between the calculated and the expected expectation value. 
        # The square is used to make the function more well-behaved.
        return (W - estimated_expectation_value)**2
                
    optimized_mu = optimize.golden(objective_function, **options)
    
    return optimized_mu


# Default optimization functions that can be used.
def FSolve(estimated_expectation_value, constrained_method_setup, initial_guess=None, **options):
    """
    An optimization procedure that solves for the root of the objective function.

    :param estimated_expectation_value:         The expectation value for which you wish to optimize.
    :param constrainedMethodSetup:              The setup required to calculate the expectation value.
    :param options:                             The options that you want to pass to `optimize.fsolve` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html)

    :returns:                                   An optimized multiplier belonging to the estimated expectation value.
    """
    def objective_function(mu):
        
        # The constrained solver contains the necessary method to calculate the average expectation value.
        _, W = constrained_method_setup.calculateEnergyAndExpectationValue(mu[0])
        
        # We want to optimize the difference between the calculated and the expected expectation value. 
        # The square is used to make the function more well-behaved.
        return (W - estimated_expectation_value)
    
    # Root finding always requires a guess. If no guess is specified, we use 0.0.
    if initial_guess is None:
        guess = [0.0]
    else:
        guess = [initial_guess]           

    optimized_mu = optimize.fsolve(objective_function, x0=guess, **options)[0]
    
    return optimized_mu


def RootScalar(estimated_expectation_value, constrained_method_setup, initial_guess=None, **options):
    """
    A root finding function.

    Note: RootScalar does not require an initial guess.

    :param estimated_expectation_value:     The expectation value for which you wish to optimize.
    :param constrained_method_setup:        The setup required to calculate the expectation value.
    :param options:                         The options that you want to pass to `optimize.root_scalar` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root_scalar.html)

    :returns:                               A root representing an multiplier belonging to the estimated expectation value.
    """
    def objective_function(mu):
                
        # The constrained solver contains the necessary method to calculate the average expectation value.
        _, W = constrained_method_setup.calculateEnergyAndExpectationValue(mu)

        # We want to optimize the difference between the calculated and the expected expectation value.    
        return (W - estimated_expectation_value)
                
    optimized_mu = optimize.root_scalar(objective_function, x0=initial_guess, **options).root
    
    return optimized_mu


def Basinhopping(estimated_expectation_value, constrained_method_setup, initial_guess, **options):
    """
    A global optimization function that runs subsequent local optimizations at each step.

    Note: An initial guess is obligatory for basinhopping.

    :param estimated_expectation_value:     The expectation_value for which you wish to optimize.
    :param constrained_method_setup:        The setup required to calculate the expectation value.
    :param initial_guess:                   The initial guess for the basinhopping algorithm.
    :param options:                         The options that you want to pass to `optimize.minimize.basinhopping` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html#scipy.optimize.basinhopping)

    :returns:                               An optimized multiplier belonging to the estimated expectation value.
    """
    def objective_function(mu):        
        # Calculate the expectation values.
        _, W = constrained_method_setup.calculateEnergyAndExpectationValue(mu[0])

        # We want to optimize the difference between the calculated and the expected expectation_value. 
        # The square is used to make the function more well-behaved.
        return (W - estimated_expectation_value)**2
                
    # Use the global optimization algorithm `brute` in order to find the minimum.
    optimized = optimize.basinhopping(objective_function, x0=initial_guess, **options)
    
    return optimized.x[0]


def Bisect(estimated_expectation_value, constrained_method_setup, initial_guess=None, **options):
    """
    A Bisection algorithm that searches for the correct value in a pre-defined bracket.

    Note: It is obligatory to provide a bracket within the options dictionary.

    :param estimated_expectation_value:     The expectation_value for which you wish to optimize.
    :param constrained_method_setup:        The setup required to calculate the expectation value.
    :param initial_guess:                   The initial guess for the basinhopping algorithm.
    :param options:                         The options contain a bracket, the maximum_iterations, the tolerance and a boolean log parameter.

    :returns:                               An optimized multiplier belonging to the estimated expectation value.
    """

    # Define the bisection algorithm
    def _bisection_algorithm(objective_function, target_value, bracket=None, maximum_iterations=10000, tolerance=1e-4, log=False):
        # Timing for the calculation.
        start = time.time()

        # dictionary containing information about the optimization.
        infodict = {}

        # Number of iterations
        iter = 1

        # Unpack the bracket.
        if bracket is None:
            raise Exception("You need to specify a bracket")

        a, b = bracket[0], bracket[1]
        if (lower := objective_function(a)) > (upper := objective_function(b)):
            a, b = b, a
            lower, upper = upper, lower

        assert target_value >= lower - 0.1*tolerance, f"y is smaller than the lower bound. {target_value} < {lower}"
        assert target_value <= upper + 0.1*tolerance, f"y is larger than the upper bound. {target_value} > {upper}"

        # Time the optimization loops.
        loop_time = 0
  
        # Optimization loop.
        while iter <= maximum_iterations:
            loop_start = time.time()
            # Take the middle point of the bracket
            c = (a + b) / 2
            # If the function value of this point - the target value < the threshold, the algorithm finishes.
            if abs((y_c := objective_function(c)) - target_value) < tolerance:
                loop_end = time.time()
                loop_time += (loop_end-loop_start)
                average_loop_time = (loop_time / iter)
                end = time.time()
                infodict["number of iterations"] = iter
                infodict["average loop time (s)"] = average_loop_time
                infodict["total computation time (s)"] = (end-start)
                infodict['Optimized result'] = c

                # print the infodict if log is true.
                if log:
                    print("************************")
                    for key, value in infodict.items():
                        print(key, ' : ', value)
                    print("************************")
                return c
            # If the target value < function value of the middle point, repeat the process in the half bracket up to the function value.
            elif target_value < y_c:
                b, upper = c, y_c
                loop_end = time.time()
                loop_time += (loop_end - loop_start)
            # Otherwise, start the new bracket at the function value. 
            else:
                a, lower = c, y_c
                loop_end = time.time()
                loop_time += (loop_end - loop_start)
        
            # increase the number of iterations.
            iter += 1

        # If the maximum number of iterations is exceeded, print this info and return nothing.
        if iter > maximum_iterations: 
            print("Not converged within the maximally allowed number of iterations")
            return None

    def objective_function(mu):
                
        # The constrained solver contains the necessary method to calculate the average expectation value.
        _, W = constrained_method_setup.calculateEnergyAndExpectationValue(mu)

        # We want to optimize the difference between the calculated and the expected expectation value.    
        return W
                
    optimized_mu = _bisection_algorithm(objective_function, target_value=estimated_expectation_value, **options)
    
    return optimized_mu
