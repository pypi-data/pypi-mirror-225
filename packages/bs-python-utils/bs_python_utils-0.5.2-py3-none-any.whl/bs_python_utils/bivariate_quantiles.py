"""This takes in observations of a bivariate random variable `y`
and computes vector quantiles and vector ranks.

The sequence of steps is as follows:

1.  choose a  number of Chebyshev nodes for numerical integration and
 optimize the weights: `v = solve_for_v(y, n_nodes)`

2a. to obtain the $(u_1,u_2)$ quantiles for $u_1, u_2\\in [0,1]$, run
`qtiles_y = bivariate_quantiles_v(y, v, u1, u2)`

2b.  to compute the vector ranks for all points in the sample (the barycenters of the cells in the power diagram):
`ranks_y = bivariate_ranks_v(y, v, n_nodes)`

Steps 1 and 2a can be combined: `qtiles_y = bivariate_quantiles(y, v, u1, u2, n_nodes)`

Steps 1 and 2b can be combined: `ranks_y = bivariate_ranks(y, n_nodes)`
"""
from typing import cast

import numpy as np

from bs_python_utils.bs_opt import (
    minimize_free,
    print_optimization_results,
)
from bs_python_utils.bsnputils import (
    TwoArrays,
    npmaxabs,
)
from bs_python_utils.bsutils import bs_error_abort
from bs_python_utils.chebyshev import Interval, cheb_get_nodes_1d


def compute_ab_(y_sorted: np.ndarray, v_sorted: np.ndarray) -> TwoArrays:
    """evaluates the A and B matrices

    Args:
        y_sorted: the observations, an `(n,2)` matrix sorted by increasing `y[:, 1]`
        v_sorted: the weights, an `n`-vector in the same sort order

    Returns:
        two `(n, n)` matrices

    Warning:
        the user must make sure that `y` and `v` have been sorted beforehand
    """
    n = v_sorted.size
    y1 = y_sorted[:, 0]
    dy1 = np.subtract.outer(y1, y1)
    y2 = y_sorted[:, 1]
    dy2 = np.subtract.outer(y2, y2)
    np.fill_diagonal(dy2, np.ones(n))  # to avoid division by 0
    dv = np.subtract.outer(v_sorted, v_sorted)
    a_mat = dy1.T / dy2
    b_mat = dv.T / dy2
    return a_mat, b_mat


def compute_u2_bounds_(
    k: int, u1: np.ndarray, a_mat: np.ndarray, b_mat: np.ndarray
) -> TwoArrays:
    """for given u1, calculates the bounds on u2 that make k the chosen observation

    Args:
        k: an integer between 0 and (n-1)
        u1: a vector of size `m`
        a_mat: the `A` matrix of size `(n,n)`
        b_mat: the `B` matrix of size `(n,n)`

    Returns:
        two vectors of size `m`, the left and right bounds in [0,1]
    """
    n = a_mat.shape[0]
    m = u1.size
    if k == 0:
        left_bound = np.zeros(m)
        a_right = a_mat[0, 1:]
        b_right = b_mat[0, 1:]
        right_bound = np.min(np.outer(u1, a_right) - b_right, 1)
    elif 1 <= k < n - 1:
        a_left = a_mat[k, :k]
        b_left = b_mat[k, :k]
        left_bound = np.max(np.outer(u1, a_left) - b_left, 1)
        a_right = a_mat[k, (k + 1) :]
        b_right = b_mat[k, (k + 1) :]
        right_bound = np.min(np.outer(u1, a_right) - b_right, 1)
    elif k == n - 1:
        a_left = a_mat[-1, :-1]
        b_left = b_mat[-1, :-1]
        left_bound = np.max(np.outer(u1, a_left) - b_left, 1)
        right_bound = np.ones(m)
    else:
        bs_error_abort(f"{k=} is not compatible with {n=}")
    left_bound = np.clip(left_bound, 0.0, 1.0)
    right_bound = np.clip(right_bound, 0.0, 1.0)

    return left_bound, right_bound


