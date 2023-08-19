"""
Spin Unresolved Constraints - GHF
---------------------------------

This module is used for constraining spin-unresolved operators in generalized Hartree-Fock calculations. By setting up the constrained GHF object, the module prepares the basic functionalities to run constrained calculations for single values or to be used in one of the pre-set methods offered by GQCC.

"""

# Import statements
import gqcpy
import numpy as np
import numpy.random as rand
import scipy

from GQCC.Optimization.SpinUnresolvedOptimizer import SpinUnresolvedOptimizer


class GHF(SpinUnresolvedOptimizer):
    """
    A constructor that sets up everything needed for constrained GHF calculations.

    :param molecule:                    The GQCP molecule used for the calculations.
    :param SQ_basis:                    The second quantized GQCP basis set used for the calculations, defined for a molecule in a certain basis set. Make sure it is the same basis as in which the operator is defined.
    :param solver:                      The solver used for the UHF calculations.
    :param initial_guess:               The initial guess for the UHF calculation.
    :param operator:                    The GQCP operator that will be constrained.     
    :param constrained_observable:      The name of the observable being constrained.
    :param stability_analysis:          Boolean flag denoting whether stability analysis is performed. Default is `True`.
    :param stability_scaling_factor:    The scaling factor for constructing the stability rotation matrix when internal instabilities are found.
    :param stability_output:            Boolean flag on whether to print the outpuut of the stability analysis or not. Default is `False`.


    :returns:                An object which contains all required data (basis, Hamiltonian,... ) and possesses the necessary methods to perform calculations.

    In order to set up a GHF calculation with spin unresolved constraints we need several GQCP elements. First, set up some basic variables.

    .. code-block:: python

        H3 =  gqcpy.Molecule.HRingFromDistance(3, 1.88972, 0)                                       # The molecule.
        basis = gqcpy.GSpinorBasis_d(H3, "STO-3G")                                                  # The spinor basis.
        solver = gqcpy.GHFSCFSolver_d.Plain(threshold=1e-8, maximum_number_of_iterations=250000)    # The solver for the Hartree-Fock algorithm.

    We also need to give the object an initial guess for the SCF procedure. In this case, let's generate a random symmetric guess.

    .. code-block:: python

        import numpy.random as rand

        rand.seed(2)
        random_matrix = np.random.rand(basis.numberOfSpinors(), basis.numberOfSpinors())
        random_matrix_transpose = random_matrix.T
        symmetric_random_matrix = random_matrix + random_matrix_transpose
        _, guess = np.linalg.eigh(symmetric_random_matrix)
        init_guess = gqcpy.GTransformation_d(guess)

    Now we choose an operator to constrain. Let's take the :math:`S_z` operator.

    .. code-block:: python

        Sz = basis.quantize(gqcpy.ElectronicSpin_zOperator())

    Finally we can construct the constrained object using GQCC.

    .. code-block:: python

        Constrained_object = GQCC.SpinUnresolvedConstraints.GHF(H3, basis, solver, init_guess, Sz, "Sz value")

    """
    def __init__ (self, molecule, SQ_basis, solver, initial_guess, operator, constrained_observable, stability_analysis=True, stability_scaling_factor=1.0, stability_output=False):
        # Check compatibility of the operator type based on the used basis type.
        if type(SQ_basis) is gqcpy.gqcpy.GSpinorBasis_d:
            compatible_operators = [gqcpy.gqcpy.ScalarGSQOneElectronOperator_d, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_d]
            assert (type(solver) is gqcpy.gqcpy.IterativeAlgorithm_GHFSCFEnvironment_d)

        elif type(SQ_basis) is gqcpy.gqcpy.GSpinorBasis_cd:
            compatible_operators = [gqcpy.gqcpy.ScalarGSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_cd, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_cd]
            assert (type(solver) is gqcpy.gqcpy.IterativeAlgorithm_GHFSCFEnvironment_cd)

        else:
            raise ValueError("the chosen `SQ_basis` or `solver` is not compatible with this type of calculation. Use `gqcpy.GSpinorBasis_(c)d`instead.")
        assert (type(operator) in compatible_operators), "Only `ScalarGSQOneElectronOperator_(c)d` or `ScalarGSQTwoElectronOperator_(c)d` can be constrained with this method."     

        # This basis can now quantize the Hamiltonian.
        self._sq_hamiltonian = SQ_basis.quantize(gqcpy.FQMolecularHamiltonian(molecule))

        # We will need the number of electrons, as well as the total number of Spinors later on.        
        self._K = SQ_basis.numberOfSpinors()
        self._N = molecule.numberOfElectrons()

        # Save the overlap and nuclear repulsion operators. 
        self._nuclear_repulsion = gqcpy.NuclearRepulsionOperator(molecule.nuclearFramework()).value()
        self._overlap = SQ_basis.quantize(gqcpy.OverlapOperator())

        # Save the operator you want to constrain.
        self._operator = operator
        self._constrained_observable = constrained_observable

        # Select the type of solver for the SCF algorithm.
        self._solver = solver
        self._initial_guess = initial_guess

        # Whether to perform a stability check for each calculation and corresponding parameters.
        self._stability_analysis = stability_analysis
        self._stability_scaling_factor = stability_scaling_factor
        self._stability_output = stability_output

        if self._stability_output and self._stability_analysis is False:
            print("Stability analysis is turned off so no output can be printed.")



    # A solver for the GHF problem.
    # The GHF solver always takes a random guess, in order to activate the `off-diagonal` blocks. 
    def _solveGHFProblem(self, hamiltonian):
        """
        A method used to solve the iterative GHF problem. A stability check is performed automatically. If an internal instability is encountered, it will be followed by rotating the coefficients in the direction of the lowest Hessian eigenvector. This will be shown in the output.

        :param hamiltonian:      The GSQHamiltonian used for the calculation.

        :returns:                The ground state energy.
        :returns:                The ground state parameters
        """

        # To solve the GHF problem we need an environment and a solver.
        if type(hamiltonian) is gqcpy.gqcpy.GSQHamiltonian_d:
            environment = gqcpy.GHFSCFEnvironment_d(self._N, hamiltonian, self._overlap, self._initial_guess)
            qc_structure = gqcpy.GHF_d.optimize(self._solver, environment)
        else:
            environment = gqcpy.GHFSCFEnvironment_cd(self._N, hamiltonian, self._overlap, self._initial_guess)
            qc_structure = gqcpy.GHF_cd.optimize(self._solver, environment)

        if self._stability_analysis:
            if self._stability_output:
                print("**************************************************************")
                print("            Checking for an internal instability.             ")
                print("**************************************************************")
            # For generalized Hartree-Fock, a stability check is always performed.
            # Transform the hamiltonian to MO basis and calculate the stability matrices. Print the resulting stabilities of the wavefunction model.
            coefficients = qc_structure.groundStateParameters().expansion()
            MO_hamiltonian = hamiltonian.transformed(coefficients)
            stability_matrices = qc_structure.groundStateParameters().calculateStabilityMatrices(MO_hamiltonian)

            internal_stability = stability_matrices.isInternallyStable(-1e-5)
            H = stability_matrices.internal()
            v, _ = scipy.linalg.eigh(H)
            print(v)

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
                rotation = stability_matrices.instabilityRotationMatrix(self._N, self._K-self._N, self._stability_scaling_factor)
                coefficients.rotate(rotation)

                # Perform a new SCF calculation with the rotated coefficients as initial guess.
                if type(hamiltonian) is gqcpy.gqcpy.GSQHamiltonian_d:
                    environment_rotated = gqcpy.GHFSCFEnvironment_d(self._N, hamiltonian, self._overlap, coefficients)
                    qc_structure = gqcpy.GHF_d.optimize(self._solver, environment_rotated)
                else:
                    environment_rotated = gqcpy.GHFSCFEnvironment_cd(self._N, hamiltonian, self._overlap, coefficients)
                    qc_structure = gqcpy.GHF_cd.optimize(self._solver, environment_rotated)

                coefficients = qc_structure.groundStateParameters().expansion()

                # Perform a new stability check. Print the resulting stabilities.
                hamiltonian_MO = hamiltonian.transformed(coefficients)
                stability_matrices = qc_structure.groundStateParameters().calculateStabilityMatrices(hamiltonian_MO)

                # Update the internal stability parameter.
                internal_stability = stability_matrices.isInternallyStable(-1e-5)
                H = stability_matrices.internal()
                v, _ = scipy.linalg.eigh(H)
                print(v)

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


    # A function to calculate the energy and expectation value value of GHF at a certain multiplier. 
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
        # For a one- or two- electron operator this happens in the same way.
        # Note that the one-electron operator modifies the one-electron intergrals, and the two-electron operator modifies the two-electron integrals.
        if type(self._operator) in [gqcpy.gqcpy.ScalarGSQOneElectronOperator_d, gqcpy.gqcpy.ScalarGSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_cd]:
            modified_hamiltonian = self._sq_hamiltonian - multiplier * self._operator
        # For an operator product.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_d, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_cd]:
            modified_hamiltonian = self._sq_hamiltonian - (multiplier * self._operator.oneElectron()) - (multiplier * self._operator.twoElectron())
        else:
            raise ValueError("Something went wrong with the operator type.") 
        
        gs_energy, gs_parameters = self._solveGHFProblem(modified_hamiltonian)

        # Calculate the density matrices.
        D = gs_parameters.calculateScalarBasis1DM()
        d = gs_parameters.calculateScalarBasis2DM()

        # Calculate the expectation value of the constrained operator.
        # This differs depending on which kind of operator is being used.
        # For a one electron operator.
        if type(self._operator) in [gqcpy.gqcpy.ScalarGSQOneElectronOperator_d, gqcpy.gqcpy.ScalarGSQOneElectronOperator_cd]:
            expectation_value = self._operator.calculateExpectationValue(D)[0]
        # For a two electron operator.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarGSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_cd]:
            expectation_value = self._operator.calculateExpectationValue(d)[0]
        # For an operator product.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_d, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_cd]:
            expectation_value = self._operator.calculateExpectationValue(D, d)

        # Perform the energy correction
        energy = gs_energy + ((multiplier * expectation_value) + self._nuclear_repulsion)

        # Print the progress of which mu values have been completed if verbose >= 2.
        if verbose >= 2:
            print("--------------------------------------------------------")
            print("Mu = " + str(np.around(multiplier, 2)) + " done.")

        if return_parameters:
            return energy, expectation_value, gs_parameters
        else:
            return energy, expectation_value
