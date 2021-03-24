import pandas as pd

class Garantia:

    def __init__(self, operaciones, precios):
        """
        La clase Garantía es usada para hallar la exigencia de caja de la CRCC

        Recibe como parámeros las operaciones realizadas y los precios de cierre de los activos. Ambos son dataframes de pandas.
        """

        self.operaciones = operaciones
        self.precios = precios


    def calculo(self, escenario):
        """
        Método para calcular la exigencia de garantías por parte de la CRCC para cierto escenario.

        
        """
        
        Cons_Actual = pd.DataFrame()
    
        #Grupo de compensación
        temp = []
        for grupo in escenario.Referencia:
        
            temp.append(grupo)
            
        temp = list(set(temp))
        temp = sorted(temp)
        Cons_Actual["GrupoCompensacion"] = temp
        
        #Cantidad Neta por Grupo, y Garantía por Posicón Neta por Grupo y, VMP Total por Grupo
        temp = []
        temp_1 = []
        temp_2 = []
        for grupo in Cons_Actual.GrupoCompensacion:
            
            suma = 0
            suma_1 = 0
            suma_2 = 0
            for i in escenario.index:
                
                if grupo == escenario.iloc[i,7]:
                    suma += escenario.iloc[i,8]
                    suma_1 += escenario.iloc[i,13]
                    suma_2 += escenario.iloc[i,15]
                
            temp.append(suma)
            temp_1.append(suma_1) 
            temp_2.append(suma_2)

        Cons_Actual["CantNeta"] = temp
        Cons_Actual["GarantiaPos"] = temp_1
        Cons_Actual["VMP"] = temp_2
        
        #Precio de Cierre
        temp = []
        for grupo in Cons_Actual.GrupoCompensacion:
            
            precio = 0
            for i in escenario.index:
                
                if grupo == escenario.iloc[i,7]:
                    precio = escenario.iloc[i,12]
                    break
                
            temp.append(precio)
            
        Cons_Actual["PrecioCierre"] = temp
        
        
        #VMD
        temp = []
        for grupo in Cons_Actual.GrupoCompensacion:
            
            VMD = 0
            for i in escenario.index:
                
                if grupo == escenario.iloc[i,7]:
                    VMD = escenario.iloc[i,10]
                    break
                
            temp.append(VMD)
            
        Cons_Actual["VMD"] = temp
        
        
        #Fluctuacion
        temp = []
        for grupo in Cons_Actual.GrupoCompensacion:
            
            Fluctuacion = 0
            for i in escenario.index:
                
                if grupo == escenario.iloc[i,7]:
                    Fluctuacion = escenario.iloc[i,11]
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
        GE = 0
        for gar in Cons_Actual.GarTotal:
            
            GE += gar
        
        #print ("La garantía total es", round(GE))
        GE = round(GE)


        return GE

        

    def escenario(self, direccion, fecha_M, Grup_Comp, VMDacc, Fluct):

        """Este método organiza el escenario para el cálculo de garantías.

        Recibe como parámetro la dirección del mercado, que puede ser al alza, a la baja, o estable.
        Recibe como parámetro la fecha mayor entre los dos días evaliados.
        Recibe como parámetro los grupos de compensación según especie.
        Recibe como parámetro 
        """

        #Comienza con indicativo vto: A si es a un día hábil, C si es a dos
        temp = []
        for vto in self.operaciones.FechaCum:
            
            if vto == fecha_M:
                temp.append("C")
            else:
                temp.append("A")
            
        self.operaciones["Vencimiento"] = temp

        #Grupo Base según especie
        temp = []
        for nemo in self.operaciones.strIDEspecie:
            
            base = Grup_Comp.index.get_loc(nemo)
            temp.append(str(Grup_Comp.iloc[base,0]))
        
        
        self.operaciones["GrupoBase"] = temp
        
        #Referencia del Grupo de Compensación respecto al día de cumplimiento, y Cantidad y Efectivo Netos por Operación
        temp = []
        temp_1 = []
        temp_2 = []
        for i in self.operaciones.index:
            
            if len(self.operaciones.iloc[i,6]) == 1:
                base = "0" + self.operaciones.iloc[i,6] + self.operaciones.iloc[i,5]
            else:
                base = self.operaciones.iloc[i,6] + self.operaciones.iloc[i,5]
            temp.append(base)

            if self.operaciones.iloc[i,0] == "V":
                base_1 = 0 - self.operaciones.iloc[i,2]
            else:
                base_1 = self.operaciones.iloc[i,2]
            temp_1.append(base_1)
            
            base_2 = base_1 * self.operaciones.iloc[i,3]
            temp_2.append(base_2)
        
        self.operaciones["Referencia"] = temp
        self.operaciones["CantNeta"] = temp_1
        self.operaciones["EfectivoNeto"] = temp_2    

    

        #VMD de la especie y Fluctuación de la especie
        temp = []
        temp_1 = []
        for nemo in self.operaciones.strIDEspecie:
            
            base = VMDacc.index.get_loc(nemo)
            base_1 = Fluct.index.get_loc(nemo)
            temp.append(VMDacc.iloc[base,0])
            temp_1.append(Fluct.iloc[base_1,0])

        self.operaciones["VMDEspecie"] = temp        
        self.operaciones["Fluctuacion"] = temp_1


        #Trae Precios de Cierre del Escenario

        temp = []
        for nemo in self.operaciones.strIDEspecie:
        
            base = self.precios.index.get_loc(nemo)
            temp.append(self.precios.iloc[base,direccion])
            
        self.operaciones["PrecioCierre"] = temp


        #Garantía por posición, Valoración Posición y VMP de cada operación para Escenario Actual
        temp = []
        temp_1 = []
        temp_2 = []
        
        for i in self.operaciones.index:
            
            base = round(self.operaciones.iloc[i,11]*self.operaciones.iloc[i,12],2) * self.operaciones.iloc[i,8]
            temp.append(base)
            
            base_1 = self.operaciones.iloc[i,12]*self.operaciones.iloc[i,8]
            temp_1.append(base_1)
            
        self.operaciones["GarPos"] = temp
        self.operaciones["Valoracion"] = temp_1  
        
        for i in self.operaciones.index:
        
            base_2 = self.operaciones.iloc[i,14] - self.operaciones.iloc[i,9]
            temp_2.append(base_2)
            
        self.operaciones["VMP"] = temp_2


        return self.operaciones


        
            




    