def bivariate_quantiles_v(y: np.ndarray, u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """computes the vector quantiles of `y` at values `u`, given the converged `v`

    Args:
        y: the observations, an `(n,2)` matrix
        u: the values where we want the quantiles, an `(m,2)` matrix in $[0,1]$
        v: the converged values of the weights, an `n`-vector

    Returns:
        an `(m,2)` matrix with the quantiles of `y` at the values `u`
    """
    net_val = u @ y.T - v
    k_max = np.argmax(net_val, 1)
    return cast(np.ndarray, y[k_max])


def bivariate_ranks_v(
    y: np.ndarray, v: np.ndarray, n_nodes: int = 32, presorted: bool = False
) -> np.ndarray:
    """computes the vector ranks of `y`, given the converged `v`

    Args:
        y: the observations, an `(n,2)` matrix
        v: the converged values of the weights, an `n`-vector
        n_nodes: the number of nodes for Chebyshev integration
        presorted: if `True`, then `y` and `v` are sorted by increasing `y[:, 1]`.

    Returns:
        an `(n,2)` matrix with the average ranks of `y`
    """
    n, d = y.shape

    if d != 2:
        bs_error_abort(f"only works for 2-dimensional y, not for {d}")

    interval01 = Interval(0.0, 1.0)
    u1_nodes, u1_weights = cheb_get_nodes_1d(interval01, n_nodes)

    if presorted:
        sort_order = np.arange(n)
        y_sorted = y
        v_sorted = v
    else:
        sort_order = np.argsort(y[:, 1])
        y_sorted = y[sort_order, :]
        v_sorted = v[sort_order]

    a_mat, b_mat = compute_ab_(y_sorted, v_sorted)

    average_ranks = np.zeros((n, 2))

    for k in range(n):
        left_bounds, right_bounds = compute_u2_bounds_(k, u1_nodes, a_mat, b_mat)
        pos_diffs = np.maximum(right_bounds - left_bounds, 0.0)
        pos_diffs_sq = np.maximum(
            right_bounds * right_bounds - left_bounds * left_bounds, 0.0
        )
        prob_k = pos_diffs @ u1_weights
        average_ranks[sort_order[k], 0] = ((u1_nodes * pos_diffs) @ u1_weights) / prob_k
        average_ranks[sort_order[k], 1] = ((pos_diffs_sq @ u1_weights) / 2.0) / prob_k

    return average_ranks


def objgrad_(
    v_sorted: np.ndarray, args: list, gr: bool = False
) -> float | tuple[float, np.ndarray]:
    """computes the expectation of $\\psi(U, v)$ and perhaps its gradient wrt `v`

    Args:
        v_sorted: an `n`-vector of weights, sorted by increasing `y[:, 1]`
        args: a list of other arguments `[y_sorted, u1_nodes, u1_weights, verbose]`
        gr: if `True`, we also evaluate the gradient

    Returns:
        the value of the expectation and perhaps its gradient
    """
    y_sorted = args[0]
    n = y_sorted.shape[0]
    u1_nodes = args[1]
    u1_weights = args[2]
    vs1 = np.append(v_sorted, -np.sum(v_sorted))
    a_mat, b_mat = compute_ab_(y_sorted, vs1)

    obj_val = 0.0
    probs = np.zeros(n)
    for k in range(n):
        left_bounds, right_bounds = compute_u2_bounds_(k, u1_nodes, a_mat, b_mat)
        pos_diffs = np.maximum(right_bounds - left_bounds, 0.0)
        pos_diffs_sq = np.maximum(
            right_bounds * right_bounds - left_bounds * left_bounds, 0.0
        )
        obj_val += (
            y_sorted[k, 0] * ((u1_nodes * pos_diffs) @ u1_weights)
            + y_sorted[k, 1] * (pos_diffs_sq @ u1_weights) / 2.0
        )
        probs[k] = pos_diffs @ u1_weights
        obj_val -= vs1[k] * probs[k]

    if gr:
        grad_val = probs[-1] - probs[:-1]
        return obj_val, grad_val
    else:
        return cast(float, obj_val)


def obj_(v_sorted: np.ndarray, args: list):
    return objgrad_(v_sorted, args)


def grad_(v_sorted: np.ndarray, args: list):
    res_objg = cast(tuple[float, np.ndarray], objgrad_(v_sorted, args, gr=True))
    grad_val = res_objg[1]
    verbose = args[3]
    if verbose:
        print(f"grad_err is {npmaxabs(grad_val)}")
    return grad_val


def solve_for_v_(y: np.ndarray, n_nodes: int = 32, verbose: bool = False) -> np.ndarray:
    n, d = y.shape

    if d != 2:
        bs_error_abort(f"only works for 2-dimensional y, not for {d}")

    # sort by increasing y[:, 1]
    sort_order = np.argsort(y[:, 1])
    y_sorted = y[sort_order, :]

    v0 = np.mean(y_sorted[:-1, :], 1)

    interval01 = Interval(0.0, 1.0)
    u1_nodes, u1_weights = cheb_get_nodes_1d(interval01, n_nodes)

    argsog = [y_sorted, u1_nodes, u1_weights, verbose]

    res = minimize_free(obj_, grad_, v0, args=argsog)
    if verbose:
        print_optimization_results(res, "Minimizing over v")

    if not res.success:
        bs_error_abort("Problem! the optimization failed.")
    vstar = res.x
    if verbose:
        print(f"The final gradient over v is close to 0: error {npmaxabs(res.jac)}")
    vstar1_sorted = np.append(vstar, -np.sum(vstar))

    # revert to original order
    vstar1 = np.zeros_like(vstar1_sorted)
    vstar1[sort_order] = vstar1_sorted

    return vstar1


def bivariate_quantiles(
    y: np.ndarray, u: np.ndarray, n_nodes: int = 32, verbose: bool = False
) -> np.ndarray:
    """computes the bivariate quantiles of `y` at the quantiles `u`

    Args:
        y: the observations, an `(n, 2)` matrix
        u: the quantiles at which to compute the bivariate quantiles,
            an `(m, 2)` matrix
        n_nodes: the number of nodes to use for the quadrature
        verbose: if `True`, print some information

    Returns:
        an `(m, 2)` matrix of bivariate quantiles
    """
    v = solve_for_v_(y, n_nodes, verbose)
    return bivariate_quantiles_v(y, u, v)


def bivariate_ranks(
    y: np.ndarray, n_nodes: int = 32, verbose: bool = False
) -> np.ndarray:
    """computes the bivariate ranks of `y`

    Args:
        y: the observations, an `(n, 2)` matrix
        n_nodes: the number of nodes to use for the quadrature
        verbose: if `True`, print some information

    Returns:
        the `(n, 2)` matrix of bivariate average ranks
    """
    v = solve_for_v_(y, n_nodes, verbose)
    return bivariate_ranks_v(y, v, n_nodes)
