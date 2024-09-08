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
    elif  not (new_macro[2].isalpha() or new_macro[2].isalnum()):
        return False
    if (new_macro[3]=="(") and (new_macro[4]==")"):
        #revisar bloque
        #suponiendo que esta bien definido
        global macros
        macros.append(new_macro[1:4])
        pass
    else:
        submacro=new_macro[3:]
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
            if (tokens[i+2] == "D") or tokens[i+2] == "front" or tokens[i+2] == "back":
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
            if (tokens[i+2] == "O"):
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
            if (tokens[i] == "fi") or (tokens[i] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {0} en vez y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens[i+1]))
        elif (tokens[i] == "do"):
            i += validarDo(tokens[i:])
            if (tokens[i] == "od"):
                i += 1
            if (tokens[i] == ";"):
                i += 1
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {0} en vez y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens))

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
                    i += validarElse(tokens[i:])    #Ultimo token del else y su bloque
                if (tokens[i] == "fi"):
                    return i
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
        print("El i es {0} y el token[i] es {1}".format(i, tokens[i]))
        return i+1
    else:
        raise ValueError("Error de sintaxis: La estructura else no es válida. Hay {0} y el i es {1}".format(tokens[0], i))
    
#Funcion que validala estructura de control do y devuelve la posicion del token que cierra la estructura
def validarDo(tokens: list[str]) -> int:
    if (tokens[0] == "do"):
        i:int = 1
        i += validarCondiciones(tokens[i:])
        if (tokens[i] == "{"):
            i += validarBloque(tokens[i:])+1
            if (tokens[i] == "od"):
                return i
            else:
                raise ValueError("Error de sintaxis: Falta el cierre de la estructura do. Hay {0} y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens[i+1]))
        else:
            raise ValueError("Error de sintaxis: Falta el bloque de la estructura do.")
    else:
        raise ValueError("Error de sintaxis: La estructura do no es válida.")
##Prueba para validarDo
#do: list[str] = ["do",          #0
#                 "isblocked?",  #1
#                 "(",           #2
#                 "front",       #3
#                 ")",           #4
#                 "{",           #5
#                 "moves",       #6
#                 "(",           #7
#                 "D2",          #8
#                 ",",           #9
#                 "D",           #10
#                 ",",           #11
#                 "D2",          #12
#                 ")",           #13
#                 ";",           #14
#                 "do",          #15
#                 "zero?",       #16
#                 "(",           #17
#                 "variable",    #18
#                 ")",           #19
#                 "{",           #20
#                 "if",          #21
#                    "isblocked?",  #22
#                    "(",           #23
#                    "front",       #24
#                    ")",           #25
#                    "then",        #26
#                    "{",           #27
#                    "do",          #28
#                        "not",      #29
#                        "(",        #30
#                        "isblocked?",#31
#                        "(",        #32
#                        "front",    #33
#                        ")",        #34
#                        ")",        #35
#                        "{",        #36
#                        "moves",    #37
#                        "(",        #38
#                        "D2",       #39
#                        ",",        #40
#                        "D",        #41
#                        ",",        #42
#                        "D2",       #43
#                        ")",        #44
#                        ";",        #45
#                        "}",        #46
#                        "od",       #47
#                    ";",            #48
#                    "}",            #49
#                    "else",         #50
#                    "{",            #51
#                        "nop",      #52
#                    ";",            #53
#                    "}",            #54
#                    "else",         #55
#                    "{",            #56
#                        "safeexec", #57
#                        "(",        #58
#                        "command",  #59
#                        "(",        #60
#                            "n",    #61
#                        ")",        #62
#                        ")",        #63
#                        ";",        #64
#                        "do",        #65
#                        "isblocked?",#66
#                        "(",        #67
#                            "back", #68
#                        ")",        #69
#                        "{",        #70
#                            "nop",  #71
#                        ";",        #72
#                        "}",        #73
#                        "od",       #74
#                        ";",        #75
#                        "if",       #76
#                            "zero?",    #77
#                            "(",        #78
#                                "variable", #79
#                            ")",        #80
#                            "then",     #81
#                            "{",        #82
#                                "nop",  #83
#                            ";",        #84
#                            "}",        #85
#                            "fi",       #86
#                        ";",        #87
#                    "}",            #88
#                    "fi",           #89
#                 ";",               #90
#                 "}",               #91
#                 "od",              #92
#                 ";",               #93
#                 "}",               #94
#                 "od"]              #95
#do: list[str] = ["do",          #0
#                    "isblocked?",  #1
#                    "(",           #2
#                        "front",   #3
#                    ")",           #4
#                    "{",           #5
#                        "command",  #6
#                        "(",        #7
#                            "n",    #8
#                        ")",        #9
#                        ";",        #10
#                        "if",       #11
#                        "isblocked?",#12
#                        "(",        #13
#                            "D",    #14
#                        ")",        #15
#                        "then",     #16
#                        "{",        #17
#                            "moves",#18
#                            "(",    #19
#                                "D2",#20
#                                ",",    #21
#                                "D",#22
#                                ",",    #23
#                                "D2",#24
#                            ")",    #25
#                        ";",        #26
#                        "}",        #27
#                        "fi",       #28
#                    ";",            #29
#                    "}",            #30
#                "od"           #31
#                ]
#try:
#    print(validarDo(do))
#except ValueError as e:
#    print(e)

#Prueba para validarIf
#si:list[str] = ["if",           #0
#                "isblocked?",   #1
#                "(",            #2
#                "front",        #3
#                ")",            #4
#                "then",         #5
#                "{",            #6
#                    "moves",        #7
#                    "(",            #8
#                        "D2",           #9
#                        ",",            #10
#                        "D",            #11
#                        ",",            #12
#                        "D2",           #13
#                    ")",            #14
#                ";",            #15
#                "}",            #16
#                "else",         #17
#                "{",            #18
#                    "command",      #19
#                    "(",            #20
#                    "n",            #21
#                    ")",            #22
#                    ";",            #23
#                    "}",            #24
#                "else",         #25
#                "{",            #26
#                    "turntomy",     #27
#                    "(",            #28
#                        "D",            #29
#                    ")",            #30
#                ";",            #31
#                "}",            #32
#                "else",         #33
#                "{",            #34
#                    "if",           #35
#                        "isblocked?",   #36
#                        "(",            #37
#                            "front",        #38
#                        ")",            #39
#                    "then",         #40
#                    "{",            #41
#                        "nop",          #42
#                    ";",            #43
#                    "}",            #44
#                    "fi",           #45
#                ";",            #46
#                "}",            #47
#                "else",         #48
#                "{",            #49
#                    "if",           #50
#                        "isblocked?",   #51
#                        "(",            #52
#                            "back",         #53
#                        ")",            #54
#                    "then",         #55
#                    "{",            #56
#                        "nop",           #57
#                    ";",            #58
#                    "}",            #59
#                    "fi",           #60
#                ";",            #61
#                    "nop",          #62
#                ";",            #63
#                "}",            #64
#                "fi"]           #65

#si2:list[str] = ["if",           #0
#                        "isblocked?",   #1
#                        "(",            #2
#                            "back",    #3
#                        ")",            #4
#                        "then",         #5
#                        "{",            #6
#                            "do",       #7
#                            "not",      #8
#                            "(",        #9
#                            "isfacing?",#10
#                            "(",        #11
#                                "O",#12
#                            ")",        #13
#                            ")",        #14
#                            "{",        #15
#                                "command",#16
#                                "(",    #17
#                                    "n",#18
#                                ")",    #19
#                                ";",    #20
#                            "}",        #21
#                            "od",       #22
#                        ";",            #23
#                        "}",            #24
#                        "fi",           #25
#                        ";",            #26
#                        ]
#try:
#    print(validarIf(si))
#except ValueError as e:
#    print(e)

#Prueba para validarBloque
#bloque: list[str] = ["{",               #0
#                     "command",         #1
#                     "(",               #2
#                        "n",            #3
#                     ")",               #4
#                     ";",               #5
#                        "if",           #6
#                        "isblocked?",   #7
#                        "(",            #8
#                            "D",    #9
#                        ")",            #10
#                        "then",         #11
#                        "{",            #12
#                            "moves",    #13
#                            "(",        #14
#                                "D2",   #15
#                                ",",    #16
#                                "D",    #17
#                                ",",    #18
#                                "D2",   #19
#                            ")",        #20
#                        ";",            #21
#                        "}",            #22
#                        "fi",           #23
#                     ";",               #24
#                        "do",           #25
#                        "not",          #26
#                        "(",            #27
#                            "isblocked?",#28
#                            "(",        #29
#                                "front",#30
#                            ")",        #31
#                        ")",            #32
#                        "{",            #33
#                            "nop",      #34
#                        ";",            #35
#                        "if",           #36
#                        "zero?",        #37
#                        "(",            #38
#                            "variable", #39
#                        ")",            #40
#                        "then",         #41
#                        "{",            #42
#                            "command",  #43
#                            "(",        #44
#                                "n",    #45
#                            ")",        #46
#                            ";",        #47
#                        "}",            #48
#                        "fi",           #49
#                        ";",            #50  
#                        "if",           #51
#                        "isblocked?",   #52
#                        "(",            #53
#                            "back",    #54
#                        ")",            #55
#                        "then",         #56
#                        "{",            #57
#                            "do",       #58
#                            "not",      #59
#                            "(",        #60
#                            "isfacing?",#61
#                            "(",        #62
#                                "O",#63
#                            ")",        #64
#                            ")",        #65
#                            "{",        #66
#                                "command",#67
#                                "(",    #68
#                                    "n",#69
#                                ")",    #70
#                                ";",    #71
#                            "}",        #72
#                            "od",       #73
#                        ";",            #74
#                        "}",            #75
#                        "fi",           #76
#                        ";",            #77
#                        "}",           #78
#                        "od",          #79
#                        ";",           #80
#                        "if",          #81
#                        "isfacing?",   #82
#                        "(",           #83
#                            "O",       #84
#                        ")",           #85
#                        "then",        #86
#                        "{",           #87
#                            "command",  #88
#                            "(",        #89
#                                "n",    #90
#                            ")",        #91
#                            ";",        #92
#                        "}",           #93
#                        "else",        #94
#                        "{",            #95
#                            "nop",      #96
#                            ";",            #97
#                            "nop",      #98
#                            ";",            #99
#                        "}",            #100
#                        "fi",          #101
#                        ";",           #102
#                     "}"]              #103
#try:
#    print(validarBloque(bloque))
#except ValueError as e:
#    print(e)
tokens:list[str] = leerTokens("files/prueba")
revisar_lista_tokens(tokens)