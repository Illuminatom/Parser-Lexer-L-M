import os
import Lexer

def leerTokens(archivo: str) -> list[str]:
    tokens:list[str] = Lexer.convertirATokens(Lexer.crearListaPalabras(archivo))
    
    return tokens

