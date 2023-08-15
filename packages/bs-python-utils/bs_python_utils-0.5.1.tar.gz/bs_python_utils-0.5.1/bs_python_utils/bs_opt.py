""" interface to scipy.optimize """
from dataclasses import dataclass
from math import sqrt
from typing import Any, Callable, Iterable, Optional, Union, cast

import numpy as np
import scipy.linalg as spla
import scipy.optimize as spopt

from bs_python_utils.bsnputils import TwoArrays, check_vector, npmaxabs
from bs_python_utils.bsutils import bs_error_abort, print_stars
from bs_python_utils.Timer import timeit

ScalarFunctionAndGradient = Callable[
    [np.ndarray, Iterable, Optional[bool]], Union[float, tuple[float, np.ndarray]]
]
"""Type of f(v, args, gr) that returns a scalar value and also a gradient if gr is True"""


ProximalFunction = Callable[[np.ndarray, float, Iterable], np.ndarray]
"""Type of h(x, t, pars) that returns a scalar value"""


@dataclass
class OptimizeParams:
    """
    used for optimization;
    combines values, bounds and initial values for a parameter vector
    """

    params_values: np.ndarray | None
    params_bounds: list[tuple] | None
    params_init: np.ndarray | None


def print_optimization_results(
    resus: spopt.OptimizeResult, title: str = "Minimizing"
) -> None:
    """
    print results from unconstrained optimization

    Args:
        resus: results from optimization
        title: a title

    Returns:
        just prints
    """
    print_stars(title)
    print(resus.message)
    if resus.success:
        print(f"Successful! in {resus.nit} iterations")
        print(f" evaluated {resus.nfev} functions functions and {resus.njev} gradients")
        print("\nMinimizer and grad_f:")
        print(np.column_stack((resus.x, resus.jac)))
        print(f"Minimized value is {resus.fun}")
    else:
        print_stars("Minimization failed!")
    return


def print_constrained_optimization_results(
    resus: spopt.OptimizeResult,
    title: str = "Minimizing",
    print_constr: bool = False,
    print_multipliers: bool = False,
) -> None:
    """
    print results from constrained optimization

       Args:
        resus: results from optimization
        str title: a title
        print_constr: if `True`, print the values of the constraints
        print_multipliers: if `True`, print the values of the multipliers

    Returns:
        just prints
    """
    print_stars(title)
    print(resus.message)
    if resus.success:
        print(f"Successful! in {resus.nit} iterations")
        print(f" evaluated {resus.nfev} functions and {resus.njev} gradients")
        print(f"Minimized value is {resus.fun}")
        print(f"The Lagrangian norm is {resus.optimality}")
        print(f"The largest constraint violation is {resus.constr_violation}")
        if print_multipliers:
            print(f"The multipliers are {resus.v}")
        if print_constr:
            print(f"The values of the constraints are {resus.constr}")
    else:
        print_stars("Constrained minimization failed!")
    return


def armijo_alpha(
    f: Callable,
    x: np.ndarray,
    d: np.ndarray,
    args: Iterable,
    alpha_init: float = 1.0,
    beta: float = 0.5,
    max_iter: int = 100,
    tol: float = 0.0,
) -> float:
    """Given a function `f` we are minimizing, computes the step size `alpha`
    to take in the direction `d` using the Armijo rule

    Args:
        f: the function
        x: the current point
        d: the direction we are taking
        args: other arguments passed to `f`
        alpha_init: the initial step size
        beta: the step size reduction factor
        max_iter: the maximum number of iterations
        tol: a tolerance

    Returns:
        the step size alpha
    """
    f0 = f(x, args)
    alpha = alpha_init
    for _ in range(max_iter):
        x1 = x + alpha * d
        f1 = f(x1, args)
        if f1 < f0 + tol:
            return alpha
        alpha *= beta
    else:
        bs_error_abort("Too many iterations")
    return alpha


