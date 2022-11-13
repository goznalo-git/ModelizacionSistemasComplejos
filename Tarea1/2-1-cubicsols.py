#! /bin/python

'''
Title: Comparación entre las tres raíces de la ec. cúbica
Author: Gonzalo Contreras Aso
'''

import secrets
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("GTK3Agg")
plt.style.use('science')


SR = secrets.SystemRandom()
ur = [SR.random() for i in range(100000)]

xcubic = lambda u, k: -2 * np.sin(1/3 * np.arcsin(u) - 2*np.pi*k/3)

fig, ax = plt.subplots(1,3, figsize=(8,2))

for i, axis in enumerate(ax):
    xr = [xcubic(u,i) for u in ur]
    
    _ = axis.hist(xr, 100, density=True, facecolor='royalblue', alpha=0.75)
    
    xrmin = min(xr)
    xrmax = max(xr)
    
    axis.plot(np.linspace(xrmin,xrmax,100), 3/2*(1-np.linspace(xrmin,xrmax,100)**2), color='r', alpha=0.8)
    
ax[0].set_title('a)')
ax[1].set_title('b)')
ax[2].set_title('c)')

fig.tight_layout(pad=0.5)
plt.savefig('comparacion_cubic.png', transparent=False)