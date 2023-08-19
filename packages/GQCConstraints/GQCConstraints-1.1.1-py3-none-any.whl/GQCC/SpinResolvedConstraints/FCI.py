"""
Spin Resolved Constraints - FCI
-------------------------------

This module is used for constraining spin-resolved operators in full configuration interaction calculations. By setting up the constrained FCI object, the module prepares the basic functionalities to run constrained calculations for single values or to be used in one of the pre-set methods offered by GQCC.

"""

# Import statements
import gqcpy
import numpy as np

from GQCC.Optimization.SpinResolvedOptimizer import SpinResolvedOptimizer

class FCI(SpinResolvedOptimizer):
    """
    A constructor that sets up everything needed for spin resolved constrained CI calculations.

    :param molecule:                    The GQCP molecule used for the calculations.
    :param SQ_basis:                    The second quantized GQCP basis set used for the calculations, defined for a molecule in a certain basis set. Make sure it is the same basis as in which the operator is defined.
    :param operator:                    The GQCP operator that will be constrained.        
    :param constrained_observable:      The name of the observable being constrained.

    :returns:                 An object which contains all required data (basis, Hamiltonian,... ) and possesses the necessary methods to perform calculations.

    To initialize a constrained FCI object, we need several objects from GQCP.

    First, we need a molecule.

    .. code-block:: python

        H2 =  gqcpy.Molecule.HChain(2, 4.5, 0)

    Secondly, we need to create our spin-orbital basis. Since this is FCI, it should be orthonormal.

    .. code-block:: python

        basis = gqcpy.USpinOrbitalBasis_d(H2, "6-31G")
        basis.lowdinOrthonormalize()

    Finally we can create a spin-resolved operator to constrain. Let's use a Mulliken operator in this example.

    .. code-block:: python

        S = basis.quantize(gqcpy.OverlapOperator())
        mulliken_domain = basis.mullikenDomain(lambda shell: shell.nucleus().position()[1] == 0 and shell.nucleus().position()[2] == 0)
        P = mulliken_domain.projectionMatrix(basis.expansion())
        mulliken_operator = S.partitioned(P)

    Now we can use GQCC to construct our constrained ansatz.

    .. code-block:: python

        Constrained_object = GQCC.SpinResolvedConstraints.FCI(H2, basis, mulliken_operator, "population")
    """
    def __init__(self, molecule, SQ_basis, operator, constrained_observable): 
        # Check compatibility of the operator type based on the used basis_type.
        if type(SQ_basis) is gqcpy.gqcpy.USpinOrbitalBasis_d:
            compatible_operators = [gqcpy.gqcpy.ScalarUSQOneElectronOperator_d, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_d]
        elif type(SQ_basis) is gqcpy.gqcpy.USpinOrbitalBasis_cd:
            compatible_operators = [gqcpy.gqcpy.ScalarUSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_cd, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_d]
        else:
            raise ValueError("the chosen `SQ_basis` is not compatible with this type of calculation. Use `gqcpy.USpinOrbitalBasis_(c)d`instead.")
        
        assert (type(operator) in compatible_operators), "Only `ScalarUSQOneElectronOperator_(c)d` or `ScalarUSQTwoElectronOperator_(c)d` can be constrained with this method."     

        # We can now create a first quantized hamiltonian and use the spin orbital basis to "quantize" it to second quantization.
        # The SQHamiltonian is stored in the class object.
        fq_hamiltonian = gqcpy.FQMolecularHamiltonian(molecule)
        self._sq_hamiltonian = SQ_basis.quantize(fq_hamiltonian)

        # Since we are going to do full CI calculations, we need an ONV-basis.
        # From the total number of orbitals and total number of electrons we can set up an ONV basis.
        K = int(SQ_basis.numberOfSpinors() / 2)
        N_total = molecule.numberOfElectrons()

        if N_total % 2 == 0:
            N_a = int(N_total / 2)
            N_b = int(N_total / 2)
        else:
            N_a = int(np.ceil(N_total / 2))
            N_b = int(np.floor(N_total / 2))

        # The ONV basis gets stored within the class object.
        self._onv_basis = gqcpy.SpinResolvedONVBasis(K, N_a, N_b)

        # Calculate the nuclear repulsion term and store it in the class object.
        self._nuclear_repulsion = gqcpy.NuclearRepulsionOperator(molecule.nuclearFramework()).value()

        # Store the operator.
        self._operator = operator
        
        self._constrained_observable = constrained_observable
        self._constrained_alpha_observable = "alpha " + self._constrained_observable
        self._constrained_beta_observable = "beta " + self._constrained_observable
    

    def _solveCIEigenproblem(self, hamiltonian):
        """
        A method used to solve an unrestricted CI eigenproblem.

        :param hamiltonian:      The USQHamiltonian used for the calculation.

        :returns:                The ground state energy.
        :returns:                The ground state parameters
        """
        # Use GQCP to set up a full CI calculation.
        if type(hamiltonian) is gqcpy.gqcpy.USQHamiltonian_d:
            CIsolver = gqcpy.EigenproblemSolver.Dense_d()
            CIenvironment = gqcpy.CIEnvironment.Dense(hamiltonian, self._onv_basis)
            qc_structure = gqcpy.CI(self._onv_basis).optimize(CIsolver, CIenvironment)
        else:
            CIsolver = gqcpy.EigenproblemSolver.Dense_cd()
            CIenvironment = gqcpy.CIEnvironment.Dense_cd(hamiltonian, self._onv_basis)
            qc_structure = gqcpy.CI_cd(self._onv_basis).optimize(CIsolver, CIenvironment)

        return qc_structure.groundStateEnergy(), qc_structure.groundStateParameters()
        

    def calculateEnergyAndExpectationValue(self, multiplier_array, return_parameters=False, verbose=0):
        """
        A method used to calculate the energy and the expectation value at a given multiplier `mu`.

        :param multiplier_array:      The multiplier used to modify the Hamiltonian. Must be an array/list that contains an alpha and beta value.
        :param verbose:               An integer representing the amount of output that will be printed.
        :return_parameters:           A boolean flag that specifies whether the wavefunction parameters are also returned.

        :returns:                     The energy at the given `mu` values.
        :returns:                     The alpha/beta expectation values at the given `mu` values.
        :returns:                     The total spin unresolved expectation value at the given `mu`.
        :returns:                     The wavefunction parameters (only if `return_parameters` is set to `True`).

        In order to calculate the energy and expectation value of your operator, associated with a certain Lagrange multiplier for the alpha and beta part (let's say -1 and -1).

        .. code-block:: python

            energy, alpha_beta_expval, total_expval = Constrained_object.calculateEnergyAndExpectationValue([-1, -1])
        
        """
        # Raise an exception if the multiplier is not conform with the requirements.
        if type(multiplier_array) is float or len(multiplier_array) != 2:
             raise ValueError("Multiplier_array must be of dimension 2 as it must contain both an alpha and beta value.")

        # Modify the Hamiltonian with the given multiplier. Do this respectively for the alpha and beta parts.
        # This is done differently when the operator is a one electron operator.
        if type(self._operator) in [gqcpy.gqcpy.ScalarUSQOneElectronOperator_d, gqcpy.gqcpy.ScalarUSQOneElectronOperator_cd]:
            unrestricted_operator = type(self._operator)((self._operator.alpha * multiplier_array[0]), (self._operator.beta * multiplier_array[1]))
            modified_hamiltonian = self._sq_hamiltonian - unrestricted_operator
        # Or a two electron operator.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarUSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_cd]:
            raise NotImplementedError("This is not yet implemented. Some general issues need to be cleared out before this can be added.")
        # Or an operator product.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_d, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_cd]:
            raise NotImplementedError("This is not yet implemented. Some general issues need to be cleared out before this can be added.")
        else:
            raise ValueError("Something went wrong with the operator type.")

        # Use the private method to solve the full CI eigenproblem.
        gs_energy, gs_parameters = self._solveCIEigenproblem(modified_hamiltonian)

        # Use the ground state parameters to calculate the 1DM and use it to calculate the expectation value of the Mulliken operator.
        # The separate alpha and beta expectation values are calculated as well.
        D = gs_parameters.calculateSpinResolved1DM()

        total_expectation_value = self._operator.calculateExpectationValue(D)[0]
        alpha_expectation_value = self._operator.alpha.calculateExpectationValue(D.alpha)[0]
        beta_expectation_value = self._operator.beta.calculateExpectationValue(D.beta)[0]

        # Calculate the energy by correcting the ground state energy of the modified Hamiltonian.
        energy = gs_energy + (multiplier_array[0] * alpha_expectation_value) + (multiplier_array[1] * beta_expectation_value) + self._nuclear_repulsion

        # Print the progress of which mu values have been completed if verbose >= 2.
        if verbose >= 2:
            print("--------------------------------------------------------")
            print("Mu combo: alpha = " + str(np.around(multiplier_array[0], 2)) + " , beta = " + str(np.around(multiplier_array[1], 2)) + " done.")
        if return_parameters:
            return energy, [alpha_expectation_value, beta_expectation_value], total_expectation_value, gs_parameters
        else:
            return energy, [alpha_expectation_value, beta_expectation_value], total_expectation_value