def barzilai_borwein_alpha(
    grad_f: Callable, x: np.ndarray, args: Iterable
) -> tuple[float, np.ndarray]:
    """Given a function `f` we are minimizing, computes the step size `alpha`
    to take in the opposite direction of the gradient using the Barzilai-Borwein rule

    Args:
        grad_f: the gradient of the function
        x: the current point
        args: other arguments passed to `f`

    Returns:
        the step size `alpha` and the gradient `g` at the point `x`
    """
    g = grad_f(x, args)
    alpha = 1.0 / spla.norm(g)
    x_hat = x - alpha * g
    g_hat = grad_f(x_hat, args)
    norm_dg = spla.norm(g - g_hat)
    norm_dg2 = norm_dg * norm_dg
    alpha = np.abs(np.dot(x - x_hat, g - g_hat)) / norm_dg2
    return alpha, g


def check_gradient_scalar_function(
    fg: ScalarFunctionAndGradient,
    p: np.ndarray,
    args: Iterable,
    mode: str = "central",
    EPS: float = 1e-6,
) -> TwoArrays:
    """Checks the gradient of a scalar function

    Args:
        fg: should return the scalar value, and the gradient if its `gr` argument is `True`
        p: where we are checking the gradient
        args: other arguments passed to `fg`
        mode: "central" or "forward" derivatives
        EPS: the step for forward or central derivatives

    Returns:
        the analytic and numeric gradients
    """
    f0, f_grad = fg(p, args, gr=True)  # type: ignore
    f0 = cast(float, f0)

    print_stars("checking the gradient: analytic, numeric")

    g = np.zeros_like(p)
    if mode == "central":
        for i, x in enumerate(p):
            p1 = p.copy()
            p1[i] = x + EPS
            f_plus = cast(float, fg(p1, args, gr=False))  # type: ignore
            p1[i] -= 2.0 * EPS
            f_minus = cast(float, fg(p1, args, gr=False))  # type: ignore
            g[i] = (f_plus - f_minus) / (2.0 * EPS)
            print(f"{i}: {f_grad[i]}, {g[i]}")
    elif mode == "forward":
        for i, x in enumerate(p):
            p1 = p.copy()
            p1[i] = x + EPS
            f_plus = cast(float, fg(p1, args, gr=False))  # type: ignore
            g[i] = (f_plus - f0) / EPS
            print(f"{i}: {f_grad[i]}, {g[i]}")
    else:
        bs_error_abort("mode must be 'central' or 'forward'")

    return f_grad, g


