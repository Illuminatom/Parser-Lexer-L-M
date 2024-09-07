import os
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
        

tokens:list[str] = leerTokens("files/prueba")


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

#####                                     #####
##### FUNCIONES VERIFICADORAS DE COMANDOS #####
#####                                     #####
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

#####                                                     #####
#####        FUNCIONES PARA VERIFICAR LOS BLOQUES         #####
#####                                                     ##### 
# Funcion que valida la estructura de un bloque y devuelve la posicion del token que cierra el bloque
def validarBloque(tokens: list[str]) -> int:
    i:int = 1
    while(i < len(tokens)):
        if (tokens[i] == "command"):
            i += validarComandosN(tokens[i:])
            if (tokens[i+1] == ";"):
                i += 2
                print(tokens[i])
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {} en vez".format(tokens[i]))
        elif (tokens[i] == "turntomy") or (tokens[i] == "turntothe"):
            i += validarTurns(tokens[i:])
            if (tokens[i+1] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {} en vez".format(tokens[i]))
        elif (tokens[i] == "moves"):
            i += validarMoves(tokens[i:])
            if (tokens[i+1] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {} en vez".format(tokens[i]))
        elif (tokens[i] == "safeexec"):
            i += validarSafeExe(tokens[i:])
            if (tokens[i+1] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {} en vez".format(tokens[i]))
        elif (tokens[i] == "nop"):
            if (tokens[i+1] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {} en vez".format(tokens[i]))
        elif (tokens[i] == "if"):
            i += validarIf(tokens[i:])
            if (tokens[i] == "fi"):
                i += 1
            if (tokens[i] == ";"):
                i += 1
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {0} en vez y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens[i+1]))

        elif (tokens[i] == "}"):
            return i
        else:
            raise ValueError("Error de sintaxis: El bloque no es válido. Hay {0} en vez y despues hay {1} y i es {2}".format(tokens[i], tokens[i+1], i))

#####                                                     #####
##### FUNCIONES VERIFICADORAS DE ESTRUCTURAS DE CONTROL   #####
#####                                                     #####
# Funcion que valida la estructura de control if y devuelve la posicion del token que cierra la estructura
def validarIf(tokens: list[str]) -> int:
    if (tokens[0] == "if"):
        i:int = 1
        i += validarCondiciones(tokens[i:])     #Ultimo token de la condicion
        if (tokens[i] == "then"):
            i += 1
            if (tokens[i] == "{"):
                i += validarBloque(tokens[i:])+ 1  #Ultimo token del bloque
                if (tokens[i] == "else"):         #Que haya o no un else es opcional
                    i += validarElse(tokens[i:]) +1   #Ultimo token del else y su bloque
                if (tokens[i] == ";"):
                    return i +2
                if (tokens[i] == "fi"):
                    return i+1
                else:
                    raise ValueError("Error de sintaxis: Falta el cierre de la estructura if. Hay {0} y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens[i+1]))
        else:
            raise ValueError("Error de sintaxis: Falta la palabra reservada 'then' despues de la condicion. {}".format(tokens[i]))
    else:
        raise ValueError("Error de sintaxis: La estructura if no valida.")

#Funcion para verificar recursivamente los else's de un if
def validarElse(tokens: list[str]) -> int:
    if (tokens[0] == "else"):
        i:int = 1
        if (tokens[i] == "{"):
            i += validarBloque(tokens[i:])  #Ultimo token del bloque
        if (tokens[i+1] == "else"):
            i += validarElse(tokens[i+1:])
        return i
    else:
        raise ValueError("Error de sintaxis: La estructura else no es válida. Hay {0} y el i es {1}".format(tokens[0], i))

#Prueba para validarIf
#si:list[str] = ["if",           #0
#                "isblocked?",   #1
#                "(",            #2
#                "front",        #3
#                ")",            #4
#                "then",         #5
#                "{",            #6
#                "moves",        #7
#                "(",            #8
#                "D2",           #9
#                ",",            #10
#                "D",            #11
#                ",",            #12
#                "D2",           #13
#                ")",            #14
#                ";",            #15
#                "}",            #16
#                "else",         #17
#                "{",            #18
#                "command",      #19
#                "(",            #20
#                "n",            #21
#                ")",            #22
#                ";",            #23
#                "}",            #24
#                "else",         #25
#                "{",            #26
#                "turntomy",     #27
#                "(",            #28
#                "D",            #29
#                ")",            #30
#                ";",            #31
#                "}",            #32
#                "else",         #33
#                "{",            #34
#                "if",           #35
#                "isblocked?",   #36
#                "(",            #37
#                "front",        #38
#                ")",            #39
#                "then",         #40
#                "{",            #41
#                "nop",          #42
#                ";",            #43
#                "}",            #44
#                "fi",           #45
#                ";",            #46
#                "}",            #47
#                "fi"]           #48
#try:
#    print(validarIf(si))
#except ValueError as e:
#    print(e)

#Prueba para validarBloque
#bloque: list[str] = ["{", 
#                     "command", 
#                     "(", 
#                     "n", 
#                     ")", 
#                     ";",
#                     "if", 
#                     "isblocked?", 
#                     "(", 
#                     "front", 
#                     ")", 
#                     "then", 
#                     "{", 
#                     "moves", 
#                     "(", 
#                     "D2", 
#                     ",", 
#                     "D", 
#                     ",", 
#                     "D2", 
#                     ")", 
#                     ";", 
#                     "}", 
#                     "fi", 
#                     ";", 
#                     "}"]
#try:
#    print(validarBloque(bloque))
#except ValueError as e:
#    print(e)