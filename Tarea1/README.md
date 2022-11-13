# TAREA 1: Métodos de Monte Carlo

En esta tarea usamos números aleatorios (generados usando el módulo `secrets` de Python) para realizar una serie de cálculos, a saber:

1. Estimación de Pi (archivo `1_pi.py`)
2. Integración numérica
    - Selección de solución de la ecuación cúbica apropiada (archivo `2-1-cubicsols.py`)
    - Cálculo en si para densidades uniforme y no uniforme (archivo `2_integral.py`)

Los módulos requeridos son estándar en programación científica (`numpy`, `matplotlib`, etc). Lo más particular es el uso de paralelización en procesos para realizar cada una de las iteraciones, ya que de lo contrario lleva demasiado tiempo.
