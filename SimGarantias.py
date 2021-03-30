# -*- coding: utf-8 -*-
"""
Created on Tue Mar  30 17:35:24 2021

@author: david.mejia
"""

import pandas as pd
from datetime import datetime
import dateutil.relativedelta
import plotly.express as px
from time import time
from Grarantias_Class import Garantia


t0 = time()

def organiza_df(Fluct, Grup_Comp, VMDacc, operaciones_h):
    
    Fluct.set_index('Especie', inplace = True)
    Grup_Comp.set_index('Especie', inplace = True)
    VMDacc.set_index('Especie', inplace = True)
    todas_las_fechas = list(set(operaciones_h["FechaCum"]))
    todas_las_fechas = sorted(todas_las_fechas)

    return Fluct, Grup_Comp, VMDacc, todas_las_fechas
    


def main(Fluct, Deltas, Grup_Comp, VMDacc, operaciones_h, precios_h):
     
    Fluct, Grup_Comp, VMDacc, todas_las_fechas = organiza_df(Fluct, Grup_Comp, VMDacc, operaciones_h)


    Almacena_GE = []
    Almacena_LMC = []
    Almacena_date = []

    for i in range(0,len(todas_las_fechas)-1): 
        
        fecha_1 = todas_las_fechas[i]
        fecha_2 = todas_las_fechas[i+1]
        
        parte1 = operaciones_h[operaciones_h["FechaCum"] == fecha_1]
        parte2 = operaciones_h[operaciones_h["FechaCum"] == fecha_2]
        
        operaciones  = pd.concat([parte1, parte2], ignore_index = True)
                
        precios = precios_h[precios_h["Fecha"] == fecha_2]
        precios = pd.concat([precios], ignore_index = True)
        
        precios = precios.drop(['Fecha'], axis = 1)
        
        indexs = ["UltimoPrecio"]
        
        precios["Nemotecnico"] = indexs
        precios.set_index("Nemotecnico", inplace = True)
        
        precios = precios.T
        temp = []
        for nemo in precios.index:
            
            base = Fluct.index.get_loc(nemo)
            temp.append(Fluct.iloc[base,0])


        precios["Flt"] = temp
        precios["Alza"] = round(precios["UltimoPrecio"] * (1 + precios["Flt"]*0.75),0)
        precios["Baja"] = round(precios["UltimoPrecio"] * (1 - precios["Flt"]*0.75),0)
        
        neutral = Garantia(operaciones, precios)
        bullish = Garantia(operaciones, precios)
        bearish = Garantia(operaciones, precios)

        escenario_neutral = neutral.escenario(0, fecha_2, Grup_Comp, VMDacc, Fluct)
        ge_n = neutral.calculo(escenario_neutral)

        escenario_alza = bullish.escenario(2, fecha_2, Grup_Comp, VMDacc, Fluct)
        ge_a = bullish.calculo(escenario_alza)

        escenario_baja = bearish.escenario(3, fecha_2, Grup_Comp, VMDacc, Fluct)
        ge_b = bearish.calculo(escenario_baja)

        Almacena_date.append(fecha_2)
        Almacena_GE.append(ge_n)
        Almacena_LMC.append(max(ge_a, ge_b))

    return Almacena_date, Almacena_GE, Almacena_LMC

if __name__ == '__main__':

    Fluct = pd.read_excel("Fluct.xlsx")
    Deltas = pd.read_excel("Deltas.xlsx")
    Grup_Comp = pd.read_excel("VMD.xlsx").loc[:,['Especie','Grupo']]
    VMDacc = pd.read_excel("VMD.xlsx").loc[:,['Especie','VMD']]
    operaciones_h = pd.read_excel("OperacionesSimula.xlsx")
    precios_h = pd.read_excel("Historico Acciones.xlsx")


    dates, exigencia, stress = main(Fluct, Deltas, Grup_Comp, VMDacc, operaciones_h, precios_h)
    

        
    

tnp2 = time() - t0
print("Tiempo de Ejecución: ", tnp2)
    