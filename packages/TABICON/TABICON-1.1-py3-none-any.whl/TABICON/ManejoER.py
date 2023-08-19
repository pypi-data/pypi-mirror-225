#! usr/bin/env python 3
# coding=utf-8
import regex as re

__autor__ = 'Ulises García Calderón'

class ManejoER():

    def __init__(self,er: str):
        '''
        Crear un objeto con la expersión regular
        :param er: expresión regular
        '''
        self.p = re.compile(er) # creación del objeto patrón
        self.m = None

    def existER(self,line: str) -> bool:
        '''
        Este método evalua que la cadena line cumple con la expresion regular self.p

        :param line: linea de texto a evaluar
        :return: True si la cadena cumple con la expresión regular
        '''
        self.m = self.p.match(line)
        return True if self.m else False

    def grupo(self,grupo: int) -> str:
        #re.compile(regex).groups
        if(0<= grupo and grupo <= len(self.m.groups())):
            return self.m.group(grupo)
        else:
            return ''