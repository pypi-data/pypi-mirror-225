"""
Cntains various `scikit-learn` utility programs.
"""

from itertools import cycle
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Lasso, lasso_path
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def skl_npreg_lasso(
    y: np.ndarray, X: np.ndarray, alpha: float, degree: int = 4
) -> np.ndarray:
    """
    Lasso nonparametric regression of `y` over polynomials of `X`

    Args:
        y:  shape `(nobs)`
        X: shape  `(nobs, nfeatures)`
        alpha:  Lasso penalty parameter
        degree: highest total degree

    Returns:
        the `(nobs)` array `E(y\\vert X)` over the sample
    """

    # first scale the X variables
    stdsc = StandardScaler()
    sfit = stdsc.fit(X)
    X_scaled = sfit.transform(X)
    pf = PolynomialFeatures(degree)
    # Create the features and fit
    X_poly = pf.fit_transform(X_scaled)
    # now run Lasso
    reg = Lasso(alpha=alpha).fit(X_poly, y)
    expy_X = reg.predict(X_poly)
    return cast(np.ndarray, expy_X)


def plot_lasso_path(y: np.ndarray, X: np.ndarray, eps: float = 1e-3) -> None:
    """
    plot Lasso coefficient paths

    Args:
        y:  shape `(nobs)`
        X: shape  `(nobs, nfeatures)`
        eps: length of path

    Returns:
        plots the paths
    """
    # Compute paths
    print("Computing regularization path using the lasso...")
    alphas_lasso, coefs_lasso, _ = lasso_path(X, y, eps)

    plt.clf()
    # Display results
    plt.figure(1)
    colors = cycle(["b", "r", "g", "c", "k"])
    neg_log_alphas_lasso = -np.log10(alphas_lasso)
    for coef_l, c in zip(coefs_lasso, colors, strict=True):
        plt.plot(neg_log_alphas_lasso, coef_l, c=c)

    plt.xlabel("-Log(alpha)")
    plt.ylabel("coefficients")
    plt.title("Lasso Paths")
    plt.axis("tight")

    plt.show()

    return
