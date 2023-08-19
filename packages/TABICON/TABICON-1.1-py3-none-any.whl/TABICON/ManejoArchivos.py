#! usr/bin/env python 3
# coding=utf-8

import codecs
import os
import shutil
import numpy as np
import regex

__autor__ = 'Ulises García Calderón'

class ManejoArchivos():
    '''
     Proporciona metodos para el manejo de archivos de texto tanto para lectura como
     para escritura, tambien se proporcionan metodos para el manejo de carpetas y de
     sus archivos.

     '''

    def __init__(self):
        '''Constructor de la clase'''
        self.filename = ''
        self.contenido = ''
        self.charset = ''

    def write_file_add(self, filename: str, contenido: list) -> bool:
        '''
        Crea un archivo de texto en el cual se escribe un arreglo de cadenas al final del
        archivo, si el archivo no existe lo crea.

        :param filename: Nombre del archivo
        :param contenido: Arreglo de cadenas a Agregar
        :return: True si se pudo crear el archivo junto con su contenido
        '''
        with open(filename, 'a+') as archivo:
            for i in contenido:
                archivo.write(i + '\n')
            return True

    def write_string_file_add(self, filename: str, contenido: str) -> bool:
        '''
        Crea un archivo de texto en el cual se escribe una solo cadena al final del mismo,
        si el archivo no existe lo crea.

        :param filename: Nombre del archivo
        :param contenido: Arreglo de lineas a escribir
        :return: True si se pudo crear el archivo junto con su contenido
        '''
        with open(filename, 'a+') as archivo:
            archivo.write('\n' + contenido)
            return True

    def get_filename(self, path: str) -> str:
        '''
        Obtienen solo el nombre del archivo de la ruta especificada, obtiene el nombre del archivo, es decir,
        corta la ruta y devuelve el nombre del archivo, sino existe no regresa nada.

        :param path: Ruta de donde se va a extraer el archivo
        :return: Cadena con el nombre del archivo y su extension
        '''
        archive = os.path.basename(path)
        return archive

    def until_crear_carpetas(self, path: str) -> bool:
        '''
        Crea una carpeta y no avanza hasta que crea la carpeta.

        :param path: Ruta de donde se va a crear la carpeta
        :return: True cuando halla creado la carpeta
        '''
        while not os.path.exists(path):
            os.makedirs(path)
        return True

    def crear_carpetas(self, path: str) -> bool:
        '''
        Este método crear un conjunto de carpetas, dada una cadena separada por /
        :param path:
        :return:
        '''
        return False if os.makedirs(path) else True

    def existe_carpeta_archivo(self, path: str) -> bool:
        '''
        Permite saber si existe ya sea un archivo o una ruta especificada.

        :param path: Ruta o archivo del que se desea saber si existe
        :return: True si existe el path como ruta o como archivo.
        '''
        return False if os.path.exists(path) else True

    def rename_path(self, oldname: str, newname: str) -> bool:
        '''
        Renombra una carpeta con un nuevo nombre.

        :param oldname: Nombre con la carpea origen
        :param newname: Nombre que se le va asignar a la carpeta origen
        :return: True si se pudo llevar con exito la operación
        '''
        return False if os.rename(oldname,newname) else True

    def add_to_path(self, root: str, file_path: str) -> str:
        '''
        Agrega un nombre de una carpeta o de un archivo a una ruta.

        :param Root:
        :param file_path:
        :return: La ruta root a la que se el agrego el archivo o ruta filepath
        '''
        return root + file_path if root.endswith(os.path.sep) else root + os.path.sep + file_path

    def copy_file(self, fromfilename: str, topathName: str) -> [str,OSError]:
        '''
        Se encarga de copiar un archivo a una ruta especificada.

        :param fromfilename: Archivo fuente a copiar
        :param topathName: Ruta donde se va a copiar el archivo/puede incluir nuevo nombre
        :return: True si se copio el archivo
        '''
        if os.path.exists(fromfilename):
            if os.path.isfile(fromfilename):
                shutil.copy(fromfilename, topathName)
                return True
            elif os.path.isdir:
                return 'el archivo especificado es una ruta,no se puede copiar', IOError(fromfilename)
        else:
            return 'No existe el archivo: ' + fromfilename

    def copy_files(self, fromfilename: str, topathName:str) -> bool:  ###falta
        '''
        Copia la lista de arhivos (especificados con su ruta absoluta) a la ruta topathName.

        :param fromfilename: Arreglo con la lista de archivo para copiar(especificados con su ruta absoluta).
        :param topathName: Rute destino donde se va a copiar los archivos.
        :return: True si se copiaron todos los archivos.
        '''
        if os.path.exists(fromfilename):
            shutil.copytree(fromfilename, topathName)
            return True
        else:
            return False

    def until_del_carpeta(self, dir: str) -> bool:
        '''
        Cuando se llama esta funcion el sistema no avanza hasta que se borra la carpeta.

        :param dir: dirección de la carpeta a borrar
        :return: True si pudo borrar la carpeta

        *Solo borra carpetas vacias
        '''
        return False if os.rmdir(dir) else True

    def del_carpeta(self, dir: str) -> bool:
        '''
        Esta funcion borra un directorio y todos sus archivos y subcarpetas, sin confirmar.

        :param dir: directorio que se quiere borrar
        :return: True si se borró la carpeta dir, en caso contrario False
        '''
        return False if shutil.rmtree(dir) else True

    def list_carpetas(self, dir: str) -> list:
        '''
        Permite obtener la lista de carpetas que hay en un subdirectorio

        :param dir(str): Nombre del directorio donde se van a buscar las carpetas
        :return: lista de carpetas
        '''
        dir, subdirs, archivos = next(os.walk(dir))
        return subdirs

    def list_files(self, dir: str, extension: str) -> list:
        '''
        Funcion que recibe el nombre de un directorio y la extension del archivo y regresa la lista
        con los nombres de los archivos que estan en esa carpeta.

        :param dir: Nombre del directorio donde se va a buscar los archivos
        :param extension: extension del archivo empezando con '.' ejemplo .bin''
        :return: Lista de cadenas con los nombres de archivos que hay dentro
        '''
        return [x for x in os.listdir(dir) if x.endswith(extension)]

    def list_files_abs(self, dir: str, extension: str) -> list:
        '''
        Funcion que recibe el nombre de un directorio y la extension del archivo y regresa la lista con
        los nombres (y su ruta absoluta) de los archivos que estan en esa carpeta indican la ubicacion
        de los archivos o directorios respecto a la unidad de disco en el cual se almacenan los datos, y se
        define por el  conjunto de directorios  que tenemos que atravesar hasta llegar a una determinada capa o directorio.

        :param dir: Nombre del directorio donde se va a buscar los archivos
        :param extension: Extensión del archivo empezando con '.', ejemplo .bin''
        :return: Lista de cadenas con los nombres de archivos que hay dentro
        '''
        rx = regex.compile(extension)
        paths = []
        for path, dnames, fnames in os.walk(dir):
            paths.extend([os.path.join(path, x) for x in fnames if rx.search(x)])
        return paths

    def open_read_file(self, filename: str, charset: str) -> open:
        '''
        Abre un archivo para lectura considerando la codificacion charset, pero no lee nada, solo deja abierto
        el buffer de entrada para que se leea el contenido más adelante.

        :param filename: Nombre del archivo
        :param charset: Codificación del archivo
        :return: Objeto file abierto

        ver   #Read_NextLine_NoNull(j)
        '''
        archivo = codecs.open(filename, 'r', charset)
        return archivo

    def read_nextline_nonull(self) -> open:
        '''
        Una vez abierto un archivo para lectura con Open_Read_file se puede leer la siguiente linea
        de texto del archivo que no esta vacia, de lo contrario se regresa null.

        :return: Lineas de texto leidas
        :self.Open_Read_file(self.filename,self.charset): Función de lectura de lectura del cual se va a leer el archivo

        ver    #Open_Read_file(self.filename, self.charset)
        '''
        return self.open_read_file(self.filename, self.charset).read()

    def close_read_file(self) -> open:
        '''
        Cierra el archivo que se abrio previamente con Open_Read_file

        :param Open_Read_file:
        :return: True si se pudo cerrar el archivo, False en otro caso

        ver #Open_Read_file(java.lang.String, java.lang.String)
        ver #Read_NextLine_NoNull(java.io.BufferedReader)
        '''
        if not self.open_read_file(self.filename, self.charset).closed:
            self.open_read_file(self.filename, self.charset).close()
            return True
        else:
            return False

    def read_text_file(self, filename: str) -> list:
        '''
        Lee un archivo y regresa una arreglo con las lineas de ese archivo.

        :param filename: Este parametro se refiere al nombre del archivo que se desea abrir para lectura
        :return: Regresa un arreglo con las lineas del archivo leido
        '''
        lista = []
        with open(filename, 'r') as archivo:
            for linea in archivo:
                lista.append(linea)
        return lista

    def read_text_file_nonull(self, filename: str) -> list:
        '''
        Lee un archivo de texto y regresa una arreglo con las lineas de ese 
        archivo, pero filtra las lineas que solo estan en blanco (es decir que 
        no tienen algo).
        :param filename: Este parametro se refiere al nombre del archivo que 
        se desea abrir para lectura
        :return: Regresa un arreglo con las lineas del archivo leido
        '''
        lista = []
        with open(filename, 'r') as archivo:
            for linea in archivo.readlines():
                if linea.strip()!='':
                    lista.append(linea)
        return lista

    def read_text_file_charset(self, filename: str, charset: str) -> list:  # le cambie el nombre(agregue _charset)
        '''
        Lee un archivo de texto con una codificación dada y regresa una arreglo con las lineas de ese archivo, pero filtra las
        lineas que solo estan en blanco (es decir que no tienen algo).

        :param filename: Este parametro se refiere al nombre del archivo que se desea abrir para lectura
        :return: Regresa un arreglo con las lineas del archivo leido

        :param filename: Nombre del archivo que se desea abrir
        :param charset: Tipo de codificación de apertura del archivo
        :return: regresa un arreglo con las lineas del archivo leido
        '''
        lista = []
        with codecs.open(filename, 'r', charset) as archivo:
            for linea in archivo:
                lista.append(linea)
        return lista

    def read_text_file_nonull_charset(self, filename: str, charset: str) -> list:  # le cambie el nombre(agregue _charset)
        '''
        Lee un archivo de texto omitiendo aquellas lineas que no contienen nada de acuerdo a la
        codificacion especificada y regresa todo el contenido en un arreglo de cadenas.

        :param filename: Nombre del archivo a abrir
        :param charset: Codificación de lectura de archivo
        :return: Arreglo de lineas omitiendo las vacias
        '''
        lista = []
        with codecs.open(filename, 'r', charset) as archivo:
            for line in archivo:
                lista.append(line)
        return lista

    def get_lines_nonull(self, filename: str, charset: str) -> int:
        '''
        Obtiene el numero de lineas de un archivo de texto omitiendo aquellas lineas que no
        contienen nada de acuerdo a la codificacion especificada.

        :param filename: Nombre del archivo a abrir
        :param charset: Codificación de lectura del archivo
        :return: Numero de lineas del archivo filename, omitiendo las vacias
        '''
        l = 0
        with codecs.open(filename, 'r', charset) as archivo:
            for line in archivo:
                line = line.rstrip('\n')  # elimina los saltos de linea
                l += 1
            return l

    def read_nlines_nonull(self, filename: str, nlines: int, charset: str) -> list:
        '''
        Lee un NLineas de texto omitiendo aquellas lineas que no contienen nada de acuerdo a la codificacion
        especificada y regresa el contenido en un arreglo de cadenas.
        Por lo tanto, el arreglo de lineas resultante puede ser menor a NLines Esta funcion tiene como objetivo
        disminuir el numero de memoria necesaria cuando solo se requieren leer las primeras lineas.

        :param filename: Nombre del archivo a abrir
        :param Nlines: Numero de lineas que se desean leer
        :param charset: Codificación de la lectura del archivo
        :return: Arreglo de linea omitiendo las vacias
        '''

        lista = []
        with codecs.open(filename, 'r', charset) as archivo:
            for l, line in enumerate(archivo):
                if l < nlines:
                    lista.append(line)
            return lista

    def reads_text_file(self, filename: str) -> list:
        '''
        Lee un archivo de texto y regresa su salida en una sola linea

        :param filename: Este parametro se refiere al nombre del archivo que se desea abrir para lectura
        :return: Regresa un arreglo con las lineas del archivo leido
        '''
        lista = []
        with open(filename, 'r') as archivo:
            lista.append(archivo.readlines())
        return lista

    def write_file(self, filename: str, contenido: list) -> open:
        '''
        Crea un archivo de texto en el cual se escribe un arreglo de cadenas.

        :param filename: Nombre del archivo
        :param contenido: Arreglo de lineas a escribir
        :return: True si se pudo crear el archivo junto con su contenido
        '''
        with open(filename, 'w') as archivo:
            for line in contenido:
                archivo.write(line + '\n')

    def write_file_charset(self, filename: str, contenido: list, charset: str):
        '''
        Crea un archivo de texto en el cual se escribe un arreglo de cadenas.

        :param filename: Nombre del archivo
        :param contenido: Areglo de lineas a escribir
        :param charset: Codificacion de Apertura del archivo
        :return: Si pudo crear el archivo junto con su contenido
        '''
        with codecs.open(filename, 'w', charset) as archivo:
            archivo.write(contenido)

    def read_text_file_fast(self, filename: str, charset: str) -> list:
        '''
        Lee rápidamente las líneas de un archivo de texto en la codificación especificada.

        :param filename: Nombre del archivo
        :param charset: Codificación de lectura
        :return: Arreglo de cadenas con el contenido del archivo
        '''
        lista = []
        with codecs.open(filename, 'r', charset) as archivo:
            lista.append(archivo.readlines())
        return lista

    def read_text_file_fast_list(self, filename: str, charset: str) -> str:
        '''
         Lee rápidamente un archivo de texto y regresa su salida en una sola línea en codificación charset

        :param filename: Este parámetro se refiere al nombre del archivo que se desea abrir para lectura
        :param charset: Codificación de lectura
        :return: Regresa una cadena con el contenido
        '''
        with codecs.open(filename, 'r', charset) as archivo:
            contenido = archivo.read()
        return contenido

    def write_file_cadena(self, filename: str, contenido: list) -> bool:
        '''
        Crea un archivo de texto en el cual se escribe el contenido de la cadena

        :param filename: Nombre del archivo
        :param contenido: Arreglo de cadenas a escribir
        :return: True si pudo crear el archivo junto con su contenido
        '''
        with open(filename, 'w') as archivo:
            for linea in contenido:
                archivo.write(linea + '\n')

        return True

    def write_string_file(self, filename: str, cadena: str) -> bool:
        '''
        Crea un archivo de texto en el cual se escribe el contenido de la cadena
        :param filename: Nombre del archivo
        :param cadena: Cadena a escribir
        :return: True si pudo crear el archivo junto con su contenido
        '''
        with open(filename, 'w') as archivo:
            archivo.write(cadena + '\n')
        return True

    def write_string_file_charset(self, filename: str, charset: str, contenido: str) -> bool:
        '''
        Crea un archivo de texto de acuerdo a la codificación indicada en el cual se
        escribe el contenido de la cadena.

        :param filename: Nombre del archivo
        :param contenido: cadena a escribir
        :param charset: Codificación del archivo
        :return: True si se pudo crear el archivo junto con su contenido
        '''
        with codecs.open(filename, 'w', charset) as archivo:
            archivo.write(contenido)
        return True

    def open_write_file(self, filename: str) -> open:
        '''
        Abre un archivo para escritura pero no escribe nada, solo deja abierto el buffer de salida.
        Esta función escribe los datos de acuerdo a la codificación predefinida en el sistema. Si
        se desea controlar la codificación de salida hay que utilizar:
        Open_Read_file(filename,charset)

        :param filename: Nombre del archivo
        :return: False si no se pudo abrir el archivo

        ver #Open_Write_file_charset(filename,charset)
        ver #Write_in_file(Open_Write_file)
        ver #Close_Write_file(Open_Write_file)
        '''
        self.filename = filename
        return open(filename, 'a')

    def open_write_file_charset(self, filename: str, charset: str) -> open:
        '''
        Abre un archivo para escritura considerando la codificación charset, pero no
        escribe nada, solo deja abierto el buffer de salida para que se escriba el
        contenido más adelante.

        :param filename: Nombre del archivo
        :param charset: Codificación del archivo
        :return: Objeto del archivo abierto

        ver: Write_in_file(sel,file,Linea)
        ver: Close_Write_file(file)
        '''
        self.filename = filename
        archivo = codecs.open(self.filename, 'a', charset)
        return archivo

    def write_in_file(self, linea: str) -> open:
        '''
        Una vez abierto un archivo para escritura con Open_Write_file se puede agregar
        lineas de texto al archivo.

        :param file: Objeto del archivo abierto
        :param Linea: Texto que se va agregando al
        :return: True si pudo agregar la linea de texto, False en caso contrario

        ver: #Open_Write_file()
        ver: #Close_Write_file()
        '''
        return self.open_write_file(self.filename).write(linea + '\n')

    def close_write_file_charset(self) -> bool:
        '''

        :return: Tru si se pudo cerrar el archivo, False en otro caso
        ver: Open_Write_file()
        ver: Write_In_file()
        '''
        if not self.open_write_file_charset(self.filename, self.charset).closed:
            self.open_write_file_charset(self.filename, self.charset).close()
            return True
        else:
            return False
    def close_write_file(self) -> bool:
        '''
        :return: True si se pudo cerrar el archivo, False en otro caso
        ver: Open_Write_file()
        ver: Write_In_file()
        '''
        if not self.open_write_file(self.filename).closed:
            self.open_write_file(self.filename).close()
            return True
        else:
            return False


    def readfloatofstrasint32bits(self, data: list) -> np.array:
        '''
         Lee una cadena compuesta de numeros flotantes los cuales son convertidos
         a una representación entera y posteriormente a 32 bits. Si el arreglo de entrada
         tiene n numeros flotantes, el arreglo resultante tendría una longitud de n*32

         :param Data: Cadena compuesta de números flotantes
         :return:  Arreglo de valores enteros con los valores leídos del archivo filename
        '''
        arreglo = np.array([data]).astype(np.int32)
        return arreglo

    def readint32bitsasfloatofstr(self, data: list, split: str.split):  # duda
        '''
        Lee un vector de bits que representan un vector de flotantes y transforma su salida en
        una cadena separados por Split.

        :param Data: vector de bits
        :param Split:
        :return: cadena de valores flotantes
        '''
        cadena = split.join(str(i) for i in data)
        return cadena

    def readint32bitsasfloat(self, data: list) -> list:  # duda: split por default?
        '''
        Lee un vector de bits que representan un vector de flotantes y transforma su salida en
        una cadena separados por Split.

        :param Data: vector de bits
        :return: vector de valores flotante
        '''
        vector = []
        cadena = ','.join(str(i) for i in data)
        vector.append(cadena)
        return vector

    def readdoublestringasint64bits(self, data: str, split: str.split) -> np.array:
        '''
        Lee una cadena compuesta de numeros doubles los cuales son convertidos
        a una representación entera y posteriormente a 64 bits. Si el arreglo de entrada
        tiene n numeros doubles, el arreglo resultante tendrá una longitud de n*64.

        :param data: Cadena con los números dobles separados por Split
        :param split: Caracter que divide los datos dobles
        :return: Arreglo de valores binarios que representan la cadena Data
        '''
        lista = []
        array = data.split(split)
        for i in array:
            lista.append(float(i))
        ptr = np.array([lista]).astype(np.int64)
        return ptr


    def readint64bitsasdoublestr(self, data: list, split: str.split) -> list:
        '''
        Lee un arreglo de bits ( contenido es un arreglo de enteros)los cuales
        son convertidos a su representación de dobles y son regresados en una cadena

        :param data: Arreglo de bits
        :param split: caracter divisor de los datos salida
        :return: Una cadena con la representación de los datos dobles
        '''
        lista = []
        for i in data:
            lista.append(float(i))

        cadena = str(lista).split(split)

        return cadena

    def readint64bitsasdouble(self, data: str):
        '''
        Lee un arreglo binario compuesto de numeros doubles los cuales son convertidos
        a una representación entera y posteriormente a 64 bits. Si el arreglo de entrada
        tiene n numeros doubles, el arreglo resultante tendrá una longitud de n*64.

        :param filename: Nombre del archivo
        :return: Un arreglo de valores enteros con los valores leídos del archivo filename
        '''
        lista = []
        #array = data.split(split)
        for i in data:
            lista.append(int(i))
        arreglo = np.array([lista]).astype(np.int64)
        return arreglo