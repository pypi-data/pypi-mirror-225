"""
Contains various `numpy` utility programs.
"""

import sys
from math import cos, exp, floor, log, pi, sqrt
from typing import Any, Callable, Iterable, Union, cast

import numpy as np
from numpy.polynomial import Polynomial

from bs_python_utils.bsutils import bs_error_abort, print_stars

# some useful types
TwoArrays = tuple[np.ndarray, np.ndarray]
ThreeArrays = tuple[np.ndarray, np.ndarray, np.ndarray]
FourArrays = tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]
SixArrays = tuple[
    np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray
]
FloatOrArray = Union[float, np.ndarray]
Function_x = Callable[[np.ndarray], float]
Function_xa = Callable[[np.ndarray, int], float]
Function_xargs = Callable[[np.ndarray, list], float]
ArrayFunctionOfArray = Callable[[np.ndarray], np.ndarray]


def check_vector(v: Any, fun_name: str = None) -> int:
    """
    test that `v` is a vector; aborts otherwise

    Args:
        v: a vector, we hope
        fun_name: name of the calling function

    Returns:
        the size if successful
    """
    fun_str = ["" if fun_name is None else fun_name + ":"]
    if not isinstance(v, np.ndarray):
        bs_error_abort(f"{fun_str} v should be a Numpy array")
    v = cast(np.ndarray, v)
    ndims_v = v.ndim
    if ndims_v != 1:
        bs_error_abort(f"{fun_str} v should have one dimension, not {ndims_v}")
    return cast(int, v.size)


def check_matrix(x: Any, fun_name: str = None) -> tuple[int, int]:
    """
    test that `x` is a matrix; aborts otherwise

    Args:
        x: a matrix, we hope
        fun_name: name of the calling function

    Returns:
        the shape if successful
    """
    fun_str = ["" if fun_name is None else fun_name + ":"]
    if not isinstance(x, np.ndarray):
        bs_error_abort(f"{fun_str} Xx should be a Numpy array")
    x = cast(np.ndarray, x)
    ndims_x = x.ndim
    if ndims_x != 2:
        bs_error_abort(f"{fun_str} x should have two dimensions, not {ndims_x}")
    return cast(tuple[int, int], x.shape)


def check_vector_or_matrix(x: Any, fun_name: str = None) -> int:
    """
    test that `x` is a vector or a matrix; aborts otherwise

    Args:
        x: a vector or matrix, we hope
        fun_name: name of the calling function

    Returns:
        the number of dimensions of `x` (1 or 2)
    """
    fun_str = ["" if fun_name is None else fun_name + ":"]
    if not isinstance(x, np.ndarray):
        bs_error_abort(f"{fun_str} X should be a Numpy array")
    x = cast(np.ndarray, x)
    ndims_x = x.ndim
    if ndims_x != 1 and ndims_x != 2:
        bs_error_abort(f"{fun_str} x should have at most two dimensions, not {ndims_x}")
    return cast(int, ndims_x)


def check_square(A: Any, fun_name: str = None) -> int:
    """
    test that an object used in `fun_name` is a square matrix

    Args:
        A: square matrix, we hope
        fun_name: the name of the calling function

    Returns:
        the number of rows and columns of `A`
    """
    fun_str = ["" if fun_name is None else fun_name + ":"]
    if not isinstance(A, np.ndarray):
        bs_error_abort(f"{fun_str} A should be a Numpy array")
    A = cast(np.ndarray, A)
    if A.ndim == 2:
        n, nv = A.shape
        if nv != n:
            bs_error_abort(f"{fun_str} The matrix A should be square, not {A.shape}")
    else:
        bs_error_abort(f"{fun_name} A should have  two dimensions, not {A.ndim}")
    return cast(int, n)


def check_tensor(x: Any, n_dims: int, fun_name: str = None) -> tuple[int, ...]:
    """
    test that `x` is an `n_dims` dimensional array; aborts otherwise

    Args:
        x: an `n_dims` dimensional array, we hope
        fun_name: name of the calling function

    Returns:
        the shape if successful
    """
    fun_str = ["" if fun_name is None else fun_name + ":"]
    if not isinstance(x, np.ndarray):
        bs_error_abort(f"{fun_str} x should be a Numpy array")
    x = cast(np.ndarray, x)
    ndims_x = x.ndim
    if ndims_x != n_dims:
        bs_error_abort(f"{fun_str} x should have {n_dims} dimensions, not {ndims_x}")
        return (0,)  # for mypy
    return cast(tuple[int, ...], x.shape)


