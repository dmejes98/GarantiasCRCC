# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 00:03:09 2020

@author: david.mejia
"""

import pandas as pd
from datetime import datetime

#Importo matrices de parámetros

Fluct = pd.read_excel("Fluct.xlsx")
Fluct.set_index('Especie', inplace = True)

Deltas = pd.read_excel("Deltas.xlsx")

Grup_Comp = pd.read_excel("VMD.xlsx").loc[:,['Especie','Grupo']]
Grup_Comp.set_index('Especie', inplace = True)

VMDacc = pd.read_excel("VMD.xlsx").loc[:,['Especie','VMD']]
VMDacc.set_index('Especie', inplace = True)

Escenario_Actual = pd.read_excel("Operaciones.xlsx")
Escenario_Alza = pd.read_excel("Operaciones.xlsx")
Escenario_Baja = pd.read_excel("Operaciones.xlsx")
precios = pd.read_excel("precios.xls")
precios.set_index('Nemotecnico', inplace = True)


def garantia_CRCC (Fluct, Deltas, Grup_Comp, VMDacc, Escenario_Actual, Escenario_Alza, Escenario_Baja, precios):
        
    #Busco la Fluctuación en Fluct y la llevo a precios para calcular escenarios
    temp = []
    for nemo in precios.index:
            
        base = Fluct.index.get_loc(nemo)
        temp.append(Fluct.iloc[base,0])
    
    #Calculo escenarios por especie   
    precios["Flt"] = temp
    precios["Alza"] = round(precios["UltimoPrecio"] * (1 + precios["Flt"]*0.75),0)
    precios["Baja"] = round(precios["UltimoPrecio"] * (1 - precios["Flt"]*0.75),0)
    
    
    #Selecciono fecha mayor y fecha menor
    fecha_M = max(Escenario_Actual["FechaCum"])
    fecha_m = min(Escenario_Actual["FechaCum"])
    
    
    #Completo matriz de Escenario Actual
    #Comienza con indicativo vto: A si es a un día hábil, C si es a dos
    temp = []
    for vto in Escenario_Actual.FechaCum:
        
        if vto == fecha_M:
            temp.append("C")
        else:
            temp.append("A")
        
    Escenario_Actual["Vencimiento"] = temp
    
    #Grupo Base según especie
    temp = []
    for nemo in Escenario_Actual.strIDEspecie:
        
        base = Grup_Comp.index.get_loc(nemo)
        temp.append(str(Grup_Comp.iloc[base,0]))
    
    
    Escenario_Actual["GrupoBase"] = temp
    
    #Referencia del Grupo de Compensación respecto al día de cumplimiento
    temp = []
    for i in Escenario_Actual.index:
        
        if len(Escenario_Actual.iloc[i,6]) == 1:
            base = "0" + Escenario_Actual.iloc[i,6] + Escenario_Actual.iloc[i,5]
        else:
            base = Escenario_Actual.iloc[i,6] + Escenario_Actual.iloc[i,5]
        temp.append(base)
    
    Escenario_Actual["Referencia"] = temp
    
    
    #Cantidad y Efectivo Netos por Operación
    temp = []
    temp_1 = []
    for i in Escenario_Actual.index:
        
        if Escenario_Actual.iloc[i,0] == "V":
            base = 0 - Escenario_Actual.iloc[i,2]
        else:
            base = Escenario_Actual.iloc[i,2]
        temp.append(base)
        
        base_1 = base * Escenario_Actual.iloc[i,3]
        temp_1.append(base_1)
        
    Escenario_Actual["CantNeta"] = temp
    Escenario_Actual["EfectivoNeto"] = temp_1
    
    
    #VMD de la especie
    temp = []
    for nemo in Escenario_Actual.strIDEspecie:
        
        base = VMDacc.index.get_loc(nemo)
        temp.append(VMDacc.iloc[base,0])
    
    
    Escenario_Actual["VMDEspecie"] = temp
    
    #Fluctuación de la especie
    temp = []
    for nemo in Escenario_Actual.strIDEspecie:
        
        base = Fluct.index.get_loc(nemo)
        temp.append(Fluct.iloc[base,0])
    
    
    Escenario_Actual["Fluctuacion"] = temp
    
    #Trae Precios de Cierre del Escenario
    temp = []
    for nemo in Escenario_Actual.strIDEspecie:
        
        base = precios.index.get_loc(nemo)
        temp.append(precios.iloc[base,0])
        
    Escenario_Actual["PrecioCierre"] = temp
     
    #Garantía por posición, Valoración Posición y VMP de cada operación para Escenario Actual
    temp = []
    temp_1 = []
    temp_2 = []
    
    for i in Escenario_Actual.index:
        
        base = round(Escenario_Actual.iloc[i,11]*Escenario_Actual.iloc[i,12],2) * Escenario_Actual.iloc[i,8]
        temp.append(base)
        
        base_1 = Escenario_Actual.iloc[i,12]*Escenario_Actual.iloc[i,8]
        temp_1.append(base_1)
        
    
        
    Escenario_Actual["GarPos"] = temp
    Escenario_Actual["Valoracion"] = temp_1  
    
    for i in Escenario_Actual.index:
    
        base_2 = Escenario_Actual.iloc[i,14] - Escenario_Actual.iloc[i,9]
        temp_2.append(base_2)
        
    Escenario_Actual["VMP"] = temp_2
    
    
    
    #Completo matriz de Escenario Alza
    #Comienza con indicativo vto: A si es a un día hábil, C si es a dos
    temp = []
    for vto in Escenario_Alza.FechaCum:
        
        if vto == fecha_M:
            temp.append("C")
        else:
            temp.append("A")
        
    Escenario_Alza["Vencimiento"] = temp
    
    #Grupo Base según especie
    temp = []
    for nemo in Escenario_Alza.strIDEspecie:
        
        base = Grup_Comp.index.get_loc(nemo)
        temp.append(str(Grup_Comp.iloc[base,0]))
    
    
    Escenario_Alza["GrupoBase"] = temp
    
    #Referencia del Grupo de Compensación respecto al día de cumplimiento
    temp = []
    for i in Escenario_Alza.index:
        
        if len(Escenario_Alza.iloc[i,6]) == 1:
            base = "0" + Escenario_Alza.iloc[i,6] + Escenario_Alza.iloc[i,5]
        else:
            base = Escenario_Alza.iloc[i,6] + Escenario_Alza.iloc[i,5]
        temp.append(base)
    
    Escenario_Alza["Referencia"] = temp
    
    
    #Cantidad y Efectivo Netos por Operación
    temp = []
    temp_1 = []
    for i in Escenario_Alza.index:
        
        if Escenario_Alza.iloc[i,0] == "V":
            base = 0 - Escenario_Alza.iloc[i,2]
        else:
            base = Escenario_Alza.iloc[i,2]
        temp.append(base)
        
        base_1 = base * Escenario_Alza.iloc[i,3]
        temp_1.append(base_1)
        
    Escenario_Alza["CantNeta"] = temp
    Escenario_Alza["EfectivoNeto"] = temp_1
    
    
    #VMD de la especie
    temp = []
    for nemo in Escenario_Alza.strIDEspecie:
        
        base = VMDacc.index.get_loc(nemo)
        temp.append(VMDacc.iloc[base,0])
    
    
    Escenario_Alza["VMDEspecie"] = temp
    
    #Fluctuación de la especie
    temp = []
    for nemo in Escenario_Alza.strIDEspecie:
        
        base = Fluct.index.get_loc(nemo)
        temp.append(Fluct.iloc[base,0])
    
    
    Escenario_Alza["Fluctuacion"] = temp
    
    #Trae Precios de Cierre del Escenario
    temp = []
    for nemo in Escenario_Alza.strIDEspecie:
        
        base = precios.index.get_loc(nemo)
        temp.append(precios.iloc[base,2])
        
    Escenario_Alza["PrecioCierre"] = temp
     
    #Garantía por posición, Valoración Posición y VMP de cada operación para Escenario Actual
    temp = []
    temp_1 = []
    temp_2 = []
    
    for i in Escenario_Alza.index:
        
        base = round(Escenario_Alza.iloc[i,11]*Escenario_Alza.iloc[i,12],2) * Escenario_Alza.iloc[i,8]
        temp.append(base)
        
        base_1 = Escenario_Alza.iloc[i,12]*Escenario_Alza.iloc[i,8]
        temp_1.append(base_1)
        
    
        
    Escenario_Alza["GarPos"] = temp
    Escenario_Alza["Valoracion"] = temp_1  
    
    for i in Escenario_Alza.index:
    
        base_2 = Escenario_Alza.iloc[i,14] - Escenario_Alza.iloc[i,9]
        temp_2.append(base_2)
        
    Escenario_Alza["VMP"] = temp_2
    
    
    
    #Completo matriz de Escenario Baja
    #Comienza con indicativo vto: A si es a un día hábil, C si es a dos
    temp = []
    for vto in Escenario_Baja.FechaCum:
        
        if vto == fecha_M:
            temp.append("C")
        else:
            temp.append("A")
        
    Escenario_Baja["Vencimiento"] = temp
    
    #Grupo Base según especie
    temp = []
    for nemo in Escenario_Baja.strIDEspecie:
        
        base = Grup_Comp.index.get_loc(nemo)
        temp.append(str(Grup_Comp.iloc[base,0]))
    
    
    Escenario_Baja["GrupoBase"] = temp
    
    #Referencia del Grupo de Compensación respecto al día de cumplimiento
    temp = []
    for i in Escenario_Baja.index:
        
        if len(Escenario_Baja.iloc[i,6]) == 1:
            base = "0" + Escenario_Baja.iloc[i,6] + Escenario_Baja.iloc[i,5]
        else:
            base = Escenario_Baja.iloc[i,6] + Escenario_Baja.iloc[i,5]
        temp.append(base)
    
    Escenario_Baja["Referencia"] = temp
    
    
    #Cantidad y Efectivo Netos por Operación
    temp = []
    temp_1 = []
    for i in Escenario_Baja.index:
        
        if Escenario_Baja.iloc[i,0] == "V":
            base = 0 - Escenario_Baja.iloc[i,2]
        else:
            base = Escenario_Baja.iloc[i,2]
        temp.append(base)
        
        base_1 = base * Escenario_Baja.iloc[i,3]
        temp_1.append(base_1)
        
    Escenario_Baja["CantNeta"] = temp
    Escenario_Baja["EfectivoNeto"] = temp_1
    
    
    #VMD de la especie
    temp = []
    for nemo in Escenario_Baja.strIDEspecie:
        
        base = VMDacc.index.get_loc(nemo)
        temp.append(VMDacc.iloc[base,0])
    
    
    Escenario_Baja["VMDEspecie"] = temp
    
    #Fluctuación de la especie
    temp = []
    for nemo in Escenario_Baja.strIDEspecie:
        
        base = Fluct.index.get_loc(nemo)
        temp.append(Fluct.iloc[base,0])
    
    
    Escenario_Baja["Fluctuacion"] = temp
    
    #Trae Precios de Cierre del Escenario
    temp = []
    for nemo in Escenario_Baja.strIDEspecie:
        
        base = precios.index.get_loc(nemo)
        temp.append(precios.iloc[base,3])
        
    Escenario_Baja["PrecioCierre"] = temp
     
    #Garantía por posición, Valoración Posición y VMP de cada operación para Escenario Actual
    temp = []
    temp_1 = []
    temp_2 = []
    
    for i in Escenario_Baja.index:
        
        base = round(Escenario_Baja.iloc[i,11]*Escenario_Baja.iloc[i,12],2) * Escenario_Baja.iloc[i,8]
        temp.append(base)
        
        base_1 = Escenario_Baja.iloc[i,12]*Escenario_Baja.iloc[i,8]
        temp_1.append(base_1)
        
    
        
    Escenario_Baja["GarPos"] = temp
    Escenario_Baja["Valoracion"] = temp_1  
    
    for i in Escenario_Baja.index:
    
        base_2 = Escenario_Baja.iloc[i,14] - Escenario_Baja.iloc[i,9]
        temp_2.append(base_2)
        
    Escenario_Baja["VMP"] = temp_2
    
    
    
    
    
    #CONSOLIDAR ESCENARIOS
    
    
    #Consolidado Actual
    Cons_Actual = pd.DataFrame()
    
    #Grupo de compensación
    temp = []
    for grupo in Escenario_Actual.Referencia:
    
        temp.append(grupo)
         
    temp = list(set(temp))
    temp = sorted(temp)
    Cons_Actual["GrupoCompensacion"] = temp
    
    #Cantidad Neta por Grupo
    temp = []
    for grupo in Cons_Actual.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Actual.index:
            
            if grupo == Escenario_Actual.iloc[i,7]:
                suma += Escenario_Actual.iloc[i,8]
            
        temp.append(suma)
        
    Cons_Actual["CantNeta"] = temp
    
    #Garantía por Posicón Neta por Grupo
    temp = []
    for grupo in Cons_Actual.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Actual.index:
            
            if grupo == Escenario_Actual.iloc[i,7]:
                suma += Escenario_Actual.iloc[i,13]
            
        temp.append(suma)
        
    Cons_Actual["GarantiaPos"] = temp
    
    #VMP Total por Grupo
    temp = []
    for grupo in Cons_Actual.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Actual.index:
            
            if grupo == Escenario_Actual.iloc[i,7]:
                suma += Escenario_Actual.iloc[i,15]
            
        temp.append(suma)
        
    Cons_Actual["VMP"] = temp
    
    #Precio de Cierre
    temp = []
    for grupo in Cons_Actual.GrupoCompensacion:
        
        precio = 0
        for i in Escenario_Actual.index:
            
            if grupo == Escenario_Actual.iloc[i,7]:
                precio = Escenario_Actual.iloc[i,12]
                break
            
        temp.append(precio)
        
    Cons_Actual["PrecioCierre"] = temp
    
    
    #VMD
    temp = []
    for grupo in Cons_Actual.GrupoCompensacion:
        
        VMD = 0
        for i in Escenario_Actual.index:
            
            if grupo == Escenario_Actual.iloc[i,7]:
                VMD = Escenario_Actual.iloc[i,10]
                break
            
        temp.append(VMD)
        
    Cons_Actual["VMD"] = temp
    
    
    #Fluctuacion
    temp = []
    for grupo in Cons_Actual.GrupoCompensacion:
        
        Fluctuacion = 0
        for i in Escenario_Actual.index:
            
            if grupo == Escenario_Actual.iloc[i,7]:
                Fluctuacion = Escenario_Actual.iloc[i,11]
                break
            
        temp.append(Fluctuacion)
        
    Cons_Actual["Fluctuacion"] = temp
    
    
    #Calculo Gran Posición por Grupo
    temp = []
    for i in Cons_Actual.index:
        
        if Cons_Actual.iloc[i,5] == 0:
            base = 3
        else:
            base = abs(Cons_Actual.iloc[i,1])/Cons_Actual.iloc[i,5]
    
        
        temp.append(base)
        
    Cons_Actual["GranPos"] = temp
    
    
    #Garantía Ajustada por Gran Posición
    temp = []
    for i in Cons_Actual.index:
        
        if Cons_Actual.iloc[i,7] >= 1 and Cons_Actual.iloc[i,7] < 1.5:
            base = round(Cons_Actual.iloc[i,6]*1.28*Cons_Actual.iloc[i,4],2)*Cons_Actual.iloc[i,1]
        elif Cons_Actual.iloc[i,7] >= 1.5 and Cons_Actual.iloc[i,7] < 2:
            base = round(Cons_Actual.iloc[i,6]*1.52*Cons_Actual.iloc[i,4],2)*Cons_Actual.iloc[i,1]
        elif Cons_Actual.iloc[i,7] >= 2:
            base = round(Cons_Actual.iloc[i,6]*1.73*Cons_Actual.iloc[i,4],2)*Cons_Actual.iloc[i,1]
        else:
            base = Cons_Actual.iloc[i,2]
    
        base = abs(base)
        temp.append(base)
        
    Cons_Actual["GarAjustadaGP"] = temp
       
    
    #Garantía Total por especie
    temp = []
    for i in Cons_Actual.index:
        
        base = Cons_Actual.iloc[i,8] - Cons_Actual.iloc[i,3]
        temp.append(base)
        
    Cons_Actual["GarTotal"] = temp
    
    
    #Garantía Final
    suma = 0
    for gar in Cons_Actual.GarTotal:
        
        suma += gar
    
    #print ("La garantía total es", round(suma))
    GE = round(suma)
    
    
    
    
    
    #Consolidado Baja
    Cons_Baja = pd.DataFrame()
    
    #Grupo de compensación
    temp = []
    for grupo in Escenario_Baja.Referencia:
    
        temp.append(grupo)
         
    temp = list(set(temp))
    temp = sorted(temp)
    Cons_Baja["GrupoCompensacion"] = temp
    
    #Cantidad Neta por Grupo
    temp = []
    for grupo in Cons_Baja.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Baja.index:
            
            if grupo == Escenario_Baja.iloc[i,7]:
                suma += Escenario_Baja.iloc[i,8]
            
        temp.append(suma)
        
    Cons_Baja["CantNeta"] = temp
    
    #Garantía por Posicón Neta por Grupo
    temp = []
    for grupo in Cons_Baja.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Baja.index:
            
            if grupo == Escenario_Baja.iloc[i,7]:
                suma += Escenario_Baja.iloc[i,13]
            
        temp.append(suma)
        
    Cons_Baja["GarantiaPos"] = temp
    
    #VMP Total por Grupo
    temp = []
    for grupo in Cons_Baja.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Baja.index:
            
            if grupo == Escenario_Baja.iloc[i,7]:
                suma += Escenario_Baja.iloc[i,15]
            
        temp.append(suma)
        
    Cons_Baja["VMP"] = temp
    
    #Precio de Cierre
    temp = []
    for grupo in Cons_Baja.GrupoCompensacion:
        
        precio = 0
        for i in Escenario_Baja.index:
            
            if grupo == Escenario_Baja.iloc[i,7]:
                precio = Escenario_Baja.iloc[i,12]
                break
            
        temp.append(precio)
        
    Cons_Baja["PrecioCierre"] = temp
    
    
    #VMD
    temp = []
    for grupo in Cons_Baja.GrupoCompensacion:
        
        VMD = 0
        for i in Escenario_Baja.index:
            
            if grupo == Escenario_Baja.iloc[i,7]:
                VMD = Escenario_Baja.iloc[i,10]
                break
            
        temp.append(VMD)
        
    Cons_Baja["VMD"] = temp
    
    
    #Fluctuacion
    temp = []
    for grupo in Cons_Baja.GrupoCompensacion:
        
        Fluctuacion = 0
        for i in Escenario_Baja.index:
            
            if grupo == Escenario_Baja.iloc[i,7]:
                Fluctuacion = Escenario_Baja.iloc[i,11]
                break
            
        temp.append(Fluctuacion)
        
    Cons_Baja["Fluctuacion"] = temp
    
    
    #Calculo Gran Posición por Grupo
    temp = []
    for i in Cons_Baja.index:
        
        if Cons_Baja.iloc[i,5] == 0:
            base = 3
        else:
            base = abs(Cons_Baja.iloc[i,1])/Cons_Baja.iloc[i,5]
    
        
        temp.append(base)
        
    Cons_Baja["GranPos"] = temp
    
    
    #Garantía Ajustada por Gran Posición
    temp = []
    for i in Cons_Baja.index:
        
        if Cons_Baja.iloc[i,7] >= 1 and Cons_Baja.iloc[i,7] < 1.5:
            base = round(Cons_Baja.iloc[i,6]*1.28*Cons_Baja.iloc[i,4],2)*Cons_Baja.iloc[i,1]
        elif Cons_Baja.iloc[i,7] >= 1.5 and Cons_Baja.iloc[i,7] < 2:
            base = round(Cons_Baja.iloc[i,6]*1.52*Cons_Baja.iloc[i,4],2)*Cons_Baja.iloc[i,1]
        elif Cons_Baja.iloc[i,7] >= 2:
            base = round(Cons_Baja.iloc[i,6]*1.73*Cons_Baja.iloc[i,4],2)*Cons_Baja.iloc[i,1]
        else:
            base = Cons_Baja.iloc[i,2]
    
        base = abs(base)
        temp.append(base)
        
    Cons_Baja["GarAjustadaGP"] = temp
       
    
    #Garantía Total por especie
    temp = []
    for i in Cons_Baja.index:
        
        base = Cons_Baja.iloc[i,8] - Cons_Baja.iloc[i,3]
        temp.append(base)
        
    Cons_Baja["GarTotal"] = temp
    
    
    #Garantía Final
    sumab = 0
    for gar in Cons_Baja.GarTotal:
        
        sumab += gar
    
    
    
    
    
    
    
    #Consolidado Alza
    Cons_Alza = pd.DataFrame()
    
    #Grupo de compensación
    temp = []
    for grupo in Escenario_Alza.Referencia:
    
        temp.append(grupo)
         
    temp = list(set(temp))
    temp = sorted(temp)
    Cons_Alza["GrupoCompensacion"] = temp
    
    #Cantidad Neta por Grupo
    temp = []
    for grupo in Cons_Alza.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Alza.index:
            
            if grupo == Escenario_Alza.iloc[i,7]:
                suma += Escenario_Alza.iloc[i,8]
            
        temp.append(suma)
        
    Cons_Alza["CantNeta"] = temp
    
    #Garantía por Posicón Neta por Grupo
    temp = []
    for grupo in Cons_Alza.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Alza.index:
            
            if grupo == Escenario_Alza.iloc[i,7]:
                suma += Escenario_Alza.iloc[i,13]
            
        temp.append(suma)
        
    Cons_Alza["GarantiaPos"] = temp
    
    #VMP Total por Grupo
    temp = []
    for grupo in Cons_Alza.GrupoCompensacion:
        
        suma = 0
        for i in Escenario_Alza.index:
            
            if grupo == Escenario_Alza.iloc[i,7]:
                suma += Escenario_Alza.iloc[i,15]
            
        temp.append(suma)
        
    Cons_Alza["VMP"] = temp
    
    #Precio de Cierre
    temp = []
    for grupo in Cons_Alza.GrupoCompensacion:
        
        precio = 0
        for i in Escenario_Alza.index:
            
            if grupo == Escenario_Alza.iloc[i,7]:
                precio = Escenario_Alza.iloc[i,12]
                break
            
        temp.append(precio)
        
    Cons_Alza["PrecioCierre"] = temp
    
    
    #VMD
    temp = []
    for grupo in Cons_Alza.GrupoCompensacion:
        
        VMD = 0
        for i in Escenario_Alza.index:
            
            if grupo == Escenario_Alza.iloc[i,7]:
                VMD = Escenario_Alza.iloc[i,10]
                break
            
        temp.append(VMD)
        
    Cons_Alza["VMD"] = temp
    
    
    #Fluctuacion
    temp = []
    for grupo in Cons_Alza.GrupoCompensacion:
        
        Fluctuacion = 0
        for i in Escenario_Alza.index:
            
            if grupo == Escenario_Alza.iloc[i,7]:
                Fluctuacion = Escenario_Alza.iloc[i,11]
                break
            
        temp.append(Fluctuacion)
        
    Cons_Alza["Fluctuacion"] = temp
    
    
    #Calculo Gran Posición por Grupo
    temp = []
    for i in Cons_Alza.index:
        
        if Cons_Alza.iloc[i,5] == 0:
            base = 3
        else:
            base = abs(Cons_Alza.iloc[i,1])/Cons_Alza.iloc[i,5]
    
        
        temp.append(base)
        
    Cons_Alza["GranPos"] = temp
    
    
    #Garantía Ajustada por Gran Posición
    temp = []
    for i in Cons_Alza.index:
        
        if Cons_Alza.iloc[i,7] >= 1 and Cons_Alza.iloc[i,7] < 1.5:
            base = round(Cons_Alza.iloc[i,6]*1.28*Cons_Alza.iloc[i,4],2)*Cons_Alza.iloc[i,1]
        elif Cons_Alza.iloc[i,7] >= 1.5 and Cons_Alza.iloc[i,7] < 2:
            base = round(Cons_Alza.iloc[i,6]*1.52*Cons_Alza.iloc[i,4],2)*Cons_Alza.iloc[i,1]
        elif Cons_Alza.iloc[i,7] >= 2:
            base = round(Cons_Alza.iloc[i,6]*1.73*Cons_Alza.iloc[i,4],2)*Cons_Alza.iloc[i,1]
        else:
            base = Cons_Alza.iloc[i,2]
    
        base = abs(base)
        temp.append(base)
        
    Cons_Alza["GarAjustadaGP"] = temp
       
    
    #Garantía Total por especie
    temp = []
    for i in Cons_Alza.index:
        
        base = Cons_Alza.iloc[i,8] - Cons_Alza.iloc[i,3]
        temp.append(base)
        
    Cons_Alza["GarTotal"] = temp
    
    
    #Garantía Final
    sumaa = 0
    for gar in Cons_Alza.GarTotal:
        
        sumaa += gar
    
    
    
    #print ("La garantía total por LMC es", round(max([sumab,sumaa])))
    GELMC = round(max([sumab,sumaa]))
    
    
    return (GE, GELMC, Cons_Actual)


if __name__ == '__main__':
    (v1, v2, v3) = garantia_CRCC (Fluct, Deltas, Grup_Comp, VMDacc, Escenario_Actual, Escenario_Alza, Escenario_Baja, precios) 

    print ("La garantía total es", v1)
    print ("La garantía total por LMC es", v2) 
