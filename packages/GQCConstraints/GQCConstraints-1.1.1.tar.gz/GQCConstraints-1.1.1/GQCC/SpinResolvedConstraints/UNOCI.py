"""
Spin Resolved Constraints - UNOCI
---------------------------------

This module is used for constraining spin-resolved operators in non-orthogonal configuration interaction calculations, carried out in a basis of unrestricted states. By setting up the constrained UNOCI object, the module prepares the basic functionalities to run constrained calculations for single values or to be used in one of the pre-set methods offered by GQCC.

"""

# Import statements
import gqcpy
import numpy as np

from GQCC.Optimization.SpinResolvedOptimizer import SpinResolvedOptimizer


class UNOCI(SpinResolvedOptimizer):
    """
    A constructor that sets up everything needed for constrained NOCI calculations in an unrestricted basis.

    :param molecule:                    The GQCP molecule used for the calculations.
    :param electrons:                   The amount of alpha and beta electrons in the molecule as an array.
    :param SQ_basis:                    The second quantized GQCP basis set used for the calculations, defined for a molecule in a certain basis set. Make sure it is the same basis as in which the operator is defined.
    :param basis_state_vector:          A vector of non-orthogonal states that will serve as a basis for NOCI.
    :param operator:                    The GQCP operator that will be constrained.    
    :param constrained_observable:      The name of the observable being constrained.

    :returns:                           An object which contains all required data (basis, Hamiltonian,... ) and possesses the necessary methods to perform calculations.

    First we need to set up some basic variables with GQCP.

    .. code-block:: python

        H3 =  gqcpy.Molecule.HRingFromDistance(3, 1.88972, 0)   # The molecule.
        electrons = [2,1]                                       # The number of alpha and beta electrons.
        spinor_basis = gqcpy.USpinOrbitalBasis_d(H3, "STO-3G")  # The spin orbital basis.

    We also set up an operator (Mulliken in this case).

    .. code-block:: python

        S = spinor_basis.quantize(gqcpy.OverlapOperator())
        mulliken_domain = spinor_basis.mullikenDomain(lambda shell: shell.nucleus().position()[1] == 0 and shell.nucleus().position()[2] == 0)
        P = mulliken_domain.projectionMatrix(spinor_basis.expansion())
        mulliken_operator = S.partitioned(P)

    For UNOCI we need a vector of basis states consisting of unrestricted states, `basis_vector`. One way to generate such states is by running several constrained UHF calculations. 

    .. note:: 
    
        For info on generating states with constrained UHF see the `Constrained Hartree-Fock <https://gqcg-res.github.io/GQCConstraints/ConstrainedHartreeFock.html>`_ section or look at our `examples on github <https://github.com/GQCG-res/GQCConstraints/tree/develop/examples>`_.

    Once we have a everything, the constrained NOCI object can be created with GQCC.

    .. code-block:: python

        Constrained_object = GQCC.SpinResolvedConstraints.UNOCI(H3, electrons, spinor_basis, basis_vector, mulliken_operator, "population")
    """
    def __init__(self, molecule, electrons, SQ_basis, basis_state_vector, operator, constrained_observable):
        # Raise an exception if the electrons array is not conform with the requirements.
        if type(electrons[0]) is float or type(electrons[1]) is float or len(electrons) != 2:
            raise ValueError("Electrons must be of dimension 2 and must contain two ìnt`s as it must contain the number of alpha and beta electrons.")
        
        # Check compatibility of the operator type based on the used basis type.
        if type(SQ_basis) is gqcpy.gqcpy.USpinOrbitalBasis_d:
            compatible_operators = [gqcpy.gqcpy.ScalarUSQOneElectronOperator_d, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_d, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_d]
        elif type(SQ_basis) is gqcpy.gqcpy.USpinOrbitalBasis_cd:
            compatible_operators = [gqcpy.gqcpy.ScalarUSQOneElectronOperator_cd, gqcpy.gqcpy.ScalarUSQTwoElectronOperator_cd, gqcpy.gqcpy.ScalarUSQOneElectronOperatorProduct_cd]
        else:
            raise ValueError("the chosen `SQ_basis` or `solver` is not compatible with this type of calculation. Use `gqcpy.USpinOrbitalBasis_(c)d`instead.")
        assert (type(operator) in compatible_operators), "Only `ScalarUSQOneElectronOperator_(c)d` or `ScalarUSQTwoElectronOperator_(c)d` can be constrained with this method."     

        # Here, a molecule does need to be saved as it is needed to construct the NOCI Hamiltonian.
        self._molecule = molecule

        # Save the number of electrons.
        self._Na = electrons[0]
        self._Nb = electrons[1]

        # Quantize the Hamiltonian in the spinor basis.
        self._sq_hamiltonian = SQ_basis.quantize(gqcpy.FQMolecularHamiltonian(molecule))

        # Save the overlap operator.
        self._overlap = SQ_basis.quantize(gqcpy.OverlapOperator())

        # Generate a Non-orthogonal state basis.
        self._NOCIBasis = gqcpy.UNonOrthogonalStateBasis_d(basis_state_vector, self._overlap, self._Na, self._Nb)

        # Save the operator you want to constrain.
        self._operator = operator

        self._constrained_observable = constrained_observable
        self._constrained_alpha_observable = "alpha " + self._constrained_observable
        self._constrained_beta_observable = "beta " + self._constrained_observable


    # A solver for the NOCI problem.
    def _solveNOCIEigenproblem(self, hamiltonian):
        """
        A method used to solve a NOCI eigenproblem.

        :param hamiltonian:      The SQHamiltonian used for the calculation.

        :returns:                The ground state energy.
        :returns:                The ground state parameters
        """
        if type(hamiltonian) is gqcpy.gqcpy.USQHamiltonian_d:
            environment = gqcpy.NOCIEnvironment.Dense_d(hamiltonian, self._NOCIBasis, self._molecule)
            solver = gqcpy.GeneralizedEigenproblemSolver.Dense_d()
            qc_structure = gqcpy.NOCI_d(self._NOCIBasis).optimize(solver, environment)
        else:
            environment = gqcpy.NOCIEnvironment.Dense_cd(hamiltonian, self._NOCIBasis, self._molecule)
            solver = gqcpy.GeneralizedEigenproblemSolver.Dense_cd()
            qc_structure = gqcpy.NOCI_cd(self._NOCIBasis).optimize(solver, environment)

        return qc_structure.groundStateEnergy(), qc_structure.groundStateParameters()

     
    # A function to calculate the energy and expectation value of NOCI at a certain multiplier. 
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
        gs_energy, gs_parameters = self._solveNOCIEigenproblem(modified_hamiltonian)

        # Use the ground state parameters to calculate the 1DM and use it to calculate the expectation value of the Mulliken operator.
        # The separate alpha and beta expectation values are calculated as well.
        D = gs_parameters.calculate1DM()

        total_expectation_value = self._operator.calculateExpectationValue(D)[0]
        alpha_expectation_value = self._operator.alpha.calculateExpectationValue(D.alpha)[0]
        beta_expectation_value = self._operator.beta.calculateExpectationValue(D.beta)[0]

        # Calculate the energy by correcting the ground state energy of the modified Hamiltonian.
        energy = gs_energy + (multiplier_array[0] * alpha_expectation_value) + (multiplier_array[1] * beta_expectation_value)

        # Print the progress of which mu values have been completed if verbose >= 2.
        if verbose >= 2:
            print("--------------------------------------------------------")
            print("Mu combo: alpha = " + str(np.around(multiplier_array[0], 2)) + " , beta = " + str(np.around(multiplier_array[1], 2)) + " done.")
        if return_parameters:
            return energy, [alpha_expectation_value, beta_expectation_value], total_expectation_value, gs_parameters
        else:
            return energy, [alpha_expectation_value, beta_expectation_value], total_expectation_value