def grid_function(
    fun: Callable[[np.ndarray, np.ndarray], np.ndarray],
    x_points: np.ndarray,
    y_points: np.ndarray,
) -> np.ndarray:
    """apply a function f(x, y) on a lattice grid

    Args:
        fun: should return a matrix `(m, n)`  when called with two matrices `(m, n)`
        x_points: an `m`-vector
        y_points: an `n`-vector

    Returns:
        the `(m, n)` matrix of values of `fun` on the grid
    """
    _ = check_vector(x_points)
    _ = check_vector(y_points)
    X1, Y1 = np.meshgrid(x_points, y_points)
    z_grid = fun(X1, Y1).T
    return z_grid


# Numpy parallel RNG
def generate_RNG_streams(
    nsim: int, initial_seed: int = 13091962
) -> list[np.random.Generator]:
    """
    return `nsim` RNGs

    Args:
        nsim:  number of RNGs we want
        initial_seed: any large integer

    Returns:
        `nsim` streams

    Example:
        streams = generate_RNG_streams(10, 575856896)
        x = streams[i].normal(scale=s, size=(nmarkets, nproducts))
    """
    ss = np.random.SeedSequence(initial_seed)
    # Spawn off child SeedSequences to pass to child processes.
    child_seeds = ss.spawn(nsim)
    streams = [np.random.default_rng(s) for s in child_seeds]
    return streams


def ecdf(x: np.ndarray) -> np.ndarray:
    """Evaluate the empirical cdf at each point in sample

    Args:
        x: 1-dim array `(nobs)`

    Returns:
        A 1-dim array `(nobs)`  with the values of the empirical cdf at `x`, from 1/`nobs` to 1

    """
    if x.ndim != 1:
        print_stars(f"ecdf: x should have 1 dimension, not {x.ndim}")
        sys.exit()
    nx = x.size
    order_x = np.argsort(x)
    ecdf_val = np.zeros(nx)
    for i_order, n_order in enumerate(order_x):
        ecdf_val[n_order] = (i_order + 1.0) / nx
    return ecdf_val


def inv_ecdf(v: np.ndarray, q: np.ndarray | float) -> np.ndarray | float:
    """Evaluate the empirical `q`-quantiles of the sample `v`
    in a way that is consistent with `ecdf`.

    Args:
        v: 1-dim array `(nobs)` of the data points
        q: 1-dim array `(nobs)` of quantiles or float

    Returns:
        A 1-dim array `(nobs)`  with the values of the `q`-quantiles of `v`, or just the one quantile

    """
    if v.ndim != 1:
        bs_error_abort(f"v should have 1 dimension, not {v.ndim}")
    nv = v.size
    sorted_v = np.zeros(nv + 2)
    sorted_v[1 : (nv + 1)] = np.sort(v)
    sorted_v[0] = 2.0 * sorted_v[1] - sorted_v[2]  # added to extend for q < 1/nv
    sorted_v[nv + 1] = sorted_v[nv]  # added to extend for q = 1
    if isinstance(q, float):
        q_floor = np.array([floor(nv * q)])
        val_q = sorted_v[q_floor] + (nv * q - q_floor) * (
            sorted_v[q_floor + 1] - sorted_v[q_floor]
        )
        return cast(float, val_q)
    elif isinstance(q, np.ndarray):
        q_floor = np.floor(nv * q).astype(int)
        vals_q = sorted_v[q_floor] + (nv * q - q_floor) * (
            sorted_v[q_floor + 1] - sorted_v[q_floor]
        )
        return cast(np.ndarray, vals_q)


def nprepeat_col(v: np.ndarray, n: int) -> np.ndarray:
    """
    create a matrix with `n` columns equal to `v`

    Args:
        v: a 1-dim array of size `m`
        n: the number of columns requested

    Returns:
        a 2-dim array of shape `(m, n)`
    """
    return np.repeat(v[:, np.newaxis], n, axis=1)


def nprepeat_row(v: np.ndarray, m: int) -> np.ndarray:
    """
    create a matrix with `m` rows equal to `v`

    Args:
        v: a 1-dim array of size `n`
        m: the number of rows requested

    Returns:
        a 2-dim array of shape `(m, n)`
    """
    return np.repeat(v[np.newaxis, :], m, axis=0)


def npmaxabs(arr: np.ndarray) -> float:
    """
    maximum absolute value in an array

    Args:
        arr: any Numpy array

    Returns:
        the largest element in absolute value
    """
    return cast(float, np.max(np.abs(arr)))


