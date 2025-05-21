import re
from collections import defaultdict

""" ------------------------- Analizador Semántico ------------------------- """

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
"""

analizar_codigo(codigo_ejemplo)

""" ------------------------- Generador de Código intermedio ------------------------- """

class GeneradorCodigoIntermedio:
    def __init__(self):
        self.codigo_intermedio = []
        self.temp_count = 0
        self.label_count = 0
        self.var_types = {}  # Tipos de variables
        
    def nueva_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def nuevo_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def generar_intermedio(self, tokens):
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Declaración de variable
            if token.tipo == "TIPO_DATO" and i+1 < len(tokens) and tokens[i+1].tipo == "IDENTIFICADOR":
                tipo = token.lexema
                var_name = tokens[i+1].lexema
                self.var_types[var_name] = tipo
                
                # Asignación en declaración
                if i+2 < len(tokens) and tokens[i+2].lexema == "=":
                    value = self.procesar_expresion(tokens[i+3:])
                    self.codigo_intermedio.append(f"STORE {value} -> {var_name}")
                    # Avanzar hasta el ;
                    while i < len(tokens) and tokens[i].lexema != ";":
                        i += 1
            
            # Asignación simple
            elif token.tipo == "IDENTIFICADOR" and i+1 < len(tokens) and tokens[i+1].lexema == "=":
                var_name = token.lexema
                value = self.procesar_expresion(tokens[i+2:])
                self.codigo_intermedio.append(f"STORE {value} -> {var_name}")
                # Avanzar hasta el ;
                while i < len(tokens) and tokens[i].lexema != ";":
                    i += 1
            
            # Estructura if
            elif token.lexema == "if":
                label_else = self.nuevo_label()
                label_end = self.nuevo_label()
                
                # Procesar condición
                i += 2  # Saltar 'if' y '('
                cond = self.procesar_expresion(tokens[i:])
                self.codigo_intermedio.append(f"IF_NOT {cond} GOTO {label_else}")
                
                # Procesar cuerpo del if
                while i < len(tokens) and tokens[i].lexema != "{":
                    i += 1
                i += 1  # Saltar '{'
                
                # Generar código del bloque if
                bloque_if = []
                while i < len(tokens) and tokens[i].lexema != "}":
                    bloque_if.append(tokens[i])
                    i += 1
                self.generar_intermedio(bloque_if)
                
                self.codigo_intermedio.append(f"GOTO {label_end}")
                self.codigo_intermedio.append(f"LABEL {label_else}")
                
                # Procesar else si existe
                if i+1 < len(tokens) and tokens[i+1].lexema == "else":
                    i += 3  # Saltar '}' 'else' '{'
                    bloque_else = []
                    while i < len(tokens) and tokens[i].lexema != "}":
                        bloque_else.append(tokens[i])
                        i += 1
                    self.generar_intermedio(bloque_else)
                
                self.codigo_intermedio.append(f"LABEL {label_end}")
            
            i += 1
        
        return self.codigo_intermedio
    
    def procesar_expresion(self, tokens):
        if not tokens:
            return ""
        
        # Caso simple: constante o variable
        if len(tokens) == 1 and tokens[0].tipo in ["IDENTIFICADOR", "CONSTANTE_NUM", "CONSTANTE_STR"]:
            return tokens[0].lexema
        
        # Buscar operadores en orden de precedencia
        for op_types in [["OP_MULTIPLICACION", "OP_DIVISION"], ["OP_ADICION", "OP_SUSTRACCION"], ["OP_RELACIONAL"], ["OP_LOGICO"]]:
            for i, token in enumerate(tokens):
                if token.tipo in op_types:
                    left = self.procesar_expresion(tokens[:i])
                    right = self.procesar_expresion(tokens[i+1:])
                    temp = self.nueva_temp()
                    self.codigo_intermedio.append(f"{temp} = {left} {token.lexema} {right}")
                    return temp
        
        # Expresión entre paréntesis
        if tokens[0].lexema == "(" and tokens[-1].lexema == ")":
            return self.procesar_expresion(tokens[1:-1])
        
        return tokens[0].lexema

""" ------------------------- GENERADOR DE ENSAMBLADOR (x86 básico) ------------------------- """

class GeneradorEnsamblador:
    def __init__(self):
        self.codigo_asm = []
        self.var_types = {}
        self.var_memory = {}
        self.memory_offset = 0
        self.label_count = 0
        
    def nuevo_label(self):
        label = f"label_{self.label_count}"
        self.label_count += 1
        return label
    
    def generar_ensamblador(self, codigo_intermedio):
        self.codigo_asm.append("section .data")
        self.codigo_asm.append("; Variables declaradas aquí")
        self.codigo_asm.append("\nsection .text")
        self.codigo_asm.append("global _start")
        self.codigo_asm.append("\n_start:")
        
        for instruccion in codigo_intermedio:
            if instruccion.startswith("STORE"):
                # STORE valor -> variable
                parts = instruccion.split()
                value = parts[1]
                var = parts[3]
                
                if var not in self.var_memory:
                    self.var_memory[var] = self.memory_offset
                    self.memory_offset += 4
                    self.codigo_asm.append(f"; Reservar espacio para {var}")
                
                if value.isdigit():
                    self.codigo_asm.append(f"mov eax, {value}")
                else:
                    self.codigo_asm.append(f"mov eax, [{value}]")
                self.codigo_asm.append(f"mov [var_{var}], eax")
            
            elif instruccion.startswith("IF_NOT"):
                # IF_NOT cond GOTO label
                parts = instruccion.split()
                cond = parts[1]
                label = parts[3]
                
                self.codigo_asm.append(f"mov eax, [{cond}]")
                self.codigo_asm.append("cmp eax, 0")
                self.codigo_asm.append(f"je {label}")
            
            elif instruccion.startswith("GOTO"):
                label = instruccion.split()[1]
                self.codigo_asm.append(f"jmp {label}")
            
            elif instruccion.startswith("LABEL"):
                label = instruccion.split()[1]
                self.codigo_asm.append(f"{label}:")
            
            elif "=" in instruccion and ("+" in instruccion or "-" in instruccion or "*" in instruccion or "/" in instruccion):
                # t1 = a + b
                temp, expr = instruccion.split(" = ")
                op1, op, op2 = expr.split()
                
                self.codigo_asm.append(f"mov eax, [{op1}]")
                
                if op == "+":
                    self.codigo_asm.append(f"add eax, [{op2}]")
                elif op == "-":
                    self.codigo_asm.append(f"sub eax, [{op2}]")
                elif op == "*":
                    self.codigo_asm.append(f"imul eax, [{op2}]")
                elif op == "/":
                    self.codigo_asm.append("cdq")
                    self.codigo_asm.append(f"idiv dword [{op2}]")
                
                self.codigo_asm.append(f"mov [{temp}], eax")
        
        # Agregar terminación del programa
        self.codigo_asm.append("\n; Terminar programa")
        self.codigo_asm.append("mov eax, 1")
        self.codigo_asm.append("xor ebx, ebx")
        self.codigo_asm.append("int 0x80")
        
        # Agregar declaración de variables al inicio
        var_decls = ["\nsection .bss"]
        for var, offset in self.var_memory.items():
            var_decls.append(f"var_{var} resd 1")
        
        self.codigo_asm = var_decls + self.codigo_asm
        
        return "\n".join(self.codigo_asm)

# ------------------------- FLUJO PRINCIPAL -------------------------
def traducir_a_ensamblador(codigo_fuente):
    # 1. Análisis léxico/sintáctico/semántico
    tokens, _ = analizar_lexico(codigo_fuente)
    errores_semanticos = analizar_semantica(tokens)
    
    if errores_semanticos:
        print("Errores semánticos encontrados:")
        for error in errores_semanticos:
            print(error)
        return None, None
    
    # 2. Generación de código intermedio
    generador_intermedio = GeneradorCodigoIntermedio()
    codigo_intermedio = generador_intermedio.generar_intermedio(tokens)
    
    # 3. Generación de ensamblador
    generador_asm = GeneradorEnsamblador()
    generador_asm.var_types = generador_intermedio.var_types
    codigo_asm = generador_asm.generar_ensamblador(codigo_intermedio)
    
    return codigo_intermedio, codigo_asm

# ------------------------- EJEMPLO DE USO -------------------------
codigo_fuente = """
int x = 10;
int y = 5;
int z;

if (x > y) {
    z = x + y;
} else {
    z = x - y;
}
"""

codigo_intermedio, codigo_asm = traducir_a_ensamblador(codigo_fuente)

print("\nCódigo Intermedio Generado:")
for instruccion in codigo_intermedio:
    print(instruccion)

print("\nCódigo Ensamblador Generado:")
print(codigo_asm)

# Para generar un ejecutable, necesitarías:
# 1. Guardar el código ensamblador en un archivo .asm
# 2. Ensamblarlo con NASM: nasm -f elf32 programa.asm
# 3. Enlazarlo con ld: ld -m elf_i386 -s -o programa programa.o