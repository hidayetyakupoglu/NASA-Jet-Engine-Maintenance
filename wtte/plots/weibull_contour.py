from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from six.moves import xrange
from wtte import weibull


def weibull_contour(Y, U, is_discrete, true_alpha, true_beta,
                    logx=True, samples=200, lines=True):
    xlist = np.linspace(true_alpha / np.e, true_alpha * np.e, samples)
    ylist = np.linspace(true_beta / np.e, true_beta * np.e, samples)
    x_grid, y_grid = np.meshgrid(xlist, ylist)
    loglik = x_grid * 0
    if is_discrete:
        fun = weibull.discrete_loglik
    else:
        fun = weibull.continuous_loglik
    for i in xrange(len(Y)):
        loglik = loglik + fun(Y[i], x_grid, y_grid, U[i])
    z_grid = loglik / len(Y)
    plt.figure()
    if logx:
        x_grid = np.log(x_grid)
        true_alpha = np.log(true_alpha)
        xlab = r'$\log(\alpha)$'
    else:
        xlab = r'$\alpha$'
    cp = plt.contourf(x_grid, y_grid, z_grid, 100, cmap='jet')
    plt.colorbar(cp)
    if lines:
        plt.axvline(true_alpha, linestyle='dashed', c='black')
        plt.axhline(true_beta, linestyle='dashed', c='black')
    plt.xlabel(xlab)
    plt.ylabel(r'$\beta$')