def rice_stderr(
    y: np.ndarray, x: np.ndarray, is_sorted: bool = False
) -> np.ndarray | float:
    """
    computes the Rice local estimators of the standard error of y | x

    Args:
        y: vector of y-values
        x: vector of x-values
        is_sorted: set it to `True` if `x` is in increasing order

    Returns:
        an array of the same size with the stderr(y | x)
    """
    n = check_vector(x)
    ny = check_vector(y)
    if ny != n:
        bs_error_abort("x and y should have the same size")

    if not is_sorted:
        # need to sort by increasing value of x
        order_x = np.argsort(x)
        ys = y[order_x]
    else:
        ys = y

    variance_estimator = np.zeros(n)

    # we average over neighbors
    n_neighbors = int(sqrt(float(n)) / 2.0)
    facd = 1.0 / (2.0 * n_neighbors)
    n_neighbors2 = n_neighbors // 2

    # for the first observations
    yleft = ys[:n_neighbors2]
    dy = yleft[1:] - yleft[:-1]
    variance_estimator[:n_neighbors2] = np.sum(dy * dy) * facd

    # for the middle of the sample
    minus_nn2 = n - n_neighbors2
    for ix in range(n_neighbors2, minus_nn2):
        ix_neighbors = slice(ix - n_neighbors2, ix + n_neighbors2)
        yx = ys[ix_neighbors]
        dy = yx[1:] - yx[:-1]
        variance_estimator[ix] = np.sum(dy * dy) * facd

    # and for the last observations
    yright = ys[minus_nn2:]
    dy = yright[1:] - yright[:-1]
    variance_estimator[minus_nn2:] = np.sum(dy * dy) * facd

    stderr_estimator = np.sqrt(variance_estimator)

    return stderr_estimator


def nplog(
    arr: np.ndarray,
    eps: float = 1e-30,
    deriv: int = 0,
    verbose: bool = False,
) -> np.ndarray | TwoArrays | ThreeArrays:
    """
    $C^2$ extension of  $\\ln(a)$ below `eps`, perhaps with derivatives

    Args:
        arr: any Numpy array
        eps: lower bound
        deriv: if 1, compute derivative, if 2, second derivative
        verbose: prints debugging info

    Returns:
        $\\ln(a)$  $C^2$-extended below `eps`, perhaps with derivatives
    """
    if deriv not in [0, 1, 2]:
        bs_error_abort(f"deriv can only be 0, 1, or 2; not {deriv}")
    if np.min(arr) > eps:
        if deriv == 0:
            return cast(np.ndarray, np.log(arr))
        elif deriv == 1:
            return cast(TwoArrays, (np.log(arr), 1.0 / arr))
        # deriv == 2
        return cast(ThreeArrays, (np.log(arr), 1.0 / arr, -1.0 / (arr * arr)))
    else:
        logarreps = np.log(np.maximum(arr, eps))
        darr = 1.0 - arr / eps
        logarr_smaller = log(eps) - darr * (1.0 + darr / 2.0)
        if verbose:
            n_small_args = np.sum(arr < eps)
            if n_small_args > 0:
                finals = "s" if n_small_args > 1 else ""
                print(
                    f"nplog: {n_small_args} argument{finals} smaller than {eps}: mini ="
                    f" {np.min(arr)}"
                )
        logeps = np.where(arr > eps, logarreps, logarr_smaller)
        if deriv == 0:
            return logeps
        arreps = np.maximum(arr, eps)
        der_logarreps = 1.0 / arreps
        der_logarr_smaller = (1.0 + darr) / eps
        dlogeps = np.where(arr > eps, der_logarreps, der_logarr_smaller)
        if deriv == 1:
            return cast(TwoArrays, (logeps, dlogeps))
        # deriv == 2
        der2_logarreps = -1.0 / (arreps * arreps)
        der2_logarr_smaller = np.full(arr.shape, -1.0 / (eps * eps))
        d2logeps = np.where(arr > eps, der2_logarreps, der2_logarr_smaller)
        return cast(ThreeArrays, (logeps, dlogeps, d2logeps))


