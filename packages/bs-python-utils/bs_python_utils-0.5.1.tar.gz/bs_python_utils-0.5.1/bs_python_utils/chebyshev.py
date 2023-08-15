from dataclasses import dataclass
from typing import cast

import numpy as np
import numpy.polynomial.chebyshev as ncheb

from bs_python_utils.bsnputils import (
    ArrayFunctionOfArray,
    FloatOrArray,
    TwoArrays,
    bsgrid,
    check_square,
    check_vector,
)
from bs_python_utils.bsutils import bs_error_abort


@dataclass
class Interval:
    """a real interval $[x_0,x_1]$"""

    x0: float
    x1: float

    def __post_init__(self):
        x0, x1 = self.x0, self.x1
        if x0 > x1:
            bs_error_abort(f"x0 = {x0} is larger than x1 = {x1}")

    def bounds(self):
        return self.x0, self.x1


@dataclass
class Rectangle:
    """a product interval $[x_0,x_1] \times [y_0, y_1]$"""

    x_interval: Interval
    y_interval: Interval


def move_from1m1(t: FloatOrArray, interval: Interval) -> FloatOrArray:
    """get the position of `t` in $[-1,1]$ and move it in the same position in `interval`

    Args:
        t: position(s) within `$[-1,1]$
        interval: the Interval

    Returns:
        `x` rescaled to $[-1,1]$
    """
    x0, x1 = interval.bounds()
    return cast(FloatOrArray, ((x1 - x0) * t + (x0 + x1)) / 2.0)


def move_to1m1(x: FloatOrArray, interval: Interval) -> FloatOrArray:
    """get the position of `x` in `interval` and move it to the same position in $[-1,1]$

    Args:
        x: position(s) within `interval`
        interval: the Interval

    Returns:
        `x` rescaled to $[-1,1]$
    """
    x0, x1 = interval.bounds()
    return cast(FloatOrArray, (2.0 * x - (x0 + x1)) / (x1 - x0))


def cheb_get_nodes_1d(interval: Interval, degree: int) -> TwoArrays:
    """get the Chebyshev nodes and weights on the interval $[x0, x1]$

    Args:
        interval: the Interval $[x_0, x_1]$
        degree: the degree of the highest Chebyshev polynomial

    Returns:
        two `degree`-vectors of Chebyshev nodes and weights on the interval $[x_0, x_1]$
        so that `g(nodes) @ weights` approximates the unweighted integral of $g(x)$ on $[x_0,x_1]$
    """
    nodes1m1, weights1m1 = ncheb.chebgauss(degree)  # om=n [-1, 1]
    x0, x1 = interval.bounds()
    nodes = move_from1m1(nodes1m1, interval)
    weights = (x1 - x0) * weights1m1 * np.sqrt(1.0 - nodes1m1 * nodes1m1) / 2.0
    return cast(np.ndarray, nodes), cast(np.ndarray, weights)


def cheb_eval_fun_at_nodes_1d(
    fun: ArrayFunctionOfArray,
    nodes: np.ndarray | None = None,
    interval: Interval | None = None,
    degree: int | None = None,
) -> np.ndarray:
    """evaluate a function at the Chebyshev nodes on an interval

    Args:
        fun: the function to evaluate on an interval
        nodes: the Chebyshev nodes on that interval, if precomputed
        interval: the Interval
        degree: the degree of the Chebyshev  expansion

    Notes:
        `interval`, `degree` are required if `nodes` is not provided

    Returns:
        the values of the function at the Chebyshev nodes
    """
    if nodes is None:
        if degree is None or interval is None:
            bs_error_abort("if nodes is not provided, then degree and interval must be")
        degree = cast(int, degree)
        interval = cast(Interval, interval)
        nodes, _ = cheb_get_nodes_1d(interval, degree)
    vals_at_nodes = fun(nodes)
    return vals_at_nodes


def cheb_get_coefficients_1d(
    fun: ArrayFunctionOfArray, interval: Interval, degree: int
) -> np.ndarray:
    """get the Chebyshev coefficients for `fun` on an interval

    Args:
        fun: the function
        interval: the Interval
        degree: the degree of the Chebyshev  expansion

    Returns:
        a `degree`-vector of coefficients
    """

    def fun_t(t: np.ndarray) -> np.ndarray:
        x = cast(np.ndarray, move_from1m1(t, interval))
        return fun(x)

    c = ncheb.chebinterpolate(fun_t, degree)
    return cast(np.ndarray, c)


