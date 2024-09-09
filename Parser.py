import Lexer

macros:list = []
variables = {}

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

def revisar_lista_tokens(tokens: list[str])-> bool:
    str_tokens=" ".join(tokens)
    for i, token in enumerate(tokens):
        print(f"Token {i+1}: {token}")
        if token=="exec":
            corchetes=revisar_corchetes(str_tokens,i)
            print(corchetes)

#####                                         #####
##### FUNCIONES VERIFICADORAS DE DEFINICIONES #####
#####                                         #####
# Funcion que valida la creacion de un nuevo macro o una nueva variable y retorna la posicion del token que cierra la definicion del mismo
def validarNew(tokens:list[str]) -> int:
    if tokens[0] == "new":
        if tokens[1] == "macro":
            if (tokens[2].isalpha() or tokens[2].isalnum()):
                if (tokens[3] == "("):
                    i:int = 3
                    i += validarListaAtributos(tokens[i:])
                    j:int = i
                    macros.append("".join(tokens[2:j+1])) 
                    if (tokens[i+1] == "{"):
                            i += validarBloque(tokens[i+1:])+1
                            return i          
                    else:
                        raise ValueError("Error de sintaxis: Falta un bloque después de la definición del macro.")
                else:
                    raise ValueError("Error de sintaxis: Faltan los atributos despues del nombre del macro.")
        elif (tokens[1] == "variable"):
            if(tokens[2] == "="):
                if(tokens[3] == "n") or (tokens[3] == "variable"):
                    return 3
                else:
                    raise ValueError("Error de sintaxis: El valor de la variable debe ser 'n' o 'variable' pero es {}.".format(tokens[3]))
            else:
                raise ValueError("Error de sintaxis: Falta un signo de igual despues del nombre de la variable.")  
        else:
            raise ValueError("Error de sintaxis: Despues de la palabra reservada new debe haber macro o variable pero hay {}.".format(tokens[1]))      
    else:
        raise ValueError("Error de sintaxis: La creacion de macro no es valida.")

#Funcion que valida que una lista de atributos para un macro sea correcta y devuelve la posicion del token que cierra la lista
def validarListaAtributos(tokens: list[str]) -> int:
    i:int = 1
    while(i < len(tokens)):
        if (tokens[i] == "O") or (tokens[i] == "n") or (tokens[i] == "D") or (tokens[i] == ","):
            i += 1
        elif (tokens[i] == ")"):
            return i
        else:
            raise ValueError("Error de sintaxis: La lista de atributos no es válida. Hay {0} en vez e i es {1}".format(tokens[i], i))


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
    if (tokens[0] == "safeexe"):
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

           
#Funcion que valida que la asignacion de valor a una variable sea correcta y devuelve la posicion del token que cierra la asignacion
def validarAsignacionVariable(tokens: list[str]) -> int:
    if(tokens[0] == "variable"):
        if[(tokens[1] == "=")]: 
            if(tokens[2] == "n") or (tokens[2] == "variable"):
                return 2
            else:
                raise ValueError("Error de sintaxis: El valor de la variable debe ser 'n' o 'variable' pero es {}.".format(tokens[2]))
        else:
            raise ValueError("Error de sintaxis: Falta un signo de igual despues del nombre de la variable.")
    else:
        raise ValueError("Error de sintaxis: La asignacion de valor a la variable no es valida.")  

