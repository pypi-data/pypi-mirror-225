from dataclasses import dataclass

from typing import Callable

import jax.numpy as jnp
import jax.scipy as jsp

from .distributions import FullPriorDistribution, SparsePriorDistribution


@dataclass(frozen=True)
class NegativeLogMarginalLikelihood:
    '''Collection of the different loss functions.

    Parameters
    ----------
    sparse : bool
        flag if the Prior should calculate a sparse or a full PriorDistribution

    Returns
    -------
    Callable
        returns a function that calculates the negative marginal log likelihood 
        of a model depending on the chosen Parameters
    '''
    sparse: bool = False

    def __call__(self) -> Callable:
        if self.sparse:
            return _fitc_NLML
        else:
            return _full_NLML
        


def _full_NLML(Prior: FullPriorDistribution) -> float:
    '''Negative log marginal likelihood for the full GPR

    Parameters
    ----------
    Prior : FullPriorDistribution
        prior distribution for which to calculate the NLML

    Returns
    -------
    float
    '''
    # logdet calculation
    K_NN_diag = jnp.diag(Prior.k_nn)
    logdet = 2*jnp.sum(jnp.log(K_NN_diag))

    # Fit calculation
    fit = Prior.y_data.T@jsp.linalg.cho_solve((Prior.k_nn, False), Prior.y_data)

    nlle = 0.5*(logdet + fit + len(Prior.y_data)*jnp.log(2*jnp.pi))
    
    return nlle / len(Prior.y_data)

def _fitc_NLML(Prior: SparsePriorDistribution) -> float:
    '''Negative log marginal likelihood for the sparse GPR

    Parameters
    ----------
    Prior : SparsePriorDistribution
        sparsified prior distribution for which to calculated the NLML

    Returns
    -------
    float
    '''
    # Logdet calculations
    U_inv_diag = jnp.diag(Prior.U_inv)
    logdet_K_inv = 2*jnp.sum(jnp.log(U_inv_diag))
    logdet_fitc = jnp.sum(jnp.log(Prior.diag))

    # Fit calculation
    Y_scaled = Prior.y_data / jnp.sqrt(Prior.diag)
    fit = Y_scaled.T@Y_scaled - Prior.proj_labs.T@Prior.proj_labs

    nlle = 0.5*(logdet_fitc + logdet_K_inv + fit + len(Prior.y_data)*jnp.log(2*jnp.pi))
    
    return nlle / len(Prior.y_data)