def cheb_interp_1d(
    x_vals: np.ndarray,
    interval: Interval,
    c: np.ndarray | None = None,
    fun: ArrayFunctionOfArray | None = None,
    degree: int | None = None,
) -> TwoArrays:
    """interpolate a function on on interval using Chebyshev polynomials

    Args:
        x_vals: the values at which to interpolate
        interval: the Interval
        c: the Chebyshev coefficients for `fun`, if already known; otherwise we compute them
        fun: the function to interpolate
        degree: the degree of the Chebyshev expansion

    Notes:
        `fun` and `degree` are required if `c` is not provided

    Returns:
        the values of the interpolation at `x_vals` and the Chebyshev coefficients `c`
    """
    if c is None:
        if degree is None or fun is None:
            bs_error_abort("since c is not  provided, fun and degree must be.")
        degree = cast(int, degree)
        fun = cast(ArrayFunctionOfArray, fun)
        c = cheb_get_coefficients_1d(fun, interval, degree)
    y_vals = ncheb.chebval(move_to1m1(x_vals, interval), c)
    return y_vals, c


def cheb_find_root(
    f: ArrayFunctionOfArray, degree: int, interval: Interval | None = None
) -> np.ndarray | tuple[np.ndarray, np.ndarray | float | None]:
    """find the roots of $f(x)=0$ in $[0,1]$; also return the one(s) within the interval, if given

    Args:
        f: the function
        degree: the degree of the Chebyshev expansion
        interval: the interval where we want the root

    Returns:
        the roots in $[0,1]$;  and the one(s) in `interval`, if specified
    """
    interval01 = Interval(0.0, 1.0)
    coeffs_f = cheb_get_coefficients_1d(f, interval01, degree)
    roots = cast(np.ndarray, move_from1m1(ncheb.chebroots(coeffs_f), interval01))

    if interval:
        roots_in_interval = roots[(roots >= interval.x0) & (roots <= interval.x1)]
        if len(roots_in_interval) == 0:
            return roots, None
        elif len(roots_in_interval) == 1:
            return roots, roots_in_interval[0]
        else:
            return roots, roots_in_interval
    else:
        return roots


def cheb_integrate_from_coeffs_1d(c: np.ndarray, interval: Interval) -> float:
    """integrate a function on an interval using the coefficients of its Chebyshev expansion

    Args:
        c: the Chebyshev coefficients for `fun`
        interval: the Interval

    Returns:
        the value of the integral over the interval
    """
    x0, x1 = interval.bounds()
    Mc = check_vector(c)
    k_even = slice(0, Mc, 2)
    k_vals = np.arange(0, Mc, 2)
    val_integral = np.sum(c[k_even] / (1.0 - k_vals * k_vals)) * (x1 - x0)
    return cast(float, val_integral)


def cheb_integrate_from_nodes_1d(
    vals_at_nodes: np.ndarray,
    weights: np.ndarray,
) -> float:
    """integrate a function given its values at the Chebyshev nodes

    Args:
        vals_at_nodes: the values of the function at these nodes
        weights: the Chebyshev nodes

    Returns:
        the value of the integral

    Notes:
        this is much less precise than `cheb_integrate_from_coeffs_1d`
    """
    Mv = check_vector(vals_at_nodes)
    Mw = check_vector(weights)
    if Mv != Mw:
        bs_error_abort(
            f"weights and vals_at_nodes must have the same length, not {Mw} and {Mv}"
        )
    return cast(float, weights @ vals_at_nodes)


def cheb_get_nodes_2d(rectangle: Rectangle, degree: int) -> TwoArrays:
    """get the Chebyshev nodes and weights on a rectangle

    Args:
        rectangle: the Rectangle
        degree: the degree of the highest Chebyshev polynomial in each dimension

    Returns:
        two $(\text{degree}^2, 2)$`-matrices of Chebyshev nodes and weights
        on the rectangle $[x0, x1]\times [y0, y1]$
    """
    nodes1d_x, weights1d_x = cheb_get_nodes_1d(rectangle.x_interval, degree)
    nodes1d_y, weights1d_y = cheb_get_nodes_1d(rectangle.y_interval, degree)
    nodes2d = bsgrid(nodes1d_x, nodes1d_y)
    weights2d = bsgrid(weights1d_x, weights1d_y)
    return nodes2d, weights2d[:, 0] * weights2d[:, 1]


