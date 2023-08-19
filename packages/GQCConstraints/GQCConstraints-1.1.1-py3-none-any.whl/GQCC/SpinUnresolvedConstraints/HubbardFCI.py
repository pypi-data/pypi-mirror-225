"""
Spin Unresolved Constraints - Hubbard FCI
-----------------------------------------

This module is used for constraining spin-unresolved operators in full configuration interaction calculations on the Hubbard model. By setting up the constrained Hubbard FCI object, the module prepares the basic functionalities to run constrained calculations for single values or to be used in one of the pre-set methods offered by GQCC.

"""

# Import statements
import gqcpy
import numpy as np

from GQCC.SpinUnresolvedConstraints import FCI

class HubbardFCI(FCI):
    """
    A constructor that sets up everything needed for constrained Hubbard model calculations.

    :param hubbard_hamiltonian:              The GQCP Hubbard Hamiltonian defining the Hubbard model.
    :param operator:                         The GQCP operator that will be constrained.        
    :param constrained_observable:           The name of the observable being constrained.

    :returns:                       An object which contains all required data (basis, Hamiltonian,... ) and possesses the necessary methods to perform calculations.

    To initialize a Hubbard FCI object we need a Hubbard Hamiltonian and an operator from GQCP. The Hubbard Hamiltonian can be constructed.

    .. code-block:: python

        L = 3       # number of sites
        t = 1e-4    # hopping parameter
        U = 1.0     # on-site repulsion
        
        adjacency_matrix = gqcpy.AdjacencyMatrix.Linear(L)
        hopping_matrix = gqcpy.HoppingMatrix.Homogeneous(adjacency_matrix, t)
        unmodified_hubbard_chain = gqcpy.HubbardHamiltonian(hopping_matrix, U)

    .. note::

        The Hubbard Hamiltonian does not need to be Homogeneous. Any GQCP Hubbard Hamiltonian will work.
    
    and an operator (e.g. number operator) can be made with the following code.

    .. code-block:: python

        P = np.zeros((L, L))
        P[0, 0] = 1
        number_operator = gqcpy.ScalarRSQOneElectronOperator_d(P)

    .. note::

        Contrary to the regular spin-unresolved FCI module, the Hubbard FCI module only works with **restricted** operators.

    A constrained Hubbard FCI object can then be constructed.

    .. code-block:: python

        Constrained_object = GQCC.SpinUnresolvedConstraints.HubbardFCI(unmodified_hubbard_chain, number_operator, "population")
    """
    def __init__(self, hubbard_hamiltonian, operator, constrained_observable):
        # Check compatibility of the operator type based on the used basis_type.
        compatible_operators = [gqcpy.gqcpy.ScalarRSQOneElectronOperator_d, gqcpy.gqcpy.ScalarRSQTwoElectronOperator_d]        
        assert (type(operator) in compatible_operators), "Only `ScalarRSQOneElectronOperator_d` or `ScalarRSQTwoElectronOperator_d` can be constrained with this method."
        
        # Hopping matrix of the defined Hubbard model.
        self._hubbard_hamiltonian = hubbard_hamiltonian
        self._sq_hamiltonian = gqcpy.RSQHamiltonian_d.FromHubbard(self._hubbard_hamiltonian)

        # Assume that each site can hold two electrons, one alpha and one beta.
        # From this, the N_alpha and N_beta are determined.
        L = self._hubbard_hamiltonian.hoppingMatrix().numberOfLatticeSites()
        N_beta = L // 2
        N_alpha = N_beta if L % 2 == 0 else N_beta + 1

        # With this information, a correct ONV basis can be constructed.
        self._onv_basis = gqcpy.SpinResolvedONVBasis(L, N_alpha, N_beta)

        # In order to be able to inherit from the CI methods, we need a nuclear repulsion.
        # Hubbard does not have this, so we just define it as zero.
        self._nuclear_repulsion = 0.0

        # Save the operator.
        self._operator = operator
        self._constrained_observable = constrained_observable


    def vonNeumannEntropy(self, domain_partition, wavefunction_parameters):
        """
        A method to calculate the von Neumann entropy of a certain partition within the Hubbard model.

        :param domain_partition:              The partition of the universe into "system" and "environment" for which the entropic relations will be calculated.
        :param wavefunction_parameters:       The parameters of the final wavefunction for which the entropic measures will be calculated.

        :returns:                             The Von Neumann entropy calculated according to eq. 6 in the following paper by Rissler et. al.: https://doi.org/10.1016/j.chemphys.2005.10.018.

        The Hubbard module can also look at the entanglement between different **domain partitions**. To do so we need to define certain domain partitions.

        .. code-block:: python

            domain_partition_p = gqcpy.DiscreteDomainPartition([0, 1, 1])
            domain_partition_q = gqcpy.DiscreteDomainPartition([1, 0, 1])

        .. note::

            To calculate entanglement you need the wavefunction parameters. To get them, set **return_parameters** to **True** in the `calculateEnergyAndExpectationValue()` or the `verifyCombination()` method.

        Using these partitions along with the wavefunction parameters, we can calculate the von Neumann entropy.

        .. code-block:: python

            Sp = Constrained_object.vonNeumannEntropy(domain_partition_p, parameters)
            Sq = Constrained_object.vonNeumannEntropy(domain_partition_q, parameters)
        """
        # Sometimes, the result will not fullfil the constraint. If this is the case, no parameters are saved.
        # This clause circumvents the error that would arise if the type of the saved wavefunction parameters is wrong.
        if type(wavefunction_parameters) is not gqcpy.gqcpy.LinearExpansion_SpinResolved:
            return None

        # Calculate the orbital RDM.
        rdm = wavefunction_parameters.calculateSystemOrbitalRDM(domain_partition)

        # Diagonalize the orbital RDM to obtain its eigenvalues.
        omegas,_ = np.linalg.eigh(rdm)

        # Calculate the von Neumann entropy according to eq. (6) in Rissler2005.
        ln_omegas = np.log(omegas)
        valid_values = np.where(~np.isnan(ln_omegas))
        entropy = -np.sum((omegas * ln_omegas)[valid_values])

        return entropy
    

    def mutualInformation(self, domain_partition_p, domain_partition_q, domain_partition_pq, wavefunction_parameters):
        """
        A method to calculate the mutual information, i.e. half the difference between two single site entropies and their two site entropy..

        :param domain_partition_p:               The partition of the universe into "system" and "environment" for which the first domain.
        :param domain_partition_q:               The partition of the universe into "system" and "environment" for which the second domain.
        :param domain_partition_pq:              The partition of the universe into "system" and "environment" for which the domain containing domain one and two.
        :param wavefunction_parameters:          The parameters of the final wavefunction for which the entropic measures will be calculated.

        :returns:                                The mutual information of site one and two calculated according to eq. 8 in the following paper by Rissler et. al.: https://doi.org/10.1016/j.chemphys.2005.10.018.

        The mutual information is an entanglement measure that elucidates how much two domains know about one another. To use this we need domain partitions for the two single site von Neumann entropies and one of the two site entropy.

        .. code-block:: python

            domain_partition_pq = gqcpy.DiscreteDomainPartition([0, 0, 1])
            domain_partition_p = gqcpy.DiscreteDomainPartition([0, 1, 1])
            domain_partition_q = gqcpy.DiscreteDomainPartition([1, 0, 1])

        Now we can call the mutual information.

        .. note::

            To calculate mutual information you need the wavefunction parameters. To get them, set **return_parameters** to **True** in the `calculateEnergyAndExpectationValue()` or the `verifyCombination()` method.

        .. code-block:: python

            I_pq = Constrained_object.mutualInformation(domain_partition_p, domain_partition_q, domain_partition_pq, parameters)

        """
        # Sometimes, the result will not fullfil the constraint. If this is the case, no parameters are saved.
        # This clause circumvents the error that would arise if the type of the saved wavefunction parameters is wrong.
        if type(wavefunction_parameters) is not gqcpy.gqcpy.LinearExpansion_SpinResolved:
            return None
        
        S_p = self.vonNeumannEntropy(domain_partition_p, wavefunction_parameters)
        S_q = self.vonNeumannEntropy(domain_partition_q, wavefunction_parameters)
        S_pq = self.vonNeumannEntropy(domain_partition_pq, wavefunction_parameters)

        # Calculate the mutual information between the two orbitals according to eq. (8) in Rissler2005.
        mutual_information = 0.5 * (S_p + S_q - S_pq) * (domain_partition_p != domain_partition_q)

        return mutual_information
