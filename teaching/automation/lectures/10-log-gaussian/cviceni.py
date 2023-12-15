# %%
from ariane.lib.gaussian_process_regression.implementations.sklearn \
    import ScikitLearnGaussianProcessRegressor, kernels
from ariane.lib.gaussian_process_regression import LogGaussianProcessRegressor
import numpy as np
from ariane.lib.utils.math import normalizer
from ariane.lib.utils import math
+

# %%

level_backgr_diffs_rel_max = 0.5
level_backgr_diffs_abs_min = 15
level_backgr_decile_max = 6
thresh_intens_fact = 0.5
num_kernel_optim_restarts = 100
kernel_bounds_variance = [1e-3, 1e2]
kernel_bounds_length_scales = [1e-3, 1e2]
num_kernel_optims_min = 25
num_kernel_optims_max = 75
kernel_optims_stop_num_last = 9
kernel_optims_stop_eps = 0.025
length_scales_min_fact = 1e-3
length_scales_max_fact = 1.

random_state = np.random.RandomState()

limits = np.array([[0, 1], [0, 1]])
kernel = kernels.ConstantKernel(1., kernel_bounds_variance) * \
            kernels.RBF(len(limits) * [1.], kernel_bounds_length_scales)
gpr_impl = ScikitLearnGaussianProcessRegressor(
            kernel=kernel, optimizer="fmin_l_bfgs_b",
            n_restarts_optimizer=num_kernel_optim_restarts,
            normalize_y=False, copy_X_train=True, random_state=random_state)
# %%
lgpr = LogGaussianProcessRegressor(gpr_impl)
# %%
limits = [[1., 3.], [1, 5]]
x1_normalizer = normalizer(*limits[0])
x2_normalizer = normalizer(*limits[1])


def f(x):
    x1 = x1_normalizer(x[0])
    x2 = x2_normalizer(x[1])

    ampl_min = 400
    ampl_max = 602
    ampl = ampl_max - (ampl_max - ampl_min)*x1

    sigma_min = 0.07
    sigma_max = 0.1
    sigma = sigma_max - (sigma_max - sigma_min)*x1

    return ampl * np.exp(-1/(2*sigma**2) * (x2 - (0.02*np.sin(3*2*np.pi*x1) + 0.6))**2)
# %%

import matplotlib.pyplot as plt

x1s = np.linspace(*limits[0], num=10)
x2s = np.linspace(*limits[1], num=10)

#x_train_init = [x1s, x2s] #math.cartesian_product(x1s, x2s)
x_train_init = np.array(np.meshgrid(x1s, x2s)).T.reshape(-1,2)

y_train_init = f(x_train_init.reshape(2,-1))

# %%
from ariane.lib.plotting import contour_gpr_2d

# %%
lgpr.fit(x_train_init, y_train_init, np.sqrt(y_train_init))
# %%
x_train_init
# %%
fig, (ax_pred, ax_uncert) = contour_gpr_2d(lgpr, x1_plt=x1s, x2_plt=x2s)

# %%
plt.imshow(y_train_init.reshape(100,100), cmap='hot', interpolation='nearest')
plt.show()
# %%
y_train_init
# %%
