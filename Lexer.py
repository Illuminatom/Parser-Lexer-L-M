import os
import re

directions:list[str] = ["left", "right"]
moveDirections:list[str] = ["forward", "backwards"]
orientations:list[str] = ["north", "south", "east", "west"]
constants:list[str] = ["size", "myx", "myy", "mychips", "myballons", "balloonshere", "chipshere", "roomforchips"]
commands:list[str] = ["walk", "jump", "drop", "pick", "grab", "letgo", "pop"]
noChanges:list[str] = ["exec", "if", "fi", "else", "then", "do", "od", "rep", "times", "per", "nop", "moves", "not",
                        "isblocked?", "isfacing?", "zero?", "turntomy", "turntothe", "safeexe", "front", "back"]
symbols:list[str] = ["(", ")", "{", "}", ",", ";","="]
personalizedMacros:list[str] = []
personalizedVariables:list[str] = []
def revisar_corchetes(str_palabras: str,index:int) :
    str_palabras=" ".join(str_palabras[index:])
    #print(index)
    #print(str_palabras)
    cerrado=False
    open_counter=0
    close_counter=0
    indice_open=0
    indice_close=0
    i=0
    while (cerrado==False) and (i<len(str_palabras)):
        token=str_palabras[i]
        if (open_counter==close_counter) and (close_counter>0):
            cerrado=True
            indice_close=i-1
        if token=="{":
            open_counter+=1
            if open_counter==1:
                indice_open=i
        if token=="}":
            close_counter+=1
        i+=1
    if cerrado==True:
        rta=str_palabras[indice_open:indice_close+1]
        #print(rta) 
        return rta
    else:
        rta=str_palabras[indice_open:]
        #print(rta) 
        return rta
def extraer_parametros_turntomy(cadena: str):
    # Expresión regular para extraer todos los parámetros de turntomy
    resultados = re.findall(r"turntomy\((.*?)\)", cadena)
    
    # Si hay resultados, retornarlos; de lo contrario, retornar un mensaje
    if resultados:
        return resultados
    else:
        return "No se encontraron funciones turntomy."
def extraer_parametros_turntothe(cadena: str):
    # Expresión regular para extraer todos los parámetros de turntomy
    resultados = re.findall(r"turntothe\((.*?)\)", cadena)
    
    # Si hay resultados, retornarlos; de lo contrario, retornar un mensaje
    if resultados:
        return resultados
    else:
        return "No se encontraron funciones turntothe."
def procesarParametros(parametros: str,lista_palabras,index) -> tuple[list[str], str]:
    macro=revisar_corchetes(lista_palabras,index)
    macro_sin_espacios = macro.replace(" ", "")
    parametros_d=[]
    parametros_o=[]
    if "turntomy" in macro_sin_espacios:
        parametros_d=extraer_parametros_turntomy(macro_sin_espacios)
        #print(parametros_d)
        
    if "turntothe" in macro_sin_espacios:
        parametros_o=extraer_parametros_turntothe(macro_sin_espacios)
        #print(parametros_o)
        
    #print(macro_sin_espacios)
    #print(macro)
    # Verificar que los paréntesis están bien colocados
    # Verificar que los paréntesis están bien colocados
    if parametros.startswith("(") and parametros.endswith(")"):
        # Remover los paréntesis externos y separar los parámetros por comas
        listaParametros = parametros[1:-1].split(",")
        
        # Limpiar espacios en blanco alrededor de los parámetros
        listaParametros = [p.strip() for p in listaParametros]
        
        # Retornar la lista de parámetros junto con los parámetros 'd' y 'o'
        return listaParametros, parametros_o, parametros_d
    else:
        raise

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
  

