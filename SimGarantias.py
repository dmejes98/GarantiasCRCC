# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:52:24 2020

@author: david.mejia
"""

from Garantias import garantia_CRCC
import pandas as pd
from datetime import datetime
import dateutil.relativedelta
import plotly.express as px
from time import time

t0 = time()

Fluct = pd.read_excel("Fluct.xlsx")
Fluct.set_index('Especie', inplace = True)

Deltas = pd.read_excel("Deltas.xlsx")

Grup_Comp = pd.read_excel("VMD.xlsx").loc[:,['Especie','Grupo']]
Grup_Comp.set_index('Especie', inplace = True)

VMDacc = pd.read_excel("VMD.xlsx").loc[:,['Especie','VMD']]
VMDacc.set_index('Especie', inplace = True)


Escenario_Ac = pd.read_excel("OperacionesSimula.xlsx")
Escenario_Al = pd.read_excel("OperacionesSimula.xlsx")
Escenario_Ba = pd.read_excel("OperacionesSimula.xlsx")

todas_las_fechas = list(set(Escenario_Al["FechaCum"]))
todas_las_fechas = sorted(todas_las_fechas)
    
#Selecciono fecha mayor y fecha menor
fecha_inicial = min(Escenario_Ac["FechaCum"])
fecha_final = max(Escenario_Ac["FechaCum"]) 
 

Almacena_GE = []
Almacena_LMC = []
Almacena_date = []

for i in range(0,len(todas_las_fechas)-1): #len(todas_las_fechas)-1

    Escenario_Ac = pd.read_excel("OperacionesSimula.xlsx")
    Escenario_Al = pd.read_excel("OperacionesSimula.xlsx")
    Escenario_Ba = pd.read_excel("OperacionesSimula.xlsx")
    
    
    todas_las_fechas = list(set(Escenario_Al["FechaCum"]))
    todas_las_fechas = sorted(todas_las_fechas)
    
    fecha_1 = todas_las_fechas[i]
    fecha_2 = todas_las_fechas[i+1]
    
    parte1 = Escenario_Ac[Escenario_Ac["FechaCum"] == fecha_1]
    parte2 = Escenario_Ac[Escenario_Ac["FechaCum"] == fecha_2]
    
    Escenario_Alza = pd.concat([parte1, parte2], ignore_index = True)
    Escenario_Baja = pd.concat([parte1, parte2], ignore_index = True)
    Escenario_Actual = pd.concat([parte1, parte2], ignore_index = True)
    
    todos = pd.read_excel("Historico Acciones.xlsx")
    todas_las_fechas = list(set(todos["Fecha"]))
    todas_las_fechas = sorted(todas_las_fechas)
    #todos.set_index("Fecha", inplace = True)
    
    precios_t = todos[todos["Fecha"] == fecha_2]
    precios_t = pd.concat([precios_t], ignore_index = True)
    
    precios_t = precios_t.drop(['Fecha'], axis = 1)
    
    indexs = ["UltimoPrecio"]
    
    precios_t["Nemotecnico"] = indexs
    precios_t.set_index("Nemotecnico", inplace = True)
    
    precios = precios_t.T
    
    (v1, v2, v3) = garantia_CRCC(Fluct, Deltas, Grup_Comp, VMDacc, Escenario_Actual, Escenario_Alza, Escenario_Baja, precios)
    
    Almacena_GE.append(v1)
    Almacena_LMC.append(v2)
    Almacena_date.append(fecha_2)
        
    

tnp2 = time() - t0
print("Tiempo de Ejecución: ", tnp2)
    