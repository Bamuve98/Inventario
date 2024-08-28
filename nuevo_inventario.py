import pandas as pd
from datetime import datetime
import math

pd.set_option('future.no_silent_downcasting', True)

path ='Proyectos\Inventario\INVENTARIO_FURO.xlsx'
fecha_hora_utc = datetime.now()
dia_semana_numero = fecha_hora_utc.weekday()
dia_semana_numero_corr = fecha_hora_utc.weekday() + 1 #Corrige el indice, ya que lunes = 0
dias_semana_texto = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
dia_semana_texto = dias_semana_texto[dia_semana_numero]

#Creacion de Dataframe para alcoholes

destilados = pd.read_excel(path, sheet_name='Alcohol')
columnas = destilados.columns[0], destilados.columns[-1] #Columna de etiquetas y columna del inventario del dia actual
stock_hoy = pd.read_excel(path, sheet_name='Alcohol', usecols=columnas)

#print(stock_hoy) #Check para ver que todo este OK

#Creacion de funciones recurrentes para el codigo

def pedir(liquido, cantidad, optimo):
    if cantidad < optimo:
        minimo = optimo - cantidad
        print(f'La cantidad de "{liquido}" es: {cantidad}, se sugiere pedir: {round(minimo)}')
        
def pedir_pack(liquido, cantidad, optimo, pack):
    if cantidad < optimo:
        minimo = optimo - cantidad
        ratio = math.ceil(minimo/pack)
        minimo_std = ratio * pack
        print(f'La cantidad de "{liquido}" es: {cantidad}, se sugiere pedir: {round(minimo_std)}')
        
def desgloe(stock):
    liquido = stock.loc[i,'Unidades Botella']
    dia = stock.columns[1]
    cantidad = stock.loc[i, dia]
    return liquido, dia, cantidad

def desgloe_bebidas(stock):
    liquido = stock.loc[i,'Unnamed: 1']
    dia = stock.columns[1]
    cantidad = stock.loc[i, dia]
    return liquido, dia, cantidad

def stock(inicio, fin):
    liquido_stock = stock_hoy.loc[inicio:fin].reset_index(drop=True).fillna(0) #reset de indices y se rellenan los espacios faltantes con 0 ***** OJO CON ESTO
    return liquido_stock

#Creacion de Sub-DataFrames para un analisis mas limpio

#Pisco
piscos_stock = stock(0,12)

#print(piscos_stock) # Check para Revisar si esta todo OK
print("Pisco: \n")

for i in range(len(piscos_stock.index)):
    pisco, dia, cantidad = desgloe(piscos_stock)
    idx_poca_rotacion = [1 , 2, 9] #Piscos de poca rotacion, idealmente tener 4 de estos minimos / Se ignora el 3, 11 y 12 porque no se pide
    if i in idx_poca_rotacion:
        pedir(pisco, cantidad, 4)
    elif i == 4: #Indice Mistral 35 1 Lt
        if dia_semana_numero_corr == 3 or dia_semana_numero_corr == 5: # Pedidos para las promos de Jueves y Sabado
            pedir(pisco, cantidad, 32)
        else:
            pedir(pisco, cantidad, 20)
    elif i == 5 or i == 6: # Mistral 40 y Nobel
        pedir(pisco, cantidad, 12)
    elif i == 7: # Mistral Apple
        if dia_semana_numero_corr == 1: #Pedido para promo del Martes
            pedir(pisco, cantidad, 12)
        else:
            pedir(pisco, cantidad, 8)
    elif i == 8: # Espiritu Los andes
        pedir(pisco, cantidad, 6)
    elif i == 10: #Alto 35 1 Lt
        pedir(pisco, cantidad, 18)
        
print("\n")

#Ron
ron_stock = stock(13,21)

#print(ron_stock) # Check para revisar si esta todo OK
print("Ron: \n")

for i in range(len(ron_stock.index)):
    ron, dia, cantidad = desgloe(ron_stock)
    idx_poca_rotacion = [2,3,7,8] # Se excluye 4 de todo el analisis
    if i in idx_poca_rotacion:
        pedir(ron, cantidad, 4)
    elif i == 1: # Habana Club 3 Años
        pedir(ron, cantidad, 9)
    elif i == 5 or i == 6: # Bacardi blanco 750 o Bacardi Coco
        pedir(ron, cantidad, 6)