def convertirATokens(listaPalabras: list[str],parametros_macros=[],param_O=[],param_D=[]) -> list[str]: # Funcion que convierte una lista de palabras en una lista de tokens

    listTokens:list[str] = []                           # Lista de tokens que se va a retornar

    i:int = 0;                                           # Variable de control para el while

    while(i < len(listaPalabras)):                       # Mientras no se haya recorrido toda la lista de palabras
        palabra:str = listaPalabras[i]                   # Se toma la palabra en la posicion i y se le asigna un token dependiendo de su tipo
        
        #print("la palabra actual es:-"+palabra+"-")
        #print(param_O)
        if (palabra in noChanges) or (palabra in symbols): # Si la palabra es un token que no cambia se agrega a la lista de tokens tal cual
            listTokens.append(palabra)  
            #print("se agrega el token:",palabra)
        elif  (palabra in param_O):
            listTokens.append("O") 

        elif  (palabra in param_D):
            listTokens.append("D") 
                   
        elif (palabra in constants) or (isNumber(palabra)) or (palabra in parametros_macros):                    
            listTokens.append("n")                       # Si la palabra es una constante o un numero se agrega un token n
            #print("se agrega el token:","n")  
        elif (palabra in personalizedVariables):         # Si la palabra es un numero
            listTokens.append("variable")
        elif (palabra in commands):                      # Si la palabra es un comando
            listTokens.append("command")
            #print("se agrega el token:","command")  
        elif (palabra in directions):                    # Si la palabra es una direccion
            listTokens.append("D")
            #print("se agrega el token:","D")  
        elif (palabra in moveDirections):                # Si la palabra es una direccion de movimiento
            listTokens.append("D2")
            #print("se agrega el token:","D2")  
        elif (palabra in orientations):                  # Si la palabra es una orientacion
            listTokens.append("O")
            #print("se agrega el token:","O")  
        elif (palabra in personalizedMacros):            # Si la palabra es un macro anteriormente definido
           listTokens.append(palabra)

        elif (palabra == "new"):                         # Si la palabra es NEW se debe ver si se esta definiendo una nueva variable o un nuevo macro
            listTokens.append("new")
            if (listaPalabras[i+1] == "var") and (listaPalabras[i+2].isalpha() or listaPalabras[i+2].isalnum()):
                personalizedVariables.append(listaPalabras[i+2])
                i+=1
            elif (listaPalabras[i+1] == "var") and not(listaPalabras[i+2].isalpha() or listaPalabras[i+2].isalnum()):
                nuevaVar:str = cleanPalabra(listaPalabras[i+2])[0] 
                personalizedVariables.append(nuevaVar)
                i+=1
            elif (listaPalabras[i+1] == "macro") and (listaPalabras[i+2].isalpha() or listaPalabras[i+2].isalnum()):
                personalizedMacros.append(listaPalabras[i+2])
                listTokens.append("macro")
                if listaPalabras[i+3] != "()":
                    #print(listaPalabras[i+3]+listaPalabras[i+4])
                    listaParametros,param_d,param_o=procesarParametros(listaPalabras[i+3]+listaPalabras[i+4],listaPalabras,i+4)
                    parametros_macros=parametros_macros+listaParametros
                    param_D=param_D+param_d
                    param_O=param_O+param_o
                    #print("yesid",listaParametros,parametros_macros)
                i+=1 
            elif (listaPalabras[i+1] == "macro") and not(listaPalabras[i+2].isalpha() or listaPalabras[i+2].isalnum()):
                nuevoMacro:str = cleanPalabra(listaPalabras[i+2])[0] 
                listTokens.append("macro")
                personalizedMacros.append(nuevoMacro)
                i+=1

        elif(palabra == ""):
            pass
        else:                                                # Si en esa posicion no se encontro ninguno de los tokens anteriores
            listaPequeña:list[str] = cleanPalabra(palabra)     # Se limpia la palabra porque pueden ser simbolos mezclados con palabras o otros simbolos ej: "walk(1)"
            if listaPequeña != [palabra]:  
                #print("lista pequenia",listaPequeña)
                tokens = convertirATokens(listaPequeña,parametros_macros,param_O,param_D)  # Se convierte la palabra limpia en tokens
                listTokens.extend(tokens)                # Se agregan los tokens a la lista de tokens
                #print(tokens, " - -- - ",palabra)
            else:
                listTokens.append("ERROR")  # Si no se encontro ningun token se agrega un error a la lista        
                print("Se agregó un error en la palabra:",palabra)  
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

#print(" ".join(tokens))
