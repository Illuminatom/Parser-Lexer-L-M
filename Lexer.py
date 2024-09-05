import os

directions = ["left", "right", "backwards"]
orientations = ["north", "south", "east", "west"]
constants = ["size", "myx", "myy", "mychips", "myballons", "ballonshere", "chipshere", "roomforchips"]
commands = ["walk", "jump", "drop", "pick", "grab", "letgo", "pop"]
conditions = ["isblocked?", "isfacing?", "zero?"]
personalizedMacros = []
personalizedVariables = []

def crearListaPalabras(archivo: str):
    strLineas = ""
    listPalabras = []
    nombreTxt = archivo+".txt"
    file = open(nombreTxt)

    fileList = file.readlines()

    i= 0                                                 #
    while i <= len(fileList)-1:                          #
        if i < len(fileList)-1:                          # Toma todas las lineas del archivo y las une en
            strLineas += " "+fileList[i][:-1]            # una sola cadena de caracteres (String)
        else:                                            #
            strLineas += " "+fileList[i]                 #
        i+=1                                             #
        

    listPalabras = strLineas.split()                     # Toma la cadena de caracteres anterior y la convierte
                                                         # en una lista cuyos elementos son todas las palabras
                                                         # omitiendo los espacios en blanco y las tabulaciones
    
    file.close()
    
    return listPalabras

prueba = crearListaPalabras("files/prueba")
print(prueba)