def npexp(
    arr: np.ndarray,
    bigx: float = 50.0,
    lowx: float = -50.0,
    deriv: int = 0,
    verbose: bool = False,
) -> np.ndarray | TwoArrays | ThreeArrays:
    """
    $C^2$ extension of  $\\exp(a)$ above `bigx` and below `lowx`,
    perhaps with derivatives

    Args:
        arr: any Numpy array
        bigx: upper bound
        lowx: lower bound
        deriv: if 1, compute derivative, if 2, second derivative
        verbose: prints debugging info


    Returns:
        $\\exp(a)$  $C^2$-extended above `bigx` and below `lowx`,
        perhaps with derivatives
    """
    if deriv not in [0, 1, 2]:
        bs_error_abort(f"deriv can only be 0, 1, or 2; not {deriv}")
    min_arr, max_arr = np.min(arr), np.max(arr)
    if max_arr <= bigx and min_arr >= lowx:
        exparr = np.exp(arr)
        if deriv == 0:
            return cast(np.ndarray, exparr)
        elif deriv == 1:
            return cast(TwoArrays, (exparr, exparr))
        # deriv == 2
        return cast(ThreeArrays, (exparr, exparr, exparr))
    else:  # some large and/or small arguments
        exparr = np.exp(np.maximum(np.minimum(arr, bigx), lowx))
        print(f"{exparr=}")
        ebigx = exp(bigx)
        elowx = exp(lowx)
        darrb = arr - bigx
        darrl = lowx - arr
        exparr_larger = ebigx * (1.0 + darrb * (1.0 + 0.5 * darrb))
        exparr_smaller = elowx * (1.0 - darrl * (1.0 - 0.5 * darrl))
        if verbose:
            n_large_args = np.sum(arr > bigx)
            finals = "s" if n_large_args > 1 else ""
            print(
                f"npexp: {n_large_args} argument{finals} larger than {bigx}:\n"
                f"maxi = {np.max(arr)}"
            )
            n_small_args = np.sum(arr < lowx)
            finals = "s" if n_small_args > 1 else ""
            print(
                f"npexp: {n_small_args} argument{finals} smaller than {lowx}:\n"
                f"mini = {np.min(arr)}"
            )
        expval = exparr
        print(expval)
        expval = np.where(arr > bigx, exparr_larger, expval)
        expval = np.where(arr < lowx, exparr_smaller, expval)
        if deriv == 0:
            return cast(np.ndarray, expval)
        dexpval = exparr
        dexparr_larger = ebigx * (1.0 + darrb)
        dexparr_smaller = elowx * (1.0 - darrl)
        dexpval = np.where(arr > bigx, dexparr_larger, dexpval)
        dexpval = np.where(arr < lowx, dexparr_smaller, dexpval)
        if deriv == 1:
            return cast(TwoArrays, (expval, dexpval))
        # deriv == 2
        d2expval = exparr
        return cast(ThreeArrays, (expval, dexpval, d2expval))


def _nppow_arrays(
    a: np.ndarray, b: np.ndarray, deriv: int
) -> np.ndarray | ThreeArrays | SixArrays:
    """implements nppow when a and b are conformal arrays"""
    avec = a.ravel()
    bvec = b.ravel()
    a_pow_b = avec**bvec
    a_pow_br = a_pow_b.reshape(a.shape)
    if deriv == 0:
        return cast(np.ndarray, a_pow_br)
    der_wrt_a = a_pow_b * bvec / avec
    log_avec = nplog(avec)
    der_wrt_b = a_pow_b * log_avec
    derivs1 = (der_wrt_a.reshape(a.shape), der_wrt_b.reshape(a.shape))
    if deriv == 1:
        return cast(ThreeArrays, (a_pow_br, *derivs1))
    # deriv == 2
    a_pow_b1 = a_pow_b / avec
    b1 = bvec - 1.0
    der2_wrt_aa = bvec * b1 * a_pow_b1 / avec
    der2_wrt_ab = a_pow_b1 * (1.0 + bvec * log_avec)
    der2_wrt_bb = a_pow_b * log_avec * log_avec
    derivs2 = (
        der2_wrt_aa.reshape(a.shape),
        der2_wrt_ab.reshape(a.shape),
        der2_wrt_bb.reshape(a.shape),
    )
    return cast(SixArrays, (a_pow_br, *derivs1, *derivs2))


def nppow(
    a: np.ndarray, b: int | float | np.ndarray, deriv: int = 0
) -> np.ndarray | ThreeArrays | SixArrays:
    """
    evaluates a**b element-by-element, perhaps with derivatives

    Args:
        a: an array
        b: if an array, should have the same shape as `a`
        deriv: if 1, compute derivative, if 2, second derivative

    Returns:
        an array of the same shape as `a`
    """
    if isinstance(b, float):
        mina = np.min(a)
        if mina < 0.0:
            bs_error_abort("All elements of a must be positive!")

    if isinstance(b, (int, float)):
        a_pow_b = a**b
        if deriv == 0:
            return a_pow_b
        log_a = np.log(a)
        derivs1 = (b * a_pow_b / a, a_pow_b * log_a)
        if deriv == 1:
            return cast(ThreeArrays, (a_pow_b, *derivs1))
        b1 = b - 1.0
        a_pow_b1 = a_pow_b / a
        # deriv == 2
        derivs2 = (
            b * b1 * a_pow_b1 / a,
            a_pow_b1 * (1.0 + b * log_a),
            a_pow_b * log_a * log_a,
        )
        return cast(SixArrays, (a_pow_b, *derivs1, *derivs2))
    else:
        if a.shape != b.shape:
            bs_error_abort("b is not a number or an array of the same shape as a!")
        return _nppow_arrays(a, b, deriv)


