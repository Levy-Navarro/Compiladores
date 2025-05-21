#Importación de librería para las expresiones regulares
import re

tokens = []
indice = 0

#Funcion para recibir la expresion y encontrar coincidencias comparando la re que se hace aquí
def tokenize(expresion):
    tokens_especificos = [
        ("Numero", r'\d+'),         #Números
        ("Identificador", r'[a-zA-Z][a-zA-Z0-9_]*'), #Identificadores
        ("Asignacion", r'='),           # Operador de asignación
        ("Mas", r'\+'),            #Suma
        ("Multi", r'\*'),           #Multiplicación
        ("Division", r'/'),           #División
        ("IParente", r'\('),          #Paréntesis izquierdo
        ("DParente", r'\)'),          #Paréntesis derecho
        ("PuYCo", r';'),        #Punto y coma
        ("Salto", r'[ \t\n]+'),      #Espacios y saltos de línea (ignorar)
        ("Restante", r'.')          #Cualquier otro carácter no válido
    ]
    
    #Fusion de las reglas de la parte superior
    expresion_completa = '|'.join(f'(?P<{par[0]}>{par[1]})' for par in tokens_especificos)
    
    #Bucles para encontrar coincidencias en la expresión recibida respecto a la expresión fusionada (reglas)
    for coincidencia in re.finditer(expresion_completa, expresion):
        #Toma el nombre de la primer parte del diccionario
        tipo = coincidencia.lastgroup
        #Toma el nombre de la segunda parte del diccionario
        valor = coincidencia.group()

        #Si encuentra coincidencia con el tipo salto le permite continuar
        if tipo == "Salto":
            continue
        #Si encuentra un error detecta el token que está mal
        elif tipo == "Restante":
            raise SyntaxError(f"Token inesperado: {valor}")
        #Se añade a la lista de tokens la dupla del diccionario
        tokens.append((tipo, valor))

#Funcion para detectar el tipo de token
def coincidencia(tipo_esperado):
    global indice
    if indice < len(tokens) and tokens[indice][0] == tipo_esperado:
        indice += 1
        return True
    return False

#Función para detectar tipos de tokens iniciales del lado izquierdo y parentesis
def factor():
    if coincidencia("Numero") or coincidencia("Identificador"):
        return True
    elif coincidencia("IParente"):
        if expresion():
            return coincidencia("DParente")
    return False

#Función para detectar operadores
def term():
    if factor():
        while coincidencia("Multi") or coincidencia("Division"):
            if not factor():
                return False
        return True
    return False

def expresion():
    if term():
        while coincidencia("Mas"):
            if not term():
                return False
        return True
    return False

#Funcipo para detectar asignaciones y terminaciones de instrucciones con punto y coma
def asignacion():
    if coincidencia("Identificador") and coincidencia("Asignacion") and expresion() and coincidencia("PuYCo"):
        return True
    return False

#Función para parsear la expresión (elementos en la lista de ejemplos)
def parsear(codigo):
    global tokens, indice
    tokens = []
    indice = 0
    tokenize(codigo)
    return asignacion() and indice == len(tokens)

#Ejemplos
ejemplos = ["x = 5;", "y = y (x + 3;", "z = (y *) / 4;", "y = z + y"]
for ejemplo in ejemplos:
    print(f"{ejemplo} -> {'Válido' if parsear(ejemplo) else 'Inválido'}")
