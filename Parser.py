import os
import Lexer

def leerTokens(archivo: str) -> list[str]:
    tokens:list[str] = Lexer.convertirATokens(Lexer.crearListaPalabras(archivo))
    
    return tokens

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
        