def nppad_beg_zeros(v: np.ndarray, n: int) -> np.ndarray:
    """
    pad the beginning of a 1-dim array with zeros to increase its size to `n`, if needed

    Args:
        v: 1-dim array of size `(nv)`
        n: size requested

    Returns:
        padded array if `nv` < `n`, otherwise `v`
    """
    nv = check_vector(v)
    if nv < n:
        return np.pad(v, (n - nv, 0))
    else:
        return v


def nppad_end_zeros(v: np.ndarray, n: int) -> np.ndarray:
    """
    pad the end of a 1-dim array with zeros to increase its size to `n`, if needed

    Args:
        v: 1-dim array of size `(nv)`
        n: size requested

    Returns:
        padded array if `nv` < `n`, else `v`
    """
    nv = check_vector(v)
    if nv < n:
        return np.pad(v, (0, n - nv))
    else:
        return v


def nppad2_end_zeros(mat: np.ndarray, m: int, n: int) -> np.ndarray:
    """
    pad the ends of a 2-dim array with zeros to increase its size to `(m,n)`, if needed

    Args:
        mat: 2-dim array
        m: number of rows requested
        n: number of columns requested

    Returns:
        padded array, where needed
    """
    nrows, ncols = check_matrix(mat)
    max_rows = max(m, nrows)
    max_cols = max(n, ncols)
    if nrows < max_rows and ncols < max_cols:  # pad both dimensions
        pmat = np.zeros((m, n))
        pmat[:nrows, :ncols] = mat
        return pmat
    elif nrows < max_rows:  # pad rows
        pmat = np.zeros((m, ncols))
        pmat[:nrows, :] = mat
        return pmat
    elif ncols < max_cols:  # pad columns
        pmat = np.zeros((nrows, n))
        pmat[:, :ncols] = mat
        return pmat
    else:  # no need for padding
        return mat


def bsgrid(v: np.ndarray, w: np.ndarray) -> np.ndarray:
    """
    make a two-dimensional matrix of all pairs of elements of the vectors `v` and `w`

    Args:
        v: basis vector, size m
        w: basis vector, size n

    Returns:
        an array of shape `(m n, 2)`
    """
    m = check_vector(v)
    n = check_vector(w)
    m, n = v.size, w.size
    v1 = np.repeat(v, n)
    v2 = np.tile(w, m)
    return np.column_stack((v1, v2))


def bs_sqrt_pdmatrix(m: np.ndarray) -> np.ndarray:
    """
    square root of a positive definite matrix

    Args:
        m: a positive definite matrix

    Returns:
        the square root of the matrix
    """
    _ = check_square(m, "bs_sqrt_pdmatrix")
    eigval, eigvec = np.linalg.eigh(m)
    eigval = np.maximum(eigval, 0.0)
    eigval_sqrt = np.sqrt(eigval)
    eigval_sqrt_diag = np.diag(eigval_sqrt)
    res = eigvec @ eigval_sqrt_diag @ eigvec.T
    return cast(np.ndarray, res)


def make_lexico_grid(arr: np.ndarray) -> np.ndarray:
    """
    make a lexicographic grid

    Args:
        arr: `nr`-vector or `(nr,nc)` matrix; `nc` must be 1, 2 or 3

    Returns:
        `arr` if it is a vector; otherwise a matrix `({nr}^{nc}, {nc})`
            for `nc=2`  it is like `bsgrid`
    """
    ndims_arr = check_vector_or_matrix(arr, "make_lexico_grid`")
    if ndims_arr == 1:
        return arr
    else:
        nr, nc = arr.shape
        if nc == 2:
            n0 = np.repeat(arr[:, 0], nr)
            n1 = np.tile(arr[:, 1], nr)
            return np.column_stack((n0, n1))
        elif nc == 3:
            nr2 = nr * nr
            n0 = np.repeat(arr[:, 0], nr2)
            n1 = np.repeat(np.tile(arr[:, 1], nr), nr)
            n2 = np.tile(arr[:, 2], nr2)
            return np.column_stack((n0, n1, n2))
        else:
            bs_error_abort(
                f"at this stage, the number of columns must be 3 or less, not {nc}..."
            )
            return arr  # for mypy


