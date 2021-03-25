"""
Created on Wed Mar 24 10:53:59 2021

@author: david.mejia
"""

import pandas as pd
from datetime import datetime
from Grarantias_Class import Garantia




def organiza_df(Fluct, Grup_Comp, VMDacc, precios):
    """Organiza los dataframes entregados, dejándolos aptos para las funciones de Garantias_Class.

    Todos los parámetros son dataframes
    """
    Fluct.set_index('Especie', inplace = True)
    Grup_Comp.set_index('Especie', inplace = True)
    VMDacc.set_index('Especie', inplace = True)
    precios.set_index('Nemotecnico', inplace = True)

    temp = []
    for nemo in precios.index:
            
        base = Fluct.index.get_loc(nemo)
        temp.append(Fluct.iloc[base,0])


    precios["Flt"] = temp
    precios["Alza"] = round(precios["UltimoPrecio"] * (1 + precios["Flt"]*0.75),0)
    precios["Baja"] = round(precios["UltimoPrecio"] * (1 - precios["Flt"]*0.75),0)

    return Fluct, Grup_Comp, VMDacc, precios


def main(Fluct, Deltas, Grup_Comp, VMDacc, operaciones, precios, fecha_M):
    """
    Función principal
    """

    Fluct, Grup_Comp, VMDacc, precios = organiza_df(Fluct, Grup_Comp, VMDacc, precios)
    
    neutral = Garantia(operaciones, precios)
    bullish = Garantia(operaciones, precios)
    bearish = Garantia(operaciones, precios)

    escenario_neutral = neutral.escenario(0, fecha_M, Grup_Comp, VMDacc, Fluct)
    ge_n = neutral.calculo(escenario_neutral)

    escenario_alza = bullish.escenario(2, fecha_M, Grup_Comp, VMDacc, Fluct)
    ge_a = bullish.calculo(escenario_alza)

    escenario_baja = bearish.escenario(3, fecha_M, Grup_Comp, VMDacc, Fluct)
    ge_b = bearish.calculo(escenario_baja)

    return print(f'La garantía total es {ge_n}, la garantía por LMC es {max(ge_a, ge_b)}')

if __name__ == '__main__':
    Fluct = pd.read_excel("Fluct.xlsx")
    Deltas = pd.read_excel("Deltas.xlsx")
    Grup_Comp = pd.read_excel("VMD.xlsx").loc[:,['Especie','Grupo']]
    VMDacc = pd.read_excel("VMD.xlsx").loc[:,['Especie','VMD']]
    operaciones = pd.read_excel("Operaciones.xlsx")
    precios = pd.read_excel("precios.xls")
    fecha_M = max(operaciones["FechaCum"])

    main(Fluct, Deltas, Grup_Comp, VMDacc, operaciones, precios, fecha_M)