#Funcion que valida que cuando se invoca un macro se haga de forma correcta y devuelve la posicion del token que cierra la invocacion
def validarInvocacionMacro(tokens: list[str]) -> int:
    if(tokens[0] in Lexer.personalizedMacros):
        if(tokens[1] == "("):
            i:int = 2
            i += validarListaAtributos(tokens[i-1:])
            macroCompleto:str = "".join(tokens[0:i])
            if (tokens[i-1] == ")"):
                if(macroCompleto in macros):
                    return i-1
                else:
                    raise ValueError("El macro no esta guardado en la lista de macros definidos hasta el momento el macro completo es {0} y los macros guardados son {1}".format(macroCompleto, macros))
            else:
                raise ValueError("Error de sintaxis: Falta un paréntesis de cierre. Hay {0} en vez".format(tokens[i]))
        else:
            raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
    else:
        raise ValueError("Error de sintaxis: La invocacion de macro no es valida.")

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
        elif (tokens[i] == "safeexe"):
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
            if (tokens[i] == "od") or (tokens[i] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {0} en vez y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens))
        elif (tokens[i] == "rep"):
            i += validarRep(tokens[i:])
            if (tokens[i] == "per") or (tokens[i] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {0} en vez y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens))    
        elif(tokens[i] in Lexer.personalizedMacros):
            i += validarInvocacionMacro(tokens[i:])
            if (tokens[i+1] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {} en vez".format(tokens[i]))
        elif(tokens[i] == "variable"):
            i += validarAsignacionVariable(tokens[i:])
            if (tokens[i+1] == ";"):
                i += 2
            else:
                raise ValueError("Error de sintaxis: Falta un punto y coma. Hay {} en vez".format(tokens[i]))
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
        if (tokens[1] == "("):
            i:int = 2
            i += validarCondiciones(tokens[i:])  +1   #Posicion despues de la condicion
            print(tokens[i])
        else:
            raise ValueError("La condicion del if debe estar entre parentesis")
        if (tokens[i] == "then"):
            i += 1
            if (tokens[i] == "{"):
                i += validarBloque(tokens[i:])+ 1  ##Posicion despues de la condicion
                if (tokens[i] == "else"):         #Que haya o no un else es opcional
                    i += validarElse(tokens[i:])    ##Posicion despues de los else y sus bloques
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
        return i+1
    else:
        raise ValueError("Error de sintaxis: La estructura else no es válida. Hay {0} y el i es {1}".format(tokens[0], i))
    
#Funcion que validala estructura de control do y devuelve la posicion del token que cierra la estructura
def validarDo(tokens: list[str]) -> int:
    if (tokens[0] == "do"):
        if (tokens[1] == "("):
            i:int = 2
            i += validarCondiciones(tokens[i:])  +1   #Posicion despues de la condicion
            print(tokens[i])
        else:
            raise ValueError("La condicion del do debe estar entre parentesis")
        if (tokens[i] == "{"):
            i += validarBloque(tokens[i:])+1            #Posicion despues del bloque
            if (tokens[i] == "od"):
                return i
            else:
                raise ValueError("Error de sintaxis: Falta el cierre de la estructura do. Hay {0} y el i es {1} y antes hay {2} y despues hay {3}".format(tokens[i], i, tokens[i-1], tokens[i+1]))
        else:
            raise ValueError("Error de sintaxis: Falta el bloque de la estructura do.")
    else:
        raise ValueError("Error de sintaxis: La estructura do no es válida.")
    
#Funcion que valida la estructura de control rep y devuelve la posicion del token que cierra la estructura
def validarRep(tokens: list[str]) -> int:
    if (tokens[0] == "rep"):
        if (tokens[1] == "n") or (tokens[1] == "variable"):
            if (tokens[2] == "times"):
                if (tokens[3] == "{"):
                    i:int = 3
                    i += validarBloque(tokens[i:])+1
                    if (tokens[i] == "per"):
                        return i
                    else:
                        raise ValueError("Error de sintaxis: Falta el cierre de la estructura rep.")
                else:
                    raise ValueError("Error de sintaxis: Falta el bloque de la estructura rep.")
            else:
                raise ValueError("Error de sintaxis: Falta la palabra reservada 'times' despues del valor de rep.")
        else:
            raise ValueError("Error de sintaxis: Falta el valor de rep.")
    else:
        raise ValueError("Error de sintaxis: La estructura rep no es válida.")

####                          ####
####  EJECUCION DEL PROGRAMA  ####
####                          ####
tokens:list[str] = leerTokens("files/prueba")

def validarCompleto(tokens:list[str]) -> str:
    i:int = 0
    while (i < len(tokens)):
        print("Analizando token: {0} en la posicion {1}".format(tokens[i], i))
        if (tokens[i] == "exec"):
            j:int = i
            i += validarBloque(tokens[i+1:])+2
            print("El EXEC en la posicion {} esta bien escrito \n".format(j))
        elif (tokens[i] == "new"):
            j:int = i
            i += validarNew(tokens[i:])+1
            print("La definicion en la posicion {} esta bien escrita".format(j))
            if (tokens[j+1] == "macro"):
                print("\t Se definio el macro {} \n".format(tokens[j+2]))
            elif (tokens[j+1] == "variable"):
                print("\t Se declaro una variable \n")
        else:
            raise ValueError("Error de sintaxis: El programa no es válido. El input paara el robot debe ser una instruccion exec o una definicion de macro o variable pero hay {} en vez de eso.".format(tokens[i]))
    return "El programa es válido."

def Parser() -> None:
    print("\nBIENVENIDO AL PARSER PARA LA GRAMATICA DEL ROBOT")
    direccionArchivo:str = input("Por favor ingrese el la direccion del archivo sin el .txt: ")
    tokens:list[str] = leerTokens(direccionArchivo)
    opcionI:str = input("Que desea realizar? \n 1. Verificar la validez del archivo \n 2. Ver los Tokens numerados \n 3. Ver los Tokens como cadena\n 4. Salir \n \t>")
    while(opcionI != "4"):
        if(opcionI == "1"):
            try:
                print(validarCompleto(tokens))
                print("FELICIDADES, TODO PARECE FUNCIONAR")
                opcionI = input("\nQue desea realizar? \n 1. Verificar el archivo \n 2. Ver los Tokens numerados \n 3. Ver los Tokens como cadena\n 4. Salir \n \t> ")
            except ValueError as e:
                print(e)
                print("Muy mal, el programa fallo :C")
                opcionI:str = input("\nQue desea realizar? \n 1. Verificar la validez del archivo \n 2. Ver los Tokens numerados \n 3. Ver los Tokens como cadena\n 4. Salir \n \t> ")
        elif(opcionI == "2"):
            Lexer.imprimirTokensNumerados(tokens)    
            opcionI:str = input("\nQue desea realizar? \n 1. Verificar la validez del archivo \n 2. Ver los Tokens numerados \n 3. Ver los Tokens como cadena\n 4. Salir \n \t> ")
        elif(opcionI == "3"):
            Lexer.imprimirTokensStr(tokens)
            opcionI:str = input("\nQue desea realizar? \n 1. Verificar la validez del archivo \n 2. Ver los Tokens numerados \n 3. Ver los Tokens como cadena\n 4. Salir \n \t > ")
        elif(opcionI == "4"):
            print("Gracias por usar el programa. Hasta luego")
        else:
            print("Opcion invalida")
            opcionI:str = input("\nQue desea realizar? \n 1. Verificar la validez del archivo \n 2. Ver los Tokens numerados \n 3. Ver los Tokens como cadena\n 4. Salir \n \t > ")

Parser()