"""
Spin Unresolved Constraints - FCI
---------------------------------

This module is used for constraining spin-unresolved operators in full configuration interaction calculations. By setting up the constrained FCI object, the module prepares the basic functionalities to run constrained calculations for single values or to be used in one of the pre-set methods offered by GQCC.

"""

# Import statements
import gqcpy
import numpy as np

from GQCC.Optimization.SpinUnresolvedOptimizer import SpinUnresolvedOptimizer


class FCI(SpinUnresolvedOptimizer):
    """
    A constructor that sets up everything needed for spin unresolved constrained CI calculations.

    :param molecule:         The molecule used for the calculations.
    :param basis_set:        The basis set used for the calculations.
    :param operator:         The operator that will be constrained.
    :param basis:            The type of basis in which the FCI calculation will be performed. Default is restricted.

    :returns:                An object which contains all required data (basis, Hamiltonian,... ) and possesses the necessary methods to perform calculations.
    
    To initialize a constrained FCI object, we need several objects from GQCP.

    First, we need a molecule.

    .. code-block:: python

        H2 =  gqcpy.Molecule.HChain(2, 4.5, 0)

    Secondly, we need to create our spin-orbital basis. Since this is FCI, it should be orthonormal.

    .. code-block:: python

        basis = gqcpy.RSpinOrbitalBasis_d(H2, "6-31G")
        basis.lowdinOrthonormalize()

    Finally we can create a spin-unresolved operator to constrain. Let's use a Mulliken operator in this example.

    .. code-block:: python

        S = basis.quantize(gqcpy.OverlapOperator())
        mulliken_domain = basis.mullikenDomain(lambda shell: shell.nucleus().position()[1] == 0 and shell.nucleus().position()[2] == 0)
        P = mulliken_domain.projectionMatrix(basis.expansion())
        mulliken_operator = S.partitioned(P)

    Now we can use GQCC to construct our constrained ansatz.

    .. code-block:: python

        Constrained_object = GQCC.SpinUnresolvedConstraints.FCI(H2, basis, mulliken_operator, "population")

    .. note:

        The spin-unresolved FCI module also works with generalized `gqcpy.GSpinorBasis_(c)d` bases.
    """
    def __init__(self, molecule, SQ_basis, operator, constrained_observable):
       # Check compatibility of the operator type based on the used basis_type.
        if type(SQ_basis) is gqcpy.gqcpy.RSpinOrbitalBasis_d:
            compatible_operators = [gqcpy.gqcpy.ScalarRSQOneElectronOperator_d, gqcpy.gqcpy.ScalarRSQTwoElectronOperator_d]
        elif type(SQ_basis) is gqcpy.gqcpy.RSpinOrbitalBasis_cd:
            compatible_operators = [gqcpy.gqcpy.ScalarRSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarRSQTwoElectronOperator_cd]
        elif type(SQ_basis) is gqcpy.gqcpy.GSpinorBasis_d:
            compatible_operators = [gqcpy.gqcpy.ScalarGSQOneElectronOperator_d, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_d]
        elif type(SQ_basis) is gqcpy.gqcpy.GSpinorBasis_cd:
            compatible_operators = [gqcpy.gqcpy.ScalarGSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_cd, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_cd]
        else:
            raise ValueError("the chosen `SQ_basis` is not compatible with this type of calculation. Use `gqcpy.R/GSpinOrbitalBasis_(c)d`instead.")
        
        assert (type(operator) in compatible_operators), "Only `ScalarR/GSQOneElectronOperator_(c)d` or `ScalarR/GSQTwoElectronOperator_(c)d` can be constrained with this method."

        # We can now create a first quantized hamiltonian and use the spin orbital basis to "quantize" it to second quantization.
        # The SQHamiltonian is stored in the class object.
        fq_hamiltonian = gqcpy.FQMolecularHamiltonian(molecule)
        self._sq_hamiltonian = SQ_basis.quantize(fq_hamiltonian)

        # Since we are going to do full CI calculations, we need an ONV-basis.
        # From the total number of orbitals and total number of electrons we can set up an ONV basis.
        if type(SQ_basis) is gqcpy.gqcpy.RSpinOrbitalBasis_d or type(SQ_basis) is gqcpy.gqcpy.RSpinOrbitalBasis_cd:
            K = int(SQ_basis.numberOfSpatialOrbitals())
        else:
            K = int(SQ_basis.numberOfSpinors())
        
        N_total = molecule.numberOfElectrons()

        if N_total % 2 == 0:
            N_a = int(N_total / 2)
            N_b = int(N_total / 2)
        else:
            N_a = int(np.ceil(N_total / 2))
            N_b = int(np.floor(N_total / 2))

        # The ONV basis gets stored within the class object.
        if type(SQ_basis) is gqcpy.gqcpy.RSpinOrbitalBasis_d or type(SQ_basis) is gqcpy.gqcpy.RSpinOrbitalBasis_cd:
            self._onv_basis = gqcpy.SpinResolvedONVBasis(K, N_a, N_b)
        else:
            full_onv_basis = gqcpy.SpinUnresolvedONVBasis(K, N_total)
            self._onv_basis = gqcpy.SpinUnresolvedSelectedONVBasis(full_onv_basis)

        # Calculate the nuclear repulsion term and store it in the class object.
        self._nuclear_repulsion = gqcpy.NuclearRepulsionOperator(molecule.nuclearFramework()).value()

        # Stor the operator that is being constrained.
        self._operator = operator
        self._constrained_observable = constrained_observable
    

    def _solveCIEigenproblem(self, hamiltonian):
        """
        A method used to solve a CI eigenproblem.

        :param hamiltonian:      The SQHamiltonian used for the calculation.

        :returns:                The ground state energy.
        :returns:                The ground state parameters
        """
        # Use GQCP to set up a full CI calculation.
        if type(hamiltonian) is gqcpy.gqcpy.RSQHamiltonian_d or type(hamiltonian) is gqcpy.gqcpy.GSQHamiltonian_d:
            CIsolver = gqcpy.EigenproblemSolver.Dense_d()
            CIenvironment = gqcpy.CIEnvironment.Dense(hamiltonian, self._onv_basis)
            qc_structure = gqcpy.CI(self._onv_basis).optimize(CIsolver, CIenvironment)
        else:
            CIsolver = gqcpy.EigenproblemSolver.Dense_cd()
            CIenvironment = gqcpy.CIEnvironment.Dense_cd(hamiltonian, self._onv_basis)
            qc_structure = gqcpy.CI_cd(self._onv_basis).optimize(CIsolver, CIenvironment)

        return qc_structure.groundStateEnergy(), qc_structure.groundStateParameters()
        

    def calculateEnergyAndExpectationValue(self, multiplier, return_parameters=False, verbose=0):
        """
        A method used to calculate the energy and the expectation value of the operator at a given multiplier `mu`.

        :param multiplier:              The multiplier used to modify the Hamiltonian.
        :param return_parameters:       A boolean flag to indicate whether only the wavefunction parameters should also be returned.
        :param verbose:                 An integer representing the amount of output that will be printed.

        :returns:                       The energy at the given `mu` value.
        :returns:                       The expectation value of the operator at the given `mu` value.
        :returns:                       The wavefunction parameters (only if `return_parameters` is set to `True`).

        In order to calculate the energy and expectation value of your operator, associated with a certain Lagrange multiplier (let's say -1).

        .. code-block:: python

            energy, expval = Constrained_object.calculateEnergyAndExpectationValue(-1)
        
        """
        # Modify the Hamiltonian with the given multiplier.
        # For a one- or two- electron operator this happens in the same way.
        # Note that the one-electron operator modifies the one-electron intergrals, and the two-electron operator modifies the two-electron integrals.
        if type(self._operator) in [gqcpy.gqcpy.ScalarRSQOneElectronOperator_d, gqcpy.gqcpy.ScalarRSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarGSQOneElectronOperator_d, gqcpy.gqcpy.ScalarGSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarRSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarRSQTwoElectronOperator_cd, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_cd]:
            modified_hamiltonian = self._sq_hamiltonian - multiplier * self._operator
        # For an operator product.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_d, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_cd]:
            modified_hamiltonian = self._sq_hamiltonian - (multiplier * self._operator.oneElectron()) - (multiplier * self._operator.twoElectron())
        else:
            raise ValueError("Something went wrong with the operator type.")
        
        # Use the private method to solve the full CI eigenproblem.
        gs_energy, gs_parameters = self._solveCIEigenproblem(modified_hamiltonian)

        # Calculate the density matrices.
        D = gs_parameters.calculate1DM()
        d = gs_parameters.calculate2DM()

        # Calculate the expectation value of the constrained operator.
        # This differs depending on which kind of operator is being used.
        # For a one electron operator.
        if type(self._operator) in [gqcpy.gqcpy.ScalarRSQOneElectronOperator_d, gqcpy.gqcpy.ScalarRSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarGSQOneElectronOperator_d, gqcpy.gqcpy.ScalarGSQOneElectronOperator_cd]:
            expectation_value = self._operator.calculateExpectationValue(D)[0]
        # For a two electron operator.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarRSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarRSQTwoElectronOperator_cd, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarGSQTwoElectronOperator_cd]:
            expectation_value = self._operator.calculateExpectationValue(d)[0]
        # For an operator product.
        elif type(self._operator) in [gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_d, gqcpy.gqcpy.ScalarGSQOneElectronOperatorProduct_cd]:
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
