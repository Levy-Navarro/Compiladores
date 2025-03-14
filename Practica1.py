import re
from collections import defaultdict

#Diccionario de todos los tokens contemplados y su expresión regular correspondiente
TOKENS = [
    (0, r'\b(int|float|char|void|string)\b'),  #Tipos de datos
    (10, r'\bif\b'),                           #if
    (11, r'\bwhile\b'),                        #while
    (12, r'\breturn\b'),                       #return
    (13, r'\belse\b'),                         #else
    (14, r'\bfor\b'),                          #for
    (1, r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),        #Identificadores
    (2, r'\b\d+(\.\d+)?\b|\bpi\b'),       #Constantes (números o "pi")
    (3, r';'),                                   #Punto y coma
    (4, r','),                                   #Coma
    (5, r'\('),                                 #Paréntesis izquierdo
    (6, r'\)'),                                 #Paréntesis derecho
    (7, r'\{'),                                 #Llave izquierda
    (8, r'\}'),                                 #Llave derecha
    (9, r'='),                                   #Igual (=)
    (15, r'(\+|\-)'),                          #Operadores de adición (+, -)
    (16, r'(\*|/|<<)'),                         #Operadores de multiplicación (*, /, <<)
    (17, r'(&&|\|\|)'),                        #Operadores lógicos (&&, ||)
    (18, r'(<|>|>=|<=|==|!=)'),                  #Operadores relacionales
    (19, r'\$'),                                #Símbolo "$"
]

#Expresión regular combinada
TOKEN_REGEX = '|'.join(f'(?P<TOKEN_{t[0]}>{t[1]})' for t in TOKENS)

#Función de análisis léxico
def analizar_lexico(codigo):
    tokens_encontrados = []
    conteo_tokens = defaultdict(int)
    
    for match in re.finditer(TOKEN_REGEX, codigo):
        for id_token, _ in TOKENS:
            if match.group(f'TOKEN_{id_token}'):
                lexema = match.group(f'TOKEN_{id_token}')
                tokens_encontrados.append((id_token, lexema))
                conteo_tokens[id_token] += 1
                break
    
    return tokens_encontrados, conteo_tokens

#Código de prueba
codigo_prueba = '''
int x = 10;
if (x > 5) {
    return x;
}
while x < 5 {
    x = x + 1;
    $ // Token de prueba
}

y = 2 + 4

x >= 1
'''

#Retorno de los tokens y el conteo de los mismos
tokens, conteo = analizar_lexico(codigo_prueba)

#Impresion los tokens encontrados
for token in tokens:
    print(f'Tipo: {token[0]}, Lexema: {token[1]}')

#Impresión del conteo de tokens
print("\nConteo de tokens:")
for token_id, count in conteo.items():
    print(f'Tipo {token_id}: {count} veces')