@timeit
def acc_grad_descent(
    grad_f: Callable,
    x_init: np.ndarray,
    other_params: Iterable,
    prox_h: ProximalFunction | None = None,
    print_result: bool = False,
    verbose: bool = False,
    tol: float = 1e-9,
    alpha: float = 1.01,
    beta: float = 0.5,
    maxiter: int = 10000,
) -> tuple[np.ndarray, int]:
    """
    minimizes `(f+h)` by Accelerated Gradient Descent where `f` is smooth and convex  and `h` is convex.

    By default `h` is zero.
    The convergence criterion is that the largest component of the absolute value of the gradient must be smaller than `tol`.


    Args:
        grad_f: grad_f of `f`; should return an `(n)` array from an `(n)` array \
        and the `other_ params` object
        x_init: initial guess, shape `(n)`
        prox_h: proximal projector of `h`, if any
        other_params: an iterable with additional parameters
        verbose: if `True`, print remaining gradient error every 10 iterations
        tol: convergence criterion on grad_f
        alpha: ceiling on step multiplier
        beta: floor on step multiplier
        maxiter: max number of iterations

    Returns: 
        the candidate solution, and a convergence code (0 if successful, 1 if not)
    """

    # no proximal projection if no h
    local_prox_h: ProximalFunction = prox_h if prox_h else lambda x, t, p: x

    x = x_init.copy()
    y = x_init.copy()

    #  for stepsize we use Barzilai-Borwein
    t, g = barzilai_borwein_alpha(grad_f, y, other_params)

    grad_err_init = npmaxabs(g)

    if verbose:
        print(f"agd: grad_err_init={grad_err_init}")

    n_iter = 0
    theta = 1.0

    while n_iter < maxiter:
        grad_err = npmaxabs(g)
        if grad_err < tol:
            break
        xi = x
        yi = y
        x = y - t * g
        x = local_prox_h(x, t, other_params)

        theta = 2.0 / (1.0 + sqrt(1.0 + 4.0 / theta / theta))

        if np.dot(y - x, x - xi) > 0:  # wrong direction, we restart
            x = xi
            y = x
            theta = 1.0
        else:
            y = x + (1.0 - theta) * (x - xi)

        gi = g
        g = grad_f(y, other_params)
        ndy = spla.norm(y - yi)
        t_hat = 0.5 * ndy * ndy / abs(np.dot(y - yi, gi - g))
        t = min(alpha * t, max(beta * t, t_hat))

        n_iter += 1

        if verbose and n_iter % 10 == 0:
            print(f" AGD with grad_err = {grad_err} after {n_iter} iterations")

    x_conv = y

    ret_code = 0 if grad_err < tol else 1

    if verbose or print_result:
        if ret_code == 0:
            print_stars(
                f" AGD converged with grad_err = {grad_err} after {n_iter} iterations"
            )
        else:
            print_stars(
                f" Problem in AGD: grad_err = {grad_err} after {n_iter} iterations"
            )

    return x_conv, ret_code


def _fix_some(
    obj: Callable, grad_obj: Callable, fixed_vars: list[int], fixed_vals: np.ndarray
) -> tuple[Callable, Callable]:
    """
    Takes in a function and its gradient, fixes the variables
    whose indices are `fixed_vars` to the values in `fixed_vals`,
    and returns the modified function and its gradient

    Args:
        obj: the original function
        grad_obj: its gradient function
        fixed_vars: a list if the indices of variables whose values are fixed
        fixed_vals: their fixed values

    Returns:
        the modified function and its modified gradient function
    """

    def fixed_obj(t, other_args):
        t_full = list(t)
        for i, i_coef in enumerate(fixed_vars):
            t_full.insert(i_coef, fixed_vals[i])
        arr_full = np.array(t_full)
        return obj(arr_full, other_args)

    def fixed_grad_obj(t, other_args):
        t_full = list(t)
        for i, i_coef in enumerate(fixed_vars):
            t_full.insert(i_coef, fixed_vals[i])
        arr_full = np.array(t_full)
        grad_full = grad_obj(arr_full, other_args)
        return np.delete(grad_full, fixed_vars)

    return fixed_obj, fixed_grad_obj