print("\n")

#Gin
gin_stock = stock(23,28)
        
#print(gin_stock) # Check para revisar si esta todo OK
print("Gin: \n")
        
for i in range(len(gin_stock.index)):
    gin, dia, cantidad = desgloe(gin_stock)
    if i == 1:
        if dia_semana_numero_corr == 2 or dia_semana_numero_corr == 5:
            pedir(gin, cantidad, 18)
        else:
            pedir(gin, cantidad, 12)
    elif i == 2 or i ==4:
        pedir(gin, cantidad, 6)
    elif i == 3:
        if dia_semana_numero_corr == 3 or dia_semana_numero_corr == 6:
            pedir(gin, cantidad, 12)
        else:
            pedir(gin, cantidad, 8)
    elif i == 5:
        if dia_semana_numero_corr == 3 or dia_semana_numero_corr == 6:
            pedir(gin, cantidad, 18)
        else:
            pedir(gin, cantidad, 12)
            
print("\n")

#Whisky
whisky_stock = stock(30,39)

#print(whisky_stock) # Check para ver que todo vaya bien
print("Whisky: \n")

for i in range(len(whisky_stock.index)):
    whisky, dia, cantidad = desgloe(whisky_stock)
    idx_poca_rotacion = [4, 6, 7, 8, 9]
    if i in idx_poca_rotacion:
        pedir(whisky, cantidad, 4)
    elif i == 1 or i == 2 or i == 3: #Gama Jhonny
        pedir(whisky, cantidad, 6)
    elif i == 5: # Jack 7
        pedir(whisky, cantidad, 6)
        
print("\n")

#Vodka
voda_stock = stock(41,44)

#print(voda_stock) # Check para ver que todo este OK
print("Vodka: \n")
    
for i in range(len(voda_stock.index)):
    vodka, dia, cantidad = desgloe(voda_stock)
    if i > 0:
        pedir(vodka, cantidad, 4)
    
print("\n")

#Tequila
tequila_stock = stock(45,48)

#print(tequila_stock) # Check para ver que todo este OK
print("Tequila: \n")
    
for i in range(len(tequila_stock.index)):
    tequila, dia, cantidad = desgloe(tequila_stock)
    if i > 0:
        pedir(tequila, cantidad, 6)
        
print("\n")
        
#Licores
licores_stock = stock(50, 68)

#print(licores_stock) # Check para ver que todo este OK
print("Licores: \n")

for i in range(len(licores_stock.index)):
    licor, dia, cantidad = desgloe(licores_stock)
    idx_poca_rotacion = [3,5,6,9,10,12,14,16,17,18] # Se excluye 8, 13
    if i in idx_poca_rotacion:
        pedir(licor, cantidad, 4)
    elif i == 1:
        pedir(licor, cantidad, 10)
    elif i == 2:
        if dia_semana_numero_corr == 1:
            pedir(licor, cantidad, 24)
        else:
            pedir(licor, cantidad, 12)
    elif i == 4:
        pedir(licor, cantidad, 8)
    elif i in [7,11, 15]:
        pedir(licor, cantidad, 6)
        
print("\n")

#Cervezas
cerveza_stock = stock(70, 87)

#print(cerveza_stock) #Check para ver que todo este OK
print("Cervezas: \n")

for i in range(len(cerveza_stock.index)):
    cerveza, dia, cantidad = desgloe(cerveza_stock)
    idx_poca_rotacion = [3,8,15] #Se omite 7, 12, 13, 14, 16
    idx_alta_rotacion = [1,2,4,5,6,9,10,11,17]
    if i in idx_poca_rotacion:
        pedir_pack(cerveza, cantidad, 4, 24)
    elif i in idx_alta_rotacion:
        pedir_pack(cerveza, cantidad, 12, 24)
  
print("\n")  


#Barriletes
barrilete_stock = stock(88, 91)
    
#print(barrilete_stock) # Check para ver que todo este OK
print("Barriletes: \n")
    
