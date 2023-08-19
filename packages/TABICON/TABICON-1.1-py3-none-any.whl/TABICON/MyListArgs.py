#! usr/bin/env python 3
# coding=utf-8
from TABICON.ManejoArchivos import *
from TABICON.ManejoER import *
from pathlib import Path
from decimal import Decimal
import datetime
import regex as re
import os

__autor__ = 'Ulises García Calderón'

class MyListArgs():
    '''
    Permite la lectura de argumentos pasado por linea de comandos o por lectura
    de archivo. Además permite buscar y recuperar cadena.
    '''
    def __init__(self,strings: list):
        '''
        Construye una Lista de cadenas a partir de una arreglo de cadenas
        :param strings: arreglo de cadenas
        '''
        self.args = {}
        self.oLineas = []
        self.er_Keys = ManejoER(r'^\s*(-\w+[\p{Print}&&[^\s]]*)\s*(\'(.+)\'\s*$|(.+))')
        self.er_Comen = ManejoER(r'^\\s*#(.*)') #^\\s*#(.*)

        for i in range(1,len(strings),2):
            self.args.update({strings[i - 1].upper():strings[i]})

    def addArguments(self, strings:list):
        '''
        Construye una lista de cadenas a partir de un arreglo de cadenas
        :param strings: Arreglo de cadenas
        :return: lista de cadena
        '''
        for i in range(1, len(strings),2):
            self.args.update({strings[i-1],strings[i]})

        for i in range(1, len(self.args)):
            print(self.args.values())

    def saveToFile(self,filename: str) -> bool:
        '''
        El objetivo de esta función es hacer una reconstrucción del archivo de parámetros
        de acuerdo con la estructura del archivo original, pero considerando los valores
        del mapa, además que es posible que se agreguen nuevas claves.

        :param filenName: Nuevo nombre del archivo
        :return: True si se pudo hacer la operación, en otro caso False
        '''
        io = ManejoArchivos()
        io.open_write_file(filename)
        key = ''
        tempo = []
        for linea in self.oLineas: #hacerlo para todas las lineas del archvivo

            if self.er_Keys.existER(linea): #si la linea es un key
                key = self.er_Keys.grupo(1)
                if self.args[key] in self.args: #y si el mapa contiene esa key entonces escribirla en al archivo
                    io.write_in_file(key + ('\t\t' if (len(key) < 8) else ('\t')) + self.args.get(key))
                    tempo.append(key)

            elif self.er_Comen.existER(linea):
                io.write_in_file(linea)

        #ahora a revisar cuales se van a agregar

        claves = set(self.args.keys())

        for clave in claves:
            if not tempo.__contains__(clave):
                io.write_in_file(clave + ('\t\t' if (len(key)) < 8 else ('\t')) + self.args.get(key))

        io.close_write_file()

        return True

    def addIfnotArgValue(self,arg: str,value: str) -> dict.get:
        '''
        Se agrega al arreglo el para Argumento Valor, si ya esta el argumento entonces
        no se agrega nada y se regresa el valor que estaba.

        :param arg: Parámetro a agregar
        :param value: Valor a agregar
        :return: Valor que corresponde a ese parámetro
        '''
        self.args.setdefault(arg, value)#inserta un elemento en el diccionario, si la clave existe no lo inserta
        '''if not self.args.has_key(arg):
            self.args[arg] = value'''

        return self.args.get(arg)

    def changeOrAdd(self,arg: str, value: str) -> dict.values:
        '''
        Si el argumento no está se agrega al diccionario con su par Clave-valor
        de lo contrario si el valor ya existe se actualiza su valor por value

        :param arg: Clave que se desea agregar
        :param value: Valor que se desea asociar a su clave
        :return:
        '''
        self.args.update({arg:value})

    #duda
    second = ''
    def addArgsFromFile(self,filename: str) -> bool:
        '''
        Lee los parámetros que se pasaron mediante un archivo
        :param filename: Nombre del archivo con los parámetros
        :return: True si se pudo cargar el archivo
        '''
        io = ManejoArchivos()
        texto = io.reads_text_file(filename)
        lineas = io.read_text_file(filename)
        #print(self.er_Keys.grupo(0))
        
        for i in range(len(lineas)):
            self.oLineas.append(lineas[i])
            if self.er_Keys.existER(lineas[i]): # entonces se agrega
                if (self.er_Keys.grupo(3) != None):
                    self.second = self.er_Keys.grupo(3)
                else:
                    self.second = self.er_Keys.grupo(4)
                    #print("second = ",self.second)
                self.args.update({self.er_Keys.grupo(1).strip(): self.second})

        return (True)

    def exist(self,label: str) -> bool:
        '''
        Revisa si existe la clave
        :param label: cadena que se valla a buscar si existe en el arreglo
        :return: True si existe la cadena label en el arreglo, Falso en otro caso
        '''
        return self.args.__contains__(label)

    def valueArgsAsString(self,label: str, default: str) -> str:
        '''
        Se utiliza para leer parámetros de tipo string, primero se busca la cadena en
        la lista de cadena y se regresa la siguiente cadena como string.

        :param label: párametro a leer
        :param default: valor por default que se regresa si no se encuentra label en el arreglo
        :return: el valor del parámetro como una cadena
        '''
        key = str(self.args.get(label)) if self.args.get(label) else default
        
        
        key = key.replace("@HOME@", str(Path.home()))
        key = key.replace("@WORK_PATH@", os.getcwd())
        #if key.startswith("@WORK_PATH@"):
        #    print ("entra if")
        #    key = self.getCurrentDir(key)

        return key.replace('\\', os.sep)

    def getCurrentDir(self, key:str) -> str:
        '''
        Reemplaza la cadena @WORK_PATH@ por la ruta desde donde se está llamando al script python

        :param key: llave dentro de los argumentos a ser reemplazada
        :return: llave reemplazada por la ruta pwd
        '''
        pattern = ManejoER(r"^@WORK_PATH@")
        result = pattern.existER(key)
        if result:
            print ("encontrado")
            print (pattern.grupo(0))
            print ("end ++++++++")
            key = key.replace(pattern.grupo(0), os.getcwd())
            
        return key


    def valueArgsAsInteger(self,label: str, default: int) -> int:
        '''
        Se utiliza para leer parámetros de tipo int, primero se busca la cadena en la lista de cadenas
        y se regresa la siguiente cadena como int.

        :param label: parametro a leer
        :param default: valor por default que se regresa si no se encuentra label en el arreglo
        :return: el valor del parametro como un entero (int)
        '''
        return int(self.args.get(label) if self.args.get(label) else default)

    def valueArgsAsFloat(self,label: str, default: float) -> float:
        '''
        Se utiliza para leer parámetros de tipo float, primero se busca la cadena en la lista de
        cadenas y se regresa la siguiente cadena como float.

        :param label: párametro a leer
        :param default: valor por default que se regresa si no se encuentra label en el arreglo
        :return: valor del parámetro como un real (float)
        '''
        return float(self.args.get(label) if self.args.get(label) else default)

    def valueArgsAsDouble(self,label: str, default: Decimal) -> Decimal:
        '''
        Se utiliza para leer parámetros de tipo double, primero se busca la cadena en la lista de
        cadenas y se regresa la siguiente cadena como double.

        :param label: párametro a leer
        :param default: valor por default que se regresa si no se encuentra label en el arreglo
        :return: valor del parámetro como un real (double)
        '''
        return Decimal(self.args.get(label) if self.args.get(label) else default)

    def valueArgsAsDecimal(self,label: str,default: Decimal) -> Decimal:
        '''
        Se utiliza para leer parámetros de tipo double, primero se busca la cadena en la lista de
        cadenas y se regresa la siguiente cadena como double.

        :param label: párametro a leer
        :param default: valor por default que se regresa si no se encuentra label en el arreglo
        :return: valor del parámetro como decimal
        '''
        return Decimal(self.args.get(label) if self.args.get(label) else default)

    def valueArgsAsBoolean(self,label: str, default: bool) -> bool:
        '''
        Se utiliza para leer parámetros de tipo bool, primero se busca la cadena en la lista de
        cadenas y se regresa la siguiente cadena como bool.

        :param label: párametro a leer
        :param default: valor por default que se regresa si no se encuentra label en el arreglo
        :return: valor del parámetro como un real (bool)
        '''
        salida = default

        if self.args.get(label):
            salida = eval(self.args.get(label).capitalize())#eval cadena a booleano, capitalize para usar True y False

        return salida

    def valueArgsAsDate(self,label: str, default: datetime) -> datetime:
        '''
        Se utiliza para leer parametros de tipo Calendar, primero se busca la cadena en la lista de
        cadenas y se regresa a siguiente cadena como Calendar. Puesto que en nuestro sistema el mes 1
        corresponde a ENERO entonces a nivel de codificación se le resta 1 al mes para coincidir con la
        fecha de Calendar.

        :param label: parámetro a leer
        :param defautl: valor por default en caso de no encontrarse
        :return:
        '''
        fecha = datetime
        format = ManejoER(r'(\\d{2,4})/(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])/([01]?[0-9]|[2][0-3])/([0-5][0-9])')
                #^(3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9])/(?:[0-9]{2})?[0-9]{2}$
        date = default if self.args.get(label) else self.args.get(label)
        print(date)

        if format.existER(date):
            fecha  = datetime.datetime(format.grupo(1),format.grupo(2),format.grupo(3),format.grupo(4),format.grupo(5))
        return fecha

    def valueArgsAsDate_get(self,label: str, default: datetime) -> datetime:
        '''
        Se utiliza para leer parametros de tipo Calendar, primero se busca la cadena en la lista de
        cadenas y se regresa a siguiente cadena como Calendar. Puesto que en nuestro sistema el mes 1
        corresponde a ENERO entonces a nivel de codificación se le resta 1 al mes para coincidir con la
        fecha de Calendar.

        :param label: parámetro a leer
        :param defautl: valor por default en caso de no encontrarse
        :return:
        '''
        fecha = datetime
        format = ManejoER(r'^(3[01]|[12][0-9]|0?[1-9])/(1[0-2]|0?[1-9])/(?:[0-9]{2})?[0-9]{2}$')
        match = re.search(format,label)
        if(match):
            fecha = datetime.datetime.strftime(match.group(), '%d-%m-%Y')
        else: fecha = default

        return fecha