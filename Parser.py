macros = []
variables = {}

import os
import re
import Lexer

def leerTokens(archivo: str) -> list[str]:
    tokens: list[str] = Lexer.convertirATokens(Lexer.crearListaPalabras(archivo))
   
    return tokens

def revisar_corchetes(str_tokens: str,index:int) -> bool:
    cerrado=False
    open_counter=0
    close_counter=0
    indice_open=0
    indice_close=0
    while (cerrado==False) and (index<len(str_tokens)):
        token=str_tokens[index]
        if (open_counter==close_counter) and (close_counter>0):
            cerrado=True
            indice_close=index-1
        if token=="{":
            open_counter+=1
            if open_counter==1:
                indice_open=index
        if token=="}":
            close_counter+=1
        index+=1
    if cerrado==True:
        print(str_tokens[indice_open:indice_close+1]) 
    else:
        print(str_tokens[indice_open:])
    return True
def revisar_definicion(tipo:str, cadena:str,index:int):
    
    pass
def revisar_lista_tokens(tokens: list[str])-> bool:
    str_tokens=" ".join(tokens)
    for i, token in enumerate(tokens):
        print(f"Token {i+1}: {token}")
        if token=="exec":
            corchetes=revisar_corchetes(str_tokens,i)
            print(corchetes)
def validar_asignacion_variables(asignacion):
    respuesta = True
    respuesta = asignacion[0] == "variable"
    respuesta = respuesta and asignacion[1] == "="
    respuesta = respuesta and asignacion[2] == "n"
    return respuesta 
def validar_llamada_macro(llamada):
    llamada_str="".join(llamada)
    if llamada_str in macros:
        return True
    else:
        return False       
def validar_new_variable(new_variable):
    str_variable=" ".join(new_variable[1:])
    respuesta = True
    respuesta = new_variable[0] == "new"
    respuesta = respuesta and new_variable[1] == "variable"
    respuesta = respuesta and new_variable[2] == "="
    respuesta = respuesta and (new_variable[2] == "n" or new_variable[2] == "variable")
    if respuesta:
        global variables
        variables.append(str_variable)
    return respuesta 
def validar_new_macro(new_macro:list[str]):
    respuesta = True
    if new_macro[0] != "new":
        return False
    elif new_macro[1] != "macro":
        return False
    elif new_macro[2] == "(":
        return False
    elif new_macro[2] != "(":
        return False
    elif  not (new_macro[3].isalpha() or new_macro[1].isalnum()):
        return False
    elif new_macro[4] == ")":
        return False
    if (new_macro[5]=="(") and (new_macro[6]==")"):
        #revisar bloque
        #suponiendo que esta bien definido
        global macros
        macros.append(new_macro[1:7])
        pass
    else:
        submacro=new_macro[5:]
        inicio = submacro.index('(')
        fin = submacro.index(')', inicio)
        subcadena = "".join(submacro[inicio:fin+1]) 

        if re.match(r"\((O|n|D)(,(O|n|D))*\)", subcadena):
            #revisar bloque
            #suponiendo que esta bien definido
            global macros
            macros.append(new_macro[1:fin+1])            
            pass
        else:
            return False 
 # Funcion que valida las condiciones y devuelve la posicion del token que cierra la condicion
