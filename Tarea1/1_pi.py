#! /bin/python

'''
Title: Estimación de Pi mediante Monte Carlo
Author: Gonzalo Contreras Aso
'''

import secrets
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use("GTK3Agg")
plt.style.use('science')

SR = secrets.SystemRandom()

# Parámetros
Nspace = range(10,1000,1)
it = 200

# Funciones necesarias
def conteo(N):
    'Cuenta los puntos que caen dentro del círculo'
    N_int = 0 
    for n in range(N):
        x = SR.random()
        y = SR.random()
        z = SR.random()

        if (x-1/2)**2 + (y-1/2)**2 + (z-1/2)**2 <= 1/4:
            N_int += 1

    return N_int

def iteration(i):
    'Realiza el cálculo una vez para cada N'
    pi_est_it = []
    for N in Nspace:
        N_int = conteo(N)
        
        proportion = N_int/N 

        pi_est_it.append(proportion * 6)
        
    return pi_est_it

# Programa
pi_est_tot = []

## Paralelización
with ProcessPoolExecutor(max_workers=10) as executor:
    results = executor.map(iteration, range(it))

for result in results:
    pi_est_tot.append(np.array(result))

pi_est_tot = np.array(pi_est_tot)

## Promedio por cada iteración
pi_est = np.mean(pi_est_tot, axis=0)

## Varianza entre todas las iteraciones realizadas
pi_var = np.mean((pi_est_tot - pi_est)**2, axis=0)


# Figura
fig, ax = plt.subplots(3,1, sharex=True, figsize=(4,6))

ax[0].set_ylabel('Estimación')
ax[0].plot(Nspace, pi_est)
ax[0].plot(Nspace, [np.pi] * len(Nspace), linewidth=1.5, color='red', alpha=0.5, label='Real')
ax[0].legend()

ax[1].set_ylabel('True error')
ax[1].plot(Nspace, np.abs(np.array(pi_est) - np.array([np.pi] * len(Nspace))))

ax[2].set_ylabel('Variance')
ax[2].plot(Nspace, pi_var)
ax[2].plot(Nspace, 1/np.sqrt(np.array(Nspace)), linewidth=1.5, color='red', alpha=0.5, label='1/sqrt(N)')
ax[2].legend()


fig.tight_layout()
plt.savefig('estimacion_pi.png', facecolor="white", transparent=True)