@timeit
def minimize_some_fixed(
    obj: Callable,
    grad_obj: Callable,
    x_init: np.ndarray,
    args: Iterable,
    fixed_vars: list[int] | None,
    fixed_vals: np.ndarray | None,
    options: dict | None = None,
    bounds: list[tuple[float, float]] | None = None,
) -> Any:
    """
    minimize a function with some variables fixed, using L-BFGS-B

    Args:
        obj: the original function
        grad_obj: its gradient function
        fixed_vars: a list if the indices of variables whose values are fixed
        fixed_vals: their fixed values
        x_init: the initial values of all variables (those on fixed variables are not used)
        args: other parameters
        options: any options passed on to `scipy.optimize.minimize`
        bounds: the bounds on all variables (those on fixed variables are not used)

    Returns:
        the result of optimization, on all variables
    """
    if fixed_vars is None:
        resopt = spopt.minimize(
            obj,
            x_init,
            method="L-BFGS-B",
            args=args,
            options=options,
            jac=grad_obj,
            bounds=bounds,
        )
    else:
        fixed_vars = cast(list, fixed_vars)
        n_fixed = check_vector(fixed_vals)
        fixed_vals = cast(np.ndarray, fixed_vals)
        if len(fixed_vars) != n_fixed:
            bs_error_abort(
                f"fixed_vars has {len(fixed_vars)} indices but fixed_vals has"
                f" {fixed_vals.size} elements."
            )
        fixed_obj, fixed_grad_obj = _fix_some(obj, grad_obj, fixed_vars, fixed_vals)

        # drop fixed variables and the corresponding bounds
        n = len(x_init)
        not_fixed = np.ones(n, dtype=bool)
        not_fixed[fixed_vars] = False
        t_init = x_init[not_fixed]
        t_bounds = (
            None if bounds is None else [bounds[i] for i in range(n) if not_fixed[i]]
        )

        resopt = spopt.minimize(
            fixed_obj,
            t_init,
            method="L-BFGS-B",
            args=args,
            options=options,
            jac=fixed_grad_obj,
            bounds=t_bounds,
        )

        # now re-fill the values of the variables
        t = resopt.x
        t_full = list(t)
        for i, i_coef in enumerate(fixed_vars):
            t_full.insert(i_coef, fixed_vals[i])
        resopt.x = t_full

        # and re-fill the values of the gradients
        g = grad_obj(np.array(t_full), args)
        resopt.jac = g

    return resopt


@timeit
def minimize_free(
    obj: Callable,
    grad_obj: Callable,
    x_init: np.ndarray,
    args: Iterable,
    options: dict | None = None,
    bounds: list[tuple[float, float]] | None = None,
) -> Any:
    """
    minimize a function on all of its variables, using BFGS or L-BFGS-B

    Args:
        obj: the original function
        grad_obj: its gradient function
        x_init: the initial values of all variables
        args: other parameters
        options: any options passed on to `scipy.optimize.minimize`
        bounds: the bounds on all variables, if any

    Returns:
        the result of optimization, on all variables
    """
    if bounds is None:
        resopt = spopt.minimize(
            obj,
            x_init,
            method="BFGS",
            args=args,
            options=options,
            jac=grad_obj,
        )
    else:
        resopt = spopt.minimize(
            obj,
            x_init,
            method="L-BFGS-B",
            args=args,
            options=options,
            jac=grad_obj,
            bounds=bounds,
        )

    return resopt


def dfp_update(
    hess_inv: np.ndarray, gradient_diff: np.ndarray, x_diff: np.ndarray
) -> np.ndarray:
    """runs a DFP update for the inverse Hessian

    Args:
        hess_inv: the current inverse Hessian
        gradient_diff: the update in the gradient
        x_diff: the update in x

    Returns:
        the updated inverse Hessian
    """
    xdt = x_diff.T
    xxp = x_diff @ xdt
    xpg = xdt @ gradient_diff
    hdg = hess_inv @ gradient_diff
    dgp_hdg = gradient_diff.T @ hdg
    hess_inv_new = hess_inv + xxp / xpg - (hdg @ hdg.T) / dgp_hdg
    return cast(np.ndarray, hess_inv_new)


def bfgs_update(
    hess_inv: np.ndarray, gradient_diff: np.ndarray, x_diff: np.ndarray
) -> np.ndarray:
    """runs a DFP update for the inverse Hessian

    Args:
        hess_inv: the current inverse Hessian
        gradient_diff: the update in the gradient
        x_diff: the update in x

    Returns:
        the updated inverse Hessian
    """
    xdt = x_diff.T
    xpg = xdt @ gradient_diff
    hdg = hess_inv @ gradient_diff
    dgp_hdg = gradient_diff.T @ hdg
    u = x_diff / xpg - hdg / dgp_hdg
    hess_inv_new = dfp_update(hess_inv, gradient_diff, x_diff) + dgp_hdg * (u @ u.T)
    return cast(np.ndarray, hess_inv_new)