class BivariatePolynomial:
    """
    a class for bivariate polynomials as a list of `Polynomial` objects

    minimal interface:

        * construct from matrix of coefficients
        * add, subtract, multiply (with constant and with :class:`BivariatePolynomial`)
        * evaluate  p(x, y) when x, y are at most vectors (and have the same shape if both vectors)
    """

    def __init__(self, coeffs: np.ndarray):
        """
        constructor for :class:`BivariatePolynomial`

        coeffs: a two-dimensional array `(deg1+1, deg2+2)`
        """
        self.deg1, self.deg2 = coeffs.shape[0] - 1, coeffs.shape[1] - 1
        self.coef = coeffs
        self.listpol2 = []
        for k in range(self.deg1 + 1):
            self.listpol2.append(Polynomial(coeffs[k, :]))

    def __add__(self, bivpol):
        if isinstance(bivpol, (int, float)):
            coeffs = self.coef.copy()
            coeffs[0, 0] += bivpol
            return BivariatePolynomial(coeffs)
        degbp1, degbp2 = bivpol.deg1, bivpol.deg2
        max_deg1 = max(degbp1, self.deg1)
        max_deg2 = max(degbp2, self.deg2)
        coeffs_new = nppad2_end_zeros(self.coef, max_deg1 + 1, max_deg2 + 1)
        coeffsbp_new = nppad2_end_zeros(bivpol.coef, max_deg1 + 1, max_deg2 + 1)
        return BivariatePolynomial(coeffs_new + coeffsbp_new)

    def __repr__(self):
        return f"BivariatePolynomial({self.deg1!r}, {self.deg2!r})"

    def __iadd__(self, bivpol):
        return self.__add__(bivpol)

    def __radd__(self, bivpol):
        return self.__add__(bivpol)

    def __sub__(self, bivpol):
        if isinstance(bivpol, (int, float)):
            coeffs = self.coef.copy()
            coeffs[0, 0] -= bivpol
            return BivariatePolynomial(coeffs)
        degbp1, degbp2 = bivpol.deg1, bivpol.deg2
        max_deg1 = max(degbp1, self.deg1)
        max_deg2 = max(degbp2, self.deg2)
        coeffs_new = nppad2_end_zeros(self.coef, max_deg1 + 1, max_deg2 + 1)
        coeffsbp_new = nppad2_end_zeros(bivpol.coef, max_deg1 + 1, max_deg2 + 1)
        return BivariatePolynomial(coeffs_new - coeffsbp_new)

    def __mul__(self, bivpol):
        if isinstance(bivpol, (int, float)):
            return BivariatePolynomial(bivpol * self.coef)
        deg1, degbp1 = self.deg1, bivpol.deg1
        deg2, degbp2 = self.deg2, bivpol.deg2
        degmul1 = deg1 + degbp1
        degmul2 = deg2 + degbp2
        lp2, blp2 = self.listpol2, bivpol.listpol2

        coeffs_mul = np.zeros((degmul1 + 1, degmul2 + 1))
        for m in range(degmul1 + 1):
            minm = max(0, m - degbp1)
            maxm = min(m, self.deg1)
            pm = Polynomial(0)
            for i in range(minm, maxm + 1):
                pm += lp2[i] * blp2[m - i]
            coeffs_mul[m, :] += pm.coef

        bp_mul = BivariatePolynomial(coeffs_mul)
        return bp_mul

    def __rmul__(self, bivpol):
        return self.__mul__(bivpol)

    def __call__(self, x1, x2):
        x1fac = 1.0
        val = 0.0
        for p in self.listpol2:
            val += p(x2) * x1fac
            x1fac *= x1
        return val


def outer_bivar(pol1: Polynomial, pol2: Polynomial) -> BivariatePolynomial:
    """
    make a `BivariatePolynomial` from the  product of two `Polynomial` objects

    Args:
        pol1: Polynomial in the first variable
        pol2: Polynomial in the second variable

    Returns:
        a `BivariatePolynomial` = `pol1 * pol2`
    """
    p1 = pol1.coef
    p2 = pol2.coef
    prod_coef = np.outer(p1, p2)
    return BivariatePolynomial(prod_coef)


def npxlogx(
    arr: np.ndarray,
    eps: float = 1e-30,
    deriv: int = 0,
    verbose: bool = False,
) -> np.ndarray | TwoArrays | ThreeArrays:
    """
    $C^2$ extension of  $a\\ln(a)$ below `eps`, perhaps with derivatives

    Args:
        arr: a Numpy array
        eps: lower bound
        deriv: if 1, compute derivative, if 2, second derivative
        verbose: prints debugging info

    Returns:
        $a\\ln(a)$  $C^2$-extended  below `eps`, perhaps with derivatives
    """
    if deriv not in [0, 1, 2]:
        bs_error_abort(f"deriv must be 0, 1, or 2; not {deriv}")
    if np.min(arr) > eps:
        return cast(np.ndarray, arr * np.log(arr))
    else:
        logeps = log(eps)
        logarreps = np.log(np.maximum(arr, eps))
        xlogarreps = arr * logarreps
        xlogarr_smaller = arr * (arr / eps + logeps - 1.0)
        if verbose:
            n_small_args = np.sum(arr < eps)
            if n_small_args > 0:
                finals = "s" if n_small_args > 1 else ""
                print(
                    f"npxlogx: {n_small_args} argument{finals} smaller than {eps}: mini"
                    f" = {np.min(arr)}"
                )
        xlogval = np.where(arr > eps, xlogarreps, xlogarr_smaller)
        if deriv == 0:
            return xlogval
        dxlogarreps = 1.0 + logarreps
        dxlogarr_smaller = logeps + arr / eps
        dxlogval = np.where(arr > eps, dxlogarreps, dxlogarr_smaller)
        if deriv == 1:
            return cast(TwoArrays, (xlogval, dxlogval))
        # deriv == 2
        d2xlogval = 1.0 / np.maximum(arr, eps)
        return cast(ThreeArrays, (xlogval, dxlogval, d2xlogval))


