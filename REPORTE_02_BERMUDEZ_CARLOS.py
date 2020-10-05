"""
Created on Sat Sep 19 16:31:49 2020

@author: Carlos Jesús Bermúdez Bonilla
"""
# Se abre el archivo.csv y se alamcena como una lista de diccionario en la variable datos.
import csv
datos = []
with open("synergy_logistics_database.csv", "r") as logistics:
    lector = csv.DictReader(logistics)
    for linea in lector:
        datos.append(linea)

        
def totales(direccion):
    #esta función lo que hace es sacar los totales de exportaciones, importaciones o todos los datos
    conteo = 0
    for elemento in direccion:
        conteo += int(elemento['total_value'])
    return conteo
    
def continuar():
    #esta función lo que hace es crear la opción para ver otrso datos, entre exportaciones, importaciones o generales
    eleccion = input('¿Desea ver otros datos? Si[1]/No[0]: ')
    if '0' in eleccion:
        cambio = 1
    else:
        cambio = 0
    return cambio
def continuar2():
    #Esta funcion nos permite ver otros análisis
    eleccion = input('¿Desea hacer otro análisis? Si[1]/No[0]: ')
    if '0' in eleccion:
        cambio = 1
    else:
        cambio = 0
    return cambio

def menu(direccion):
    #En esta función estan definidos todos los análisis que se pueden hacer
    interruptor = 0
    while interruptor < 1:
        print("Hacer análisis por rutas [1]\n"
                "Hacer análisis por años [2]\n"
                "Hacer análisis por medio de transporte [3]\n"
                "Hacer análisis por producto [4]\n"
                "Hacer análisis por empresa [5]\n"
                "Hacer análisis por país [6]")
        respuesta = input("Opción: ")
        if '1' in respuesta:
            #Nos permite ver las rutas, contemplado como la misma ruta si está de la forma
            # Mexico- China o China- Mexico
            lista_rutas = []
            rutas_completas = []         
            for pais in direccion:
                ruta = [pais['origin'],pais['destination']]
                ruta_completa = [pais['origin'] + "-" + pais['destination']]
                if [pais['origin'], pais ['destination']] not in lista_rutas:
                    lista_rutas.append(ruta)
                    rutas_completas.append(ruta_completa)
                if [pais['destination'], pais['origin']] in lista_rutas:
                    lista_rutas.remove(ruta)
                    rutas_completas.remove(ruta_completa)
            for route in rutas_completas:
                contador = 0
                for pais in direccion:
                    temporal = route[0].split('-')
                    if (temporal[0] == pais['origin'] and temporal[1] == pais['destination']) or (temporal[0] == pais['destination'] and temporal[1] == pais['origin']):
                        contador += int(pais['total_value'])
                route.append(contador)
            rutas_completas.sort(key = lambda x: x[1], reverse = True)
            print('La cantidad de rutas a ver es: {}'.format(len(rutas_completas)))
            top = int(input('Indique la cantidad de rutas que desea ver: '))
            #Hace una impresión de la cantidad de rutas, se pueden ver desde 0 rutas al máximo de rutas que hay
            if top > len(rutas_completas):
                top = len(rutas_completas)
                
            valor = 0
            for n in range(top):
                print('{}. {}: ${:,}'.format(n + 1, rutas_completas[n][0], rutas_completas[n][1]))
                valor += rutas_completas[n][1]
            valor_total = totales(direccion)
            porcentaje = valor / valor_total * 100
            print('El valor total de las {} rutas equivale a ${:,} que representa el {}% del total.'.format(top,valor,porcentaje))
            interruptor = continuar2()
        elif '2' in respuesta:
            #Nos permite ver valor por año
            years = {}
            for registro in direccion:
                years[registro['year']] = years.get(registro['year'], 0) + int(registro['total_value'])
            for k,v in years.items():
                print("El valor para el año {} fue de: ${:,}".format(k,v))
            interruptor = continuar2()
        elif '3' in respuesta:
            #Nos permite ver valor por transporte
            transporte = {}
            for registro in direccion:
                transporte[registro['transport_mode']] = transporte.get(registro['transport_mode'], 0) + int(registro['total_value'])
            for k,v in transporte.items():
                print("El valor para {} fue de: ${:,}".format(k,v))
            interruptor = continuar2()
        elif '4' in respuesta:
            #nos permite ver el valor de cada producto
            producto = {}
            for registro in datos:
                producto[registro['product']] = producto.get(registro['product'], 0) + int(registro['total_value'])
            for k,v in producto.items():
                print("El valor del producto {} fue de: ${:,}".format(k,v))
            interruptor = continuar2()
        elif '5' in respuesta:
            # Nos permite ver el valor por empresa
            empresa = {}
            for registro in datos:
                empresa[registro['company_name']] = empresa.get(registro['company_name'], 0) + int(registro['total_value'])
            for k,v in empresa.items():
                print("La empresa {} nos genera: ${:,}".format(k,v))
            interruptor = continuar2()
        elif '6' in respuesta:
            #Nos permite ver el valor por cada pais
            #Si es exportación se toma el país de origen
            #Si es importación se toma el país de destino
            paises = {}
            for dato in direccion:
                if dato['direction'] == 'Imports':
                    paises[dato['destination']] = paises.get(dato['destination'], 0) + int(dato['total_value'])
                else:
                    paises[dato['origin']] = paises.get(dato['origin'], 0) + int(dato['total_value'])
            paises_lista = []
            for k,v in paises.items():
                paises_lista.append([k,v])
            paises_lista.sort(key = lambda x: x[1], reverse = True)
            porcentaje = 0
            suma_paises = 0
            contador = 0
            valor_total = totales(direccion)
            print('Los siguientes paises generan cerca del 80%')
            for pais in paises_lista:
                if porcentaje <= 80:
                    contador += 1
                    suma_paises += pais[1]
                    porcentaje = suma_paises / valor_total * 100
                    print("{}. {} genera: ${:,}".format(contador,pais[0],pais[1]))
            print('Estos paises generan el {}%'.format(porcentaje))
            interruptor = continuar2()

#acá hacemos una lista de diccionarios para importacion y otra para exportaciones,
#Estos van a ir como argumentos para las funciones, son la direccion
exportaciones = []
importaciones = []   
for dato in datos:
    if dato["direction"] == 'Exports':
        exportaciones.append(dato)
    else:
        importaciones.append(dato)
#Esyte es nuestro menu principal
interruptor = 0
while interruptor < 1:
     
    print ("Hola, los datos se pueden ver de las siguientes formas:\n"
            "Datos de exportaciones [1].\n"
            "Datos de importaciones [2].\n"
            "Datos generales [3].")
    respuesta = input("Opción: ")
    if '1' in respuesta:
        opcion = menu(exportaciones)
        interruptor = continuar()
    elif '2' in respuesta:
        opcion = menu(importaciones)
        interruptor = continuar()
    elif '3' in respuesta:
        opcion = menu(datos)
        interruptor = continuar()
        








