"""
Spin Unresolved Constraints - UHF
----------------------------------

This module is used for constraining spin-unresolved operators in unrestricted Hartree-Fock calculations. By setting up the constrained UHF object, the module prepares the basic functionalities to run constrained calculations for single values or to be used in one of the pre-set methods offered by GQCC.

"""

# Import statements
import gqcpy
import numpy as np
import numpy.random as rand

from GQCC.Optimization.SpinUnresolvedOptimizer import SpinUnresolvedOptimizer


class UHF(SpinUnresolvedOptimizer):
    """
    A constructor that sets up everything needed for constrained UHF calculations.

    :param molecule:                    The GQCP molecule used for the calculations.
    :param electrons:                   The amount of alpha and beta electrons in the molecule as an array.
    :param SQ_basis:                    The second quantized GQCP basis set used for the calculations, defined for a molecule in a certain basis set. Make sure it is the same basis as in which the operator is defined.
    :param solver:                      The solver used for the UHF calculations.
    :param initial_guess:               The initial guess for the UHF calculation.
    :param operator:                    The GQCP operator that will be constrained.     
    :param constrained_observable:      The name of the observable being constrained.
    :param stability_analysis:          Boolean flag denoting whether stability analysis is performed. Default is `True`.
    :param stability_scaling_factor:    The scaling factor for constructing the stability rotation matrix when internal instabilities are found.
    :param stability_output:            Boolean flag on whether to print the outpuut of the stability analysis or not. Default is `False`.

    :returns:                           An object which contains all required data (basis, Hamiltonian,... ) and possesses the necessary methods to perform calculations.

    In order to set up a UHF calculation with spin resolved constraints we need several GQCP elements. First, set up some basic variables.

    .. code-block:: python

        H2 =  gqcpy.Molecule.HChain(2, 2.5, 0)                                                      # The molecule.
        electrons = [1,1]                                                                           # The number of alpha and beta electrons.
        basis = gqcpy.USpinOrbitalBasis_d(H2, "6-31G")                                              # The spin orbital basis.
        solver = gqcpy.UHFSCFSolver_d.Plain(threshold=1e-6, maximum_number_of_iterations=250000)    # The solver for the Hartree-Fock algorithm.

    We also need to give the object an initial guess for the SCF procedure. In this case, let's generate a random symmetric guess that's different for alpha and beta.

    .. code-block:: python

        import numpy.random as rand

        rand.seed(2)
        random_matrix_alpha = np.random.rand(basis.numberOfSpinors() // 2, basis.numberOfSpinors() // 2)
        random_matrix_alpha_transpose = random_matrix_alpha.T
        symmetric_random_matrix_alpha = random_matrix_alpha + random_matrix_alpha_transpose
        _, alpha_guess = np.linalg.eigh(symmetric_random_matrix_alpha)

        rand.seed(3)
        random_matrix_beta = np.random.rand(basis.numberOfSpinors() // 2, basis.numberOfSpinors() // 2)
        random_matrix_beta_transpose = random_matrix_beta.T
        symmetric_random_matrix_beta = random_matrix_beta + random_matrix_beta_transpose
        _, beta_guess = np.linalg.eigh(symmetric_random_matrix_beta)

        guess = gqcpy.UTransformation_d(gqcpy.UTransformationComponent_d(alpha_guess), gqcpy.UTransformationComponent_d(beta_guess))

    Now we choose an operator to constrain. Let's set up an :math:`S^2` operator product.

    .. code-block:: python

        S = basis.quantize(gqcpy.ElectronicSpinSquaredOperator())

    The construction of the constrained object can now be done with GQCC.

    .. code-block:: python

        Constrained_object = GQCC.SpinUnresolvedConstraints.UHF(H2, electrons, basis, solver, guess, S, "population")
    """
    def __init__(self, molecule, electrons, SQ_basis, solver, initial_guess, operator, constrained_observable, stability_analysis=True, stability_scaling_factor=1.0, stability_output=False):
        # Raise an exception if the electrons array is not conform with the requirements.
        if type(electrons[0]) is float or type(electrons[1]) is float or len(electrons) != 2:
            raise ValueError("Electrons must be of dimension 2 and must contain two ìnt`s as it must contain the number of alpha and beta electrons.")
        
        # Check compatibility of the operator type based on the used basis type.
        if type(SQ_basis) is gqcpy.gqcpy.USpinOrbitalBasis_d:
            compatible_operators = [gqcpy.gqcpy.ScalarUSQOneElectronOperator_d, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_d]
            assert (type(solver) is gqcpy.gqcpy.IterativeAlgorithm_UHFSCFEnvironment)

        elif type(SQ_basis) is gqcpy.gqcpy.USpinOrbitalBasis_cd:
            compatible_operators = [gqcpy.gqcpy.ScalarUSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_cd, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_cd]
            assert (type(solver) is gqcpy.gqcpy.IterativeAlgorithm_UHFSCFEnvironment_cd)

        else:
            raise ValueError("the chosen `SQ_basis` or `solver` is not compatible with this type of calculation. Use `gqcpy.USpinOrbitalBasis_(c)d`instead.")
        assert (type(operator) in compatible_operators), "Only `ScalarUSQOneElectronOperator_(c)d` or `ScalarUSQTwoElectronOperator_(c)d` can be constrained with this method."     

        # This basis can now quantize the Hamiltonian.
        self._sq_hamiltonian = SQ_basis.quantize(gqcpy.FQMolecularHamiltonian(molecule))

        # We will need the number of electrons, as well as the total number of Spinors later on.        
        self._K = SQ_basis.numberOfSpinors() // 2
        self._Ka = self._K
        self._Kb = self._K

        self._Na = electrons[0]
        self._Nb = electrons[1]

        # Save the overlap and nuclear repulsion operators. 
        self._nuclear_repulsion = gqcpy.NuclearRepulsionOperator(molecule.nuclearFramework()).value()
        self._overlap = SQ_basis.quantize(gqcpy.OverlapOperator())

        # Save the operator you want to constrain.
        self._operator = operator

        self._constrained_observable = constrained_observable
        self._constrained_alpha_observable = "alpha " + self._constrained_observable
        self._constrained_beta_observable = "beta " + self._constrained_observable

        # Select the type of solver for the SCF algorithm and where to start the iterations.
        self._solver = solver
        self._initial_guess = initial_guess

        # Wheter to perform a stability check for each calculation and corresponding parameters.
        self._stability_analysis = stability_analysis
        self._stability_scaling_factor = stability_scaling_factor
        self._stability_output = stability_output

        if self._stability_output and self._stability_analysis is False:
            print("Stability analysis is turned off so no output can be printed.")


    # A solver for the UHF problem.
    def _solveUHFProblem(self, hamiltonian, stability_hamiltonian):
        """
        A method used to solve the iterative UHF problem. A stability check is performed automatically. If an internal instability is encountered, it will be followed by rotating the coefficeints in the direction of the lowest Hessian eigenvector. This will be shown in the output.

        :param hamiltonian:      The USQHamiltonian used for the calculation.

        :returns:                The ground state energy.
        :returns:                The ground state parameters
        """

        # To solve the GHF problem we need an environment and a solver.
        if type(hamiltonian) is gqcpy.gqcpy.USQHamiltonian_d:
            environment = gqcpy.UHFSCFEnvironment_d(self._Na, self._Nb, hamiltonian, self._overlap, self._initial_guess)
            qc_structure = gqcpy.UHF_d.optimize(self._solver, environment)
        else:
            environment = gqcpy.UHFSCFEnvironment_cd(self._Na, self._Nb, hamiltonian, self._overlap, self._initial_guess)
            qc_structure = gqcpy.UHF_cd.optimize(self._solver, environment)

        if self._stability_analysis:
            if self._stability_output:
                print("**************************************************************")
                print("            Checking for an internal instability.             ")
                print("**************************************************************")
            # For unrestricted Hartree-Fock, a stability check can be performed.
            # Transform the hamiltonian to MO basis and calculate the stability matrices. Print the resulting stabilities of the wavefunction model.
            coefficients = qc_structure.groundStateParameters().expansion()
            MO_hamiltonian = stability_hamiltonian.transformed(coefficients)
            stability_matrices = qc_structure.groundStateParameters().calculateStabilityMatrices(MO_hamiltonian)

            internal_stability = stability_matrices.isInternallyStable(-1e-5)

            if internal_stability:
                if self._stability_output:
                    # Print the new stability consitions.
                    stability_matrices.printStabilityDescription()
                    print("**************************************************************")

            # Add counter to prevent infinite stability loops.
            i = 0
            while internal_stability is False and i <= 15:
                if self._stability_output:
                    print("There is an internal instability. Follow it using the Hessian.")
                    print("**************************************************************")

                # Rotate the coefficients in the direction of the lowest Hessian eigenvector.
                rotation = stability_matrices.instabilityRotationMatrix(self._Na, self._Nb, self._Ka-self._Na, self._Kb-self._Nb, self._stability_scaling_factor)
                coefficients.rotate(rotation)

                # Perform a new SCF calculation with the rotated coefficients as initial guess.
                if type(hamiltonian) is gqcpy.gqcpy.USQHamiltonian_d:
                    environment_rotated = gqcpy.UHFSCFEnvironment_d(self._Na, self._Nb, hamiltonian, self._overlap, coefficients)
                    qc_structure = gqcpy.UHF_d.optimize(self._solver, environment_rotated)
                else:
                    environment_rotated = gqcpy.UHFSCFEnvironment_d(self._Na, self._Nb, hamiltonian, self._overlap, coefficients)
                    qc_structure = gqcpy.UHF_d.optimize(self._solver, environment_rotated)

                coefficients = qc_structure.groundStateParameters().expansion()

                # Perform a new stability check. Print the resulting stabilities.
                hamiltonian_MO = stability_hamiltonian.transformed(coefficients)
                stability_matrices = qc_structure.groundStateParameters().calculateStabilityMatrices(hamiltonian_MO)

                # Update the internal stability parameter.
                internal_stability = stability_matrices.isInternallyStable(-1e-5)

                # Up the counter.
                i += 1

                if internal_stability:
                    if self._stability_output:
                        # Print the new stability consitions.
                        stability_matrices.printStabilityDescription()
                        print("**************************************************************")

                if i == 16:
                    if self._stability_output:
                        print("        No stable solution found after 15 cycles.             ")
                        print("**************************************************************")

        return qc_structure.groundStateEnergy(), qc_structure.groundStateParameters()


    # A function to calculate the energy and expectation value value of UHF at a certain multiplier. 
    def calculateEnergyAndExpectationValue(self, multiplier, return_parameters=False, verbose=0):
        """
        A method used to calculate the energy and the expectation value at a given multiplier `mu`.

        :param multiplier:      The multiplier used to modify the Hamiltonian.
        :param verbose:         An integer representing the amount of output that will be printed.
        :return_parameters:     A boolean flag that specifies whether the wavefunction parameters are also returned.

        :returns:               The energy at the given `mu` values.
        :returns:               The expectation value of the operator at the given `mu` value.
        :returns:               The wavefunction parameters (only if `return_parameters` is set to `True`).

        In order to calculate the energy and expectation value of your operator, associated with a certain Lagrange multiplier (let's say -1).

        .. code-block:: python

            energy, expval = Constrained_object.calculateEnergyAndExpectationValue(-1)
        
        """
        # Modify the Hamiltonian with the given multiplier.
        # Do this respectively for the alpha and beta parts.
        if type(self._operator) in [gqcpy.gqcpy.ScalarUSQOneElectronOperator_d, gqcpy.gqcpy.ScalarUSQOneElectronOperator_cd]:
            unrestricted_operator = type(self._operator)((self._operator.alpha * multiplier), (self._operator.beta * multiplier))

            modified_hamiltonian = self._sq_hamiltonian - unrestricted_operator
            stability_hamiltonian = self._sq_hamiltonian - unrestricted_operator
        # Or a two electron operator.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarUSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_cd]:
            zero_component = type(self._operator.alphaBeta())(np.zeros((self._K, self._K, self._K, self._K)))
            dense_component_aa = type(self._operator.alphaAlpha())((self._operator.alphaAlpha() + self._operator.alphaBeta()) * multiplier)
            dense_component_bb = type(self._operator.betaBeta())((self._operator.betaAlpha() + self._operator.betaBeta()) * multiplier)
            unrestricted_operator = type(self._operator)(dense_component_aa, zero_component, zero_component, dense_component_bb)
            unrestricted_operator_stability = type(self._operator.twoElectron())((self._operator.twoElectron().alphaAlpha() * multiplier), (self._operator.twoElectron().alphaBeta() * multiplier), (self._operator.twoElectron().betaAlpha() * multiplier), (self._operator.twoElectron().betaBeta() * multiplier))

            # A second stability Hamiltonian needs to be constructed in order for GQCP's stability analysis to work. 
            # The Hamiltonian used for the calculations puts everything of the constraint into the aa/bb parts, which is required for UHF. 
            # However, this will result in wrongfully constructed stability matrices. Hence the second `stability Hamiltonian`.
            modified_hamiltonian = self._sq_hamiltonian - unrestricted_operator
            stability_hamiltonian = self._sq_hamiltonian - unrestricted_operator_stability
        elif type(self._operator) in [gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_d, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_cd]:
            unrestricted_matrix_operator = type(self._operator.oneElectron())((self._operator.oneElectron().alpha * multiplier), (self._operator.oneElectron().beta * multiplier))

            zero_component = type(self._operator.twoElectron().alphaBeta())(np.zeros((self._K, self._K, self._K, self._K)))
            
            parameters_aa = self._operator.twoElectron().alphaAlpha().parameters()
            parameters_ab = self._operator.twoElectron().alphaBeta().parameters()
            parameters_ba = self._operator.twoElectron().betaAlpha().parameters()
            parameters_bb = self._operator.twoElectron().betaBeta().parameters()

            dense_component_aa = type(self._operator.twoElectron().alphaAlpha())(parameters_aa + parameters_ab) * multiplier
            dense_component_bb = type(self._operator.twoElectron().betaBeta())(parameters_ba + parameters_bb) * multiplier

            unrestricted_tensor_operator = type(self._operator.twoElectron())(dense_component_aa, zero_component, zero_component, dense_component_bb)
            unrestricted_tensor_operator_stability = type(self._operator.twoElectron())((self._operator.twoElectron().alphaAlpha() * multiplier), (self._operator.twoElectron().alphaBeta() * multiplier), (self._operator.twoElectron().betaAlpha() * multiplier), (self._operator.twoElectron().betaBeta() * multiplier))

            # A second stability Hamiltonian needs to be constructed in order for GQCP's stability analysis to work. 
            # The Hamiltonian used for the calculations puts everything of the constraint into the aa/bb parts, which is required for UHF. 
            # However, this will result in wrongfully constructed stability matrices. Hence the second `stability Hamiltonian`.
            modified_hamiltonian = self._sq_hamiltonian - unrestricted_matrix_operator - unrestricted_tensor_operator
            stability_hamiltonian = self._sq_hamiltonian - unrestricted_matrix_operator - unrestricted_tensor_operator_stability
        else:
            raise ValueError("Something went wrong with the operator type.")

        gs_energy, gs_parameters = self._solveUHFProblem(modified_hamiltonian, stability_hamiltonian)

        # Calculate the density matrices.
        D = gs_parameters.calculateScalarBasis1DM()
        d = gs_parameters.calculateScalarBasis2DM()

        if type(self._operator) in [gqcpy.gqcpy.ScalarUSQOneElectronOperator_d, gqcpy.gqcpy.ScalarUSQOneElectronOperator_cd]:
            expectation_value = self._operator.calculateExpectationValue(D)[0]
        # For a two electron operator.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarUSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_cd]:
            expectation_value = self._operator.calculateExpectationValue(d)[0]
        # For an operator product.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_d, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_cd]:
            expectation_value = self._operator.calculateExpectationValue(D, d)
        
        # Calculate the energy by correcting the ground state energy of the modified Hamiltonian.
        energy = gs_energy + (multiplier * expectation_value) + self._nuclear_repulsion

        # Print the progress of which mu values have been completed if verbose >= 2.
        if verbose >= 2:
            print("--------------------------------------------------------")
            print("Mu = " + str(np.around(multiplier, 2)) + " done.")

        if return_parameters:
            return energy, expectation_value, gs_parameters
        else:
            return energy, expectation_value
