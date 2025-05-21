import re
from collections import defaultdict

# Diccionario de tokens mejorado
TOKENS = [
    ("TIPO_DATO", r'\b(int|float|char|void|string)\b', "tipo"),
    ("PALABRA_RESERVADA", r'\b(if|while|return|else|for)\b', None),
    ("IDENTIFICADOR", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', None),
    ("CONSTANTE_NUM", r'\b\d+(\.\d+)?\b|\bpi\b', "valor"),
    ("CONSTANTE_STR", r'\"([^\"\\]|\\.)*\"|\'([^\'\\]|\\.)*\'', "valor"),
    ("PUNTO_COMA", r';', None),
    ("COMA", r',', None),
    ("PARENTESIS_IZQ", r'\(', None),
    ("PARENTESIS_DER", r'\)', None),
    ("LLAVE_IZQ", r'\{', None),
    ("LLAVE_DER", r'\}', None),
    ("ASIGNACION", r'=', None),
    ("OP_ADICION", r'(\+|\-)', None),
    ("OP_MULTIPLICACION", r'(\*|/|<<)', None),
    ("OP_LOGICO", r'(&&|\|\|)', None),
    ("OP_RELACIONAL", r'(<|>|>=|<=|==|!=)', None),
    ("COMENTARIO", r'//.*?$|/\*.*?\*/', None),  # Comentarios de línea y bloque
    ("ESPACIO", r'[ \t\n]+', None),  # Espacios (ignorar)
]

# Tabla de símbolos
tabla_simbolos = {}

class Token:
    def __init__(self, tipo, lexema, valor=None, tipo_dato=None, linea=None):
        self.tipo = tipo
        self.lexema = lexema
        self.valor = valor
        self.tipo_dato = tipo_dato
        self.linea = linea
    
    def __str__(self):
        return f"Token(tipo={self.tipo}, lexema='{self.lexema}', valor={self.valor}, tipo_dato={self.tipo_dato}, linea={self.linea})"

def analizar_lexico(codigo):
    tokens_encontrados = []
    errores = []
    linea_actual = 1
    
    # Preprocesar: eliminar comentarios (podríamos conservarlos si queremos)
    codigo_sin_comentarios = re.sub(r'//.*?$|/\*.*?\*/', '', codigo, flags=re.MULTILINE|re.DOTALL)
    
    for match in re.finditer('|'.join(f'(?P<{t[0]}>{t[1]})' for t in TOKENS), codigo_sin_comentarios):
        tipo = match.lastgroup
        lexema = match.group()
        
        # Saltar espacios
        if tipo == "ESPACIO":
            linea_actual += lexema.count('\n')
            continue
        
        # Determinar tipo de dato y valor
        tipo_dato = None
        valor = None
        
        if tipo == "TIPO_DATO":
            tipo_dato = lexema
        elif tipo == "CONSTANTE_NUM":
            if lexema == "pi":
                valor = 3.141592653589793
                tipo_dato = "float"
            elif '.' in lexema:
                valor = float(lexema)
                tipo_dato = "float"
            else:
                valor = int(lexema)
                tipo_dato = "int"
        elif tipo == "CONSTANTE_STR":
            valor = lexema[1:-1]  # Eliminar comillas
            tipo_dato = "string" if lexema.startswith('"') else "char"
        
        tokens_encontrados.append(Token(tipo, lexema, valor, tipo_dato, linea_actual))
        linea_actual += lexema.count('\n')
    
    return tokens_encontrados, errores

def analizar_semantica(tokens):
    errores = []
    variables_declaradas = set()
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Detectar declaración de variable
        if token.tipo == "TIPO_DATO" and i + 1 < len(tokens) and tokens[i+1].tipo == "IDENTIFICADOR":
            tipo_var = token.lexema
            nombre_var = tokens[i+1].lexema
            variables_declaradas.add(nombre_var)
            
            # Verificar asignación en declaración
            if i + 2 < len(tokens) and tokens[i+2].lexema == "=":
                if i + 3 < len(tokens):
                    valor_asignado = tokens[i+3]
                    if valor_asignado.tipo_dato:
                        if not tipos_compatibles(tipo_var, valor_asignado.tipo_dato):
                            errores.append(f"Línea {valor_asignado.linea}: Tipo incompatible. '{nombre_var}' es de tipo {tipo_var} pero se le asigna un {valor_asignado.tipo_dato}")
            
            # Buscar el punto y coma
            while i < len(tokens) and tokens[i].lexema != ";":
                i += 1
        
        # Detectar asignación a variable
        elif token.tipo == "IDENTIFICADOR" and i + 1 < len(tokens) and tokens[i+1].lexema == "=":
            nombre_var = token.lexema
            if nombre_var not in variables_declaradas:
                errores.append(f"Línea {token.linea}: Variable '{nombre_var}' no declarada")
            else:
                # Verificar tipo en asignación
                if i + 2 < len(tokens):
                    valor_asignado = tokens[i+2]
                    if valor_asignado.tipo_dato:
                        # Obtener el tipo declarado de la variable
                        tipo_var = next((t.lexema for t in tokens[:i] if t.tipo == "TIPO_DATO" and t.linea < token.linea), None)
                        if tipo_var and not tipos_compatibles(tipo_var, valor_asignado.tipo_dato):
                            errores.append(f"Línea {token.linea}: Tipo incompatible. '{nombre_var}' es de tipo {tipo_var} pero se le asigna un {valor_asignado.tipo_dato}")
            
            # Buscar el punto y coma
            while i < len(tokens) and tokens[i].lexema != ";":
                i += 1
        
        i += 1
    
    return errores

def tipos_compatibles(tipo_declarado, tipo_asignado):
    # Reglas de compatibilidad de tipos
    if tipo_declarado == tipo_asignado:
        return True
    if tipo_declarado == "float" and tipo_asignado == "int":
        return True
    if tipo_declarado == "string" and tipo_asignado == "char":
        return True
    return False

def analizar_codigo(codigo):
    # Limpiar tabla de símbolos para cada nuevo análisis
    global tabla_simbolos
    tabla_simbolos = {}
    
    # Análisis léxico
    tokens, errores_lexicos = analizar_lexico(codigo)
    if errores_lexicos:
        print("Errores léxicos:")
        for error in errores_lexicos:
            print(error)
        return
    
    # Análisis semántico (ahora más robusto)
    errores_semanticos = analizar_semantica(tokens)
    
    if errores_semanticos:
        print("Errores semánticos encontrados:")
        for error in errores_semanticos:
            print(error)
    else:
        print("El código es semánticamente correcto")

# Código de prueba mejorado
codigo_ejemplo = """
int x = 10;
float y = 3.14;
char c = 'a';
string s = "hola";

if (x > 5) {
    y = y + x;
} else {
    x = 0;
}

z = x + y;  // Error semántico: z no declarada
int w = "hola";  // Error semántico: tipo incorrecto
char letra = 65;  // Esto sería válido (ASCII)
float f = "texto";  // Error de tipo
"""

analizar_codigo(codigo_ejemplo)