def gauher(n: int) -> TwoArrays:
    """
    nodes and weights for Gauss-Hermite integration

    Args:
        n: number of nodes

    Returns:
        array of `n` nodes, array of `n` weights
    """
    EPS = 1.0e-14
    PIM4 = 0.7511255444649425
    MAXIT = 10

    x = np.zeros(n)
    w = np.zeros(n)

    m = (n + 1) // 2

    for i in range(m):
        if i == 0:
            n2 = 2.0 * n + 1.0
            z = sqrt(n2) - 1.85575 * (n2**-0.16667)
        elif i == 1:
            z -= 1.14 * (n**0.426) / z
        elif i == 2:
            z = 1.86 * z - 0.86 * x[0]
        elif i == 3:
            z = 1.91 * z - 0.91 * x[1]
        else:
            z = 2.0 * z - x[i - 2]
        for _n_iter in range(MAXIT):
            p1 = PIM4
            p2 = 0.0
            for j in range(n):
                p3 = p2
                p2 = p1
                p1 = z * sqrt(2.0 / (j + 1)) * p2 - sqrt(j / (j + 1)) * p3
            pp = sqrt(2 * n) * p2
            z1 = z
            z = z1 - p1 / pp
            if abs(z - z1) <= EPS:
                break
        if _n_iter >= MAXIT:
            bs_error_abort(f"too many iterations: {_n_iter}")
        x[i] = z
        x[n - 1 - i] = -z
        w[i] = 2.0 / (pp * pp)
        w[n - 1 - i] = w[i]

    # need to reverse order for x (w is symmetric)
    return cast(TwoArrays, (x[::-1], w))


def gauleg(n: int) -> TwoArrays:
    """
    nodes and weights for Gauss-Legendre integration `\\int_{-1}^1 f(x)dx`

    Args:
        n: number of nodes

    Returns:
        array of `n` nodes, array of `n` weights
    """
    x = np.zeros(n)
    w = np.zeros(n)
    EPS = 3e-11
    m = (n + 1) // 2
    for i in range(1, m + 1):
        z = cos(pi * (i - 0.25) / (n + 0.5))
        z1 = np.inf
        while abs(z - z1) > EPS:
            p1 = 1.0
            p2 = 0.0
            for j in range(1, n + 1):
                p3 = p2
                p2 = p1
                p1 = ((2.0 * j - 1.0) * z * p2 - (j - 1.0) * p3) / j
            pp = n * (z * p1 - p2) / (z * z - 1.0)
            z1 = z
            z = z1 - p1 / pp
        x[i - 1] = -z
        x[n - i] = z
        w[i - 1] = 2.0 / ((1.0 - z * z) * pp * pp)
        w[n - i] = w[i - 1]

    return cast(TwoArrays, (x, w))


def gaussian_expectation(
    f: Callable,
    x: np.ndarray | None,
    w: np.ndarray | None,
    n: int = 16,
    vectorized: bool = False,
    pars: Iterable = None,
) -> np.ndarray | float:
    """
    computes the expectation of a function of an `N(0,1)` random variable
    using Gauss-Hermite with n nodes
    the nodes and weights can be provided, if available

    Args:
        f: a scalar or array function of a scalar or array variable and possibly other parameters
        vectorized: if True, the function accepts an array as argument
        pars: parameters for `f`, if any
        n: number of nodes
        x: locations of the nodes
        w: their weights

    Returns:
        the expectation of `f(N(0,1))`
    """
    if x is None:
        nodes, weights = gauher(n)
        nodes *= sqrt(2.0)
        weights /= sqrt(pi)
        n_nodes = n
    elif w is None:
        bs_error_abort("x is None but w is not")
    elif w.size != x.size:
        bs_error_abort("x has {x.size} elements and w has {w.size}")
    else:
        nodes = x * sqrt(2.0)
        weights = w / sqrt(pi)
        n_nodes = nodes.size
    if pars is None:
        if vectorized:
            integral_vec = f(nodes) @ weights
        else:
            # to ensure integral_val has the same shape as f
            integral_val = weights[0] * f(nodes[0])
            for i in range(1, n_nodes):
                integral_val += weights[i] * f(nodes[i])
    else:
        if vectorized:
            integral_vec = f(nodes, pars) @ weights
        else:
            # to ensure integral_val has the same shape as f
            integral_val = weights[0] * f(nodes[0], pars)
            for i in range(1, n_nodes):
                integral_val += weights[i] * f(nodes[i], pars)

    return cast(np.ndarray, integral_vec) if vectorized else cast(float, integral_val)