def cheb_eval_fun_at_nodes_2d(
    fun: ArrayFunctionOfArray,
    nodes: np.ndarray | None = None,
    rectangle: Rectangle | None = None,
    degree: int | None = None,
) -> np.ndarray:
    """evaluate a function at the Chebyshev nodes on a rectangle $

    Args:
        fun: the function to evaluate on the rectangle
        nodes: the Chebyshev nodes on that rectangle, if precomputed
        rectangle: the Rectangle
        degree: the degree of the Chebyshev  expansion in each dimension

    Notes:
        `rectangle` and `degree` are required if `nodes` is not provided

    Returns:
        the values of the function at the Chebyshev nodes
    """
    if nodes is None:
        if degree is None or rectangle is None:
            bs_error_abort(
                "if nodes is not provided, then degree and rectangle must be"
            )
        degree = cast(int, degree)
        rectangle = cast(Rectangle, rectangle)
        nodes, _ = cheb_get_nodes_2d(rectangle, degree)
    vals_at_nodes = fun(nodes)
    return vals_at_nodes


def cheb_get_coefficients_2d(
    rectangle: Rectangle,
    degree: int,
    vals_at_nodes: np.ndarray | None = None,
    fun: ArrayFunctionOfArray | None = None,
) -> np.ndarray:
    """get the Chebyshev coefficients for `fun` on a rectangle,
    using an OLS fit on the values on the grid of nodes

    Args:
        rectangle: the Rectangle
        degree: the degree of the Chebyshev expansion in each dimension
        vals_at_nodes: the values on the grid, if precomputed
        fun: the function

    Notes:
        if `vals_at-nodes` is not provided then `fun` must be.

    Returns:
        the Chebyshev coefficients of the OLS Chebyshev fit, an `(M,M)` matrix
        the approximation is $f(x_1,x_2) = \\sum_{k,l} c_{kl} T_k(x_1)T_l(x_2)$
    """
    if vals_at_nodes is None:
        if fun is None:
            bs_error_abort("vals_at_nodes was not provided, so fun must be.")
        fun = cast(ArrayFunctionOfArray, fun)
        vals_at_nodes = cheb_eval_fun_at_nodes_2d(
            fun, rectangle=rectangle, degree=degree
        )
    # we need the nodes on $[-1, 1]$
    interval_1m1 = Interval(x0=-1.0, x1=1.0)
    nodes1m1, _ = cheb_get_nodes_1d(interval_1m1, degree)
    # first we fit fixing the node on the first dimension
    c = np.zeros((degree, degree))
    c_bar = np.zeros((degree, degree))
    i_beg = 0
    for i in range(degree):
        i_end = i_beg + degree
        vals_for_i = vals_at_nodes[i_beg:i_end]
        c_bar[i, :] = ncheb.chebfit(nodes1m1, vals_for_i, degree - 1)
        i_beg = i_end
    # then we fit to the values of c_bar
    for k in range(degree):
        c[:, k] = ncheb.chebfit(nodes1m1, c_bar[:, k], degree - 1)
    return c


