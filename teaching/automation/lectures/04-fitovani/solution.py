# %%

# !python -m pip install iminuit

import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from iminuit.cost import LeastSquares

# Funkce pro Gaussovu křivku
def gauss(x, A, mu, sigma):
    return A * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

np.random.seed(42)  # Pro opakovatelnost výsledků

angles = np.linspace(-10, 10, 100)
true_sigma = 1.5  # Výsledek

params = [ (100, -3),  # A, úhel
          (150, 0),
          (80, 3)  ]

# %%

data = []
for A, mu in params:
    intensity = gauss(angles, A, mu, true_sigma) + np.random.normal(0, 5, angles.size)
    data.append(intensity)

# Vizualizace generovaných dat
for intensity, (A, mu) in zip(data, params):
    plt.plot(angles, intensity, 'o', label=f'A={A}, mu={mu}')

plt.xlabel('Úhel (°)')
plt.ylabel('Intenzita')
plt.legend()
plt.show()

# %%

fit_intensities_1 = gauss(angles, m.values['A1'], m.values['mu1'], m.values['sigma'])
fit_intensities_2 = gauss(angles, m.values['A2'], m.values['mu2'], m.values['sigma'])
fit_intensities_3 = gauss(angles, m.values['A3'], m.values['mu3'], m.values['sigma'])

plt.plot(angles, data[0], 'o', label="Data 1")
plt.plot(angles, data[1], 'o', label="Data 2")
plt.plot(angles, data[2], 'o', label="Data 3")
plt.plot(angles, fit_intensities_1, '-', label="Fit 1")
plt.plot(angles, fit_intensities_2, '-', label="Fit 2")
plt.plot(angles, fit_intensities_3, '-', label="Fit 3")
plt.xlabel('Úhel (°)')
plt.ylabel('Intenzita')
plt.legend()
plt.show()

# %%

