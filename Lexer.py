import os

directions:list[str] = ["left", "right", "back"]
moveDirections:list[str] = ["forward", "backwards"]
orientations:list[str] = ["north", "south", "east", "west"]
constants:list[str] = ["size", "myx", "myy", "mychips", "myballons", "balloonshere", "chipshere", "roomforchips"]
commands:list[str] = ["walk", "jump", "drop", "pick", "grab", "letgo", "pop"]
noChanges:list[str] = ["exec", "if", "fi", "else", "then", "do", "od", "rep", "times", "nop", "moves", "not",
                        "isblocked?", "isfacing?", "zero?", "turntomy", "turntothe", "safeexe"]
symbols:list[str] = ["(", ")", "{", "}", ",", ";", ":","="]
personalizedMacros:list[str] = []
personalizedVariables:list[str] = []

def crearListaPalabras(archivo: str) -> list[str]:
    strLineas = ""
    listPalabras = []
    nombreTxt = archivo+".txt"
    file = open(nombreTxt)

    fileList = file.readlines()

    i= 0                                                 #
    while i <= len(fileList)-1:                          #
        if i < len(fileList)-1:                          # Toma todas las lineas del archivo y las une en
            strLineas += " "+str.lower(fileList[i][:-1]) # una sola cadena de caracteres (String)
        else:                                            #
            strLineas += " "+str.lower(fileList[i])      #
        i+=1                                             #
        

    listPalabras = strLineas.split()                     # Toma la cadena de caracteres anterior y la convierte
                                                         # en una lista cuyos elementos son todas las palabras
                                                         # omitiendo los espacios en blanco y las tabulaciones
    
    file.close()
    
    return listPalabras

#print(crearListaPalabras("files/prueba"))


def isNumber(palabra: str) -> bool:
    try:
        int(palabra)
        return True
    except ValueError:
        return False
    

def cleanPalabra(palabra: str) -> list[str]: # Funcion que separa las palabras de los simbolos
    listPalabras:list[str] = []
    z:int = 0
    for i in range(len(palabra)):
        if palabra[i] in symbols:            
            if z < i:  # Evitar añadir partes vacías
                listPalabras.append(palabra[z:i])
            listPalabras.append(palabra[i])
            z = i+1
    listPalabras.append(palabra[z:])
    
    return listPalabras


def convertirATokens(listaPalabras: list[str]) -> list[str]: # Funcion que convierte una lista de palabras en una lista de tokens
    listTokens:list[str] = []                           # Lista de tokens que se va a retornar

    i:int = 0;                                           # Variable de control para el while

    while(i < len(listaPalabras)):                       # Mientras no se haya recorrido toda la lista de palabras
        palabra:str = listaPalabras[i]                   # Se toma la palabra en la posicion i y se le asigna un token dependiendo de su tipo
        if (palabra in noChanges) or (palabra in symbols): # Si la palabra es un token que no cambia se agrega a la lista de tokens tal cual
            listTokens.append(palabra)                   
        elif (palabra in constants):                     # Si la palabra es una constante o una variable
            listTokens.append("n")
        elif (isNumber(palabra)):                        # Si la palabra es un numero
            listTokens.append("#")
        elif (palabra in commands):                      # Si la palabra es un comando
            listTokens.append("command")
        elif (palabra in directions):                    # Si la palabra es una direccion
            listTokens.append("D")
        elif (palabra in moveDirections):                # Si la palabra es una direccion de movimiento
            listTokens.append("D2")
        elif (palabra in orientations):                  # Si la palabra es una orientacion
            listTokens.append("O")
        elif (palabra in personalizedVariables):         # Si la palabra es una variable anteriormente definida
            listTokens.append("var".format(palabra))
        elif (palabra in personalizedMacros):            # Si la palabra es un macro anteriormente definido
            listTokens.append("macro({})".format(palabra))

        elif (palabra == "new"):                         # Si la palabra es NEW se debe ver si se esta definiendo una nueva variable o un nuevo macro
            if (listaPalabras[i+1] == "var") and (listaPalabras[i+2].isalpha()):
                personalizedVariables.append(listaPalabras[i+2])
                i+=1
            elif (listaPalabras[i+1] == "var") and not(listaPalabras[i+2].isalpha()):
                nuevaVar:str = cleanPalabra(listaPalabras[i+2])[0] 
                personalizedVariables.append(nuevaVar)
                i+=1
            elif (listaPalabras[i+1] == "macro") and (listaPalabras[i+2].isalpha()):
                personalizedMacros.append(listaPalabras[i+2])
                i+=1 
            elif (listaPalabras[i+1] == "macro") and not(listaPalabras[i+2].isalpha()):
                nuevaVar:str = cleanPalabra(listaPalabras[i+2])[0] 
                personalizedVariables.append(nuevaVar)
                i+=1

        elif(palabra == ""):
            pass
        else:                                                # Si en esa posicion no se encontro ninguno de los tokens anteriores
            listaPequeña:list[str] = cleanPalabra(palabra)     # Se limpia la palabra porque pueden ser simbolos mezclados con palabras o otros simbolos ej: "walk(1)"
            if listaPequeña != [palabra]:  
                tokens = convertirATokens(listaPequeña)  # Se convierte la palabra limpia en tokens
                listTokens.extend(tokens)                # Se agregan los tokens a la lista de tokens
                print(tokens, " - -- - ",palabra)
            else:
                listTokens.append("ERROR({})".format(palabra))  # Si no se encontro ningun token se agrega un error a la lista        

        i+=1                                             # Se aumenta el contador para pasar a la siguiente palabra
    
    return listTokens

convertirATokens(crearListaPalabras("files/prueba"))
# Generar archivos con los resultados
lista_palabras = crearListaPalabras("files/prueba")
with open("files/lista_palabras.txt", "w") as file:
    file.write("\n".join(lista_palabras))

tokens = convertirATokens(lista_palabras)
with open("files/tokens.txt", "w") as file:
    file.write(" ".join(tokens))

print(" ".join(tokens))