def validarCondiciones(tokens: list[str]) -> int:                 
    i:int = 0
    if (tokens[i] == "isblocked?"):
        if (tokens[i+1] == "("):
            if (tokens[i+2] in Lexer.directions) or tokens[i+2] == "front" or tokens[i+2] == "back":
                if (tokens[i+3] == ")"):
                    i+=4
                    return i
                else:
                    raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
            else:
                raise ValueError("Error de sintaxis: El parametro para la condicion isBlocked? debe ser una direccion (front, back, left, rigth) pero es {}.".format(tokens[i+2]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    elif (tokens[i] == "isfacing?"):
        if (tokens[i+1] == "("):
            if (tokens[i+2] in Lexer.orientations):
                if (tokens[i+3] == ")"):
                    i+=4
                    return i
                else:
                    raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
            else:
                raise ValueError("Error de sintaxis: El parametro para la condicion isFacing? debe ser una orientacion (north, south, east, west) pero es {}.".format(tokens[i+2]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    elif (tokens[i] == "zero?"):
        if (tokens[i+1] == "("):
            if (tokens[i+2] == "n") or (tokens[i+2] == "variable"):
                if (tokens[i+3] == ")"):
                    i+=4
                    return i
                else:
                    raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
            else:
                raise ValueError("Error de sintaxis: El parametro para la condicion zero? debe ser 'n' o 'variable' pero es {}.".format(tokens[i+2]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    elif (tokens[i] == "not"):
        if(tokens[i+1] == "("):
            i+=2
            i += validarCondiciones(tokens[i:])
            if (i <= len(tokens) -1) and (tokens[i] == ")"):
                i+=1
                return i
            else:
                raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    else:
        raise ValueError("Error de sintaxis: La condicion no es válida.")
#Prueba para validarCondiciones
#notAnidados = [
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "not", "(", 
#    "isblocked?", "(", "front", ")", 
#    ")", ")", ")", ")", ")", ")", ")", ")", ")", ")", 
#    ")", ")", ")", ")", ")", ")", ")", ")", ")"
#]
#
#condicionNormal: list[str] = ["isfacing?","(","north",")"]
#try:  
#    print(len(notAnidados))
#    print(validarCondiciones(notAnidados))
#except ValueError as e:
#    print(e)
#


# Funcion que valida los comandos que reciben un parametro n o variable ("walk", "jump", "drop", "pick", "grab", "letgo", "pop") y devuelve la posicion del token que cierra el comando
def validarComandosN(tokens:list[str]) -> int: 
    if (tokens[0] == "command"):
        if (tokens[1] == "("):
            if (tokens[2] == "n") or (tokens[2] == "variable"):
                if (tokens[3] == ")"):
                    return 3
                else:
                    raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
            else:
                raise ValueError("Error de sintaxis: El parametro para el comando debe ser 'n' o 'variable' pero es {}.".format(tokens[2]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    else:
        raise ValueError("Error de sintaxis: El comando no es válido.")
#Prueba para validarComandosN
#comando: list[str] = ["command", "(", "n", ")", "if", "(", "isblocked?", "(", "front", ")", ")", "then", "{", "moves", "(", "D2", ",", "D", ",", "D2", ")", "}"]
#try:
#    print(validarComandosN(comando))
#except ValueError as e:
#    print(e)

    
# Funcion que valida los comandos que son tipo turn (turntomy, turntothe) y devuelve la posicion del token que cierra el comando
def validarTurns(tokens:list[str]) -> int:
    if (tokens[0] == "turntomy"):
        if (tokens[1] == "("):
            if (tokens[2] == "D") or (tokens[2] == "back"):
                if (tokens[3] == ")"):
                    return 3
                else:
                    raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
            else:
                raise ValueError("Error de sintaxis: El parametro para el comando debe ser una direccion (left, right, back) pero es {}.".format(tokens[2]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    elif (tokens[0] == "turntothe"):
        if (tokens[1] == "("):
            if (tokens[2] == "O"):
                if (tokens[3] == ")"):
                    return 3
                else:
                    raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
            else:
                raise ValueError("Error de sintaxis: El parametro para el comando debe ser una orientacion (north, south, east, west) pero es {}.".format(tokens[2]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    else:
        raise ValueError("Error de sintaxis: El comando no es válido.")
#Prueba para validarTurns
#turntomy: list[str] = ["turntomy", "(", "D", ")", "exec", "{", "moves", "(", "D2", ",", "D", ",", "D2", ")", "}"]
#try:
#    print(validarTurns(turntomy))
#except ValueError as e:
#    print(e)
#
#turntothe: list[str] = ["turntothe", "(", "O", ")", "exec", "{", "moves", "(", "D2", ",", "D", ",", "D2", ")", "}"]
#try:
#    print(validarTurns(turntothe))
#except ValueError as e:
#    print(e)


# Funcion que valida que el comando moves que recibe parametros de tipo D2 o D y devuelve la posicion del token que cierra el comando
def validarMoves(tokens:list[str]) -> int:
    if (tokens[0] == "moves"):
        if (tokens[1] == "("):
            i:int = 2
            i += validarListaMoves(tokens[i:])
            if (i <= len(tokens) -1) and (tokens[i] == ")"):
                return i
            else:
                raise ValueError("Error de sintaxis: El parametro para el comando debe ser una direccion de movimiento (forward, backward, left, right) pero es {}.".format(tokens[2]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    else:
        raise ValueError("Error de sintaxis: El comando no es válido.")
    
# Funcion que valida que la lista de D2 y/o D sea correcta y devuelve la posicion del token que cierra la lista
def validarListaMoves(tokens:list[str]) -> int:
    i:int = 0
    while(i < len(tokens)):
        if (tokens[i] == "D2") or (tokens[i] == "D") or (tokens[i] == ","):
            i += 1
        elif (tokens[i] == ")"):
            return i
        else:
            raise ValueError("Error de sintaxis: La lista de movimientos no es válida.")
#Prueba para validarMoves
#moves: list[str] = ["moves", "(", "D2", ",", "D", ",", "D2", ")", "new", "var", "n", "(", "isblocked?", "(", "front", ")", ")"]
#try:
#    print(validarMoves(moves))
#except ValueError as e:
#    print(e)

def validarSafeExe(tokens: list[str]) -> int:
    if (tokens[0] == "safeexec"):
        if (tokens[1] == "("):
            i:int = 2
            i += validarComandosN(tokens[i:])
            if (i <= len(tokens) -1) and (tokens[i+1] == ")"):
                return i+1
            else:
                raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    else:
        raise ValueError("Error de sintaxis: El comando no es válido porrque no es un safeexe.")
#Prueba para validarSafeExe
#safeexec: list[str] = ["safeexec", "(","command", "(", "n", ")", ")", "if", "(", "isblocked?", "(", "front", ")", ")", "then", "{", "moves", "(", "D2", ",", "D", ",", "D2", ")", "}"]
#try:
#    print(validarSafeExe(safeexec))
#except ValueError as e:
#    print(e)
tokens:list[str] = leerTokens("files/prueba")
revisar_lista_tokens(tokens)