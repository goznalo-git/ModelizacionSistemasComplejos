#! /bin/python

'''
Title: Integración mediante Monte Carlo
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
it = 100

# Funciones necesarias
f = lambda x: np.cos(np.pi * x / 2)
rho_no_unif = lambda x: (3/2) * (1 - x ** 2)
xcubic = lambda u: -2 * np.sin(1/3 * np.arcsin(u))

def conteo(N, rho):
    'Conteo de puntos a incluir en la suma final, para cada método "rho"'
    N_int = 0 
    for n in range(N):
        x = SR.random()

        if rho == 'unif-conteo':
            y = SR.random()

            if y < f(x):
                N_int += 1

        elif rho == 'unif-MC':
            N_int += f(x)

        elif rho == 'no-unif-inv':
            x = xcubic(x)
            N_int += f(x) / rho_no_unif(x)

    return N_int

def iteration(i):
    'Una iteración del cálculo para cada valor de N, para cada método'
    int_est_unif_c_it = []
    int_est_unif_MC_it = []
    int_est_nunif_i_it = []
    for N in Nspace:
        N_int = conteo(N, rho='unif-conteo')
        proportion = N_int/N
        int_est_unif_c_it.append(proportion)

        N_int = conteo(N, rho='unif-MC')
        proportion = N_int/N
        int_est_unif_MC_it.append(proportion)

        N_int = conteo(N, rho='no-unif-inv')
        proportion = N_int/N
        int_est_nunif_i_it.append(proportion)

    return int_est_unif_c_it, int_est_unif_MC_it, int_est_nunif_i_it


# Programa
int_est_unif_c_j = []
int_est_unif_MC_j = []
int_est_nunif_i_j = []

## Paralelización
with ProcessPoolExecutor(max_workers=10) as executor:
    results = executor.map(iteration, range(it))

for result in results:
    int_est_unif_c_j.append(np.array(result[0]))
    int_est_unif_MC_j.append(np.array(result[1]))
    int_est_nunif_i_j.append(np.array(result[2]))

int_est_unif_c_j = np.array(int_est_unif_c_j)
int_est_unif_MC_j = np.array(int_est_unif_MC_j)
int_est_nunif_i_j = np.array(int_est_nunif_i_j)


## Extracción de resultados
int_est_unif_c = np.mean(int_est_unif_c_j, axis=0)
int_est_unif_MC = np.mean(int_est_unif_MC_j, axis=0)
int_est_nunif_i = np.mean(int_est_nunif_i_j, axis=0)

## Varianza
int_var_unif_c = np.mean(int_est_unif_c_j**2, axis=0) - np.mean(int_est_unif_c_j, axis=0)**2
int_var_unif_MC = np.mean(int_est_unif_MC_j**2, axis=0) - np.mean(int_est_unif_MC_j, axis=0)**2
int_var_nunif_i = np.mean(int_est_nunif_i_j**2, axis=0) - np.mean(int_est_nunif_i_j, axis=0)**2


# Figura
fig, ax = plt.subplots(3,3, sharex=True, figsize=(8,6))

ax[0,0].set_ylabel('Estimación')
ax[1,0].set_ylabel('Error')
ax[2,0].set_ylabel('Varianza')

fig.supxlabel('N')

ax[0,0].set_title('Uniforme, conteo')
ax[0,0].plot(Nspace, int_est_unif_c)
ax[0,0].plot(Nspace, [2/np.pi] * len(Nspace), linewidth=1.5, color='red', alpha=0.5, label='Real')
ax[0,0].legend()

ax[1,0].plot(Nspace, np.abs(np.array(int_est_unif_c) - np.array([2/np.pi] * len(Nspace))))

ax[2,0].plot(Nspace, int_var_unif_c)

ax[0,1].set_title('Uniforme, Monte Carlo')
ax[0,1].plot(Nspace, int_est_unif_MC)
ax[0,1].plot(Nspace, [2/np.pi] * len(Nspace), linewidth=1.5, color='red', alpha=0.5, label='Real')
ax[0,1].legend()

ax[1,1].plot(Nspace, np.abs(np.array(int_est_unif_MC) - np.array([2/np.pi] * len(Nspace))))

ax[2,1].plot(Nspace, int_var_unif_MC)


ax[0,2].set_title('No uniforme, inversa')
ax[0,2].plot(Nspace, int_est_nunif_i)
ax[0,2].plot(Nspace, [2/np.pi] * len(Nspace), linewidth=1.5, color='red', alpha=0.5, label='Real')
ax[0,2].legend()

ax[1,2].plot(Nspace, np.abs(np.array(int_est_nunif_i) - np.array([2/np.pi] * len(Nspace))))

ax[2,2].plot(Nspace, int_var_nunif_i)

fig.tight_layout()
plt.savefig('estimacion_integral.png', transparent=False)