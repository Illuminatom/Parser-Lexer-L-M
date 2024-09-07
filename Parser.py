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

def validarCondiciones(tokens: list[str]) -> int:
    i:int = 0
    while i < len(tokens):
        if (tokens[i] == "isblocked?"):
            if (tokens[i+1] == "("):
                if (tokens[i+2] in Lexer.directions) or tokens[i+2] == "front":
                    if (tokens[i+3] == ")"):
                        i+=4
                        continue
                    else:
                        raise ValueError("Error de sintaxis: Falta un paréntesis de cierre.")
                else:
                    raise ValueError("Error de sintaxis: El parametro para la condicion isBlocked? debe ser una direccion (front, back, left, rigth) pero es {}.".format(tokens[i+2]))
            else:
                raise ValueError("Error de sintaxis: Falta un paréntesis de apertura.")
        