for i in range(len(barrilete_stock.index)):
    barrilete, dia, cantidad = desgloe(barrilete_stock)
    if i == 1 or i == 2:
        if dia_semana_numero_corr == 4:
            pedir(barrilete, cantidad, 5)
        else:
            pedir(barrilete, cantidad, 3)
    elif i == 3:
        pedir(barrilete, cantidad, 1)

print("\n")

#Vinos Blancos
vinos_blancos_stock = stock(98, 109)

#print(vinos_blancos_stock) # Check para ver que todo este OK
print("Vinos: \n")

for i in range(len(vinos_blancos_stock.index)):
    vino_blanco, dia, cantidad = desgloe(vinos_blancos_stock)
    idx_marca = [0,3,6,9]
    if i in idx_marca:
        print(f'\n {vino_blanco}:')
    else:
        pedir(vino_blanco, cantidad, 6)
    
print("\n")

#Vinos Rojos
vinos_rojos_stock = stock(111, 152)

#print(vinos_rojos_stock)

for i in range(len(vinos_rojos_stock.index)):
    vino_rojo, dia, cantidad = desgloe(vinos_rojos_stock)
    idx_alta_rotacion = [2,3,6,10,11,36,37,38]
    idx_poca_rotacion = [4,5,6,7,12,13,14,17,18,19,20,21,24,25,26,27,28]
    idx_a_ignorar = [0,8,15,22,29,34,39]
    idx_marca = [1,9,16,23,30,35,40]
    if i in idx_alta_rotacion:
        pedir(vino_rojo, cantidad, 8)
    elif i in idx_poca_rotacion:
        pedir(vino_rojo, cantidad, 4)
    elif i in idx_marca:
        print(f'\n {vino_rojo}:')
    elif i in idx_a_ignorar:
        pass
    else:
        pedir(vino_rojo, cantidad, 1)
        
print("\n")

#Espumantes
espumante_stock = stock(164, 180)

#print(espumante_stock) # Check para ver que todo este OK
print("Espumantes: \n")

for i in range(len(espumante_stock.index)):
    espumante, dia, cantidad = desgloe(espumante_stock)
    if i == 3:
        if dia_semana_numero_corr == 1 or dia_semana_numero_corr == 5:
            pedir_pack(espumante, cantidad, 60, 6)
        else:
            pedir_pack(espumante, cantidad, 42, 6)
    elif i == 16:
        pedir_pack(espumante, cantidad, 8, 12)
    elif i == 1 or i == 14:
        print(f'\n {espumante}:')
    else:
        pass
        
print("\n")

#Bebidas y liquidos

liquidos = pd.read_excel(path, sheet_name='Liquidos')
columnas = liquidos.columns[1], liquidos.columns[-1]
stock_hoy = pd.read_excel(path, sheet_name='Liquidos', usecols=columnas)
    
#print(stock_hoy) # Check para ver que todo este OK

#Bebidas
bebida_stock = stock(1, 24)

#print(bebida_stock) # Check para ver que todo este OK
print("Bebidas: \n")

for i in range(len(bebida_stock.index)):
    bebida, dia, cantidad = desgloe_bebidas(bebida_stock)
    idx_cocacola = list(range(10)) + [18,19]
    idx_pepsi = [10, 11, 12, 14, 15, 16, 20, 21, 22, 23]
    if i in idx_cocacola:
        if i == 1 or i == 4: # Coca-Cola 0 350 y 220
            pedir_pack(bebida, cantidad, 120, 24)
        elif i in [18,19]: # Fanta
            pedir_pack(bebida, cantidad, 24, 24)
        else: 
            pedir_pack(bebida, cantidad, 48, 24)
    elif i in idx_pepsi:
        if (i == 21 or i == 23): # Pepsi 0 350 y 220
            if dia_semana_numero_corr == 3 or dia_semana_numero_corr == 5: # Promo dia jueves y sabado
                pedir_pack(bebida, cantidad, 180, 24)
            else:
                pedir_pack(bebida, cantidad, 96, 24)
        elif i in [11,15,16]:
            if dia_semana_numero_corr == 2 or dia_semana_numero_corr == 5: #Promo dia miercoles y sabado
                pedir_pack(bebida, cantidad, 120, 24)
            else:
                pedir_pack(bebida, cantidad, 72, 24)
        else:
            pedir_pack(bebida, cantidad, 48, 24)