def legendre_polynomials(
    x: np.ndarray,
    max_deg: int,
    a: float = -1.0,
    b: float = 1.0,
    no_constant: bool = False,
) -> np.ndarray:
    """evaluates the Legendre polynomials over x in the interval [a, b]

    Args:
        x: the points where the polynomials are to be evaluated
        max_deg: the maximum degree
        a: the start of the interval, classically -1
        b: the end of the interval, classically 1
        no_constant: if True, delete the constant polynomial

    Returns:
        an array of (max_deg+1) arrays of the shape of x
    """
    sx = check_vector(x)
    if a > np.min(x):
        sys.exit("legendre_polynomials: points below start of interval")
    if b < np.max(x):
        sys.exit("legendre_polynomials: points above end of interval")
    p = np.zeros((sx, max_deg + 1))
    x_transf = 2.0 * (x - a) / (b - a) - 1.0
    p[:, 0] = np.ones_like(x)
    p[:, 1] = x_transf
    for deg in range(2, max_deg + 1):
        p2 = (2 * deg - 1) * (p[:, deg - 1] * x_transf) - (deg - 1) * p[:, deg - 2]
        p[:, deg] = p2 / deg
    polys_p = p[:, 1:] if no_constant else p
    return polys_p


def quantile_transform(v: np.ndarray) -> np.ndarray:
    """transform a vector of counts into the corresponding quantiles

    Args:
        v:  a vector of counts

    Returns:
         the corresponding quantiles
    """
    n = check_vector(v)
    q = np.zeros(n)
    for i in range(n):
        q[i] = np.sum(v <= v[i]) / (n + 1)
    return q


def print_quantiles(
    v: np.ndarray | Iterable[np.ndarray], quantiles: np.ndarray
) -> np.ndarray:
    """print these quantiles of the array(s)

    Args:
        v:  a vector or an iterable of vectors
        quantiles: quantiles in [0,1]

    Returns:
         the corresponding quantiles as a vector or a matrix
    """
    nq = check_vector(quantiles)
    if isinstance(v, np.ndarray):
        qvals = np.quantile(v, quantiles)
        for q, qv in zip(quantiles, qvals, strict=True):
            print(f"Quantile {q: .3f}: {qv: >10.3f}")
    elif isinstance(v, Iterable):
        v = list(v)
        for v_i in v:
            _ = check_vector(v_i)
        nv = len(v)
        qvals = np.zeros((nq, nv))
        for i in range(nv):
            qvals[:, i] = np.quantile(v[i], quantiles)
        for iq, q in enumerate(quantiles):
            s = f"Quantile {q: .3f}: "
            qv = qvals[iq, :]
            for i in range(nv):
                s += f"  {qv[i]: >10.3f}"
            print(f"{s}")
    else:
        bs_error_abort("v must be  a vector or a list of vectors")

    return cast(np.ndarray, qvals)


def set_elements_abovebelow_diagonal(
    matrix: np.ndarray, scalar: int | float, location: str
) -> np.ndarray:
    """
    Sets all elements of the given matrix above or below the diagonal
    to the specified scalar value.

    Args:
        matrix: the input matrix; it must be square
        scalar: The scalar value to set the elements above or below the diagonal.
        location: 'above', 'below', 'on_above', 'on_below'.

    Returns:
        The updated matrix with elements above or below the diagonal set to the scalar value,
        including the diagonal for the `on_` options.
    """
    _ = check_square(matrix, "set_elements_abovebelow_diagonal")
    # copy the matrix
    new_matrix = matrix.copy()

    # Get the indices of elements above or below the diagonal
    if location == "above":
        row_indices, col_indices = np.triu_indices_from(new_matrix, k=1)
    elif location == "below":
        row_indices, col_indices = np.tril_indices_from(new_matrix, k=-1)
    elif location == "on_above":
        row_indices, col_indices = np.triu_indices_from(new_matrix, k=0)
    elif location == "on_below":
        row_indices, col_indices = np.tril_indices_from(new_matrix, k=0)
    else:
        bs_error_abort(
            f"""
        location can only be 'above', 'below', 
        'on_above' or 'on_below', not {location}
        """
        )

    # Set the elements above or below the diagonal to the scalar value
    new_matrix[row_indices, col_indices] = scalar

    return new_matrix