def cheb_interp_2d(
    xy_vals: np.ndarray,
    rectangle: Rectangle,
    c: np.ndarray | None = None,
    fun: ArrayFunctionOfArray | None = None,
    degree: int | None = None,
    vals_at_nodes: np.ndarray | None = None,
) -> TwoArrays | tuple[float, np.ndarray]:
    """interpolate a function on a rectangle using Chebyshev polynomials

    Args:
        xy_vals: the values at which to interpolate, an `(n,2)` matrix or a 2-vector
        rectangle: the Rectangle
        c: the Chebyshev coefficients for `fun`, if already known; otherwise we compute them
        fun: the function to interpolate
        degree: the degree of the Chebyshev expansion
        vals_at_nodes: the values on the grid, if precomputed

    Notes:
        `degree` is required if `c` is not provided, as well as either `fun` or `vals_at_nodes`

    Returns:
        the `n`-vector of values of the interpolation at `xy_vals` and the Chebyshev coefficients `c`
    """
    if c is None:
        if degree is None:
            bs_error_abort("either c or degree must be provided")
        degree = cast(int, degree)
        c = cheb_get_coefficients_2d(
            rectangle, degree, vals_at_nodes=vals_at_nodes, fun=fun
        )
    # transform xy_vals to $[-1,1]\times [-1,1]$
    xy_vals1 = np.zeros_like(xy_vals)
    if xy_vals.ndim == 2:
        xy_vals1[:, 0] = move_to1m1(xy_vals[:, 0], rectangle.x_interval)
        xy_vals1[:, 1] = move_to1m1(xy_vals[:, 1], rectangle.y_interval)
        n_vals = xy_vals.shape[0]
        deg = c.shape[0]
        c2 = np.zeros((deg, n_vals))
        for k, c_k in enumerate(c):
            c2[k, :] = ncheb.chebval(xy_vals1[:, 1], c_k)
        f_vals = np.zeros(n_vals)
        for i in range(n_vals):
            f_vals[i] = ncheb.chebval(xy_vals1[i, 0], c2[:, i])
    else:
        xy_vals1[0] = move_to1m1(xy_vals[0], rectangle.x_interval)
        xy_vals1[1] = move_to1m1(xy_vals[1], rectangle.y_interval)
        deg = c.shape[0]
        c2 = np.zeros(deg)
        for k, c_k in enumerate(c):
            c2[k] = ncheb.chebval(xy_vals1[1], c_k)
        f_vals = ncheb.chebval(xy_vals1[0], c2)
    return f_vals, c


def cheb_integrate_from_coeffs_2d(c: np.ndarray, rectangle: Rectangle) -> float:
    """integrate a function on an interval using the coefficients of its Chebyshev expansion

    Args:
        c: the Chebyshev coefficients for `fun`
        rectangle: the Rectangle

    Returns:
        the value of the integral over the interval
    """
    x0, x1 = rectangle.x_interval.bounds()
    y0, y1 = rectangle.y_interval.bounds()
    M = check_square(c)
    k_even = slice(0, M, 2)
    k_vals = np.arange(0, M, 2)
    denom = 1.0 - k_vals * k_vals
    val_integral = cast(float, np.sum(c[k_even, k_even] / np.outer(denom, denom)))
    return cast(float, val_integral * (x1 - x0) * (y1 - y0))


def cheb_integrate_from_nodes_2d(
    vals_at_nodes: np.ndarray,
    weights: np.ndarray,
) -> float:
    """integrate a function given its values at the Chebyshev nodes

    Args:
        vals_at_nodes: the values of the function on the grid of 2d nodes
        weights: the Chebyshev weights in 2d

    Returns:
        the value of the integral

    Warning:
        this is much less precise than `cheb_integrate_from_coeffs_2d`
    """
    Mv = check_vector(vals_at_nodes)
    Mw = check_vector(weights)
    if Mv != Mw:
        bs_error_abort(
            f"weights and vals_at_nodes must have the same length, not {Mw} and {Mv}"
        )
    return cast(float, vals_at_nodes @ weights)


def cheb_integrate_from_nodes_4d(
    vals_at_nodes4d: np.ndarray, weights2d: np.ndarray
) -> float:
    """integrate a function on the square of a rectangle given its values at the 4d Chebyshev nodes

    Args:
        vals_at_nodes4d: the values of the function on the square of the grid of 2d nodes, an $(M^2, M^2)$ matrix
        weights2d: the Chebyshev weights on the rectangular grid, an $M^2$-vector

    Returns:
        the value of the integral

    Warning:
        it would be better to have a `cheb_integrate_from_coeffs_4d`
    """
    Mv2 = check_square(vals_at_nodes4d)
    Mw2 = check_vector(weights2d)
    if Mv2 != Mw2:
        bs_error_abort(
            "weights2d and vals_at_nodes4d should have the same number of rows, not"
            f" {Mv2} and {Mw2}"
        )
    return cast(float, weights2d @ (vals_at_nodes4d @ weights2d))
