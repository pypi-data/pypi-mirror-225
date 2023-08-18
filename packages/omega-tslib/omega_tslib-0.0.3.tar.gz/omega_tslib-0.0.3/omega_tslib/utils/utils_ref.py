import pandas as pd
import numpy as np


def ref_min():

    # 1/hora, 1/dia, 1/semana, 1/mes, 1/ano
    lista_frequencias = [1/60, 1/(60*24), 1/(60*24*7), 1/(60*24*30), 1/(60*24*365)]
    lista_frequencias = [float(f'{x:.5f}') for x in lista_frequencias]

    return lista_frequencias


def ref_15_min():

    # 1/hora, 1/dia, 1/semana, 1/mes, 1/ano
    lista_frequencias = [1/4, 1/(4*24), 1/(4*24*7), 1/(4*24*30), 1/(4*24*365)]
    lista_frequencias = [float(f'{x:.5f}') for x in lista_frequencias]

    return lista_frequencias


def ref_hora():

    # 1/dia, 1/semana, 1/mes, 1/ano
    lista_frequencias = [1/24, 1/(24*7), 1/(24*30), 1/(24*365)]
    lista_frequencias = [float(f'{x:.5f}') for x in lista_frequencias]

    return lista_frequencias


def ref_dia():

    # 1/semana, 1/mes, 1/ano
    lista_frequencias = [1/7, 1/30, 1/365]
    lista_frequencias = [float(f'{x:.5f}') for x in lista_frequencias]

    return lista_frequencias


def ref_mes():

    # 1/ano
    lista_frequencias = [1/12]
    lista_frequencias = [float(f'{x:.5f}') for x in lista_frequencias]

    return lista_frequencias

