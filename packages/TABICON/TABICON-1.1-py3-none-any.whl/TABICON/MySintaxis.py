#! usr/bin/env python 3
# coding=utf-8

from TABICON.MyListArgs import *
from TABICON.ManejoER import *

__autor = 'Ulises García Calderón'

class MySintaxis():
    '''
    Esta clase permite revisar el nivel léxico y sintactico de gramaticas del
    tipo TABICON. en el nivel léxico se revisa si las etquetas escritas por el usuario
    están de manera correcta, por ultimo se revisa si estan escritas de acuerdo con
    la gramatica para la aplicación
    '''
    param = MyListArgs
    tokens = []
    subtok = []
    reOrder = ''
    newPath = ''
    er = ManejoER('(-\\w+)(:[\\p{Graph}]+)*')
    er1 = ManejoER('-\\w+:([\\p{Graph}]+)')

    def __init__(self,sintaxis, parametros):
        '''
        Constructor donde se hace practicamente todo el trabajo, la estrategia seguida es:
        1.- En la sintaxis se separan los elementos de asociación y el operador de disyunción, por espacios en blanco
        2.- De acuerdo a los elementos léxicos de la sintaxis se revisan cuales utiliza el usuario y su formato
          Desde aqui es posible que ocurran errores
        3.- Cada etiqueta de los elementos utilizados por el usuario son escritos en una nueva cadena
        4.- En la sintaxis original se cambian [ por ( y ] por )?

        :param sintaxis: La gramatica tipo tabicon utilizada para la aplicación
        :param parametros: Objeto con el mapa de los parámetros y sus valores leeidos previamente
        '''
        self.error = ''
        self.param = parametros
        self.sintaxis = sintaxis.replace('(\\(|\\)|\\[|\\]|\\|)', '$1')
        self.sintaxis = sintaxis.replace('\\s+', ' ')
        self.tokens = sintaxis.strip().split(' ')
        self.newPath = sintaxis.strip().replace('\\[', '(').replace('\\]', ')?')
        self.newPath = self.newPath.replace(' ','\\\\s*')
        for token in self.tokens:
            #print 'if token: ', re.compile('(\\(|\\)|\\[|\\]|\\|)').match(token)
            if token.format('(\\(|\\)|\\[|\\]|\\|)'):
                continue
            elif self.er.existER(token): #self.er.existER(token):
                #print 'token[',token,'] Grupo(1)',self.er.grupo(1),']'
                if self.param.exist(self.er.grupo(1)):
                    self.reOrder = self.reOrder + ' ' + token.strip()
                    if self.er.grupo(2) != None:
                        self.error = self.revisarTipoDato(self.er.grupo(1),self.er.grupo(2))
                        if not self.error is '':
                            print('error')
            else:
                print('Se desconoce el elemento: [',token,']')

        self.reOrder = self.reOrder.strip()
        try:
            if not self.reOrder.format(self.newPath):
                print('OldPath [',self.sintaxis,']\n','NewPath [',self.newPath,']\nBuscar en ['+self.reOrder+']')
                print('OldPath {}, NewPath {} Buscar en {}',self.sintaxis)
                print('Error en los parametros')
                exit(0)
        except IOError:
            print('Error de sintaxis: el sistema reporta: ',IOError.strerror)
            exit(0)

    def revisarTipoDato(self,token,tipo):
        '''
        Revisa si se especificó un tipo de dato para el parámetro y si el del usuario cumple con dicho formato. También
        es posible definir un conjunto de valor que solo pueden ocurrir, esto sucede cuando hay dos o más tipos expresa-
        dos para esa etiqueta.

        :param token (string): Etiqueta correspondiente al tipo de dato
        :param tipo (string): Tipo de dato o conjunto de datos posibles separados por :
        :return: '' si no se detectó ningún error, de contrario el error encontrado
        '''
        while tipo.startswith(':'):
            tipo = tipo.replace('^:','')

        self.subtok = tipo.strip().split(':')

        if len(self.subtok) > 1:
            tipo = self.param.args.get(token)

            for tok in self.subtok:
                if tipo.__eq__(tok):
                    return ''

            return 'Para la etiqueta [',token,'] se encontró el valor [',tipo,'] y no concuerda ninguno de los tipos predefinidos ',tipo

        else:
            tipo = self.subtok[0]

        if tipo is 'str':
            if self.param.args.get(token) is '':
                return 'Se esparaba una cadena para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'

            elif tipo is 'int':
                if not self.param.args.get(token).lower().format('-?\\d+'):
                    return 'Se esperaba un entero para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'

            elif tipo is 'float':
                if self.param.valueArgsAsFloat(token,float)!= float:
                    return 'Se esperaba un flotante para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'

            elif tipo is 'bool':
                if not self.param.args.get(token).lower().format('true|false'):
                    return 'Se esperaba una fecha para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'

            elif tipo is 'date':
                if not self.param.args.get(token).lower().format('(\\d{2,4})/(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01])/([01]?[0-9]|[2][0-3])/([0-5]?[0-9])'):
                    return 'Se esperaba una fecha para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'

            elif tipo is 'char':
                if len(self.param.args.get(token)) != 1:
                    return 'Se esperaba un caracter para la etiqueta [',token,'] '

            elif tipo is 'hex':
                if not self.param.args.get(token).lower().format('[0-9a-f]+'):
                    return 'Se esperaba un hexadecimal para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'

            elif tipo is 'byte':
                if not self.param.args.get(token).lower().format('([0-1]?[0-9]?[0-9])|(2[0-4][0-9])|(25[0-5])'):
                    return 'Se esperaba un byte para la etiqueta [',token,'] pero se encontró [',self.param.args.get(token),']'
        else:
            return 'Tipo de dato desconocido: ',tipo

        return ''
